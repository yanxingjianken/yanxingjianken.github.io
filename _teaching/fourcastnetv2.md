---
title: "Run Your Own AI Weather Model"
collection: notes
type: "misc."
permalink: /teaching/fourcastnetv2
venue: "misc."
date: 2025-04-10
location: "Cambridge, MA"
---

This is a quick intro on how to use run the fourcastnetv2 ai model from ecmwf [instructions](https://github.com/ecmwf-lab/ai-models-fourcastnetv2).

Partial results are used in 12.810 Atm. Dynm. taught by Paul for my final project - Are AI Weather Forecasts Respecting Atmosphere Dynamics?
---

## Install packages and set up the conda env (MIT Dolma Cluster)
1. module load apps/miniconda/3.6
2. conda create -n fourcastnetv2 -c conda-forge python=3.10 -y
3. source activate fourcastnetv2
4. pip install ai-models ai-models-fourcastnetv2
5. Make dir of where you want to store the weights and climatology files: mkdir -p /net/flood/data/users/x_yan/fourcastnetv2/assets
6. Follow [link](https://confluence.ecmwf.int/display/WEBAPI/Access+MARS) to get MARS access
7. Download data by running: ai-models --download-assets fourcastnetv2-small \
  --path /net/flood/data/users/x_yan/fourcastnetv2 \
  --assets-sub-directory
8. Make file .ecmwfapirc, add {
    "url"   : "https://api.ecmwf.int/v1",
    "key"   : "xxxxxxxxxxxxxxxxxxx",
    "email" : "xxxxxxxxx"
}
9. /net/flood/data/users/x_yan/fourcastnetv2/
├── assets/
│   ├── weights.tar
│   ├── global_means.npy
│   └── global_stds.npy
└── fourcastnetv2-small.grib     # Output forecast file
10. Turns out not to be free! See [post](https://github.com/google/weather-tools/issues/35).. Yikes!
11. call command: ai-models fourcastnetv2-small \
  --date 2023-10-01 \
  --time 00:00 \
  --lead-time 24h \
  --path /net/flood/data/users/x_yan/fourcastnetv2 \
  --assets-sub-directory \
  --input cds \
  --output file


