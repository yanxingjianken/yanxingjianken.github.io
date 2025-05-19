---
title: "Using Tempest Extreme to track (Anti)Cyclones anywhere on any level surfaces!"
collection: misc.
type: "2025 Princeton GFDL Hackathon"
permalink: /teaching/tempest_extreme
venue: "Princeton GFDL"
date: 2025-05-14
location: "Princeton, NJ"
---

Some takeways from the 2025 Princeton GFDL Hackathon, esp. on tempest extreme, a tracking algo.

---

The amazing group of hk25-blocking worked jointly on identifying blocking (persistent mid/high latitude anticyclones) and (extra)tropical cyclones. 
Members include [Dr. Gan Zhang](https://climas.illinois.edu/directory/profile/gzhang13) from UIUC, [Dr. Mingyu Park](https://mingyupark.scholar.princeton.edu/) from Princeton, [Yanjun Hu](https://scholar.google.com/citations?user=YIl2UewAAAAJ&hl=zh-CN) from Purdue, [Coleman Gliddon](https://cjgliddon.github.io/) from MIT, and me.

A tool to track any features that depart from neighboring points (say, cyclones on surface pressure, or anticyclones on z500 isobaric level, etc.) could be using
this tool of [Tempest Extreme](https://gmd.copernicus.org/articles/14/5023/2021/), results can be downloaded from here:

1. xsh24 surface cyclone tracking (200 Pa increase outward within 6 degs) [raw csv link](https://drive.google.com/file/d/1w9IJb7SIOEB--zS1Wm0p1NHC-B4rdBII/view?usp=sharing), [reformatted csv link]()
2. xsh24 z500 anticyclone tracking (10 m z500 decrease outward within 6 degs)[raw csv link](), [reformatted csv link]()
3. ERA5 z500 anticyclone tracking (1990-2020) (10 m z500 decrease outward within 6 degs) [link](https://drive.google.com/file/d/1xRmgEvVNLUCzKgLYXIICqBztefmYb6gs/view?usp=sharing)

...and here's a quick tutorial on how to use:

(Note: Performance comparison assessments of results compared to blocking tracking algo [ConTrack](https://github.com/steidani/ConTrack) is also done by Mingyu.)

The following tutorial uses stellar-amd node of GFDL and runs on the X-Shield 2024 data that is not published yet.

1. Go get env yml file "environment_coleman.yml" located [in this repo](https://github.com/cjgliddon/hackathon25_blocking/tree/main/tempest_extreme)
2. module load anaconda3/2024.10 and install the yml file to get conda env tempest_extreme: conda env create --name tempest_extreme --file=environment_coleman.yml
3. (2025-05-19 Update) the latest .yml with nco and cdo installed could be found [here](https://github.com/cjgliddon/hackathon25_blocking/blob/main/tempest_extreme/tempest_env.yml).
4. conda install -c conda-forge nco (also register as ipykernel, optional)
5. Also conda install cdo for ERA5 geopotential height tracking
6. Go to /scratch/cimes/xy4043/tutorial and get all .sh files (or visit the hackathon blocking group [repo](https://github.com/cjgliddon/hackathon25_blocking))
7. chmod +x stitch_nodes_3hrly_anticyclone.sh (and all other 3 sh files)
8. run  ./detect_node_anticyclone.sh 
9. run  ./stitch_nodes_3hrly_anticyclone.sh
10. The results (raw, and reformatted csv) are in /scratch/cimes/xy4043/tracks/

![image](https://github.com/user-attachments/assets/97be3fbd-cde0-43d9-9fca-e280d686d4f0)

If we impose certain spatialtemporal constraints, we can filter out persistent blocking events:
![image](https://github.com/user-attachments/assets/78eb1eff-8a05-452c-96ce-d7e48821e974)


The xsh24 model also has several temperature tendecy terms, and here's a quick note:
1. shallow convection is called 'tendency_of_air_temperature_due_to_shallow_convection_coarse_C3072_1440x720'
2. deep convection is called 't_dt_gfdlmp_coarse_C3072_1440x720', mp = micro-physics
3. temperature tendecy 't_dt_phys_coarse_C3072_1440x720' includes both radiation and shallow convection
4. More to search up from tendency_of_air_temperature_due_to....!

![image](https://github.com/user-attachments/assets/ebc546a6-f480-4b4b-9e1b-648324c326d9)



