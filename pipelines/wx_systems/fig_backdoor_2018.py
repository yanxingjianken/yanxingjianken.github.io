"""Backdoor cold front, eastern New England, ERA5 26 May 2018 (2000 and 2300 UTC)."""
import sys, json
import numpy as np
import jstyle as J, helpers_A as H, cities

E = H.REG
D = H.REG_DATA
TA, TB = "2018-05-26T20", "2018-05-26T23"
OUT = sys.argv[1] if len(sys.argv) > 1 else "../../images/wx_systems_v3/backdoor_2018.png"
g = lambda var, t: J.fetch(var, t, D)

fig = J.new_figure(height=4.2)
H.prep(fig)
axs = [J.map_axes(fig, 121 + i, E) for i in range(2)]
nums = {}
for k, t in enumerate((TA, TB)):
    ax = axs[k]
    t2 = g("2m_temperature", t) - 273.15
    msl = H.smooth(g("mean_sea_level_pressure", t) / 100, 2)
    u = g("10m_u_component_of_wind", t); v = g("10m_v_component_of_wind", t)
    cf = J.shade(ax, t2, np.arange(8, 33, 2), "RdYlBu_r")
    H.contour_clean(ax, msl, np.arange(996, 1041, 2), label_levels=np.arange(996, 1041, 4), extent=E)
    J.barbs(ax, u, v, skip=5, length=3.6)
    cities.add(ax, ["Boston", "Worcester", "Portland", "Quebec City"], where={"Worcester": "left", "Quebec City": "left", "Boston": "ur" if k == 0 else "right"})
    J.panel_label(ax, "ab"[k], f"{t[11:13]} UTC: pressure (hPa), 2-m temp., wind")
    J.colorbar(fig, cf, ax, "2-m temperature (°C)", ticks=np.arange(8, 33, 8))
    for nm, xy in {"Boston": (-71.03, 42.36), "Worcester": (-71.80, 42.27), "Hartford": (-72.68, 41.94), "Portland_ME": (-70.31, 43.65)}.items():
        uu, vv = H.at(u, *xy), H.at(v, *xy)
        nums.setdefault(nm, {})[t[11:13] + "Z"] = dict(T2m_C=round(H.at(t2, *xy), 1),
            Td2m_C=round(H.at(g("2m_dewpoint_temperature", t) - 273.15, *xy), 1),
            wind_dir_deg=int(round(np.degrees(np.arctan2(-uu, -vv)) % 360, -1)), wind_kt=round(float(np.hypot(uu, vv)) * 1.94384))
    if k == 1:
        pm = g("mean_sea_level_pressure", t) / 100
        nums["MSLP_23Z_hPa"] = {nm: round(H.at(pm, *xy), 1) for nm, xy in {"Quebec_City": (-71.2, 46.8), "Boston": (-71.03, 42.36), "NYC": (-73.97, 40.78)}.items()}

nums["dT_Boston_20Z_to_23Z_K"] = round(nums["Boston"]["23Z"]["T2m_C"] - nums["Boston"]["20Z"]["T2m_C"], 1)
nums["dT_Worcester_minus_Boston_23Z_K"] = round(nums["Worcester"]["23Z"]["T2m_C"] - nums["Boston"]["23Z"]["T2m_C"], 1)
print(json.dumps(nums))
H.annotate(axs[1], "backdoor"+chr(10)+"front", xy=(-71.2, 42.45), xytext=(-76.0, 44.85))
H.anchor_south(axs)
H.check_text(fig, axs)
J.save(fig, OUT)
H.finish()
