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

## check CPU usages - live view
1. ```bash
   htop
   ```
2. ```bash
   top -u "$USER"
   ```
3. ```bash
   top -p 78309
   ```

## top 11 CPU occupying tasks, or single event checks:
1. ```bash
   ps -u "$USER" -o pid,ppid,%cpu,%mem,etime,cmd --sort=-%cpu | head -n 11
   ```
2. Basic status snapshot:
```bash
ps -p 78309 -o pid,ppid,sid,tty,stat,%cpu,%mem,etime,cmd
```

## Download and Unzip
1. download a zip file:
```bash
wget https://www2.mmm.ucar.edu/projects/mpas/real/cfsr.2010102300.tar.gz
```
2. ```bash
   unzip a file: tar xf cfsr.2010102300.tar.gz
   ```

## Close your VSCode and go home without task being stopped
1. ```bash
   nohup "$(command -v python)" -u download_era5_pressure_levels.py   > logs/era5_$(date +%F_%H%M).log 2>&1 & echo $! > era5.pid
   ```
2. ```bash
   disown
   ```

#### Another example
```bash
chmod +x blocking_clim_detect.sh
LOGDIR="/net/flood/data/users/x_yan/isobaric_era5/tracking_tmppp"
mkdir -p "$LOGDIR"
LOG="${LOGDIR}/blocking_clim_detect_$(date +%F_%H%M%S).log"
nohup bash -lc '
  source ~/.bashrc
  source activate tempest_extreme_new
  export OMP_NUM_THREADS=1
  nice -n 10 ionice -c2 -n7 ./blocking_clim_detect.sh
' > "$LOG" 2>&1 & echo $! > "${LOG}.pid" && disown
```
#### To Watch progress 
```bash
tail -f "$LOG"
# or only show warnings/errors:
tail -f "$LOG" | egrep -i 'error|warn|fail|missing'

# Check if running
ps -fp "$(cat "${LOG}.pid")"
```

#### To stop
```bash
PID=$(cat "${LOG}.pid")
PGID=$(ps -o pgid= -p "$PID" | tr -d ' ')
# TERM first, then KILL if needed:
kill -TERM -"$PGID" 2>/dev/null || kill -TERM "$PID"
sleep 5
kill -KILL -"$PGID" 2>/dev/null || true
```

