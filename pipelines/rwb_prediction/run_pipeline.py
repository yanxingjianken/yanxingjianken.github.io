"""Daily RWB prediction check: ERA5T breaking onsets against four methods, published to a Hugging Face dataset.

Daily mode (GitHub Actions): fetch the ERA5T days not yet cached (the newest is about 5 days behind real time),
process every 00/12 UTC issue time whose 24-h verification window is now covered, render the maps, and upload the
issue records, maps, summary and index. The surfaces of the last few days are cached on the dataset, so each run
downloads about one new ERA5 day.

Backfill mode (run once by hand): the same for a range of issue times from local ERA5 files, in parallel.

Dataset layout: index.json; summary.json (per-issue outcome strings for the heatmaps, the onset log); issues/<YYYY
MMDDHH>.json; maps/<YYYYMMDDHH>_<surface>.png; cache/surf_<YYYYMMDD>.npz.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import date, datetime, timedelta, timezone

import numpy as np

import core
import era5
import events as E
import gfs
import render
import surfaces as S
from config import AMP_FIT_LAST_ISSUE, AMP_THRESHOLD_DEG, GFS_STEPS_H, OPUS_SPAN_H, SURFACES, WINDOW_H

CACHE_DAYS = 5          # an issue at 00 UTC needs fields from 84 h before: five whole days plus the new one
H_GLOBAL = None


def log(msg):
    print(f"[{datetime.now(timezone.utc):%H:%M:%S}] {msg}", flush=True)


def step_summary(lines):
    """Append lines to the GitHub Actions run summary (shown on the run page); no-op elsewhere."""
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a") as fh:
            fh.write("\n".join(lines) + "\n")


def not_released(e):
    """True for the Climate Data Store's answers that a day is not (completely) available yet; anything else, such as
    a rejected API key or a network failure, is an error that must fail the run."""
    return isinstance(e, era5.Incomplete) or "None of the data you have requested is available" in str(e) \
        or "is not available yet" in str(e)


# ------------------------------------------------------------------------------------------------ surfaces per day
def day_surfaces(path):
    times, F = era5.read_day(path)
    out = {}
    for h in range(24):
        out[h] = S.surfaces(F["u"][h], F["v"][h], F["t"][h])
    return [np.datetime64(x, "h").astype(datetime) for x in times], out


def pack_day(times, surf):
    arr = {}
    for name in SURFACES:
        for k, var in enumerate("quv"):
            arr[f"{name}_{var}"] = np.array([surf[h][name][k] for h in range(24)], np.float32)
    arr["t0"] = np.array(times[0].strftime("%Y%m%d%H"))
    buf = io.BytesIO()
    np.savez_compressed(buf, **arr)
    return buf.getvalue()


def unpack_day(blob):
    z = np.load(io.BytesIO(blob))
    t0 = datetime.strptime(str(z["t0"]), "%Y%m%d%H")
    out = {}
    for h in range(24):
        out[t0 + timedelta(hours=h)] = {n: tuple(z[f"{n}_{v}"][h] for v in "quv") for n in SURFACES}
    return out


# ------------------------------------------------------------------------------------------------ one issue time
def gfs_surfaces(t):
    try:
        out = {}
        for s in GFS_STEPS_H:
            f = gfs.fetch_step(t, s)
            out[s] = S.surfaces(f["u"], f["v"], f["t"])
        return out
    except Exception as e:                                            # a missing run: no GFS alarm for this time
        log(f"GFS {t:%Y%m%d%H} unavailable: {type(e).__name__}: {str(e)[:120]}")
        return None


def run_issue(t, outdir, H=None):
    H = H if H is not None else H_GLOBAL
    rec, masks = core.issue(H, t, gfs_surfaces(t))
    tag = t.strftime("%Y%m%d%H")
    end = t + timedelta(hours=WINDOW_H)
    os.makedirs(f"{outdir}/issues", exist_ok=True)
    os.makedirs(f"{outdir}/maps", exist_ok=True)
    for name in SURFACES:
        r = rec["surfaces"][name]
        r["jet_axis_end"] = [round(float(x), 1) for x in E.jet_axis(*H.d[end][name][1:])]
        onset_objs = [o for _, o in core.truth_onsets(H, name, t)]
        render.draw(r, name, H.d[end][name][0], H.objs(name, end), onset_objs, masks[name],
                    f"{outdir}/maps/{tag}_{name}.png")
    with open(f"{outdir}/issues/{tag}.json", "w") as fh:
        json.dump(rec, fh, separators=(",", ":"))
    return tag


# ------------------------------------------------------------------------------------------------ summary
def build_summary(records):
    """records: issue records in time order -> summary dict: per issue, surface and method the box counts, the alarm
    regions (longitude extent, confirmed or not) and the onset hits; and the log of onsets with each method's lead."""
    cells, events = {}, {}
    for rec in records:
        t = datetime.strptime(rec["issue"], "%Y%m%d%H")
        cells[rec["issue"]] = {}
        for name, r in rec["surfaces"].items():
            cells[rec["issue"]][name] = {}
            for m in core.METHODS:
                res = r["methods"].get(m)
                cells[rec["issue"]][name][m] = None if res is None else dict(
                    boxes=res["boxes"], hits=[int(h) for h in res["onset_hits"]],
                    regions=[[g["lon0"], g["lon1"], int(g["confirmed"])] for g in res["regions"]],
                    area=res["area_fraction"])
            cells[rec["issue"]][name]["onsets"] = [[o["lon"], o["time"]] for o in r["onsets"]]
            for k, o in enumerate(r["onsets"]):
                key = (name, o["time"], o["lon"], o["lat"], o["type"])
                ev = events.setdefault(key, dict(surface=name, time=o["time"], lon=o["lon"], lat=o["lat"],
                                                 type=o["type"], flank=o["flank"], issue=rec["issue"],
                                                 lead_h={m: None for m in core.METHODS}))
                lead = int((datetime.strptime(o["time"], "%Y%m%d%H") - t).total_seconds() // 3600)
                for m in core.METHODS:
                    res = r["methods"].get(m)
                    if res is not None and res["onset_hits"][k] and (ev["lead_h"][m] is None or lead > ev["lead_h"][m]):
                        ev["lead_h"][m] = lead
    return dict(methods=list(core.METHODS), issues=sorted(cells), cells=cells,
                events=sorted(events.values(), key=lambda e: (e["time"], e["surface"], e["lon"])))


# ------------------------------------------------------------------------------------------------ backfill
def backfill(a, b, era5_dir, outdir, workers):
    global H_GLOBAL
    first = (a - timedelta(hours=OPUS_SPAN_H + 24)).date()
    last = (b + timedelta(hours=WINDOW_H)).date()
    H = core.Hours()
    d = first
    while d <= last:
        path = f"{era5_dir}/era5_{d:%Y%m%d}.nc"
        era5.fetch_day(d, path)
        times, surf = day_surfaces(path)
        for h, tt in enumerate(times):
            H.add(tt, surf[h])
        d += timedelta(days=1)
    log(f"surfaces {first} .. {last}")
    ts = [t for t in core.issue_times(a, b)
          if H.has(t - timedelta(hours=OPUS_SPAN_H + 24), t + timedelta(hours=WINDOW_H))]
    H_GLOBAL = H
    with ProcessPoolExecutor(workers) as ex:                       # fork: workers share the surfaces
        for tag in ex.map(run_issue, ts, [outdir] * len(ts)):
            log(f"issue {tag}")
    os.makedirs(f"{outdir}/cache", exist_ok=True)                 # seed the daily cache with the last days
    for k in range(CACHE_DAYS):
        d = last - timedelta(days=k)
        t0 = datetime(d.year, d.month, d.day)
        times = [t0 + timedelta(hours=h) for h in range(24)]
        with open(f"{outdir}/cache/surf_{d:%Y%m%d}.npz", "wb") as fh:
            fh.write(pack_day(times, {h: H.d[t] for h, t in enumerate(times)}))
    finish(outdir, sorted(f[:-5] for f in os.listdir(f"{outdir}/issues")), f"{last:%Y-%m-%d}")


def finish(outdir, tags, era5_last):
    records = [json.load(open(f"{outdir}/issues/{t}.json")) for t in tags]
    summary = build_summary(records)
    with open(f"{outdir}/summary.json", "w") as fh:
        json.dump(summary, fh, separators=(",", ":"))
    index = dict(updated=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), issues=summary["issues"],
                 surfaces=list(SURFACES), era5_last_day=era5_last, amp_threshold_deg=AMP_THRESHOLD_DEG,
                 amp_fit_last_issue=AMP_FIT_LAST_ISSUE)
    with open(f"{outdir}/index.json", "w") as fh:
        json.dump(index, fh, indent=1)
    log(f"summary: {len(summary['issues'])} issue times, {len(summary['events'])} onsets")


