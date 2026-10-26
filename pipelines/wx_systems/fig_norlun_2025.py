"""Norlun (inverted) trough over southern Maine, 23-24 Dec 2025 (ERA5). Group C style."""
import json
import numpy as np
import jstyle as J
import helpers_C as H
import cities

T = "2025-12-24T09"                    # 0900 UTC 24 Dec = 4 a.m. EST, height of the band
EXT = (-77, -59, 36, 49)               # panels a, b: offshore low and New England
EXT_C = (-72.6, -66.6, 42.4, 46.4)     # panel c: Maine and New Hampshire
# accumulation: hours ending 2200 UTC 23 Dec ... 1800 UTC 24 Dec = 2100 UTC 23 Dec to 1800 UTC 24 Dec
ACC_T = [f"2025-12-23T{h:02d}" for h in range(22, 24)] + [f"2025-12-24T{h:02d}" for h in range(0, 19)]

mslr = J.fetch("mean_sea_level_pressure", T, EXT) / 100.0
msl = H.smooth(mslr, 1)
u10 = J.fetch("10m_u_component_of_wind", T, EXT)
v10 = J.fetch("10m_v_component_of_wind", T, EXT)
tp = J.fetch("total_precipitation", T, EXT) * 1000.0           # mm in the hour ending at T
z5 = J.fetch("geopotential", T, EXT, level=500) / H.G / 10.0    # dam
u5 = J.fetch("u_component_of_wind", T, EXT, level=500)
v5 = J.fetch("v_component_of_wind", T, EXT, level=500)
zeta = H.smooth(H.rel_vort(u5, v5), 2) * 1e5
acc = H.fetch_series("total_precipitation", ACC_T, EXT_C).sum("time") * 1000.0   # mm

# offshore low and 500-hPa spin maximum
lo_lon, lo_lat, lo_p = H.local_min(mslr, -64, 39, radius=4)
vx_lon, vx_lat, vx_val = H.local_max(zeta, -72, 43.5, radius=4)

# trough axis: along each latitude between the low and the Maine coast, the longitude of lowest
# pressure west of the low (the isobars' sharpest bend)
axis = []
for la in np.arange(40.0, 44.51, 0.5):
    row = mslr.sel(latitude=la).sel(longitude=slice(-71.5, lo_lon + 0.5))
    k = int(np.argmin(row.values))
    axis.append((round(float(row.longitude[k]), 2), float(la), round(float(row.values[k]), 1)))
print("trough axis (lon, lat, hPa):", axis)

fig = J.new_figure(height=2.6)
S = H.slots(fig, 3, gaps=[0.03, 0.03])

ax1 = J.map_axes(fig, S[0], EXT)
cf1 = J.shade(ax1, tp.where(tp >= 0.1), [0.1, 0.5, 1, 2, 3, 4, 6], "YlGnBu", extend="max")
cs1 = J.contour(ax1, msl, np.arange(970, 1041, 2), label=False)
J.mark(ax1, lo_lon, lo_lat, "L", fontsize=8, bbox=dict(boxstyle="circle,pad=0.05", fc="white", ec="none"))
J.panel_label(ax1, "a", "Pressure (hPa), precipitation, wind")
cb1 = J.colorbar(fig, cf1, ax1, "Precipitation rate (mm h$^{-1}$)", ticks=[0.1, 0.5, 1, 2, 3, 4, 6], extend="max")
cb1.ax.set_xticklabels(["0.1", "0.5", "1", "2", "3", "4", "6"])
cities.add(ax1, ["Boston", "Portland"], where={"Boston": "left", "Portland": "left"})
ann = H.arrow_label(ax1, (axis[4][0], axis[4][1]), (-75.0, 38.6), "inverted\ntrough", fontsize=6.5, halo=True, linespacing=1.0)
H.clabel_avoid(ax1, cs1, list(ax1.texts) + [ann], levels=np.arange(972, 1041, 4))
H.barbs_avoid(ax1, u10, v10, skip=9, length=3.6, avoid=list(ax1.texts) + [ann])

