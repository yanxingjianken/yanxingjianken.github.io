---
title: "ASOS Reliability &amp; Live Temperature Nowcast"
excerpt: "Per-reading reliability + an intraday forecast of today's official daily high/low, calibrated live from ASOS + GOES + HRRR.<br/><img src='/files/asos_demo/fig/webapp_shot.png' style='max-width:70%;height:auto;'>"
collection: portfolio
---

A per-station Bayesian state-space + ML model for short-fuse temperature markets (e.g. Kalshi
"highest temperature today"). For any live 5-minute ASOS reading it returns a calibrated reliability —
P(exactly right / ±1 °F / ≥2 °F), a corrected value, and change/stuck/fault warnings — and it forecasts
**today's official daily high/low** intraday: starting from the HRRR forecast and calibrating as the
day's reads arrive, until the peak passes and it locks onto the settlement.

It fuses the live whole-°C/°F ASOS feed with **GOES** split-window skin temperature and **HRRR**, using a
faithful implementation of **field alignment** (Ravela, Emanuel &amp; McLaughlin 2007) to separate an
advecting satellite feature from a real local change.

<div style="margin:22px 0;padding:18px;border:1px solid #ccc;border-radius:10px;background:#f7f9fb">
  <b>🔒 Interactive demo — password-protected</b><br/>
  Three worked out-of-sample examples (with a B0 / A / M model toggle), the full methodology &amp; findings,
  and a <b>live</b> "pick a station → forecast today's high/low" tab that pulls the latest Synoptic + GOES +
  HRRR and runs the model in real time.
  <div style="margin-top:12px">
    <a href="/files/asos_demo/" style="display:inline-block;padding:10px 20px;background:#1f6fb2;color:#fff;
       border-radius:8px;text-decoration:none;font-weight:600">Launch the interactive demo →</a>
  </div>
  <div style="color:#777;font-size:0.85em;margin-top:8px">Ask the author for the access password.</div>
</div>

**Highlights** (held out by day, all 20 stations): the learned head reaches **69 % fine-°F accuracy**
(naive 56 %); the augmented-physics model catches **100 %** of injected spikes; and the intraday nowcast
beats the no-forecast baseline at every decision hour — most by mid-morning, before the day's high has
happened.
