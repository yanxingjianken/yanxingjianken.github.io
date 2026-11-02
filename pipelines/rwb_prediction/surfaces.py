"""PV on the 330 K and 350 K isentropes and potential temperature on the 2-PVU surface, from u, v, T on pressure
levels (identical code for ERA5 and GFS).

Ertel PV in pressure coordinates (hydrostatic):
    PV = -g [ (f + zeta) d(theta)/dp - (dv/dp)(d theta/dx) + (du/dp)(d theta/dy) ],
    zeta = (1/(a cos phi)) [dv/dlambda - d(u cos phi)/dphi],   theta = T (1000 hPa / p)^kappa,
centred differences on the 1-degree grid (one-sided at the edges, cos phi floored at cos 89.5 deg).
Isentropic surface: from the top level down, the first pair of adjacent levels that brackets theta0; PV, u, v
linear in ln p between them. 2-PVU surface: from the top down, the first pair with PV >= 2 above and < 2 below;
theta, u, v linear in ln p. Columns without a bracket (the deep tropics for 2 PVU) take the value of the top level
(theta) or are left NaN (isentropes); fields are returned with latitude ascending 0..90 N, longitude 0..359 E.
Every surface is also returned as a quantity q that increases toward the pole (PV, or -theta on 2 PVU).
"""
from __future__ import annotations

import numpy as np

from config import A_EARTH, G, KAPPA, LEVELS_HPA, OMEGA

LAT = np.arange(0.0, 90.01, 1.0)
LON = np.arange(0.0, 360.0, 1.0)
PHI = np.deg2rad(LAT)[:, None]
COS = np.maximum(np.cos(PHI), np.cos(np.deg2rad(89.5)))
P_PA = np.array(LEVELS_HPA, float) * 100.0


def _ddlam(f):
    return (np.roll(f, -1, -1) - np.roll(f, 1, -1)) / (2 * np.deg2rad(1.0))


def _ddphi(f):
    return np.gradient(f, np.deg2rad(1.0), axis=-2)


def ertel_pv(u, v, t):
    """PV [PVU] and theta [K] on the pressure levels; u, v, t (L, ny, nx)."""
    th = t * (1000.0 / np.array(LEVELS_HPA, float))[:, None, None] ** KAPPA
    f = 2 * OMEGA * np.sin(PHI)
    zeta = (_ddlam(v) - _ddphi(u * COS)) / (A_EARTH * COS)
    dth_dp = np.gradient(th, P_PA, axis=0)
    du_dp = np.gradient(u, P_PA, axis=0)
    dv_dp = np.gradient(v, P_PA, axis=0)
    dth_dx = _ddlam(th) / (A_EARTH * COS)
    dth_dy = _ddphi(th) / A_EARTH
    pv = -G * ((f + zeta) * dth_dp - dv_dp * dth_dx + du_dp * dth_dy)
    return (pv * 1e6).astype(np.float32), th.astype(np.float32)


def _first_bracket(a, x0, rising_down):
    """Index k (upper level of the pair k, k+1 with levels ordered top -> bottom) of the first pair from the top
    where a crosses x0, and the weight w toward level k+1; -1 where none."""
    L = a.shape[0]
    k_out = np.full(a.shape[1:], -1, int)
    w_out = np.zeros(a.shape[1:], float)
    for k in range(L - 1):
        hi, lo = a[k], a[k + 1]
        if rising_down:
            hit = (lo >= x0) & (hi < x0)
        else:
            hit = (hi >= x0) & (lo < x0)
        new = hit & (k_out < 0)
        with np.errstate(divide="ignore", invalid="ignore"):
            w = (x0 - hi) / (lo - hi)
        k_out[new] = k
        w_out[new] = w[new]
    return k_out, w_out


def _interp(fields, k, w):
    """Linear interpolation in ln p between levels k and k+1 (fields (L, ny, nx)); NaN where k < 0."""
    kk = np.clip(k, 0, fields.shape[0] - 2)
    a = np.take_along_axis(fields, kk[None], 0)[0]
    b = np.take_along_axis(fields, (kk + 1)[None], 0)[0]
    out = a + w * (b - a)
    return np.where(k >= 0, out, np.nan)


def surfaces(u, v, t):
    """{name: (q, u, v)} for pv330, pv350 and th2pvu; arrays (91, 360) float32."""
    pv, th = ertel_pv(u, v, t)
    # LEVELS_HPA run from the top (70 hPa) down; theta decreases downward, so it 'rises' going up
    out = {}
    for name, th0 in (("pv330", 330.0), ("pv350", 350.0)):
        k, w = _first_bracket(th, th0, rising_down=False)     # w is also the ln-p fraction (theta linear in ln p)
        out[name] = tuple(_interp(f, k, w).astype(np.float32) for f in (pv, u, v))
    k, w = _first_bracket(pv, 2.0, rising_down=False)
    th2 = _interp(th, k, w)
    th2 = np.where(k >= 0, th2, th[0])
    u2 = np.where(k >= 0, _interp(u, k, w), u[0])
    v2 = np.where(k >= 0, _interp(v, k, w), v[0])
    out["th2pvu"] = (-th2.astype(np.float32), u2.astype(np.float32), v2.astype(np.float32))
    return out
