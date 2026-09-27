# Northern-Hemisphere forecast pipeline

Runs hourly on GitHub Actions (`.github/workflows/nh_forecast.yml`) and publishes a
model whenever a newer complete run exists (GFS 0.25° from NOAA Open Data, ECMWF
AIFS-single 0.25° from ECMWF open data). For each run it keeps u, v, T, Z, ω, q at 850/500/250 hPa for
0–90°N (0.5°) and a 0.25° CONUS window, tracks 500-hPa cyclones/anticyclones
over the previous 5 days + the forecast, and publishes everything to the public
Hugging Face dataset `yanxingjianken/nh-forecast-6hourly`.  The web page
`/blocking-plots/nh-forecast/` reads that dataset directly.

No model data is kept on the runner or on any laptop: the script works in a
temporary directory that is deleted when it finishes.

Local dry run (nothing uploaded, output kept under /tmp/nhf_test):

    python run_pipeline.py --dry-run --models gfs --max-step 12 --out /tmp/nhf_test

One-off: rebuild the Z500 climatology used for anomalies

    python -c "import climatology; climatology.build_z500_ltm('hgt.day.ltm.1991-2020.nc', out_u16_gz='data/z500_ltm_1991-2020_2p5.u16.gz')"
