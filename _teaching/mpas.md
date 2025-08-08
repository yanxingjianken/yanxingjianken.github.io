---
title: "MPAS-A Notes"
collection: modeling
type: "Notes for Running MODEL FOR PREDICTION ACROSS SCALES - ATMOSPHERE"
permalink: /teaching/mpas
venue: "MIT EAPS"
date: 2025-08-08
location: "Cambridge, MA"
---

Notes for building everything MPAS from [this tutorial](https://www2.mmm.ucar.edu/projects/mpas/tutorial/Boulder2019/index.html).

### Dependency installation

1. load modules

module purge

module load apps/nvhpc/22.7

2. export

export MPI_ROOT="$NVHPC/Linux_x86_64/22.7/comm_libs/openmpi"

export PATH="$MPI_ROOT/bin:$PATH"

export LD_LIBRARY_PATH="$MPI_ROOT/lib:$LD_LIBRARY_PATH"

#### Sanity check: 
which nvfortran && which nvc && which mpicc && which mpif90


