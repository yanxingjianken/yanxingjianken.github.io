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

## TL;DR
[Slide Show here!](https://docs.google.com/presentation/d/195VkSwTUJrdwDYuSByEvev7b5TyzoMqF/edit?usp=sharing&ouid=116465514317596629476&rtpof=true&sd=true)

## Allocate Rescource
```bash
qsub -I -l select=1:ncpus=32:mem=128GB -q main -l walltime=8:00:00 -A <Project id>
```

## Run
On Derecho
```bash
kenyan@dec2435:~> module swap intel gcc/12.4.0

Due to MODULEPATH changes, the following have been reloaded:
  1) cray-mpich/8.1.29     2) hdf5/1.12.3     3) ncarcompilers/1.0.0     4) netcdf/4.9.2

kenyan@dec2435:~> module unload netcdf 


kenyan@dec2435:~> module load   hdf5-mpi/1.12.3 netcdf-mpi/4.9.3 parallel-netcdf/1.14.0 parallelio/2.6.6
kenyan@dec2435:~> module load cdo ncl ncview
kenyan@dec2435:~> module list

Currently Loaded Modules:
  1) ncarenv/24.12 (S)   3) gcc/12.4.0            5) libfabric/1.15.2.0   7) hdf5-mpi/1.12.3    9) parallel-netcdf/1.14.0  11) cdo/2.4.4  13) ncview/2.1.9
  2) craype/2.7.31       4) ncarcompilers/1.0.0   6) cray-mpich/8.1.29    8) netcdf-mpi/4.9.3  10) parallelio/2.6.6        12) ncl/6.6.2

  Where:
   S:  Module is Sticky, requires --force to unload or purge
```
On Dolma
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
/net/flood/data2/users/x_yan/mpas_toolchain/MPAS-Tools/mesh_tools/grid_rotate/grid_rotate x20.835586.grid.nc PR.grid.nc
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



&preproc_stages
    config_static_interp = true
    config_native_gwd_static = true
    config_vertical_grid = false
    config_met_interp = false
    config_input_sst = false
    config_frac_seaice = false
/



'''

./init_atmosphere_model

```

Then we Interpolating real-data initial conditions as in section 3.4
```bash
ln -s /net/flood/data2/users/x_yan/mpas_toolchain/mpas_tutorial/met_data/GFS:2014-09-10_00 .

## CHANGE namelist.init_atmosphere
## CHANGE streams.init_atmosphere

<immutable_stream name="input"
                  type="input"
                  filename_template="PR.static.nc"
                  input_interval="initial_only" />

<immutable_stream name="output"
                  type="output"
		  io_type="pnetcdf, cdsf5"
                  filename_template="PR.init.nc"
                  packages="initial_conds"
                  output_interval="initial_only" />

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

ln -s /net/flood/data2/users/x_yan/mpas_toolchain/meshes/x20.835586.graph.info.part.240 .

## if running in parallel, needs to match the grid decomposition file prefix
mpiexec -n 64 ./atmosphere_model
```

Finally we visualize by convert to lat-lon grid - outputnamde latlon.nc

```bash

convert_mpas history.2014-09-15_00.00.00.nc

convert_mpas PR.init.nc diag*nc

# or
/net/flood/data2/users/x_yan/mpas_toolchain/convert_mpas/convert_mpas history.2014-09-15_00.00.00.nc
```
---

### Prepare LENS2 to GFS-like IC inputs
Use [pywinter](https://pywinter.readthedocs.io/en/latest/#id6) and [cam-se-regrid](https://ncar.github.io/esds/posts/2023/cam-se-analysis/)

What we need:
<img width="719" height="369" alt="image" src="https://github.com/user-attachments/assets/a84586de-bd39-471b-8010-6473b66bb37c" />


TL; DR: We run 2 scripts: 
```bash
## On Derecho, run
/glade/u/home/kenyan/mpas_lens/process_ihesp_data.csh


# We should see in /glade/derecho/scratch/kenyan/iHESP_stage/2001-04-30_06Z/:
atmos_ta.nc     atmos_hus.nc   atmos_ua.nc   atmos_va.nc
atmos_z3.nc     atmos_ps.nc    atmos_base.nc
atmos_tos_1.nc  atmos_ts_1.nc  atmos_snw_1.nc atmos_ps2.nc
atmos_tsl_1.nc  atmos_mrlsl_1.nc
atmos_zsfc.nc -> (symlink to invariant)
atmos_lmask.nc -> (symlink to invariant)


## On Dolma, run with pangeos3_ken (needs > 200 GB memory)
/net/flood/data2/users/x_yan/mpas_lens/edit_nc_files.py

# Should see
/glade/derecho/scratch/kenyan/MPAS/intermediate/iHESP/mem2/2001/FILE:2001-04-30_06

# To Watch:
qstat -u $USER   

```
---
### Errors and Fixes

#### Thompson microphysics tables for clouds
```bash
subroutine thompson_init: failure opening MP_THOMPSON_QRacrQG.DBL

# 1) build the tables (writes MP_THOMPSON_* files in the CWD)
cd /net/flood/data2/users/x_yan/mpas_toolchain/mpas
./build_tables

# 2) put the generated tables in your run directory
cp MP_THOMPSON_*.DBL /net/flood/data2/users/x_yan/mpas_runs/mimic_mem2_May_2001/


```


---

### Side stuff on HPC without setenv - use export
```bash
cp /net/flood/data2/users/x_yan/mpas_toolchain/mpas_tutorial/ncl_scripts/mesh_resolution.ncl .
export FNAME=/net/flood/data2/users/x_yan/mpas_runs/240-48km_variable/PR.grid.nc
ncl mesh_resolution.ncl
```








