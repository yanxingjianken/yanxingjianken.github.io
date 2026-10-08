"""Bomb cyclone, 3-5 Jan 2018 (ERA5). Group C."""
import json
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import cartopy.crs as ccrs
import jstyle as J
import helpers_C as H
import cities

EXT = (-82, -58, 25, 48)
SER_EXT = (-84, -50, 26, 52)
T_MAP = "2018-01-04 12"
times = [str(t)[:13] for t in pd.date_range("2018-01-03T00", "2018-01-05T12", freq="1h")]
p = H.fetch_series("mean_sea_level_pressure", times, SER_EXT) / 100.0

# ---- track the low hourly from its first closed centre (3 Jan 10 UTC)
i0 = times.index("2018-01-03 10")
lon, lat = -76.0, 26.75
trk = []
for i in range(i0, len(times)):
    lon, lat, v = H.local_min(p.isel(time=i), lon, lat, radius=2.0)
    trk.append((times[i], lon, lat, v))
trk = pd.DataFrame(trk, columns=["time", "lon", "lat", "pmin"])
trk["dt"] = pd.to_datetime(trk.time)
trk = trk.set_index("dt")
# 24-h falls
fall = trk.pmin - trk.pmin.shift(-24)          # fall over the 24 h starting at t
istart = fall.idxmax()
iend = istart + pd.Timedelta(hours=24)
max_fall = float(fall.max())
lat_mid = float(trk.lat.loc[istart:iend].mean())
sg = 24.0 * np.sin(np.deg2rad(lat_mid)) / np.sin(np.deg2rad(60.0))
# fall over the card's window ending 4 Jan 12 UTC
t_a, t_b = pd.Timestamp("2018-01-03 12"), pd.Timestamp("2018-01-04 12")
fall_card = float(trk.pmin.loc[t_a] - trk.pmin.loc[t_b])
lat_card = float(trk.lat.loc[t_a:t_b].mean())
sg_card = 24.0 * np.sin(np.deg2rad(lat_card)) / np.sin(np.deg2rad(60.0))
pmin_overall = float(trk.pmin.min())
t_pmin = trk.pmin.idxmin()
print(trk.iloc[::3])
print("max 24h fall", max_fall, istart, iend, "lat", lat_mid, "SG", sg)
print("card window fall", fall_card, "lat", lat_card, "SG", sg_card, "min", pmin_overall, t_pmin)

# ---- fields
it = times.index(T_MAP)
mslp = p.isel(time=it)
dp24 = mslp - p.isel(time=it - 24)
tstr = "2018-01-04T12"
u3 = J.fetch("u_component_of_wind", tstr, EXT, level=300)
v3 = J.fetch("v_component_of_wind", tstr, EXT, level=300)
z5 = J.fetch("geopotential", tstr, EXT, level=500) / 9.80665 / 10.0
spd = np.hypot(u3, v3) * 1.94384

CITY = ["Boston", "New York", "Washington"]
CW1 = {"Washington": "below", "New York": "left", "Boston": "left"}
CW2 = {"Washington": "below", "New York": "left", "Boston": "left"}
fig = J.new_figure(height=2.75)
S = H.slots(fig, 3, gaps=[0.03, 0.085], rel=[1.12, 1.12, 0.76])
ax1 = J.map_axes(fig, S[0], EXT)
cf = J.shade(ax1, dp24, np.arange(-50, 51, 5), "RdBu_r")
csp = J.contour(ax1, mslp, np.arange(940, 1048, 8), label=False)
J.contour(ax1, mslp, np.arange(944, 1048, 8), label=False)
tr = trk.loc["2018-01-03 12":T_MAP]
six = tr[tr.index.hour % 6 == 0]
ax1.plot(six.lon[:-1], six.lat[:-1], "o-", color="k", ms=1.8, lw=0.6, transform=ccrs.PlateCarree(), zorder=6)
lc = trk.loc[pd.Timestamp(T_MAP)]
ax1.plot([six.lon.iloc[-2], lc.lon], [six.lat.iloc[-2], lc.lat], color="k", lw=0.6, transform=ccrs.PlateCarree(), zorder=6)
J.mark(ax1, lc.lon, lc.lat, "L", fontsize=8, bbox=dict(boxstyle="circle,pad=0.05", fc="white", ec="none"))
J.panel_label(ax1, "a", "Sea-level pressure, 24-h change (hPa)")
cb1 = J.colorbar(fig, cf, ax1, "24-h pressure change (hPa)", ticks=np.arange(-50, 51, 25), extend="both")
c1 = cities.add(ax1, CITY, where=CW1)
H.clabel_avoid(ax1, csp, c1 + [ax1.texts[0]], levels=[l for l in csp.levels if l <= 1012])

