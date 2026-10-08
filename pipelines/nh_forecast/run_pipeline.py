"""6-hourly pipeline: latest NWP runs -> NH fields at 850/500/250 hPa -> Hugging Face.

Usage (GitHub Actions, hourly):  python run_pipeline.py --repo yanxingjianken/nh-forecast-6hourly
Local dry run:                   python run_pipeline.py --dry-run --models gfs --max-step 24 --out /tmp/x

Models: gfs (NOAA GFS 0.25), aifs (ECMWF AIFS-single 0.25) and ifs (ECMWF IFS 0.25).  For each model
the script finds the newest run whose last step is available, skips it if the
dataset already holds it (idempotent, so the job can run hourly), otherwise
downloads the 18 fields for every 6-h step, encodes them, tracks Z500 centres
over the previous five days plus the forecast, and publishes one commit per
model.  All working files live in a temporary directory that is removed when
the run ends; nothing model-sized is kept on the machine that runs this.

Dataset layout (paths relative to the repo root):
  index.json                                    per-model latest run, steps, analyses, grids
  <model>/runs/<RUN>/meta.json
  <model>/runs/<RUN>/f<STEP>/<var><lev>.u16.gz  NH 0.5 deg (181 x 720), one file per field
  <model>/runs/<RUN>/f<STEP>/conus.u16.gz       CONUS 0.25 deg (141 x 281), 18 fields packed
  <model>/analyses/<RUN>/<var><lev>.u16.gz      NH 0.5 deg analysis (f000), last 5 days
  <model>/tracks/latest.json                    tracks (anomaly and total-field bases)
  climatology/z500_ltm_1991-2020_2p5.u16.gz
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone

import numpy as np
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from common import CONUS_QTR, LEVELS, NH_HALF, VARS, decode_field, encode_field, field_filename, write_json  # noqa: E402
import climatology  # noqa: E402
import tracking  # noqa: E402
from gribio import derive_surface  # noqa: E402
import model_gfs  # noqa: E402
import model_aifs  # noqa: E402
import model_ifs  # noqa: E402

MODELS = {"gfs": model_gfs, "aifs": model_aifs, "ifs": model_ifs}
N_ANALYSIS_DAYS = 5
VAR_UNITS = {v: u for _s, (v, u) in VARS.items()}
# near-surface fields, stored with level "sfc" (files <var>sfc.u16.gz): 2-m temperature and dew point,
# 10-m wind, mean-sea-level pressure and precipitation over the 6 h ending at the valid time
SFC_UNITS = {"t2m": "K", "d2m": "K", "u10": "m s-1", "v10": "m s-1", "msl": "hPa", "tp6": "mm"}
VAR_UNITS.update(SFC_UNITS)


def log(msg):
    print(f"[{datetime.now(timezone.utc):%H:%M:%S}] {msg}", flush=True)


# ----------------------------------------------------------------------------
# encoding
# ----------------------------------------------------------------------------
def subsample(fields, grid):
    """Pick grid.lats/grid.lons out of the 0.25 deg NH arrays (361 x 1440)."""
    jj = np.round((grid.lats - 0.0) / 0.25).astype(int)
    ii = np.round((grid.lons % 360.0) / 0.25).astype(int) % 1440
    return {k: np.ascontiguousarray(a[jj][:, ii]) for k, a in fields.items()}


def write_nh_fields(fields, dirpath, hdr_base):
    os.makedirs(dirpath, exist_ok=True)
    sub = subsample(fields, NH_HALF)
    for (vid, lev), arr in sub.items():
        hdr = dict(hdr_base, var=vid, level=lev, units=VAR_UNITS[vid], lat0=NH_HALF.lat0, dlat=NH_HALF.dlat,
                   lon0=NH_HALF.lon0, dlon=NH_HALF.dlon)
        with open(os.path.join(dirpath, field_filename(vid, lev)), "wb") as f:
            f.write(encode_field(arr, hdr))
    return sub.get(("z", 500))


def write_conus_pack(fields, dirpath, hdr_base):
    """All CONUS fields (18 pressure-level + 6 surface) in one gzip file: JSON header line + concatenated uint16 blocks; 65535 = missing."""
    os.makedirs(dirpath, exist_ok=True)
    sub = subsample(fields, CONUS_QTR)
    blocks, entries = [], []
    for (vid, lev), arr in sub.items():
        a = np.asarray(arr, dtype=np.float64)
        fin = np.isfinite(a)
        vmin, vmax = (float(a[fin].min()), float(a[fin].max())) if fin.any() else (0.0, 0.0)
        scale = (vmax - vmin) / 65000.0 if vmax > vmin else 1.0
        q = np.full(a.shape, 65535, dtype="<u2")
        q[fin] = np.round((a[fin] - vmin) / scale).astype("<u2")
        entries.append({"var": vid, "level": lev, "units": VAR_UNITS[vid], "offset": vmin, "scale": scale,
                        "vmin": vmin, "vmax": vmax})
        blocks.append(q.tobytes())
    hdr = dict(hdr_base, kind="pack", ny=CONUS_QTR.ny, nx=CONUS_QTR.nx, lat0=CONUS_QTR.lat0, dlat=CONUS_QTR.dlat,
               lon0=CONUS_QTR.lon0, dlon=CONUS_QTR.dlon, fields=entries, dtype="uint16le", missing=65535)
    htxt = json.dumps(hdr, separators=(",", ":"))
    if len(htxt.encode()) % 2 == 0:
        htxt += " "
    with open(os.path.join(dirpath, "conus.u16.gz"), "wb") as f:
        f.write(gzip.compress(htxt.encode() + b"\n" + b"".join(blocks), 6))


# ----------------------------------------------------------------------------
# Hugging Face helpers
# ----------------------------------------------------------------------------
def hf_api():
    from huggingface_hub import HfApi
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN is not set")
    return HfApi(token=token)


def hf_index(repo):
    """Current index.json on the Hub (None if absent)."""
    try:
        r = requests.get(f"https://huggingface.co/datasets/{repo}/resolve/main/index.json",
                         headers={"Cache-Control": "no-cache"}, timeout=60)
        if r.status_code == 200:
            return r.json()
    except requests.RequestException:
        pass
    return None


def hf_z500_analyses(repo, model, run_ids, tmp):
    from huggingface_hub import hf_hub_download
    out = {}
    for rid in run_ids:
        try:
            p = hf_hub_download(repo_id=repo, repo_type="dataset", filename=f"{model}/analyses/{rid}/z500.u16.gz",
                                cache_dir=os.path.join(tmp, "hfcache"))
            with open(p, "rb") as f:
                out[rid] = decode_field(f.read())[1]
        except Exception:
            pass
    return out


def hf_list(api, repo):
    try:
        return api.list_repo_files(repo, repo_type="dataset")
    except Exception:
        return []


# ----------------------------------------------------------------------------
def process_model(mid, args, api, index, tmp_root):
    M = MODELS[mid]
    if args.run:
        init = datetime.strptime(args.run, "%Y%m%d%H").replace(tzinfo=timezone.utc)
    else:
        init = M.latest_complete_run(max_step=args.max_step)
    run_id = M.run_id(init)
    cur = (index or {}).get("models", {}).get(mid, {})
    max_step = M.last_step(init, args.max_step) if hasattr(M, "last_step") else args.max_step
    if not args.force and cur.get("latest_run") == run_id and cur.get("steps", [None])[-1] == max_step:
        log(f"{mid}: run {run_id} already published; nothing to do")
        return None
    steps = list(range(0, max_step + 1, args.step_hours))
    log(f"{mid}: run {run_id}, {len(steps)} steps to f{max_step:03d}")
    out_root = os.path.join(tmp_root, mid, "publish")
    run_dir = os.path.join(out_root, mid, "runs", run_id)
    os.makedirs(run_dir, exist_ok=True)
    t_model = time.time()

    z500_fcst = []
    tp_state = {}
    for step in steps:
        t0 = time.time()
        fields = M.fetch_fields(init, step, cache_dir=args.cache_dir)
        sfc = derive_surface(fields, step, tp_state, M.TP_TO_MM)
        fields = {k: v for k, v in fields.items() if isinstance(k[1], int)}
        valid = init + timedelta(hours=step)
        hdr = {"model": mid, "init": init.strftime("%Y-%m-%dT%H:00Z"), "valid": valid.strftime("%Y-%m-%dT%H:00Z"), "step": step}
        d = os.path.join(run_dir, f"f{step:03d}")
        z500_fcst.append(write_nh_fields(fields, d, hdr))
        write_nh_fields(sfc, d, hdr)
        write_conus_pack({**fields, **sfc}, d, hdr)
        log(f"  f{step:03d} done ({time.time() - t0:.1f}s)")
    anl_dir = os.path.join(out_root, mid, "analyses", run_id)
    shutil.copytree(os.path.join(run_dir, "f000"), anl_dir, ignore=shutil.ignore_patterns("conus.u16.gz", "*sfc.u16.gz"))

    # ---- analysis history (last 5 days) --------------------------------------
    n_anl = N_ANALYSIS_DAYS * 24 // 6
    anl_times = [init - timedelta(hours=6 * k) for k in range(n_anl, 0, -1)]
    anl_ids = [M.run_id(t) for t in anl_times]
    have = hf_z500_analyses(args.repo, mid, anl_ids, tmp_root) if api else {}
    z500_anl = []
    for t, rid in zip(anl_times, anl_ids):
        if rid in have:
            z500_anl.append(have[rid]); continue
        try:
            log(f"  fetching missing analysis {rid}")
            fields = M.fetch_fields(t, 0, cache_dir=args.cache_dir)
            fields = {k: v for k, v in fields.items() if isinstance(k[1], int)}
            hdr = {"model": mid, "init": t.strftime("%Y-%m-%dT%H:00Z"), "valid": t.strftime("%Y-%m-%dT%H:00Z"), "step": 0}
            z500_anl.append(write_nh_fields(fields, os.path.join(out_root, mid, "analyses", rid), hdr))
        except Exception as e:
            log(f"  analysis {rid} unavailable ({e}); skipping")
            z500_anl.append(None)
    times = anl_times + [init + timedelta(hours=s) for s in steps]
    series = z500_anl + z500_fcst
    keep = [i for i, z in enumerate(series) if z is not None]
    times = [times[i] for i in keep]; series = [series[i] for i in keep]
    n_analysis = sum(1 for i in keep if i < len(anl_times))

    # ---- tracks ----------------------------------------------------------------
    lats, lons = NH_HALF.lats, NH_HALF.lons
    ltm = climatology.load_z500_ltm()
    anom = [z - climatology.clim_on_grid(t, lats, lons, ltm) for z, t in zip(series, times)]
    tracks = {}
    for basis in ("anom", "total"):
        t0 = time.time()
        tracks[basis] = tracking.track_series(times, series, anom, lats, lons, basis=basis, n_analysis=n_analysis)
        log(f"  tracking ({basis}): {len(tracks[basis])} tracks ({time.time() - t0:.1f}s)")
    tracks_obj = {"model": mid, "run": run_id, "init": init.strftime("%Y-%m-%dT%H:00Z"),
                  "times": [t.strftime("%Y-%m-%dT%H:00Z") for t in times], "n_analysis": n_analysis,
                  "method": {"params": tracking.PARAMS, "search_km": tracking.SEARCH_KM, "min_life_steps": tracking.MIN_LIFE,
                             "lat_range": [tracking.LAT_MIN, tracking.LAT_MAX],
                             "anomaly": "NCEP/NCAR R1 1991-2020 daily LTM, 2.5 deg, bilinear", "doc": tracking.__doc__},
                  "bases": {"anom": "extrema of smoothed Z500 anomaly (default)", "total": "extrema of smoothed total Z500"},
                  "tracks": tracks}
    write_json(os.path.join(out_root, mid, "tracks", "latest.json"), tracks_obj)
    write_json(os.path.join(out_root, mid, "tracks", f"tracks_{run_id}.json"), tracks_obj)

    # ---- meta ------------------------------------------------------------------
    fields_list = [f"{v}{l}" for _s, (v, _u) in VARS.items() for l in LEVELS] + [f"{v}sfc" for v in SFC_UNITS]
    meta = {"model": mid, "label": M.LABEL, "run": run_id, "init": init.strftime("%Y-%m-%dT%H:00Z"), "steps": steps,
            "fields": fields_list, "grids": {"nh": NH_HALF.__dict__, "conus": CONUS_QTR.__dict__}, "source": M.SOURCE,
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    write_json(os.path.join(run_dir, "meta.json"), meta)
    log(f"{mid}: prepared in {(time.time() - t_model) / 60:.1f} min")
    return {"out_root": out_root, "run_id": run_id, "init": meta["init"], "steps": steps, "fields": fields_list,
            "grids": meta["grids"], "anl_keep": set(anl_ids + [run_id]), "label": M.LABEL, "source": M.SOURCE}


def publish(mid, res, args, api, index, existing):
    from huggingface_hub import CommitOperationAdd, CommitOperationDelete
    out_root = res["out_root"]
    # climatology (small, republished with every commit so it is never missing)
    src = os.path.join(HERE, "data", "z500_ltm_1991-2020_2p5.u16.gz")
    if os.path.exists(src):
        dst = os.path.join(out_root, "climatology", "z500_ltm_1991-2020_2p5.u16.gz")
        os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(src, dst)
    # index.json (merged with what is already on the Hub)
    index = index or {}
    index.setdefault("models", {})
    published_anl = sorted(({p.split("/")[2] for p in existing if p.startswith(f"{mid}/analyses/")} | res["anl_keep"]) & res["anl_keep"])
    index["models"][mid] = {"label": res["label"], "source": res["source"], "latest_run": res["run_id"], "init": res["init"],
                            "steps": res["steps"], "fields": res["fields"], "grids": res["grids"], "analyses": published_anl,
                            "tracks": f"{mid}/tracks/latest.json"}
    index["climatology"] = "climatology/z500_ltm_1991-2020_2p5.u16.gz"
    index["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    index["format"] = "gzip(JSON header line + uint16 LE array); value = offset + scale*u16; 65535 = missing"
    write_json(os.path.join(out_root, "index.json"), index)
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(out_root) for f in fs)
    log(f"{mid}: {total / 1e6:.1f} MB to upload")
    if args.dry_run:
        return index
    ops = []
    for dp, _, fs in os.walk(out_root):
        for f in fs:
            p = os.path.join(dp, f)
            ops.append(CommitOperationAdd(path_in_repo=os.path.relpath(p, out_root), path_or_fileobj=p))
    for r in {p.split("/")[2] for p in existing if p.startswith(f"{mid}/runs/") and p.split("/")[2] != res["run_id"]}:
        ops.append(CommitOperationDelete(path_in_repo=f"{mid}/runs/{r}/", is_folder=True))
    for a in {p.split("/")[2] for p in existing if p.startswith(f"{mid}/analyses/")} - res["anl_keep"]:
        ops.append(CommitOperationDelete(path_in_repo=f"{mid}/analyses/{a}/", is_folder=True))
    old_tracks = sorted(p for p in existing if p.startswith(f"{mid}/tracks/tracks_") and res["run_id"] not in p)
    for p in old_tracks[:-8]:
        ops.append(CommitOperationDelete(path_in_repo=p))
    log(f"{mid}: committing {len(ops)} operations to {args.repo}")
    api.create_commit(repo_id=args.repo, repo_type="dataset", operations=ops,
                      commit_message=f"{mid.upper()} {res['run_id']}: {len(res['steps'])} steps, tracks, analyses")
    return index


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.environ.get("HF_DATASET", "yanxingjianken/nh-forecast-6hourly"))
    ap.add_argument("--models", default="gfs,aifs,ifs")
    ap.add_argument("--run", help="force a run id YYYYMMDDHH (applies to every selected model)")
    ap.add_argument("--max-step", type=int, default=240)
    ap.add_argument("--step-hours", type=int, default=6)
    ap.add_argument("--force", action="store_true", help="publish even if the run is already on the Hub")
    ap.add_argument("--dry-run", action="store_true", help="do not upload; keep output in --out")
    ap.add_argument("--out", help="output directory for --dry-run (default: temp dir)")
    ap.add_argument("--cache-dir", help="GRIB cache for development only (never used in CI)")
    ap.add_argument("--squash", action="store_true", help="squash dataset history after upload")
    args = ap.parse_args()

    t_start = time.time()
    tmp_root = args.out if (args.dry_run and args.out) else tempfile.mkdtemp(prefix="nhf_")
    api = None if args.dry_run else hf_api()
    index = hf_index(args.repo)
    if api:
        api.create_repo(args.repo, repo_type="dataset", exist_ok=True, private=False)
    existing = hf_list(api, args.repo) if api else []
    published = 0
    try:
        for mid in [m.strip() for m in args.models.split(",") if m.strip()]:
            try:
                res = process_model(mid, args, api, index, tmp_root)
            except Exception as e:
                log(f"{mid}: FAILED ({e})")
                continue
            if res is None:
                continue
            index = publish(mid, res, args, api, index, existing)
            published += 1
        if api and args.squash:
            log("squashing history")
            api.super_squash_history(repo_id=args.repo, repo_type="dataset")
        log(f"done in {(time.time() - t_start) / 60:.1f} min ({published} model run(s) published)")
    finally:
        if not (args.dry_run and args.out):
            shutil.rmtree(tmp_root, ignore_errors=True)


if __name__ == "__main__":
    main()
