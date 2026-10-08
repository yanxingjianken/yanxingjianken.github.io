# Northern-Hemisphere forecast pipeline

Runs hourly on GitHub Actions (`.github/workflows/nh_forecast.yml`) and publishes a
model whenever a newer complete run exists (GFS 0.25° from NOAA Open Data, ECMWF AIFS-single and IFS 0.25°
from ECMWF open data; the IFS 06/18 UTC cycles end at 144 h). For each run it keeps u, v, T, Z, ω, q at 850/500/250 hPa for
0–90°N (0.5°) and a 0.25° CONUS window, plus near-surface fields (2-m temperature
and dew point, 10-m wind, mean-sea-level pressure in hPa, and precipitation over
the 6 h ending at each step in mm; files `<var>sfc.u16.gz`), tracks 500-hPa
lows/highs over the previous 5 days + the forecast, and publishes everything to
the public Hugging Face dataset `yanxingjianken/nh-forecast-6hourly` (history
squashed daily).  The pages `/blocking-plots/nh-forecast/` and `/wxchallenge/`
read that dataset directly.

Precipitation: GFS files carry a 6-h bucket; ECMWF files carry run totals, so the
6-h amount is the difference from the previous step. Units are read from each
GRIB message (IFS in m, AIFS and GFS in kg m-2) and converted to mm.

No model data is kept on the runner or on any laptop: the script works in a
temporary directory that is deleted when it finishes.

Local dry run (nothing uploaded, output kept under /tmp/nhf_test):

    python run_pipeline.py --dry-run --models gfs --max-step 12 --out /tmp/nhf_test

One-off: rebuild the Z500 climatology used for anomalies

    python -c "import climatology; climatology.build_z500_ltm('hgt.day.ltm.1991-2020.nc', out_u16_gz='data/z500_ltm_1991-2020_2p5.u16.gz')"
