"""Sea breeze, Boston area, ERA5 27 Mar 2007 (18 and 20 UTC)."""
import sys, json
import numpy as np
import jstyle as J, helpers_A as H, cities

T0 = "2007-03-27T18"
T1 = "2007-03-27T20"
E = H.MESO
OUT = sys.argv[1] if len(sys.argv) > 1 else "../../images/wx_systems_v3/seabreeze_2007.png"

t2 = J.fetch("2m_temperature", T0, E) - 273.15
t2b = J.fetch("2m_temperature", T1, E) - 273.15
td = J.fetch("2m_dewpoint_temperature", T0, E) - 273.15
u = J.fetch("10m_u_component_of_wind", T0, E)
v = J.fetch("10m_v_component_of_wind", T0, E)
div = H.divergence(u, v) * 1e5
dT = t2b - t2

fig = J.new_figure(height=3.4)
H.prep(fig)
axs = [J.map_axes(fig, 131 + i, E) for i in range(3)]

ax = axs[0]
cf = J.shade(ax, t2, np.arange(4, 21, 1), "RdYlBu_r")
J.barbs(ax, u, v, skip=2, length=4.0)
cities.add(ax, ["Boston", "Worcester"], where={"Worcester": "left"})
J.panel_label(ax, "a", "2-m temperature (°C), wind (kt)")
J.colorbar(fig, cf, ax, "2-m temperature (°C)", ticks=np.arange(4, 21, 4))

ax = axs[1]
cf = J.shade(ax, div, np.arange(-6, 6.5, 1), "RdBu_r")
H.contour_clean(ax, t2, np.arange(6, 21, 2), label_levels=np.arange(6, 21, 4), extent=E)
cities.add(ax, ["Boston", "Worcester"], where={"Worcester": "left", "Boston": "lr"})
J.panel_label(ax, "b", "Converging air (blue), temp. (°C)")
J.colorbar(fig, cf, ax, r"Wind divergence (10$^{-5}$ s$^{-1}$)", ticks=np.arange(-6, 7, 2))

ax = axs[2]
cf = J.shade(ax, dT, np.arange(-3, 3.25, 0.5), "RdBu_r")
cities.add(ax, ["Boston", "Worcester"], where={"Worcester": "left"})
J.panel_label(ax, "c", "Temperature change, 18–20 UTC")
J.colorbar(fig, cf, ax, "Change in 2-m temperature (K per 2 h)", ticks=np.arange(-3, 4, 1))

pts = {"Boston": (-71.03, 42.36), "Worcester": (-71.80, 42.27)}
nums = {}
for k, xy in pts.items():
    uu, vv = H.at(u, *xy), H.at(v, *xy)
    nums[k] = dict(T2m_18Z_C=round(H.at(t2, *xy), 1), T2m_20Z_C=round(H.at(t2b, *xy), 1),
                   dT_18_20_K=round(H.at(dT, *xy), 1), Td2m_18Z_C=round(H.at(td, *xy), 1),
                   wind_dir_18Z_deg=int(round(np.degrees(np.arctan2(-uu, -vv)) % 360, -1)),
                   wind_kt_18Z=round(float(np.hypot(uu, vv)) * 1.94384))
# hourly Boston / Worcester grid-point T2m, 15-21 UTC
for k, xy in pts.items():
    nums[k]["T2m_hourly_15_21Z_C"] = [round(H.at(J.fetch("2m_temperature", f"2007-03-27T{h:02d}", E) - 273.15, *xy), 1) for h in range(15, 22)]
nums["dT_Worcester_minus_Boston_18Z_K"] = round(nums["Worcester"]["T2m_18Z_C"] - nums["Boston"]["T2m_18Z_C"], 1)
lo, la, dmin = H.local_min(div, (-71.6, -70.6, 42.0, 42.9))
nums["min_10m_div_E_MA_1e-5_s-1"] = round(dmin, 1); nums["min_div_lonlat"] = [lo, la]
print(json.dumps(nums))
H.annotate(axs[1], "sea-breeze\nfront", xy=(-71.05, 42.6), xytext=(-72.55, 43.15))
H.anchor_south(axs)
H.check_text(fig, axs)
J.save(fig, OUT)
H.finish()
