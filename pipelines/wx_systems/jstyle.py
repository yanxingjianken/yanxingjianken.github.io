"""Shared journal (AMS/AGU-style) figure conventions for the 051 NE weather-systems page.

Every figure on the page must be drawn through this module so the 21 figures read as one set.

Conventions
-----------
* Arial 8 pt everywhere (AMS asks for a sans-serif figure font, >= 6 pt at final size).
* Full page width = 6.5 in (AMS two-column width, 39 pc). 300 dpi PNG.
* No figure suptitle and no sentence-long panel titles: the explanation belongs in the HTML
  caption. Each panel gets a bold panel label "(a)" at top-left and a SHORT field label
  (<= 45 characters, e.g. "MSLP (hPa), 2-m T (°C)") left-aligned above the map.
* Every shaded field has a colorbar with the variable symbol and units, ticks at round values,
  scaled to readable magnitudes (e.g. vorticity in 10^-5 s^-1, not 0.00015).
* Contours are black (solid positive / dashed negative where signed), 0.5 pt, labels 6 pt.
* Coastlines 0.5 pt black, state/province lines 0.3 pt grey, no land fill, no grey masks
  over the data. Light graticule only if it helps orientation.
* Colormaps: diverging fields -> "RdBu_r" centered on zero; temperature -> "RdYlBu_r";
  moisture/precip -> sequential ("YlGnBu" / "Blues"); cloud -> "Greys_r". Never jet/rainbow.
"""
from __future__ import annotations

import os
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache"
CACHE.mkdir(exist_ok=True)

ARCO_URL = "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3"

PAGE_W = 6.5           # inches, AMS full width
COL_W = 3.2            # inches, AMS single column

# ------------------------------------------------------------------ style
def use_style():
    mpl.rcParams.update({
        "font.family": "Arial",
        "font.size": 8,
        "axes.titlesize": 8,
        "axes.labelsize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "lines.linewidth": 0.8,
        "contour.linewidth": 0.5,
        "savefig.dpi": 300,
        "figure.dpi": 150,
        "mathtext.default": "regular",
        "mathtext.fontset": "custom",
        "mathtext.rm": "Arial",
        "mathtext.it": "Arial:italic",
        "mathtext.bf": "Arial:bold",
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })


# ------------------------------------------------------------------ data
_DS = None

def arco():
    """Open the public ARCO-ERA5 store (anonymous, 0.25°, hourly, 37 pressure levels)."""
    global _DS
    if _DS is None:
        _DS = xr.open_zarr(ARCO_URL, chunks=None, storage_options=dict(token="anon"))
    return _DS


def fetch(var: str, time: str, extent, level: int | None = None, pad: float = 6.0) -> xr.DataArray:
    """Fetch one ERA5 field over extent=(lon0, lon1, lat0, lat1) in degrees E (negative = W).

    The fetch box is padded by `pad` degrees so a Lambert map of `extent` is filled to its
    corners (no white wedges). Cached to cache/*.nc so re-runs are instant.
    """
    lon0, lon1, lat0, lat1 = extent
    lon0, lon1, lat0, lat1 = lon0 - pad, lon1 + pad, max(lat0 - pad, -90), min(lat1 + pad, 90)
    tag = f"{var}_{level if level is not None else 'sfc'}_{time.replace(':', '')}_{lon0}_{lon1}_{lat0}_{lat1}.nc"
    f = CACHE / tag
    if f.exists():
        return xr.open_dataarray(f).load()
    ds = arco()
    da = ds[var].sel(time=time)
    if level is not None:
        da = da.sel(level=level)
    da = da.sel(latitude=slice(lat1, lat0), longitude=slice(lon0 % 360, lon1 % 360)).load()
    da = da.assign_coords(longitude=(((da.longitude + 180) % 360) - 180))
    da.to_netcdf(f)
    return da


