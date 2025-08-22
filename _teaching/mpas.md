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

### Start:
0) Activate env & go to your run dir
conda activate mpas_toolchain
cd /net/flood/data2/users/x_yan/mpas/MPAS-Model

1) Sanity env (same as before)
./smoke.sh 

4) Run
mpirun -n 1 ./init_atmosphere_model |& tee run.log

5) Quick skim for issues
grep -E "Bootstrapping|filename template|CFSR|CRITICAL|ERROR" log.init_atmosphere.0000.out



