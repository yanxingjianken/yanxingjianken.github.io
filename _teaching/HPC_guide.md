---
title: "HPC Quick Notes"
collection: notes
type: "misc."
permalink: /teaching/hpc_guide
venue: "misc."
date: 2025-08-25
location: "Cambridge, MA"
---

Some useful HPC commands

---

1. htop: check CPU usages
2.  ps -u "$USER" -o pid,ppid,%cpu,%mem,etime,cmd --sort=-%cpu | head -n 11: top 11 CPU occupying commands by you

