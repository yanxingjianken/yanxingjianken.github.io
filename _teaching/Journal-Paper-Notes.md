---
title: "Journal Paper Reading Notes"
collection: teaching
type: "Literature Review"
permalink: /teaching/Journal_Paper_reading_notes
venue: "MIT EAPS"
date: 2026-06-01
location: "Cambridge, MA"
---

Reading notes and reproduction status for atmospheric blocking, Rossby wave
breaking (RWB), and related machine-learning methods. All code, simulations,
and notes live in the unified repository:

**[github.com/yanxingjianken/blocking_rwb_literature_review](https://github.com/yanxingjianken/blocking_rwb_literature_review)**

> **Status legend:** ✅ Reproduced &nbsp; 🔧 In Progress &nbsp; 📖 Literature Review (GIFs generated) &nbsp; 📋 Planned

---

## 1. Blocking Theories — 11 Canonical Mechanisms

Each subdirectory contains a Python spectral-model simulation with animated
GIFs. See the [blocking README](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/blocking)
for the inheritance diagram of the common barotropic solver.

| # | Experiment | Key Reference | Status |
|---|-----------|---------------|--------|
| 1 | [Energy Dispersion](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/blocking/1948_energy_dispersion) | Yeh (1949) — Rossby wave group velocity & energy trapping | 📖 |
| 2 | [Hydraulic Jump](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/blocking/1949_hydraulic_jump) | Rex (1950) — 1-D shallow-water hydraulic jump analogy | 📖 |
| 3 | [Multi-Equilibria (CdV)](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/blocking/1979_low_index_weather_regime) | Charney & DeVore (1979) — 3-mode ODE, S-curve bifurcation | 📖 |
| 4 | [Modon / Equivalent Barotropic](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/blocking/1979_modon) | McWilliams (1980), Haines & Marshall (1987) — Dipole vortex, resonant forcing in Dedalus | 🔧 |
| 5 | [Wave Resonance](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/blocking/1979_wave_resonance) | Tung & Lindzen (1979) — Stationary wave amplitude peaks near $\bar{U}_c = 15.8$ m/s | 📖 |
| 6 | [Eddy Straining](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/blocking/1983_eddy_straining_mechanism) | Shutts (1983), Wang & Kuang (2019) — Eddy straining dipole convergence | 📖 |
| 7 | [Deterministic Chaos](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/blocking/1984_deterministic_chaos) | Legras & Ghil (1985) — 25-mode strange attractor with blocking/zonal regimes | 📖 |
| 8 | [Wave Accumulation & AWB/CWB](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/blocking/1999_stationary_wave) | Swanson (2000, 2001) — Anticyclonic vs cyclonic wave breaking diagnosis | 📖 |
| 9 | [Selective Absorption](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/blocking/2012_selective_absorption_mechanism) | Yamazaki & Itoh (2013) — Same-sign eddies absorbed, opposite expelled | 📖 |
| 10 | [NLS Soliton / Envelope](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/blocking/2014_nonlinear_schrodinger) | Luo et al. (2014, 2019) — Blocking envelope as localized soliton | 📖 |
| 11 | [FAWA / Traffic Jam](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/blocking/2018_traffic_jam_theory) | Nakamura & Huang (2018) — Finite-amplitude wave activity "traffic jam" | 📖 |

> **Common library:** `blocking/common/` — pseudospectral barotropic solver (RK4) + GIF maker.

---

## 2. Rossby Wave Breaking (RWB) — Idealized Life-Cycle Experiments

Canonical baroclinic-wave experiments run with three different models
(MPAS-Atmosphere, SpeedyWeather.jl, Dedalus).

| Experiment | Engine | Reference | Status |
|-----------|--------|-----------|--------|
| [Jablonowski & Williamson Dycore Test](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/rwb/Jablonowski_and_Williamson_Baroclinic_Wave_MPAS) | MPAS-A (x1.40962, ~240 km) | JW2006, *QJRMS* **132**, 2943–2975 | ✅ |
| [Thorncroft LC1 / LC2](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/rwb/thorncroft93_baroclinic) | SpeedyWeather.jl (T42, 15σ) | Thorncroft et al. 1993, *QJRMS* **119**, 17–55 | 🔧 |
| [Polvani & Plumb Stratospheric RWB](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/rwb/polvani_plumb92) | Dedalus | Polvani & Plumb (1992) | 📋 |
| [Vallis Barotropic Decay](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/rwb/vallis04_barotropic) | SpeedyWeather.jl (barotropic) | Vallis (2004) | 📋 |
| [Schemm COSMO Diagnostics](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/rwb/schemm13_cosmo) | COSMO-LM archive | Schemm et al. (2013) | 📋 |

### JW06 — What's reproduced ✅

16-day hydrostatic baroclinic wave on the x1.40962 Voronoi mesh (64 ranks, no
physics). Validated against the published reference: 850 hPa temperature at
day 9 (cold/warm fronts), 250 hPa zonal wind (jet streak), surface pressure
minimum evolution, Ertel PV on isentropic surfaces. Lat-lon regridding via
`convert_mpas` barycentric interpolation.

### Thorncroft LC1 / LC2 — In progress 🔧

LC1 (anticyclonic, equatorward wave breaking) and LC2 (cyclonic, poleward
wave breaking) life cycles in SpeedyWeather.jl. LC1 uses J&W basic state with
∇⁶ hyperdiffusion; LC2 adds a barotropic cyclonic perturbation. Diagnostics
in development: EKE(t), PV on θ surfaces, EP-flux cross-sections.

---

## 3. SFNO — Spectral Fourier Neural Operator

| Item | Details |
|------|---------|
| **Paper** | [Spectral Fourier Neural Operator](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/sfno) — arXiv: 2306.03838 |
| **Status** | 🔧 Training infrastructure ready (PyTorch + `torch-harmonics`) |
| **Contents** | Checkpoints, literature PDF, training scripts for SFNO weather prediction |

Spherical-harmonic neural operator that leverages the convolution theorem on
the sphere to achieve equivariance without explicit spherical-harmonic
transforms in every layer.

---

## 4. Spherical Attention — Equivariant Transformers on S²

| Item | Details |
|------|---------|
| **Paper** | [Attention on the Sphere](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/spherical_attention) — Bonev, Rietmann, Paris, Carpentieri, Kurth (NVIDIA, 2024; arXiv: 2505.11157) |
| **Status** | 🔧 Training ready |
| **Key Result** | Quadrature-weighted geodesic attention **reduces pole errors** vs Euclidean attention on lat-lon grids |
| **Experiments** | (i) Shallow-water 6-h forecast; (ii) ERA5 Z500 6-h real-data forecast, 128×256 Gaussian grid |
| **Contents** | S² vs R² Transformer implementations, checkpoints, MP4 animations, training data |

---

## 5. Hilbert Transform — ERA5 Scale Decomposition & Analytic Signals

| Item | Details |
|------|---------|
| **Paper** | [The Analytic Signal and Hilbert Transform](https://github.com/yanxingjianken/blocking_rwb_literature_review/tree/main/hilbert_transform) — Huang et al. (1998) |
| **Status** | ✅ Complete (all 15 phases of `plan.md`) |
| **Data** | ERA5 Z500, Oct–Nov 2012, 61 days, 1464 hourly snapshots |
| **Pipeline** | Zonal wavenumber + temporal frequency filtering → 9 bands (3 spatial × 3 temporal) → Hilbert analytic signal → complex PCA |
| **Outputs** | 3.3 GB NetCDF, 9 PNG snapshots, 5.6 MB MP4 (9-panel animation) |
| **Contents** | Download scripts, main pipeline, extended animation stitcher, literature PDFs |

---

## Related Repositories

- [PV_Ertel_Computation](https://github.com/yanxingjianken/PV_Ertel_Computation) — Ertel PV on sigma levels (ERA5-validated)
- [PV_Inversion](https://github.com/yanxingjianken/PV_Inversion) — Piecewise PV inversion (Wu SOR + SH spectral dual-track)




