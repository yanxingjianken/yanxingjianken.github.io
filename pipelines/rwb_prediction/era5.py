"""ERA5 (ERA5T near real time) hourly u, v, T on the pipeline's pressure levels, 0-90 N on a 1-degree grid, from the
Copernicus Climate Data Store (dataset reanalysis-era5-pressure-levels). Needs a personal access token of the ECMWF
data stores (~/.cdsapirc, or CDSAPI_KEY holding the token or the text of such a file)."""
from __future__ import annotations

import os
from datetime import date

import numpy as np

from config import GRID_DEG, LEVELS_HPA

VARS = {"u": "u_component_of_wind", "v": "v_component_of_wind", "t": "temperature"}
CDS_URL = "https://cds.climate.copernicus.eu/api"          # ERA5 is served by the Climate Data Store only


def credentials():
    """(url, key) for the Climate Data Store from CDSAPI_KEY, which may hold the key itself or the whole text of an
    API configuration file ('url: ...' and 'key: ...' lines, for any ECMWF data store: the personal access token is
    the same for all of them). (None, None) when unset, so that cdsapi reads ~/.cdsapirc."""
    raw = (os.environ.get("CDSAPI_KEY") or "").strip()
    if not raw:
        return None, None
    key = raw
    for line in raw.splitlines():
        if line.strip().lower().startswith("key:"):
            key = line.split(":", 1)[1].strip()
    return CDS_URL, key


class Incomplete(Exception):
    """The Climate Data Store does not yet hold all 24 hours of the day."""


def fetch_day(day: date, path: str) -> str:
    """Download one UTC day (24 hourly fields) to a netCDF file; returns the path (skips an existing file). A day
    that ERA5T has not completed yet raises Incomplete (the partial file is removed)."""
    if os.path.exists(path):
        return path
    import cdsapi
    url, key = credentials()
    c = cdsapi.Client(url=url, key=key, quiet=True, progress=False) if key else cdsapi.Client(quiet=True, progress=False)
    tmp = path + ".part"
    c.retrieve("reanalysis-era5-pressure-levels", {
        "product_type": ["reanalysis"], "variable": list(VARS.values()),
        "year": [f"{day:%Y}"], "month": [f"{day:%m}"], "day": [f"{day:%d}"],
        "time": [f"{h:02d}:00" for h in range(24)], "pressure_level": [str(p) for p in LEVELS_HPA],
        "data_format": "netcdf", "download_format": "unarchived",
        "area": [90, -180, 0, 180], "grid": [GRID_DEG, GRID_DEG]}, tmp)
    import xarray as xr
    with xr.open_dataset(tmp) as ds:
        n = ds.sizes.get("valid_time", 0)
    if n < 24:
        os.remove(tmp)
        raise Incomplete(f"{day}: {n} of 24 hours")
    os.replace(tmp, path)
    return path


def read_day(path: str):
    """(times [datetime64, 24], fields {u, v, t: float32 (24, L, 91, 360)}) with latitude ascending 0..90 and
    longitude 0..359, levels in LEVELS_HPA order."""
    import xarray as xr
    with xr.open_dataset(path) as ds:
        ds = ds.sortby("latitude")
        ds = ds.assign_coords(longitude=(ds.longitude % 360)).sortby("longitude")
        ds = ds.sel(pressure_level=list(LEVELS_HPA))
        assert np.allclose(ds.latitude.values, np.arange(0, 90.01, GRID_DEG))
        assert np.allclose(ds.longitude.values, np.arange(0, 360, GRID_DEG))
        times = ds.valid_time.values
        out = {k: ds[k].values.astype(np.float32) for k in VARS}
    assert len(times) == 24, f"{path}: {len(times)} times"
    return times, out
