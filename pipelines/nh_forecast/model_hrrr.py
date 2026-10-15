"""NOAA HRRR 3 km (CONUS): pressure-level and surface fields from the AWS Open Data bucket via
.idx byte ranges, regridded to the 0.05 deg US grid (regional.REG_GRID).  Synoptic cycles
(00/06/12/18 UTC) run to 48 h; we keep 6-hourly steps."""
from __future__ import annotations

import concurrent.futures as cf
import os
import re
import time
from datetime import datetime, timedelta, timezone

import requests

from gribio import check_fields
from regional import REG_GRID, read_lambert_fields

MODEL_ID = "hrrr"
LABEL = "HRRR 3 km (NOAA)"
SOURCE = "NOAA HRRR 3 km, NOAA Open Data Dissemination (noaa-hrrr-bdp-pds), regridded to 0.05 deg"
REGIONAL = True
GRID = REG_GRID
GRID_NOTE = "HRRR fields interpolated bilinearly from the 3-km Lambert-conformal grid to a 0.05° latitude–longitude grid"
STEP_HOURS = 6
MAX_STEP = 48
TP_TO_MM = 1.0
AWS = "https://noaa-hrrr-bdp-pds.s3.amazonaws.com"
WANT = re.compile(r":(UGRD|VGRD|TMP|HGT|VVEL|SPFH):(850|500|250) mb:|:(TMP|DPT):2 m above ground:|:(UGRD|VGRD):10 m above ground:|:MSLMA:mean sea level:")
SESSION = requests.Session()
SESSION.headers["User-Agent"] = "nh-forecast-pipeline (github.com/yanxingjianken)"


def run_id(dt):
    return dt.strftime("%Y%m%d%H")


def _key(init, step):
    return f"hrrr.{init:%Y%m%d}/conus/hrrr.t{init:%H}z.wrfprsf{step:02d}.grib2"


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
    raise RuntimeError("no complete HRRR run found")


def fetch_fields(init, step, cache_dir=None):
    path = None
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        path = os.path.join(cache_dir, f"hrrr.{run_id(init)}.f{step:02d}.grib2")
        if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
            return check_fields(read_lambert_fields(open(path, "rb").read()))
    key = _key(init, step)
    idx = _get(f"{AWS}/{key}.idx").decode("utf-8", "replace").splitlines()
    recs = []
    for i, line in enumerate(idx):
        parts = line.split(":")
        if len(parts) < 6:
            continue
        end = int(idx[i + 1].split(":")[1]) - 1 if i + 1 < len(idx) else None
        recs.append((line, int(parts[1]), end))
    ranges = [(s, e) for (line, s, e) in recs if WANT.search(line)]
    if step > 0:   # run-total precipitation; the 6-h amount is differenced in gribio.derive_surface
        ranges += [(s, e) for (line, s, e) in recs if f":APCP:surface:0-{step} hour acc fcst:" in line][:1]
    if len(ranges) < 23:
        raise RuntimeError(f"expected 23+ records in {key}.idx, found {len(ranges)}")

    def one(rng):
        s, e = rng
        return _get(f"{AWS}/{key}", headers={"Range": f"bytes={s}-{e}" if e is not None else f"bytes={s}-"})

    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        data = b"".join(ex.map(one, ranges))
    if path:
        open(path, "wb").write(data)
    return check_fields(read_lambert_fields(data))
