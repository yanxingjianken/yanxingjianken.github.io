---
title: "Ertel PV Computation on Sigma Levels"
collection: teaching
type: "Climate Dynamics"
permalink: /teaching/ertel-pv-computation
venue: "MIT EAPS"
date: 2026-06-01
location: "Cambridge, MA"
---

How to correctly compute **Ertel Potential Vorticity (PV)** for CMIP-class models
that do **not** provide PV as a native output (unlike ERA5 or MPAS-Atmosphere).

**Source repository:** [github.com/yanxingjianken/PV_Ertel_Computation](https://github.com/yanxingjianken/PV_Ertel_Computation)

---

## Motivation

ERA5 and MPAS output Ertel PV directly on model/pressure levels, but most CMIP
models (CESM2, IPSL, MIROC, etc.) do not. Computing PV from the standard 3-D
output $(u, v, T, p_s)$ seems straightforward, but the naive pressure-level
finite-difference approach gives **severely degraded PV near the surface** and
near steep topography.

**The fix:** compute PV on terrain-following $\sigma = p/p_s$ coordinates, where
the lower boundary is a material surface and vertical derivatives are naturally
aligned with the flow.

## Formula

$$\text{PV}_\sigma = -\frac{g}{p_s}\left[ \frac{\partial v}{\partial\sigma}\frac{\partial\theta}{\partial x} - \frac{\partial u}{\partial\sigma}\frac{\partial\theta}{\partial y} + (f + \zeta)\frac{\partial\theta}{\partial\sigma} \right] \times 10^6 \ \text{PVU}$$

where:

- $\sigma = p/p_s(x,y)$ — terrain-following vertical coordinate
- $\theta = T\,(p_0/p)^{R_d/c_p}$ — potential temperature ($p_0 = 1000$ hPa)
- $\zeta$ — relative vorticity via spherical-harmonic operators
- $f = 2\Omega\sin\phi$ — Coriolis parameter
- Horizontal derivatives: spectral (spherical harmonics) — no polar singularity
- Vertical derivatives: MPAS-style centred interior, one-sided boundaries

## ERA5 Validation

We validate against ERA5's native isobaric PV output. The sigma method
**dramatically improves** near-surface PV:

| $\sigma$ level | Nominal hPa | RMSE (PVU) | Correlation |
|:---:|:---:|:---:|:---:|
| 0.850 | 861 | 0.30 | 0.92 |
| 0.500 | 507 | 0.37 | 0.94 |
| 0.250 | 253 | 1.12 | 0.97 |

> **Key result:** 850 hPa correlation improves from **0.28** (isobaric
> finite-difference) to **0.92** (sigma coordinate).

![ERA5 PV Sigma Comparison](/images/era5_pv_sigma_comparison.png)

*Figure: Sigma-coordinate PV (left) vs ERA5 native PV (center) and their
difference (right) at three representative levels. The sigma method captures
the near-surface PV structure that isobaric finite-differences miss.*

## Usage

### Quick start (ERA5)

```bash
cd era_sanity_check
micromamba run -n blocking python validate_era5.py
```

### Quick start (CESM2-LENS2)

```bash
cd cesm2_compute
micromamba run -n blocking python compute_cesm2_pv.py
```

### Python API

```python
from src.ertel_pv import ertel_pv_sigma, DEFAULT_SIGMA_LEVELS

# sigma PV on 11 levels (primary)
pv_sigma, p_3d = ertel_pv_sigma(u, v, t, plev_Pa, ps, lat, lon)
# pv_sigma: (11, nlat, nlon) in PVU
```

## Required Input Variables

| Variable | ERA5 name | CESM2 name | Units |
|----------|-----------|------------|-------|
| Eastward wind | `u` | `U` | m s⁻¹ |
| Northward wind | `v` | `V` | m s⁻¹ |
| Temperature | `t` | `T` | K |
| Surface pressure | `sp` | `PS` | Pa |
| Pressure levels | (coordinate) | `lev` | Pa or hPa |
| Latitude | `latitude` | `lat` | °N |
| Longitude | `longitude` | `lon` | °E |

## References

- Source code & documentation: [github.com/yanxingjianken/PV_Ertel_Computation](https://github.com/yanxingjianken/PV_Ertel_Computation)
- Uses `pvtend.sh_ops` for spherical-harmonic gradients
- Linear vertical interpolation: NCL `int2p_n` → scipy/numpy port
