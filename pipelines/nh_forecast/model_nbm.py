"""NOAA National Blend of Models 2.5 km (CONUS core): surface fields only (2-m temperature and
dew point, 10-m wind speed and direction, 6-h precipitation; NBM has no sea-level pressure and
no pressure levels), regridded to the 0.05 deg US grid.  Cycles 00/06/12/18 UTC, steps 6-72 h."""
from __future__ import annotations

import concurrent.futures as cf
import os
import re
import time
from datetime import datetime, timedelta, timezone

import requests

from regional import REG_GRID, read_lambert_fields

MODEL_ID = "nbm"
LABEL = "NBM 2.5 km (NOAA)"
SOURCE = "NOAA National Blend of Models v4 2.5 km, NOAA Open Data Dissemination (noaa-nbm-grib2-pds), regridded to 0.05 deg"
REGIONAL = True
SURFACE_ONLY = True
GRID = REG_GRID
GRID_NOTE = "NBM fields interpolated bilinearly from the 2.5-km Lambert-conformal grid to a 0.05° latitude–longitude grid"
STEP_HOURS = 6
MAX_STEP = 72
FIRST_STEP = 6          # NBM files start at f001; we keep 6-hourly steps from f006
TP_TO_MM = 1.0
AWS = "https://noaa-nbm-grib2-pds.s3.amazonaws.com"
SESSION = requests.Session()
SESSION.headers["User-Agent"] = "nh-forecast-pipeline (github.com/yanxingjianken)"


def run_id(dt):
    return dt.strftime("%Y%m%d%H")


def _key(init, step):
    return f"blend.{init:%Y%m%d}/{init:%H}/core/blend.t{init:%H}z.core.f{step:03d}.co.grib2"


def _get(url, headers=None, tries=4, timeout=120):
    last = None
    for k in range(tries):
        try:
            r = SESSION.get(url, headers=headers, timeout=timeout)
            if r.status_code in (200, 206):
                return r.content
            last = RuntimeError(f"HTTP {r.status_code} for {url}")
        except requests.RequestException as e:
            last = e
        time.sleep(2 * (k + 1))
    raise last


def latest_complete_run(now=None, max_step=MAX_STEP, lookback_runs=6):
    now = now or datetime.now(timezone.utc)
    cand = now.replace(minute=0, second=0, microsecond=0)
    cand = cand.replace(hour=(cand.hour // 6) * 6)
    for _ in range(lookback_runs):
        if SESSION.head(f"{AWS}/{_key(cand, max_step)}.idx", timeout=30).status_code == 200:
            return cand
        cand -= timedelta(hours=6)
    raise RuntimeError("no complete NBM run found")


def fetch_fields(init, step, cache_dir=None):
    path = None
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        path = os.path.join(cache_dir, f"nbm.{run_id(init)}.f{step:03d}.grib2")
        if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
            return _check(read_lambert_fields(open(path, "rb").read()))
    key = _key(init, step)
    idx = _get(f"{AWS}/{key}.idx").decode("utf-8", "replace").splitlines()
    # deterministic records only (no "ens std dev" or probability variants): the line ends right after "fcst:"
    want = re.compile(r":(TMP|DPT):2 m above ground:\d+ hour fcst:$|:(WIND|WDIR):10 m above ground:\d+ hour fcst:$"
                      + rf"|:APCP:surface:{step - 6}-{step} hour acc fcst:$")
    ranges = []
    for i, line in enumerate(idx):
        parts = line.split(":")
        if len(parts) < 6 or not want.search(line):
            continue
        end = int(idx[i + 1].split(":")[1]) - 1 if i + 1 < len(idx) else None
        ranges.append((int(parts[1]), end))
    if len(ranges) < 5:
        raise RuntimeError(f"expected 5 records in {key}.idx, found {len(ranges)}")

    def one(rng):
        s, e = rng
        return _get(f"{AWS}/{key}", headers={"Range": f"bytes={s}-{e}" if e is not None else f"bytes={s}-"})

    with cf.ThreadPoolExecutor(max_workers=5) as ex:
        data = b"".join(ex.map(one, ranges))
    if path:
        open(path, "wb").write(data)
    return _check(read_lambert_fields(data))


def _check(f):
    missing = [v for v in ("t2m", "d2m", "u10", "v10") if (v, "sfc") not in f]
    if missing:
        raise RuntimeError(f"NBM fields missing: {missing}")
    return f
