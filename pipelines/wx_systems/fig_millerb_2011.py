"""Miller-B-type redevelopment, 26-27 Jan 2011, ERA5: MSLP and 3-h MSLP tendency at three times."""
import sys, json
import numpy as np
import pandas as pd
from scipy.ndimage import minimum_filter
import jstyle as J, helpers_A as H, cities

E = H.SYN
D = H.SYN_DATA
TIMES = ["2011-01-26T12", "2011-01-26T18", "2011-01-27T06"]
OUT = sys.argv[1] if len(sys.argv) > 1 else "../../images/wx_systems_v3/millerb_2011.png"


def msl(t):
    return J.fetch("mean_sea_level_pressure", t, D) / 100


def minus3h(t):
    return (pd.Timestamp(t) - pd.Timedelta(hours=3)).strftime("%Y-%m-%dT%H")


def lows(p, ext, size=9, pmax=1012):
    s = H.subset(p, ext)
    a = s.values
    m = (a == minimum_filter(a, size=size))
    out = []
    for i, j in np.argwhere(m):
        if 1 < i < a.shape[0] - 2 and 1 < j < a.shape[1] - 2 and a[i, j] < pmax:
            out.append((float(s.longitude[j]), float(s.latitude[i]), round(float(a[i, j]), 1)))
    return sorted(out, key=lambda x: x[2])


fig = J.new_figure(height=3.4)
H.prep(fig)
axs = [J.map_axes(fig, 131 + i, E) for i in range(3)]
labels = ["12 UTC 26 Jan 2011", "18 UTC 26 Jan 2011", "06 UTC 27 Jan 2011"]
nums = {}
inner = (-86, -63, 31, 47)
for k, (ax, t) in enumerate(zip(axs, TIMES)):
    p = msl(t)
    dp = H.smooth(p - msl(minus3h(t)), 1)
    cf = J.shade(ax, dp, np.arange(-6, 6.5, 1), "RdBu_r")
    H.contour_clean(ax, H.smooth(p, 1), np.arange(960, 1041, 4), label_levels=[l for l in np.arange(960, 1041, 8) if not (k > 0 and l == 1016)], extent=E)
    cities.add(ax, (["Washington"] if k == 0 else []) + ["New York", "Boston"], where={"Washington": "left", "New York": "left", "Boston": "ur" if k == 2 else "right"})
    J.panel_label(ax, "abc"[k], f"{labels[k]}: pressure change")
    J.colorbar(fig, cf, ax, "3-h pressure change (hPa per 3 h)", ticks=np.arange(-6, 7, 2))
    L = lows(p, inner)
    nums[t] = [dict(lon=lo, lat=la, p_hPa=pp, dp3h_hPa=round(H.at(dp, lo, la), 1)) for lo, la, pp in L[:3]]
    J.mark(ax, L[0][0], L[0][1], "L")
    if k == 0:   # inland primary: the northern-most centre west of the Appalachian crest
        inl = max([x for x in L if x[0] < -79], key=lambda x: x[1])
        J.mark(ax, inl[0], inl[1], "L")
        nums["inland_primary_marked"] = inl
    if k == 2:
        ax.plot(-70, 40, marker="+", color="k", ms=5, mew=0.8, transform=__import__("cartopy.crs", fromlist=["x"]).PlateCarree(), zorder=7)
print(json.dumps(nums))
H.anchor_south(axs)
H.check_text(fig, axs)
J.save(fig, OUT)
H.finish()
