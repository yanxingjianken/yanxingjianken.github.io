"""Map of one issue time and surface, in the style of a journal figure (sans-serif annotations, thin frames, panel
letters, no title; the page supplies the title, key and caption): four stacked Northern-Hemisphere panels (10-90 N,
rectangular), one per method. Each shows the smoothed analysis at the end of the 24-h window with contours at the
fixed values used for the events (PV every 0.5 PVU, theta every 5 K), the folds present at that time (thin),
the jet axis, the onsets of the window with their own folded contours (bold, drawn at their onset times), and the
method's alarm regions issued 24 h earlier."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import ListedColormap  # noqa: E402

import core  # noqa: E402
import events as E  # noqa: E402
from config import PV_LEVELS, TH_LEVELS  # noqa: E402

METHODS = (("uc", "U − c matching"), ("opus", "Opus model"), ("amp", "Wave amplitude (no forecast)"),
           ("gfs", "GFS 24-h forecast"))
C_HIT, C_FALSE, C_MISS, C_JET = "#1a9850", "#d73027", "#f46d43", "#1b3a6b"
LAT_LO = 10.0
plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Helvetica", "Arial", "Nimbus Sans", "Liberation Sans", "DejaVu Sans"],
                     "font.size": 8, "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
                     "xtick.major.size": 2.5, "ytick.major.size": 2.5, "xtick.direction": "out",
                     "ytick.direction": "out"})


def _coast(ax):
    try:
        import cartopy.feature as cfeature
        for geom in cfeature.COASTLINE.with_scale("110m").geometries():
            for line in getattr(geom, "geoms", [geom]):
                x, y = np.asarray(line.coords).T
                x = np.mod(x, 360.0)
                br = np.flatnonzero(np.abs(np.diff(x)) > 180) + 1
                for xs, ys in zip(np.split(x, br), np.split(y, br)):
                    ax.plot(xs, ys, color="#6b8fb3", lw=0.35, zorder=3)
    except Exception:
        pass


def _line(ax, lon, lat, **kw):
    """Polyline in longitude 0..360, broken where it crosses the date line of the map edge."""
    lon, lat = np.asarray(lon), np.asarray(lat)
    br = np.flatnonzero(np.abs(np.diff(lon)) > 180) + 1
    for xs, ys in zip(np.split(lon, br), np.split(lat, br)):
        ax.plot(xs, ys, **kw)


def draw(rec, name, q_end, objs_end, onset_objs, masks, path):
    """rec: the surface record of the issue; q_end: the analysis at the end of the window; objs_end: breaking objects
    then (with their folded contour pieces); onset_objs: the window's new breakings as found at their onset times;
    masks: {method: alarm mask}."""
    pv = name.startswith("pv")
    field = E.smooth(q_end) if pv else -E.smooth(q_end)
    levels = np.array(PV_LEVELS if pv else TH_LEVELS, float)
    lab = "PV (PVU)" if pv else "θ (K)"
    fig, axs = plt.subplots(len(METHODS), 1, figsize=(6.5, 7.1), sharex=True)
    for n, (ax, (m, title)) in enumerate(zip(axs, METHODS)):
        im = ax.contourf(E.LON, E.LAT, field, levels=levels, cmap="Greys" if pv else "Greys_r", extend="both",
                         alpha=0.55, zorder=1)
        ax.contour(E.LON, E.LAT, field, levels=levels, colors="0.35", linewidths=0.3, zorder=2)
        _coast(ax)
        for o in objs_end:                                   # folds present at the end of the window
            for lev, lo, la in o["folds"]:
                _line(ax, lo, la, color="0.25", lw=0.8, zorder=5)
        for o in onset_objs:                                 # the new breakings, at their onset times
            for lev, lo, la in o["folds"]:
                _line(ax, lo, la, color="black", lw=1.6, zorder=5)
        _line(ax, E.LON, rec["jet_axis_end"], color=C_JET, lw=1.0, zorder=5)
        res = rec["methods"].get(m)
        if res is None:
            ax.text(180, 50, "no forecast available for this issue time", ha="center", va="center")
        else:
            labels, nreg = core.regions(masks[m])
            ok = np.zeros(labels.shape)
            for r, reg in enumerate(res["regions"], start=1):
                ok[labels == r] = 2 if reg["confirmed"] else 1
            ax.contourf(E.LON, E.LAT, ok, levels=[0.5, 1.5, 2.5], colors=[C_FALSE, C_HIT], alpha=0.33, zorder=4)
            ax.contour(E.LON, E.LAT, (ok > 0).astype(float), levels=[0.5], colors="0.15", linewidths=0.5, zorder=4)
            for o, hit in zip(rec["onsets"], res["onset_hits"]):
                ax.plot(o["lon"], o["lat"], marker="^" if o["type"] == "AWB" else "o", ms=6,
                        mfc=C_HIT if hit else "white", mec="black" if hit else C_MISS, mew=1.4, zorder=6)
            nh = sum(res["onset_hits"])
            nf = sum(not r["confirmed"] for r in res["regions"])
            ax.text(1.0, 1.03, f"onsets hit {nh} of {len(res['onset_hits'])}   alarm regions {len(res['regions'])},"
                    f" false {nf}", transform=ax.transAxes, ha="right", va="bottom", fontsize=7)
        ax.text(0.0, 1.03, f"({'abcd'[n]}) {title}", transform=ax.transAxes, ha="left", va="bottom", fontsize=8.5,
                fontweight="bold")
        ax.set_ylim(LAT_LO, 90)
        ax.set_xlim(0, 360)
        ax.set_yticks([30, 60])
        ax.set_yticklabels(["30°N", "60°N"])
    axs[-1].set_xticks(np.arange(0, 361, 60))
    axs[-1].set_xticklabels(["0°", "60°E", "120°E", "180°", "120°W", "60°W", "0°"])
    fig.subplots_adjust(left=0.07, right=0.9, top=0.96, bottom=0.04, hspace=0.3)
    cax = fig.add_axes([0.915, 0.3, 0.015, 0.4])
    cb = fig.colorbar(im, cax=cax, orientation="vertical", ticks=levels[1::4] if pv else levels[::4])
    cb.set_label(lab)
    cb.outline.set_linewidth(0.5)
    fig.savefig(path, dpi=170)
    plt.close(fig)
