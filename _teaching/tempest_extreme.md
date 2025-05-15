---
title: "Using Tempest Extreme to track (Anti)Cyclones anywhere on any level surfaces!"
collection: misc.
type: "2025 Princeton GFDL Hackathon"
permalink: /teaching/tempest_extreme
venue: "Princeton GFDL"
date: 2025-05-14
location: "Princeton, NJ"
---

Some takeways from the 2025 Princeton GFDL Hackathon, a tracking algo!

---

The amazing group of hk25-blocking worked jointly on identifying blocking (persistent mid/high latitude anticyclones) and extratropical cyclones. 
Members include [Dr. Gan Zhang](https://climas.illinois.edu/directory/profile/gzhang13) from UIUC, [Dr. Mingyu Park](https://mingyupark.scholar.princeton.edu/) from Princeton, [Yanjun Hu](https://scholar.google.com/citations?user=YIl2UewAAAAJ&hl=zh-CN) from Purdue, [Coleman Gliddon](https://cjgliddon.github.io/) from MIT, and me.

A tool to track any features that depart from neighboring points (say, cyclones on surface pressure, or anticyclones on z500 isobaric level, etc.) could be using
this tool of [Tempest Extreme](), and here's a quick tutorial.

Note: Performance comparison assessments of results compared to blocking tracking algo [ConTrack]() is also done by Minyu.

The following tutorial uses stellar-amd node of GFDL and runs on the X-Shield 2024 data that is not published yet.

1. Go get env yml file "environment_coleman.yml" located [in this repo](https://github.com/cjgliddon/hackathon25_blocking/tree/main/tempest_extreme)
2. module load anaconda3/2024.10 and install the yml file to get conda env tempest_extreme
3. conda install -c conda-forge nco (also register as ipykernel, optional)
4. Go to /scratch/cimes/xy4043/tutorial and get all files
5. chmod +x stitch_nodes_3hrly_anticyclone.sh (and all other 3 sh files)
6. run  ./detect_node_anticyclone.sh 
7. run  ./stitch_nodes_3hrly_anticyclone.sh
8. The results (raw, and reformatted csv) are in /scratch/cimes/xy4043/tracks/

![image](https://github.com/user-attachments/assets/97be3fbd-cde0-43d9-9fca-e280d686d4f0)

Some comments from our wonder colleagues / fellow hackers in Hamburg:
![image](https://github.com/user-attachments/assets/33235014-dfbe-46ac-8c93-bf38cbdf58d0)


