"""Convert ETOPO 2022 subsets (NetCDF from NOAA NCEI's THREDDS subset service) into
the compact uint16 container used by the site's map pages.

    python build_elevation.py elev_nh.nc    ../../assets/data/elev_nh_0p25.u16.gz
    python build_elevation.py elev_conus.nc ../../assets/data/elev_conus_0p05.u16.gz

Source (one-off downloads, CC0 / public domain):
  https://www.ngdc.noaa.gov/thredds/ncss/grid/global/ETOPO2022/60s/60s_surface_elev_netcdf/
      ETOPO_2022_v1_60s_N90W180_surface.nc?var=z&north=89.9&south=0&west=-180&east=179.9&horizStride=15
  ...?var=z&north=55.91&south=19.01&west=-130.99&east=-59.01&horizStride=3
Ocean cells (z < 0) are stored as missing; heights are metres above sea level.
NOAA National Centers for Environmental Information. 2022: ETOPO 2022 15 Arc-Second Global
Relief Model. doi:10.25921/fd45-gt74.
"""
from __future__ import annotations

import gzip
import json
import sys

import numpy as np
import xarray as xr


def main(src, dst):
    ds = xr.open_dataset(src)
    z = ds["z"]
    lat = ds["lat"].values.astype(float)
    lon = ds["lon"].values.astype(float) % 360.0
    if lat[0] > lat[-1]:
        z = z.isel(lat=slice(None, None, -1)); lat = lat[::-1]
    arr = z.values.astype(np.float32)
    # drop a duplicated wrap column (e.g. -180 and 180 both present)
    if len(lon) > 1 and abs((lon[-1] - lon[0]) % 360.0) < 1e-6:
        arr = arr[:, :-1]; lon = lon[:-1]
    # make longitude start at its minimum in 0..360 order (roll if the subset wraps)
    order = np.argsort(lon)
    lon = lon[order]; arr = arr[:, order]
    dlat = float(np.round(np.median(np.diff(lat)), 6)); dlon = float(np.round(np.median(np.diff(lon)), 6))
    arr = np.where(arr < 0, np.nan, arr)
    ny, nx = arr.shape
    finite = np.isfinite(arr)
    vmin, vmax = 0.0, float(np.nanmax(arr))
    scale = max(vmax, 1.0) / 65000.0
    q = np.full(arr.shape, 65535, dtype=np.uint16)
    q[finite] = np.round((arr[finite] - vmin) / scale).astype(np.uint16)
    hdr = {"var": "elev", "units": "m", "source": "NOAA NCEI ETOPO 2022 (60 arc-second surface), subset via THREDDS NCSS",
           "ny": ny, "nx": nx, "lat0": round(float(lat[0]), 5), "dlat": dlat, "lon0": round(float(lon[0]), 5), "dlon": dlon,
           "offset": vmin, "scale": scale, "vmin": vmin, "vmax": vmax, "missing": 65535, "dtype": "uint16le",
           "order": "row-major, lat ascending, lon ascending", "note": "ocean (z<0) stored as missing"}
    htxt = json.dumps(hdr, separators=(",", ":"))
    if len(htxt.encode()) % 2 == 0:
        htxt += " "
    with open(dst, "wb") as f:
        f.write(gzip.compress(htxt.encode() + b"\n" + q.astype("<u2").tobytes(), 9))
    print(f"{dst}: {ny}x{nx}, lat {lat[0]:.3f}..{lat[-1]:.3f} step {dlat}, lon {lon[0]:.3f}..{lon[-1]:.3f} step {dlon}, max {vmax:.0f} m")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
