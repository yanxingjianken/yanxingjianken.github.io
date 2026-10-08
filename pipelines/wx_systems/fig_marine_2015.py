"""Sea fog / marine stratus on the southern New England coast, ERA5 10 May 2015."""
import sys, json
import numpy as np
import jstyle as J, helpers_A as H, cities

HOUR = int(sys.argv[1]) if len(sys.argv) > 1 else 20
T0 = f"2015-05-10T{HOUR:02d}"
E = H.REG
D = H.REG_DATA
OUT = sys.argv[2] if len(sys.argv) > 2 else "../../images/wx_systems_v3/marine_2015.png"
f = lambda var, lev=None: J.fetch(var, T0, D, level=lev)

t2 = f("2m_temperature"); td = f("2m_dewpoint_temperature"); sst = f("sea_surface_temperature")
u = f("10m_u_component_of_wind"); v = f("10m_v_component_of_wind")
lcc = f("low_cloud_cover") * 100
t925 = f("temperature", 925)
dTs = t2 - sst                     # > 0: air warmer than the sea (cooled from below)
inv = t925 - t2                    # > 0: temperature increases with height (inversion)

fig = J.new_figure(height=3.4)
H.prep(fig)
axs = [J.map_axes(fig, 131 + i, E) for i in range(3)]

ax = axs[0]
cf = J.shade(ax, lcc, np.arange(0, 101, 10), "Greys_r", extend="neither")
J.barbs(ax, u, v, skip=5, length=3.6)
cities.add(ax, ["Boston", "Worcester", "Nantucket"], where={"Worcester": "left"})
J.panel_label(ax, "a", "Low cloud cover (%), wind (kt)")
J.colorbar(fig, cf, ax, "Low cloud cover (%)", ticks=np.arange(0, 101, 20))

ax = axs[1]
cf = J.shade(ax, dTs, np.arange(-6, 6.5, 1), "RdBu_r")
H.contour_clean(ax, sst - 273.15, np.arange(0, 31, 2), label_levels=np.arange(0, 31, 4), extent=E)
cities.add(ax, ["Boston", "Worcester", "Nantucket"], where={"Worcester": "left", "Boston": "above"})
J.panel_label(ax, "b", "Air minus sea (K), sea temp. (°C)")
J.colorbar(fig, cf, ax, "Air minus sea-surface temperature (K)", ticks=np.arange(-6, 7, 2))

ax = axs[2]
cf = J.shade(ax, inv, np.arange(-12, 12.5, 2), "RdBu_r")
cities.add(ax, ["Boston", "Worcester", "Nantucket"], where={"Worcester": "left"})
J.panel_label(ax, "c", "925-hPa minus 2-m temperature (K)")
J.colorbar(fig, cf, ax, "925-hPa minus 2-m temperature (K)", ticks=np.arange(-12, 13, 4))

pts = {"Nantucket_ACK": (-70.06, 41.25), "Marthas_Vineyard_MVY": (-70.61, 41.39), "Boston": (-71.03, 42.36), "Worcester": (-71.80, 42.27)}
nums = {}
for k, xy in pts.items():
    uu, vv = H.at(u, *xy), H.at(v, *xy)
    nums[k] = dict(T2m_C=round(H.at(t2, *xy) - 273.15, 1), Td2m_C=round(H.at(td, *xy) - 273.15, 1),
                   low_cloud_pct=round(H.at(lcc, *xy)), T925_minus_T2m_K=round(H.at(inv, *xy), 1),
                   wind_dir_deg=int(round(np.degrees(np.arctan2(-uu, -vv)) % 360, -1)), wind_kt=round(float(np.hypot(uu, vv)) * 1.94384))
box = (-72.5, -69.5, 40.3, 41.4)       # waters south of RI / Cape Cod / Islands
w = np.isfinite(H.subset(sst, box))
nums["southcoast_box"] = box
nums["southcoast_mean_low_cloud_pct"] = round(float(H.subset(lcc, box).where(w).mean()))
nums["southcoast_mean_T2m_minus_SST_K"] = round(float(H.subset(dTs, box).where(w).mean()), 1)
nums["southcoast_mean_SST_C"] = round(float(H.subset(sst, box).where(w).mean() - 273.15), 1)
nums["southcoast_mean_T925_minus_T2m_K"] = round(float(H.subset(inv, box).where(w).mean()), 1)
nums["southcoast_mean_dewpoint_depression_K"] = round(float(H.subset(t2 - td, box).where(w).mean()), 1)
print(json.dumps(nums))
H.annotate(axs[0], "sea fog,"+chr(10)+"stratus", xy=(-71.3, 40.75), xytext=(-75.6, 41.3))
H.anchor_south(axs)
H.check_text(fig, axs)
J.save(fig, OUT)
H.finish()
