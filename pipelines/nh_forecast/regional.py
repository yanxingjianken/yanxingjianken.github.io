"""Regional (US) models on Lambert-conformal grids -> a common 0.05 deg latitude-longitude grid.

HRRR (3 km) and NBM (2.5 km) are published on tangent Lambert-conformal grids.  The web
maps want plain latitude-longitude arrays, so every field is interpolated bilinearly to
REG_GRID (20-54 N, 135-60 W, 0.05 deg, about 5 km).  Points outside the model domain are
missing.  Grid-relative winds (HRRR) are rotated to east/north components with the
standard Lambert angle  alpha = sin(latin) * (lon - LoV).
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage

from common import Grid
from gribio import split_messages

REG_GRID = Grid(lat0=20.0, dlat=0.05, ny=681, lon0=225.0, dlon=0.05, nx=1501)
D2R = np.pi / 180.0

# shortName -> (variable id, level) for the fields we keep
PL_SHORT = {"gh": "z", "t": "t", "u": "u", "v": "v", "w": "w", "q": "q"}
SFC_SHORT = {"2t": "t2m", "2d": "d2m", "10u": "u10", "10v": "v10", "mslma": "msl", "prmsl": "msl",
             "10si": "spd10", "10wdir": "dir10"}


class LambertRegridder:
    """Bilinear interpolation from one Lambert grid (described by GRIB keys) to REG_GRID."""

    def __init__(self, P: dict, grid: Grid = REG_GRID):
        self.grid = grid
        self.nx, self.ny = int(P["Nx"]), int(P["Ny"])
        R = float(P.get("radius") or 6371229.0)
        lat1 = float(P["Latin1InDegrees"]); lov = float(P["LoVInDegrees"])
        n = np.sin(lat1 * D2R)
        F = np.cos(lat1 * D2R) * np.tan(np.pi / 4 + lat1 * D2R / 2) ** n / n
        rho = lambda la: R * F / np.tan(np.pi / 4 + la * D2R / 2) ** n
        r0 = rho(lat1)

        def fwd(la, lo):
            th = n * (((lo - lov) + 540.0) % 360.0 - 180.0) * D2R
            r = rho(la)
            return r * np.sin(th), r0 - r * np.cos(th)

        x0, y0 = fwd(float(P["latitudeOfFirstGridPointInDegrees"]), float(P["longitudeOfFirstGridPointInDegrees"]))
        LA, LO = np.meshgrid(grid.lats, grid.lons, indexing="ij")
        x, y = fwd(LA, LO)
        self.fi = (x - x0) / float(P["DxInMetres"])
        self.fj = (y - y0) / float(P["DyInMetres"])
        self.inside = (self.fi >= 0) & (self.fi <= self.nx - 1) & (self.fj >= 0) & (self.fj <= self.ny - 1)
        # rotation from grid-relative to earth-relative wind components
        self.alpha = n * ((((LO - lov) + 540.0) % 360.0) - 180.0) * D2R

    def __call__(self, vals2d: np.ndarray) -> np.ndarray:
        out = ndimage.map_coordinates(vals2d.astype(np.float32), [self.fj, self.fi], order=1, mode="constant", cval=np.nan, prefilter=False)
        out[~self.inside] = np.nan
        return out.astype(np.float32)

    def rotate(self, u: np.ndarray, v: np.ndarray):
        ca, sa = np.cos(self.alpha), np.sin(self.alpha)
        return (ca * u + sa * v).astype(np.float32), (-sa * u + ca * v).astype(np.float32)


_REGRIDDERS: dict = {}


def read_lambert_fields(data: bytes, levels=(850, 500, 250)) -> dict:
    """Decode Lambert GRIB2 messages and regrid them to REG_GRID.

    Returns {(var, level): array} with level an int for isobaric fields and "sfc" for surface fields;
    precipitation as ("tp", stepRange) in mm.  Grid-relative u/v pairs are rotated to earth-relative."""
    import eccodes
    out, gridrel = {}, set()
    for msg in split_messages(data):
        h = eccodes.codes_new_from_message(msg)
        try:
            g = lambda k: eccodes.codes_get(h, k)
            short, tol, lev = g("shortName"), g("typeOfLevel"), int(g("level"))
            if short in PL_SHORT and tol == "isobaricInhPa" and lev in levels:
                key = (PL_SHORT[short], lev)
            elif short in SFC_SHORT:
                key = (SFC_SHORT[short], "sfc")
            elif short == "tp":
                key = ("tp", str(g("stepRange")))
            else:
                continue
            if g("gridType") != "lambert":
                raise ValueError(f"expected a Lambert grid, got {g('gridType')}")
            P = {k: g(k) for k in ("Nx", "Ny", "Latin1InDegrees", "LoVInDegrees", "latitudeOfFirstGridPointInDegrees",
                                   "longitudeOfFirstGridPointInDegrees", "DxInMetres", "DyInMetres")}
            try:
                P["radius"] = g("radius")
            except Exception:
                P["radius"] = None
            sig = tuple(sorted((k, round(float(v), 6) if v is not None else None) for k, v in P.items()))
            if sig not in _REGRIDDERS:
                _REGRIDDERS[sig] = LambertRegridder(P)
            rg = _REGRIDDERS[sig]
            vals = np.asarray(eccodes.codes_get_values(h), dtype=np.float32).reshape(int(P["Ny"]), int(P["Nx"]))
            try:   # boustrophedonic files (NBM): every second stored row runs right to left; eccodes does not reorder
                if int(g("alternativeRowScanning")):
                    vals[1::2] = vals[1::2, ::-1]
            except Exception:
                pass
            if not int(g("jScansPositively")):
                vals = vals[::-1]
            if key[0] == "tp" and str(g("units")).strip() == "m":
                vals = vals * 1000.0
            out[key] = rg(vals)
            try:
                if key[0] in ("u", "v", "u10", "v10") and int(g("uvRelativeToGrid")):
                    gridrel.add(key[1])
            except Exception:
                pass
            out["_rg"] = rg
        finally:
            eccodes.codes_release(h)
    rg = out.pop("_rg", None)
    for lev in gridrel:   # rotate grid-relative winds
        ku, kv = (("u10", "v10") if lev == "sfc" else ("u", "v"))
        if (ku, lev) in out and (kv, lev) in out and rg is not None:
            out[(ku, lev)], out[(kv, lev)] = rg.rotate(out[(ku, lev)], out[(kv, lev)])
    # wind speed + direction (NBM, degrees true, direction the wind blows from) -> components
    if ("spd10", "sfc") in out and ("dir10", "sfc") in out:
        sp, di = out.pop(("spd10", "sfc")), out.pop(("dir10", "sfc"))
        out[("u10", "sfc")] = (-sp * np.sin(di * D2R)).astype(np.float32)
        out[("v10", "sfc")] = (-sp * np.cos(di * D2R)).astype(np.float32)
    return out
