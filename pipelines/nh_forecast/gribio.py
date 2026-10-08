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
# surface / near-surface messages -> (our id, "sfc"); GFS PRMSL decodes as 'prmsl', ECMWF as 'msl'.
# Precipitation ('tp') is keyed by its stepRange, e.g. ("tp", "6-12"), and converted to mm on reading.
SFC_SHORT = {"2t": "t2m", "2d": "d2m", "10u": "u10", "10v": "v10", "prmsl": "msl", "msl": "msl"}


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
            if short in SFC_SHORT:
                key = (SFC_SHORT[short], "sfc")
            elif short == "tp":
                key = ("tp", str(eccodes.codes_get(h, "stepRange")))
                # IFS writes metres of water, AIFS and GFS kg m-2 (= mm): convert to mm here
                tp_factor = 1000.0 if str(eccodes.codes_get(h, "units")).strip() == "m" else 1.0
            elif short in SHORT_TO_VAR and tol == "isobaricInhPa" and lev in levels:
                key = (SHORT_TO_VAR[short], lev)
            else:
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
            out[key] = np.ascontiguousarray(vals[j0:j1] * tp_factor) if key[0] == "tp" else np.ascontiguousarray(vals[j0:j1])
        finally:
            eccodes.codes_release(h)
    return out


PL_COUNT = 18          # u, v, T, Z, omega, q at 850/500/250 hPa
SFC_REQUIRED = ("t2m", "d2m", "u10", "v10", "msl")


def check_fields(fields: dict) -> dict:
    """Require the 18 pressure-level fields and the 5 instantaneous surface fields."""
    pl = [k for k in fields if isinstance(k[1], int)]
    missing = [v for v in SFC_REQUIRED if (v, "sfc") not in fields]
    if len(pl) != PL_COUNT or missing:
        raise RuntimeError(f"decoded {len(pl)} of {PL_COUNT} pressure-level fields; missing surface {missing}")
    return fields


def derive_surface(fields: dict, step: int, state: dict, tp_to_mm: float = 1.0) -> dict:
    """Surface fields for publication: t2m, d2m (K), u10, v10 (m s-1), msl (hPa) and
    tp6, the precipitation accumulated over the 6 h ending at this step (mm).

    GFS files carry a 6-h bucket "(s-6)-s" (and the run total "0-s"); ECMWF files carry
    only the run total "0-s", so tp6 is the difference from the previous 6-h step,
    whose total is kept in `state`."""
    out = {}
    for v in ("t2m", "d2m", "u10", "v10"):
        if (v, "sfc") in fields:
            out[(v, "sfc")] = fields[(v, "sfc")]
    if ("msl", "sfc") in fields:
        out[("msl", "sfc")] = fields[("msl", "sfc")] / 100.0
    shape = next(iter(fields.values())).shape
    bucket, total = ("tp", f"{step - 6}-{step}"), ("tp", f"0-{step}")
    if step == 0:
        tp6 = np.zeros(shape, np.float32)
        state["tp_total"] = np.zeros(shape, np.float32)
    elif bucket in fields:
        tp6 = fields[bucket] * tp_to_mm
        state["tp_total"] = fields[total] if total in fields else state.get("tp_total", 0) + fields[bucket]
    elif total in fields:
        tp6 = (fields[total] - state.get("tp_total", 0)) * tp_to_mm
        state["tp_total"] = fields[total]
    else:
        tp6 = np.full(shape, np.nan, np.float32)
    out[("tp6", "sfc")] = np.clip(np.asarray(tp6, np.float32), 0, None)
    return out
