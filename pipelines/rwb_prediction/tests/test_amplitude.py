"""Wave amplitude: zero for a zonally symmetric field; for contours displaced by a0 sin(6 lambda) the zonal rms of
the local amplitude is the rms of the displacement left after the 3-degree smoothing, a0 g / sqrt(2)."""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import predictors as PR  # noqa: E402
from config import EVENT_SMOOTH_DEG  # noqa: E402


def test_zonal_field_has_no_amplitude():
    theta = 350.0 - PR.LA                                     # decreasing poleward, as theta on 2 PVU
    a = PR.amp_field(-theta)
    assert np.abs(a[10:81]).max() < 0.1
    mask, _ = PR.amp_alarm(-theta, threshold=0.5)
    assert not mask.any()


def test_displaced_contours():
    a0, m = 5.0, 6
    theta = 350.0 - (PR.LA - a0 * np.sin(np.deg2rad(m * PR.LO)))
    a = PR.amp_field(-theta)
    for lat in (35, 45, 55):
        sig = EVENT_SMOOTH_DEG / np.cos(np.deg2rad(lat))         # longitude smoothing (deg) at this latitude
        g = np.exp(-0.5 * (np.deg2rad(m) * sig) ** 2)          # its damping of wavenumber m
        expect = a0 * g / np.sqrt(2.0)
        got = np.sqrt(np.mean(a[lat] ** 2))
        assert abs(got - expect) < 0.1 * expect, (lat, got, expect)
    mask, _ = PR.amp_alarm(-theta, threshold=1.0)
    assert mask[30:60].mean() > 0.5 and not mask[~PR.IN_BAND].any()
