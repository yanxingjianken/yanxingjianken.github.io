# WeatherNext 3 team files

`run_wn3.py` runs hourly on GitHub Actions (`.github/workflows/wn3_forecast.yml`). It reads the newest complete
00/06/12/18 UTC run of Google DeepMind's WeatherNext 3 from the free statistics bucket
(`gs://weathernext3_statistics_spatial`), keeps:

- hourly station series to 48 h for every station in `assets/data/asos_stations.json`: station-calibrated 2-m
  temperature and dew point (mean, 10th and 90th percentile), 10-m wind speed (mean, p10, p90) and direction,
  hourly precipitation (mean, p90, IMERG-calibrated mean), sea-level pressure and cloud cover (total, low, middle, high);
- 6-hourly maps to 240 h on a 0.1° window over the US (20–54°N, 135–60°W): 2-m temperature, dew point and
  temperature spread (p90 − p10), 10-m and 100-m wind, sea-level pressure, 6-h precipitation (model and
  IMERG-calibrated) and cloud cover;

and publishes them to `wn3/` in the Hugging Face dataset `yanxingjianken/nh-forecast-6hourly`.

**Why the files are encrypted.** Live WeatherNext forecasts are covered by the
[GDM Real-Time Weather Forecasting Experimental Data Terms of Use](https://storage.googleapis.com/weathernext-public/terms-of-use.pdf),
which allow sharing only with clearly identified people, for educational purposes, through controlled
distribution. Every data file is AES-256-GCM encrypted with a key derived (PBKDF2-HMAC-SHA256, 600 000
iterations) from the team passcode; the WxChallenge page asks for the passcode and decrypts in the browser.
The passcode lives only in the GitHub secret `WN3_PASSCODE` and with the team. The Terms, the
`LEGALLY_BINDING_TERMS_OF_USE.txt` notice and the copyright notice travel with the data.

**Secrets:** `GCP_ADC_JSON` (application-default credentials of the allowlisted Google account, from
`gcloud auth application-default login`), `WN3_PASSCODE`, `HF_TOKEN`.

Pressure levels are not used: they exist only in the requester-pays 64-member bucket, where the downloader pays
Google's network charges.

Local checks (nothing uploaded; delete the output afterwards):

    python run_wn3.py --list
    WN3_PASSCODE=test python run_wn3.py --dry-run --out /tmp/wn3_test --ts-hours 3 --map-steps 6,12 --stations KBOS,KTPA
