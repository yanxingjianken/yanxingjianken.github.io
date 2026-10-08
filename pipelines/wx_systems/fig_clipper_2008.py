"""Alberta clipper crossing New England, 22-23 Jan 2008 (ERA5). Group C."""
import json
import numpy as np
import cartopy.crs as ccrs
import jstyle as J
import helpers_C as H
import cities

T_STR = "2008-01-23T00"
T_M12 = "2008-01-22T12"
EXT = (-88, -64, 34, 52)

mslp = J.fetch("mean_sea_level_pressure", T_STR, EXT) / 100.0
t2 = J.fetch("2m_temperature", T_STR, EXT) - 273.15
u10 = J.fetch("10m_u_component_of_wind", T_STR, EXT)
v10 = J.fetch("10m_v_component_of_wind", T_STR, EXT)
uv = H.fetch_levels("u_component_of_wind", T_STR, EXT, [500])
vv = H.fetch_levels("v_component_of_wind", T_STR, EXT, [500])
z0 = H.fetch_levels("geopotential", T_STR, EXT, [500, 1000]) / 9.80665
z1 = H.fetch_levels("geopotential", T_M12, EXT, [500, 1000]) / 9.80665

zeta = H.rel_vort(uv.sel(level=500), vv.sel(level=500))
zeta = H.smooth(zeta, 2) * 1e5
thk = (z0.sel(level=500) - z0.sel(level=1000)) / 10.0          # dam
thk_prev = (z1.sel(level=500) - z1.sel(level=1000)) / 10.0
dthk = thk - thk_prev

# surface low and 500-hPa vorticity maximum
lo_lon, lo_lat, lo_p = H.local_min(mslp, -74.5, 45.0, radius=2.5)
vx_lon, vx_lat, vx_val = H.local_max(zeta, lo_lon, lo_lat, radius=4.5)
R = 6371.0
dx = np.deg2rad(vx_lon - lo_lon) * np.cos(np.deg2rad(0.5 * (lo_lat + vx_lat))) * R
dy = np.deg2rad(vx_lat - lo_lat) * R
dist = float(np.hypot(dx, dy))
bearing = float((np.degrees(np.arctan2(dx, dy)) + 360) % 360)
print("low", lo_lon, lo_lat, lo_p, "vortmax", vx_lon, vx_lat, vx_val, "dist", dist, "bearing", bearing)

fig = J.new_figure(height=2.55)
S = H.slots(fig, 3, gaps=[0.03, 0.03])

CITY = ["Toronto", "Albany", "New York", "Boston"]
CW = {"Toronto": "below", "Albany": "above", "New York": "left", "Boston": "right"}
ax1 = J.map_axes(fig, S[0], EXT)
cf1 = J.shade(ax1, zeta, np.arange(-16, 17, 2), "RdBu_r")
cs1 = J.contour(ax1, mslp, np.arange(980, 1048, 4), label=False)
J.mark(ax1, lo_lon, lo_lat, "L", fontsize=8, bbox=dict(boxstyle="circle,pad=0.05", fc="white", ec="none"))
J.panel_label(ax1, "a", "Spin at 500 hPa, sea-level pressure")
cb1 = J.colorbar(fig, cf1, ax1, r"Spin at 500 hPa (10$^{-5}$ s$^{-1}$)", ticks=np.arange(-16, 17, 8), extend="both")
cities.add(ax1, CITY, where=CW)
H.clabel_avoid(ax1, cs1, list(ax1.texts))

ax2 = J.map_axes(fig, S[1], EXT)
cf2 = J.shade(ax2, dthk, np.arange(-12, 13, 2), "RdBu_r")
cs2 = J.contour(ax2, thk, np.arange(480, 570, 6), label=False)
J.panel_label(ax2, "b", "Thickness and its 12-h change (dam)")
cb2 = J.colorbar(fig, cf2, ax2, "12-h thickness change (dam)", ticks=np.arange(-12, 13, 6), extend="both")
cities.add(ax2, CITY, where=CW)
H.clabel_avoid(ax2, cs2, list(ax2.texts))

ax3 = J.map_axes(fig, S[2], EXT)
cf3 = J.shade(ax3, t2, np.arange(-24, 25, 2), "RdYlBu_r")
J.panel_label(ax3, "c", "2-m temperature (°C), 10-m wind (kt)")
cb3 = J.colorbar(fig, cf3, ax3, "2-m temperature (°C)", ticks=np.arange(-24, 25, 12), extend="both")
cities.add(ax3, CITY, where=CW)
H.barbs_avoid(ax3, u10, v10, skip=10, length=3.8, avoid=list(ax3.texts))
H.check_layout(fig, [ax1, ax2, ax3], [cb1, cb2, cb3])
J.save(fig, H.OUT / "clipper_2008.png")

box = dict(latitude=slice(EXT[3], EXT[2]), longitude=slice(EXT[0], EXT[1]))
nums = dict(
    surface_low_lon=lo_lon, surface_low_lat=lo_lat, surface_low_mslp_hPa=round(lo_p, 1),
    vort500_max_lon=vx_lon, vort500_max_lat=vx_lat, vort500_max_1e5_per_s=round(vx_val, 1),
    vortmax_to_low_distance_km=round(dist, 0), vortmax_bearing_from_low_deg=round(bearing, 0),
    max_12h_thickness_fall_dam=round(float(-dthk.sel(**box).min()), 1),
    min_t2m_C=round(float(t2.sel(**box).min()), 1),
)
json.dump(nums, open(J.ROOT / "_numbers_clipper.json", "w"), indent=1)
print(nums)
H.finish()
