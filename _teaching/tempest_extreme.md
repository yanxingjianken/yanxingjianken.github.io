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

---

1. xsh24 surface cyclone tracking (200 Pa increase outward within 6 degs) [GFDL downloadable from /scratch/cimes/xy4043/tracks]
2. xsh24 z500 anticyclone tracking (10 m z500 decrease outward within 6 degs) [GFDL downloadable from /scratch/cimes/xy4043/tracks]
3. ERA5 z500 anticyclone tracking (1990-2020) (10 m z500 decrease outward within 6 degs) [link](https://drive.google.com/file/d/1xRmgEvVNLUCzKgLYXIICqBztefmYb6gs/view?usp=sharing)
4. Filtered Euro-Atlantic ERA5 z500 anticyclone tracking (1990-2020) [link](https://drive.google.com/file/d/1GcURsA59RdJqnkb_LyJ4Ms7PD4LiWezP/view?usp=sharing)

---

...and here's a quick tutorial on how to use the tool:

(Note: Performance comparison assessments of results compared to blocking tracking algo [ConTrack](https://github.com/steidani/ConTrack) is also done by Mingyu.)

The following tutorial uses stellar-amd node of GFDL and runs on the X-Shield 2024 data that is not published yet.

1. module load anaconda3/2024.10
2. Install the [yml file]((https://github.com/cjgliddon/hackathon25_blocking/blob/main/tempest_extreme/tempest_env.yml)) via: conda env create -f env_tempest.yml 
3. Register as an ipynb kernel: conda activate tempest_extreme_new
python -m ipykernel install --user \
       --name tempest_extreme_new \
       --display-name "Python (tempest_extreme_new)"
4. Check nco
5. Check cdo
6. Go to /scratch/cimes/xy4043/tutorial and get all .sh files (or visit the hackathon blocking group [repo](https://github.com/cjgliddon/hackathon25_blocking))
7. chmod +x stitch_nodes_3hrly_anticyclone.sh (and all other 3 sh files)
8. run  ./detect_node_anticyclone.sh 
9. run  ./stitch_nodes_3hrly_anticyclone.sh
10. The results (raw, and reformatted csv) are in /scratch/cimes/xy4043/tracks/
11. If you want to extract specific tracks that pass through some lon lat boxes, run filter_tracks.py (email Ken for code)

![image](https://github.com/user-attachments/assets/97be3fbd-cde0-43d9-9fca-e280d686d4f0)

If we impose certain spatialtemporal constraints, we can filter out persistent blocking events:
![image](https://github.com/user-attachments/assets/78eb1eff-8a05-452c-96ce-d7e48821e974)


The xsh24 model also has several temperature tendecy terms, and here's a quick note:
1. shallow convection is called 'tendency_of_air_temperature_due_to_shallow_convection_coarse_C3072_1440x720'
2. deep convection is called 't_dt_gfdlmp_coarse_C3072_1440x720', mp = micro-physics
3. temperature tendecy 't_dt_phys_coarse_C3072_1440x720' includes both radiation and shallow convection
4. More to search up from tendency_of_air_temperature_due_to....!

![image](https://github.com/user-attachments/assets/ebc546a6-f480-4b4b-9e1b-648324c326d9)


### Misc. Notes
#### Multiple track constraints
```bash
# Extract Nodes from ERA5 Data
extract_nodes(){
    local yr=$1
    local mth=$2

    # Prepare list of input files
    [ ! -e files_$yr$mth.tmp ] || rm files_$yr$mth.tmp
    msl_file=$parent_folder/era5_msl_${yr}_${mth}.nc
    u10_file=$parent_folder/era5_u10_${yr}_${mth}.nc
    v10_file=$parent_folder/era5_v10_${yr}_${mth}.nc
    t_file=$parent_folder/ta_day_FGOALS-f3-H_hist-1950_r1i1p1f1_gr_${yr}${mth}01-${yr}${mth}$(cal $mth $yr | awk 'NF {DAYS = $NF}; END {print DAYS}').nc
    echo -e "${t_file};${msl_file};${u10_file};${v10_file}" >> files_$yr$mth.tmp

    # Output file
    node_file=$save_folder/${yr}${mth}

    # Detect Nodes
    /home/anamitra/cyclone_tracks/trackers/tempestextremes/bin/DetectNodes \
        --in_data_list files_$yr$mth.tmp \
        --out $node_file \
        --timestride 6 \
        --searchbymin psl \
        --closedcontourcmd "psl,200.0,5.5,0;ta(50000Pa),-0.4,8.0,1.1" \
        --mergedist 6.0 \
        --outputcmd  "psl,min,0;_VECMAG(uas,vas),max,2" \
        --latname lat --lonname lon
    
    # Cleanup
    rm files_$yr$mth.tmp
}
```

#### Multiple Stitch Constraints
```bash
/glade/work/anamitra/tempestextremes/bin/StitchNodes \
        --in_list nodeslist.tmp \
        --out tracks/ERA5_TempestExtremes.csv \
        --in_fmt "lon,lat,slp,zs,wind10" \
        --range 8.0 \
        --mintime "54h" \
        --maxgap "24h" \
        --threshold "wind10,>=,10.0,10;lat,<=,50.0,10;lat,>=,-50.0,10;zs,<=,150.0,10" \
        --out_file_format "csv"
```



