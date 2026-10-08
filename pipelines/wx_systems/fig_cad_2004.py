"""Cold-air damming (Appalachian wedge), ERA5 1800 UTC 26 Jan 2004 (group B, replaces cad_2007)."""
import json
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import jstyle as J
import helpers_B as H

NAME = "cad_2004"
T = "2004-01-26T18"
EXT = (-89.0, -67.0, 30.5, 47.5)
LAT_X = 36.5                                    # cross-section latitude
XLON = (-86.0, -76.0)
LEVS = [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600]

(msl, t2, u10, v10, sp_map) = H.getmany(
    [(v, T, None) for v in ("mean_sea_level_pressure", "2m_temperature", "10m_u_component_of_wind",
                            "10m_v_component_of_wind", "surface_pressure")], EXT)
msl = msl / 100
t2c = t2 - 273.15

# ---- cross-section data (narrow box, no pad)
XB = (XLON[0] - 1, XLON[1] + 1, LAT_X - 0.5, LAT_X + 0.5)
Tc = H.column("temperature", T, XB, LEVS)
Uc = H.column("u_component_of_wind", T, XB, LEVS)
Vc = H.column("v_component_of_wind", T, XB, LEVS)
(spx, zsx, t2x) = H.getmany([(v, T, None) for v in ("surface_pressure", "geopotential_at_surface", "2m_temperature")], XB, pad=0.0)

def row(da):
    return da.sel(latitude=slice(LAT_X + 0.26, LAT_X - 0.26)).mean("latitude").sel(longitude=slice(*XLON))

tx, ux, vx = row(Tc) - 273.15, row(Uc), row(Vc)
psx = row(spx) / 100
lev = tx.level.values.astype(float)
th = (tx + 273.15) * (1000.0 / tx.level) ** 0.2857
below = tx.level > psx                          # pressure-level points under the ground
# below-ground points: copy the lowest above-ground value downward (the terrain fill hides them;
# this only avoids a white gap between the data and the terrain)
def fill_down(da):
    a = da.where(~below).transpose("level", "longitude").values.copy()   # level order 1000 -> 600
    for j in range(a.shape[1]):
        col = a[:, j]
        k = np.flatnonzero(~np.isnan(col))[0]
        col[:k] = col[k]
    return xr.DataArray(a, coords=dict(level=da.level, longitude=da.longitude), dims=("level", "longitude"))
txf, thf = fill_down(tx), fill_down(th)

# ---- numbers
pts = {"GSO": (-79.94, 36.10), "RDU": (-78.79, 35.88), "IAD": (-77.45, 38.95), "DCA": (-77.04, 38.85),
       "ROA": (-79.97, 37.32), "TYS": (-83.99, 35.81), "TRI": (-82.41, 36.48), "ORF": (-76.20, 36.90)}
wd10 = np.degrees(np.arctan2(-u10, -v10)) % 360
ws10 = np.hypot(u10, v10) * 1.94384
num = {}
for k, (lo, la) in pts.items():
    num[f"T2m_{k}_C"] = round(H.nearest(t2c, lo, la), 1)
    num[f"MSLP_{k}_hPa"] = round(H.nearest(msl, lo, la), 1)
    num[f"wdir10_{k}_deg"] = round(H.nearest(wd10, lo, la))
    num[f"wspd10_{k}_kt"] = round(H.nearest(ws10, lo, la))
nb = msl.sel(latitude=slice(60, 40), longitude=slice(-85, -60))
k = np.unravel_index(int(nb.argmax().values), nb.shape)
num["Hmax_hPa"] = round(float(nb.max()), 1)
num["Hmax_lon"] = float(nb.longitude[k[1]]); num["Hmax_lat"] = float(nb.latitude[k[0]])
# column at Greensboro (from the cross-section box, nearest point)
for k2, (lo, la) in {"GSO": (-79.94, 36.10), "TYS": (-83.99, 35.81)}.items():
    col = (Tc - 273.15).sel(longitude=lo, latitude=la, method="nearest")
    ps = H.nearest(spx, lo, la) / 100
    ok = col.level <= ps
    c = col.where(ok, drop=True)
    num[f"psfc_{k2}_hPa"] = round(ps, 1)
    num[f"Tprofile_{k2}_C"] = {int(l): round(float(v), 1) for l, v in zip(c.level.values, c.values)}
    num[f"Tmax_aloft_{k2}_C"] = round(float(c.max()), 1)
    num[f"Tmax_aloft_{k2}_hPa"] = int(c.level[int(c.argmax())])
    for L in (925, 850):
        uu = float(Uc.sel(level=L).sel(longitude=lo, latitude=la, method="nearest"))
        vv = float(Vc.sel(level=L).sel(longitude=lo, latitude=la, method="nearest"))
        num[f"wdir{L}_{k2}_deg"] = round(float(np.degrees(np.arctan2(-uu, -vv)) % 360))
        num[f"wspd{L}_{k2}_kt"] = round(float(np.hypot(uu, vv) * 1.94384))