ax2 = J.map_axes(fig, S[1], EXT)
cf2 = J.shade(ax2, zeta, np.arange(-24, 25, 4), "RdBu_r")
cs2 = J.contour(ax2, z5, np.arange(486, 600, 6), label=False)
J.panel_label(ax2, "b", "500-hPa height (dam) and spin")
cb2 = J.colorbar(fig, cf2, ax2, r"Spin at 500 hPa (10$^{-5}$ s$^{-1}$)", ticks=np.arange(-24, 25, 8), extend="both")
cities.add(ax2, ["Boston", "Portland"], where={"Boston": "left", "Portland": "left"})
H.clabel_avoid(ax2, cs2, list(ax2.texts))

ax3 = J.map_axes(fig, S[2], EXT_C)
cf3 = J.shade(ax3, acc, [2, 5, 10, 15, 20, 25, 30], "YlGnBu", extend="max")
J.panel_label(ax3, "c", "Precipitation over 21 h (mm)")
cb3 = J.colorbar(fig, cf3, ax3, "Precipitation, 23–24 Dec (mm)", ticks=[2, 5, 10, 15, 20, 25, 30], extend="max")
EXTRA = {"Lewiston": (-70.21, 44.10)}
cities.add(ax3, ["Portland", "Lewiston", "Bangor", "Concord"], extra=EXTRA,
           where={"Portland": "lr", "Lewiston": "left", "Bangor": "right", "Concord": "left"})
H.check_layout(fig, [ax1, ax2, ax3], [cb1, cb2, cb3])
J.save(fig, H.OUT / "norlun_2025.png")

R = 6371.0
def km(a, b):
    dx = np.deg2rad(b[0] - a[0]) * np.cos(np.deg2rad(0.5 * (a[1] + b[1]))) * R
    dy = np.deg2rad(b[1] - a[1]) * R
    return round(float(np.hypot(dx, dy)))

# site coordinates as given in the NWS Gray snowfall reports (PNSGYX 1426 UTC 25 Dec 2025)
SITES = {"Topsham": (-69.9601, 43.9287), "Lewiston_2E": (-70.17, 44.10), "Portland_jetport": (-70.3044, 43.6422),
         "Boothbay_Harbor_3SE": (-69.5922, 43.8265), "Bangor": (-68.77, 44.80), "Concord": (-71.54, 43.21)}
box = acc.sel(latitude=slice(46.0, 43.0), longitude=slice(-72.0, -67.0))
i = np.unravel_index(np.nanargmax(box.values), box.shape)
mband = tp.sel(latitude=slice(46.0, 43.4), longitude=slice(-71.5, -67.5))
j = np.unravel_index(np.nanargmax(mband.values), mband.shape)
nums = dict(
    time=T, low_lon=lo_lon, low_lat=lo_lat, low_mslp_hPa=round(lo_p, 1),
    vort500_max_lon=vx_lon, vort500_max_lat=vx_lat, vort500_max_1e5=round(vx_val, 1),
    trough_axis=axis,
    max_precip_rate_maine_mm_h=round(float(mband.values[j]), 2),
    max_precip_rate_lonlat=[float(mband.longitude[j[1]]), float(mband.latitude[j[0]])],
    acc_max_mm=round(float(box.values[i]), 1), acc_max_lonlat=[float(box.longitude[i[1]]), float(box.latitude[i[0]])],
    acc_at_sites_mm={k: round(float(acc.interp(longitude=a, latitude=b)), 1) for k, (a, b) in SITES.items()},
    dist_km={"Topsham-Portland_jetport": km(SITES["Topsham"], SITES["Portland_jetport"]),
             "Topsham-Boothbay_3SE": km(SITES["Topsham"], SITES["Boothbay_Harbor_3SE"]),
             "Lewiston2E-Portland_jetport": km(SITES["Lewiston_2E"], SITES["Portland_jetport"]),
             "low-Portland": km((lo_lon, lo_lat), SITES["Portland_jetport"])},
)
json.dump(nums, open(J.ROOT / "_numbers_norlun.json", "w"), indent=1)
print(json.dumps(nums, indent=1))
H.finish()
