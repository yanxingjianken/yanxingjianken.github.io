"""Omega block over eastern North America, 15-17 Apr 2016 (ERA5). Group C."""
import json
import numpy as np
import xarray as xr
from scipy.ndimage import maximum_filter, minimum_filter
import jstyle as J
import helpers_C as H
import cities

FETCH_EXT = (-130, -20, 25, 72)            # cached fetch box (pad 10)
EXT = (-120, -56, 22, 64)
DAYS = ["2016-04-15 12", "2016-04-16 12", "2016-04-17 12"]
clim = xr.open_dataarray(J.CACHE / "C_z500clim_0416T12_1991-2020_omega2016.nc").load() / 10.0  # dam

fig = J.new_figure(height=2.35)
S = H.slots(fig, 3, gaps=[0.02, 0.02])
nums = {}
PR = []
CB = []
AX = []
THICK = 570                                   # the height contour that outlines the omega
CITY = ["Denver", "New York"]
for k, t in enumerate(DAYS):
    z = J.fetch("geopotential", t, FETCH_EXT, level=500, pad=10) / 9.80665 / 10.0
    anom = z - clim.values
    ax = J.map_axes(fig, S[k], EXT)
    cf = J.shade(ax, anom, np.arange(-30, 31, 5), "RdBu_r")
    csz = J.contour(ax, z, [l for l in np.arange(510, 600, 6) if l != THICK], label=False)
    cst = J.contour(ax, z, [THICK], label=False, lw=1.2)
    # closed high over eastern North America
    sub = z.sel(latitude=slice(55, 37), longitude=slice(-100, -70))
    i, j = np.unravel_index(int(sub.values.argmax()), sub.shape)
    hlon, hlat, hz = float(sub.longitude[j]), float(sub.latitude[i]), float(sub.values[i, j])
    J.mark(ax, hlon, hlat, "H", fontsize=8)
    # flanking lows (west and east of the high)
    w = z.sel(latitude=slice(50, 25), longitude=slice(hlon - 30, hlon - 8))
    e = z.sel(latitude=slice(50, 25), longitude=slice(hlon + 8, hlon + 32))
    iw = np.unravel_index(int(w.values.argmin()), w.shape)
    ie = np.unravel_index(int(e.values.argmin()), e.shape)
    am = anom.sel(latitude=slice(55, 32), longitude=slice(-100, -70))
    nums[t[:10]] = dict(
        high_lon=hlon, high_lat=hlat, high_z500_dam=round(hz, 1),
        west_low=[float(w.longitude[iw[1]]), float(w.latitude[iw[0]]), round(float(w.values[iw]), 1)],
        east_low=[float(e.longitude[ie[1]]), float(e.latitude[ie[0]]), round(float(e.values[ie]), 1)],
        max_anom_dam_near_high=round(float(am.max()), 1),
    )
    day = t[8:10].lstrip("0")
    J.panel_label(ax, "abc"[k], f"500-hPa height (dam), anomaly, {day} Apr")
    PR.append((ax, csz, cst))
    CB.append(J.colorbar(fig, cf, ax, "Height departure from normal (dam)", ticks=np.arange(-30, 31, 15), extend="both"))
    AX.append(ax)
for a_, c_, t_ in PR:
    cities.add(a_, CITY, where={"Chicago": "left", "New York": "right", "Denver": "left"})
    H.clabel_avoid(a_, t_, list(a_.texts), edge=0.03)
    H.clabel_avoid(a_, c_, list(a_.texts), edge=0.03, levels=[l for l in c_.levels if 552 <= l <= 582], min_len=4.0)
H.check_layout(fig, AX, CB)
J.save(fig, H.OUT / "omegablock_2016.png")
json.dump(nums, open(J.ROOT / "_numbers_omega.json", "w"), indent=1)
print(json.dumps(nums, indent=1))
H.finish()
