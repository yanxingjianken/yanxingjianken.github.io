"""Settings shared by every step. Fixed before any score was computed, except the wave-amplitude threshold, which
was chosen on the issue times of October 2026 (AMP_FIT_LAST_ISSUE) and is fixed for every later issue time."""
from __future__ import annotations

LEVELS_HPA = (70, 100, 150, 200, 250, 300, 350, 400, 450, 500)   # pressure levels used for ERA5 and GFS alike
GRID_DEG = 1.0                                                  # 0-90 N x 0-359 E, latitude ascending
SURFACES = ("pv330", "pv350", "th2pvu")
SURFACE_LABEL = {"pv330": "PV on 330 K", "pv350": "PV on 350 K", "th2pvu": "θ on 2 PVU"}

# events (circumpolar-contour overturning, after pvtend.rwb)
EVENT_STEP_H = 6                 # events are detected every 6 h
PV_LEVELS = tuple(round(0.5 * k, 1) for k in range(1, 21))      # PVU: contours every 0.5 PVU, 0.5-10
TH_LEVELS = tuple(range(280, 401, 5))                          # K: theta on 2 PVU every 5 K
CIRCUMPOLAR_MIN_SPAN = 355.0     # deg of longitude
MIN_CROSS = 3                    # meridian crossings that make a fold
AREA_MIN_DEG2 = 300.0            # minimum bay area (deg^2), on the smoothed field
EVENT_SMOOTH_DEG = 3.0           # Gaussian smoothing before contouring: sigma in latitude, sigma/cos(lat) in longitude
CLUSTER_KM = 1000.0              # bays closer than this form one breaking object
MATCH_KM = 1500.0                # an object is new if no object of the same type lay within this 6 h and 12 h earlier
JET_BAND = (20.0, 70.0)          # jet axis: latitude of the strongest wind on the surface in this band

# alarms and scoring: each method outputs alarm regions on the 1-degree grid
ISSUE_HOURS = (0, 12)            # alarms are issued at 00 and 12 UTC
WINDOW_H = 24                    # an alarm region claims: a new breaking within this distance of it in the next 24 h
MATCH_ALARM_KM = 1000.0          # an onset is a hit if an alarm region of the same issue lies within this distance
BOX_DEG = 9.0                    # equal-area verification boxes (about 1000 km) in 10-90 N for the false positive rate
ALARM_LAT = (10.0, 88.0)         # alarm regions are confined to these latitudes

# predictor: U - c matching
UC_THRESHOLD_MS = 2.0            # alarm where |U - c| on a piece of contour is below this
UC_MIN_CORR = 0.5                # phase speed used only where the 24-h lagged correlation reaches this
UC_LEVEL_LATS = tuple(range(25, 71, 5))   # contours at these equivalent latitudes
UC_LON_STEP = 15.0               # |U - c| every 15 deg of longitude along each contour
UC_WINDOW_DEG = 30.0             # phase speed from the lagged correlation within +-30 deg
UC_BUFFER_KM = 500.0             # alarm region: within this distance of the matching contour segment

# predictor: Opus model (computed on theta on 2 PVU, which air parcels conserve in adiabatic, frictionless flow;
# the same alarm regions are scored against the onsets of every surface)
OPUS_SURFACE = "th2pvu"
OPUS_N_PARCELS = 20000
OPUS_SEED_BAND = (15.0, 80.0)
OPUS_DT_S = 900.0
OPUS_SPAN_H = 60                 # parcels run over the 60 h before the issue time
OPUS_REF_H = (-59, -36)          # reference window (hours relative to the issue time)
OPUS_NOW_H = (-23, -1)           # current window
OPUS_BAND_DEG = 3.0
OPUS_LON_BIN = 15.0              # local cells: 3-deg bands of the label's equivalent latitude x 15 deg
OPUS_MIN_SAMPLES = 60
OPUS_MIN_SPREAD_DEG = 0.3
OPUS_MIN_REF_D2 = 0.3
OPUS_RATIO = 0.1                 # alarm when the predictor variable falls to this fraction of its reference value

# predictor: wave amplitude (no forecast), on theta on 2 PVU at the issue time only; the same alarm regions are scored
# against the onsets of every surface
AMP_SURFACE = "th2pvu"
AMP_BOX_DEG = (3, 15)            # local amplitude: rms displacement over 3 deg of latitude x 15 deg of longitude
AMP_THRESHOLD_DEG = 8.5          # alarm where the local amplitude reaches this (deg of latitude); set 2026-11-02 as
                                 # the best box skill on theta on 2 PVU over the issue times 2026-09-30 12 UTC to
                                 # 2026-10-26 12 UTC (sweep 1-15 deg in steps of 0.5 deg)
AMP_FIT_LAST_ISSUE = "2026102612"    # threshold chosen on the issue times up to here; later ones are out of sample

# baseline forecast
GFS_STEPS_H = (0, 6, 12, 18, 24)
GFS_BUFFER_KM = 500.0            # alarm region: within this distance of a forecast onset

A_EARTH = 6.371e6
OMEGA = 7.292e-5
G = 9.80665
KAPPA = 287.05 / 1004.6