# east-west contrast along the section
t2row = row(t2x) - 273.15
num["T2m_section_min_C"] = round(float(t2row.min()), 1); num["T2m_section_min_lon"] = float(t2row.longitude[int(t2row.argmin())])
num["T2m_section_max_west_C"] = round(float(t2row.sel(longitude=slice(-86, -82)).max()), 1)
print(json.dumps(num, indent=1))

# ---- figure
fig = J.new_figure(height=3.3)
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.08], wspace=0.22, left=0.01, right=0.99)
ax = J.map_axes(fig, gs[0], EXT)
TLEV = np.arange(-12, 17, 2)
cf = J.shade(ax, H.crop(t2c, EXT), TLEV, "RdYlBu_r")
J.barbs(ax, H.crop(u10, EXT, 1), H.crop(v10, EXT, 1), skip=10, length=3.6)
ax.plot(XLON, [LAT_X, LAT_X], transform=ccrs.PlateCarree(), color="k", lw=0.7, ls=(0, (3, 2)), zorder=6)
cities = {"Washington": (-77.04, 38.90, 0.35, 0.0, "left", "top"), "Raleigh": (-78.64, 35.78, 0.3, 0.02, "left", "bottom"),
          "Greensboro": (-79.79, 36.07, -0.45, -0.3, "center", "top"), "Knoxville": (-83.92, 35.96, -0.3, 0.0, "right", "center")}
for nm, (lo, la, dx, dy, ha, va) in cities.items():
    ax.plot(lo, la, "o", ms=2.6, mfc="k", mec="w", mew=0.4, transform=ccrs.PlateCarree(), zorder=9)
    ax.text(lo + dx, la + dy, nm, fontsize=6, ha=ha, va=va,
            transform=ccrs.PlateCarree(), zorder=8,
            bbox=dict(boxstyle="square,pad=0.08", fc="w", ec="none", alpha=0.7))
cmsl = H.contour_smart(ax, H.crop(msl, EXT), np.arange(1000, 1044, 4), fmt="%d", every=1)
ax.__dict__.setdefault("_hb_clabels", []).extend(cmsl.labelTexts)   # let declutter drop labels on barbs
J.panel_label(ax, "a", "MSLP (hPa), 2-m T (°C), 10-m wind (kt)")
J.colorbar(fig, cf, ax, "2-m temperature (°C)", ticks=np.arange(-12, 17, 4), extend="both")
H.declutter(ax, barb_px=5)

# cross-section
bx = fig.add_subplot(gs[1])
X = tx.longitude.values
cs = bx.contourf(X, lev, txf.values, levels=TLEV, cmap="RdYlBu_r", extend="both", zorder=1)
cth = bx.contour(X, lev, thf.values, levels=np.arange(260, 320, 3), colors="k", linewidths=0.5, zorder=2)
for t in bx.clabel(cth, [284, 290, 296], fmt="%d", fontsize=6, inline=True, inline_spacing=2):
    if not (XLON[0] + 0.4 < t.get_position()[0] < XLON[1] - 0.6):
        t.remove()
c0 = bx.contour(X, lev, txf.values, levels=[0], colors="k", linewidths=1.2, zorder=2)
sk = 4
LB = [975, 925, 875, 825, 775, 700, 650]
xx, yy = np.meshgrid(X[::sk], LB)
ub = ux.sel(level=LB).values[:, ::sk] * 1.94384
vb = vx.sel(level=LB).values[:, ::sk] * 1.94384
ok = ~below.sel(level=LB).values[:, ::sk]
bx.barbs(xx[ok], yy[ok], ub[ok], vb[ok], length=4.2, linewidth=0.4, color="k", zorder=4)
bx.fill_between(X, psx.values, 1100, color="0.6", zorder=3, lw=0)
bx.plot(X, psx.values, color="k", lw=0.6, zorder=3)
H.pressure_axis(bx, pmax=1000, pmin=600, ticks=(1000, 925, 850, 700, 600))
bx.set_xlim(XLON)
bx.set_xticks(np.arange(-86, -75, 2))
bx.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"{-v:.0f}°W"))
bx.set_xlabel(f"Longitude along {LAT_X}°N")
J.panel_label(bx, "b", f"T (°C), θ (K), wind (kt) along {LAT_X}°N")
cb = fig.colorbar(cs, ax=bx, orientation="horizontal", fraction=0.05, pad=0.15, aspect=30,
                  ticks=np.arange(-12, 17, 4), extend="both")   # J.colorbar's pad is too small with an x-axis label
cb.set_label("Temperature (°C)", fontsize=7.5, labelpad=2)
cb.ax.tick_params(labelsize=7, width=0.5, length=2, direction="out")
cb.outline.set_linewidth(0.5)
bx.text(-78.4, 958, "cold wedge", fontsize=7, ha="center", va="center", zorder=6,
        bbox=dict(boxstyle="square,pad=0.15", fc="w", ec="none", alpha=0.8))

out = J.save(fig, H.OUT / f"{NAME}.png")
json.dump(num, open(J.ROOT / f"_num_{NAME}.json", "w"), indent=1)
print(out)
H.finish()
