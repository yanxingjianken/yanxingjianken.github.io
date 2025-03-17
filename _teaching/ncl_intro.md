---
title: "Intro to NCL (on HPC and PC)"
collection: notes
type: "misc."
permalink: /teaching/into2ncl
venue: "misc."
date: 2025-03-16
location: "Cambridge, MA"
---

This is a quick intro on how to use NCL to process raw grib files downloaded from ECMWF using MARS api requests.

An IMPORTANT reminder is that the official ECMWF python script for converting from model level hybrid scales to height / pressure levels 
has significant errors and runs very slowly. See the forum [link](https://forum.ecmwf.int/t/bugs-in-era5-complete-reanalysis-cds-conversion-python-scripts/10696) for details.

Instead, the [CDO command line interface](http://www.idris.fr/media/ada/cdo.pdf) of the ml2pl and ml2hl functions would come to rescue!

## Install NCl and CDO in the conda env
1. For Windows users, install Ubuntu from the microsoft store, then proceed to step 2.
2. For Linux users, module load your conda setup via module load anaconda, or, for MIT Engaging users, use: module load miniforge/24.3.0-0.
3. Create a conda env with specifying the desired installed package: conda create -n ncl_stable -c conda-forge ncl
4. Then conda install cdo
5. If the above is not working, try following the conda forge commannds in [this link](https://bairdlangenbrunner.github.io/python-for-climate-scientists/conda/setting-up-conda-environments.html) or the [offical tutorial](https://www.ncl.ucar.edu/Download/conda.shtml)
6. The conda forge for cdo may not be working, so you can try [the Max-Plack Institut link](https://code.mpimet.mpg.de/projects/cdo/wiki/Anaconda) here, if your HPC supports docker...


## Convert from hybrid model levels (1-137) to pressure levels
1. cd to your desired path where input and output files are (will be) located.
2. cdo ml2pl,90000,85000,80000,75000,70000,65000,60000,55000,50000,45000,40000,35000,30000,25000,20000,15000,10000 1998_pt_lapse.grib 1998_pt_lapse_pl.grib

Something to notice is that ml2pl function may not work well on date ranges containing more than 2 time stamps, so it would be better to [download the raw data **in daily segment**](https://colab.research.google.com/drive/1ugiWBGnX5VypfHle1PuOJgWs9PHV2Ood?usp=sharing), and then use [a batch process scirpt](https://colab.research.google.com/drive/12CvdhawhnsKMBHQBNRZ-x2tjl0N5vALI?usp=sharing) to convert.
1. download raw data and load the above sh script
2. chmod +x convert_grib_files.sh
3. dos2unix convert_grib_files.sh
4. ./convert_grib_files.sh
5. you should see something like ![image](https://github.com/user-attachments/assets/03eef26e-add5-4ae1-874b-7d37fe0cd45e)


## Convert from spherical harmonics coord to gridded resolution
1. Convert from "reduced Gaussian" to "regular Gaussian": 
cdo setgridtype,regular T639_19980915_19980930_330isentropic_pv.grib T639_19980915_19980930_330isentropic_pv_gauss.grib
2. cdo invertlat in out: cdo -f nc -sp2gpl /mnt/c/Users/yanxi/Downloads/T639_19980915_19980930_330isentropic_uvvo.grib /mnt/c/Users/yanxi/Downloads/T639_19980915_19980930_330isentropic_uvvo_gauss.nc
3. cdo merge T639_19980915_19980930_330isentropic_pv.nc T639
_19980915_19980930_330isentropic_uvvo_gauss.nc T639_19980915_19980930_330isentropic_concat.nc

## Spatial Derivatives
Please email Ken for code.

## Mean-Perturbation Decompositions
Please email Ken for code.