# ------------------------------------------------------------------------------------------------ daily (Actions)
class HFStore:
    """The Hugging Face dataset that holds the results."""

    def __init__(self, repo, tmp):
        from huggingface_hub import HfApi
        self.repo, self.tmp = repo, tmp
        self.api = HfApi(token=os.environ.get("HF_TOKEN"))

    def ls(self):
        return set(self.api.list_repo_files(self.repo, repo_type="dataset"))

    def get(self, f):
        from huggingface_hub import hf_hub_download
        return hf_hub_download(self.repo, f, repo_type="dataset", local_dir=f"{self.tmp}/dl")

    def issues_dir(self):
        from huggingface_hub import snapshot_download
        return snapshot_download(self.repo, repo_type="dataset", allow_patterns=["issues/*.json"],
                                 local_dir=f"{self.tmp}/snap") + "/issues"

    def commit(self, adds, deletes, msg):
        from huggingface_hub import CommitOperationAdd, CommitOperationDelete
        ops = [CommitOperationAdd(r, p) for r, p in adds] + [CommitOperationDelete(r) for r in deletes]
        self.api.create_commit(repo_id=self.repo, repo_type="dataset", operations=ops, commit_message=msg)


class LocalStore:
    """A local folder laid out like the dataset (for testing the daily mode without uploading)."""

    def __init__(self, root):
        self.root = root

    def ls(self):
        return {os.path.relpath(os.path.join(d, f), self.root) for d, _, fs in os.walk(self.root) for f in fs}

    def get(self, f):
        return f"{self.root}/{f}"

    def issues_dir(self):
        return f"{self.root}/issues"

    def commit(self, adds, deletes, msg):
        for r, p in adds:
            os.makedirs(os.path.dirname(f"{self.root}/{r}"), exist_ok=True)
            shutil.copy(p, f"{self.root}/{r}")
        for r in deletes:
            os.remove(f"{self.root}/{r}")
        log(f"local commit: {msg}")


