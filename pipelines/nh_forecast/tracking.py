"""Quick cyclone / anticyclone detection and tracking on 500-hPa height.

Two detection bases are produced for every run:

  "anom"  (default in the viewer): extrema of the Gaussian-smoothed anomaly
          Z' = Z500 - daily climatology (NCEP/NCAR R1, 1991-2020).  This is the
          usual choice in the literature (Liu et al.; TRACK-style filtered
          fields) because raw-Z500 minima pile up in the polar-vortex core and
          the strong meridional gradient hides mobile systems.
  "total": extrema of the smoothed total Z500 (closed lows / highs proxy).

Detection (per 6-h time, 0.5-degree NH grid, 20-85N):
  * candidates: local minima (lows) / maxima (highs) of the smoothed field F
    within a neighbourhood of radius R_nbr (lows 1000 km, highs 1200 km);
  * amplitude: |F| >= amp_min on the anomaly basis (lows -60 m, highs +80 m);
  * depth: mean(F on the 0.75-1.25 R ring) - F(centre) >= depth_min
    (sign flipped for highs); 30 m on the anomaly basis, 40 m on the total;
  * merge candidates closer than merge_km (lows 700, highs 900), keeping the
    most extreme one.

Linking (t -> t+6 h): first guess = last position + last displacement; accept
a candidate if it lies within 500 km of the first guess and within D_max of the
last position (D_max: lows 700 km, highs 500 km per 6 h); greedy assignment by
distance; unmatched candidates start new tracks.  Tracks that end before the
last time of the series are dropped when shorter than 24 h (lows) / 48 h
(highs); tracks still alive at the end are kept whatever their length.

Every point stores lat, lon, Z, anomaly, depth, time, source (anl/fcst) and the
cumulative zonal / meridional displacement (km, path-integrated on the
mid-latitude of each 6-h leg), the path length, and the unwrapped longitude.
"""
from __future__ import annotations

from datetime import datetime

import numpy as np
from scipy import ndimage

from common import haversine_km, zonal_meridional_km

PARAMS = {
    "anom": {"sigma": 3.0, "L": {"radius_km": 1000, "amp_min": 60, "depth_min": 30, "merge_km": 700, "dmax_km": 700},
             "H": {"radius_km": 1200, "amp_min": 80, "depth_min": 30, "merge_km": 900, "dmax_km": 500}},
    "total": {"sigma": 2.0, "L": {"radius_km": 800, "amp_min": 0, "depth_min": 40, "merge_km": 700, "dmax_km": 700},
              "H": {"radius_km": 1000, "amp_min": 0, "depth_min": 40, "merge_km": 900, "dmax_km": 500}},
}
SEARCH_KM = 500.0          # radius around the first-guess position
MIN_LIFE = {"L": 4, "H": 8}  # steps (24 h / 48 h) for tracks that have ended
LAT_MIN, LAT_MAX = 20.0, 85.0


def smooth(field: np.ndarray, sigma: float) -> np.ndarray:
    return ndimage.gaussian_filter(field, sigma=(sigma, sigma), mode=("nearest", "wrap"))


