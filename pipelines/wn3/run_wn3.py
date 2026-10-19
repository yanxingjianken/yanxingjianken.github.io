"""Google DeepMind WeatherNext 3 -> encrypted station series and US maps for the WxChallenge page.

Source (no egress charges; readable only by allowlisted Google accounts):
  gs://weathernext3_statistics_spatial/weathernext_3_0_0_statistics/zarr/2026_to_present/<YYYYMMDD_HHhr_01_preds>/predictions.zarr
  Statistics (mean, p10 ... p90) of the 64-member ensemble: 0.1 deg surface variables named <base>_<stat> and
  station-calibrated 2-m temperature and dew point (station_head_*, 0.05 deg).  Dims: lead_time (1 ... 360 h),
  lat_0p1 / lon_0p1 or lat_0p05 / lon_0p05 (latitude ascending, longitude 0-360).  One zstd chunk holds one
  global field for one lead time (about 19 MB at 0.1 deg, 77 MB at 0.05 deg), so every needed lead is read
  in full and cut to a window over the stations and the map area.  Only the 00/06/12/18 UTC runs are used.
  Pressure levels exist only in the requester-pays full-ensemble bucket and are not read.

Licensing.  Forecasts for times less than an hour old or in the future fall under the GDM Real-Time Weather
Forecasting Experimental Data Terms of Use, which allow sharing only with clearly identified people, for
educational purposes, through controlled distribution.  Every data file is therefore encrypted
(AES-256-GCM; key = PBKDF2-HMAC-SHA256 of the team passcode, GitHub secret WN3_PASSCODE) before upload.
The public dataset holds ciphertext, run metadata, the Terms, the required notice file and the copyright
notice.  The passcode never appears in the repository or the dataset.

Published (Hugging Face dataset, default yanxingjianken/nh-forecast-6hourly):
  wn3/index.json                                metadata: run, steps, fields, grid, encryption parameters
  wn3/maps/<RUN>/f<STEP>/<field>sfc.u16.gz.enc  0.1 deg US window, 6-hourly to 240 h (latest run only)
  wn3/stations/<RUN>/s<NNN>.json.gz.enc         hourly series to 48 h for every catalogue station, 128 shards
                                                (last 8 runs kept)
  wn3/TERMS_OF_USE.pdf, wn3/LEGALLY_BINDING_TERMS_OF_USE.txt, wn3/NOTICE.txt

Usage:  GOOGLE_APPLICATION_CREDENTIALS=adc.json WN3_PASSCODE=... HF_TOKEN=... python run_wn3.py
Inspect the newest run:  python run_wn3.py --list
Local test (nothing uploaded):  python run_wn3.py --dry-run --out /tmp/wn3_test --ts-hours 3 --map-steps 6,12 --stations KBOS,KTPA
"""
from __future__ import annotations

import argparse
import base64
import gzip
import json
import os
import re
import shutil
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import numpy as np
import requests
import xarray as xr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "nh_forecast"))
from common import Grid, encode_field  # noqa: E402

GCS_ROOT = "gs://weathernext3_statistics_spatial/weathernext_3_0_0_statistics/zarr/2026_to_present"
STATIONS_JSON = os.path.join(HERE, "..", "..", "assets", "data", "asos_stations.json")
TERMS_URL = "https://storage.googleapis.com/weathernext-public/terms-of-use.pdf"
NOTICE_TEXT = "By using this information, you agree to the Terms of Use found at https://storage.googleapis.com/weathernext-public/terms-of-use.pdf"
COPYRIGHT = "Copyright 2024-6 Google LLC"
MAP_GRID = Grid(lat0=20.0, dlat=0.1, ny=341, lon0=225.0, dlon=0.1, nx=751)   # 20-54 N, 135-60 W
MAP_STEPS = list(range(6, 241, 6))
TS_HOURS = 48
N_SHARDS = 128
KEEP_STATION_RUNS = 8
KDF_ITER = 600_000
N_THREADS = int(os.environ.get("WN3_THREADS", "12"))

