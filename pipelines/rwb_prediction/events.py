"""Rossby wave breaking objects and their onsets on one surface, from overturning circumpolar contours.

The field is first smoothed with a Gaussian of EVENT_SMOOTH_DEG (in longitude EVENT_SMOOTH_DEG / cos(latitude),
capped at 60 deg) so that only large-scale overturning counts. Contours are traced at fixed values: PV every 0.5 PVU
(PV_LEVELS) on the isentropes, potential temperature every 5 K (TH_LEVELS) on 2 PVU. Contour method after pvtend.rwb
(X. Yan and T. Tamarin-Brodsky, MIT License): on the full Northern Hemisphere, the longest contour at each value that
spans >= 355 deg of longitude is circumpolar; a meridian that crosses it >= 3 times lies in a fold; each run of
folded meridians gives a bay whose envelope must cover >= AREA_MIN_DEG2; the bay is anticyclonic (AWB) or cyclonic
(CWB) by the path-order rule (the first-visited highest crossing before the first-visited lowest crossing -> CWB,
median over the bay's meridians). The rule was written for 500-hPa height, which decreases poleward, so contours are
traced on -q (q increases poleward: PV, or -theta on 2 PVU).

Bays from different contour values within CLUSTER_KM form one breaking object (centroid: area-weighted mean; type:
area-weighted majority; area: the largest bay); for the maps only the contour of the largest bay is kept. Flank: the
object lies equatorward or poleward of the jet axis, the latitude of the strongest wind on the surface in 20-70 N at
the object's longitude (smoothed over +-30 deg). Onset: an object with no object of the same type within MATCH_KM at
the two previous event times (6 h and 12 h before).
"""
from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter1d, uniform_filter1d

from config import (A_EARTH, AREA_MIN_DEG2, CIRCUMPOLAR_MIN_SPAN, CLUSTER_KM, EVENT_SMOOTH_DEG, JET_BAND,
                    MATCH_KM, MIN_CROSS, PV_LEVELS, TH_LEVELS)

LAT = np.arange(0.0, 90.01, 1.0)
LON = np.arange(0.0, 360.0, 1.0)


def great_circle_km(lat1, lon1, lat2, lon2):
    p1, p2 = np.deg2rad(lat1), np.deg2rad(lat2)
    dl = np.deg2rad(np.asarray(lon2) - np.asarray(lon1))
    c = np.sin(p1) * np.sin(p2) + np.cos(p1) * np.cos(p2) * np.cos(dl)
    return A_EARTH / 1e3 * np.arccos(np.clip(c, -1, 1))


def smooth(q, sig=EVENT_SMOOTH_DEG):
    """Gaussian smoothing on the 1-degree grid: sigma sig in latitude, sig / cos(latitude) in longitude (<= 60)."""
    f = np.where(np.isfinite(q), q, np.nanmedian(q))
    f = gaussian_filter1d(f, sig, axis=0, mode="nearest")
    out = np.empty_like(f)
    for i, lat in enumerate(LAT):
        out[i] = gaussian_filter1d(f[i], min(sig / max(np.cos(np.deg2rad(lat)), 0.087), 60.0), mode="wrap")
    return out


def levels_for(name):
    """Contour values of -q for a surface (q = PV, or -theta on 2 PVU)."""
    return -np.array(PV_LEVELS) if name.startswith("pv") else np.array(TH_LEVELS, float)


def display_values(name, levels):
    return -levels if name.startswith("pv") else levels


def circumpolar_contours(field, levels):
    """[(level, lon, lat)] of the longest contour at each level spanning >= CIRCUMPOLAR_MIN_SPAN deg; field
    (91, 360) with latitude ascending; the field is doubled in longitude (0..540) so a closed circle is traced."""
    from skimage.measure import find_contours
    f = np.where(np.isfinite(field), field, np.nanmedian(field))
    n_wrap = 181
    lon_ext = np.concatenate([LON, LON[:n_wrap] + 360.0])
    f_ext = np.concatenate([f, f[:, :n_wrap]], axis=1)
    out = []
    for lev in levels:
        cs = find_contours(f_ext, level=lev)
        if not cs:
            continue
        c = max(cs, key=len)
        if len(c) < 30:
            continue
        lon_c = np.interp(c[:, 1], np.arange(len(lon_ext)), lon_ext)
        lat_c = np.interp(c[:, 0], np.arange(len(LAT)), LAT)
        if lon_c.max() - lon_c.min() < CIRCUMPOLAR_MIN_SPAN:
            continue
        out.append((float(lev), lon_c, lat_c))
    return out


def crossings(x, y, xm):
    """Crossing latitudes of the polyline (x, y) with meridians xm, as an (M, N-1) array in path order (NaN where a
    segment does not cross), vectorized over meridians and segments."""
    x1, x2, y1, y2 = x[:-1], x[1:], y[:-1], y[1:]
    dx = x2 - x1
    lo, hi = np.minimum(x1, x2), np.maximum(x1, x2)
    xm = xm[:, None]
    hit = (xm >= lo) & (xm <= hi) & (dx != 0)
    with np.errstate(divide="ignore", invalid="ignore"):
        yc = y1 + (xm - x1) / dx * (y2 - y1)
    return np.where(hit, yc, np.nan)


