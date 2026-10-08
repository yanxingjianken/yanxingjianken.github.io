"""Extra helpers for group-C figures (does not modify jstyle)."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import xarray as xr

import jstyle as J

SP = Path(__file__).resolve().parent.parent
OUT = SP.parent / "images" / "wx_systems_v3"
G = 9.80665
RD = 287.04
CP = 1004.0


def fetch_levels(var, time, extent, levels, pad=6.0):
    """Fetch several pressure levels of one variable in one request (cached)."""
    lon0, lon1, lat0, lat1 = extent
    lon0, lon1, lat0, lat1 = lon0 - pad, lon1 + pad, max(lat0 - pad, -90), min(lat1 + pad, 90)
    lv = "-".join(str(int(l)) for l in levels)
    tag = f"C_{var}_{lv}_{time.replace(':', '')}_{lon0}_{lon1}_{lat0}_{lat1}.nc"
    f = J.CACHE / tag
    if f.exists():
        return xr.open_dataarray(f).load()
    ds = J.arco()
    da = ds[var].sel(time=time).sel(level=list(levels))
    da = da.sel(latitude=slice(lat1, lat0), longitude=slice(lon0 % 360, lon1 % 360)).load()
    da = da.assign_coords(longitude=(((da.longitude + 180) % 360) - 180))
    da.to_netcdf(f)
    return da


def fetch_series(var, times, extent, level=None, pad=6.0):
    """Fetch one field at many times in one request (cached)."""
    lon0, lon1, lat0, lat1 = extent
    lon0, lon1, lat0, lat1 = lon0 - pad, lon1 + pad, max(lat0 - pad, -90), min(lat1 + pad, 90)
    t0, t1 = times[0], times[-1]
    tag = f"C_ser_{var}_{level}_{t0.replace(':', '')}_{t1.replace(':', '')}_{len(times)}_{lon0}_{lon1}_{lat0}_{lat1}.nc"
    f = J.CACHE / tag
    if f.exists():
        return xr.open_dataarray(f).load()
    ds = J.arco()
    da = ds[var].sel(time=list(np.array(times, dtype="datetime64[ns]")))
    if level is not None:
        da = da.sel(level=level)
    da = da.sel(latitude=slice(lat1, lat0), longitude=slice(lon0 % 360, lon1 % 360)).load()
    da = da.assign_coords(longitude=(((da.longitude + 180) % 360) - 180))
    da.to_netcdf(f)
    return da


def smooth(da, n=1):
    """Simple 9-point (1-2-1) smoother applied n times, edges kept."""
    a = da.values.astype(float).copy()
    for _ in range(n):
        b = a.copy()
        b[1:-1, 1:-1] = (4 * a[1:-1, 1:-1] + 2 * (a[:-2, 1:-1] + a[2:, 1:-1] + a[1:-1, :-2] + a[1:-1, 2:])
                         + a[:-2, :-2] + a[:-2, 2:] + a[2:, :-2] + a[2:, 2:]) / 16.0
        a = b
    return da.copy(data=a)


def ddx_ddy(da):
    """Centred finite differences on a regular lat/lon grid (m^-1)."""
    R = 6.371e6
    lat = np.deg2rad(da.latitude.values)
    lon = np.deg2rad(da.longitude.values)
    a = da.values
    dfdlat = np.gradient(a, lat, axis=-2)
    dfdlon = np.gradient(a, lon, axis=-1)
    dx = dfdlon / (R * np.cos(lat)[:, None])
    dy = dfdlat / R
    return dx, dy


def rel_vort(u, v):
    R = 6.371e6
    lat = np.deg2rad(u.latitude.values)
    vx, _ = ddx_ddy(v)
    # d(u cos)/dy / cos
    ucos = u.values * np.cos(lat)[:, None]
    ducos = np.gradient(ucos, lat, axis=-2) / R
    zeta = vx - ducos / np.cos(lat)[:, None]
    return u.copy(data=zeta)


def divergence(u, v):
    R = 6.371e6
    lat = np.deg2rad(u.latitude.values)
    ux, _ = ddx_ddy(u)
    vcos = v.values * np.cos(lat)[:, None]
    dvcos = np.gradient(vcos, lat, axis=-2) / R
    return u.copy(data=ux + dvcos / np.cos(lat)[:, None])


def barbs_kt(ax, u, v, skip, length=4.2):
    """Thinned barbs in knots; thin by grid index (wrapper keeps jstyle look)."""
    return J.barbs(ax, u, v, skip=skip, length=length)


def arrow_label(ax, xy, xytext, text, fontsize=7, halo=False, **kw):
    """One minimal black annotation: short arrow + 1-3 word label (lon/lat inputs)."""
    import cartopy.crs as ccrs
    import matplotlib.patheffects as pe
    tr = ccrs.PlateCarree()._as_mpl_transform(ax)
    a = ax.annotate(text, xy=xy, xycoords=tr, xytext=xytext, textcoords=tr, fontsize=fontsize,
                    ha=kw.pop("ha", "center"), va=kw.pop("va", "center"), color="k", zorder=8,
                    arrowprops=dict(arrowstyle="-|>", lw=0.6, color="k", mutation_scale=6,
                                    shrinkA=1, shrinkB=1), **kw)
    if halo:
        a.set_path_effects([pe.withStroke(linewidth=1.8, foreground="white")])
    return a


def local_min(da, lon, lat, radius=4.0):
    """Location and value of the minimum of da within `radius` degrees of (lon, lat)."""
    sub = da.where((abs(da.latitude - lat) <= radius) & (abs(da.longitude - lon) <= radius / max(np.cos(np.deg2rad(lat)), 0.3)), drop=True)
    i = np.unravel_index(np.nanargmin(sub.values), sub.shape)
    return float(sub.longitude[i[1]]), float(sub.latitude[i[0]]), float(sub.values[i])


def local_max(da, lon, lat, radius=4.0):
    m = local_min(-da, lon, lat, radius)
    return m[0], m[1], -m[2]


def mark_site(ax, lon, lat, ms=3.5):
    """Small open black circle at a station location."""
    import cartopy.crs as ccrs
    ax.plot(lon, lat, "o", ms=ms, mfc="white", mec="k", mew=0.7, transform=ccrs.PlateCarree(), zorder=8)


def slots(fig, n=3, gaps=None, left=0.01, right=0.99, rel=None):
    """GridSpec slots of equal width with explicit gaps (fractions of figure width).

    gaps: list of n-1 gap widths; use a wider gap before a non-map panel that needs a y label.
    Returns list of SubplotSpecs usable by J.map_axes / fig.add_subplot.
    """
    from matplotlib.gridspec import GridSpec
    gaps = gaps if gaps is not None else [0.03] * (n - 1)
    w = (right - left - sum(gaps)) / n
    rel = rel if rel is not None else [1.0] * n
    rel = [r * n / sum(rel) for r in rel]
    ratios = []
    for k in range(n):
        ratios.append(w * rel[k])
        if k < n - 1:
            ratios.append(gaps[k])
    gs = GridSpec(1, len(ratios), figure=fig, width_ratios=ratios, wspace=0, left=left, right=right,
                  top=0.92, bottom=0.08)
    return [gs[2 * k] for k in range(n)]


def match_box(fig, ax_plain, ax_ref):
    """Give a non-map axes the same height/vertical position as a (colorbar-shrunk) map axes."""
    fig.canvas.draw()
    r = ax_ref.get_position()
    s = ax_plain.get_position()
    ax_plain.set_position([s.x0, r.y0, s.width, r.height])


def half_cmap(name="RdYlBu_r", lo=0.5, hi=1.0, n=256):
    import matplotlib as mpl
    base = mpl.colormaps[name]
    return mpl.colors.LinearSegmentedColormap.from_list(f"{name}_{lo}_{hi}", base(np.linspace(lo, hi, n)))


def finish():
    """ARCO/gcsfs threads keep the interpreter alive at exit; leave hard."""
    import os, sys
    sys.stdout.flush(); sys.stderr.flush()
    os._exit(0)


def barbs_clear(ax, u, v, skip, length=3.8, clear=()):
    """J.barbs, but drop barbs within r degrees of given (lon, lat, r) spots (keeps labels clean)."""
    u = u.copy(); v = v.copy()
    lon2, lat2 = np.meshgrid(u.longitude.values, u.latitude.values)
    m = np.zeros(lon2.shape, bool)
    for lo, la, r in clear:
        m |= (np.abs(lon2 - lo) * np.cos(np.deg2rad(la)) < r) & (np.abs(lat2 - la) < 0.6 * r)
    u = u.where(~m); v = v.where(~m)
    return J.barbs(ax, u, v, skip=skip, length=length)


def prune_edge_labels(ax, cs, frac=0.07):
    """Remove contour labels that sit within `frac` of the axes edges (avoids clipped labels)."""
    fig = ax.figure
    fig.canvas.draw()
    bb = ax.get_window_extent()
    for t in list(getattr(cs, "labelTexts", [])):
        x, y = ax.transData.transform(t.get_position())
        if (x < bb.x0 + frac * bb.width or x > bb.x1 - frac * bb.width or
                y < bb.y0 + frac * bb.height or y > bb.y1 - frac * bb.height):
            t.set_visible(False)


# ------------------------------------------------------------------ declutter (v3 polish)
def _pad_bb(bb, px):
    from matplotlib.transforms import Bbox
    return Bbox.from_extents(bb.x0 - px, bb.y0 - px, bb.x1 + px, bb.y1 + px)


def _boxes(ax, avoid, pad_pt):
    fig = ax.figure
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    px = pad_pt * fig.dpi / 72.0
    return [_pad_bb(t.get_window_extent(r), px) for t in avoid if t.get_visible()], r


def _coast_paths(ax):
    """Coastline and lake outlines inside the map, as display-coordinate vertex arrays."""
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    pc = ccrs.PlateCarree()
    x0, x1, y0, y1 = ax.get_extent(crs=pc)
    ext = (x0 - 1, x1 + 1, y0 - 1, y1 + 1)
    out = []
    for feat in (cfeature.COASTLINE.with_scale("50m"), cfeature.LAKES.with_scale("50m")):
        for g in feat.intersecting_geometries(ext):
            geoms = getattr(g, "geoms", [g])
            for gg in geoms:
                lines = [gg.exterior] + list(gg.interiors) if gg.geom_type == "Polygon" else [gg]
                for ln in lines:
                    xy = np.asarray(ln.coords)
                    if len(xy) < 2:
                        continue
                    pr = ax.projection.transform_points(pc, xy[:, 0], xy[:, 1])[:, :2]
                    out.append(ax.transData.transform(pr))
    return out


def clabel_avoid(ax, cs, avoid=(), levels=None, fmt="%d", fontsize=6, pad_pt=2.5, edge=0.0,
                 min_len=3.0, coast=True, cross=True):
    """Contour labels placed only inside the visible map, clear of `avoid` texts (city labels,
    annotations, L/H) and of each other: one label per visible stretch of each contour that is at
    least `min_len` label-widths long, as near the middle of the stretch as possible. Labels are
    chosen BEFORE the lines are broken, so no unlabeled gaps are left."""
    boxes, r = _boxes(ax, avoid, pad_pt)
    px = pad_pt * ax.figure.dpi / 72.0
    axbb = ax.get_window_extent(r)
    inner = _pad_bb(axbb, -max(2.0, edge * min(axbb.width, axbb.height)))
    trans = cs.get_transform()
    inv = ax.transData.inverted()
    keep, keep_lev, kept = [], [], []
    # every contour vertex drawn in this axes (all line ContourSets), tagged by component, so a
    # label is never placed where another line (or another branch of its own line) runs through it
    from matplotlib.contour import ContourSet
    from matplotlib.path import Path as MPath
    allxy, allid, allpaths = [], [], []
    comps = {}
    cid = 0
    for c in ax.collections:
        if not isinstance(c, ContourSet) or c.filled:
            continue
        tr_c = c.get_transform()
        for lev_c, p_c in zip(c.levels, c.get_paths()):
            if p_c is None or len(p_c.vertices) == 0:
                continue
            for sub_c in p_c._iter_connected_components():
                v = tr_c.transform(sub_c.vertices)
                allxy.append(v); allid.append(np.full(len(v), cid))
                allpaths.append((cid, MPath(v)))
                if c is cs:
                    comps[(float(lev_c), len(comps))] = cid
                cid += 1
    if coast:
        for v in _coast_paths(ax):
            allpaths.append((-1, MPath(v)))
    allxy = np.concatenate(allxy) if allxy else np.zeros((0, 2))
    allid = np.concatenate(allid) if allid else np.zeros(0, int)
    own_ids = list(comps.values())
    ci = 0
    for lev, path in zip(cs.levels, cs.get_paths()):
        if path is None or len(path.vertices) == 0:
            continue
        for sub in path._iter_connected_components():
            my_id = own_ids[ci]; ci += 1
            if levels is not None and lev not in levels:
                continue
            xy = trans.transform(sub.vertices)
            arc_full = np.r_[0.0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
            mine = allid == my_id
            ins = ((xy[:, 0] > inner.x0) & (xy[:, 0] < inner.x1) & (xy[:, 1] > inner.y0) & (xy[:, 1] < inner.y1))
            # runs of consecutive inside points
            k = 0
            n = len(xy)
            while k < n:
                if not ins[k]:
                    k += 1
                    continue
                k0 = k
                while k < n and ins[k]:
                    k += 1
                run = xy[k0:k]
                if len(run) < 3:
                    continue
                seg = np.r_[0.0, np.cumsum(np.hypot(*np.diff(run, axis=0).T))]
                # label width estimate from a trial label
                ax.clabel(cs, levels=[lev], fmt=fmt, fontsize=fontsize, inline=False,
                          manual=[inv.transform(run[len(run) // 2])])
                w = cs.labelTexts[-1].get_window_extent(r).width
                cs.pop_label()
                if seg[-1] < min_len * w:
                    continue
                order = np.argsort(np.abs(seg - 0.5 * seg[-1]))
                lo, hi = 0.5 * w, seg[-1] - 0.5 * w
                for q in order[:: max(1, len(order) // 40)]:
                    if not (lo <= seg[q] <= hi):
                        continue
                    pos = inv.transform(run[q])
                    ax.clabel(cs, levels=[lev], fmt=fmt, fontsize=fontsize, inline=False, manual=[pos])
                    bb = cs.labelTexts[-1].get_window_extent(r)
                    cs.pop_label()
                    okin = bb.x0 >= inner.x0 and bb.x1 <= inner.x1 and bb.y0 >= inner.y0 and bb.y1 <= inner.y1
                    clear = not any(bb.overlaps(b) for b in boxes)
                    apart = not any(_pad_bb(bb, px).overlaps(b) for b in kept)
                    near = np.nonzero(np.abs(arc_full - arc_full[k0 + q]) <= 0.6 * w + 3.0)[0]
                    a_, b_ = near.min(), near.max()
                    bq = _pad_bb(bb, 1.0)
                    crossed = any(pp.intersects_bbox(bq, filled=False) for cc, pp in allpaths
                                  if cc != my_id and (cross or cc == -1))
                    if cross and not crossed:
                        for piece in (xy[:a_], xy[b_ + 1:]):
                            if len(piece) >= 2 and MPath(piece).intersects_bbox(bq, filled=False):
                                crossed = True
                                break
                    if okin and clear and apart and not crossed:
                        keep.append(pos); keep_lev.append(lev); kept.append(bb)
                        break
    if keep:
        ax.clabel(cs, levels=sorted(set(keep_lev)), fmt=fmt, fontsize=fontsize, inline=True,
                  inline_spacing=2, manual=keep)
    return cs


def barbs_avoid(ax, u, v, skip, length=3.8, avoid=(), pad_pt=4.0, clear=(), staff_pt=7.0):
    """J.barbs, but drop thinned barbs whose base lies within pad_pt of any `avoid` text, and
    within (lon, lat, r) `clear` spots (as barbs_clear)."""
    import cartopy.crs as ccrs
    boxes, r = _boxes(ax, avoid, pad_pt)
    u = u.copy(); v = v.copy()
    lon2, lat2 = np.meshgrid(u.longitude.values, u.latitude.values)
    m = np.zeros(lon2.shape, bool)
    for lo, la, rr in clear:
        m |= (np.abs(lon2 - lo) * np.cos(np.deg2rad(la)) < rr) & (np.abs(lat2 - la) < 0.6 * rr)
    sub = np.zeros(lon2.shape, bool)
    sub[::skip, ::skip] = True
    ii, jj = np.nonzero(sub)
    xyz = ax.projection.transform_points(ccrs.PlateCarree(), lon2[ii, jj], lat2[ii, jj])
    disp = ax.transData.transform(xyz[:, :2])
    uu = u.values[ii, jj]; vv = v.values[ii, jj]
    sp = np.hypot(uu, vv); sp[sp == 0] = 1.0
    ptx = ax.figure.dpi / 72.0
    for k, (x, y) in enumerate(disp):
        dx, dy = -uu[k] / sp[k], -vv[k] / sp[k]          # staff points upwind
        pts = [(x + f * staff_pt * ptx * dx, y + f * staff_pt * ptx * dy) for f in (0.0, 0.5, 1.0)]
        if any(b.contains(px_, py_) for b in boxes for px_, py_ in pts):
            m[ii[k], jj[k]] = True
    u = u.where(~m); v = v.where(~m)
    return J.barbs(ax, u, v, skip=skip, length=length)


def halo_text(ax, lon, lat, text, fontsize=6.5, **kw):
    """Plain haloed in-map label at lon/lat."""
    import cartopy.crs as ccrs
    import matplotlib.patheffects as pe
    return ax.text(lon, lat, text, transform=ccrs.PlateCarree(), fontsize=fontsize, zorder=9,
                   ha=kw.pop("ha", "center"), va=kw.pop("va", "center"),
                   path_effects=[pe.withStroke(linewidth=1.8, foreground="white")], **kw)


def check_layout(fig, axes, cbars=()):
    """Print warnings when a panel title runs past the next panel / figure, or a colorbar label
    is wider than its colorbar."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    fw = fig.bbox.width
    for k, ax in enumerate(axes):
        t = ax._left_title
        tb = t.get_window_extent(r)
        lim = axes[k + 1].get_window_extent(r).x0 - 4 if k + 1 < len(axes) else fw
        # allow a non-map next panel's y-label region: compare with its tight bbox
        if k + 1 < len(axes):
            lim = min(lim, axes[k + 1].get_tightbbox(r).x0 - 4)
        status = "OK" if tb.x1 <= lim else "OVERFLOW"
        print(f"title[{k}] '{t.get_text()}' x1={tb.x1:.0f} limit={lim:.0f} {status}")
    for k, cb in enumerate(cbars):
        lb = cb.ax.xaxis.label.get_window_extent(r)
        cbb = cb.ax.get_window_extent(r)
        status = "OK" if lb.width <= cbb.width + 2 else "WIDE"
        print(f"cbar[{k}] '{cb.ax.xaxis.label.get_text()}' w={lb.width:.0f} cb={cbb.width:.0f} {status}")