# logical name -> (variable name stem in the store, grid)
VARS = {
    "t_st": ("station_head_temperature_2m", "0p05"), "td_st": ("station_head_dewpoint_temperature_2m", "0p05"),
    "t2m": ("temperature_2m", "0p1"), "d2m": ("dewpoint_temperature_2m", "0p1"),
    "u10": ("u_component_of_wind_10m", "0p1"), "v10": ("v_component_of_wind_10m", "0p1"),
    "ws10": ("wind_speed_10m", "0p1"), "u100": ("u_component_of_wind_100m", "0p1"),
    "v100": ("v_component_of_wind_100m", "0p1"), "msl": ("mean_sea_level_pressure", "0p1"),
    "tp": ("total_precipitation_1hr", "0p1"), "tpi": ("imerg_tp_1hr", "0p1"),
    "tcc": ("total_cloud_cover", "0p1"), "lcc": ("low_cloud_cover", "0p1"),
    "mcc": ("medium_cloud_cover", "0p1"), "hcc": ("high_cloud_cover", "0p1"),
}
# map files: stored name -> (logical var, statistic, stored units); tp6/tp6i are sums of six hourly means
MAP_FIELDS = {
    "t2m": ("t2m", "mean", "K"), "d2m": ("d2m", "mean", "K"), "u10": ("u10", "mean", "m s-1"),
    "v10": ("v10", "mean", "m s-1"), "u100": ("u100", "mean", "m s-1"), "v100": ("v100", "mean", "m s-1"),
    "msl": ("msl", "mean", "hPa"), "tcc": ("tcc", "mean", "%"), "lcc": ("lcc", "mean", "%"),
    "mcc": ("mcc", "mean", "%"), "hcc": ("hcc", "mean", "%"),
    "tp6": ("tp", "mean", "mm"), "tp6i": ("tpi", "mean", "mm"),
    "t2msp": ("t2m", "p90-p10", "K"),
}
MAP_INST = {("t2m", "mean"), ("d2m", "mean"), ("u10", "mean"), ("v10", "mean"), ("u100", "mean"), ("v100", "mean"),
            ("msl", "mean"), ("tcc", "mean"), ("lcc", "mean"), ("mcc", "mean"), ("hcc", "mean"), ("t2m", "p10"), ("t2m", "p90")}
SUM6 = {("tp", "mean"), ("tpi", "mean")}


def K2F(k):
    return (k - 273.15) * 1.8 + 32.0


def kt(x):
    return x * 1.94384


def m2in(x):
    return x * 39.3701


# station series: key -> (logical var, statistic, conversion, quantum of the stored integers)
TS_SERIES = {
    "t": ("t_st", "mean", K2F, 0.1), "t10": ("t_st", "p10", K2F, 0.1), "t90": ("t_st", "p90", K2F, 0.1),
    "td": ("td_st", "mean", K2F, 0.1), "td10": ("td_st", "p10", K2F, 0.1), "td90": ("td_st", "p90", K2F, 0.1),
    "ws": ("ws10", "mean", kt, 0.1), "ws10": ("ws10", "p10", kt, 0.1), "ws90": ("ws10", "p90", kt, 0.1),
    "u": ("u10", "mean", None, 0.1), "v": ("v10", "mean", None, 0.1),
    "p": ("tp", "mean", m2in, 0.001), "p90": ("tp", "p90", m2in, 0.001), "pi": ("tpi", "mean", m2in, 0.001),
    "msl": ("msl", "mean", lambda x: x / 100.0, 0.1),
    "tcc": ("tcc", "mean", None, 1), "lcc": ("lcc", "mean", None, 1), "mcc": ("mcc", "mean", None, 1), "hcc": ("hcc", "mean", None, 1),
}
CLOUD = ("tcc", "lcc", "mcc", "hcc")


def log(msg):
    print(f"[{datetime.now(timezone.utc):%H:%M:%S}] {msg}", flush=True)


def shard_of(icao: str) -> int:
    """Same hash as wn3Shard() on the page."""
    h = 0
    for ch in icao:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return h % N_SHARDS


# ----------------------------------------------------------------------------- encryption
def derive_key(passcode: str, salt: bytes) -> bytes:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=KDF_ITER).derive(passcode.encode("utf-8"))


