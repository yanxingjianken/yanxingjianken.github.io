"""Morning low-level inversion and mixing out, New York City, ERA5 1200 and 1800 UTC 20 Mar 2012 (group B)."""
import json
import numpy as np
import pandas as pd
import xarray as xr
import jstyle as J
import helpers_B as H

NAME = "capping_2012"
T1, T2 = "2012-03-20T12", "2012-03-20T18"
EXT = H.EXT_NE
LEVS = [1000, 975, 950, 925, 900, 850]
LGA = (-73.88, 40.78)
ASOS = J.ROOT.parent / "factcheck" / "caseB_mixout" / "asos" / "LGA.csv"     # local time (EDT)


def load(t):
    t2, sp, lcc, u10, v10 = H.getmany([(v, t, None) for v in ("2m_temperature", "surface_pressure", "low_cloud_cover",
                                                             "10m_u_component_of_wind", "10m_v_component_of_wind")], EXT)
    tl = H.getmany([("temperature", t, l) for l in LEVS], EXT)
    return dict(t2=t2, sp=sp, lcc=lcc, u10=u10, v10=v10, T=dict(zip(LEVS, tl)))


A, B = load(T1), load(T2)


for D in (A, B):
    D["inv"] = H.t_above_ground(D["T"], D["sp"], dp=50.0) - D["t2"]   # K; > 0 = warmer ~400 m above ground than at 2 m

ob = pd.read_csv(ASOS, na_values=["M"])
ob["valid"] = pd.to_datetime(ob["valid"])
ob = ob.set_index("valid")
obs1 = (ob.loc["2012-03-20 07:51", "tmpf"] - 32) * 5 / 9      # 1151 UTC
obs2 = (ob.loc["2012-03-20 13:51", "tmpf"] - 32) * 5 / 9      # 1751 UTC


def profile(D):
    ps = H.nearest(D["sp"], *LGA) / 100
    p = [ps] + [l for l in LEVS if l < ps]
    t = [H.nearest(D["t2"], *LGA) - 273.15] + [H.nearest(D["T"][l], *LGA) - 273.15 for l in LEVS if l < ps]
    return np.array(p), np.array(t)


pA, tA = profile(A)
pB, tB = profile(B)
num = {
    "LGA_ERA5_T2m_12UTC_C": round(tA[0], 1), "LGA_ERA5_T975_12UTC_C": round(H.nearest(A["T"][975], *LGA) - 273.15, 1),
    "LGA_ERA5_Tps50_minus_T2m_12UTC_K": round(H.nearest(A["inv"], *LGA), 1),
    "LGA_ERA5_lowcloud_12UTC_pct": round(H.nearest(A["lcc"], *LGA) * 100),
    "LGA_ERA5_T2m_18UTC_C": round(tB[0], 1), "LGA_ERA5_T975_18UTC_C": round(H.nearest(B["T"][975], *LGA) - 273.15, 1),
    "LGA_ERA5_Tps50_minus_T2m_18UTC_K": round(H.nearest(B["inv"], *LGA), 1),
    "LGA_ERA5_lowcloud_18UTC_pct": round(H.nearest(B["lcc"], *LGA) * 100),
    "LGA_ERA5_surface_pressure_hPa": round(pA[0], 1),
    "LGA_ASOS_T_0751EDT_C": round(float(obs1), 1), "LGA_ASOS_T_1351EDT_C": round(float(obs2), 1),
    "LGA_ASOS_T_1451EDT_F": float(ob.loc["2012-03-20 14:51", "tmpf"]),
}
print(num)

# ---- figure
fig = J.new_figure(height=3.2)
fig.subplots_adjust(left=0.01, right=0.99, wspace=0.08)
axs = [J.map_axes(fig, 131 + i, EXT) for i in range(2)]
for ax, D, letter, hh in ((axs[0], A, "a", "12"), (axs[1], B, "b", "18")):
    cf = J.shade(ax, D["inv"], np.arange(-8, 8.1, 1), "RdBu_r")
    H.place_cities(ax, ["New York", "Boston", "Philadelphia"], prefer={"New York": "lr", "Philadelphia": "left"})
    H.contour_smart(ax, D["lcc"] * 100, [80], fmt="%d", lw=0.6)
    J.panel_label(ax, letter, f"Near-surface inversion (K), {hh} UTC")
    J.colorbar(fig, cf, ax, "Air 400 m up minus air at 2 m (K)", ticks=np.arange(-8, 9, 4))

fig.canvas.draw()
p, p0 = axs[1].get_position(), axs[0].get_position()
gap = p.x0 - p0.x1
ax = fig.add_axes([p.x1 + gap + 0.045, p.y0, p.width - 0.045, p.height])
ax.plot(tA, pA, color="k", lw=1.0, marker="o", ms=2.2, label="1200 UTC")
ax.plot(tB, pB, color="k", lw=1.0, ls="--", marker="o", ms=2.2, mfc="white", label="1800 UTC")
ax.plot([obs1], [pA[0]], marker="s", ms=4, color="k", ls="none", label="obs. 1151 UTC")
ax.plot([obs2], [pB[0]], marker="s", ms=4, mfc="white", color="k", ls="none", label="obs. 1751 UTC")
H.pressure_axis(ax, pmax=1030, pmin=850, ticks=(1000, 950, 900, 850))
ax.set_xlim(4, 24)
ax.set_xticks([4, 8, 12, 16, 20, 24])
ax.set_xlabel("Temperature (°C)")
ax.set_ylabel("Pressure (hPa)", labelpad=1)
ax.legend(loc="upper right", frameon=False, fontsize=6.5, handlelength=1.8, borderaxespad=0.6)
J.panel_label(ax, "c", "Temperature at LaGuardia, NYC")
for a in axs:
    H.declutter(a)
out = J.save(fig, H.OUT / f"{NAME}.png")
json.dump(num, open(J.ROOT / f"_num_{NAME}.json", "w"), indent=1)
print(out)
H.finish()
