"""NOAA GFS 0.25 deg: pressure-level fields from the AWS Open Data bucket (byte
ranges via the .idx files), NOMADS grib filter as fallback."""
from __future__ import annotations

import concurrent.futures as cf
import os
import re
import time
from datetime import datetime, timedelta, timezone

import requests

from gribio import read_fields

MODEL_ID = "gfs"
LABEL = "GFS 0.25° (NCEP)"
SOURCE = "NOAA GFS 0.25 deg, NOAA Open Data Dissemination (noaa-gfs-bdp-pds) / NOMADS"
STEP_HOURS = 6
MAX_STEP = 240
AWS = "https://noaa-gfs-bdp-pds.s3.amazonaws.com"
NOMADS_FILTER = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
WANT = re.compile(r":(UGRD|VGRD|TMP|HGT|VVEL|SPFH):(850|500|250) mb:")
SESSION = requests.Session()
SESSION.headers["User-Agent"] = "nh-forecast-pipeline (github.com/yanxingjianken)"


def run_id(dt: datetime) -> str:
    return dt.strftime("%Y%m%d%H")


def aws_key(init: datetime, step: int) -> str:
    return f"gfs.{init:%Y%m%d}/{init:%H}/atmos/gfs.t{init:%H}z.pgrb2.0p25.f{step:03d}"


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


def latest_complete_run(now=None, max_step=MAX_STEP, lookback_runs=6) -> datetime:
    now = now or datetime.now(timezone.utc)
    cand = now.replace(minute=0, second=0, microsecond=0)
    cand = cand.replace(hour=(cand.hour // 6) * 6)
    for _ in range(lookback_runs):
        r = SESSION.head(f"{AWS}/{aws_key(cand, max_step)}.idx", timeout=30)
        if r.status_code == 200:
            return cand
        cand -= timedelta(hours=6)
    raise RuntimeError("no complete GFS run found on AWS in the look-back window")


def _fetch_aws(init, step) -> bytes:
    key = aws_key(init, step)
    idx = _get(f"{AWS}/{key}.idx").decode("utf-8", "replace").splitlines()
    recs = []
    for i, line in enumerate(idx):
        parts = line.split(":")
        if len(parts) < 6:
            continue
        start = int(parts[1])
        end = int(idx[i + 1].split(":")[1]) - 1 if i + 1 < len(idx) else None
        recs.append((line, start, end))
    ranges = [(s, e) for (line, s, e) in recs if WANT.search(line)]
    if len(ranges) != 18:
        raise RuntimeError(f"expected 18 records in {key}.idx, found {len(ranges)}")

    def one(rng):
        s, e = rng
        return _get(f"{AWS}/{key}", headers={"Range": f"bytes={s}-{e}" if e is not None else f"bytes={s}-"})

    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        return b"".join(ex.map(one, ranges))


def _fetch_nomads(init, step) -> bytes:
    params = {"dir": f"/gfs.{init:%Y%m%d}/{init:%H}/atmos", "file": f"gfs.t{init:%H}z.pgrb2.0p25.f{step:03d}",
              "var_HGT": "on", "var_TMP": "on", "var_UGRD": "on", "var_VGRD": "on", "var_VVEL": "on", "var_SPFH": "on",
              "lev_850_mb": "on", "lev_500_mb": "on", "lev_250_mb": "on",
              "subregion": "", "toplat": "90", "leftlon": "0", "rightlon": "360", "bottomlat": "0"}
    r = SESSION.get(NOMADS_FILTER, params=params, timeout=300)
    if r.status_code != 200 or not r.content.startswith(b"GRIB"):
        raise RuntimeError(f"NOMADS filter failed: HTTP {r.status_code}")
    return r.content


def fetch_fields(init: datetime, step: int, cache_dir: str | None = None) -> dict:
    """{(var, level): array(361, 1440)} on the 0.25 deg NH grid."""
    path = None
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        path = os.path.join(cache_dir, f"gfs.{run_id(init)}.f{step:03d}.grib2")
        if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
            with open(path, "rb") as f:
                return _check(read_fields(f.read()))
    try:
        data = _fetch_aws(init, step)
    except Exception as e:
        print(f"  AWS failed ({e}); trying NOMADS filter", flush=True)
        data = _fetch_nomads(init, step)
    if path:
        with open(path, "wb") as f:
            f.write(data)
    return _check(read_fields(data))


def _check(fields):
    if len(fields) != 18:
        raise RuntimeError(f"decoded {len(fields)} of 18 fields: {sorted(fields)}")
    return fields