# ------------------------------------------------------------------ maps
def map_axes(fig, rect_or_spec, extent, central_lon=None):
    """Lambert conformal map axes with coastlines/states, no land fill."""
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    lon0, lon1, lat0, lat1 = extent
    clon = central_lon if central_lon is not None else 0.5 * (lon0 + lon1)
    proj = ccrs.LambertConformal(central_longitude=clon, central_latitude=0.5 * (lat0 + lat1),
                                 standard_parallels=(33, 45))
    ax = fig.add_subplot(rect_or_spec, projection=proj)
    ax.set_extent([lon0, lon1, lat0, lat1], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale("50m"), linewidth=0.5, edgecolor="k", zorder=5)
    ax.add_feature(cfeature.LAKES.with_scale("50m"), linewidth=0.4, edgecolor="k", facecolor="none", zorder=5)
    ax.add_feature(cfeature.BORDERS.with_scale("50m"), linewidth=0.4, edgecolor="0.3", zorder=5)
    ax.add_feature(cfeature.STATES.with_scale("50m"), linewidth=0.25, edgecolor="0.45", zorder=5)
    for sp in ax.spines.values():
        sp.set_linewidth(0.6)
        sp.set_edgecolor("k")
    return ax


def panel_label(ax, letter: str, text: str = ""):
    """Bold '(a)' plus a short field label, left-aligned above the panel."""
    ax.set_title(f"$\\bf{{({letter})}}$ {text}", loc="left", pad=3, fontsize=8)


def colorbar(fig, mappable, ax, label: str, ticks=None, extend="neither"):
    cb = fig.colorbar(mappable, ax=ax, orientation="horizontal", fraction=0.05, pad=0.04,
                      aspect=30, ticks=ticks, extend=extend)
    cb.set_label(label, fontsize=7.5, labelpad=2)
    cb.ax.tick_params(labelsize=7, width=0.5, length=2, direction="out")
    cb.outline.set_linewidth(0.5)
    return cb


def contour(ax, da, levels, transform=None, label=True, fmt="%d", colors="k", lw=0.5, **kw):
    import cartopy.crs as ccrs
    tr = transform or ccrs.PlateCarree()
    cs = ax.contour(da.longitude, da.latitude, da, levels=levels, colors=colors,
                    linewidths=lw, transform=tr, zorder=4, **kw)
    if label:
        ax.clabel(cs, fmt=fmt, fontsize=6, inline=True, inline_spacing=2)
    return cs


def shade(ax, da, levels, cmap, extend="both", transform=None):
    import cartopy.crs as ccrs
    tr = transform or ccrs.PlateCarree()
    return ax.contourf(da.longitude, da.latitude, da, levels=levels, cmap=cmap,
                       extend=extend, transform=tr, zorder=2)


def barbs(ax, u, v, skip=6, length=4.2, transform=None, kt=True):
    """Wind barbs in knots, thinned; black 0.4 pt."""
    import cartopy.crs as ccrs
    tr = transform or ccrs.PlateCarree()
    f = 1.94384 if kt else 1.0
    uu = u[::skip, ::skip] * f
    vv = v[::skip, ::skip] * f
    lon2, lat2 = np.meshgrid(uu.longitude, uu.latitude)
    return ax.barbs(lon2, lat2, uu.values, vv.values, length=length, linewidth=0.4,
                    color="k", transform=tr, zorder=6, regrid_shape=None)


def mark(ax, lon, lat, text, transform=None, **kw):
    """Plain black text marker, e.g. 'L' / 'H' at a centre."""
    import cartopy.crs as ccrs
    tr = transform or ccrs.PlateCarree()
    ax.text(lon, lat, text, transform=tr, ha="center", va="center", fontsize=kw.pop("fontsize", 9),
            fontweight=kw.pop("fontweight", "bold"), zorder=7, **kw)


def new_figure(ncols=3, height=2.6, width=PAGE_W):
    use_style()
    fig = plt.figure(figsize=(width, height))
    return fig


def save(fig, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.03, facecolor="white")
    plt.close(fig)
    return path
