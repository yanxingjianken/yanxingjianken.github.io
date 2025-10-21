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


```bash
module load apps/miniconda/3.6 
micromamba activate mpas_toolchain

## Setups
link to model: /net/flood/data2/users/x_yan/mpas_toolchain/mpas
different meshes (60-3km being x20): /net/flood/data2/users/x_yan/mpas_toolchain/meshes
convert to lat-lon toolbox: /net/flood/data2/users/x_yan/mpas_toolchain/convert_mpas
create init mesh: /net/flood/data2/users/x_yan/mpas_toolchain/MPAS-Tools/mesh_tools/grid_rotate
WPS_GEOG is at: /net/flood/data2/users/x_yan/WPS_ncar

```

We get the static Puerto Rico Mesh right
```bash
# 1) Copy and link
mkdir /net/flood/data2/users/x_yan/mpas_runs/240-48km_variable
cd /net/flood/data2/users/x_yan/mpas_runs/240-48km_variable
ln -s /net/flood/data2/users/x_yan/mpas_toolchain/meshes/x20.835586.grid.nc .
cp /net/flood/data2/users/x_yan/mpas_toolchain/MPAS-Tools/mesh_tools/grid_rotate/namelist.input .

# 2) Rewrite a minimal, clean namelist with a final newline + blank line
cat > namelist.input << 'EOF'
&input
  config_original_latitude_degrees  = 0.0
  config_original_longitude_degrees = 0.0
  config_new_latitude_degrees       = 18.25
  config_new_longitude_degrees      = -66.50
  config_birdseye_rotation_counter_clockwise_degrees = 0.0
/
 
EOF

# 3) Ensure Unix line endings (harmless if already OK)
dos2unix namelist.input 2>/dev/null || true

# 4) Verify that the last line is truly blank (there should be output here)
tail -n 2 -v namelist.input

# 5) Run the rotation
grid_rotate x20.835586.grid.nc PR.grid.nc
```
We should see /net/flood/data2/users/x_yan/mpas_runs/240-48km_variable/PR.grid.nc
<img width="1256" height="786" alt="569ed333871385abbc73cf47c1745ce8" src="https://github.com/user-attachments/assets/91457428-1157-42e9-8a0a-6f8ae8cf0fb3" />


Then we do [3.2 Static, terrestrial field processing](https://www2.mmm.ucar.edu/projects/mpas/tutorial/Boulder2019/index.html)
```bash
ln -s /net/flood/data2/users/x_yan/mpas_toolchain/mpas/init_atmosphere_model .
cp /net/flood/data2/users/x_yan/mpas_toolchain/mpas/namelist.init_atmosphere .
cp /net/flood/data2/users/x_yan/mpas_toolchain/mpas/streams.init_atmosphere .

## CHANGE the 2 files copied!
'''
In namelist.init_atmosphere, for nhyd_model - config_init_case
2 = ideal baroclinic wave
4 = ideal squall line
5 = ideal supercell
6 = ideal mountain wave
7 = real-data initialization
8 = surface update file creation (like sst_update=1 in WRF)
9 = lateral boundary conditions
'''

./init_atmosphere_model

```

Then we Interpolating real-data initial conditions as in section 3.4
```bash
ln -s /net/flood/data2/users/x_yan/mpas_toolchain/mpas_tutorial/met_data/GFS:2014-09-10_00 .

## CHANGE namelist.init_atmosphere
## CHANGE streams.init_atmosphere

./init_atmosphere_model

```
Then we Integrate as in section 3.5
```bash
ln -s /net/flood/data2/users/x_yan/mpas_toolchain/mpas/atmosphere_model . 
ln -s /net/flood/data2/users/x_yan/mpas_toolchain/mpas/src/core_atmosphere/physics/physics_wrf/files/* .

cp /net/flood/data2/users/x_yan/mpas_toolchain/mpas/namelist.atmosphere .
cp /net/flood/data2/users/x_yan/mpas_toolchain/mpas/streams.atmosphere .
cp /net/flood/data2/users/x_yan/mpas_toolchain/mpas/stream_list.atmosphere.* .

## CHANGE namelist.atmosphere -
## config_dt — the model timestep (delta-t) in seconds.
## config_len_disp — the length-scale for explicit horizontal diffusion, in meters.

ln -s /net/flood/data2/users/x_yan/mpas_toolchain/meshes/x20.835586.graph.info.part.64 .

mpiexec -n 4 ./atmosphere_model
```

Finally we visualize by convert to lat-lon grid - outputnamde latlon.nc

```bash

convert_mpas history.2014-09-15_00.00.00.nc

# or
/net/flood/data2/users/x_yan/mpas_toolchain/convert_mpas/convert_mpas history.2014-09-15_00.00.00.nc
```

Side stuff on HPC without setenv - use export
```bash
cp /net/flood/data2/users/x_yan/mpas_toolchain/mpas_tutorial/ncl_scripts/mesh_resolution.ncl .
export FNAME=/net/flood/data2/users/x_yan/mpas_runs/240-48km_variable/PR.grid.nc
ncl mesh_resolution.ncl
```