def encrypt(key: bytes, data: bytes) -> bytes:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    nonce = os.urandom(12)
    return nonce + AESGCM(key).encrypt(nonce, data, None)    # nonce | ciphertext | 16-byte tag (WebCrypto layout)


def decrypt(key: bytes, blob: bytes) -> bytes:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    return AESGCM(key).decrypt(blob[:12], blob[12:], None)


# ----------------------------------------------------------------------------- source
class Source:
    def __init__(self, root):
        self.root = root.rstrip("/")
        self.gcs = self.root.startswith("gs://")
        if self.gcs:
            import gcsfs
            self.fs = gcsfs.GCSFileSystem(token="google_default")

    def runs(self):
        names = [p.rstrip("/").split("/")[-1] for p in (self.fs.ls(self.root, detail=False) if self.gcs else os.listdir(self.root))]
        out = {}
        for n in names:
            m = re.match(r"^(\d{8})_(\d{2})hr_(\d+)_preds$", n)
            if not m:
                continue
            init = datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H").replace(tzinfo=timezone.utc)
            if init.hour % 6:
                continue                                   # interim hourly runs (48 h) are not used
            if init not in out or n > out[init]:
                out[init] = n
        return sorted(out.items(), reverse=True)

    def complete(self, name, last_lead=360):
        """The run is complete when the chunk of the last lead exists for a late-written variable."""
        if not self.gcs:
            return True
        p = f"{self.root}/{name}/predictions.zarr/station_head_temperature_2m_p90/c/{last_lead - 1}/0/0"
        return self.fs.exists(p)

    def open(self, name):
        path = f"{self.root}/{name}/predictions.zarr"
        kw = {"storage_options": {"token": "google_default"}} if self.gcs else {}
        return xr.open_zarr(path, chunks=None, **kw)


def dims(da):
    lat = next(d for d in da.dims if d.startswith("lat"))
    lon = next(d for d in da.dims if d.startswith("lon"))
    lead = next(d for d in da.dims if "lead" in d)
    return lat, lon, lead


class Window:
    """Index window of one source grid that covers every station and the map grid, with interpolation weights."""

    def __init__(self, da, st_lat, st_lon360, mg):
        lat, lon, _ = dims(da)
        la = np.asarray(da[lat].values, dtype=float)
        lo = np.asarray(da[lon].values, dtype=float) % 360.0
        if la[0] > la[-1]:
            raise RuntimeError("expected ascending latitude")
        lat_lo = min(st_lat.min(), mg.lat0) - 0.5
        lat_hi = max(st_lat.max(), mg.lat0 + mg.dlat * (mg.ny - 1)) + 0.5
        lon_lo = min(st_lon360.min(), mg.lon0) - 0.5
        lon_hi = max(st_lon360.max(), mg.lon0 + mg.dlon * (mg.nx - 1)) + 0.5
        jj = np.where((la >= lat_lo) & (la <= lat_hi))[0]
        ii = np.where((lo >= lon_lo) & (lo <= lon_hi))[0]
        self.j0, self.j1 = int(jj.min()), int(jj.max()) + 1
        self.i0, self.i1 = int(ii.min()), int(ii.max()) + 1
        self.lat, self.lon = la[self.j0:self.j1], lo[self.i0:self.i1]
        self.st = (self._axis(self.lat, st_lat), self._axis(self.lon, st_lon360))
        self.mj, self.mi = self._axis(self.lat, mg.lats), self._axis(self.lon, mg.lons % 360.0)

    @staticmethod
    def _axis(src, tgt):
        f = np.interp(tgt, src, np.arange(len(src)), left=np.nan, right=np.nan)
        ok = np.isfinite(f)
        i0 = np.clip(np.floor(np.where(ok, f, 0.0)).astype(int), 0, len(src) - 2)
        w = np.where(ok, f - i0, np.nan)
        return i0, w

    def read(self, da, k):
        lat, lon, lead = dims(da)
        return da.isel({lead: k, lat: slice(self.j0, self.j1), lon: slice(self.i0, self.i1)}).values.astype(np.float32)

    def at_stations(self, a):
        (j0, wj), (i0, wi) = self.st
        return (1 - wj) * ((1 - wi) * a[j0, i0] + wi * a[j0, i0 + 1]) + wj * ((1 - wi) * a[j0 + 1, i0] + wi * a[j0 + 1, i0 + 1])

    def on_map(self, a):
        (j0, wj), (i0, wi) = self.mj, self.mi
        r0 = a[j0][:, i0] * (1 - wi) + a[j0][:, i0 + 1] * wi
        r1 = a[j0 + 1][:, i0] * (1 - wi) + a[j0 + 1][:, i0 + 1] * wi
        return r0 * (1 - wj)[:, None] + r1 * wj[:, None]


