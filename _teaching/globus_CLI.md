---
title: "Intro to Globus CLI (on HPC)"
collection: notes
type: "misc."
permalink: /teaching/globus_CLI
venue: "misc."
date: 2025-06-10
location: "Cambridge, MA"
---

This is a quick intro on how to use Globus Command Line Interface [line](https://docs.globus.org/cli/) to transfer from NCAR to MIT oceans

---

x_yan@dolma:~$ cd /net/flood/data/users/x_yan/cmip_data

x_yan@dolma:/net/flood/data/users/x_yan/cmip_data$ module add apps/globusconnectpersonal/3.2.2

x_yan@dolma:/net/flood/data/users/x_yan/cmip_data$ pip install --user globus-cli

x_yan@dolma:/net/flood/data/users/x_yan/cmip_data$ echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

x_yan@dolma:/net/flood/data/users/x_yan/cmip_data$ source ~/.bashrc

x_yan@dolma:/net/flood/data/users/x_yan/cmip_data$ which globus 

/home/x_yan/.local/bin/globus

x_yan@dolma:/net/flood/data/users/x_yan/cmip_data$ globus login --no-local-server

x_yan@dolma:/net/flood/data/users/x_yan/cmip_data$ globusconnectpersonal -setup 

x_yan@dolma:/net/flood/data/users/x_yan/cmip_data$ nohup globusconnectpersonal -start 

x_yan@dolma:/net/flood/data/users/x_yan/cmip_data$ globus whoami --verbose

x_yan@dolma:/net/flood/data/users/x_yan/cmip_data$ export CASPER_ID=d33b3614-6d04-11e5-ba46-22000b92c6ec

export DOLMA_ID=b86736ea-463c-11f0-afdf-0affd01a5913

x_yan@dolma:/net/flood/data/users/x_yan/cmip_data$ for n in {2..10}; do
  globus transfer \
      $CASPER_ID:/glade/derecho/scratch/doughert/MPAS/mem${n} \
      $DOLMA_ID:/net/flood/data/users/x_yan/cmip_data/mem${n} \
      --recursive --verify-checksum --preserve-mtime \
      --label "mpas_mem${n}"
done
The collection you are trying to access data on requires you to grant consent for the Globus CLI to access it.

Please run: xxxx


x_yan@dolma:/net/flood/data/users/x_yan/cmip_data$ for n in {2..10}; do
  globus transfer \
      $CASPER_ID:/glade/derecho/scratch/doughert/MPAS/mem${n} \
      $DOLMA_ID:mem${n} \
      --recursive --verify-checksum --preserve-mtime \
      --label "mpas_mem${n}"
done
![image](https://github.com/user-attachments/assets/b740f52a-95ba-49d0-b69c-7fc58b0a941f)



