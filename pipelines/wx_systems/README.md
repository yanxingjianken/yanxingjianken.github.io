# ERA5 case figures for portfolio 051 (Special Weather Systems)

Each `fig_<system>_<year>.py` draws one figure into `images/wx_systems_v3/`.
Data come from the public ARCO-ERA5 store on Google Cloud
(`gs://gcp-public-data-arco-era5`, 0.25°, hourly, anonymous access) and are cached in `cache/`.

```
pip install xarray zarr gcsfs cartopy matplotlib
cd pipelines/wx_systems
python fig_seabreeze_2007.py
```

- `jstyle.py`: shared figure style (Arial 8 pt, 6.5-in width, panel labels, colorbars, Lambert maps) and the ERA5 fetcher.
- `helpers_A/B/C.py`, `cities.py`: extra map helpers and the reference-city dots.
- `manifest_A/B/C.json`: case time, panels, caption text and the numbers quoted in each caption.
  The captions on the page are later edits of these; the numbers are the same.