def _ring_mean(field, lats, lons, j, i, r_in, r_out):
    ny, nx = field.shape
    dlat = float(lats[1] - lats[0]); dlon = float(lons[1] - lons[0])
    dj = int(np.ceil(r_out / 111.0 / dlat)) + 1
    j0, j1 = max(0, j - dj), min(ny, j + dj + 1)
    cosl = max(np.cos(np.radians(lats[j])), 0.05)
    di = min(int(np.ceil(r_out / (111.0 * cosl) / dlon)) + 1, nx // 2)
    ii = np.arange(i - di, i + di + 1) % nx
    sub = field[j0:j1][:, ii]
    d = haversine_km(lats[j], lons[i], lats[j0:j1][:, None], lons[ii][None, :])
    m = (d >= r_in) & (d <= r_out)
    return float(sub[m].mean()) if m.any() else np.nan


def _merge(cands, merge_km, kind):
    """Drop candidates within merge_km of a stronger one."""
    key = (lambda c: c["score"]) if kind == "L" else (lambda c: -c["score"])
    cands = sorted(cands, key=key)              # most extreme first
    kept = []
    for c in cands:
        if all(haversine_km(c["lat"], c["lon"], k["lat"], k["lon"]) > merge_km for k in kept):
            kept.append(c)
    return kept


def detect_centres(z_total, z_anom, lats, lons, basis="anom"):
    P = PARAMS[basis]
    base = z_anom if basis == "anom" else z_total
    if base is None:
        raise ValueError("anomaly basis requested but no anomaly field given")
    f = smooth(base, P["sigma"])
    dlat = float(lats[1] - lats[0])
    out = {}
    for kind in ("L", "H"):
        p = P[kind]
        win = int(round(p["radius_km"] / 111.0 / dlat)) * 2 + 1
        fp = np.ones((win, min(2 * win + 1, len(lons))), bool)
        ext = (ndimage.minimum_filter if kind == "L" else ndimage.maximum_filter)(f, footprint=fp, mode=("nearest", "wrap"))
        jj, ii = np.where((f == ext) & (lats[:, None] >= LAT_MIN) & (lats[:, None] <= LAT_MAX))
        cands = []
        for j, i in zip(jj, ii):
            val = float(f[j, i])
            if basis == "anom" and ((kind == "L" and val > -p["amp_min"]) or (kind == "H" and val < p["amp_min"])):
                continue
            rm = _ring_mean(f, lats, lons, j, i, 0.75 * p["radius_km"], 1.25 * p["radius_km"])
            if not np.isfinite(rm):
                continue
            depth = (rm - val) if kind == "L" else (val - rm)
            if depth < p["depth_min"]:
                continue
            cands.append({"lat": round(float(lats[j]), 2), "lon": round(float(lons[i]), 2),
                          "z": round(float(z_total[j, i]), 1),
                          "anom": (round(float(z_anom[j, i]), 1) if z_anom is not None else None),
                          "depth": round(float(depth), 1), "score": val})
        out[kind] = [{k: v for k, v in c.items() if k != "score"} for c in _merge(cands, p["merge_km"], kind)]
    return out["L"], out["H"]


class Tracker:
    def __init__(self, params):
        self.P = params
        self.tracks = []
        self._n = {"L": 0, "H": 0}

    @staticmethod
    def _guess(tr):
        p = tr["points"]
        if len(p) >= 2:
            a, b = p[-2], p[-1]
            dlon = ((b["lon"] - a["lon"] + 180) % 360) - 180
            return b["lat"] + (b["lat"] - a["lat"]), (b["lon"] + dlon) % 360
        return p[-1]["lat"], p[-1]["lon"]

    def step(self, kind, cands, t, source):
        dmax = self.P[kind]["dmax_km"]
        active = [tr for tr in self.tracks if tr["kind"] == kind and not tr["ended"]]
        pairs = []
        for ti, tr in enumerate(active):
            glat, glon = self._guess(tr)
            last = tr["points"][-1]
            for ci, c in enumerate(cands):
                d_last = float(haversine_km(last["lat"], last["lon"], c["lat"], c["lon"]))
                d_guess = float(haversine_km(glat, glon, c["lat"], c["lon"]))
                if d_last <= dmax and (len(tr["points"]) < 2 or d_guess <= SEARCH_KM):
                    pairs.append((d_guess if len(tr["points"]) >= 2 else d_last, ti, ci))
        pairs.sort()
        used_t, used_c = set(), set()
        for d, ti, ci in pairs:
            if ti in used_t or ci in used_c:
                continue
            used_t.add(ti); used_c.add(ci)
            self._append(active[ti], cands[ci], t, source)
        for ti, tr in enumerate(active):
            if ti not in used_t:
                tr["ended"] = True
        for ci, c in enumerate(cands):
            if ci not in used_c:
                self._n[kind] += 1
                tr = {"id": f"{kind}{self._n[kind]:02d}", "kind": kind, "points": [], "ended": False}
                self._append(tr, c, t, source)
                self.tracks.append(tr)

    @staticmethod
    def _append(tr, c, t, source):
        pt = dict(c)
        pt["t"] = t.strftime("%Y-%m-%dT%H:00Z")
        pt["src"] = source
        if tr["points"]:
            prev = tr["points"][-1]
            dx, dy = zonal_meridional_km(prev["lat"], prev["lon"], c["lat"], c["lon"])
            dlon = ((c["lon"] - prev["lon"] + 180) % 360) - 180
            pt["dx"] = round(prev["dx"] + dx, 1)
            pt["dy"] = round(prev["dy"] + dy, 1)
            pt["dist"] = round(prev["dist"] + float(haversine_km(prev["lat"], prev["lon"], c["lat"], c["lon"])), 1)
            pt["lon_u"] = round(prev["lon_u"] + dlon, 2)      # unwrapped longitude
        else:
            pt["dx"] = 0.0; pt["dy"] = 0.0; pt["dist"] = 0.0; pt["lon_u"] = c["lon"]
        tr["points"].append(pt)


def track_series(times, z_total_series, z_anom_series, lats, lons, basis="anom", n_analysis=0):
    trk = Tracker(PARAMS[basis])
    for k, t in enumerate(times):
        src = "anl" if k < n_analysis else "fcst"
        za = z_anom_series[k] if z_anom_series is not None else None
        L, H = detect_centres(z_total_series[k], za, lats, lons, basis=basis)
        trk.step("L", L, t, src)
        trk.step("H", H, t, src)
    t_end = times[-1].strftime("%Y-%m-%dT%H:00Z")
    tracks = []
    for tr in trk.tracks:
        pts = tr["points"]
        alive = pts[-1]["t"] == t_end
        if not alive and len(pts) < MIN_LIFE[tr["kind"]]:
            continue
        tracks.append({"id": tr["id"], "kind": tr["kind"], "n": len(pts), "start": pts[0]["t"],
                       "end": pts[-1]["t"], "alive": alive, "points": pts})
    tracks.sort(key=lambda tr: (-tr["n"], tr["id"]))
    return tracks
