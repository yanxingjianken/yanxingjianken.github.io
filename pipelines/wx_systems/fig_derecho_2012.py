"""Derecho environment, 29 Jun 2012 (ERA5). Group C."""
import json
import numpy as np
import pandas as pd
import jstyle as J
import helpers_C as H
import cities

T_STR = "2012-06-29T18"
FEXT = (-96, -72, 33, 46)          # fetch/cache box (padded 6 deg)
EXT = (-92, -73, 32.5, 46)         # plotted box
KT = 1.94384

t850 = H.fetch_levels("temperature", T_STR, FEXT, [850]).sel(level=850) - 273.15
z500 = H.fetch_levels("geopotential", T_STR, FEXT, [500]).sel(level=500) / 9.80665 / 10.0
u5 = H.fetch_levels("u_component_of_wind", T_STR, FEXT, [500]).sel(level=500)
v5 = H.fetch_levels("v_component_of_wind", T_STR, FEXT, [500]).sel(level=500)
u10 = J.fetch("10m_u_component_of_wind", T_STR, FEXT)
v10 = J.fetch("10m_v_component_of_wind", T_STR, FEXT)
cape = J.fetch("convective_available_potential_energy", T_STR, FEXT).fillna(0).clip(min=0)
times = [str(t)[:13] for t in pd.date_range("2012-06-29T15", "2012-06-29T23", freq="1h")]
gust = H.fetch_series("instantaneous_10m_wind_gust", times, FEXT)
tp = H.fetch_series("total_precipitation", times, FEXT) * 1000.0
gmax = gust.max("time") * KT
t2s = H.fetch_series("2m_temperature", times, FEXT) - 273.15
dT3 = t2s.sel(time="2012-06-29T23") - t2s.sel(time="2012-06-29T20")
tp23 = tp.sel(time="2012-06-29T23")
tpmax = tp.max("time")
du, dv = u5 - u10, v5 - v10
shear = np.hypot(du, dv) * KT

fig = J.new_figure(height=2.45)
S = H.slots(fig, 3, gaps=[0.04, 0.03])

CITY = ["Chicago", "Columbus", "Washington"]
CW = {"Chicago": "left", "Columbus": "right", "Washington": "below"}
ax1 = J.map_axes(fig, S[0], EXT)
cf1 = J.shade(ax1, t850, np.arange(10, 31, 1), "RdYlBu_r")
cs1 = J.contour(ax1, z500, np.arange(564, 600, 3), label=False)
J.panel_label(ax1, "a", "Temperature (°C), 500-hPa height (dam)")
cb1 = J.colorbar(fig, cf1, ax1, "850-hPa temperature (°C)", ticks=np.arange(10, 31, 5), extend="both")
cities.add(ax1, CITY, where=CW)
H.clabel_avoid(ax1, cs1, list(ax1.texts))

ax2 = J.map_axes(fig, S[1], EXT)
cf2 = J.shade(ax2, cape, np.arange(0, 6001, 500), "YlOrRd", extend="max")
J.panel_label(ax2, "b", "Storm energy (CAPE), wind shear (kt)")
cb2 = J.colorbar(fig, cf2, ax2, r"Storm energy, CAPE (J kg$^{-1}$)", ticks=np.arange(0, 6001, 2000), extend="max")
cities.add(ax2, CITY, where=CW)
H.barbs_avoid(ax2, du, dv, skip=10, length=3.8, avoid=list(ax2.texts))

ax3 = J.map_axes(fig, S[2], EXT)
cf3 = J.shade(ax3, dT3, np.arange(-10, 11, 1), "RdBu_r")
cs3 = J.contour(ax3, tp23, [2.0], label=False, lw=0.6)
J.panel_label(ax3, "c", "3-h change in 2-m temperature (K)")
cb3 = J.colorbar(fig, cf3, ax3, "Change from 20 to 23 UTC (K)", ticks=np.arange(-10, 11, 5), extend="both")
cities.add(ax3, CITY, where=CW)
H.clabel_avoid(ax3, cs3, list(ax3.texts))
H.check_layout(fig, [ax1, ax2, ax3], [cb1, cb2, cb3])
J.save(fig, H.OUT / "derecho_2012.png")

box = dict(latitude=slice(EXT[3], EXT[2]), longitude=slice(EXT[0], EXT[1]))
ig = np.unravel_index(int(gmax.sel(**box).values.argmax()), gmax.sel(**box).shape)
nums = dict(
    max_cape_J_per_kg=round(float(cape.sel(**box).max()), -1),
    max_t850_C=round(float(t850.sel(**box).max()), 1),
    max_z500_dam=round(float(z500.sel(**box).max()), 1),
    max_shear_kt=round(float(shear.sel(**box).max()), 0),
    shear_kt_at_max_cape=round(float(shear.sel(**box).values.flat[int(cape.sel(**box).values.argmax())]), 0),
    max_gust_15_23Z_kt=round(float(gmax.sel(**box).max()), 0),
    max_gust_lonlat=[float(gmax.sel(**box).longitude[ig[1]]), float(gmax.sel(**box).latitude[ig[0]])],
    max_hourly_precip_15_23Z_mm=round(float(tpmax.sel(**box).max()), 1),
    min_dT2m_20_23Z_K=round(float(dT3.sel(**box).min()), 1),
    min_dT2m_lonlat=[float(dT3.sel(**box).longitude[np.unravel_index(int(dT3.sel(**box).values.argmin()), dT3.sel(**box).shape)[1]]),
                     float(dT3.sel(**box).latitude[np.unravel_index(int(dT3.sel(**box).values.argmin()), dT3.sel(**box).shape)[0]])],
    max_precip_23Z_mm_per_h=round(float(tp23.sel(**box).max()), 1),
)
json.dump(nums, open(J.ROOT / "_numbers_derecho.json", "w"), indent=1)
print(nums)
H.finish()
