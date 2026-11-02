"""NOAA GFS 1-degree forecasts (pgrb2.1p00) from the NOAA Open Data bucket on AWS: u, v, T on the pipeline's pressure
levels for one run and step, fetched by byte ranges listed in the .idx files."""
from __future__ import annotations

import re
import time
from datetime import datetime

import numpy as np
import requests

from config import LEVELS_HPA

AWS = "https://noaa-gfs-bdp-pds.s3.amazonaws.com"
NAME = {"UGRD": "u", "VGRD": "v", "TMP": "t"}
WANT = re.compile(r":(UGRD|VGRD|TMP):(\d+) mb:")
SESSION = requests.Session()
SESSION.headers["User-Agent"] = "rwb-prediction-pipeline (github.com/yanxingjianken)"


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


def key(init: datetime, step: int) -> str:
    return f"{AWS}/gfs.{init:%Y%m%d}/{init:%H}/atmos/gfs.t{init:%H}z.pgrb2.1p00.f{step:03d}"


def ranges(idx_text: str):
    """[(var, level, start, end_or_None)] of the wanted messages."""
    lines = [l for l in idx_text.splitlines() if l.strip()]
    starts = [int(l.split(":")[1]) for l in lines]
    out = []
    for n, l in enumerate(lines):
        m = WANT.search(l)
        if m and int(m.group(2)) in LEVELS_HPA:
            end = starts[n + 1] - 1 if n + 1 < len(lines) else None
            out.append((NAME[m.group(1)], int(m.group(2)), starts[n], end))
    return out


def fetch_step(init: datetime, step: int) -> dict:
    """{u, v, t: float32 (L, 91, 360)}, latitude ascending 0..90, longitude 0..359, levels in LEVELS_HPA order."""
    import eccodes
    url = key(init, step)
    want = ranges(_get(url + ".idx").decode())
    assert len(want) == 3 * len(LEVELS_HPA), f"{url}: {len(want)} messages"
    out = {v: np.full((len(LEVELS_HPA), 91, 360), np.nan, np.float32) for v in NAME.values()}
    for var, lev, a, b in want:
        rng = f"bytes={a}-" + ("" if b is None else str(b))
        msg = _get(url, headers={"Range": rng})
        h = eccodes.codes_new_from_message(msg)
        try:
            nj, ni = eccodes.codes_get(h, "Nj"), eccodes.codes_get(h, "Ni")
            lat1 = eccodes.codes_get(h, "latitudeOfFirstGridPointInDegrees")
            vals = eccodes.codes_get_values(h).reshape(nj, ni)
        finally:
            eccodes.codes_release(h)
        assert (nj, ni) == (181, 360) and lat1 == 90.0
        out[var][LEVELS_HPA.index(lev)] = vals[:91][::-1]          # rows 90..0 N -> 0..90 N
    assert all(np.isfinite(a).all() for a in out.values())
    return out