def bays(lon_c, lat_c, step=0.5):
    """Bays of one circumpolar contour: [(type, area_deg2, centroid_lon (0..360), centroid_lat, fold_lines)], where
    fold_lines are the contour's passes through the bay's longitude interval [(lon 0..360, lat)]. Meridians are probed
    every `step` deg over one full turn in the middle of the doubled domain (90..450)."""
    xm = np.arange(90.0, 450.0, step)
    yc = crossings(lon_c, lat_c, xm)
    n = np.isfinite(yc).sum(1)
    folded = n >= MIN_CROSS
    out = []
    if not folded.any():
        return out
    edges = np.flatnonzero(np.diff(np.concatenate([[0], folded.astype(int), [0]])))
    for a, b in zip(edges[::2], edges[1::2]):
        if b - a < 3:
            continue
        y = yc[a:b]
        ymin, ymax = np.nanmin(y, 1), np.nanmax(y, 1)
        xs = xm[a:b]
        area = float(np.sum(ymax - ymin) * step)
        if area < AREA_MIN_DEG2:
            continue
        cx = float(np.sum(xs * (ymax - ymin)) / np.sum(ymax - ymin))
        cy = float(np.sum(0.5 * (ymax + ymin) * (ymax - ymin)) / np.sum(ymax - ymin))
        big = np.where(np.isfinite(y), y, -np.inf)
        small = np.where(np.isfinite(y), y, np.inf)
        sign = np.where(np.argmax(big, 1) < np.argmin(small, 1), 1.0, -1.0)
        med = float(np.median(sign))
        typ = "CWB" if med > 0 else ("AWB" if med < 0 else "UNK")
        idx = np.flatnonzero((lon_c >= xs[0]) & (lon_c <= xs[-1]))       # the contour's passes through the fold
        runs = [r for r in np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1) if r.size >= 2]
        line = [(np.round(np.mod(lon_c[r], 360.0), 2), np.round(lat_c[r], 2)) for r in runs]
        out.append((typ, area, cx % 360.0, cy, line))
    return out


def jet_axis(u, v):
    """Latitude (deg) of the strongest wind in JET_BAND at each longitude, smoothed over +-30 deg."""
    sp = np.hypot(u, v)
    sel = (LAT >= JET_BAND[0]) & (LAT <= JET_BAND[1])
    sp = np.where(np.isfinite(sp), sp, -1.0)
    lat = LAT[sel][np.argmax(sp[sel], 0)]
    return uniform_filter1d(lat.astype(float), 61, mode="wrap")


def objects(q, u, v, name):
    """Breaking objects on one surface at one time: list of dicts lon, lat, type, area, flank, jet_lat, and the
    folded contour pieces `folds` [(level, lons, lats)] (level in PVU or K)."""
    f = -smooth(q)                                          # decreasing poleward, as 500-hPa height
    raw = []
    for lev, lon_c, lat_c in circumpolar_contours(f, levels_for(name)):
        shown = float(display_values(name, np.array([lev]))[0])
        raw += [(t, a, x, y, (shown, ln)) for t, a, x, y, ln in bays(lon_c, lat_c) if t != "UNK"]
    axis = jet_axis(u, v)
    n = len(raw)
    label = np.arange(n)
    for i in range(n):
        for j in range(i + 1, n):
            if great_circle_km(raw[i][3], raw[i][2], raw[j][3], raw[j][2]) < CLUSTER_KM:
                label[label == label[j]] = label[i]
    out = []
    for c in np.unique(label):
        m = [raw[i] for i in range(n) if label[i] == c]
        w = np.array([r[1] for r in m])
        lon = np.rad2deg(np.angle(np.sum(w * np.exp(1j * np.deg2rad([r[2] for r in m]))))) % 360.0
        lat = float(np.sum(w * np.array([r[3] for r in m])) / w.sum())
        typ = "AWB" if w[[r[0] == "AWB" for r in m]].sum() >= 0.5 * w.sum() else "CWB"
        jl = float(axis[int(round(lon)) % 360])
        big = max(m, key=lambda r: r[1])                     # the contour whose bay is largest
        folds = [(big[4][0], lo, la) for lo, la in big[4][1]]
        out.append(dict(lon=round(float(lon), 2), lat=round(lat, 2), type=typ, area=round(float(w.max()), 1),
                        flank="eq" if lat < jl else "pol", jet_lat=round(jl, 1), folds=folds))
    return out


def onsets(objs_by_time):
    """objs_by_time: list of (time, [objects]) every 6 h in order. Returns [(time, object)] of objects with no object
    of the same type within MATCH_KM at the two previous times (the first two times cannot have onsets)."""
    out = []
    for k in range(2, len(objs_by_time)):
        t, objs = objs_by_time[k]
        prev = objs_by_time[k - 1][1] + objs_by_time[k - 2][1]
        for o in objs:
            near = [p for p in prev if p["type"] == o["type"]
                    and great_circle_km(o["lat"], o["lon"], p["lat"], p["lon"]) < MATCH_KM]
            if not near:
                out.append((t, o))
    return out
