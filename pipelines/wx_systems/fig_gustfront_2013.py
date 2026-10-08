"""Gust front / cold pool environment, 8 Jul 2013, New England (ERA5). Group C."""
import json
import numpy as np
import pandas as pd
import jstyle as J
import helpers_C as H
import cities

T_STR = "2013-07-08T18"
EXT = (-79, -67, 40, 47.5)
KT = 1.94384

t2 = J.fetch("2m_temperature", T_STR, EXT) - 273.15
u10 = J.fetch("10m_u_component_of_wind", T_STR, EXT)
v10 = J.fetch("10m_v_component_of_wind", T_STR, EXT)
cape = J.fetch("convective_available_potential_energy", T_STR, EXT).fillna(0).clip(min=0)
u5 = H.fetch_levels("u_component_of_wind", T_STR, EXT, [500]).sel(level=500)
v5 = H.fetch_levels("v_component_of_wind", T_STR, EXT, [500]).sel(level=500)
times = [str(t)[:13] for t in pd.date_range("2013-07-08T07", "2013-07-08T15", freq="1h")]
tp = H.fetch_series("total_precipitation", times, EXT) * 1000.0
pacc = tp.sum("time")                          # mm, 06-15 UTC (hourly totals ending 07..15 UTC)
du, dv = u5 - u10, v5 - v10
shear = np.hypot(du, dv) * KT

# boundary: strongest meridional 2-m T gradient along 72 W between 41.8 and 44.5 N
col = t2.sel(longitude=-72.0, method="nearest").sel(latitude=slice(44.5, 41.8))
g = np.gradient(col.values, col.latitude.values)           # degC per deg lat (lat descending)
kb = int(np.argmin(g))                                      # T falls northward fastest
b_lat = float(col.latitude[kb])
t_s = float(t2.sel(longitude=-72.0, latitude=b_lat - 0.75, method="nearest"))
t_n = float(t2.sel(longitude=-72.0, latitude=b_lat + 0.75, method="nearest"))
print("boundary lat at 72W", b_lat, "T south", t_s, "T north", t_n)

fig = J.new_figure(height=3.6)
S = H.slots(fig, 2, gaps=[0.04])
CITY = ["Albany", "Concord", "Portland", "Boston"]
CW = {"Albany": "below", "Concord": "left", "Portland": "right", "Boston": "below"}

ax1 = J.map_axes(fig, S[0], EXT)
cf1 = J.shade(ax1, t2, np.arange(16, 35, 1), "RdYlBu_r")
H.arrow_label(ax1, (-72.0, b_lat), (-75.0, 45.4), "boundary")
cities.add(ax1, CITY, where=CW)
J.panel_label(ax1, "a", "2-m temperature (°C), 10-m wind (kt)")
cb1 = J.colorbar(fig, cf1, ax1, "2-m temperature (°C)", ticks=np.arange(16, 35, 6), extend="both")
H.barbs_avoid(ax1, u10, v10, skip=5, length=4.2, avoid=list(ax1.texts), clear=[(-75.0, 45.4, 1.6)])

ax2 = J.map_axes(fig, S[1], EXT)
cf2 = J.shade(ax2, pacc.where(pacc >= 0.5), [0.5, 1, 2, 5, 10, 20], "YlGnBu", extend="max")
cs2 = J.contour(ax2, H.smooth(t2, 1), [24, 28], label=False)
J.panel_label(ax2, "b", "Morning rain (mm), 2-m temperature (°C)")
cb2 = J.colorbar(fig, cf2, ax2, "Rain, 06–15 UTC (mm)", ticks=[0.5, 1, 2, 5, 10, 20], extend="max")
cb2.ax.set_xticklabels(["0.5", "1", "2", "5", "10", "20"])
cities.add(ax2, CITY, where=CW)
H.clabel_avoid(ax2, cs2, list(ax2.texts), min_len=6.0)
H.check_layout(fig, [ax1, ax2], [cb1, cb2])
J.save(fig, H.OUT / "gustfront_2013.png")

box = dict(latitude=slice(EXT[3], EXT[2]), longitude=slice(EXT[0], EXT[1]))
nums = dict(
    boundary_lat_at_72W=b_lat, t2m_0p75deg_south_C=round(t_s, 1), t2m_0p75deg_north_C=round(t_n, 1),
    max_cape_18Z_J_per_kg=round(float(cape.sel(**box).max()), -1),
    max_shear_18Z_kt=round(float(shear.sel(**box).max()), 0),
    median_shear_18Z_kt=round(float(shear.sel(**box).median()), 0),
    max_precip_06_15Z_mm=round(float(pacc.sel(**box).max()), 1),
    max_t2m_18Z_C=round(float(t2.sel(**box).max()), 1),
)
json.dump(nums, open(J.ROOT / "_numbers_gustfront.json", "w"), indent=1)
print(nums)
H.finish()
