"""Reference-city dots for the ERA5 maps (orientation aids for lay readers).

Usage (after shading/contours/barbs, before any declutter call):
    import cities
    cities.add(ax, ["Boston", "New York", "Albany"])
    cities.add(ax, ["Buffalo"], where={"Buffalo": "left"})

Small black dot + 6.5-pt label with a white halo, so labels stay legible on shading.
Cities outside the visible map (with a small inner margin) are skipped silently.
`where` per city: "right" (default), "left", "above", "below", "ul", "ur", "ll", "lr",
or an explicit (dx_pt, dy_pt, ha, va) tuple.
"""
from __future__ import annotations

import matplotlib.patheffects as pe

CITIES = {
    # Northeast
    "Boston": (-71.06, 42.36), "Worcester": (-71.80, 42.26), "Providence": (-71.41, 41.82),
    "Hartford": (-72.67, 41.76), "New York": (-74.01, 40.71), "Albany": (-73.75, 42.65),
    "Buffalo": (-78.88, 42.89), "Syracuse": (-76.15, 43.05), "Rochester": (-77.61, 43.16),
    "Elmira": (-76.81, 42.09), "Philadelphia": (-75.17, 39.95), "Washington": (-77.04, 38.90),
    "Baltimore": (-76.61, 39.29), "Pittsburgh": (-79.99, 40.44), "Portland": (-70.26, 43.66),
    "Concord": (-71.54, 43.21), "Manchester": (-71.46, 42.99), "Burlington": (-73.21, 44.48),
    "Nantucket": (-70.10, 41.28), "Bangor": (-68.77, 44.80), "Montreal": (-73.57, 45.50),
    "Quebec City": (-71.21, 46.81), "Toronto": (-79.38, 43.65), "Halifax": (-63.57, 44.65),
    "Norfolk": (-76.29, 36.85), "Richmond": (-77.44, 37.54), "Raleigh": (-78.64, 35.78),
    "Charlotte": (-80.84, 35.23), "Atlanta": (-84.39, 33.75), "Cleveland": (-81.69, 41.50),
    "Detroit": (-83.05, 42.33), "Chicago": (-87.63, 41.88), "Columbus": (-83.00, 39.96),
    "Indianapolis": (-86.16, 39.77), "St. Louis": (-90.20, 38.63), "Minneapolis": (-93.27, 44.98),
    "Nashville": (-86.78, 36.16), "Charleston": (-79.93, 32.78), "Miami": (-80.19, 25.76),
    # Plains / West
    "Oklahoma City": (-97.52, 35.47), "Moore": (-97.49, 35.34), "Dallas": (-96.80, 32.78),
    "Wichita": (-97.34, 37.69), "Amarillo": (-101.83, 35.22), "Denver": (-104.99, 39.74),
    "Kansas City": (-94.58, 39.10), "Los Angeles": (-118.24, 34.05), "San Diego": (-117.16, 32.72),
    "Las Vegas": (-115.14, 36.17), "Salt Lake City": (-111.89, 40.76), "Phoenix": (-112.07, 33.45),
    "San Francisco": (-122.42, 37.77),
}

_POS = {
    "right": (3.0, 0.0, "left", "center"), "left": (-3.0, 0.0, "right", "center"),
    "above": (0.0, 2.5, "center", "bottom"), "below": (0.0, -2.5, "center", "top"),
    "ur": (2.2, 1.8, "left", "bottom"), "ul": (-2.2, 1.8, "right", "bottom"),
    "lr": (2.2, -1.8, "left", "top"), "ll": (-2.2, -1.8, "right", "top"),
}


def add(ax, names, where=None, fontsize=6.5, ms=2.4, margin=0.03, extra=None):
    """Plot dots + haloed labels for `names` (keys of CITIES or of `extra` {name: (lon, lat)})."""
    import cartopy.crs as ccrs
    from matplotlib.transforms import offset_copy
    pc = ccrs.PlateCarree()
    where = where or {}
    table = dict(CITIES, **(extra or {}))
    fig = ax.figure
    out = []
    for name in names:
        lon, lat = table[name]
        x, y = ax.projection.transform_point(lon, lat, pc)
        fx, fy = ax.transAxes.inverted().transform(ax.transData.transform((x, y)))
        if not (margin < fx < 1 - margin and margin < fy < 1 - margin):
            continue
        ax.plot(x, y, "o", ms=ms, mfc="k", mec="white", mew=0.5, zorder=9)
        pos = where.get(name, "right")
        dx, dy, ha, va = _POS[pos] if isinstance(pos, str) else pos
        tr = offset_copy(ax.transData, fig=fig, x=dx, y=dy, units="points")
        t = ax.text(x, y, name, transform=tr, fontsize=fontsize, ha=ha, va=va, color="k", zorder=9,
                    path_effects=[pe.withStroke(linewidth=1.8, foreground="white")])
        out.append(t)
    return out


def halo(t, lw=1.8):
    """Give an existing text object a white halo."""
    t.set_path_effects([pe.withStroke(linewidth=lw, foreground="white")])
    return t
