"""Shared helpers for the Northern-Hemisphere forecast pipeline.

Encoding used for every 2-D field published to the Hugging Face dataset
(readable in the browser with DecompressionStream('gzip')):

    gzip( <JSON header, utf-8, padded with spaces to an even byte length> "\n"
          <uint16 little-endian array, ny*nx values, row-major, lat ascending> )

    value = header.offset + header.scale * u16   (65535 == missing)

The header carries: var, level (hPa), units, ny, nx, lat0, dlat, lon0, dlon,
init (ISO), valid (ISO), step (h), model, offset, scale, vmin, vmax.
"""
from __future__ import annotations

import gzip
import json
import math
import os
from dataclasses import dataclass, asdict

import numpy as np

MISSING = 65535

# Variables we publish (GRIB short name -> our id), and their display units.
VARS = {
    "gh": ("z", "gpm"),
    "t": ("t", "K"),
    "u": ("u", "m s-1"),
    "v": ("v", "m s-1"),
    "w": ("w", "Pa s-1"),
    "q": ("q", "kg kg-1"),
}
LEVELS = (850, 500, 250)


@dataclass
class Grid:
    lat0: float
    dlat: float
    ny: int
    lon0: float
    dlon: float
    nx: int

    @property
    def lats(self) -> np.ndarray:
        return self.lat0 + self.dlat * np.arange(self.ny)

    @property
    def lons(self) -> np.ndarray:
        return self.lon0 + self.dlon * np.arange(self.nx)


NH_HALF = Grid(lat0=0.0, dlat=0.5, ny=181, lon0=0.0, dlon=0.5, nx=720)
# Full-resolution window used by the WxChallenge station maps (CONUS + S. Canada).
CONUS_QTR = Grid(lat0=20.0, dlat=0.25, ny=141, lon0=230.0, dlon=0.25, nx=281)


def encode_field(arr: np.ndarray, header: dict) -> bytes:
    """Quantise a 2-D float array to uint16 and gzip it with a JSON header."""
    a = np.asarray(arr, dtype=np.float64)
    if a.ndim != 2:
        raise ValueError("expected 2-D array")
    finite = np.isfinite(a)
    if finite.any():
        vmin = float(a[finite].min())
        vmax = float(a[finite].max())
    else:
        vmin = vmax = 0.0
    scale = (vmax - vmin) / 65000.0 if vmax > vmin else 1.0
    q = np.full(a.shape, MISSING, dtype=np.uint16)
    q[finite] = np.round((a[finite] - vmin) / scale).astype(np.uint16)
    hdr = dict(header)
    hdr.update({"ny": int(a.shape[0]), "nx": int(a.shape[1]), "offset": vmin,
                "scale": scale, "vmin": vmin, "vmax": vmax, "missing": MISSING,
                "dtype": "uint16le", "order": "row-major, lat ascending, lon ascending"})
    htxt = json.dumps(hdr, separators=(",", ":"))
    if len(htxt.encode("utf-8")) % 2 == 0:
        htxt += " "          # make (header + "\n") an even number of bytes
    payload = htxt.encode("utf-8") + b"\n" + q.astype("<u2").tobytes()
    return gzip.compress(payload, compresslevel=6)


def decode_field(blob: bytes):
    """Inverse of encode_field -> (header dict, float32 2-D array with NaN)."""
    raw = gzip.decompress(blob)
    nl = raw.index(b"\n")
    hdr = json.loads(raw[:nl].decode("utf-8"))
    rows = hdr["ny"] * hdr.get("nt", 1)
    q = np.frombuffer(raw[nl + 1:], dtype="<u2").reshape(rows, hdr["nx"])
    out = hdr["offset"] + hdr["scale"] * q.astype(np.float32)
    out[q == MISSING] = np.nan
    return hdr, out


def field_filename(var: str, level: int) -> str:
    return f"{var}{level}.u16.gz"


def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance (km) between points given in degrees; broadcasts."""
    r = 6371.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dl = np.radians(lon2) - np.radians(lon1)
    a = np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def zonal_meridional_km(lat1, lon1, lat2, lon2):
    """Zonal (east +) and meridional (north +) displacement in km along the
    shortest longitude difference, using the mean latitude for the zonal leg."""
    r = 6371.0
    dlon = ((lon2 - lon1 + 180.0) % 360.0) - 180.0
    latm = math.radians(0.5 * (lat1 + lat2))
    dx = r * math.cos(latm) * math.radians(dlon)
    dy = r * math.radians(lat2 - lat1)
    return dx, dy


def write_json(path: str, obj, gz: bool = False):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    data = json.dumps(obj, separators=(",", ":")).encode("utf-8")
    if gz:
        with open(path, "wb") as f:
            f.write(gzip.compress(data, 6))
    else:
        with open(path, "wb") as f:
            f.write(data)
