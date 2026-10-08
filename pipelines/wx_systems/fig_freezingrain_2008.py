"""Freezing rain: 11-12 Dec 2008 New England ice storm (ERA5). Group C."""
import json
import numpy as np
import matplotlib.ticker as mticker
import jstyle as J
import helpers_C as H
import cities

T_STR = "2008-12-12T09"
EXT = (-79, -67, 40, 47.5)
LV = [500, 550, 600, 650, 700, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000]
SITE = ("Manchester, NH", -71.43, 42.93)

T = H.fetch_levels("temperature", T_STR, EXT, LV) - 273.15
Q = H.fetch_levels("specific_humidity", T_STR, EXT, LV)
t2 = J.fetch("2m_temperature", T_STR, EXT) - 273.15
d2 = J.fetch("2m_dewpoint_temperature", T_STR, EXT) - 273.15
ps = J.fetch("surface_pressure", T_STR, EXT) / 100.0
tp = J.fetch("total_precipitation", T_STR, EXT) * 1000.0

T = T.sortby("level", ascending=False)   # 1000 -> 500
Q = Q.sortby("level", ascending=False)
lev = T.level.values.astype(float)


def column(i, j):
    """Profile from the surface up: p (hPa, decreasing), T (degC)."""
    sp = float(ps.values[i, j])
    keep = lev < sp - 1.0
    p = np.r_[sp, lev[keep]]
    t = np.r_[float(t2.values[i, j]), T.values[keep, i, j]]
    return p, t


def energies(p, t):
    """Bourgouin-type areas, Rd * int (T - 0 degC) dln p (J kg^-1).

    NA: negative area of the surface-based sub-freezing layer below the warm layer.
    PA: positive area of the elevated warm (> 0 degC) layer above it.
    Returns (PA, NA, Tmax_warm, warm_base_hPa, warm_top_hPa) or NaNs if no such profile.
    """
    if t[0] >= 0:
        return (np.nan,) * 5
    lnp = np.log(p)
    # fine resampling in ln p for accurate crossings
    x = np.linspace(lnp[0], lnp[-1], 600)
    tt = np.interp(-x, -lnp, t)
    pos = tt > 0
    if not pos.any():
        return (np.nan,) * 5
    k1 = np.argmax(pos)                     # first warm point above the cold layer
    rest = ~pos[k1:]
    k2 = k1 + (np.argmax(rest) if rest.any() else len(rest))
    dx = -np.diff(x)                        # positive (going up, ln p decreases)
    seg = 0.5 * (tt[1:] + tt[:-1])
    na = H.RD * np.sum(seg[:k1] * dx[:k1])
    pa = H.RD * np.sum(seg[k1:k2 - 1] * dx[k1:k2 - 1])
    return pa, na, tt[k1:k2].max(), np.exp(x[k1]), np.exp(x[k2 - 1])


ny, nx = t2.shape
PA = np.full((ny, nx), np.nan); NA = PA.copy(); TW = PA.copy()
for i in range(ny):
    for j in range(nx):
        pa, na, tw, _, _ = energies(*column(i, j))
        PA[i, j], NA[i, j], TW[i, j] = pa, na, tw
PA = t2.copy(data=PA); NA = t2.copy(data=NA); TW = t2.copy(data=TW)

# site sounding
i = int(np.abs(t2.latitude.values - SITE[2]).argmin()); j = int(np.abs(t2.longitude.values - SITE[1]).argmin())
p_s, t_s = column(i, j)
pa_s, na_s, tw_s, pb_s, pt_s = energies(p_s, t_s)
# dewpoint from q
qcol = Q.values[:, i, j]
keep = lev < float(ps.values[i, j]) - 1.0
e = qcol[keep] * lev[keep] / (0.622 + 0.378 * qcol[keep])          # hPa
td_lv = 243.5 * np.log(e / 6.112) / (17.67 - np.log(e / 6.112))
td_s = np.r_[float(d2.values[i, j]), td_lv]

