"""Lake-effect snow ("Snowvember", Buffalo), ERA5 2100 UTC 18 Nov 2014 (group B)."""
import json
import numpy as np
import matplotlib as mpl
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import jstyle as J
import helpers_B as H

NAME = "lakeeffect_2014"
T = "2014-11-18T21"
FETCH_EXT = H.EXT_GL                     # cache key; padded data cover the plotted box
EXT = (-86.0, -74.0, 40.5, 46.0)         # lower Great Lakes (Huron, Erie, Ontario)

(msl, u10, v10, tlake, tp, blh, t850, u850, v850) = H.getmany(
    [(v, T, None) for v in ("mean_sea_level_pressure", "10m_u_component_of_wind", "10m_v_component_of_wind",
                            "lake_mix_layer_temperature", "total_precipitation", "boundary_layer_height")]
    + [(v, T, 850) for v in ("temperature", "u_component_of_wind", "v_component_of_wind")], FETCH_EXT)
lakec, = H.getmany([("lake_cover", "2014-11-18T12", None)], FETCH_EXT)

msl = msl / 100
lake = lakec > 0.5
dT = (tlake - t850).where(lake)          # K, lake surface minus 850 hPa
t850c = t850 - 273.15
pr = tp * 1000.0                         # mm in the hour ending at T
blh_km = blh / 1000.0

# ---- numbers
erie = dict(longitude=slice(-83.5, -78.8), latitude=slice(42.9, 41.3))
ont = dict(longitude=slice(-79.9, -76.0), latitude=slice(44.3, 43.1))
box = dict(longitude=slice(EXT[0], EXT[1]), latitude=slice(EXT[3], EXT[2]))
wd = np.degrees(np.arctan2(-u850, -v850)) % 360
lee = dict(longitude=slice(-79.5, -76.5), latitude=slice(43.2, 42.2))   # Buffalo / Tug Hill downwind shores
num = {
    "Erie_mean_Tlake_C": round(float((tlake - 273.15).where(lake).sel(**erie).mean()), 1),
    "Erie_mean_T850_C": round(float(t850c.sel(**erie).mean()), 1),
    "Erie_mean_dT_K": round(float(dT.sel(**erie).mean()), 1),
    "Ontario_mean_dT_K": round(float(dT.sel(**ont).mean()), 1),
    "lake_dT_min_K_in_box": round(float(dT.sel(**box).min()), 1),
    "lake_dT_max_K_in_box": round(float(dT.sel(**box).max()), 1),
    "Erie_mean_wdir850_deg": round(float(wd.sel(**erie).mean())),
    "Erie_mean_wspd850_kt": round(float(np.hypot(u850, v850).sel(**erie).mean() * 1.94384)),
    "max_precip_mm_h_in_box": round(float(pr.sel(**box).max()), 2),
    "max_precip_mm_h_east_of_Erie": round(float(pr.sel(**lee).max()), 2),
    "max_blh_km_in_box": round(float(blh_km.sel(**box).max()), 2),
    "Erie_mean_blh_km": round(float(blh_km.sel(**erie).mean()), 2),
}
k = pr.sel(**box).argmax(...)
num["max_precip_lon"] = float(pr.sel(**box).longitude[k["longitude"]])
num["max_precip_lat"] = float(pr.sel(**box).latitude[k["latitude"]])
print(num)

# ---- figure
fig = J.new_figure(height=3.2)
fig.subplots_adjust(left=0.01, right=0.99, wspace=0.08)
axs = [J.map_axes(fig, 131 + i, EXT) for i in range(3)]

ax = axs[0]
cf = J.shade(ax, dT, np.arange(12, 29, 2), "YlOrRd", extend="both")
J.barbs(ax, u850, v850, skip=6, length=3.6)
H.place_cities(ax, ["Buffalo"], prefer={"Buffalo": "below"})
lk = dT.sel(longitude=slice(EXT[0] - 1, EXT[1] + 1), latitude=slice(EXT[3] + 1, EXT[2] - 1)).stack(p=("latitude", "longitude")).dropna("p")
lake_pts = list(zip(lk.longitude.values, lk.latitude.values))          # keep lake names off the lake shading
lake_pts += [(-79.45, 44.25), (-79.4, 44.4), (-79.3, 44.55), (-82.6, 42.45), (-82.8, 42.6)]   # Lake Simcoe, Lake St Clair
for nm, xy in (("Lake Erie", (-81.2, 42.0)), ("Lake Ontario", (-77.8, 43.6)), ("Lake Huron", (-82.3, 44.6))):
    H.smart_arrow(ax, xy, nm, fontsize=6.5, rmin=0, rmax=90, barb_px=3, arrow=False, avoid_lonlat=lake_pts,
                  text_kw=dict(style="italic"))
J.panel_label(ax, "a", "Lake minus 850-hPa temperature (K)")
J.colorbar(fig, cf, ax, "Lake minus 850-hPa air temperature (K)", ticks=np.arange(12, 29, 4), extend="both")

ax = axs[1]
plev = [0.1, 0.2, 0.5, 1, 2]
cmap = mcolors.ListedColormap(mpl.colormaps["Blues"](np.linspace(0.25, 1.0, len(plev))))
norm = mcolors.BoundaryNorm(plev, cmap.N, extend="max")
cf = ax.contourf(pr.longitude, pr.latitude, pr, levels=plev, cmap=cmap, norm=norm, extend="max",
                 transform=ccrs.PlateCarree(), zorder=2)
H.place_cities(ax, ["Buffalo"], prefer={"Buffalo": "below"})
H.contour_smart(ax, msl, np.arange(980, 1040, 4), fmt="%d")
J.panel_label(ax, "b", "Precip. (mm h$^{-1}$), pressure (hPa)")
J.colorbar(fig, cf, ax, "Precipitation in the past hour (mm)", ticks=plev, extend="max")

ax = axs[2]
cf = J.shade(ax, blh_km, np.arange(0, 3.01, 0.25), "YlGnBu", extend="max")
H.place_cities(ax, ["Buffalo"], prefer={"Buffalo": "below"})
J.panel_label(ax, "c", "Boundary-layer depth (km)")
J.colorbar(fig, cf, ax, "Boundary-layer depth (km)", ticks=np.arange(0, 3.01, 1.0), extend="max")

for a in axs:
    H.declutter(a)
out = J.save(fig, H.OUT / f"{NAME}.png")
json.dump(num, open(J.ROOT / f"_num_{NAME}.json", "w"), indent=1)
print(out)
H.finish()
