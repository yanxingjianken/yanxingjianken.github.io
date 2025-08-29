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

source activate mpas_toolchain

cd /net/flood/data2/users/x_yan/mpas/MPAS-Model

1) Always remember to download [input grids and files](https://www2.mmm.ucar.edu/projects/mpas/site/downloads.html)

Get the right mpas_static dir:
<img width="1140" height="369" alt="image" src="https://github.com/user-attachments/assets/88c79783-98f3-4399-b74f-71149ac8247a" />

2) make -j4 gfortran CORE=init_atmosphere PRECISION=single AUTOCLEAN=true

1-1) Always set autoclean! # Good minimal incantation (equivalent to what worked)
make -j$(nproc) gfortran CORE=init_atmosphere AUTOCLEAN=true \
  FC=mpif90 CC=mpicc CXX=mpicxx \
  FFLAGS="-O3 -ffree-line-length-none -fconvert=big-endian -ffree-form -mcmodel=large" \
  CFLAGS="-O3 -mcmodel=large" \
  CXXFLAGS="-O3 -mcmodel=large" \
  LDFLAGS="-O3 -mcmodel=large"

2) make clean CORE=atmosphere
   
3) make -j4 gfortran CORE=atmosphere PRECISION=single

3-1) make -j$(nproc) gfortran CORE=atmosphere PRECISION=single \
  FC=mpif90 CC=mpicc CXX=mpicxx \
  FFLAGS="-O3 -ffree-line-length-none -fconvert=big-endian -ffree-form -mcmodel=large" \
  CFLAGS="-O3 -mcmodel=large" \
  CXXFLAGS="-O3 -mcmodel=large" \
  LDFLAGS="-O3 -mcmodel=large"

4) ./init_atmosphere_model

Takes a while!
<img width="2190" height="1168" alt="image" src="https://github.com/user-attachments/assets/5048d8d5-6e10-4c57-8c9d-9522b9ba2e92" />


5) mpiexec -n 32 ./atmosphere_model
6) ncl supercell.ncl

---

### Visualize

1. cp /net/flood/data2/users/x_yan/mpas/mpas_tutorial_anamitra/ncl_scripts/plot_terrain.ncl .
2. setenv FNAME x1.10242.static.nc
3. ncl plot_terrain.ncl

---
### Some One-Click Checks for Debuggings

1) Sanity env (same as before)
./smoke.sh [download here](https://colab.research.google.com/drive/14iSte7UEvKfrQqAuW10ky1kI8TcXRsFH?usp=sharing)

2) Run
mpirun -n 1 ./init_atmosphere_model |& tee run.log

3) Quick skim for issues
grep -E "Bootstrapping|filename template|CFSR|CRITICAL|ERROR" log.init_atmosphere.0000.out

4) Original Settings to namelist.init_atmosphere

<img width="457" height="255" alt="image" src="https://github.com/user-attachments/assets/e96adb81-c8c1-4b98-a57f-401fc8c41f3e" />
<img width="733" height="361" alt="image" src="https://github.com/user-attachments/assets/6f70e25b-ae23-41a6-b4f4-2d1574a8c214" />





