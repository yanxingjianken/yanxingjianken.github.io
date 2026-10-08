"""Dryline, 20 May 2013 (Moore, OK), ERA5. Group C."""
import json
import numpy as np
import jstyle as J
import helpers_C as H
import cities

T_STR = "2013-05-20T21"
EXT = (-104, -92, 30, 40)
MOORE = (-97.49, 35.34)

td = J.fetch("2m_dewpoint_temperature", T_STR, EXT) - 273.15
t2 = J.fetch("2m_temperature", T_STR, EXT) - 273.15
ps = J.fetch("surface_pressure", T_STR, EXT) / 100.0
u10 = J.fetch("10m_u_component_of_wind", T_STR, EXT)
v10 = J.fetch("10m_v_component_of_wind", T_STR, EXT)
cape = J.fetch("convective_available_potential_energy", T_STR, EXT).fillna(0).clip(min=0)
cin = J.fetch("convective_inhibition", T_STR, EXT).fillna(0)

e = 6.112 * np.exp(17.67 * td / (td + 243.5))
w = 622.0 * e / (ps - e)                                   # g kg^-1
div = H.smooth(H.divergence(u10, v10), 1) * 1e5

# dryline position: strongest zonal Td gradient along 35.25 N (Moore latitude)
row = td.sel(latitude=35.25, method="nearest").sel(longitude=slice(-102, -95))
dtd = np.gradient(row.values, row.longitude.values)        # degC per deg lon
k = int(np.argmax(dtd))
dl_lon = float(row.longitude[k])
west = row.sel(longitude=slice(dl_lon - 1.5, dl_lon - 1.0)).mean()
east = row.sel(longitude=slice(dl_lon + 1.0, dl_lon + 1.5)).mean()
print("dryline lon at 35.25N", dl_lon, "Td west", float(west), "east", float(east))

fig = J.new_figure(height=2.75)
S = H.slots(fig, 3, gaps=[0.03, 0.03])
MX = {"Moore": MOORE}
CITY = ["Moore", "Wichita", "Dallas", "Amarillo"]
CW = {"Moore": "right", "Wichita": "right", "Dallas": "right", "Amarillo": "below"}
# the convective divergence/convergence couplet next to Moore (red-blue pair)
px_lon, px_lat, px_val = H.local_max(div, MOORE[0], MOORE[1], radius=1.0)
nx_lon, nx_lat, nx_val = H.local_min(div, MOORE[0], MOORE[1], radius=1.0)
print("couplet: div max", px_lon, px_lat, px_val, "conv max", nx_lon, nx_lat, nx_val)

ax1 = J.map_axes(fig, S[0], EXT)
cf1 = J.shade(ax1, td, np.arange(-8, 25, 2), "YlGnBu")
H.arrow_label(ax1, (dl_lon, 35.25), (dl_lon - 3.2, 37.9), "dryline")
cities.add(ax1, CITY, where=CW, extra=MX)
J.panel_label(ax1, "a", "2-m dewpoint (°C), 10-m wind (kt)")
cb1 = J.colorbar(fig, cf1, ax1, "2-m dewpoint (°C)", ticks=np.arange(-8, 25, 8), extend="both")
H.barbs_avoid(ax1, u10, v10, skip=5, length=3.8, avoid=list(ax1.texts), clear=[(dl_lon - 3.2, 37.9, 1.4)])

ax2 = J.map_axes(fig, S[1], EXT)
cf2 = J.shade(ax2, div, np.arange(-10, 11, 2), "RdBu_r")
cs2 = J.contour(ax2, w, [6, 10, 14], label=False)
J.panel_label(ax2, "b", "Convergence (blue), moisture (g kg$^{-1}$)")
cb2 = J.colorbar(fig, cf2, ax2, r"Divergence at 10 m (10$^{-5}$ s$^{-1}$)", ticks=np.arange(-10, 11, 5), extend="both")
cities.add(ax2, CITY, where=dict(CW, Moore="left"), extra=MX)
H.arrow_label(ax2, (0.5 * (px_lon + nx_lon) + 0.3, 0.5 * (px_lat + nx_lat) + 0.15), (-94.4, 36.15), "simulated\nstorm", fontsize=6.5, halo=True, linespacing=1.0)
H.clabel_avoid(ax2, cs2, list(ax2.texts), min_len=5.0)

ax3 = J.map_axes(fig, S[2], EXT)
cf3 = J.shade(ax3, cape, np.arange(0, 5001, 500), "YlOrRd", extend="max")
cs3 = J.contour(ax3, cin, [50, 200], label=False, linestyles="dashed")
J.panel_label(ax3, "c", "Storm energy and inhibition (J kg$^{-1}$)")
cb3 = J.colorbar(fig, cf3, ax3, r"Storm energy, CAPE (J kg$^{-1}$)", ticks=np.arange(0, 5001, 1000), extend="max")
cities.add(ax3, CITY, where=dict(CW, Moore="left"), extra=MX)
H.clabel_avoid(ax3, cs3, list(ax3.texts), min_len=5.0)
H.check_layout(fig, [ax1, ax2, ax3], [cb1, cb2, cb3])
J.save(fig, H.OUT / "dryline_2013.png")

box = dict(latitude=slice(EXT[3], EXT[2]), longitude=slice(EXT[0], EXT[1]))
s = lambda d: round(float(d.sel(latitude=MOORE[1], longitude=MOORE[0], method="nearest")), 1)
nums = dict(
    dryline_lon_at_35p25N=dl_lon,
    td_1p0_to_1p5deg_west_C=round(float(west), 1), td_1p0_to_1p5deg_east_C=round(float(east), 1),
    max_td_gradient_C_per_deg_lon=round(float(dtd[k]), 1),
    max_10m_convergence_1e5_per_s=round(float(-div.sel(**box).min()), 1),
    moore_cape_J_per_kg=s(cape), moore_cin_J_per_kg=s(cin), moore_td_C=s(td), moore_t2_C=s(t2),
    max_cape_J_per_kg=round(float(cape.sel(**box).max()), -1),
)
json.dump(nums, open(J.ROOT / "_numbers_dryline.json", "w"), indent=1)
print(nums)
H.finish()
