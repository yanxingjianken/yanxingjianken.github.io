"""Radiational cooling and cold pools, ERA5 0900 UTC 6 Jan 2016 (group B)."""
import json
import numpy as np
import jstyle as J
import helpers_B as H

NAME = "radcool_2016"
T = "2016-01-06T09"
EXT = H.EXT_NE

(msl, t2, u10, v10, tcc, blh, sp) = H.getmany(
    [(v, T, None) for v in ("mean_sea_level_pressure", "2m_temperature", "10m_u_component_of_wind",
                            "10m_v_component_of_wind", "total_cloud_cover", "boundary_layer_height", "surface_pressure")], EXT)
LEVS = [1000, 975, 950, 925, 900, 850]
TL = dict(zip(LEVS, H.getmany([("temperature", T, l) for l in LEVS], EXT)))

msl = msl / 100
t2c = t2 - 273.15
cloud = tcc * 100
inv = H.t_above_ground(TL, sp, dp=50.0) - t2   # K; T(p_s - 50 hPa) - T(2 m), ~400 m above the ground
ws10 = np.hypot(u10, v10)

# ---- numbers (inside the map box, land only via sp>0 is not needed: ocean has no inversion story)
box = dict(longitude=slice(EXT[0], EXT[1]), latitude=slice(EXT[3], EXT[2]))
b = lambda da: da.sel(**box)
i = b(msl).argmax(...)
hlon, hlat = float(b(msl).longitude[i["longitude"]]), float(b(msl).latitude[i["latitude"]])
j = b(t2c).argmin(...)
clon, clat = float(b(t2c).longitude[j["longitude"]]), float(b(t2c).latitude[j["latitude"]])
pts = {"SLK": (-74.21, 44.39), "ALB": (-73.80, 42.75), "CON": (-71.50, 43.20), "BOS": (-71.01, 42.36),
       "BTV": (-73.15, 44.47), "ORH": (-71.88, 42.27)}
num = {"MSLP_max_hPa": round(float(b(msl).max()), 1), "MSLP_max_lon": hlon, "MSLP_max_lat": hlat,
       "T2m_min_C": round(float(b(t2c).min()), 1), "T2m_min_lon": clon, "T2m_min_lat": clat}
for k, (lo, la) in pts.items():
    num[f"T2m_{k}_C"] = round(H.nearest(t2c, lo, la), 1)
    num[f"inv_Tps50_minus_T2m_{k}_K"] = round(H.nearest(inv, lo, la), 1)
    num[f"wind10_{k}_kt"] = round(H.nearest(ws10, lo, la) * 1.94384, 1)
    num[f"cloud_{k}_pct"] = round(H.nearest(cloud, lo, la))
    num[f"blh_{k}_m"] = round(H.nearest(blh, lo, la))
# interior New England / New York land box (no ocean)
nb = dict(longitude=slice(-76.5, -70.5), latitude=slice(45.0, 42.0))
num["interiorNE_mean_cloud_pct"] = round(float(cloud.sel(**nb).mean()))
num["interiorNE_median_wind10_kt"] = round(float(ws10.sel(**nb).median() * 1.94384), 1)
num["interiorNE_max_inv_K"] = round(float(inv.sel(**nb).max()), 1)
num["interiorNE_median_blh_m"] = round(float(blh.sel(**nb).median()))
print(num)

# ---- figure
fig = J.new_figure(height=3.2)
fig.subplots_adjust(left=0.01, right=0.99, wspace=0.08)
axs = [J.map_axes(fig, 131 + k, EXT) for k in range(3)]

ax = axs[0]
cf = J.shade(ax, cloud, np.arange(0, 101, 10), H.cloud_cmap(), extend="neither")
H.place_cities(ax, ["Boston", "Concord", "Albany"], prefer={"Albany": "left"})
H.contour_smart(ax, msl, np.arange(1000, 1050, 2), fmt="%d", every=2)
J.panel_label(ax, "a", "Cloud cover (%), pressure (hPa)")
J.colorbar(fig, cf, ax, "Total cloud cover (%)", ticks=np.arange(0, 101, 20))

ax = axs[1]
cf = J.shade(ax, t2c, np.arange(-24, 9, 2), "RdYlBu_r")
J.barbs(ax, u10, v10, skip=10, length=3.6)
H.place_cities(ax, ["Boston", "Albany"], prefer={"Albany": "left"})
H.smart_arrow(ax, (clon, clat), "cold pool", prefer=(1, 1))
J.panel_label(ax, "b", "Temperature (°C), wind")
J.colorbar(fig, cf, ax, "Temperature 2 m above ground (°C)", ticks=np.arange(-24, 9, 8))

ax = axs[2]
cf = J.shade(ax, inv, np.arange(-10, 11, 2), "RdBu_r")
H.place_cities(ax, ["Boston", "Concord", "Albany"], prefer={"Albany": "left"})
J.panel_label(ax, "c", "Near-surface inversion strength (K)")
J.colorbar(fig, cf, ax, "Air 400 m up minus air at 2 m (K)", ticks=np.arange(-10, 11, 5))

out = J.save(fig, H.OUT / f"{NAME}.png")
json.dump(num, open(J.ROOT / f"_num_{NAME}.json", "w"), indent=1)
print(out)
H.finish()
