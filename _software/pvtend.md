---
title: "PV Tendency Decomposition"
excerpt: "Orthogonal four-basis decomposition tools for PV tendency analysis."
collection: software
---

## What is `pvtend`?

[`pvtend`](https://github.com/yanxingjianken/pvtend) is a Python package for **potential vorticity (PV) tendency decomposition**, designed for analysing the lifecycle of atmospheric blocking and precursor reverse-flow (PRP) events. It works with ERA5 pressure-level data and decomposes PV tendencies into physically meaningful components using an orthogonal basis framework.

**Full documentation:** [pvtend.readthedocs.io](https://pvtend.readthedocs.io/en/latest/)

**Source code:** [github.com/yanxingjianken/pvtend](https://github.com/yanxingjianken/pvtend)

**License:** MIT

---

## Key Features

| Feature | Description |
|---|---|
| **PV tendency computation** | Advection, stretching, diabatic, and residual terms |
| **QG omega solver** | Hoskins Q-vector formulation with FFT + Thomas algorithm |
| **Helmholtz decomposition** | 4 backends (direct, FFT, DCT, SOR) for limited-area domains |
| **Moist/dry ω splitting** | Decomposes vertical motion into moist and dry contributions |
| **Orthogonal basis decomposition** | Projects PV tendency onto intensification (β), propagation (αx, αy), and deformation (γ) modes |
| **RWB detection** | Anticyclonic/cyclonic Rossby wave breaking classification |
| **Composite lifecycle** | Multi-stage ensemble averaging with onset/peak/decay staging |
| **CLI pipeline** | End-to-end processing via `pvtend-pipeline` command |

---

## Installation

```bash
# Clone and install from source
git clone https://github.com/yanxingjianken/pvtend.git
cd pvtend
pip install -e ".[dev]"
```

Or with **micromamba**:

```bash
micromamba create -f environment.yml
micromamba activate pvtend_env
pip install -e ".[dev]"
```

---

## Quick Start

### Python API

```python
import pvtend
import numpy as np

# Compute a zonal derivative
dfdx = pvtend.ddx(field, dlon_rad=np.deg2rad(0.5),
                   lat_1d=np.linspace(30, 50, 21))

# Orthogonal basis decomposition
from pvtend.decomposition import compute_orthogonal_basis, project_field

basis = compute_orthogonal_basis(q_prime, q_full, x_rel, y_rel, dx, dy)
result = project_field(tendency, basis, dx, dy)

print(f"β = {result['beta']:.3e}")   # intensification rate
print(f"αx = {result['alpha_x']:.3e}")  # zonal propagation
print(f"αy = {result['alpha_y']:.3e}")  # meridional propagation
print(f"γ = {result['gamma']:.3e}")   # deformation
```

### CLI Pipeline

```bash
# Step 1 – Compute PV tendencies for blocking events
pvtend-pipeline compute \
    --event-type blocking \
    --events-csv events.csv \
    --era5-dir /data/era5/ \
    --clim-dir /data/climatology/ \
    --out-dir /data/output/ \
    --skip-existing

# Step 2 – Build composite lifecycle
pvtend-pipeline composite \
    --npz-dir /data/output/ \
    --pkl-out composite.pkl
```

---

## How It Works

The package follows a modular pipeline:

1. **Preprocessing** — Load and regrid ERA5 monthly NetCDF onto a Northern Hemisphere grid.
2. **Climatology** — Compute Fourier-filtered monthly climatology.
3. **Tendency computation** — Decompose PV tendencies into advection, stretching, diabatic, and residual terms.
4. **QG ω & Helmholtz decomposition** — Solve the quasi-geostrophic omega equation and decompose the flow.
5. **Moist/dry splitting** — Separate vertical motion into moist and dry contributions.
6. **Compositing** — Build ensemble-mean lifecycle composites across events.
7. **Orthogonal basis projection** — Project tendencies onto the four basis modes: **β** (intensification), **αx / αy** (propagation), and **γ** (deformation).
8. **Visualization** — Generate publication-ready figures.

---

## Links

- [Full Documentation (Read the Docs)](https://pvtend.readthedocs.io/en/latest/)
- [GitHub Repository](https://github.com/yanxingjianken/pvtend)
- [Issue Tracker](https://github.com/yanxingjianken/pvtend/issues)
