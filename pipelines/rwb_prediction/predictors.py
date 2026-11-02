"""The four ways of saying, at an issue time t, where on one surface a new breaking will start within the next 24 h.
Each returns an alarm mask on the 1-degree grid (True inside alarm regions) and the numbers drawn on the maps.

uc_alarm     U - c matching: on contours at fixed equivalent latitudes, every UC_LON_STEP deg of longitude, the phase
             speed c of the contour's undulation over the past 24 h (lagged correlation within +-UC_WINDOW_DEG) against
             the wind U along that piece of contour now; the alarm region lies within UC_BUFFER_KM of the pieces where
             |U - c| <= UC_THRESHOLD_MS.
opus_alarm   Opus model: a predictor variable computed from passive parcels advected over the 60 h before t on the
             surface OPUS_SURFACE (theta on 2 PVU, the parcels' label), in local
             cells (3-deg bands of the label's equivalent latitude x OPUS_LON_BIN deg); the alarm region is the set of
             grid points in cells where it falls to OPUS_RATIO of its value in a reference window 36-59 h earlier.
amp_alarm    wave amplitude, from the field at t alone: each point of the smoothed theta on 2 PVU is displaced from the
             equivalent latitude of its value (the latitude of a circle round the pole enclosing the same area) by
             d = latitude - equivalent latitude; the local amplitude is the rms of d over AMP_BOX_DEG centred on the
             point, and the alarm region is where it reaches AMP_THRESHOLD_DEG.
gfs_alarm    GFS forecast from t: the alarm region lies within GFS_BUFFER_KM of the forecast's new breakings (same
             onset rule as the analysis) at 6-24 h.
"""
from __future__ import annotations

import numpy as np
from scipy.ndimage import uniform_filter

import events as E
from config import (A_EARTH, ALARM_LAT, AMP_BOX_DEG, AMP_THRESHOLD_DEG, GFS_BUFFER_KM, OPUS_BAND_DEG, OPUS_DT_S, OPUS_LON_BIN, OPUS_MIN_REF_D2,
                    OPUS_MIN_SAMPLES, OPUS_MIN_SPREAD_DEG, OPUS_N_PARCELS, OPUS_NOW_H, OPUS_RATIO, OPUS_REF_H,
                    OPUS_SEED_BAND, UC_BUFFER_KM, UC_LEVEL_LATS, UC_LON_STEP, UC_MIN_CORR, UC_THRESHOLD_MS,
                    UC_WINDOW_DEG)

LAT, LON = E.LAT, E.LON
LA, LO = np.meshgrid(LAT, LON, indexing="ij")
IN_BAND = (LA >= ALARM_LAT[0]) & (LA <= ALARM_LAT[1])
W_ROW = np.cos(np.deg2rad(LAT))
W_ROW[-1] = np.cos(np.deg2rad(89.75))
CELL_AREA = (np.sin(np.deg2rad(np.minimum(LAT + 0.5, 90.0)))       # area of each 1-degree row north of the equator
             - np.sin(np.deg2rad(np.maximum(LAT - 0.5, 0.0))))


def fill_nan(a):
    """NaN -> the row mean (rows without data -> overall mean)."""
    a = np.array(a, float)
    with np.errstate(all="ignore"):
        m = np.nanmean(np.where(np.isfinite(a), a, np.nan), 1)
    m = np.where(np.isfinite(m), m, np.nanmean(a))
    return np.where(np.isfinite(a), a, m[:, None])


def eq_lat(q, levels):
    """Equivalent latitude [deg] of each level from the area (Northern Hemisphere) where q >= level."""
    qf = np.where(np.isfinite(q), q, -np.inf)
    w = np.broadcast_to(W_ROW[:, None], q.shape)
    order = np.argsort(qf.ravel())[::-1]
    qs = qf.ravel()[order]
    cw = np.cumsum(w.ravel()[order]) / w.sum()
    frac = np.interp(-np.asarray(levels), -qs, cw)          # qs descending
    return np.rad2deg(np.arcsin(np.clip(1 - frac, -1, 1)))


def eq_lat_points(q):
    """Equivalent latitude [deg] of every grid point's value: from the area of the points with a larger value plus half
    the area of the points with the same value (midpoint rule, so that a zonally symmetric field maps onto itself)."""
    w = np.broadcast_to(CELL_AREA[:, None], q.shape).ravel()
    vals, inv = np.unique(-q.ravel(), return_inverse=True)        # ascending in -q: largest q first
    area = np.bincount(inv, w, minlength=len(vals))
    frac = (np.cumsum(area) - 0.5 * area) / w.sum()
    return np.rad2deg(np.arcsin(np.clip(1 - frac[inv], -1, 1))).reshape(q.shape)


