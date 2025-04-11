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

Partial results are used in my final project for 12.810 Atm. Dynm. (taught by [Paul O'Gorman](https://pog.mit.edu/))

# Are AI Weather Forecasts Respecting Atmosphere Dynamics?

[Presentation slides and write-ups will be avialable in 2025 summer]

**As of April 10th, 2025**

For non-commerical usage of ECMWF open accounts, the service/MARS will not be available, which means the **most recent 30 day reanalysis** will not be available, and the configuration of "/.ecmwfapirc" file would lead to errors of not being authorized. Issues have been encountered in [post](https://github.com/google/weather-tools/issues/35) and [issue](https://github.com/ecmwf-lab/ai-models-fourcastnetv2/issues/1)...

Instead, the resolution is to use *copernicus CDS* open access data, which requires a "/.cdsapirc" file that you can find api instructions [here](https://cds.climate.copernicus.eu/how-to-api).

---

## Tutorials on running your own ai weather forecasts! 

### HPC setup and conda env demonstration for MIT Dolma Cluster
1. Read ECMWF [ai-models documentation](https://github.com/ecmwf-lab/ai-models)
2. module load apps/miniconda/3.6
3. conda create -n fourcastnetv2 -c conda-forge python=3.10 -y
4. source activate fourcastnetv2
5. pip install ai-models ai-models-fourcastnetv2
6. Dir of model weights and climatology files will be made automactially to: /home/x_yan/fourcastnetv2-small
7. Config api - two options: (a. Commercial or ECMWF authorized MARS access), or (b. Open research CDS access)
8. (Option a. MARS) Follow [link](https://confluence.ecmwf.int/display/WEBAPI/Access+MARS) to get MARS access
9. Make file .ecmwfapirc, add {"url"   : "https://api.ecmwf.int/v1", \n "key"   : "xxxxxxxxxxxxxxxxxxx", \n "email" : "xxxxxxxxx"}
10. (Option b. CDS) Follow [link](https://cds.climate.copernicus.eu/how-to-api) to get CDS access
11. Make file .cdsapirc, url: https://cds.climate.copernicus.eu/api \n key: xxxx-xxxx-xxxx-xxxx
12. Download data by running: ai-models --download-assets fourcastnetv2-small
11. Files of weights.tar, global_means.npy, and global_stds.npy should be seen in path /home/x_yan/fourcastnetv2-small/
12. (fourcastnetv2) x_yan@dolma:~$ cd fourcastnetv2-small/
13. When using CDS option, modify when using PyTorch > 2.6: (i)cd to your model.py path: cd /home/x_yan/.conda/envs/fourcastnetv2/lib/python3.10/site-packages/ai_models_fourcastnetv2/, (ii) open model.py, (iii) change line 146 checkpoint = torch.load(checkpoint_file, map_location=self.device) into checkpoint = torch.load(checkpoint_file, map_location=self.device, weights_only=False)
14. (fourcastnetv2) x_yan@dolma:~/fourcastnetv2-small$ ai-models --input cds --date 20230110 --time 0000 fourcastnetv2-small
15. *Optional* Other params could be --date 2023-10-01 \ --time 00:00 \ --lead-time 24h \ --path /net/flood/data/users/x_yan/fourcastnetv2 \ --assets-sub-directory \ --input cds \ --output file
16. Output forecast file would be in the same folder named fourcastnetv2-small.grib
17. Enjoy! ![image](https://github.com/user-attachments/assets/05f03439-124c-404b-9741-80e426c7edc7)

### Interpret Results
1. Load the jupyter notebook from [link](https://colab.research.google.com/drive/1ieWTYO1lcaMRNH4CulRoQWXlF3o5gdAM?usp=sharing).
2. The forecast grib file is divided into surface and pressure-level data
3. Sample intial data loks look ![image](https://github.com/user-attachments/assets/053e390c-ae0b-4368-9501-a0dee4940000)

4. Sample forcasts look like ![image](https://github.com/user-attachments/assets/569621bd-0ca4-4a6b-9178-174616987539)






