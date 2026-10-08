"""Nor'easter (blizzard of 26-27 Jan 2015), ERA5 0000 UTC 27 Jan 2015."""
import sys, json
import numpy as np
import jstyle as J, helpers_A as H, cities

T0 = "2015-01-27T00"
E = H.SYN
D = H.SYN_DATA
OUT = sys.argv[1] if len(sys.argv) > 1 else "../../images/wx_systems_v3/noreaster_2015.png"
f = lambda var, lev=None: J.fetch(var, T0, D, level=lev)

mslr = f("mean_sea_level_pressure") / 100
msl = H.smooth(mslr, 1)
u = f("10m_u_component_of_wind"); v = f("10m_v_component_of_wind")
tp = f("total_precipitation") * 1000            # mm in the hour ending at T0
z5 = f("geopotential", 500) / H.G0 / 10          # dam
u5 = f("u_component_of_wind", 500); v5 = f("v_component_of_wind", 500)
eta = H.smooth(H.rel_vorticity(u5, v5), 2) * 1e5    # relative vorticity, 10^-5 s^-1
hcc = f("high_cloud_cover") * 100

fig = J.new_figure(height=3.4)
H.prep(fig)
axs = [J.map_axes(fig, 131 + i, E) for i in range(3)]

ax = axs[0]
cf = J.shade(ax, tp.where(tp >= 0.1), [0.1, 0.5, 1, 2, 3, 4, 6], "YlGnBu", extend="max")
H.contour_clean(ax, msl, np.arange(960, 1041, 4), label_levels=np.arange(960, 1041, 8), extent=E)
J.barbs(ax, u, v, skip=10, length=3.6)
cities.add(ax, ["Boston", "Nantucket", "New York"], where={"Nantucket": (3.0, -3.4, "left", "center"), "New York": "left"})
J.panel_label(ax, "a", "Pressure (hPa), precipitation, wind")
cb = J.colorbar(fig, cf, ax, "Precipitation rate (mm h$^{-1}$)", ticks=[0.1, 0.5, 1, 2, 3, 4, 6], extend="max")
cb.ax.set_xticklabels(["0.1", "0.5", "1", "2", "3", "4", "6"])
lo, la, pmin = H.local_min(mslr, (-80, -64, 32, 44))
J.mark(ax, lo, la, "L")

ax = axs[1]
cf = J.shade(ax, eta, np.arange(-24, 25, 4), "RdBu_r")
H.contour_clean(ax, z5, np.arange(480, 600, 6), label_levels=np.arange(480, 600, 12), extent=E)
cities.add(ax, ["Boston", "New York"], where={"New York": "left"})
J.panel_label(ax, "b", "500-hPa height (dam) and spin")
J.colorbar(fig, cf, ax, r"Spin (vorticity) at 500 hPa (10$^{-5}$ s$^{-1}$)", ticks=np.arange(-24, 25, 8))

ax = axs[2]
cf = J.shade(ax, hcc, np.arange(0, 101, 10), "Greys_r", extend="neither")
H.contour_clean(ax, msl, np.arange(960, 1041, 4), label_levels=np.arange(960, 1041, 8), extent=E)
cities.add(ax, ["Boston", "New York"], where={"New York": "left"})
J.panel_label(ax, "c", "High cloud cover (%), pressure")
J.colorbar(fig, cf, ax, "High cloud cover (%)", ticks=np.arange(0, 101, 20))

pts = {"Boston": (-71.03, 42.36), "Nantucket": (-70.06, 41.25), "NYC": (-73.97, 40.78)}
nums = {"low_lonlat": [lo, la], "low_central_pressure_hPa": round(pmin, 1)}
for k, xy in pts.items():
    uu, vv = H.at(u, *xy), H.at(v, *xy)
    nums[k] = dict(MSLP_hPa=round(H.at(mslr, *xy), 1), precip_mm_h=round(H.at(tp, *xy), 2),
                   wind_dir_deg=int(round(np.degrees(np.arctan2(-uu, -vv)) % 360, -1)), wind_kt=round(float(np.hypot(uu, vv)) * 1.94384))
s = H.subset(np.hypot(u, v) * 1.94384, (-75, -66, 38, 44))
nums["max_10m_wind_kt_box_75W_66W_38N_44N"] = round(float(s.max()))
lo5, la5, emax = H.local_max(eta, (-82, -68, 32, 44))
nums["max_500hPa_rel_vort_1e-5"] = round(emax, 1); nums["max_500hPa_rel_vort_lonlat"] = [lo5, la5]
print(json.dumps(nums))
H.anchor_south(axs)
H.check_text(fig, axs)
J.save(fig, OUT)
H.finish()
