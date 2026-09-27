"""6-hourly pipeline: latest GFS run -> NH fields at 850/500/250 hPa -> Hugging Face.

Usage (GitHub Actions):  python run_pipeline.py --repo yanxingjianken/nh-forecast-6hourly
Local dry run:           python run_pipeline.py --dry-run --max-step 24 --out /tmp/x

All working files live in a temporary directory that is removed when the run
ends; nothing model-sized is kept on the machine that runs this script.  The
published dataset holds: the latest run (all steps), the last 5 days of
analyses (f000 of every run), the vortex tracks, and the Z500 climatology.

Dataset layout (all paths relative to the repo root):
  index.json                          latest run id, steps, analysis list, grid
  gfs/runs/<RUN>/meta.json            run description (steps, fields, grids)
  gfs/runs/<RUN>/f<STEP>/<var><lev>.u16.gz         NH 0.5 deg  (181 x 720)
  gfs/runs/<RUN>/f<STEP>/conus/<var><lev>.u16.gz   CONUS 0.25 deg (141 x 281)
  gfs/analyses/<RUN>/<var><lev>.u16.gz             NH 0.5 deg analysis (f000)
  gfs/analyses/<RUN>/conus/<var><lev>.u16.gz
  gfs/tracks/latest.json              tracks (total-field and anomaly bases)
  climatology/z500_ltm_1991-2020_2p5.u16.gz
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from common import (CONUS_QTR, LEVELS, NH_HALF, VARS, decode_field, encode_field,  # noqa: E402
                    field_filename, write_json)
import fetch_gfs  # noqa: E402
import climatology  # noqa: E402
import tracking  # noqa: E402

MODEL = "gfs"
N_ANALYSIS_DAYS = 5


def log(msg):
    print(f"[{datetime.now(timezone.utc):%H:%M:%S}] {msg}", flush=True)


# ----------------------------------------------------------------------------
# field extraction
# ----------------------------------------------------------------------------
def subset_grid(ds, grid):
    """Return dict {(var, level): 2-D float32} on the requested grid."""
    lat_sel = grid.lats
    lon_sel = grid.lons % 360.0
    sub = ds.sel(latitude=lat_sel, longitude=lon_sel, method="nearest")
    out = {}
    for short, (vid, _units) in VARS.items():
        for lev in LEVELS:
            out[(vid, lev)] = sub[short].sel(isobaricInhPa=lev).values.astype(np.float32)
    return out


def write_fields(fields, grid, dirpath, hdr_base):
    os.makedirs(dirpath, exist_ok=True)
    for (vid, lev), arr in fields.items():
        units = [u for s, (v, u) in VARS.items() if v == vid][0]
        hdr = dict(hdr_base)
        hdr.update({"var": vid, "level": lev, "units": units, "lat0": grid.lat0, "dlat": grid.dlat,
                    "lon0": grid.lon0, "dlon": grid.dlon})
        with open(os.path.join(dirpath, field_filename(vid, lev)), "wb") as f:
            f.write(encode_field(arr, hdr))


def process_step(init, step, out_run_dir, cache_dir=None):
    data = fetch_gfs.fetch_subset(init, step, cache_dir=cache_dir)
    ds = fetch_gfs.open_grib(data)
    valid = init + timedelta(hours=step)
    hdr = {"model": MODEL, "init": init.strftime("%Y-%m-%dT%H:00Z"),
           "valid": valid.strftime("%Y-%m-%dT%H:00Z"), "step": step}
    nh = subset_grid(ds, NH_HALF)
    conus = subset_grid(ds, CONUS_QTR)
    d = os.path.join(out_run_dir, f"f{step:03d}")
    write_fields(nh, NH_HALF, d, hdr)
    write_fields(conus, CONUS_QTR, os.path.join(d, "conus"), hdr)
    return nh[("z", 500)]


# ----------------------------------------------------------------------------
# Hugging Face helpers
# ----------------------------------------------------------------------------
def hf_api():
    from huggingface_hub import HfApi
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN is not set")
    return HfApi(token=token)


def hf_download_z500_analyses(api, repo, run_ids, tmp):
    """Fetch previously published analysis z500 fields; returns {run_id: array}."""
    from huggingface_hub import hf_hub_download
    from huggingface_hub.utils import EntryNotFoundError
    out = {}
    for rid in run_ids:
        try:
            p = hf_hub_download(repo_id=repo, repo_type="dataset",
                                filename=f"gfs/analyses/{rid}/z500.u16.gz",
                                cache_dir=os.path.join(tmp, "hfcache"))
            with open(p, "rb") as f:
                _hdr, arr = decode_field(f.read())
            out[rid] = arr
        except EntryNotFoundError:
            pass
        except Exception as e:  # pragma: no cover
            log(f"  could not fetch analysis {rid} from HF: {e}")
    return out


def hf_list(api, repo):
    try:
        return api.list_repo_files(repo, repo_type="dataset")
    except Exception:
        return []


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.environ.get("HF_DATASET", "yanxingjianken/nh-forecast-6hourly"))
    ap.add_argument("--run", help="force a run id YYYYMMDDHH (default: latest complete)")
    ap.add_argument("--max-step", type=int, default=240)
    ap.add_argument("--step-hours", type=int, default=6)
    ap.add_argument("--dry-run", action="store_true", help="do not upload; keep output in --out")
    ap.add_argument("--out", help="output directory for --dry-run (default: temp dir)")
    ap.add_argument("--cache-dir", help="GRIB cache for development only (never used in CI)")
    ap.add_argument("--squash", action="store_true", help="squash dataset history after upload")
    args = ap.parse_args()

    t_start = time.time()
    if args.run:
        init = datetime.strptime(args.run, "%Y%m%d%H").replace(tzinfo=timezone.utc)
    else:
        init = fetch_gfs.latest_complete_run(max_step=args.max_step)
    run_id = fetch_gfs.run_id(init)
    steps = list(range(0, args.max_step + 1, args.step_hours))
    log(f"run {run_id}, {len(steps)} steps to f{args.max_step:03d}")

    tmp_root = args.out if (args.dry_run and args.out) else tempfile.mkdtemp(prefix="nhf_")
    out_root = os.path.join(tmp_root, "publish")
    run_dir = os.path.join(out_root, "gfs", "runs", run_id)
    os.makedirs(run_dir, exist_ok=True)
    api = None if args.dry_run else hf_api()

    try:
        # ---- forecast steps -------------------------------------------------
        z500_fcst = []
        for k, step in enumerate(steps):
            t0 = time.time()
            z500_fcst.append(process_step(init, step, run_dir, cache_dir=args.cache_dir))
            log(f"  f{step:03d} done ({time.time() - t0:.1f}s)")
        # the f000 of this run is also the newest analysis
        anl_dir = os.path.join(out_root, "gfs", "analyses", run_id)
        shutil.copytree(os.path.join(run_dir, "f000"), anl_dir)

        # ---- analysis history (last 5 days) --------------------------------
        n_anl = N_ANALYSIS_DAYS * 24 // 6
        anl_times = [init - timedelta(hours=6 * k) for k in range(n_anl, 0, -1)]
        anl_ids = [fetch_gfs.run_id(t) for t in anl_times]
        have = hf_download_z500_analyses(api, args.repo, anl_ids, tmp_root) if api else {}
        z500_anl = []
        for t, rid in zip(anl_times, anl_ids):
            if rid in have:
                z500_anl.append(have[rid])
                continue
            try:
                log(f"  fetching missing analysis {rid}")
                d_tmp = os.path.join(tmp_root, "anl_tmp", rid)
                z = process_step(t, 0, d_tmp, cache_dir=args.cache_dir)
                # publish it too so future runs do not need to refetch it
                shutil.copytree(os.path.join(d_tmp, "f000"), os.path.join(out_root, "gfs", "analyses", rid))
                z500_anl.append(z)
            except Exception as e:
                log(f"  analysis {rid} unavailable ({e}); skipping")
                z500_anl.append(None)
        # drop leading gaps; interior gaps break tracks (tracks restart), acceptable
        times = anl_times + [init + timedelta(hours=s) for s in steps]
        series = z500_anl + z500_fcst
        keep = [i for i, z in enumerate(series) if z is not None]
        times = [times[i] for i in keep]
        series = [series[i] for i in keep]
        n_analysis = sum(1 for i in keep if i < len(anl_times))

        # ---- tracks ----------------------------------------------------------
        lats, lons = NH_HALF.lats, NH_HALF.lons
        ltm = climatology.load_z500_ltm()
        anom = [z - climatology.clim_on_grid(t, lats, lons, ltm) for z, t in zip(series, times)]
        tracks = {}
        for basis in ("total", "anom"):
            t0 = time.time()
            tracks[basis] = tracking.track_series(times, series, anom, lats, lons, basis=basis,
                                                  n_analysis=n_analysis)
            log(f"  tracking ({basis}): {len(tracks[basis])} tracks ({time.time() - t0:.1f}s)")
        tracks_obj = {
            "model": MODEL, "run": run_id, "init": init.strftime("%Y-%m-%dT%H:00Z"),
            "times": [t.strftime("%Y-%m-%dT%H:00Z") for t in times],
            "n_analysis": n_analysis,
            "method": {"params": tracking.PARAMS, "search_km": tracking.SEARCH_KM, "min_life_steps": tracking.MIN_LIFE,
                       "lat_range": [tracking.LAT_MIN, tracking.LAT_MAX],
                       "anomaly": "NCEP/NCAR R1 1991-2020 daily LTM, 2.5 deg, bilinear", "doc": tracking.__doc__},
            "bases": {"anom": "extrema of smoothed Z500 anomaly (default)", "total": "extrema of smoothed total Z500"},
            "tracks": tracks,
        }
        write_json(os.path.join(out_root, "gfs", "tracks", "latest.json"), tracks_obj)
        write_json(os.path.join(out_root, "gfs", "tracks", f"tracks_{run_id}.json"), tracks_obj)

        # ---- climatology (published once; cheap to re-add) -------------------
        clim_out = os.path.join(out_root, "climatology", "z500_ltm_1991-2020_2p5.u16.gz")
        src = os.path.join(HERE, "data", "z500_ltm_1991-2020_2p5.u16.gz")
        if os.path.exists(src):
            os.makedirs(os.path.dirname(clim_out), exist_ok=True)
            shutil.copy(src, clim_out)

        # ---- meta / index -----------------------------------------------------
        fields = [f"{v}{l}" for _s, (v, _u) in VARS.items() for l in LEVELS]
        meta = {"model": MODEL, "run": run_id, "init": init.strftime("%Y-%m-%dT%H:00Z"),
                "steps": steps, "fields": fields,
                "grids": {"nh": NH_HALF.__dict__, "conus": CONUS_QTR.__dict__},
                "source": "NOAA GFS 0.25 deg (AWS noaa-gfs-bdp-pds / NOMADS)",
                "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
        write_json(os.path.join(run_dir, "meta.json"), meta)

        existing = hf_list(api, args.repo) if api else []
        anl_keep = set(anl_ids + [run_id])
        published_anl = sorted({p.split("/")[2] for p in existing if p.startswith("gfs/analyses/")} | anl_keep)
        published_anl = [a for a in published_anl if a in anl_keep]
        index = {"updated": meta["generated"], "models": {
            MODEL: {"latest_run": run_id, "init": meta["init"], "steps": steps, "fields": fields,
                    "grids": meta["grids"], "analyses": published_anl,
                    "tracks": "gfs/tracks/latest.json"}},
            "climatology": "climatology/z500_ltm_1991-2020_2p5.u16.gz"}
        write_json(os.path.join(out_root, "index.json"), index)

        total_bytes = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(out_root) for f in fs)
        log(f"prepared {total_bytes / 1e6:.1f} MB in {out_root}")

        if args.dry_run:
            log("dry run: not uploading")
            return

        # ---- upload ---------------------------------------------------------------
        from huggingface_hub import CommitOperationAdd, CommitOperationDelete
        api.create_repo(args.repo, repo_type="dataset", exist_ok=True, private=False)
        ops = []
        for dp, _, fs in os.walk(out_root):
            for f in fs:
                p = os.path.join(dp, f)
                ops.append(CommitOperationAdd(path_in_repo=os.path.relpath(p, out_root), path_or_fileobj=p))
        # delete superseded runs and analyses older than the window
        old_runs = {p.split("/")[2] for p in existing if p.startswith("gfs/runs/") and p.split("/")[2] != run_id}
        for r in old_runs:
            ops.append(CommitOperationDelete(path_in_repo=f"gfs/runs/{r}/", is_folder=True))
        old_anl = {p.split("/")[2] for p in existing if p.startswith("gfs/analyses/")} - anl_keep
        for a in old_anl:
            ops.append(CommitOperationDelete(path_in_repo=f"gfs/analyses/{a}/", is_folder=True))
        old_tracks = [p for p in existing if p.startswith("gfs/tracks/tracks_") and run_id not in p]
        for p in sorted(old_tracks)[:-8]:          # keep the last 8 track files
            ops.append(CommitOperationDelete(path_in_repo=p))
        log(f"uploading {len(ops)} operations to {args.repo}")
        api.create_commit(repo_id=args.repo, repo_type="dataset", operations=ops,
                          commit_message=f"GFS {run_id}: {len(steps)} steps, tracks, analyses")
        if args.squash:
            log("squashing history")
            api.super_squash_history(repo_id=args.repo, repo_type="dataset")
        log(f"done in {(time.time() - t_start) / 60:.1f} min")
    finally:
        if not (args.dry_run and args.out):
            shutil.rmtree(tmp_root, ignore_errors=True)


if __name__ == "__main__":
    main()