def buffer_mask(lats, lons, km):
    """Grid points within km of any of the given points (and inside ALARM_LAT)."""
    mask = np.zeros(LA.shape, bool)
    lats, lons = np.asarray(lats, float), np.asarray(lons, float)
    for la, lo in zip(lats, lons):
        mask |= E.great_circle_km(la, lo, LA, LO) <= km
    return mask & IN_BAND


# ---------------------------------------------------------------------------------------------------- U - c
def contour_lat_by_meridian(q, level):
    """Mean latitude of the circumpolar contour q = level at each meridian (360,), NaN-free (interpolated)."""
    cs = E.circumpolar_contours(-q, [-level])
    if not cs:
        return None
    _, lon_c, lat_c = cs[0]
    xm = np.arange(90.0, 450.0, 1.0)
    yc = E.crossings(lon_c, lat_c, xm)
    with np.errstate(all="ignore"):
        lat = np.nanmean(yc, 1)
    out = np.full(360, np.nan)
    out[(xm % 360).astype(int)] = lat
    ok = np.isfinite(out)
    if ok.sum() < 300:
        return None
    return np.interp(np.arange(360), np.arange(360)[ok], out[ok], period=360)


def uc_alarm(now, before):
    """now, before: (q, u, v) at t and t - 24 h, q smoothed as for the events. Returns the alarm mask and the
    matching contour pieces [(lat, lon, |U - c|)]."""
    q, u, v = now
    q0 = before[0]
    grid = np.linspace(np.nanmin(q), np.nanmax(q), 400)
    levels = np.interp(UC_LEVEL_LATS, eq_lat(q, grid), grid)
    uf = fill_nan(u)
    half = int(UC_WINDOW_DEG)
    pts = []
    for phi_l, lev in zip(UC_LEVEL_LATS, levels):
        a = contour_lat_by_meridian(q, lev)
        b = contour_lat_by_meridian(q0, lev)
        if a is None or b is None:
            continue
        ea, eb = a - phi_l, b - phi_l
        for lc in np.arange(0.0, 360.0, UC_LON_STEP):
            lon = (int(lc) + np.arange(-half, half + 1)) % 360
            x = ea[lon] - ea[lon].mean()
            best, shift = -1.0, 0
            for d in range(-40, 41):
                y = eb[(lon - d) % 360]
                y = y - y.mean()
                den = np.sqrt((x * x).sum() * (y * y).sum())
                r = (x * y).sum() / den if den > 0 else -1.0
                if r > best:
                    best, shift = r, d
            if best < UC_MIN_CORR:
                continue
            c = A_EARTH * np.cos(np.deg2rad(phi_l)) * np.deg2rad(shift) / 86400.0
            piece = (int(lc) + np.arange(-int(UC_LON_STEP // 2), int(UC_LON_STEP // 2) + 1)) % 360
            rows = np.clip(np.round(a[piece]).astype(int), 0, 90)
            om_u = np.mean(uf[rows, piece] / (A_EARTH * np.cos(np.deg2rad(np.minimum(rows, 89)))))
            du = abs(om_u * A_EARTH * np.cos(np.deg2rad(phi_l)) - c)
            if du <= UC_THRESHOLD_MS:
                pts += [(float(a[p]), float(p), round(float(du), 2)) for p in piece[::3]]
    mask = buffer_mask([p[0] for p in pts], [p[1] for p in pts], UC_BUFFER_KM) if pts else np.zeros(LA.shape, bool)
    return mask, pts


# ---------------------------------------------------------------------------------------------------- Opus model
def _bilinear(field, lat, lon):
    y = np.clip(lat, 0.0, 89.999)
    i0 = np.floor(y).astype(int)
    fy = y - i0
    x = np.mod(lon, 360.0)
    j0 = np.floor(x).astype(int) % 360
    fx = x - np.floor(x)
    j1 = (j0 + 1) % 360
    i1 = np.minimum(i0 + 1, 90)
    return ((1 - fy) * ((1 - fx) * field[i0, j0] + fx * field[i0, j1])
            + fy * ((1 - fx) * field[i1, j0] + fx * field[i1, j1]))


def _velocity(us, vs, tau, lat, lon):
    """Parcel rates [deg s-1] at fractional hour tau (linear in time between hourly fields)."""
    h0 = int(np.clip(np.floor(tau), 0, len(us) - 2))
    w = tau - h0
    u = (1 - w) * _bilinear(us[h0], lat, lon) + w * _bilinear(us[h0 + 1], lat, lon)
    v = (1 - w) * _bilinear(vs[h0], lat, lon) + w * _bilinear(vs[h0 + 1], lat, lon)
    k = 180.0 / np.pi / A_EARTH
    return u * k / np.cos(np.deg2rad(np.clip(lat, 0, 88.5))), v * k


def fibonacci_band(n, lat_lo, lat_hi):
    """Area-uniform points between two latitudes."""
    z0, z1 = np.sin(np.deg2rad(lat_lo)), np.sin(np.deg2rad(lat_hi))
    k = np.arange(n) + 0.5
    z = z0 + (z1 - z0) * k / n
    lon = np.mod(k * 180.0 * (3 - np.sqrt(5)), 360.0)
    return np.rad2deg(np.arcsin(z)), lon


def advect(qs, us, vs):
    """Parcels over the hourly fields qs, us, vs (H, 91, 360): labels q0 and hourly positions (H, N)."""
    us = np.array([fill_nan(a) for a in us])
    vs = np.array([fill_nan(a) for a in vs])
    lat, lon = fibonacci_band(OPUS_N_PARCELS, *OPUS_SEED_BAND)
    q0 = _bilinear(fill_nan(qs[0]), lat, lon)
    lats, lons = [lat.copy()], [lon.copy()]
    nsub = int(round(3600.0 / OPUS_DT_S))
    dt_h = OPUS_DT_S / 3600.0
    tau = 0.0
    for h in range(len(us) - 1):
        for _ in range(nsub):
            k1 = _velocity(us, vs, tau, lat, lon)
            k2 = _velocity(us, vs, tau + dt_h / 2, lat + OPUS_DT_S / 2 * k1[1], lon + OPUS_DT_S / 2 * k1[0])
            k3 = _velocity(us, vs, tau + dt_h / 2, lat + OPUS_DT_S / 2 * k2[1], lon + OPUS_DT_S / 2 * k2[0])
            k4 = _velocity(us, vs, tau + dt_h, lat + OPUS_DT_S * k3[1], lon + OPUS_DT_S * k3[0])
            lon = np.mod(lon + OPUS_DT_S / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]), 360.0)
            lat = np.clip(lat + OPUS_DT_S / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]), 0.5, 88.5)
            tau += dt_h
        lats.append(lat.copy())
        lons.append(lon.copy())
    return q0, np.array(lats), np.array(lons)


