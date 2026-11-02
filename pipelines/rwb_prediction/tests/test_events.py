"""Event detection: breaking-type labels on a barotropic jet that breaks on both flanks (absolute vorticity of an
idealized run 6 d after a wavenumber-6 disturbance, 1-degree grid): bays equatorward of the jet are anticyclonic,
bays poleward of it cyclonic."""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import events as E  # noqa: E402


def test_breaking_types_by_flank(monkeypatch):
    monkeypatch.setattr(E, "AREA_MIN_DEG2", 30.0)            # the orientation test uses the unsmoothed field
    q = np.load(HERE / "fixtures" / "barotropic_jet_breaking.npz")["q"].astype(float)
    found = []
    band = -q[20:81]
    levels = np.linspace(np.percentile(band, 2), np.percentile(band, 98), 100)
    for lev, lon_c, lat_c in E.circumpolar_contours(-q, levels):
        found += E.bays(lon_c, lat_c)
    eq = [b[0] for b in found if b[3] < 40]
    pol = [b[0] for b in found if b[3] > 55]
    assert eq and pol
    assert all(t == "AWB" for t in eq)
    assert all(t == "CWB" for t in pol)


def test_crossings_count():
    x = np.array([0.0, 10, 5, 15, 20])
    y = np.array([0.0, 1, 2, 3, 4])
    yc = E.crossings(x, y, np.array([7.5]))
    assert np.isfinite(yc).sum() == 3
