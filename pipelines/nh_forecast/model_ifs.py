"""ECMWF IFS 0.25 deg medium-range control (open data, CC-BY-4.0): pressure-level
fields via byte ranges from the .index files on the AWS mirror (data.ecmwf.int
fallback).  The 00/12 UTC cycles run to 360 h (3-h steps to 144 h, then 6-h);
the 06/18 UTC cycles stop at 144 h.  Data appear ~6.5-7.5 h after init.
Attribution: 'Contains modified ECMWF open data (IFS), CC BY 4.0'."""
from __future__ import annotations

import concurrent.futures as cf
import json
import os
import time
from datetime import datetime, timedelta, timezone

import requests

from gribio import check_fields, read_fields

MODEL_ID = "ifs"
LABEL = "IFS 0.25° (ECMWF)"
SOURCE = "ECMWF open data, IFS 0.25 deg medium-range control (CC BY 4.0)"
STEP_HOURS = 6
MAX_STEP = 240
ROOTS = ["https://ecmwf-forecasts.s3.eu-central-1.amazonaws.com", "https://data.ecmwf.int/forecasts"]
PARAMS = {"gh", "t", "u", "v", "w", "q"}
LEVELS = {"850", "500", "250"}
SFC_PARAMS = {"2t", "2d", "10u", "10v", "msl", "tp"}
TP_TO_MM = 1.0          # tp is converted to mm when decoded (gribio.read_fields); accumulated from the run start
SESSION = requests.Session()
SESSION.headers["User-Agent"] = "nh-forecast-pipeline (github.com/yanxingjianken)"


def run_id(dt: datetime) -> str:
    return dt.strftime("%Y%m%d%H")


def _path(init: datetime, step: int) -> str:
    return f"{init:%Y%m%d}/{init:%H}z/ifs/0p25/oper/{init:%Y%m%d%H}0000-{step}h-oper-fc"


def _get(url, headers=None, tries=4, timeout=120):
    last = None
    for k in range(tries):
        try:
            r = SESSION.get(url, headers=headers, timeout=timeout)
            if r.status_code in (200, 206):
                return r.content
            last = RuntimeError(f"HTTP {r.status_code} for {url}")
        except requests.RequestException as e:
            last = e
        time.sleep(2 * (k + 1))
    raise last


def last_step(init: datetime, max_step: int = MAX_STEP) -> int:
    """Last forecast hour available for this cycle (06/18 UTC cycles end at 144 h)."""
    return min(max_step, 144) if init.hour in (6, 18) else max_step


def latest_complete_run(now=None, max_step=MAX_STEP, lookback_runs=6) -> datetime:
    now = now or datetime.now(timezone.utc)
    cand = now.replace(minute=0, second=0, microsecond=0)
    cand = cand.replace(hour=(cand.hour // 6) * 6)
    for _ in range(lookback_runs):
        for root in ROOTS:
            try:
                r = SESSION.head(f"{root}/{_path(cand, last_step(cand, max_step))}.index", timeout=30)
                if r.status_code == 200:
                    return cand
            except requests.RequestException:
                pass
        cand -= timedelta(hours=6)
    raise RuntimeError("no complete IFS run found in the look-back window")


def fetch_fields(init: datetime, step: int, cache_dir: str | None = None) -> dict:
    path = None
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        path = os.path.join(cache_dir, f"ifs.{run_id(init)}.f{step:03d}.grib2")
        if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
            with open(path, "rb") as f:
                return _check(read_fields(f.read()))
    last = None
    for root in ROOTS:
        try:
            base = f"{root}/{_path(init, step)}"
            idx = _get(base + ".index").decode("utf-8", "replace").splitlines()
            recs = [json.loads(l) for l in idx if l.strip()]
            want = [r for r in recs if r.get("levtype") == "pl" and r.get("param") in PARAMS and str(r.get("levelist")) in LEVELS]
            if len(want) != 18:
                raise RuntimeError(f"expected 18 index records, found {len(want)}")
            want += [r for r in recs if r.get("levtype") == "sfc" and r.get("param") in SFC_PARAMS]

            def one(r):
                s, e = r["_offset"], r["_offset"] + r["_length"] - 1
                blob = _get(base + ".grib2", headers={"Range": f"bytes={s}-{e}"})
                if len(blob) != r["_length"]:
                    raise RuntimeError("short range read")
                return blob

            with cf.ThreadPoolExecutor(max_workers=6) as ex:
                data = b"".join(ex.map(one, want))
            fields = _check(read_fields(data))
            if path:
                with open(path, "wb") as f:
                    f.write(data)
            return fields
        except Exception as e:
            last = e
            print(f"  IFS fetch from {root} failed: {e}", flush=True)
    raise last


def _check(fields):
    return check_fields(fields)
