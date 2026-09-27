"""Decode GRIB2 messages with eccodes into 2-D arrays on a common grid.

Both GFS (pgrb2.0p25) and ECMWF open data (0.25 deg) are regular lat/lon grids;
they differ in scan direction (both N->S) and longitude origin (GFS 0..359.75,
ECMWF -180..179.75).  read_fields() returns every message as an array on the
Northern-Hemisphere grid used by the pipeline: latitude ascending 0..90 (361
rows), longitude 0..359.75 (1440 columns).
"""
from __future__ import annotations

import numpy as np

# eccodes shortName -> our variable id (GFS: HGT->gh, TMP->t, UGRD->u, VGRD->v, VVEL->w, SPFH->q;
# ECMWF: gh 156, t 130, u 131, v 132, w 135, q 133)
SHORT_TO_VAR = {"gh": "z", "t": "t", "u": "u", "v": "v", "w": "w", "q": "q"}


def split_messages(data: bytes):
    """Yield the individual GRIB2 messages contained in a byte string."""
    off = 0
    n = len(data)
    while off < n:
        k = data.find(b"GRIB", off)
        if k < 0:
            break
        length = int.from_bytes(data[k + 8:k + 16], "big")
        if length <= 0 or k + length > n:
            break
        yield data[k:k + length]
        off = k + length


def read_fields(data: bytes, levels=(850, 500, 250)) -> dict:
    """Return {(var, level): float32 array (361, 1440)} for the wanted messages."""
    import eccodes
    out = {}
    for msg in split_messages(data):
        h = eccodes.codes_new_from_message(msg)
        try:
            short = eccodes.codes_get(h, "shortName")
            tol = eccodes.codes_get(h, "typeOfLevel")
            lev = int(eccodes.codes_get(h, "level"))
            if short not in SHORT_TO_VAR or tol != "isobaricInhPa" or lev not in levels:
                continue
            ni = int(eccodes.codes_get(h, "Ni")); nj = int(eccodes.codes_get(h, "Nj"))
            lat1 = float(eccodes.codes_get(h, "latitudeOfFirstGridPointInDegrees"))
            lon1 = float(eccodes.codes_get(h, "longitudeOfFirstGridPointInDegrees"))
            di = float(eccodes.codes_get(h, "iDirectionIncrementInDegrees"))
            dj = float(eccodes.codes_get(h, "jDirectionIncrementInDegrees"))
            jpos = int(eccodes.codes_get(h, "jScansPositively"))
            vals = np.asarray(eccodes.codes_get_values(h), dtype=np.float32).reshape(nj, ni)
            if abs(di - 0.25) > 1e-6 or abs(dj - 0.25) > 1e-6:
                raise ValueError(f"unexpected grid spacing {di}x{dj}")
            if not jpos:                      # rows run N -> S: flip to ascending latitude
                vals = vals[::-1]
                lat_first = lat1 - dj * (nj - 1)
            else:
                lat_first = lat1
            lon1 = lon1 % 360.0
            if abs(lon1) > 1e-6:              # e.g. ECMWF starts at -180 (=180): roll so column 0 is 0E
                shift = int(round(lon1 / di))
                vals = np.roll(vals, shift, axis=1)
            # crop to 0..90N
            j0 = int(round((0.0 - lat_first) / dj))
            j1 = int(round((90.0 - lat_first) / dj)) + 1
            if j0 < 0 or j1 > nj:
                raise ValueError("grid does not cover 0-90N")
            out[(SHORT_TO_VAR[short], lev)] = np.ascontiguousarray(vals[j0:j1])
        finally:
            eccodes.codes_release(h)
    return out