fig = J.new_figure(height=2.75)
S = H.slots(fig, 3, gaps=[0.03, 0.085])
CITY = ["Manchester", "Boston", "Albany"]
CW = {"Manchester": "above", "Albany": "below", "Boston": "lr"}
ax1 = J.map_axes(fig, S[0], EXT)
cf = J.shade(ax1, TW, np.arange(0, 13, 1), H.half_cmap("RdYlBu_r", 0.55, 1.0), extend="max")
cs = J.contour(ax1, t2, [-6, -4, -2], label=False, linestyles="dashed")
cs0 = J.contour(ax1, t2, [0], label=False, lw=1.0)
J.panel_label(ax1, "a", "Warm air aloft, 2-m temperature (°C)")
cb1 = J.colorbar(fig, cf, ax1, "Warmest temperature aloft (°C)", ticks=np.arange(0, 13, 3), extend="max")
c1 = cities.add(ax1, CITY, where=CW)
H.clabel_avoid(ax1, cs, c1)
H.clabel_avoid(ax1, cs0, c1)

ax2 = J.map_axes(fig, S[1], EXT)
cf2 = J.shade(ax2, PA, np.arange(0, 301, 25), "Reds", extend="max")
cs2 = J.contour(ax2, NA, [-100, -50, -25], label=False, linestyles="dashed")
J.panel_label(ax2, "b", "Melting, refreezing energy (J kg$^{-1}$)")
cb2 = J.colorbar(fig, cf2, ax2, r"Melting energy, PA (J kg$^{-1}$)", ticks=np.arange(0, 301, 100), extend="max")
c2 = cities.add(ax2, CITY, where=CW)
H.clabel_avoid(ax2, cs2, c2, cross=False)

ax3 = fig.add_subplot(S[2])
pp = np.exp(np.linspace(np.log(p_s[0]), np.log(500), 400))
tt = np.interp(-np.log(pp), -np.log(p_s), t_s)
ax3.fill_betweenx(pp, 0, tt, where=tt > 0, color="#d6604d", alpha=0.45, lw=0)
ax3.fill_betweenx(pp, 0, tt, where=(tt < 0) & (pp > pb_s), color="#4393c3", alpha=0.45, lw=0)
ax3.axvline(0, color="k", lw=0.5, ls=(0, (3, 2)))
ax3.plot(t_s, p_s, color="k", lw=1.0, label="Temperature")
ax3.plot(td_s, p_s, color="k", lw=0.8, ls="--", label="Dewpoint")
ax3.set_yscale("log")
ax3.set_ylim(1000, 500)
ax3.set_yticks([1000, 925, 850, 700, 600, 500])
ax3.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))
ax3.yaxis.set_minor_locator(mticker.NullLocator())
ax3.set_xlim(-25, 15)
ax3.set_xticks(np.arange(-20, 16, 10))
ax3.set_xlabel("Temperature (°C)", labelpad=2)
ax3.set_ylabel("Pressure (hPa)", labelpad=2)
ax3.tick_params(which="both", top=True, right=True)
ax3.legend(loc="lower left", bbox_to_anchor=(0.0, 0.27), frameon=False, handlelength=1.8, borderaxespad=0.3, fontsize=6.5)
ax3.text(10.8, 745, "melting\n(PA)", ha="center", va="center", fontsize=6.5, linespacing=1.0)
ax3.text(-3.6, 965, "refreezing (NA)", ha="right", va="center", fontsize=6.5)
J.panel_label(ax3, "c", "Sounding, Manchester, NH")
H.match_box(fig, ax3, ax1)
H.check_layout(fig, [ax1, ax2, ax3], [cb1, cb2])
J.save(fig, H.OUT / "freezingrain_2008.png")

box = dict(latitude=slice(47.5, 40), longitude=slice(-79, -67))
fz = (np.isfinite(PA) & (tp > 0.1)).sel(**box)
nums = dict(
    site=SITE[0], site_grid=[float(t2.longitude[j]), float(t2.latitude[i])],
    site_T2m_C=round(float(t2.values[i, j]), 1), site_Td2m_C=round(float(d2.values[i, j]), 1),
    site_surface_pressure_hPa=round(float(ps.values[i, j]), 0),
    site_warm_nose_Tmax_C=round(float(tw_s), 1), site_warm_layer_base_hPa=round(float(pb_s), 0),
    site_warm_layer_top_hPa=round(float(pt_s), 0),
    site_PA_J_per_kg=round(float(pa_s), 0), site_NA_J_per_kg=round(float(na_s), 0),
    site_precip_mm_per_h=round(float(tp.values[i, j]), 1),
    domain_max_warm_nose_T_C=round(float(TW.sel(**box).max()), 1),
    n_gridpoints_fzra_profile_with_precip_gt_0p1=int(fz.sum()),
)
json.dump(nums, open(J.ROOT / "_numbers_freezingrain.json", "w"), indent=1)
print(nums)

H.finish()