def daily(make_store, era5_dir=None):
    tmp = tempfile.mkdtemp(prefix="rwbp_")
    try:
        store = make_store(tmp)
        files = store.ls()
        index = json.load(open(store.get("index.json")))
        done = set(index["issues"])
        cached = sorted(f for f in files if f.startswith("cache/surf_"))
        H = core.Hours()
        for f in cached:
            for k, v in unpack_day(open(store.get(f), "rb").read()).items():
                H.add(k, v)
        last = datetime.strptime(cached[-1][11:19], "%Y%m%d").date() if cached else None
        new_cache = []
        today = datetime.now(timezone.utc).date()
        d = last + timedelta(days=1)
        while d <= today - timedelta(days=4):
            path = f"{era5_dir or tmp}/era5_{d:%Y%m%d}.nc"
            try:
                era5.fetch_day(d, path)
            except Exception as e:
                if not not_released(e):
                    step_summary([f"ERA5 {d}: request failed ({type(e).__name__}); see the log."])
                    raise
                log(f"ERA5 {d} not available yet: {type(e).__name__}: {str(e)[:120]}")
                step_summary([f"ERA5 {d}: not complete in the Climate Data Store yet ({str(e)[:80]})."])
                break
            times, surf = day_surfaces(path)
            for h, tt in enumerate(times):
                H.add(tt, surf[h])
            local = f"{tmp}/surf_{d:%Y%m%d}.npz"
            with open(local, "wb") as fh:
                fh.write(pack_day(times, surf))
            new_cache.append((f"cache/surf_{d:%Y%m%d}.npz", local))
            if era5_dir is None:
                os.remove(path)
            last = d
            d += timedelta(days=1)
        hours = sorted(H.d)
        ts = [t for t in core.issue_times(hours[0], hours[-1]) if t.strftime("%Y%m%d%H") not in done
              and H.has(t - timedelta(hours=OPUS_SPAN_H + 24), t + timedelta(hours=WINDOW_H))]
        out = f"{tmp}/out"
        tags = [run_issue(t, out, H) for t in ts]
        log(f"processed {len(tags)} issue times")
        step_summary([f"ERA5 days added: {', '.join(n[11:19] for n, _ in new_cache) or 'none'}; "
                      f"issue times scored: {', '.join(tags) or 'none'}."])
        if not tags and not new_cache:
            return
        os.makedirs(f"{out}/issues", exist_ok=True)
        if done:                                                   # older records for the summary
            src = store.issues_dir()
            for t in sorted(done):
                shutil.copy(f"{src}/{t}.json", f"{out}/issues/{t}.json")
        finish(out, sorted(done | set(tags)), f"{last:%Y-%m-%d}")
        adds = [(f"issues/{t}.json", f"{out}/issues/{t}.json") for t in tags]
        adds += [(f"maps/{t}_{n}.png", f"{out}/maps/{t}_{n}.png") for t in tags for n in SURFACES]
        adds += new_cache + [(f, f"{out}/{f}") for f in ("summary.json", "index.json")]
        keep = {f"cache/surf_{last - timedelta(days=k):%Y%m%d}.npz" for k in range(CACHE_DAYS)}
        store.commit(adds, [f for f in cached if f not in keep], f"{len(tags)} issue times through ERA5 day {last}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.environ.get("HF_DATASET", "yanxingjianken/rwb-prediction"))
    ap.add_argument("--backfill", nargs=2, metavar=("FIRST", "LAST"), help="issue times YYYYMMDDHH YYYYMMDDHH")
    ap.add_argument("--era5-dir", default="era5")
    ap.add_argument("--out", default="out")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--local-store", help="daily mode against a local folder instead of the dataset (testing)")
    args = ap.parse_args()
    if args.backfill:
        a, b = (datetime.strptime(x, "%Y%m%d%H") for x in args.backfill)
        backfill(a, b, args.era5_dir, args.out, args.workers)
    elif args.local_store:
        daily(lambda tmp: LocalStore(args.local_store), era5_dir=args.era5_dir)
    else:
        daily(lambda tmp: HFStore(args.repo, tmp))


if __name__ == "__main__":
    main()
