"""Z500 daily climatology (NCEP/NCAR Reanalysis 1, 1991-2020 long-term mean,
2.5 deg).  build_z500_ltm() is run once locally to produce the compact file
data/z500_ltm_1991-2020_2p5.npz (also published to the dataset as JSON.gz);
load_z500_ltm() / clim_on_grid() are used by the 6-hourly pipeline."""
from __future__ import annotations

import gzip
import json
import os
from datetime import datetime

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NPZ = os.path.join(HERE, "data", "z500_ltm_1991-2020_2p5.npz")
SRC_URL = ("https://psl.noaa.gov/thredds/fileServer/Datasets/ncep.reanalysis.derived/"
           "pressure/hgt.day.ltm.1991-2020.nc")


def build_z500_ltm(src_nc: str, out_npz: str = NPZ, out_u16_gz: str | None = None):
    """Extract the 500-hPa daily long-term mean (0-90N) from the PSL file.
    Writes the compact .npz used by the pipeline and, optionally, the browser
    file (same uint16 container as the fields, with nt = number of days)."""
    import xarray as xr
    from common import encode_field
    ds = xr.open_dataset(src_nc, decode_times=False)
    z = ds["hgt"].sel(level=500)
    if float(z["lat"][0]) > float(z["lat"][-1]):
        z = z.isel(lat=slice(None, None, -1))
    z = z.sel(lat=slice(0, 90))
    lat = z["lat"].values.astype(np.float32)
    lon = z["lon"].values.astype(np.float32)
    arr = z.values.astype(np.float32)          # (nday, ny, nx)
    if not np.isfinite(arr).all() or arr.max() < 1000:
        raise RuntimeError("climatology values look wrong (missing or zero)")
    os.makedirs(os.path.dirname(out_npz), exist_ok=True)
    np.savez_compressed(out_npz, z=arr, lat=lat, lon=lon, source=np.array(SRC_URL))
    if out_u16_gz:
        nt, ny, nx = arr.shape
        hdr = {"var": "z500_ltm", "level": 500, "units": "gpm", "period": "1991-2020",
               "source": SRC_URL, "nt": nt, "lat0": float(lat[0]), "dlat": float(lat[1] - lat[0]),
               "lon0": float(lon[0]), "dlon": float(lon[1] - lon[0])}
        blob = encode_field(arr.reshape(nt * ny, nx), hdr)
        # patch ny back to the per-day row count (encode_field wrote nt*ny)
        import gzip, json
        raw = gzip.decompress(blob)
        nl = raw.index(b"\n")
        h = json.loads(raw[:nl]); h["ny"] = ny; h["nt"] = nt
        htxt = json.dumps(h, separators=(",", ":"))
        if len(htxt.encode()) % 2 == 0:
            htxt += " "
        with open(out_u16_gz, "wb") as f:
            f.write(gzip.compress(htxt.encode() + b"\n" + raw[nl + 1:], 6))
    return out_npz


def load_z500_ltm(npz: str = NPZ):
    d = np.load(npz)
    return d["z"], d["lat"], d["lon"]


def clim_on_grid(when: datetime, lats: np.ndarray, lons: np.ndarray, ltm=None) -> np.ndarray:
    """Bilinear interpolation of the day-of-year climatology to (lats, lons).
    lons may be 0..360; lats ascending."""
    from scipy.interpolate import RegularGridInterpolator
    z, clat, clon = ltm if ltm is not None else load_z500_ltm()
    doy = min(when.timetuple().tm_yday, z.shape[0]) - 1
    # wrap longitude for periodic interpolation
    clon2 = np.concatenate([clon, [clon[0] + 360.0]])
    z2 = np.concatenate([z[doy], z[doy][:, :1]], axis=1)
    f = RegularGridInterpolator((clat, clon2), z2, bounds_error=False, fill_value=None)
    LA, LO = np.meshgrid(lats, lons % 360.0, indexing="ij")
    return f(np.stack([LA.ravel(), LO.ravel()], axis=1)).reshape(LA.shape).astype(np.float32)
