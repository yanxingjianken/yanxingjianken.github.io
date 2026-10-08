"""Santa Ana (offshore) wind, Southern California, ERA5 22 Oct 2007."""
import sys, json
import numpy as np
import jstyle as J, helpers_A as H, cities
import cartopy.crs as ccrs
import matplotlib.patheffects as pe

HOUR = int(sys.argv[1]) if len(sys.argv) > 1 else 9
T0 = f"2007-10-22T{HOUR:02d}"
E = H.SOCAL
OUT = sys.argv[2] if len(sys.argv) > 2 else "../../images/wx_systems_v3/santaana_2007.png"
f = lambda var, lev=None: J.fetch(var, T0, H.SOCAL_DATA, level=lev)

mslr = f("mean_sea_level_pressure") / 100
msl = H.smooth(mslr, 2)
t2 = f("2m_temperature"); td = f("2m_dewpoint_temperature")
u = f("10m_u_component_of_wind"); v = f("10m_v_component_of_wind")
sp = f("surface_pressure") / 100
t85 = f("temperature", 850); u85 = f("u_component_of_wind", 850); v85 = f("v_component_of_wind", 850)
rh = H.rh_from_td(t2, td)
above = sp > 870.0                                   # 850 hPa at least ~20 hPa above ground
tadv = (H.smooth(H.advection(u85, v85, t85), 2) * 3600).where(above)
t85c = (t85 - 273.15).where(above)
u85m, v85m = u85.where(above), v85.where(above)

fig = J.new_figure(height=3.4)
H.prep(fig)
axs = [J.map_axes(fig, 131 + i, E) for i in range(3)]

ax = axs[0]
cf = J.shade(ax, t2 - 273.15, np.arange(0, 31, 2), "RdYlBu_r")
H.contour_clean(ax, msl, np.arange(1000, 1041, 2), label_levels=np.arange(1000, 1041, 8), extent=E)
J.barbs(ax, u, v, skip=5, length=3.6)
cities.add(ax, ["Los Angeles", "San Diego", "Las Vegas"], where={"Los Angeles": "left", "San Diego": "left", "Las Vegas": "ul"})
J.panel_label(ax, "a", "Pressure (hPa), 2-m temp., wind")
J.colorbar(fig, cf, ax, "2-m temperature (°C)", ticks=np.arange(0, 31, 10))
lo, la, pmax = H.local_max(mslr, (-120, -113, 36, 41))
J.mark(ax, lo, la, "H")

ax = axs[1]
cf = J.shade(ax, tadv, np.arange(-1.5, 1.6, 0.25), "RdBu_r")
H.contour_clean(ax, t85c, np.arange(-20, 31, 2), label_levels=np.arange(-20, 13, 4), extent=E)   # 16/20 labels sit under city dots
J.barbs(ax, u85m, v85m, skip=5, length=3.6)
cities.add(ax, ["Los Angeles", "San Diego"], where={"Los Angeles": "left", "San Diego": "left"})   # Las Vegas would sit on the arrow
ax.text(-117.9, 38.4, "850 hPa" + chr(10) + "below ground", transform=ccrs.PlateCarree(), ha="center", va="center",
        fontsize=6.5, style="italic", color="0.3", zorder=8, linespacing=0.95,
        path_effects=[pe.withStroke(linewidth=1.6, foreground="white")])
J.panel_label(ax, "b", "850-hPa temp. advection (K h$^{-1}$)")
J.colorbar(fig, cf, ax, "850-hPa temperature advection (K h$^{-1}$)", ticks=np.arange(-1.5, 1.6, 0.5))

ax = axs[2]
cf = J.shade(ax, rh, np.arange(0, 101, 10), "YlGnBu", extend="neither")
J.barbs(ax, u, v, skip=5, length=3.6)
cities.add(ax, ["Los Angeles", "San Diego", "Las Vegas"], where={"Los Angeles": "left", "San Diego": "left", "Las Vegas": "ul"})
J.panel_label(ax, "c", "Relative humidity (%), wind (kt)")
J.colorbar(fig, cf, ax, "2-m relative humidity (%)", ticks=np.arange(0, 101, 20))

pts = {"LAX": (-118.41, 33.94), "Tonopah_TPH": (-117.09, 38.06), "Daggett_DAG": (-116.79, 34.85), "San_Diego": (-117.19, 32.73), "Ontario_ONT": (-117.60, 34.06)}
nums = {"great_basin_high_lonlat": [lo, la], "great_basin_high_hPa": round(pmax, 1)}
for k, xy in pts.items():
    uu, vv = H.at(u, *xy), H.at(v, *xy)
    nums[k] = dict(MSLP_hPa=round(H.at(mslr, *xy), 1), T2m_C=round(H.at(t2, *xy) - 273.15, 1), RH2m_pct=round(H.at(rh, *xy)),
                   wind_dir_deg=int(round(np.degrees(np.arctan2(-uu, -vv)) % 360, -1)), wind_kt=round(float(np.hypot(uu, vv)) * 1.94384))
nums["TPH_minus_LAX_hPa"] = round(nums["Tonopah_TPH"]["MSLP_hPa"] - nums["LAX"]["MSLP_hPa"], 1)
nums["DAG_minus_LAX_hPa"] = round(nums["Daggett_DAG"]["MSLP_hPa"] - nums["LAX"]["MSLP_hPa"], 1)
interior = H.subset(tadv, (-120, -113, 35, 41))
nums["mean_850_Tadv_interior_K_per_h"] = round(float(interior.mean()), 2)
nums["min_850_Tadv_interior_K_per_h"] = round(float(interior.min()), 2)
coast = H.subset(rh.where(sp > 950), (-119.5, -116.5, 32.5, 34.6))
nums["min_RH2m_coastal_SoCal_pct"] = round(float(coast.min()))
print(json.dumps(nums))
H.annotate(axs[1], "cooler air"+chr(10)+"arriving", xy=(-116.9, 35.5), xytext=(-114.6, 39.2))
H.anchor_south(axs)
H.check_text(fig, axs)
J.save(fig, OUT)
H.finish()
