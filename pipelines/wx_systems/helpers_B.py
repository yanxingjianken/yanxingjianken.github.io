"""Group-B helpers on top of jstyle (do not edit jstyle.py; it is shared)."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import numpy as np
import xarray as xr
import matplotlib.ticker as mticker

import jstyle as J

G = 9.80665
OUT = J.ROOT.parent.parent / "images" / "wx_systems_v3"

# Shared extents (lon0, lon1, lat0, lat1) so same-scale systems are framed alike.
EXT_NE = (-82.0, -66.0, 37.0, 47.5)       # Northeast regional (mesoscale / synoptic-local)
EXT_CAD = (-86.0, -70.0, 31.5, 44.0)      # Carolinas-Virginia piedmont, east of Appalachians
EXT_GL = (-90.0, -74.0, 40.0, 48.5)       # Great Lakes


def getmany(reqs, extent, pad=6.0, workers=6):
    """Fetch a list of (var, time, level) in parallel; returns list of DataArrays."""
    J.arco()  # open once in the main thread
    def one(r):
        var, t, lev = r
        return safe_fetch(var, t, extent, lev, pad)
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(one, reqs))


def _cache_file(var, time, extent, level, pad):
    lon0, lon1, lat0, lat1 = extent
    lon0, lon1, lat0, lat1 = lon0 - pad, lon1 + pad, max(lat0 - pad, -90), min(lat1 + pad, 90)
    return J.CACHE / f"{var}_{level if level is not None else 'sfc'}_{time.replace(':', '')}_{lon0}_{lon1}_{lat0}_{lat1}.nc"


def safe_fetch(var, t, extent, lev=None, pad=6.0):
    """J.fetch, but a cache file left truncated by a killed run is deleted and re-fetched."""
    try:
        return J.fetch(var, t, extent, level=lev, pad=pad)
    except (OSError, ValueError, RuntimeError, KeyError):
        f = _cache_file(var, t, extent, lev, pad)
        if f.exists():
            f.unlink()
        return J.fetch(var, t, extent, level=lev, pad=pad)


def column(var, t, extent, levels, pad=0.0, workers=8):
    """Fetch var on several pressure levels -> DataArray(level, lat, lon)."""
    das = getmany([(var, t, l) for l in levels], extent, pad=pad, workers=workers)
    return xr.concat([d.drop_vars("level", errors="ignore") for d in das],
                     dim=xr.DataArray(list(levels), dims="level", name="level"))


def dewpoint_from_q(q, p_hpa):
    """Dewpoint (°C) from specific humidity (kg/kg) and pressure (hPa) (Bolton 1980)."""
    e = q * p_hpa / (0.622 + 0.378 * q)
    ln = np.log(np.maximum(e, 1e-6) / 6.112)
    return 243.5 * ln / (17.67 - ln)


def pressure_axis(ax, pmax=1000, pmin=500, ticks=(1000, 925, 850, 700, 600, 500)):
    ax.set_yscale("log")
    ax.set_ylim(pmax, pmin)
    ax.yaxis.set_major_locator(mticker.FixedLocator(ticks))
    ax.yaxis.set_minor_locator(mticker.NullLocator())
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))
    ax.set_ylabel("Pressure (hPa)")
    for sp in ax.spines.values():
        sp.set_linewidth(0.6)
        sp.set_edgecolor("k")
    ax.tick_params(which="both", top=True, right=True)


def arrow_label(ax, xy, xytext, text, fontsize=7):
    """Minimal black arrow + short label, both given in lon/lat."""
    import cartopy.crs as ccrs
    tr = ccrs.PlateCarree()._as_mpl_transform(ax)
    ax.annotate(text, xy=xy, xycoords=tr, xytext=xytext, textcoords=tr, fontsize=fontsize,
                ha="center", va="center", zorder=8,
                arrowprops=dict(arrowstyle="-|>", lw=0.6, color="k", mutation_scale=6,
                                shrinkA=1, shrinkB=1))


def label_text(ax, lon, lat, text, fontsize=7, **kw):
    J.mark(ax, lon, lat, text, fontsize=fontsize, fontweight=kw.pop("fontweight", "normal"), **kw)


def ddx_ddy(f):
    """Centered derivatives of a lat/lon field in m^-1 (spherical, 0.25 deg grid)."""
    R = 6.371e6
    lat = np.deg2rad(f.latitude)
    lon = np.deg2rad(f.longitude)
    dfdlon = f.differentiate("longitude") * 180 / np.pi   # per radian
    dfdlat = f.differentiate("latitude") * 180 / np.pi
    dfdx = dfdlon / (R * np.cos(lat))
    dfdy = dfdlat / R
    return dfdx, dfdy


def smooth(da, n=1):
    """Light 1-2-1 smoother, n passes (to keep derivative fields readable on 0.25 deg)."""
    out = da
    for _ in range(n):
        out = out.rolling(latitude=3, center=True, min_periods=1).mean()
        out = out.rolling(longitude=3, center=True, min_periods=1).mean()
    return out


def nearest(da, lon, lat):
    return float(da.sel(longitude=lon, latitude=lat, method="nearest"))


def finish():
    """Exit immediately after the work is done.

    The gcsfs/fsspec event-loop thread opened by jstyle.arco() keeps the interpreter from
    exiting on Windows (the script finishes its work and then hangs at shutdown), so scripts
    call this at the end."""
    import os, sys
    sys.stdout.flush(); sys.stderr.flush()
    os._exit(0)


def cloud_cmap(lo=0.3):
    """Greys_r starting at mid-grey instead of black, so black contours stay visible over clear sky."""
    import matplotlib as mpl
    import matplotlib.colors as mcolors
    return mcolors.ListedColormap(mpl.colormaps["Greys_r"](np.linspace(lo, 1.0, 256)), name="Greys_r_trunc")


def crop(da, extent, m=3.0):
    """Subset a field to the map extent plus a margin, so contour labels land inside the panel."""
    lon0, lon1, lat0, lat1 = extent
    return da.sel(longitude=slice(lon0 - m, lon1 + m), latitude=slice(lat1 + m, lat0 - m))


def contour(ax, da, levels, fmt="%d", margin_px=14, **kw):
    """J.contour, but labels that would be clipped at the panel edge are dropped.

    jstyle.contour labels contours anywhere in the padded fetch box, so some labels land
    outside the map or half-cut at its frame."""
    cs = J.contour(ax, da, levels, label=False, **kw)
    texts = ax.clabel(cs, fmt=fmt, fontsize=6, inline=True, inline_spacing=2)
    fig = ax.figure
    fig.canvas.draw()
    bb = ax.get_window_extent()
    for t in list(texts):
        e = t.get_window_extent()
        if (e.x0 < bb.x0 + 2 or e.x1 > bb.x1 - 2 or e.y0 < bb.y0 + 2 or e.y1 > bb.y1 - 2):
            t.remove()
        else:
            ax.__dict__.setdefault("_hb_clabels", []).append(t)
    return cs


def declutter(ax, barb_px=11, pad_px=2):
    """Remove contour labels (drawn via helpers_B.contour) that collide with annotation text
    or sit on a wind-barb base. Call after everything else is drawn on the panel."""
    import matplotlib.collections as mcoll
    from matplotlib.quiver import Barbs
    fig = ax.figure
    fig.canvas.draw()
    labels = [t for t in ax.__dict__.get("_hb_clabels", []) if t.axes is ax]
    others = [t for t in ax.texts if t not in labels and t.get_visible()]
    obox = [t.get_window_extent().expanded(1.0, 1.0) for t in others]
    pts = []
    for c in ax.collections:
        if isinstance(c, Barbs):
            pts.append(c.get_offset_transform().transform(c.get_offsets()))
    pts = np.vstack(pts) if pts else np.empty((0, 2))
    for t in labels:
        e = t.get_window_extent()
        x0, x1, y0, y1 = e.x0 - pad_px, e.x1 + pad_px, e.y0 - pad_px, e.y1 + pad_px
        hit = any(not (x1 < o.x0 or x0 > o.x1 or y1 < o.y0 or y0 > o.y1) for o in obox)
        if not hit and len(pts):
            hit = bool(((pts[:, 0] > x0 - barb_px) & (pts[:, 0] < x1 + barb_px) &
                        (pts[:, 1] > y0 - barb_px) & (pts[:, 1] < y1 + barb_px)).any())
        if hit:
            t.remove()


def _avoid_points(ax):
    """Display coords of barb bases and annotation-text centres already on the panel."""
    from matplotlib.quiver import Barbs
    pts = []
    for c in ax.collections:
        if isinstance(c, Barbs):
            pts.append(c.get_offset_transform().transform(c.get_offsets()))
    ax.figure.canvas.draw()
    for t in ax.texts:
        e = t.get_window_extent()
        xs = np.linspace(e.x0, e.x1, 5)
        pts.append(np.c_[xs, np.full(5, 0.5 * (e.y0 + e.y1))])
    return np.vstack(pts) if pts else np.empty((0, 2))


FINGER_LAKES = [(x, y) for x in np.arange(-77.4, -76.35, 0.25) for y in np.arange(42.35, 43.0, 0.2)]  # small lake outlines that clash with labels


def contour_smart(ax, da, levels, fmt="%d", every=1, min_sep=16, edge=22, avoid_lonlat=FINGER_LAKES, **kw):
    """Contours (via jstyle.contour, unlabelled) plus at most one 6-pt label per labelled level,
    placed at the point of that contour farthest from barbs, annotations and other labels.
    Draw shading, barbs and annotations first."""
    cs = J.contour(ax, da, levels, label=False, **kw)
    avoid = _avoid_points(ax)
    if avoid_lonlat:
        import cartopy.crs as ccrs
        xy = np.array(avoid_lonlat, float)
        pp = ax.projection.transform_points(ccrs.PlateCarree(), xy[:, 0], xy[:, 1])[:, :2]
        avoid = np.vstack([avoid, ax.transData.transform(pp)])
    bb = ax.get_window_extent()
    tr = cs.get_transform()
    chosen, chosen_lev = [], []
    levs = list(cs.levels)
    for i, lev in enumerate(levs):
        if i % every:
            continue
        p = cs.get_paths()[i]
        if len(p.vertices) == 0:
            continue
        try:
            disp = tr.transform(p.vertices)
        except Exception:
            continue
        ok = ((disp[:, 0] > bb.x0 + edge) & (disp[:, 0] < bb.x1 - edge) &
              (disp[:, 1] > bb.y0 + edge * 0.6) & (disp[:, 1] < bb.y1 - edge * 0.6))
        cand = disp[ok]
        if len(cand) == 0:
            continue
        ref = np.vstack([avoid] + [np.array(chosen)] if chosen else [avoid]) if len(avoid) or chosen else None
        if ref is None or len(ref) == 0:
            best = cand[len(cand) // 2]
            score = 1e9
        else:
            d = np.sqrt(((cand[:, None, :] - ref[None, :, :]) ** 2).sum(-1)).min(1)
            k = int(d.argmax())
            best, score = cand[k], d[k]
        if score < min_sep:
            continue
        chosen.append(best)
        chosen_lev.append(lev)
    if chosen:
        # one clabel call: inline labelling rewrites the paths, so all positions are chosen first
        xy = [tuple(ax.transData.inverted().transform(c)) for c in chosen]
        ax.clabel(cs, levels=chosen_lev, manual=xy, fmt=fmt, fontsize=6, inline=True, inline_spacing=2)
    return cs


def _line_points(ax, step_px=2.0):
    """Densified display-space points of every contour line on the panel."""
    from matplotlib.contour import ContourSet
    out = []
    for c in ax.collections:
        if isinstance(c, ContourSet) and c.filled is False:
            tr = c.get_transform()
            for p in c.get_paths():
                if len(p.vertices) < 2:
                    continue
                try:
                    d = tr.transform(p.vertices)
                except Exception:
                    continue
                codes = p.codes
                for a, b, cb in zip(d[:-1], d[1:], (codes[1:] if codes is not None else [2] * (len(d) - 1))):
                    if cb == 1:            # MOVETO: new segment, no line between a and b
                        continue
                    n = max(int(np.hypot(*(b - a)) / step_px), 1)
                    t = np.linspace(0, 1, n + 1)[:, None]
                    out.append(a + t * (b - a))
    return np.vstack(out) if out else np.empty((0, 2))


def smart_arrow(ax, target, text, fontsize=7, rmin=45, rmax=150, barb_px=12, prefer=None, avoid_lonlat=None,
                arrow=True, text_kw=None):
    """Arrow + label like arrow_label, but the label is put at the free spot (no contour line,
    barb, or other text under it) nearest to `target` (lon, lat). Call after everything else
    except declutter. `prefer` = (dx, dy) display direction to favour."""
    import cartopy.crs as ccrs
    fig = ax.figure
    fig.canvas.draw()
    tgt = ax.transData.transform(ax.projection.transform_point(target[0], target[1], ccrs.PlateCarree()))
    probe = ax.text(0, 0, text, fontsize=fontsize, transform=None)
    e = probe.get_window_extent(renderer=fig.canvas.get_renderer())
    w, h = e.width, e.height
    probe.remove()
    lines = _line_points(ax)
    others = _avoid_points(ax)
    extra = FINGER_LAKES + list(avoid_lonlat or [])
    xy = np.array(extra, float)
    pp = ax.projection.transform_points(ccrs.PlateCarree(), xy[:, 0], xy[:, 1])[:, :2]
    others = np.vstack([others, ax.transData.transform(pp)])
    bb = ax.get_window_extent()
    best, bestd = None, 1e9
    for x in np.arange(bb.x0 + w / 2 + 4, bb.x1 - w / 2 - 4, 4.0):
        for y in np.arange(bb.y0 + h / 2 + 4, bb.y1 - h / 2 - 4, 4.0):
            d = np.hypot(x - tgt[0], y - tgt[1])
            if d < rmin or d > rmax:
                continue
            x0, x1, y0, y1 = x - w / 2 - 2, x + w / 2 + 2, y - h / 2 - 2, y + h / 2 + 2
            if len(lines) and ((lines[:, 0] > x0) & (lines[:, 0] < x1) & (lines[:, 1] > y0) & (lines[:, 1] < y1)).any():
                continue
            if len(others) and ((others[:, 0] > x0 - barb_px) & (others[:, 0] < x1 + barb_px) &
                                (others[:, 1] > y0 - barb_px) & (others[:, 1] < y1 + barb_px)).any():
                continue
            score = d
            if prefer is not None:
                v = np.array([x - tgt[0], y - tgt[1]]) / d
                score = d * (1.5 - 0.5 * float(v @ np.asarray(prefer) / np.linalg.norm(prefer)))
            if score < bestd:
                best, bestd = (x, y), score
    if best is None:
        raise RuntimeError(f"no free spot for label {text!r}")
    lon, lat = ccrs.PlateCarree().transform_point(*ax.transData.inverted().transform(best), ax.projection)
    if arrow:
        arrow_label(ax, tuple(target), (lon, lat), text, fontsize=fontsize)
    else:                                   # plain place-name label at the free spot (no arrow)
        import matplotlib.patheffects as pe
        ax.text(lon, lat, text, transform=ccrs.PlateCarree(), fontsize=fontsize, ha="center", va="center",
                zorder=8, path_effects=[pe.withStroke(linewidth=1.8, foreground="white")], **(text_kw or {}))
    return lon, lat


def _barb_points(ax, step_px=1.5):
    """Densified display-space points along every wind barb drawn on the panel."""
    from matplotlib.quiver import Barbs
    out = []
    for c in ax.collections:
        if not isinstance(c, Barbs):
            continue
        offs = c.get_offset_transform().transform(c.get_offsets())
        M = c.get_transforms()
        for i, (p, o) in enumerate(zip(c.get_paths(), offs)):
            v = p.vertices
            if len(M):
                m = M[i % len(M)]
                v = v @ m[:2, :2].T + m[:2, 2]
            d = v + o
            for a, b in zip(d[:-1], d[1:]):
                n = max(int(np.hypot(*(b - a)) / step_px), 1)
                t = np.linspace(0, 1, n + 1)[:, None]
                out.append(a + t * (b - a))
    return np.vstack(out) if out else np.empty((0, 2))


def place_cities(ax, names, prefer=None, extra=None, pad_px=1.5):
    """cities.add, but each label goes to the first position (from `prefer[name]` then a fixed
    order) whose box is free of barbs, other text and the panel frame; contour lines are a soft
    penalty. Call after shading/contours/barbs and before contour_smart/smart_arrow/declutter.
    Returns {name: chosen position}."""
    import cities
    prefer = prefer or {}
    order = ["right", "left", "above", "below", "ur", "ul", "lr", "ll"]
    fig = ax.figure
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    import cartopy.crs as ccrs
    bpts = _barb_points(ax)
    fl = np.array(FINGER_LAKES, float)                  # small lake outlines that clash with labels
    pp = ax.projection.transform_points(ccrs.PlateCarree(), fl[:, 0], fl[:, 1])[:, :2]
    bpts = np.vstack([bpts, ax.transData.transform(pp)])
    lpts = _line_points(ax)
    bb = ax.get_window_extent()
    chosen = {}
    for name in names:
        cand = ([prefer[name]] if name in prefer else []) + [o for o in order if o != prefer.get(name)]
        best = None
        for k, pos in enumerate(cand):
            nl = len(ax.lines)
            ts = cities.add(ax, [name], where={name: pos}, extra=extra)
            if not ts:
                break                                   # outside the map
            t = ts[0]
            e = t.get_window_extent(renderer=r)
            x0, x1, y0, y1 = e.x0 - pad_px, e.x1 + pad_px, e.y0 - pad_px, e.y1 + pad_px
            inside = x0 > bb.x0 + 2 and x1 < bb.x1 - 2 and y0 > bb.y0 + 2 and y1 < bb.y1 - 2
            nb = int(((bpts[:, 0] > x0) & (bpts[:, 0] < x1) & (bpts[:, 1] > y0) & (bpts[:, 1] < y1)).sum()) if len(bpts) else 0
            others = [o for o in ax.texts if o is not t and o.get_visible()]
            nt = sum(1 for o in others if not (x1 < (oe := o.get_window_extent(renderer=r)).x0 or x0 > oe.x1
                                                or y1 < oe.y0 or y0 > oe.y1))
            nline = int(((lpts[:, 0] > x0) & (lpts[:, 0] < x1) & (lpts[:, 1] > y0) & (lpts[:, 1] < y1)).sum()) if len(lpts) else 0
            score = (0 if inside else 1e6) + 1000 * nb + 1000 * nt + 2 * nline + k
            t.remove()
            for ln in ax.lines[nl:]:
                ln.remove()
            if best is None or score < best[0]:
                best = (score, pos)
            if score == k:                              # perfectly free spot in preference order
                break
        if best is not None:
            nl = len(ax.lines)
            cities.add(ax, [name], where={name: best[1]}, extra=extra)
            chosen[name] = best[1]
            if best[0] >= 1000:
                print(f"place_cities: {name!r} label still overlaps something (score {best[0]:.0f})")
            for ln in ax.lines[nl:]:                    # later labels must not cover this dot
                xy = ax.transData.transform(np.c_[ln.get_xdata(), ln.get_ydata()])
                ring = xy[:, None, :] + 3.0 * np.array([[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]])[None]
                bpts = np.vstack([bpts, ring.reshape(-1, 2)])
    return chosen


def t_above_ground(T, sp, dp=30.0):
    """Temperature dp hPa above the surface (~250 m for dp=30), by log-p interpolation.

    T: dict {level_hPa: DataArray K}; sp: surface pressure (Pa)."""
    import xarray as xr
    target = sp / 100.0 - dp
    levs = sorted(T, reverse=True)
    out = xr.full_like(sp, np.nan, dtype=float)
    for lo, hi in zip(levs[:-1], levs[1:]):
        w = (np.log(lo) - np.log(target)) / (np.log(lo) - np.log(hi))
        val = T[lo] + w * (T[hi] - T[lo])
        sel = (target <= lo) & (target > hi)
        out = out.where(~sel, val)
    return out
