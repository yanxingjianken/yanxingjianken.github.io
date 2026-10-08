"""Coastal front, eastern New England, ERA5 27 Jan 2008 (forecast in the BOX AFD issued 0355 UTC 27 Jan). Two panels."""
import sys, json
import numpy as np
import jstyle as J, helpers_A as H, cities

HOUR = int(sys.argv[1]) if len(sys.argv) > 1 else 12
T0 = f"2008-01-27T{HOUR:02d}"
E = H.MESO
D = H.REG_DATA
OUT = sys.argv[2] if len(sys.argv) > 2 else "../../images/wx_systems_v3/coastalfront_2008.png"
f = lambda var, lev=None: J.fetch(var, T0, D, level=lev)

t2 = f("2m_temperature")
sst = f("sea_surface_temperature")
u = f("10m_u_component_of_wind"); v = f("10m_v_component_of_wind")

dTs = t2 - sst                                      # air-sea temperature difference (K), NaN over land
FG, FGc = H.frontogenesis(u, v, t2)                 # total-wind 2-D frontogenesis on 2-m T
fg = H.smooth(FG, 1) * 1e5 * 3 * 3600               # K (100 km)^-1 (3 h)^-1
t2c = t2 - 273.15

fig = J.new_figure(height=3.9)
H.prep(fig)
axs = [J.map_axes(fig, 121 + i, E) for i in range(2)]

ax = axs[0]
cf = J.shade(ax, dTs, np.arange(-10, 10.5, 1), "RdBu_r")
H.contour_clean(ax, t2c, np.arange(-20, 11, 1), label_levels=np.arange(-20, 11, 2), extent=E)
J.barbs(ax, u, v, skip=2, length=3.8)
cities.add(ax, ["Boston", "Worcester"], where={"Worcester": "left"})
J.panel_label(ax, "a", "Air minus sea temp. (K), air temp. (°C)")
J.colorbar(fig, cf, ax, "Air minus sea-surface temperature (K)", ticks=np.arange(-10, 11, 5))

ax = axs[1]
cf = J.shade(ax, fg, np.arange(-15, 16, 2.5), "RdBu_r")
H.contour_clean(ax, t2c, np.arange(-20, 11, 1), label_levels=np.arange(-20, 11, 2), extent=E)
cities.add(ax, ["Boston", "Worcester"], where={"Worcester": "left", "Boston": "left"})
J.panel_label(ax, "b", "Frontogenesis, 2-m temperature (°C)")
J.colorbar(fig, cf, ax, "Frontogenesis (K per 100 km per 3 h)", ticks=np.arange(-15, 16, 5))

pts = {"Boston": (-71.03, 42.36), "Worcester": (-71.80, 42.27), "Mass_Bay": (-70.5, 42.3)}
nums = {}
for k, xy in pts.items():
    uu, vv = H.at(u, *xy), H.at(v, *xy)
    nums[k] = dict(T2m_C=round(H.at(t2c, *xy), 1), wind_dir_deg=int(round(np.degrees(np.arctan2(-uu, -vv)) % 360, -1)),
                   wind_kt=round(float(np.hypot(uu, vv)) * 1.94384))
nums["SST_Mass_Bay_C"] = round(H.at(sst, -70.5, 42.3) - 273.15, 1)
box = (-72.0, -69.5, 41.3, 43.2)
lo, la, fmax = H.local_max(fg, box)
nums["max_frontogenesis_K_100km_3h"] = round(fmax, 1); nums["max_frontogenesis_lonlat"] = [lo, la]
nums["min_airsea_dT_K_GulfOfMaine"] = round(float(H.subset(dTs, (-71, -66, 41.5, 44.5)).min()), 1)
print(json.dumps(nums))
H.annotate(axs[1], "coastal"+chr(10)+"front", xy=(-70.85, 42.62), xytext=(-69.95, 41.85))
H.anchor_south(axs)
H.check_text(fig, axs)
J.save(fig, OUT)
H.finish()