ax2 = J.map_axes(fig, S[1], EXT)
cf2 = J.shade(ax2, spd, np.arange(60, 181, 15), "Blues", extend="max")
cs5 = J.contour(ax2, z5, np.arange(480, 600, 6), label=False)
J.panel_label(ax2, "b", "300-hPa wind (kt), 500-hPa height (dam)")
cb2 = J.colorbar(fig, cf2, ax2, r"300-hPa wind speed (kt)", ticks=np.arange(60, 181, 30), extend="max")
c2 = cities.add(ax2, CITY, where=CW2)
H.clabel_avoid(ax2, cs5, c2, levels=[l for l in cs5.levels if l <= 576])

# time-series panel in slot 3, same box as the maps
ax3 = fig.add_subplot(S[2])
H.match_box(fig, ax3, ax1)
ser = trk.loc[:"2018-01-05 12"]
ax3.axvspan(istart, iend, color="0.88", lw=0, zorder=0)
ax3.plot(ser.index, ser.pmin, color="k", lw=0.9)
ax3.plot([istart, iend], [trk.pmin.loc[istart], trk.pmin.loc[iend]], "o", ms=2.2, color="k")
ax3.set_ylabel("Central pressure (hPa)", labelpad=2)
ax3.set_ylim(945, 1015)
ax3.set_yticks(np.arange(950, 1011, 10))
ax3.xaxis.set_major_locator(mdates.HourLocator(byhour=[0]))
ax3.xaxis.set_minor_locator(mdates.HourLocator(byhour=[12]))
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%d Jan"))
ax3.tick_params(which="both", top=True, right=True)
ax3.set_xlim(pd.Timestamp("2018-01-03 06"), pd.Timestamp("2018-01-05 12"))
ax3.set_xlabel("Date (UTC), 2018", labelpad=2)
ax3.text(istart + pd.Timedelta(hours=12), 1009, f"{max_fall:.0f} hPa\nin 24 h", ha="center",
         va="top", fontsize=7)
J.panel_label(ax3, "c", "Pressure at storm centre")
H.check_layout(fig, [ax1, ax2, ax3], [cb1, cb2])
out = J.save(fig, H.OUT / "bomb_2018.png")
print(out)

nums = dict(
    max_24h_fall_hPa=round(max_fall, 1),
    max_fall_window_utc=[str(istart), str(iend)],
    mean_lat_max_window_degN=round(lat_mid, 1),
    sanders_gyakum_threshold_max_window_hPa=round(sg, 1),
    bergeron_ratio_max_window=round(max_fall / sg, 2),
    fall_3Jan12_to_4Jan12_hPa=round(fall_card, 1),
    mean_lat_3Jan12_to_4Jan12_degN=round(lat_card, 1),
    sanders_gyakum_threshold_card_window_hPa=round(sg_card, 1),
    central_pressure_3Jan12_hPa=round(float(trk.pmin.loc[t_a]), 1),
    central_pressure_4Jan12_hPa=round(float(trk.pmin.loc[t_b]), 1),
    min_central_pressure_hPa=round(pmin_overall, 1),
    min_central_pressure_time=str(t_pmin),
    max_300hPa_wind_kt=round(float(spd.sel(longitude=slice(EXT[0], EXT[1]), latitude=slice(EXT[3], EXT[2])).max()), 0),
)
json.dump(nums, open(J.ROOT / "_numbers_bomb.json", "w"), indent=1)
print(nums)

H.finish()