# ----------------------------------------------------------------------------- processing
def process(src, name, init, args, key, tmp, stations):
    t_start = time.time()
    ds = src.open(name)

    def da_of(logical, stat):
        n = f"{VARS[logical][0]}_{stat}"
        if n not in ds.data_vars:
            raise KeyError(f"{n} not in store")
        return ds[n]

    lead_index = {float(h): k for k, h in enumerate((ds["lead_time"].values / np.timedelta64(1, "h")).astype(float))}
    if max(lead_index) < max(args.map_steps):
        raise RuntimeError(f"run {name} has leads only to {max(lead_index):.0f} h")
    ts_hours = list(range(1, args.ts_hours + 1))
    ns = len(stations["icao"])

    # what to read: (logical, stat) -> sorted lead hours
    need = {}
    for logical, stat, _f, _q in TS_SERIES.values():
        need.setdefault((logical, stat), set()).update(ts_hours)
    for ls in MAP_INST:
        need.setdefault(ls, set()).update(args.map_steps)
    for ls in SUM6:
        need.setdefault(ls, set()).update(range(1, max(args.map_steps) + 1))
    tasks = [(ls, h) for ls, hs in sorted(need.items()) for h in sorted(hs) if float(h) in lead_index]
    log(f"  {len(tasks)} fields to read ({sum(1 for (l, _s), _h in tasks if VARS[l][1] == '0p05')} at 0.05 deg)")

    wins = {}
    for g, probe in (("0p1", ("t2m", "mean")), ("0p05", ("t_st", "mean"))):
        wins[g] = Window(da_of(*probe), stations["lat"], stations["lon360"], MAP_GRID)
    series = {ls: np.full((ns, args.ts_hours), np.nan, np.float32) for ls in {(v[0], v[1]) for v in TS_SERIES.values()}}
    maps = {s: {} for s in args.map_steps}
    acc, lock = {}, threading.Lock()
    done = [0]

    def work(task):
        (logical, stat), h = task
        win = wins[VARS[logical][1]]
        a = win.read(da_of(logical, stat), lead_index[float(h)])
        if (logical, stat) in series and h <= args.ts_hours:
            series[(logical, stat)][:, h - 1] = win.at_stations(a)
        if (logical, stat) in MAP_INST and h in maps:
            maps[h][(logical, stat)] = win.on_map(a)
        if (logical, stat) in SUM6:
            s = int(np.ceil(h / 6.0) * 6)
            if s in maps:
                m = win.on_map(a)
                with lock:
                    acc[(logical, s)] = m if (logical, s) not in acc else acc[(logical, s)] + m
        with lock:
            done[0] += 1
            if done[0] % 100 == 0:
                el = time.time() - t_start
                log(f"  {done[0]}/{len(tasks)} fields read ({el / 60:.1f} min)")

    with ThreadPoolExecutor(N_THREADS) as ex:
        list(ex.map(work, tasks))
    log(f"  read done in {(time.time() - t_start) / 60:.1f} min")

    # station-calibrated temperature and dew point where available, otherwise the 0.1 deg field
    for st_v, grid_v in (("t_st", "t2m"), ("td_st", "d2m")):
        for stat in ("mean", "p10", "p90"):
            a, b = series.get((st_v, stat)), series.get((grid_v, stat))
            if a is not None and b is not None:
                bad = ~np.isfinite(a).all(axis=1)
                a[bad] = b[bad]

    run_id = init.strftime("%Y%m%d%H")
    out = os.path.join(tmp, "publish")

    # ---- maps ----------------------------------------------------------------------
    fields_list = []
    for s in args.map_steps:
        valid = init + timedelta(hours=s)
        hdr = {"model": "wn3", "init": init.strftime("%Y-%m-%dT%H:00Z"), "valid": valid.strftime("%Y-%m-%dT%H:00Z"), "step": s}
        d = os.path.join(out, "wn3", "maps", run_id, f"f{s:03d}")
        os.makedirs(d, exist_ok=True)
        raw = maps[s]
        for fname, (logical, stat, units) in MAP_FIELDS.items():
            if fname == "t2msp":
                p10, p90 = raw.get(("t2m", "p10")), raw.get(("t2m", "p90"))
                arr = None if p10 is None or p90 is None else p90 - p10
            elif fname in ("tp6", "tp6i"):
                arr = acc.get((logical, s))
                arr = None if arr is None else np.maximum(arr, 0) * 1000.0                 # m -> mm
            else:
                arr = raw.get((logical, stat))
                if arr is not None and fname == "msl":
                    arr = arr / 100.0
                if arr is not None and fname in CLOUD and np.nanmax(arr) <= 1.5:
                    arr = arr * 100.0
            if arr is None:
                continue
            h = dict(hdr, var=fname, level="sfc", units=units, lat0=MAP_GRID.lat0, dlat=MAP_GRID.dlat, lon0=MAP_GRID.lon0, dlon=MAP_GRID.dlon)
            with open(os.path.join(d, f"{fname}sfc.u16.gz.enc"), "wb") as f:
                f.write(encrypt(key, encode_field(arr.astype(np.float64), h)))
            if f"{fname}sfc" not in fields_list:
                fields_list.append(f"{fname}sfc")

    # ---- station shards ---------------------------------------------------------------
    st_root = os.path.join(out, "wn3", "stations", run_id)
    os.makedirs(st_root, exist_ok=True)
    conv = {}
    for k, (logical, stat, fn, qnt) in TS_SERIES.items():
        a = series[(logical, stat)]
        a = fn(a) if fn else a
        if k in CLOUD and np.nanmax(a) <= 1.5:
            a = a * 100.0
        if k in ("p", "p90", "pi"):
            a = np.maximum(a, 0)
        conv[k] = (a, qnt)
    u, v = conv.pop("u")[0], conv.pop("v")[0]
    conv["wd"] = ((270.0 - np.degrees(np.arctan2(v, u))) % 360.0, 1)
    shards = {}
    for n, icao in enumerate(stations["icao"]):
        rec = {"lat": round(float(stations["lat"][n]), 4), "lon": round(float(stations["lon"][n]), 4)}
        for k, (a, q) in conv.items():
            rec[k] = [None if not np.isfinite(x) else int(round(x / q)) for x in a[n]]
        shards.setdefault(shard_of(icao), {})[icao] = rec
    for sh, recs in shards.items():
        obj = {"model": "wn3", "run": run_id, "init": init.strftime("%Y-%m-%dT%H:00Z"),
               "t0": (init + timedelta(hours=1)).strftime("%Y-%m-%dT%H:00Z"), "dt_h": 1, "n": args.ts_hours,
               "quantum": {k: q for k, (_a, q) in conv.items()},
               "units": {"t": "degF", "td": "degF", "ws": "kt", "wd": "deg", "p": "in", "pi": "in", "msl": "hPa", "tcc": "%"},
               "stations": recs}
        with open(os.path.join(st_root, f"s{sh:03d}.json.gz.enc"), "wb") as f:
            f.write(encrypt(key, gzip.compress(json.dumps(obj, separators=(",", ":")).encode(), 9)))
    log(f"wn3: run {run_id} prepared in {(time.time() - t_start) / 60:.1f} min")
    return {"out": out, "run_id": run_id, "init": init, "fields": fields_list}


