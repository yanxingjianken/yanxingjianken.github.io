"""Build assets/data/asos_stations.json from the IEM ASOS/AWOS network catalogue.

Source: https://mesonet.agron.iastate.edu/geojson/network/AZOS.geojson (all ASOS/AWOS
sites worldwide, ~6,000).  We keep the United States (states, DC, PR, VI, GU) and
write a compact list used by the WxChallenge page's station search.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

SRC = "https://mesonet.agron.iastate.edu/geojson/network/AZOS.geojson"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "assets", "data", "asos_stations.json")


def main(src=SRC, out=OUT):
    if src.startswith("http"):
        with urllib.request.urlopen(src, timeout=120) as r:
            g = json.load(r)
    else:
        g = json.load(open(src))
    rows = []
    for f in g["features"]:
        p = f["properties"]
        if p.get("country") != "US":
            continue
        sid = p.get("sid") or f.get("id")
        if not sid:
            continue
        icao = sid if len(sid) == 4 else ("K" + sid if len(sid) == 3 and p.get("state") not in ("AK", "HI", "PR", "VI", "GU") else sid)
        lon, lat = f["geometry"]["coordinates"]
        rows.append({
            "id": sid, "icao": icao, "name": (p.get("sname") or "").strip(), "state": p.get("state"),
            "lat": round(lat, 4), "lon": round(lon, 4), "elev": round(p.get("elevation") or 0.0, 1),
            "tz": p.get("tzname"), "network": p.get("network"), "online": bool(p.get("online")),
        })
    rows.sort(key=lambda r: r["icao"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        json.dump({"source": SRC, "n": len(rows), "stations": rows}, fh, separators=(",", ":"))
    print(f"wrote {len(rows)} stations to {out}")


if __name__ == "__main__":
    main(*sys.argv[1:])
