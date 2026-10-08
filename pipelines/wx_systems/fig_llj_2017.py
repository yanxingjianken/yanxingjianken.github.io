"""Nocturnal low-level jet over central New York, ERA5 2100 UTC 10 Jun and 0800 UTC 11 Jun 2017 (group B)."""
import json
import numpy as np
import jstyle as J
import helpers_B as H

NAME = "llj_2017"
TA, TB = "2017-06-10T21", "2017-06-11T08"
EXT = H.EXT_NE
LEVS = [1000, 975, 950, 925, 900, 850, 800, 750, 700]
PLEV = 900
ELM = (-76.89, 42.16)                 # Elmira, NY (named in the BGM AFD)
KT = 1.94384


def load(t):
    sp, u10, v10 = H.getmany([(v, t, None) for v in ("surface_pressure", "10m_u_component_of_wind",
                                                     "10m_v_component_of_wind")], EXT)
    U = H.getmany([("u_component_of_wind", t, l) for l in LEVS], EXT)
    V = H.getmany([("v_component_of_wind", t, l) for l in LEVS], EXT)
    return dict(sp=sp, u10=u10, v10=v10, U=dict(zip(LEVS, U)), V=dict(zip(LEVS, V)))


A, B = load(TA), load(TB)
Z = dict(zip(LEVS, H.getmany([("geopotential", TB, l) for l in LEVS], EXT)))   # m2 s-2


def vg_speed(phi):
    """Geostrophic wind speed (m s-1) from geopotential, after light smoothing."""
    ph = H.smooth(phi, 3)
    dx, dy = H.ddx_ddy(ph)
    f = 2 * 7.2921e-5 * np.sin(np.deg2rad(ph.latitude))
    return np.hypot(-dy / f, dx / f)


def prof(D, vg=False):
    ps = H.nearest(D["sp"], *ELM) / 100
    p = [ps]
    s = [H.nearest(np.hypot(D["u10"], D["v10"]), *ELM)]
    for l in LEVS:
        if l < ps - 5:
            p.append(l)
            s.append(H.nearest(np.hypot(D["U"][l], D["V"][l]), *ELM))
    return np.array(p), np.array(s) * KT


pA, sA = prof(A)
pB, sB = prof(B)
pg = [l for l in LEVS if l < pB[0] - 5]
sg = np.array([H.nearest(vg_speed(Z[l]), *ELM) for l in pg]) * KT

spdA = np.hypot(A["U"][PLEV], A["V"][PLEV]) * KT
spdB = np.hypot(B["U"][PLEV], B["V"][PLEV]) * KT
num = {
    "ELM_surface_pressure_hPa": round(pB[0], 1),
    "ELM_wind_profile_21UTC_kt": dict(zip([round(x) for x in pA], [round(x, 1) for x in sA])),
    "ELM_wind_profile_08UTC_kt": dict(zip([round(x) for x in pB], [round(x, 1) for x in sB])),
    "ELM_geostrophic_08UTC_kt": dict(zip(pg, [round(x, 1) for x in sg])),
    "ELM_900_21UTC_kt": round(H.nearest(spdA, *ELM), 1), "ELM_900_08UTC_kt": round(H.nearest(spdB, *ELM), 1),
    "ELM_10m_21UTC_kt": round(sA[0], 1), "ELM_10m_08UTC_kt": round(sB[0], 1),
}
land = dict(longitude=slice(-81, -73), latitude=slice(44.5, 39.5))
for k, D in (("21UTC", A), ("08UTC", B)):
    s = (np.hypot(D["U"][PLEV], D["V"][PLEV]) * KT).where(D["sp"] / 100 > PLEV + 10).sel(**land)
    num[f"max_900_land_{k}_kt"] = round(float(s.max()), 1)
    i = s.argmax(...)
    num[f"max_900_land_{k}_lonlat"] = [float(s.longitude[i["longitude"]]), float(s.latitude[i["latitude"]])]
print(num)

# ---- figure
fig = J.new_figure(height=3.2)
fig.subplots_adjust(left=0.01, right=0.99, wspace=0.08)
axs = [J.map_axes(fig, 131 + i, EXT) for i in range(2)]
lev = np.arange(0, 51, 5)
for ax, D, spd, letter, hh in ((axs[0], A, spdA, "a", "21 UTC 10 Jun"), (axs[1], B, spdB, "b", "08 UTC 11 Jun")):
    cf = J.shade(ax, spd.where(D["sp"] / 100 > PLEV), lev, "PuBu", extend="max")
    J.barbs(ax, D["U"][PLEV], D["V"][PLEV], skip=8, length=3.6)
    H.place_cities(ax, ["Elmira", "New York", "Boston"], extra={"Elmira": ELM})
    J.panel_label(ax, letter, f"Wind at 900 hPa (kt), {hh}")
    J.colorbar(fig, cf, ax, "Wind speed at 900 hPa (kt)", ticks=np.arange(0, 51, 10), extend="max")

fig.canvas.draw()
p, p0 = axs[1].get_position(), axs[0].get_position()
gap = p.x0 - p0.x1
ax = fig.add_axes([p.x1 + gap + 0.045, p.y0, p.width - 0.045, p.height])
ax.plot(sA, pA, color="k", lw=1.0, ls="--", marker="o", ms=2.2, mfc="white", label="2100 UTC")
ax.plot(sB, pB, color="k", lw=1.0, marker="o", ms=2.2, label="0800 UTC")
ax.plot(sg, pg, color="0.45", lw=1.0, ls=":", label="geostrophic")
H.pressure_axis(ax, pmax=1000, pmin=750, ticks=(1000, 950, 900, 850, 800, 750))
ax.set_xlim(0, 70)
ax.set_xticks([0, 20, 40, 60])
ax.set_xlabel("Wind speed (kt)")
ax.set_ylabel("Pressure (hPa)", labelpad=1)
ax.legend(loc="upper right", frameon=False, fontsize=6.5, handlelength=1.8, borderaxespad=0.6)
J.panel_label(ax, "c", "Wind profile at Elmira, NY")
for a in axs:
    H.declutter(a)
out = J.save(fig, H.OUT / f"{NAME}.png")
json.dump(num, open(J.ROOT / f"_num_{NAME}.json", "w"), indent=1, default=float)
print(out)
H.finish()