def write_legal(out):
    d = os.path.join(out, "wn3")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "LEGALLY_BINDING_TERMS_OF_USE.txt"), "w") as f:
        f.write(NOTICE_TEXT + "\n")
    with open(os.path.join(d, "NOTICE.txt"), "w") as f:
        f.write(COPYRIGHT + "\n\n"
                "WeatherNext 3 experimental forecasts (Google DeepMind): statistics of the 64-member ensemble, read from\n"
                "gs://weathernext3_statistics_spatial (Google Cloud Storage).\n\n"
                "Modifications made here: bilinear interpolation to US airport stations and to a 0.1 degree latitude-longitude\n"
                "window (20-54 N, 135-60 W); unit conversion; quantisation to 16-bit or fixed-step integers; 6-h precipitation\n"
                "as the sum of six hourly ensemble-mean amounts; 2-m temperature spread as the 90th minus the 10th percentile;\n"
                "wind direction from the ensemble-mean wind components; station-calibrated 2-m temperature and dew point\n"
                "replaced by the 0.1 degree field where unavailable.  The files are encrypted for controlled distribution to\n"
                "named members of the MIT WxChallenge team, for educational use only; do not share them further.\n\n"
                "This data is intended for experimental modelling only and is not intended, validated, or approved for real\n"
                "world use.  It is not an official forecast and does not replace official alerts, warnings or notices.\n")
    try:
        r = requests.get(TERMS_URL, timeout=60)
        if r.ok and r.content[:4] == b"%PDF":
            with open(os.path.join(d, "TERMS_OF_USE.pdf"), "wb") as f:
                f.write(r.content)
    except requests.RequestException:
        pass


