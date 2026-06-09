---
title: "HPC netCDF Parallelization"
excerpt: "Portable, environment-aware netCDF/HDF5 I/O + parallel-compute optimization for large gridded climate data on any HPC."
collection: software
---

## What is `hpc-netcdf-parallelization`?

[`hpc-netcdf-parallelization`](https://github.com/yanxingjianken/hpc-netcdf-parallelization) is a **Claude Code skill** that makes large gridded (climate / meteorological) array computes **fast and portable on any HPC**, by fixing the two things that actually slow them down: **I/O** (chunking + read patterns) and **parallelism** (worker sizing + load balance). It **detects** the cluster's available backends and hardware, then recommends and applies the right strategy — so the same workflow runs on an NFS workstation, a NUMA fat-node, or a Lustre/MPI cluster.

**Source code:** [github.com/yanxingjianken/hpc-netcdf-parallelization](https://github.com/yanxingjianken/hpc-netcdf-parallelization)

**License:** MIT

> **The core lesson it encodes:** a "slow parallel compute" is usually **slow serial I/O** (redundant decompression), not slow math — so *profile I/O before blaming compute or adding cores*. In the CESM2-LENS2 blocking pipeline that motivated it, a 3.5-hour "compute" was 99 % netCDF decompression; switching a scattered read to a contiguous-slab read was **77× faster**, and adding cores would have made it *worse*.

---

## Install (Claude Code, v3.7.0+)

```text
/plugin marketplace add yanxingjianken/hpc-netcdf-parallelization
/plugin install hpc-netcdf-parallelization
```

Then run `/hpc-detect` on your cluster, or just describe a slow netCDF / parallel job and the skill activates.

---

## Key Features

| Feature | Description |
|---|---|
| **Environment detection** | Probes netCDF4 / HDF5 / zarr / NCZarr / PnetCDF, MPI + parallel-HDF5, filesystem (NFS/Lustre/GPFS), cores / NUMA / RAM → a JSON recommendation |
| **Backend choice** | Decision table for netCDF4 vs zarr (v3 sharded on NFS) vs NCZarr vs PnetCDF — picks what's actually available |
| **I/O fixes** | Contiguous-slab reads (vs scattered `isel(time=[…])`), access-pattern chunking on write, data-preserving rechunking of existing files |
| **Parallel compute** | Load-balanced `pmap` (process / Dask), combinable per-pixel `(sum, valid-count)` means, BLAS pinning, NUMA pinning |
| **Worker sizing** | Sizes workers to the **memory-bandwidth knee**, not the core count (spectral/decompression plateau early) |
| **Multi-node** | Dask-distributed path (no MPI rebuild) for >1 node; MPI/PnetCDF when the stack supports it |
| **CLI + JSON tools** | `detect_env`, `read_slab`, `rechunk`, `parallel_map` — all emit JSON, MCP / agent-friendly |
| **Commands** | `/hpc-detect`, `/hpc-rechunk`, `/hpc-parallelize` |

---

## Bundled Tools

| Tool | Purpose |
|---|---|
| `detect_env.py` | Environment + backend detection → JSON recommendation (`--human` for a table) |
| `read_slab.py` | Contiguous-slab reader + `bench` (scattered vs slab on *your* file) |
| `rechunk.py` | Data-preserving rechunk to the access pattern (`nccopy` / xarray, `--verify`) |
| `parallel_map.py` | Load-balanced `pmap` + combinable-mean `add_accumulators`, BLAS-pinned |

---

## Quick Start

```bash
# Detect the cluster and get a recommendation
python scripts/detect_env.py --human

# Prove the read bottleneck on your own file (scattered vs contiguous slab)
python scripts/read_slab.py bench myfile.nc --vars t u v --n 30

# Rechunk an existing file data-preserving (byte-identical values)
python scripts/rechunk.py in.nc out.nc --chunks "time/1,lev/9,lat/192,lon/288" --verify
```

```python
from parallel_map import pmap, add_accumulators
import functools, numpy as np

parts = pmap(process_event, events, n_workers=96)          # fine-grained, BLAS-pinned
total = functools.reduce(add_accumulators, parts)           # (sum, count) merge
mean  = {v: np.where(c > 0, s / c, np.nan) for v, (s, c) in total.items()}
```

---

## Golden Rules

1. **Profile I/O before blaming compute.**
2. **Contiguous slabs in, access-pattern chunks out.**
3. **More cores ≠ faster** for memory-bandwidth-bound work — size to the bandwidth knee.
4. **Detect the cluster; don't assume** — backends, filesystem, and MPI differ everywhere.

---

## Links

- [GitHub Repository](https://github.com/yanxingjianken/hpc-netcdf-parallelization)
- [Issue Tracker](https://github.com/yanxingjianken/hpc-netcdf-parallelization/issues)
