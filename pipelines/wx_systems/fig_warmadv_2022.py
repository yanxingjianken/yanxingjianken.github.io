"""Overrunning / warm advection and a near-midnight daily high at Boston,
ERA5 0300 UTC 23 Feb 2022 plus hourly ASOS at BOS (group B)."""
import json
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import jstyle as J
import helpers_B as H

NAME = "warmadv_2022"
T = "2022-02-23T03"
EXT = H.EXT_NE
ASOS = J.ROOT.parent / "factcheck" / "caseB_warmadv" / "wind" / "BOS_2022-02-22.csv"   # times in EST (LST)

(msl, t2, u10, v10, t850, u850, v850) = H.getmany(
    [(v, T, None) for v in ("mean_sea_level_pressure", "2m_temperature", "10m_u_component_of_wind",
                            "10m_v_component_of_wind")]
    + [(v, T, 850) for v in ("temperature", "u_component_of_wind", "v_component_of_wind")], EXT)
msl = msl / 100
t2c = t2 - 273.15
t850c = t850 - 273.15
ts = H.smooth(t850, 2)
dtdx, dtdy = H.ddx_ddy(ts)
adv = -(u850 * dtdx + v850 * dtdy) * 3600.0          # K h-1, > 0 warm advection

# ---- ASOS
ob = pd.read_csv(ASOS, na_values=["M"])
ob["valid"] = pd.to_datetime(ob["valid"])
ob = ob[(ob.valid >= "2022-02-22 00:00") & (ob.valid <= "2022-02-23 06:59")].copy()
ob["tc"] = (ob.tmpf - 32) * 5 / 9
day = ob[ob.valid.dt.date == pd.Timestamp("2022-02-22").date()]
imax = day.tmpf.idxmax()

BOS = (-71.01, 42.36)
box = dict(longitude=slice(EXT[0], EXT[1]), latitude=slice(EXT[3], EXT[2]))
num = {
    "BOS_ERA5_T2m_C": round(H.nearest(t2c, *BOS), 1),
    "BOS_ERA5_adv850_K_per_h": round(H.nearest(adv, *BOS), 2),
    "BOS_ERA5_wdir850_deg": round(float(H.nearest(np.degrees(np.arctan2(-u850, -v850)) % 360, *BOS))),
    "BOS_ERA5_wspd850_kt": round(H.nearest(np.hypot(u850, v850), *BOS) * 1.94384),
    "adv850_max_K_per_h_box": round(float(adv.sel(**box).max()), 2),
    "ASOS_BOS_calday_max_F": float(day.tmpf.max()),
    "ASOS_BOS_calday_max_time_LST": str(day.loc[imax, "valid"]),
    "ASOS_BOS_T_1654LST_F": float(ob.set_index("valid").tmpf.get(pd.Timestamp("2022-02-22 16:54"))),
    "ASOS_BOS_T_2354LST_F": float(ob.set_index("valid").tmpf.get(pd.Timestamp("2022-02-22 23:54"))),
    "ASOS_BOS_T_0254LST_23Feb_F": float(ob.set_index("valid").tmpf.get(pd.Timestamp("2022-02-23 02:54"))),
    "ASOS_BOS_calday_min_F": float(day.tmpf.min()),
    "sunset_LST": "17:27", "sunrise_23Feb_LST": "06:29",
}
print(num)

# ---- figure
fig = J.new_figure(height=3.2)
fig.subplots_adjust(left=0.01, right=0.99, wspace=0.08)
axs = [J.map_axes(fig, 131 + i, EXT) for i in range(2)]

ax = axs[0]
cf = J.shade(ax, t2c, np.arange(-10, 19, 2), "RdYlBu_r")
J.barbs(ax, u10, v10, skip=8, length=3.6)
H.place_cities(ax, ["Boston", "New York", "Albany"])
H.contour_smart(ax, msl, np.arange(980, 1040, 2), fmt="%d", every=2)
J.panel_label(ax, "a", "Temperature (°C), pressure (hPa)")
J.colorbar(fig, cf, ax, "Temperature 2 m above ground (°C)", ticks=np.arange(-10, 19, 5))

ax = axs[1]
cf = J.shade(ax, adv, np.arange(-1.5, 1.51, 0.25), "RdBu_r")
J.barbs(ax, u850, v850, skip=8, length=3.6)
lev = np.arange(-16, 17, 2)
H.place_cities(ax, ["Boston", "New York", "Albany"])
H.contour_smart(ax, t850c, lev, fmt="%d", every=2,
                linestyles=["dashed" if x < 0 else "solid" for x in lev])
J.panel_label(ax, "b", "Warm-air advection, 850 hPa (K h$^{-1}$)")
cb = J.colorbar(fig, cf, ax, "Warm (+) or cold (−) advection (K h$^{-1}$)", ticks=np.arange(-1.5, 1.6, 0.5))
cb.ax.xaxis.set_major_formatter(__import__("matplotlib").ticker.FormatStrFormatter("%g"))

# (c) station time series, same box size as the map panels
fig.canvas.draw()
p = axs[1].get_position()
p0 = axs[0].get_position()
gap = p.x0 - p0.x1
ax = fig.add_axes([p.x1 + gap + 0.045, p.y0, p.width - 0.045, p.height])
ax.plot(ob.valid, ob.tc, color="k", lw=0.9, marker="o", ms=1.8)
ax.axvline(pd.Timestamp("2022-02-23 00:00"), color="k", lw=0.5, ls="--")
for t0, t1 in [(pd.Timestamp("2022-02-22 00:00"), pd.Timestamp("2022-02-22 06:29")),
               (pd.Timestamp("2022-02-22 17:27"), pd.Timestamp("2022-02-23 06:29"))]:
    ax.axvspan(t0, t1, color="0.88", lw=0, zorder=0)
ax.plot(day.loc[imax, "valid"], (day.loc[imax, "tmpf"] - 32) * 5 / 9, marker="v", color="k", ms=4,
        ls="none", zorder=5)
ax.set_xlim(pd.Timestamp("2022-02-22 00:00"), pd.Timestamp("2022-02-23 07:00"))
ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 6, 12, 18]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
ax.set_xlabel("Hour (EST), 22–23 Feb")
ax.set_ylabel("Temperature (°C)", labelpad=1)
ax.set_ylim(-2, 16)
ax.set_yticks([0, 5, 10, 15])
ax.tick_params(top=True, right=True)
for sp in ax.spines.values():
    sp.set_linewidth(0.6)
ax.annotate("daily high", xy=(day.loc[imax, "valid"], (day.loc[imax, "tmpf"] - 32) * 5 / 9 + 0.6),
            xytext=(pd.Timestamp("2022-02-22 13:00"), 14.2), fontsize=7, ha="center",
            arrowprops=dict(arrowstyle="-|>", lw=0.6, color="k", mutation_scale=6, shrinkA=1, shrinkB=2))
J.panel_label(ax, "c", "Hourly temperature, Boston (°C)")

for a in axs:
    H.declutter(a)
out = J.save(fig, H.OUT / f"{NAME}.png")
json.dump(num, open(J.ROOT / f"_num_{NAME}.json", "w"), indent=1)
print(out)
H.finish()
