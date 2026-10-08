"""Extra helpers for group-A figures (diagnostics on the ERA5 lat/lon grid).

Only kinematic/thermodynamic arithmetic lives here; all drawing goes through jstyle.
"""
from __future__ import annotations

import numpy as np
import xarray as xr

R_E = 6.371e6
G0 = 9.80665
OMEGA = 7.292e-5

# common extents (lon0, lon1, lat0, lat1) for group A
MESO = (-73.5, -69.5, 41, 43.5)      # Boston-area mesoscale
REG = (-79, -65, 38, 47)             # New England regional (map extent)
REG_DATA = (-78, -65, 39, 47)        # fetch key used for REG fields (padded 6 deg, covers REG)
SYN = (-87, -62, 30, 48)             # East-coast synoptic (map extent)
SYN_DATA = (-85, -60, 32, 50)        # fetch key used for SYN fields (padded 6 deg, covers SYN)
SOCAL = (-122.5, -111, 31, 40.5)     # Southern California + Great Basin (map extent)
SOCAL_DATA = (-125, -112, 30, 41)    # fetch key used for SOCAL fields


def _grad(da):
    """d/dx, d/dy (per metre) of a (latitude, longitude) field via centred differences."""
    lat = np.deg2rad(da.latitude.values)
    lon = np.deg2rad(da.longitude.values)
    f = da.values.astype(float)
    dfdlat = np.gradient(f, lat, axis=0)
    dfdlon = np.gradient(f, lon, axis=1)
    coslat = np.cos(lat)[:, None]
    dx = dfdlon / (R_E * coslat)
    dy = dfdlat / R_E
    return (xr.DataArray(dx, coords=da.coords, dims=da.dims),
            xr.DataArray(dy, coords=da.coords, dims=da.dims))


def divergence(u, v):
    ux, _ = _grad(u)
    _, vy = _grad(v)
    lat = np.deg2rad(v.latitude)
    return ux + vy - v * np.tan(lat) / R_E   # spherical metric term


def rel_vorticity(u, v):
    vx, _ = _grad(v)
    _, uy = _grad(u)
    lat = np.deg2rad(u.latitude)
    return vx - uy + u * np.tan(lat) / R_E


def abs_vorticity(u, v):
    return rel_vorticity(u, v) + 2 * OMEGA * np.sin(np.deg2rad(u.latitude))


def advection(u, v, s):
    """-V . grad(s) (units of s per second)."""
    sx, sy = _grad(s)
    return -(u * sx + v * sy)


def grad_mag(s):
    sx, sy = _grad(s)
    return np.hypot(sx, sy)


def frontogenesis(u, v, th):
    """2-D Petterssen kinematic frontogenesis F = d|grad th|/dt (K m^-1 s^-1).

    Returns (total, convergence_term). Convergence term = -0.5 |grad th| * div.
    """
    tx, ty = _grad(th)
    ux, uy = _grad(u)
    vx, vy = _grad(v)
    mag = np.hypot(tx, ty)
    mag = mag.where(mag > 1e-9)
    F = -(tx * (tx * ux + ty * vx) + ty * (tx * uy + ty * vy)) / mag
    conv = -0.5 * mag * (ux + vy)
    return F, conv


def theta(T, p_pa):
    return T * (1e5 / p_pa) ** 0.2854


def rh_from_td(T, Td):
    """Relative humidity (%) over liquid water from T, Td in K (Bolton 1980)."""
    def es(t):
        tc = t - 273.15
        return 6.112 * np.exp(17.67 * tc / (tc + 243.5))
    return 100 * es(Td) / es(T)


def smooth(da, n=1):
    """n passes of a 1-2-1 filter in each direction (edges kept)."""
    a = da.values.astype(float).copy()
    for _ in range(n):
        b = a.copy()
        b[1:-1, :] = 0.25 * a[:-2, :] + 0.5 * a[1:-1, :] + 0.25 * a[2:, :]
        c = b.copy()
        c[:, 1:-1] = 0.25 * b[:, :-2] + 0.5 * b[:, 1:-1] + 0.25 * b[:, 2:]
        a = c
    return xr.DataArray(a, coords=da.coords, dims=da.dims)


def subset(da, extent, pad=0.0):
    lon0, lon1, lat0, lat1 = extent
    return da.sel(latitude=slice(lat1 + pad, lat0 - pad), longitude=slice(lon0 - pad, lon1 + pad))


def local_min(da, extent, pad=0.0):
    """(lon, lat, value) of the minimum of da inside extent."""
    s = subset(da, extent, pad)
    i = np.unravel_index(np.nanargmin(s.values), s.shape)
    return float(s.longitude[i[1]]), float(s.latitude[i[0]]), float(s.values[i])


def local_max(da, extent, pad=0.0):
    s = subset(da, extent, pad)
    i = np.unravel_index(np.nanargmax(s.values), s.shape)
    return float(s.longitude[i[1]]), float(s.latitude[i[0]]), float(s.values[i])


