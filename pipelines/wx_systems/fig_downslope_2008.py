"""Downslope / lee warming, ERA5 1800 UTC 8 Jun 2008 (group B)."""
import json
import numpy as np
import jstyle as J
import helpers_B as H

NAME = "downslope_2008"
T = "2008-06-08T18"
T0 = "2008-06-08T12"
EXT = H.EXT_NE

(msl, t2, td2, u10, v10, zs, t850, u850, v850, w850, td2_0) = H.getmany(
    [(v, T, None) for v in ("mean_sea_level_pressure", "2m_temperature", "2m_dewpoint_temperature",
                            "10m_u_component_of_wind", "10m_v_component_of_wind", "geopotential_at_surface")]
    + [(v, T, 850) for v in ("temperature", "u_component_of_wind", "v_component_of_wind", "vertical_velocity")]
    + [("2m_dewpoint_temperature", T0, None)], EXT)

msl = msl / 100
t2c = t2 - 273.15
dtd = td2 - td2_0                  # K, 1200 -> 1800 UTC
zs = zs / H.G                      # m
w = H.smooth(w850 * 36.0, 1)       # Pa s-1 -> hPa h-1, positive = descent
t850c = t850 - 273.15

# ---- numbers (inside the map box)
box = dict(longitude=slice(EXT[0], EXT[1]), latitude=slice(EXT[3], EXT[2]))
pts = {"BOS": (-71.01, 42.36), "ALB": (-73.80, 42.75), "BDL": (-72.68, 41.94), "NYC": (-73.97, 40.78),
       "PHL": (-75.24, 39.87)}
num = {}
for k, (lo, la) in pts.items():
    num[f"T2m_{k}_C"] = round(H.nearest(t2c, lo, la), 1)
    num[f"dTd_12to18_{k}_K"] = round(H.nearest(dtd, lo, la), 1)
wd = (np.degrees(np.arctan2(-u850, -v850)) % 360)
num["wdir850_mean_box_deg"] = round(float(wd.sel(**box).mean()))
num["wspd850_mean_box_kt"] = round(float(np.hypot(u850, v850).sel(**box).mean() * 1.94384))
num["T2m_max_box_C"] = round(float(t2c.sel(**box).max()), 1)
hv = w.sel(longitude=slice(-74.8, -72.8), latitude=slice(43.5, 41.5))
m = hv.argmax(...)
wlon, wlat = float(hv.longitude[m["longitude"]]), float(hv.latitude[m["latitude"]])
num["omega850_max_east_of_Adirondacks_Catskills_hPa_h"] = round(float(hv.max()), 1)
num["omega850_max_lon"], num["omega850_max_lat"] = wlon, wlat
num["omega850_min_Catskills_Adirondacks_hPa_h"] = round(float(w.sel(longitude=slice(-76.5, -73.5), latitude=slice(44.5, 41.8)).min()), 1)
print(num)

# ---- figure
fig = J.new_figure(height=3.6)
fig.subplots_adjust(left=0.01, right=0.99, wspace=0.06)
axs = [J.map_axes(fig, 121 + i, EXT) for i in range(2)]

ax = axs[0]
cf = J.shade(ax, t2c, np.arange(14, 37, 2), "RdYlBu_r")
J.barbs(ax, u10, v10, skip=8, length=3.6)
H.place_cities(ax, ["Boston", "Hartford", "Albany", "Philadelphia"])
H.contour_smart(ax, msl, np.arange(990, 1030, 2), fmt="%d", every=1)
J.panel_label(ax, "a", "Temperature (°C), pressure (hPa), wind")
J.colorbar(fig, cf, ax, "Temperature 2 m above ground (°C)", ticks=np.arange(14, 37, 4))

ax = axs[1]
cf = J.shade(ax, w, np.arange(-20, 20.1, 4), "RdBu_r")
H.place_cities(ax, ["Albany", "Boston", "Hartford"])
H.contour_smart(ax, zs, [400], lw=0.6, fmt="%d")
H.smart_arrow(ax, (wlon, wlat), "lee descent", prefer=(-1, 1))
J.panel_label(ax, "b", "Sinking air, 850 hPa (hPa h$^{-1}$), terrain")
J.colorbar(fig, cf, ax, "Sinking (+) or rising (−) air, 850 hPa (hPa h$^{-1}$)", ticks=np.arange(-20, 21, 10))

for a in axs:
    H.declutter(a)
out = J.save(fig, H.OUT / f"{NAME}.png")
json.dump(num, open(J.ROOT / f"_num_{NAME}.json", "w"), indent=1)
print(out)
H.finish()
