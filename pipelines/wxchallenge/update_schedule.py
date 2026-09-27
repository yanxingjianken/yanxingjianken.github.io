"""Refresh assets/data/wxchallenge_schedule.json from https://www.wxchallenge.com/schedule.php

The schedule page is plain HTML without CORS headers, so the site cannot read it
in the browser; a weekly GitHub Action runs this script and commits the JSON.
Rows whose city is still '-' are kept as placeholders (station null).  Dates on
the page carry no year: forecast periods from September to December belong to the
first year of the season, January to April to the second.
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
import urllib.request
from datetime import date, datetime, timezone

URL = "https://www.wxchallenge.com/schedule.php"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "assets", "data", "wxchallenge_schedule.json")
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July",
                                      "August", "September", "October", "November", "December"], 1)}


def season_start_year(today: date) -> int:
    return today.year if today.month >= 8 else today.year - 1


def parse_date(txt: str, y0: int) -> str:
    m = re.match(r"([A-Za-z]+)\s+(\d{1,2})", txt.strip())
    mon, day = MONTHS[m.group(1)], int(m.group(2))
    year = y0 if mon >= 8 else y0 + 1
    return date(year, mon, day).isoformat()


def parse(html_text: str, today: date | None = None) -> dict:
    today = today or datetime.now(timezone.utc).date()
    y0 = season_start_year(today)
    periods = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", html_text, flags=re.S | re.I):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                 for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, flags=re.S | re.I)]
        if len(cells) < 4 or " - " not in cells[3]:
            continue
        city, station, climo, dates = cells[:4]
        start_txt, end_txt = [s.strip() for s in dates.split(" - ", 1)]
        tournament = city.endswith("*")
        city = city.rstrip("*").strip()
        station = station.strip().upper()
        periods.append({
            "city": None if city in ("", "-") else city,
            "station": None if station in ("", "-") else station,
            "climo": climo or None,
            "start": parse_date(start_txt, y0), "end": parse_date(end_txt, y0),
            "tournament": tournament,
        })
    if not periods:
        raise RuntimeError("no schedule rows parsed")
    return {"season": f"{y0}-{str(y0 + 1)[2:]}", "source": URL,
            "fetched": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fallback_station": "KBOS", "periods": periods}


def main(src=URL, out=OUT):
    if src.startswith("http"):
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0 (schedule refresh for yanxingjianken.github.io)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            text = r.read().decode("utf-8", "replace")
    else:
        text = open(src, encoding="utf-8", errors="replace").read()
    new = parse(text)
    old = None
    if os.path.exists(out):
        try:
            old = json.load(open(out))
        except Exception:
            old = None
    if old and old.get("periods") == new["periods"] and old.get("season") == new["season"]:
        print("schedule unchanged")
        return False
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        json.dump(new, fh, indent=1)
    print(f"wrote {len(new['periods'])} periods to {out}")
    return True


if __name__ == "__main__":
    main(*sys.argv[1:])
