"""ECCC GDPS (GEM global, 15 km): pressure-level and surface fields from the MSC Datamart, one file per
variable on a 0.15 deg latitude-longitude grid, interpolated bilinearly to the pipeline's 0.25 deg grid.
Cycles 00 and 12 UTC to 240 h.  Licence: Environment and Climate Change Canada Data Server End-use
Licence (attribution required)."""
from __future__ import annotations

import concurrent.futures as cf
import os
import time
from datetime import datetime, timedelta, timezone

import numpy as np
import requests
from scipy import ndimage

from gribio import check_fields, split_messages

MODEL_ID = "gdps"
LABEL = "GDPS 15 km (ECCC)"
SOURCE = "ECCC GDPS (GEM global 15 km), MSC Datamart; contains information licensed under the Data Server End-use Licence of Environment and Climate Change Canada"
STEP_HOURS = 6
MAX_STEP = 240
CYCLES = (0, 12)
TP_TO_MM = 1.0
ROOT = "https://dd.weather.gc.ca"
PL_FILES = {"z": "GeopotentialHeight", "t": "AirTemp", "u": "WindU", "v": "WindV", "w": "VerticalVelocity", "q": "SpecificHumidity"}
SFC_FILES = {"t2m": "AirTemp_AGL-2m", "d2m": "DewPoint_AGL-2m", "u10": "WindU_AGL-10m", "v10": "WindV_AGL-10m", "msl": "Pressure_MSL"}
SESSION = requests.Session()
SESSION.headers["User-Agent"] = "nh-forecast-pipeline (github.com/yanxingjianken)"


def run_id(dt):
    return dt.strftime("%Y%m%d%H")


def _url(init, step, name):
    return (f"{ROOT}/{init:%Y%m%d}/WXO-DD/model_gdps/15km/{init:%H}/{step:03d}/"
            f"{init:%Y%m%dT%H}Z_MSC_GDPS_{name}_LatLon0.15_PT{step:03d}H.grib2")


def _get(url, tries=4, timeout=120):
    last = None
    for k in range(tries):
        try:
            r = SESSION.get(url, timeout=timeout)
            if r.status_code == 200 and r.content[:4] == b"GRIB":
                return r.content
            last = RuntimeError(f"HTTP {r.status_code} for {url}")
            if r.status_code == 404:
                break
        except requests.RequestException as e:
            last = e
        time.sleep(2 * (k + 1))
    raise last


def latest_complete_run(now=None, max_step=MAX_STEP, lookback_runs=6):
    now = now or datetime.now(timezone.utc)
    cand = now.replace(minute=0, second=0, microsecond=0)
    cand = cand.replace(hour=(cand.hour // 12) * 12)
    for _ in range(lookback_runs):
        if SESSION.head(_url(cand, max_step, "AirTemp_IsbL-0500"), timeout=30).status_code == 200:
            return cand
        cand -= timedelta(hours=12)
    raise RuntimeError("no complete GDPS run found on the Datamart")


_IDX = {}


def _to_nh025(vals, lat1, dlat, lon1, dlon):
    """Bilinear interpolation of a global regular grid (rows south->north) to 0..90N x 0..359.75E at 0.25 deg."""
    key = (vals.shape, lat1, dlat, lon1, dlon)
    if key not in _IDX:
        lats = np.arange(361) * 0.25; lons = np.arange(1440) * 0.25
        LA, LO = np.meshgrid(lats, lons, indexing="ij")
        _IDX[key] = [(LA - lat1) / dlat, ((LO - lon1) % 360.0) / dlon]
    ext = np.concatenate([vals, vals[:, :1]], axis=1)          # periodic in longitude
    return ndimage.map_coordinates(ext, _IDX[key], order=1, mode="nearest", prefilter=False).astype(np.float32)


def _decode(data):
    import eccodes
    h = eccodes.codes_new_from_message(next(split_messages(data)))
    try:
        g = lambda k: eccodes.codes_get(h, k)
        ni, nj = int(g("Ni")), int(g("Nj"))
        vals = np.asarray(eccodes.codes_get_values(h), dtype=np.float32).reshape(nj, ni)
        lat1, dlat = float(g("latitudeOfFirstGridPointInDegrees")), float(g("jDirectionIncrementInDegrees"))
        if not int(g("jScansPositively")):
            vals = vals[::-1]; lat1 = lat1 - dlat * (nj - 1)
        return _to_nh025(vals, lat1, dlat, float(g("longitudeOfFirstGridPointInDegrees")) % 360.0, float(g("iDirectionIncrementInDegrees")))
    finally:
        eccodes.codes_release(h)


def fetch_fields(init, step, cache_dir=None):
    jobs = {}
    for v, name in PL_FILES.items():
        for lev in (850, 500, 250):
            jobs[(v, lev)] = f"{name}_IsbL-{lev:04d}"
    for v, name in SFC_FILES.items():
        jobs[(v, "sfc")] = name
    if step > 0:
        jobs[("tp", f"{step - 6}-{step}")] = "Precip-Accum6h_Sfc"   # 6-h amount in kg m-2 (decodes as 'unknown')

    def one(item):
        key, name = item
        path = os.path.join(cache_dir, f"gdps.{run_id(init)}.f{step:03d}.{name}.grib2") if cache_dir else None
        if path and os.path.exists(path):
            data = open(path, "rb").read()
        else:
            data = _get(_url(init, step, name))
            if path:
                os.makedirs(cache_dir, exist_ok=True); open(path, "wb").write(data)
        return key, _decode(data)

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        out = dict(ex.map(one, jobs.items()))
    return check_fields(out)
