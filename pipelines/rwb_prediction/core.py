"""One issue time: the analysis onsets of the next 24 h, each method's alarm regions, and their scores.

Scores per method and surface:
  onsets   an onset is a hit when an alarm region lies within MATCH_ALARM_KM of it, otherwise a miss;
  regions  an alarm region (8-connected, periodic in longitude) is confirmed when an onset lies within MATCH_ALARM_KM
           of it, otherwise it is a false alarm;
  boxes    equal-area boxes of about BOX_DEG (10-90 N): a box is observed when an onset lies in it and alarmed when
           an alarm region covers part of it -> hits, misses, false alarms, correct no, and the false positive rate.
"""
from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
from scipy.ndimage import label as nd_label

import events as E
import predictors as PR
from config import (AMP_SURFACE, AMP_THRESHOLD_DEG, BOX_DEG, EVENT_STEP_H, GFS_STEPS_H, MATCH_ALARM_KM, OPUS_SPAN_H,
                    OPUS_SURFACE, SURFACES, WINDOW_H)

METHODS = ("uc", "opus", "amp", "gfs")


def _boxes():
    """Box index of every grid point (-1 outside 10-90 N) and the number of boxes."""
    edges = list(np.arange(10.0, 90.0, BOX_DEG)) + [90.0]
    ids = np.full(PR.LA.shape, -1, int)
    n = 0
    for a, b in zip(edges[:-1], edges[1:]):
        k = max(1, int(round(360.0 * np.cos(np.deg2rad(0.5 * (a + b))) / BOX_DEG)))
        rows = (PR.LA >= a) & (PR.LA < b) if b < 90 else (PR.LA >= a)
        ids[rows] = n + (PR.LO[rows] // (360.0 / k)).astype(int)
        n += k
    return ids, n


BOX_ID, N_BOX = _boxes()


class Hours:
    """Hourly surface fields {datetime: {surface: (q, u, v)}} filled by the caller (ERA5)."""

    def __init__(self):
        self.d = {}
        self.objects = {}

    def add(self, when, surf):
        self.d[when] = surf

    def has(self, a, b):
        t = a
        while t <= b:
            if t not in self.d:
                return False
            t += timedelta(hours=1)
        return True

    def stack(self, name, a, b):
        ts = []
        t = a
        while t <= b:
            ts.append(self.d[t][name])
            t += timedelta(hours=1)
        return tuple(np.array([x[k] for x in ts]) for k in range(3))

    def objs(self, name, when):
        key = (name, when)
        if key not in self.objects:
            self.objects[key] = E.objects(*self.d[when][name], name)
        return self.objects[key]


def lean(o):
    return {k: v for k, v in o.items() if k != "folds"}


def truth_onsets(H, name, t):
    """Analysis onsets with onset time in (t, t + WINDOW_H]; needs fields from t - 12 h on."""
    times = [t + timedelta(hours=h) for h in range(-12, WINDOW_H + 1, EVENT_STEP_H)]
    seq = [(w, H.objs(name, w)) for w in times]
    return [(w, o) for w, o in E.onsets(seq) if w > t]


def regions(mask):
    """Connected alarm regions (8-connectivity, periodic in longitude): label array (0 = none) and count."""
    lab, n = nd_label(mask, structure=np.ones((3, 3), int))
    if n:
        for a, b in zip(lab[:, 0], lab[:, -1]):                   # join regions across 0/360 E
            if a and b and a != b:
                lab[lab == b] = a
        u = np.unique(lab[lab > 0])
        remap = np.zeros(lab.max() + 1, int)
        remap[u] = np.arange(1, len(u) + 1)
        lab, n = remap[lab], len(u)
    return lab, n


def near(mask, lat, lon, km=MATCH_ALARM_KM):
    if not mask.any():
        return False
    return bool((E.great_circle_km(lat, lon, PR.LA[mask], PR.LO[mask]) <= km).any())


def lon_extent(cols):
    """Smallest longitude arc [start, end] (deg, end may exceed 360) covering the occupied columns."""
    c = np.unique(cols)
    gaps = np.diff(np.concatenate([c, [c[0] + 360]]))
    k = int(np.argmax(gaps))
    start = c[(k + 1) % len(c)]
    end = c[k] + (360 if c[k] < start else 0)
    return int(start), int(end + 1)


def score_method(mask, onsets):
    lab, n = regions(mask)
    hits = [near(mask, o["lat"], o["lon"]) for _, o in onsets]
    regs = []
    for r in range(1, n + 1):
        m = lab == r
        conf = any(near(m, o["lat"], o["lon"]) for _, o in onsets)
        rows, cols = np.nonzero(m)
        a, b = lon_extent(PR.LO[m].astype(int))
        regs.append(dict(lon0=a, lon1=b, lat0=int(PR.LA[m].min()), lat1=int(PR.LA[m].max()), confirmed=conf))
    obs_box = np.zeros(N_BOX, bool)
    for _, o in onsets:
        i, j = int(round(o["lat"])), int(round(o["lon"])) % 360
        if BOX_ID[i, j] >= 0:
            obs_box[BOX_ID[i, j]] = True
    al_box = np.zeros(N_BOX, bool)
    al_box[np.unique(BOX_ID[mask & (BOX_ID >= 0)])] = True
    boxes = dict(TP=int((al_box & obs_box).sum()), FP=int((al_box & ~obs_box).sum()),
                 FN=int((~al_box & obs_box).sum()), TN=int((~al_box & ~obs_box).sum()))
    w = np.cos(np.deg2rad(PR.LA))
    frac = float((w * mask).sum() / (w * PR.IN_BAND).sum())
    return dict(onset_hits=hits, regions=regs, boxes=boxes, area_fraction=round(frac, 4)), lab


def issue(H, t, gfs_surfaces):
    """Everything for issue time t: (record for JSON, {surface: {method: alarm mask}})."""
    out = dict(issue=t.strftime("%Y%m%d%H"), opus_surface=OPUS_SURFACE, amp_surface=AMP_SURFACE,
               amp_threshold_deg=AMP_THRESHOLD_DEG, surfaces={})
    masks = {}
    qs, us, vs = H.stack(OPUS_SURFACE, t - timedelta(hours=OPUS_SPAN_H), t)
    m_op, _ = PR.opus_alarm(qs, us, vs)            # one alarm map each, scored against the onsets of every surface
    m_amp, _ = PR.amp_alarm(H.d[t][AMP_SURFACE][0])
    for name in SURFACES:
        on = truth_onsets(H, name, t)
        q, u, v = H.d[t][name]
        qb = H.d[t - timedelta(hours=24)][name]
        m_uc, uc_pts = PR.uc_alarm((E.smooth(q), u, v), (E.smooth(qb[0]), qb[1], qb[2]))
        mm = {"uc": m_uc, "opus": m_op, "amp": m_amp}
        rec = dict(onsets=[dict(time=w.strftime("%Y%m%d%H"), **lean(o)) for w, o in on],
                   jet_axis=[round(float(x), 1) for x in E.jet_axis(u, v)], methods={})
        if gfs_surfaces is not None:
            seq = [(s, E.objects(*gfs_surfaces[s][name], name)) for s in GFS_STEPS_H]
            mm["gfs"], found = PR.gfs_alarm(seq)
            rec["gfs_onsets"] = found
        for m, mask in mm.items():
            rec["methods"][m], _ = score_method(mask, on)
        out["surfaces"][name] = rec
        masks[name] = mm
    return out, masks


def issue_times(a: datetime, b: datetime, hours=(0, 12)):
    t = a.replace(minute=0, second=0, microsecond=0)
    out = []
    while t <= b:
        if t.hour in hours:
            out.append(t)
        t += timedelta(hours=1)
    return out