def load_stations(only=None):
    cat = json.load(open(STATIONS_JSON))["stations"]
    if only:
        cat = [s for s in cat if s["icao"] in only]
    lat = np.array([s["lat"] for s in cat], float)
    lon = np.array([s["lon"] for s in cat], float)
    return {"icao": [s["icao"] for s in cat], "lat": lat, "lon": lon, "lon360": lon % 360.0}


def hf_index(repo):
    try:
        r = requests.get(f"https://huggingface.co/datasets/{repo}/resolve/main/wn3/index.json", headers={"Cache-Control": "no-cache"}, timeout=60)
        if r.status_code == 200:
            return r.json()
    except requests.RequestException:
        pass
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.environ.get("HF_DATASET", "yanxingjianken/nh-forecast-6hourly"))
    ap.add_argument("--source", default=GCS_ROOT)
    ap.add_argument("--run", help="force run YYYYMMDDHH")
    ap.add_argument("--ts-hours", type=int, default=TS_HOURS)
    ap.add_argument("--map-steps", default=",".join(map(str, MAP_STEPS)))
    ap.add_argument("--stations", help="comma-separated ICAO subset (testing)")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--list", action="store_true", help="list runs and the variables of the newest one, then exit")
    args = ap.parse_args()
    args.map_steps = [int(s) for s in args.map_steps.split(",") if s]

    src = Source(args.source)
    runs = src.runs()
    if not runs:
        raise SystemExit(f"no 6-hourly runs under {args.source}")
    if args.list:
        for init, name in runs[:8]:
            print(init.strftime("%Y-%m-%d %HZ"), name, "complete" if src.complete(name) else "incomplete")
        ds = src.open(runs[0][1])
        print(ds.sizes)
        for n, da in ds.data_vars.items():
            print(f"{n:56s} {da.dims} chunks={da.encoding.get('chunks')}")
        return
    passcode = os.environ.get("WN3_PASSCODE")
    if not passcode:
        raise SystemExit("WN3_PASSCODE is not set")
    index = None if args.dry_run else hf_index(args.repo)
    enc = (index or {}).get("enc") or {}
    salt = base64.b64decode(enc["salt"]) if enc.get("salt") else os.urandom(16)
    key = derive_key(passcode, salt)
    kept_before = (index or {}).get("ts", {}).get("runs", [])
    if enc.get("check"):
        try:
            decrypt(key, base64.b64decode(enc["check"]))
        except Exception:
            log("passcode changed: new salt; older station runs are dropped because they cannot be read with the new key")
            salt = os.urandom(16)
            key = derive_key(passcode, salt)
            kept_before = []
            args.force = True
    if args.run:
        want = datetime.strptime(args.run, "%Y%m%d%H").replace(tzinfo=timezone.utc)
        runs = [r for r in runs if r[0] == want]
    stations = load_stations(set(args.stations.split(",")) if args.stations else None)
    tmp = args.out if (args.dry_run and args.out) else tempfile.mkdtemp(prefix="wn3_")
    try:
        res = None
        for init, name in runs[:3]:
            rid = init.strftime("%Y%m%d%H")
            if not args.force and index and index.get("latest_run") == rid:
                log(f"wn3: run {rid} already published; nothing to do")
                return
            if not args.force and index and index.get("latest_run", "") > rid:
                log(f"wn3: run {rid} older than the published {index['latest_run']}; nothing to do")
                return
            if not src.complete(name):
                log(f"wn3: run {rid} not complete yet")
                continue
            log(f"wn3: run {rid} ({name})")
            res = process(src, name, init, args, key, tmp, stations)
            break
        if res is None:
            log("wn3: no complete new run")
            return
        write_legal(res["out"])
        rid = res["run_id"]
        kept = sorted({rid, *kept_before}, reverse=True)[:KEEP_STATION_RUNS]
        idx = {"label": "WeatherNext 3", "source": "Google DeepMind WeatherNext 3, statistics of the 64-member ensemble (Google Cloud Storage)",
               "latest_run": rid, "init": res["init"].strftime("%Y-%m-%dT%H:00Z"), "steps": args.map_steps, "fields": res["fields"],
               "grids": {"reg": MAP_GRID.__dict__}, "domain": "regional", "mapdir": f"wn3/maps/{rid}", "enc_files": True,
               "grid_note": "WeatherNext 3 0.1° ensemble statistics (the ensemble mean unless stated), interpolated bilinearly to this 0.1° latitude–longitude window",
               "ts": {"runs": kept, "hours": args.ts_hours, "shards": N_SHARDS, "path": "wn3/stations/{run}/s{shard}.json.gz.enc"},
               "enc": {"alg": "AES-256-GCM", "kdf": "PBKDF2-HMAC-SHA256", "iter": KDF_ITER, "salt": base64.b64encode(salt).decode(),
                       "check": base64.b64encode(encrypt(key, b"WN3-OK")).decode(), "layout": "nonce(12) | ciphertext | tag(16)"},
               "legal": {"terms": "wn3/TERMS_OF_USE.pdf", "notice": "wn3/LEGALLY_BINDING_TERMS_OF_USE.txt", "readme": "wn3/NOTICE.txt",
                         "copyright": COPYRIGHT, "terms_url": TERMS_URL},
               "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
        with open(os.path.join(res["out"], "wn3", "index.json"), "w") as f:
            json.dump(idx, f, separators=(",", ":"))
        size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(res["out"]) for f in fs)
        log(f"wn3: {size / 1e6:.1f} MB to upload")
        if args.dry_run:
            return
        from huggingface_hub import CommitOperationAdd, CommitOperationDelete, HfApi
        api = HfApi(token=os.environ["HF_TOKEN"])
        existing = api.list_repo_files(args.repo, repo_type="dataset")
        ops = [CommitOperationAdd(path_in_repo=os.path.relpath(os.path.join(dp, f), res["out"]), path_or_fileobj=os.path.join(dp, f))
               for dp, _, fs in os.walk(res["out"]) for f in fs]
        for r in {p.split("/")[2] for p in existing if p.startswith("wn3/maps/")} - {rid}:
            ops.append(CommitOperationDelete(path_in_repo=f"wn3/maps/{r}/", is_folder=True))
        for r in {p.split("/")[2] for p in existing if p.startswith("wn3/stations/")} - set(kept):
            ops.append(CommitOperationDelete(path_in_repo=f"wn3/stations/{r}/", is_folder=True))
        api.create_commit(repo_id=args.repo, repo_type="dataset", operations=ops,
                          commit_message=f"WN3 {rid}: encrypted team files ({len(res['fields'])} map fields, {len(args.map_steps)} steps)")
        log(f"wn3: published {rid}")
    finally:
        if not (args.dry_run and args.out):
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
