"""Download GFS 0.25° pressure-level fields for the Northern Hemisphere.

Primary source: AWS Open Data bucket noaa-gfs-bdp-pds, using the .idx file to
fetch only the 18 GRIB messages we need by HTTP byte range (no throttling).
Fallback: NOMADS grib-filter CGI, which subsets server-side.

Returns xarray datasets with variables gh,t,u,v,w,q on (isobaricInhPa, latitude,
longitude), latitude ascending, longitude 0..359.75.
"""
from __future__ import annotations

import concurrent.futures as cf
import io
import os
import re
import time
from datetime import datetime, timedelta, timezone

import numpy as np
import requests
import xarray as xr

AWS = "https://noaa-gfs-bdp-pds.s3.amazonaws.com"
NOMADS_FILTER = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
NOMADS_PROD = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod"

WANT = re.compile(r":(UGRD|VGRD|TMP|HGT|VVEL|SPFH):(850|500|250) mb:")
SESSION = requests.Session()
SESSION.headers["User-Agent"] = "nh-forecast-pipeline (github.com/yanxingjianken)"


def run_id(dt: datetime) -> str:
    return dt.strftime("%Y%m%d%H")


def aws_key(init: datetime, step: int) -> str:
    return f"gfs.{init:%Y%m%d}/{init:%H}/atmos/gfs.t{init:%H}z.pgrb2.0p25.f{step:03d}"


def aws_exists(init: datetime, step: int) -> bool:
    r = SESSION.head(f"{AWS}/{aws_key(init, step)}.idx", timeout=30)
    return r.status_code == 200


def latest_complete_run(now: datetime | None = None, max_step: int = 240,
                        lookback_runs: int = 6) -> datetime:
    """Most recent synoptic run whose f{max_step} file is already on AWS."""
    now = now or datetime.now(timezone.utc)
    cand = now.replace(minute=0, second=0, microsecond=0)
    cand = cand.replace(hour=(cand.hour // 6) * 6)
    for _ in range(lookback_runs):
        if aws_exists(cand, max_step):
            return cand
        cand -= timedelta(hours=6)
    raise RuntimeError("no complete GFS run found on AWS in the look-back window")


def _get(url: str, headers=None, tries: int = 4, timeout: int = 120) -> bytes:
    last = None
    for k in range(tries):
        try:
            r = SESSION.get(url, headers=headers, timeout=timeout)
            if r.status_code in (200, 206):
                return r.content
            last = RuntimeError(f"HTTP {r.status_code} for {url}")
        except requests.RequestException as e:  # pragma: no cover
            last = e
        time.sleep(2 * (k + 1))
    raise last


def fetch_aws_subset(init: datetime, step: int) -> bytes:
    """Concatenate the wanted GRIB2 messages using byte ranges from the .idx."""
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
        hdr = {"Range": f"bytes={s}-{e}" if e is not None else f"bytes={s}-"}
        return _get(f"{AWS}/{key}", headers=hdr)

    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        chunks = list(ex.map(one, ranges))
    return b"".join(chunks)


def fetch_nomads_subset(init: datetime, step: int) -> bytes:
    params = {
        "dir": f"/gfs.{init:%Y%m%d}/{init:%H}/atmos",
        "file": f"gfs.t{init:%H}z.pgrb2.0p25.f{step:03d}",
        "var_HGT": "on", "var_TMP": "on", "var_UGRD": "on", "var_VGRD": "on",
        "var_VVEL": "on", "var_SPFH": "on",
        "lev_850_mb": "on", "lev_500_mb": "on", "lev_250_mb": "on",
        "subregion": "", "toplat": "90", "leftlon": "0", "rightlon": "360", "bottomlat": "0",
    }
    r = SESSION.get(NOMADS_FILTER, params=params, timeout=300)
    if r.status_code != 200 or not r.content.startswith(b"GRIB"):
        raise RuntimeError(f"NOMADS filter failed: HTTP {r.status_code}")
    return r.content


def fetch_subset(init: datetime, step: int, cache_dir: str | None = None) -> bytes:
    """GRIB2 bytes with the 18 wanted messages, from cache, AWS, or NOMADS."""
    path = None
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        path = os.path.join(cache_dir, f"gfs.{run_id(init)}.f{step:03d}.grib2")
        if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
            with open(path, "rb") as f:
                return f.read()
    try:
        data = fetch_aws_subset(init, step)
    except Exception as e:  # pragma: no cover
        print(f"  AWS failed ({e}); trying NOMADS filter")
        data = fetch_nomads_subset(init, step)
    if path:
        with open(path, "wb") as f:
            f.write(data)
    return data


def open_grib(data: bytes) -> xr.Dataset:
    """Decode the GRIB bytes with cfgrib and normalise the grid to NH, ascending."""
    tmp = f"/tmp/nh_tmp_{os.getpid()}_{time.time_ns()}.grib2"
    with open(tmp, "wb") as f:
        f.write(data)
    try:
        ds = xr.open_dataset(tmp, engine="cfgrib", backend_kwargs={"indexpath": ""})
        ds = ds.load()
    finally:
        os.remove(tmp)
    if float(ds.latitude[0]) > float(ds.latitude[-1]):
        ds = ds.isel(latitude=slice(None, None, -1))
    ds = ds.sel(latitude=slice(0, 90))
    if float(ds.longitude.min()) < 0:
        ds = ds.assign_coords(longitude=(ds.longitude % 360)).sortby("longitude")
    missing = [v for v in ("gh", "t", "u", "v", "w", "q") if v not in ds]
    if missing:
        raise RuntimeError(f"variables missing after decode: {missing}")
    return ds