def _eq_lat_tables(qs, q0):
    """Equivalent latitude of the parcel labels at every hour (H, N), smoothed +-3 h at fixed level, and the level
    table of the last hour (levels, phi_e)."""
    lev = np.linspace(np.nanpercentile(q0, 0.5), np.nanpercentile(q0, 99.5), 300)
    table = np.array([eq_lat(fill_nan(q), lev) for q in qs])
    pad = np.concatenate([table[:1].repeat(3, 0), table, table[-1:].repeat(3, 0)])
    ker = np.ones(7) / 7.0
    sm = np.array([np.convolve(pad[:, j], ker, "valid") for j in range(len(lev))]).T
    return np.array([np.interp(q0, lev, sm[h]) for h in range(len(qs))]), (lev, sm[-1])


def predictor_cells(qs, lat_p, lon_p, q0):
    """Per local cell (band x longitude bin): the predictor variable in the reference and current windows [d^-2]
    and the displacement spread [deg]; also the last hour's equivalent-latitude table."""
    H = len(qs)
    phi_e, last_table = _eq_lat_tables(qs, q0)
    eta = lat_p - phi_e
    d1 = (eta[2:] - eta[:-2]) / 2.0
    d2 = eta[2:] - 2 * eta[1:-1] + eta[:-2]
    hrs = np.arange(1, H - 1) - (H - 1)
    nb, nl = int(90 / OPUS_BAND_DEG), int(360 / OPUS_LON_BIN)
    band = np.clip(np.floor(phi_e[0] / OPUS_BAND_DEG).astype(int), 0, nb - 1)
    out = {}
    for name, (h_a, h_b) in (("ref", OPUS_REF_H), ("now", OPUS_NOW_H)):
        sel = (hrs >= h_a) & (hrs <= h_b)
        e, e1, e2 = eta[1:-1][sel], d1[sel], d2[sel]
        lbin = (np.mod(lon_p[1:-1][sel], 360.0) // OPUS_LON_BIN).astype(int) % nl
        idx = (np.broadcast_to(band, e.shape) * nl + lbin).ravel()
        e, e1, e2 = e.ravel(), e1.ravel(), e2.ravel()
        cols = [e * e, e * e1, e, e1 * e1, e1, np.ones_like(e), e2 * e, e2 * e1, e2]
        S = np.stack([np.bincount(idx, w, minlength=nb * nl) for w in cols], 1)
        k = np.full(nb * nl, np.nan)
        sd = np.full(nb * nl, np.nan)
        for i in np.flatnonzero(S[:, 5] >= OPUS_MIN_SAMPLES):
            ee, ee1, e_, e11, e1_, nn, ye, ye1, y_ = S[i]
            G = np.array([[ee, ee1, -e_], [ee1, e11, -e1_], [-e_, -e1_, nn]])
            try:
                kk = np.linalg.solve(G, np.array([-ye, -ye1, y_]))[0]
            except np.linalg.LinAlgError:
                continue
            k[i] = kk * 576.0                                     # h^-2 -> d^-2
            sd[i] = np.sqrt(max(ee / nn - (e_ / nn) ** 2, 0.0))
        out[name] = (k.reshape(nb, nl), sd.reshape(nb, nl))
    return out, last_table


def opus_alarm(qs, us, vs):
    """qs, us, vs: hourly surface fields from t - 60 h to t. Returns the alarm mask and the per-cell ratio
    (bands x longitude bins, NaN where untested)."""
    q0, lat_p, lon_p = advect(qs, us, vs)
    cells, (lev, phi_lev) = predictor_cells(qs, lat_p, lon_p, q0)
    k_ref, sd_ref = cells["ref"]
    k_now, _ = cells["now"]
    tested = (k_ref >= OPUS_MIN_REF_D2) & (sd_ref >= OPUS_MIN_SPREAD_DEG)
    ratio = np.where(tested, k_now / np.where(tested, k_ref, 1.0), np.nan)
    # map to the grid through each point's equivalent latitude (field at t, smoothed as for the events) and
    # longitude bin, so that PV filaments do not scatter a cell over the map
    phi_grid = np.interp(E.smooth(fill_nan(qs[-1])), lev, phi_lev)
    nb, nl = ratio.shape
    b = np.clip((phi_grid // OPUS_BAND_DEG).astype(int), 0, nb - 1)
    lb = (LO // OPUS_LON_BIN).astype(int) % nl
    r_grid = ratio[b, lb]
    mask = np.isfinite(r_grid) & (r_grid <= OPUS_RATIO) & IN_BAND
    return mask, ratio


# ---------------------------------------------------------------------------------------------------- wave amplitude
def amp_field(q):
    """q at the issue time -> local amplitude [deg]: the rms, over AMP_BOX_DEG (latitude, longitude) centred on each
    point, of the displacement of the smoothed field from the equivalent latitude of its value."""
    qs = E.smooth(fill_nan(q))
    d = LA - eq_lat_points(qs)
    return np.sqrt(uniform_filter(d * d, size=AMP_BOX_DEG, mode=("nearest", "wrap")))


def amp_alarm(q, threshold=AMP_THRESHOLD_DEG):
    """Alarm mask where the local amplitude reaches the threshold, and the local amplitude."""
    a = amp_field(q)
    return (a >= threshold) & IN_BAND, a


# ---------------------------------------------------------------------------------------------------- GFS
def gfs_alarm(objs_by_step):
    """objs_by_step: [(step_h, objects)] for steps 0, 6, ..., 24 of one run. An object at step >= 6 is a forecast
    onset if no object of the same type lay within MATCH_KM at the (up to two) previous steps. Returns the alarm
    mask (within GFS_BUFFER_KM of the forecast onsets) and the onsets."""
    found = []
    for n in range(1, len(objs_by_step)):
        step, objs = objs_by_step[n]
        prev = objs_by_step[n - 1][1] + (objs_by_step[n - 2][1] if n >= 2 else [])
        for o in objs:
            near = [p for p in prev if p["type"] == o["type"]
                    and E.great_circle_km(o["lat"], o["lon"], p["lat"], p["lon"]) < E.MATCH_KM]
            if not near:
                found.append(dict(step=step, **{k: v for k, v in o.items() if k != "folds"}))
    mask = buffer_mask([o["lat"] for o in found], [o["lon"] for o in found], GFS_BUFFER_KM) if found \
        else np.zeros(LA.shape, bool)
    return mask, found