def at(da, lon, lat):
    return float(da.interp(longitude=lon, latitude=lat).values)


def annotate(ax, text, xy, xytext, fontsize=7):
    """One minimal black arrow + label (lon/lat coordinates), no box."""
    import cartopy.crs as ccrs
    tr = ccrs.PlateCarree()._as_mpl_transform(ax)
    import matplotlib.patheffects as pe
    ax.annotate(text, xy=xy, xytext=xytext, xycoords=tr, textcoords=tr, fontsize=fontsize,
                color="k", ha="center", va="center", zorder=8, linespacing=0.95,
                path_effects=[pe.withStroke(linewidth=1.6, foreground="white")],
                arrowprops=dict(arrowstyle="-|>", lw=0.6, color="k", shrinkA=1, shrinkB=1,
                                mutation_scale=6))


def contour_clean(ax, da, levels, label_levels=None, fmt="%d", margin=0.12, extent=None, pad=2.0,
                  max_labels=6, **kw):
    """jstyle.contour, but with sparse labels placed only well inside the panel.

    clabel's automatic placement often puts labels on the off-map part of the padded field
    (they then show up half-clipped at the frame), so label positions are chosen here: for each
    level in `label_levels`, the contour vertex nearest the panel centre that lies inside the
    inner (1 - 2*margin) box. At most `max_labels` labels, spread over the levels."""
    import jstyle as J
    if extent is not None:
        da = subset(da, extent, pad)
    cs = J.contour(ax, da, levels, label=False, **kw)
    if label_levels is None:
        return cs
    inv = ax.transAxes.inverted()
    pos, lv_used = [], []
    for k, lev in enumerate(cs.levels):
        if not np.any(np.isclose(lev, label_levels)):
            continue
        segs = [sg for sg in cs.allsegs[k] if len(sg) > 3]
        if not segs:
            continue
        v = np.concatenate(segs)                       # lon/lat (source CRS)
        import cartopy.crs as ccrs
        v = ax.projection.transform_points(ccrs.PlateCarree(), v[:, 0], v[:, 1])[:, :2]
        fr = inv.transform(ax.transData.transform(v))
        ok = np.all((fr > margin) & (fr < 1 - margin), axis=1)
        if not ok.any():
            continue
        d = np.hypot(fr[:, 0] - 0.5, fr[:, 1] - 0.5)
        d[~ok] = np.inf
        # prefer a point away from the exact centre so labels do not pile up
        j = int(np.argmin(np.abs(d - 0.22)))
        pos.append(tuple(v[j])); lv_used.append(lev)
    if len(pos) > max_labels:
        sel = np.linspace(0, len(pos) - 1, max_labels).round().astype(int)
        pos = [pos[i] for i in sel]; lv_used = [lv_used[i] for i in sel]
    if pos:
        ax.clabel(cs, levels=lv_used, manual=pos, fmt=fmt, fontsize=6, inline=True, inline_spacing=2)
    return cs


# ------------------------------------------------------------------ layout
# jstyle.new_figure() keeps matplotlib's default subplot margins (left=0.125, right=0.9), so
# with bbox_inches="tight" a 1x3 map row comes out ~5.1 in wide instead of the 6.5-in page
# width. prep() widens the margins before the axes are created; anchor_south() pins each map to
# the bottom of its box (next to its colorbar) after the colorbars exist, so any spare height
# ends up above the panel title and is cropped by the tight bounding box.
def prep(fig, wspace=0.07):
    fig.subplots_adjust(left=0.012, right=0.985, bottom=0.03, top=0.97, wspace=wspace)


def anchor_south(axs):
    for ax in axs:
        ax.set_anchor("S")


def check_text(fig, axs):
    """Print a warning if a panel title runs past its panel (into the next one / off the figure)
    or a colorbar label is wider than its colorbar. Call just before J.save."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    for i, ax in enumerate(axs):
        tb = ax._left_title.get_window_extent(r)
        ab = ax.get_window_extent(r)
        nxt = axs[i + 1].get_window_extent(r).x0 if i + 1 < len(axs) else fig.bbox.x1
        if tb.x1 > nxt - 4:
            print(f"WARN title {i} overruns: x1={tb.x1:.0f} next={nxt:.0f} ({ax.get_title(loc='left')})")
        else:
            print(f"title {i} ok: spare {nxt - tb.x1:.0f} px past next/edge, {ab.x1 - tb.x1:.0f} px vs own frame")
    for cax in fig.axes:
        if cax in axs:
            continue
        lab = cax.xaxis.label
        if lab.get_text():
            lb = lab.get_window_extent(r); cb = cax.get_window_extent(r)
            if lb.x0 < cb.x0 - 2 or lb.x1 > cb.x1 + 2:
                print(f"WARN colorbar label wider than bar: {lab.get_text()}")


def finish():
    """Exit immediately (the ARCO/gcsfs thread can hang interpreter shutdown on Windows)."""
    import os, sys
    sys.stdout.flush(); sys.stderr.flush()
    os._exit(0)
