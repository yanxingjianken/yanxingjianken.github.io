---
title: "Special Weather Systems of the U.S. &amp; the Northeast"
excerpt: "A field guide to 21 recurring circulations — sea breeze, backdoor front, cold-air damming, nor'easters — every one with a mechanism schematic, a real ERA5 850-hPa T / 500-hPa height map of its case date, and a sourced NWS forecaster quote.<br/><img src='/images/wx_systems/noreaster_2015.png' style='max-width: 60%; height: auto;'>"
collection: portfolio
---

<style>
.wxsys{--paper:#eaeef2;--panel:#f7f9fb;--ink:#15202c;--soft:#4a5a6d;--faint:#7c8da0;--line:#ccd5de;
 --cold:#2d5a92;--warm:#c1492f;--sky:#dbe6f0;--land:#d8d2c4;--accent:#2d5a92;
 --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;--serif:Georgia,"Times New Roman",serif;
 color:var(--ink);font-size:15.5px;line-height:1.6}
@media (prefers-color-scheme:dark){.wxsys{--paper:#0b121a;--panel:#111b25;--ink:#dde6ef;--soft:#93a2b4;
 --faint:#65758a;--line:#22313f;--cold:#63a0da;--warm:#e57a58;--sky:#12212f;--land:#26303a;--accent:#63a0da}}
.wxsys *{box-sizing:border-box}
.wxsys .intro{color:var(--soft);font-family:var(--serif);font-style:italic;font-size:16px;max-width:60ch}
.wxsys .legend{display:flex;flex-wrap:wrap;gap:10px 22px;align-items:center;font-size:12.5px;color:var(--soft);
 background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:18px 0 6px}
.wxsys .legend .k{display:inline-flex;align-items:center;gap:7px}
.wxsys .sec-h{display:flex;align-items:baseline;gap:12px;margin:34px 0 4px;padding-bottom:8px;border-bottom:2px solid var(--ink)}
.wxsys .sec-h .num{font-family:var(--mono);font-size:12px;color:var(--warm);font-weight:700}
.wxsys .sec-h h2{font-family:var(--serif);font-size:21px;margin:0;border:0;padding:0}
.wxsys .sec-h .sub{font-size:12.5px;color:var(--soft);margin-left:auto}
.wxsys .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px;margin:18px 0 6px}
.wxsys .sys{background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
.wxsys .sys .fig{background:var(--sky);border-bottom:1px solid var(--line)}
.wxsys .sys .fig svg{display:block;width:100%;height:auto}
.wxsys .sys .fig text{font-family:var(--mono);font-size:9px;fill:var(--soft)}
.wxsys .sys .fig text.hi{fill:var(--ink);font-weight:600}
.wxsys .sys .fig text.wm{fill:var(--warm)}.wxsys .sys .fig text.cl{fill:var(--cold)}
.wxsys .realfig{border-bottom:1px solid var(--line);background:var(--panel)}
.wxsys .realfig img{display:block;width:100%;height:auto}
.wxsys .realfig .cap{font-family:var(--mono);font-size:10px;color:var(--faint);padding:4px 10px 7px}
.wxsys .bd{padding:14px 16px 16px;display:flex;flex-direction:column;gap:9px;flex:1}
.wxsys .chip{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--soft)}
.wxsys .sys h3{font-family:var(--serif);font-size:17.5px;margin:0}
.wxsys .lead{color:var(--soft);font-size:14px;margin:0}
.wxsys dl.mech{margin:0;display:grid;grid-template-columns:auto 1fr;gap:4px 11px;font-size:13.5px}
.wxsys dl.mech dt{font-family:var(--mono);font-size:10.5px;text-transform:uppercase;color:var(--warm);padding-top:2px;white-space:nowrap}
.wxsys dl.mech dd{margin:0}
.wxsys .diag{font-size:12px;color:var(--soft);border-top:1px dashed var(--line);padding-top:8px}
.wxsys .diag b{color:var(--ink);font-family:var(--mono);font-size:11px}
.wxsys .ex{font-size:12px;background:var(--paper);border-radius:6px;padding:7px 9px;margin-top:auto}
.wxsys .ex .d{font-family:var(--mono);font-size:10.5px;display:block;margin-bottom:2px}
.wxsys .ex .d a{color:var(--accent)}.wxsys .ex i{color:var(--soft)}
</style>

<div class="wxsys" markdown="0">
<p class="intro">Twenty-one recurring circulations — from the Boston sea breeze to the Appalachian cold-air wedge — read as mechanisms: what forces them, what they do to the near-surface temperature, and where they lead. <b>Every system carries both</b> a hand-drawn cross-section or plan-view schematic <b>and a real ERA5 map of its case date</b> — 850-hPa temperature (shaded) + 500-hPa geopotential height (contours). For the storm- and mesoscale systems the ERA5 map shows the <em>synoptic setup that permits them</em>; the feature itself lives below reanalysis resolution (look to radar). Forecaster cases are quoted from NWS Area Forecast Discussions with a link to the source text.</p>

<div class="legend">
  <span class="k"><svg width="34" height="14"><line x1="1" y1="7" x2="33" y2="7" stroke="var(--cold)" stroke-width="2"/><polygon points="9,7 13,2 17,7" fill="var(--cold)"/><polygon points="21,7 25,2 29,7" fill="var(--cold)"/></svg> cold front</span>
  <span class="k"><svg width="24" height="14"><line x1="2" y1="7" x2="22" y2="7" stroke="var(--warm)" stroke-width="2.4" marker-end="url(#mw)"/></svg> warm / rising air</span>
  <span class="k"><svg width="24" height="14"><line x1="2" y1="7" x2="22" y2="7" stroke="var(--cold)" stroke-width="2.4" marker-end="url(#mc)"/></svg> cold / sinking air</span>
  <span class="k"><svg width="18" height="12"><rect x="1" y="2" width="16" height="8" fill="var(--warm)" opacity=".22"/></svg> warm shading (θ,T)</span>
  <span class="k"><svg width="18" height="12"><rect x="1" y="2" width="16" height="8" fill="var(--cold)" opacity=".22"/></svg> cold shading</span>
</div>

<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <marker id="mw" markerWidth="7" markerHeight="7" refX="5" refY="3.2" orient="auto"><path d="M0 0 L7 3.2 L0 6.4 z" fill="var(--warm)"/></marker>
  <marker id="mc" markerWidth="7" markerHeight="7" refX="5" refY="3.2" orient="auto"><path d="M0 0 L7 3.2 L0 6.4 z" fill="var(--cold)"/></marker>
  <marker id="mk" markerWidth="7" markerHeight="7" refX="5" refY="3.2" orient="auto"><path d="M0 0 L7 3.2 L0 6.4 z" fill="var(--soft)"/></marker>
</defs></svg>

<div class="sec-h"><span class="num">I</span><h2>Coastal &amp; marine — the Northeast seaboard</h2><span class="sub">the sharpest T2m gradients in the domain</span></div>
<div class="grid">

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Sea-breeze circulation">
  <rect width="300" height="168" fill="var(--sky)"/><rect x="0" y="132" width="120" height="36" fill="var(--cold)" opacity=".30"/>
  <path d="M120 132 H300 V168 H120 Z" fill="var(--land)"/><path d="M120 132 H300" stroke="var(--line)"/>
  <g stroke="var(--warm)" stroke-width="1.3"><circle cx="248" cy="28" r="8" fill="var(--warm)" opacity=".5"/><line x1="248" y1="12" x2="248" y2="6"/></g>
  <rect x="150" y="98" width="150" height="34" fill="var(--warm)" opacity=".16"/>
  <line x1="18" y1="124" x2="146" y2="124" stroke="var(--cold)" stroke-width="2.4" marker-end="url(#mc)"/>
  <line x1="205" y1="128" x2="205" y2="72" stroke="var(--warm)" stroke-width="1.8" marker-end="url(#mw)"/>
  <line x1="196" y1="62" x2="60" y2="62" stroke="var(--warm)" stroke-width="1.8" marker-end="url(#mw)"/>
  <line x1="48" y1="70" x2="48" y2="112" stroke="var(--cold)" stroke-width="1.8" marker-end="url(#mc)"/>
  <line x1="150" y1="116" x2="150" y2="132" stroke="var(--cold)" stroke-width="2"/><polygon points="150,120 157,124 150,128" fill="var(--cold)"/>
  <text class="cl" x="8" y="150">cool sea</text><text class="wm" x="238" y="150">hot land</text><text class="hi" x="116" y="112">sea-breeze front →</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/seabreeze_2007.png" alt="Sea breeze ERA5 t850 z500"><div class="cap">ERA5 · 2007-03-27 18Z (synoptic setup)</div></div>
  <div class="bd"><span class="chip">Mesoscale · thermally direct</span><h3>Sea breeze</h3>
  <p class="lead">A daytime onshore circulation set up by the land heating faster than the sea.</p>
  <dl class="mech"><dt>Cause</dt><dd>Differential land–sea heating drives onshore flow beneath a return flow aloft.</dd>
  <dt>Affects</dt><dd>The advancing <b>sea-breeze front</b> shifts wind onshore, raises dewpoint, and caps the coastal high by late morning.</dd>
  <dt>Leads to</dt><dd>A sharp coast-vs-inland split; the convergence line can trigger inland showers.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> 10-m wind + T2m + dewpoint; radar clear-air fine-line. <em>(Mesoscale — below reanalysis resolution.)</em></p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDBOX&sdate=2007-03-27&edate=2007-03-28&fmt=text">2007-03-27 · Boston (BOX) — source</a></span><i>"eastern coastal MASS where temps have cooled into the mid 40s courtesy of the seabreeze front."</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Backdoor cold front plan view">
  <rect width="300" height="168" fill="var(--sky)"/><path d="M0 168 L0 96 C 90 92, 150 132, 300 118 L300 168 Z" fill="var(--land)"/>
  <path d="M0 96 C 90 92, 150 132, 300 118" stroke="var(--line)"/><rect x="150" y="0" width="150" height="168" fill="var(--cold)" opacity=".12"/>
  <text class="hi" x="226" y="24">cold HIGH</text><text x="232" y="36">(Québec /</text><text x="234" y="46">Maritimes)</text>
  <line x1="250" y1="60" x2="70" y2="132" stroke="var(--cold)" stroke-width="2.4"/>
  <g fill="var(--cold)"><polygon points="228,66 234,58 240,70"/><polygon points="188,80 194,72 200,84"/><polygon points="148,94 154,86 160,98"/><polygon points="108,108 114,100 120,112"/></g>
  <text x="12" y="150" class="hi">interior stays warm</text><text class="cl" x="150" y="150">← cool marine push</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/backdoor_2008.png" alt="Backdoor front 2008-03-08 t850 and z500"><div class="cap">ERA5 · 2008-03-08 18Z</div></div>
  <div class="bd"><span class="chip">Synoptic · shallow front</span><h3>Backdoor cold front</h3>
  <p class="lead">A cold front that arrives from the <em>northeast</em> — backwards from the usual NW→SE.</p>
  <dl class="mech"><dt>Cause</dt><dd>A 500-hPa ridge over eastern Canada and a surface high over Québec/the Maritimes drive cool marine air <em>southwest</em> down the coast.</dd>
  <dt>Affects</dt><dd>A coastal <b>crash of 10–30 °F</b> behind an NE wind shift and dewpoint drop; the interior often stays hot.</dd>
  <dt>Leads to</dt><dd>Big coast-vs-inland splits and forecast busts — a spring/early-summer specialty.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> MSLP + 10-m wind + dewpoint; 850-hPa T; radar fine-line.</p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDBOX&sdate=2008-03-08&edate=2008-03-09&fmt=text">2008-03-08 · Boston (BOX) — source</a></span><i>"the backdoor cold front that cooled temperatures into the upper 30s and lower 40s."</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Coastal front cross-section">
  <rect width="300" height="168" fill="var(--sky)"/><rect x="0" y="0" width="150" height="168" fill="var(--cold)" opacity=".16"/><rect x="150" y="0" width="150" height="168" fill="var(--warm)" opacity=".12"/>
  <path d="M0 132 H150 V168 H0 Z" fill="var(--land)"/><rect x="150" y="132" width="150" height="36" fill="var(--cold)" opacity=".25"/>
  <line x1="150" y1="40" x2="150" y2="132" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="4 3"/>
  <line x1="60" y1="122" x2="140" y2="122" stroke="var(--cold)" stroke-width="2" marker-end="url(#mc)"/>
  <line x1="240" y1="122" x2="162" y2="122" stroke="var(--warm)" stroke-width="2" marker-end="url(#mw)"/>
  <ellipse cx="150" cy="52" rx="34" ry="12" fill="var(--soft)" opacity=".35"/>
  <text class="cl" x="30" y="150">cold interior</text><text class="wm" x="196" y="150">mild marine</text><text class="hi" x="120" y="34">coastal front</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/coastalfront_2008.png" alt="Coastal front ERA5 t850 z500"><div class="cap">ERA5 · 2008-01-26 12Z</div></div>
  <div class="bd"><span class="chip">Mesoscale · baroclinic zone</span><h3>Coastal front</h3>
  <p class="lead">A near-stationary temperature boundary hugging the coastline in the cool season.</p>
  <dl class="mech"><dt>Cause</dt><dd>Land–sea thermal contrast (often reinforced by cold-air damming) concentrates a shallow baroclinic zone at the coast.</dd>
  <dt>Affects</dt><dd>A very tight T and precip-type gradient — a few km separate 34 °F rain/snow from 45 °F.</dd>
  <dt>Leads to</dt><dd>Rain/snow lines and a favored axis for coastal cyclogenesis.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> surface T + wind convergence; radar. <em>(Mesoscale.)</em></p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDBOX&sdate=2008-01-26&edate=2008-01-27&fmt=text">2008-01-26 · Boston (BOX) — source</a></span><i>"caveat: coastal front developing /ESE wind/… snow showers may break out Boston to NBT."</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Marine layer cross-section">
  <rect width="300" height="168" fill="var(--sky)"/><g stroke="var(--warm)" stroke-width="1.3"><circle cx="250" cy="26" r="8" fill="var(--warm)" opacity=".45"/><line x1="250" y1="10" x2="250" y2="4"/></g>
  <line x1="0" y1="86" x2="300" y2="86" stroke="var(--ink)" stroke-width="1.4" stroke-dasharray="5 3"/><text class="hi" x="6" y="80">subsidence inversion (lid)</text>
  <rect x="0" y="88" width="300" height="44" fill="var(--soft)" opacity=".38"/>
  <g fill="var(--panel)" opacity=".9"><ellipse cx="60" cy="104" rx="26" ry="9"/><ellipse cx="150" cy="110" rx="30" ry="10"/><ellipse cx="240" cy="104" rx="26" ry="9"/></g>
  <rect x="0" y="132" width="300" height="36" fill="var(--cold)" opacity=".30"/>
  <line x1="20" y1="122" x2="150" y2="122" stroke="var(--cold)" stroke-width="2" marker-end="url(#mc)"/>
  <text class="cl" x="6" y="150">cold shelf water</text><text class="hi" x="120" y="120">stratus / sea fog under lid</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/marine_2009.png" alt="Marine layer &amp; sea fog ERA5 t850 z500"><div class="cap">ERA5 · 2009-05-19 15Z</div></div>
  <div class="bd"><span class="chip">Boundary layer · low cloud</span><h3>Marine layer &amp; sea fog</h3>
  <p class="lead">Cool moist marine air trapped under an inversion, filled with stratus and fog.</p>
  <dl class="mech"><dt>Cause</dt><dd>Warm moist air over cold shelf water; a subsidence inversion caps a shallow saturated layer.</dd>
  <dt>Affects</dt><dd>Suppressed insolation and a cool, late-peaking coastal high; dense fog.</dd>
  <dt>Leads to</dt><dd>A known <b>MPAS warm-bias</b> — models burn the stratus off too fast.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> GOES visible/IR loop, ceilometer.</p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDBOX&sdate=2009-05-19&edate=2009-05-20&fmt=text">2009-05-19 · Boston (BOX) — source</a></span><i>"cooler marine-influenced region… Logan may have its warmest temps around 6 PM?"</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Nor'easter plan view">
  <rect width="300" height="168" fill="var(--sky)"/><path d="M0 168 L0 40 C 70 60, 96 130, 150 150 L120 168 Z" fill="var(--land)"/><path d="M0 40 C 70 60, 96 130, 150 150" stroke="var(--line)"/>
  <g fill="none" stroke="var(--soft)" stroke-width="1"><ellipse cx="205" cy="104" rx="20" ry="16"/><ellipse cx="205" cy="104" rx="38" ry="30"/><ellipse cx="205" cy="104" rx="58" ry="46"/></g>
  <text x="199" y="109" font-size="15" font-weight="700" fill="var(--cold)">L</text>
  <path d="M60 60 C 100 40, 150 44, 200 68" stroke="var(--soft)" stroke-width="16" opacity=".22" fill="none"/>
  <line x1="120" y1="150" x2="150" y2="96" stroke="var(--cold)" stroke-width="2" marker-end="url(#mc)"/>
  <text x="86" y="150" class="hi">strong NE winds</text><text class="hi" x="40" y="52">heavy snow NW of low</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/noreaster_2015.png" alt="Nor'easter 2015-01-27 t850 and z500"><div class="cap">ERA5 · 2015-01-27 00Z (Jan 2015 blizzard)</div></div>
  <div class="bd"><span class="chip">Synoptic · cyclogenesis</span><h3>Nor'easter</h3>
  <p class="lead">An intense coastal cyclone with a long fetch of northeasterly winds off the Atlantic.</p>
  <dl class="mech"><dt>Cause</dt><dd>Baroclinic cyclogenesis along the coast / Gulf-Stream gradient, forced by an upper trough and jet.</dd>
  <dt>Affects</dt><dd>Heavy snow/rain NW of the track, damaging NE winds, coastal surge.</dd>
  <dt>Leads to</dt><dd>The Northeast's signature high-impact winter storms.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> MSLP + 500-hPa height/vorticity; IR comma cloud; radar bands.</p>
  <p class="ex"><span class="d">27 Jan 2015 · OKX / BOX</span><i>a benchmark coastal low; 60–90 cm snowfall across eastern New England.</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Miller B redevelopment plan view">
  <rect width="300" height="168" fill="var(--sky)"/><path d="M0 168 L0 30 C 80 55, 110 130, 150 152 L110 168 Z" fill="var(--land)"/><path d="M0 30 C 80 55, 110 130, 150 152" stroke="var(--line)"/>
  <g fill="none" stroke="var(--soft)" stroke-width="1.1" stroke-dasharray="4 3"><ellipse cx="86" cy="80" rx="16" ry="13"/><ellipse cx="86" cy="80" rx="30" ry="24"/></g>
  <text x="80" y="85" font-size="13" font-weight="700" fill="var(--soft)">L</text><text x="58" y="120" class="hi">primary (weakening)</text>
  <g fill="none" stroke="var(--soft)" stroke-width="1.2"><ellipse cx="215" cy="112" rx="16" ry="13"/><ellipse cx="215" cy="112" rx="32" ry="26"/></g>
  <text x="209" y="117" font-size="14" font-weight="700" fill="var(--cold)">L</text><text class="hi" x="194" y="150">new coastal low</text>
  <path d="M104 86 C 150 96, 175 100, 196 108" stroke="var(--warm)" stroke-width="2" fill="none" marker-end="url(#mw)"/><text x="120" y="80">energy transfer →</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/millerb_2011.png" alt="Miller-B redevelopment ERA5 t850 z500"><div class="cap">ERA5 · 2011-01-27 00Z</div></div>
  <div class="bd"><span class="chip">Synoptic · redevelopment</span><h3>Miller-B redevelopment</h3>
  <p class="lead">A primary low fills over the Appalachians while a new low jumps to the coast.</p>
  <dl class="mech"><dt>Cause</dt><dd>The inland low weakens crossing the mountains; upper energy transfers to a secondary coastal low.</dd>
  <dt>Affects</dt><dd>A sudden coastal intensification and a jump in the snow gradient.</dd>
  <dt>Leads to</dt><dd>Notorious busts — the storm "reloads" on the coast hours later.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> MSLP tendency, 500-hPa vorticity handoff, the benchmark 40 °N/70 °W.</p>
  <p class="ex"><span class="d">DJF · OKX / PHI</span><i>the classic "Miller B" secondary cyclogenesis.</i></p></div></article>

</div>

<div class="sec-h"><span class="num">II</span><h2>Terrain-forced</h2><span class="sub">the Appalachians &amp; Great Lakes reshape the low-level flow</span></div>
<div class="grid">

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Cold-air damming wedge">
  <rect width="300" height="168" fill="var(--sky)"/><rect x="70" y="60" width="230" height="30" fill="var(--warm)" opacity=".16"/>
  <line x1="70" y1="90" x2="300" y2="90" stroke="var(--warm)" stroke-width="1.4" marker-end="url(#mw)"/><text class="wm" x="150" y="82">warm air overruns aloft</text>
  <polygon points="8,132 70,40 96,132" fill="var(--land)"/><rect x="96" y="132" width="204" height="36" fill="var(--land)"/><path d="M8 132 H300" stroke="var(--line)"/>
  <polygon points="96,132 300,132 300,112 96,100" fill="var(--cold)" opacity=".42"/>
  <line x1="290" y1="118" x2="150" y2="112" stroke="var(--cold)" stroke-width="2" marker-end="url(#mc)"/>
  <text x="18" y="150" class="hi">Appalachians</text><text class="cl" x="150" y="128">cold dome (wedge)</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/cad_2007.png" alt="CAD 2007-04-02 t850 z500"><div class="cap">ERA5 · 2007-04-02 12Z</div></div>
  <div class="bd"><span class="chip">Meso-α · shallow cold pool</span><h3>Cold-air damming (the wedge)</h3>
  <p class="lead">A shallow dome of cold air trapped against the east slope of the Appalachians.</p>
  <dl class="mech"><dt>Cause</dt><dd>High pressure to the N/NE forces cold, dense air against the mountains; warm air overruns it aloft.</dd>
  <dt>Affects</dt><dd>Overcast, drizzle, and a strongly suppressed daytime high from DC through NYC (8–20 °F cold).</dd>
  <dt>Leads to</dt><dd>Freezing rain and busts — models <b>erode the wedge too fast (warm bias)</b>.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> surface θ / mesonet, 850-hPa T, the in-situ pressure ridge.</p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDBOX&sdate=2007-04-02&edate=2007-04-03&fmt=text">2007-04-02 · Boston (BOX) — source</a></span><i>"stuck in the 40s as a strong wedge of high pressure knifes in from the NNE."</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Downslope warming">
  <rect width="300" height="168" fill="var(--sky)"/><polygon points="60,132 140,44 210,132" fill="var(--land)"/><rect x="0" y="132" width="300" height="36" fill="var(--land)"/><path d="M0 132 H300" stroke="var(--line)"/>
  <rect x="200" y="96" width="100" height="36" fill="var(--warm)" opacity=".20"/>
  <path d="M20 124 C 60 120, 110 70, 140 52" stroke="var(--cold)" stroke-width="2" fill="none" marker-end="url(#mc)"/>
  <path d="M140 52 C 175 70, 210 110, 280 124" stroke="var(--warm)" stroke-width="2.2" fill="none" marker-end="url(#mw)"/>
  <text x="8" y="150">W flow</text><text class="wm" x="212" y="124">warmer, drier</text><text class="hi" x="150" y="40">adiabatic compression</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/downslope_2008.png" alt="Downslope 2008-06-08 t850 z500"><div class="cap">ERA5 · 2008-06-08 18Z</div></div>
  <div class="bd"><span class="chip">Mesoscale · adiabatic</span><h3>Downslope / lee warming</h3>
  <p class="lead">Air descending the lee of the mountains warms and dries by compression.</p>
  <dl class="mech"><dt>Cause</dt><dd>W/NW flow crosses the Appalachians/Berkshires and sinks on the lee side, warming dry-adiabatically.</dd>
  <dt>Affects</dt><dd>A higher, drier maximum at NYC/PHL/DCA and lower dewpoints.</dd>
  <dt>Leads to</dt><dd>Elevated highs and fire-weather days — a mechanism MPAS handles <b>well</b> (resolved terrain).</dd></dl>
  <p class="diag"><b>Diagnose with:</b> NW gradient wind, falling dewpoint, 850-hPa thermal ridge.</p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDBOX&sdate=2008-06-08&edate=2008-06-09&fmt=text">2008-06-08 · Boston (BOX) — source</a></span><i>"highs nudged upward a few degrees… W downsloping flow expected… E-coast beaches will be hotter."</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Lake-effect snow">
  <rect width="300" height="168" fill="var(--sky)"/><rect x="0" y="140" width="150" height="28" fill="var(--cold)" opacity=".30"/><text class="cl" x="30" y="158">warm lake +</text>
  <rect x="150" y="132" width="150" height="36" fill="var(--land)"/><path d="M150 132 H300" stroke="var(--line)"/>
  <line x1="10" y1="60" x2="120" y2="60" stroke="var(--cold)" stroke-width="2.4" marker-end="url(#mc)"/><text class="cl" x="12" y="52">cold air −</text>
  <g fill="var(--soft)" opacity=".8"><ellipse cx="120" cy="96" rx="16" ry="10"/><ellipse cx="150" cy="86" rx="20" ry="12"/><ellipse cx="185" cy="92" rx="18" ry="11"/></g>
  <g stroke="var(--panel)" stroke-width="1.4" opacity=".9"><line x1="150" y1="104" x2="147" y2="130"/><line x1="168" y1="106" x2="165" y2="130"/><line x1="185" y1="104" x2="182" y2="128"/></g>
  <text class="hi" x="150" y="150">snow band</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/lakeeffect_2014.png" alt="Lake-effect snow ERA5 t850 z500"><div class="cap">ERA5 · 2014-11-07 12Z</div></div>
  <div class="bd"><span class="chip">Convective · lake-modified</span><h3>Lake-effect snow</h3>
  <p class="lead">Cold air crossing a warm lake destabilizes and dumps narrow, intense snow bands downwind.</p>
  <dl class="mech"><dt>Cause</dt><dd>Large lake-minus-850-hPa T difference (≥13 °C) plus long fetch drives shallow convection over open water.</dd>
  <dt>Affects</dt><dd>Extremely localized heavy snow and sharp gradients on the downwind shore.</dd>
  <dt>Leads to</dt><dd>Feet of snow over a few km (Tug Hill, Buffalo).</dd></dl>
  <p class="diag"><b>Diagnose with:</b> radar bands, 850-hPa T minus lake temp, boundary-layer depth, fetch.</p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDBOX&sdate=2014-11-07&edate=2014-11-08&fmt=text">2014-11-07 · Boston (BOX) — source</a></span><i>"a swath of rain/snow squalls over western NY state… some of this activity is lake-effect enhanced with CAA coming across."</i></p></div></article>

</div>

<div class="sec-h"><span class="num">III</span><h2>Boundary layer &amp; radiation</h2><span class="sub">the grey-zone processes that make or break a T2m forecast</span></div>
<div class="grid">

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Radiational cooling and valley cold pool">
  <rect width="300" height="168" fill="#0f1a26"/><circle cx="250" cy="24" r="10" fill="none" stroke="var(--faint)" stroke-width="1.4"/><circle cx="246" cy="22" r="10" fill="#0f1a26"/>
  <path d="M0 100 C 70 118, 110 150, 150 150 S 230 118, 300 100 L300 168 L0 168 Z" fill="var(--land)"/>
  <g stroke="var(--warm)" stroke-width="1.4" opacity=".85"><line x1="150" y1="146" x2="150" y2="112" marker-end="url(#mw)"/><line x1="90" y1="132" x2="90" y2="104" marker-end="url(#mw)"/><line x1="210" y1="132" x2="210" y2="104" marker-end="url(#mw)"/></g>
  <path d="M60 150 C 110 150, 190 150, 240 150 L228 132 C 190 138, 110 138, 72 132 Z" fill="var(--cold)" opacity=".5"/>
  <line x1="40" y1="122" x2="260" y2="122" stroke="#cbd6e2" stroke-width="1.2" stroke-dasharray="5 3"/>
  <text x="60" y="24" fill="#cbd6e2">clear · calm · dry night</text><text x="182" y="116" fill="#e8a0a0">IR loss ↑</text><text x="118" y="164" fill="#cbd6e2">cold pool in valley</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/radcool_2016.png" alt="Radiational cooling &amp; cold pools ERA5 t850 z500"><div class="cap">ERA5 · 2016-01-05 06Z</div></div>
  <div class="bd"><span class="chip">Boundary layer · nocturnal</span><h3>Radiational cooling &amp; cold pools</h3>
  <p class="lead">On clear, calm, dry nights the surface radiates away its heat and cold air drains downhill.</p>
  <dl class="mech"><dt>Cause</dt><dd>Strong longwave loss builds a surface inversion; the layer decouples and cold air pools in valleys (aided by snow).</dd>
  <dt>Affects</dt><dd>Drives the daily minimum, frost, and fog; large diurnal range.</dd>
  <dt>Leads to</dt><dd>Valley cold pools — MPAS runs <b>too warm</b> (stable-PBL scheme under-cools).</dd></dl>
  <p class="diag"><b>Diagnose with:</b> sky cover + wind + dewpoint, snow analysis, sfc cooling rate.</p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDBOX&sdate=2016-01-05&edate=2016-01-06&fmt=text">2016-01-05 · Boston (BOX) — source</a></span><i>"high pressure overhead along with clear skies/light winds was leading to an ideal night of radiational cooling."</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Capping inversion mixing out">
  <rect width="300" height="168" fill="var(--sky)"/><rect x="0" y="66" width="300" height="26" fill="var(--warm)" opacity=".22"/>
  <line x1="0" y1="66" x2="300" y2="66" stroke="var(--warm)" stroke-width="1.4" stroke-dasharray="5 3"/><text class="wm" x="6" y="60">elevated mixed layer — the cap</text>
  <rect x="0" y="132" width="300" height="36" fill="var(--land)"/><path d="M0 132 H300" stroke="var(--line)"/>
  <line x1="80" y1="128" x2="80" y2="96" stroke="var(--cold)" stroke-width="1.8"/><line x1="200" y1="128" x2="200" y2="58" stroke="var(--warm)" stroke-width="2.2" marker-end="url(#mw)"/>
  <text x="30" y="120">stuck</text><text class="wm" x="170" y="120">mix-out →</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/capping_2007.png" alt="Capping 2007-07-24 t850 z500"><div class="cap">ERA5 · 2007-07-24 18Z</div></div>
  <div class="bd"><span class="chip">Boundary layer · thermodynamic</span><h3>Capping inversion &amp; "mixing out"</h3>
  <p class="lead">A warm, dry layer aloft caps the boundary layer until the mixed layer erodes it.</p>
  <dl class="mech"><dt>Cause</dt><dd>An elevated mixed layer (warm dry air aloft) lids surface heating; the surface is "stuck" until the mixed layer eats through.</dd>
  <dt>Affects</dt><dd>Temperature flat for hours, then a sudden step-up when it mixes out — or a capped day that never warms.</dd>
  <dt>Leads to</dt><dd>Delayed convective initiation or a warm/cool bust on cap-break timing.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> 12Z sounding cap strength, profiler, surface T trend.</p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDBOX&sdate=2007-07-24&edate=2007-07-25&fmt=text">2007-07-24 · Boston (BOX) — source</a></span><i>"readings will be held in the upper 70s… decent cap in place and with a lack of surface convergence."</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Warm advection midnight high">
  <rect width="300" height="168" fill="var(--sky)"/><polygon points="0,132 0,110 300,70 300,132" fill="var(--cold)" opacity=".22"/><path d="M0 132 H300" stroke="var(--line)"/><rect x="0" y="132" width="300" height="36" fill="var(--land)"/>
  <path d="M20 120 C 120 108, 200 78, 290 56" stroke="var(--warm)" stroke-width="2.2" fill="none" marker-end="url(#mw)"/>
  <text class="wm" x="150" y="70">warm air overruns (isentropic upglide)</text>
  <circle cx="255" cy="112" r="13" fill="none" stroke="var(--ink)" stroke-width="1.4"/><line x1="255" y1="112" x2="255" y2="103" stroke="var(--ink)" stroke-width="1.4"/><line x1="255" y1="112" x2="262" y2="112" stroke="var(--ink)" stroke-width="1.4"/>
  <text class="hi" x="30" y="126">the "high" near midnight</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/warmadv_2008.png" alt="Warm advection 2008-08-04 t850 z500"><div class="cap">ERA5 · 2008-08-04 12Z</div></div>
  <div class="bd"><span class="chip">Synoptic · warm advection</span><h3>Overrunning &amp; the midnight high</h3>
  <p class="lead">Warm air gliding up over a cold surface can make the daily high occur at midnight.</p>
  <dl class="mech"><dt>Cause</dt><dd>Ahead of a warm front, low-level warm advection and isentropic upglide raise the temperature through the night.</dd>
  <dt>Affects</dt><dd>The temperature <em>rises after dark</em>; at NYC/BOS ~20 % of winter daily highs occur near midnight.</dd>
  <dt>Leads to</dt><dd>Timing busts — the reason a same-day run must extend past local midnight.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> 850-hPa T/θ advection, low-level jet, overnight trend. MPAS handles this <b>well</b>.</p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDBOX&sdate=2008-08-04&edate=2008-08-05&fmt=text">2008-08-04 · Boston (BOX) — source</a></span><i>"a warm front approaches Tuesday night… isentropic lift…"</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Nocturnal low-level jet">
  <rect width="300" height="168" fill="#0f1a26"/><rect x="0" y="132" width="300" height="36" fill="var(--land)"/><path d="M0 132 H300" stroke="var(--line)"/>
  <line x1="0" y1="112" x2="300" y2="112" stroke="#cbd6e2" stroke-width="1.1" stroke-dasharray="5 3"/><text x="6" y="106" fill="#cbd6e2">decoupled sfc layer</text>
  <path d="M10 90 H270" stroke="var(--warm)" stroke-width="7" opacity=".35"/><line x1="20" y1="90" x2="285" y2="90" stroke="var(--warm)" stroke-width="2.4" marker-end="url(#mw)"/>
  <text x="60" y="82" fill="#e8a0a0">nocturnal low-level jet</text><text x="80" y="128" fill="#cbd6e2">moisture &amp; warm advection ↑</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/llj_2008.png" alt="Nocturnal low-level jet ERA5 t850 z500"><div class="cap">ERA5 · 2008-06-22 06Z</div></div>
  <div class="bd"><span class="chip">Boundary layer · inertial</span><h3>Nocturnal low-level jet</h3>
  <p class="lead">After sunset the surface decouples and a fast wind ribbon accelerates just above it.</p>
  <dl class="mech"><dt>Cause</dt><dd>Frictional decoupling lets the low-level wind undergo an inertial oscillation and accelerate into a jet.</dd>
  <dt>Affects</dt><dd>Rapid overnight moisture and warm-air transport; feeds dew, fog, elevated convection.</dd>
  <dt>Leads to</dt><dd>Overnight MCS development and the midnight warm-up.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> VAD wind profile, 925/850-hPa wind max, decoupling time.</p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDOKX&sdate=2008-06-22&edate=2008-06-23&fmt=text">2008-06-22 · New York (OKX) — source</a></span><i>"training of storms possible as the low level jet aligns with upper flow."</i></p></div></article>

</div>

<div class="sec-h"><span class="num">IV</span><h2>Winter precipitation &amp; explosive cyclones</h2><span class="sub">where a shallow cold layer decides everything</span></div>
<div class="grid">

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Freezing rain temperature profile">
  <rect width="300" height="168" fill="var(--sky)"/><line x1="150" y1="8" x2="150" y2="160" stroke="var(--line)" stroke-width="1"/><text x="154" y="18">0°C</text>
  <rect x="8" y="8" width="142" height="152" fill="var(--cold)" opacity=".10"/><rect x="150" y="8" width="142" height="152" fill="var(--warm)" opacity=".08"/>
  <path d="M112 12 L128 44 L188 78 L150 112 L120 158" fill="none" stroke="var(--ink)" stroke-width="2"/>
  <text class="wm" x="176" y="72">warm nose &gt;0</text><text class="cl" x="30" y="150">cold surface &lt;0</text><text x="18" y="20">snow</text><text x="196" y="96">melts→rain</text><text class="cl" x="60" y="130">refreezes</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/freezingrain_2008.png" alt="Freezing rain &amp; ice storms ERA5 t850 z500"><div class="cap">ERA5 · 2008-01-03 12Z</div></div>
  <div class="bd"><span class="chip">Winter · thermal profile</span><h3>Freezing rain &amp; ice storms</h3>
  <p class="lead">Snow melts in a warm layer aloft, then the rain refreezes on a sub-freezing surface.</p>
  <dl class="mech"><dt>Cause</dt><dd>A shallow surface cold layer (often CAD) beneath an elevated <em>warm nose</em> &gt; 0 °C; precip melts then supercools.</dd>
  <dt>Affects</dt><dd>Rain that freezes on contact — ice accretion on every surface.</dd>
  <dt>Leads to</dt><dd>Damaging ice storms; the depth of the cold layer is the whole forecast.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> the vertical T sounding (twice crossing 0 °C), surface wet-bulb, CAD strength.</p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDBOX&sdate=2008-01-03&edate=2008-01-04&fmt=text">2008-01-03 · Boston (BOX) — source</a></span><i>"southern NH where the deep snowpack may provide sufficient low level cold air for the risk of a period of freezing rain/drizzle."</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Bomb cyclone">
  <rect width="300" height="168" fill="var(--sky)"/><g fill="none" stroke="var(--soft)" stroke-width="1.1"><ellipse cx="160" cy="88" rx="14" ry="12"/><ellipse cx="160" cy="88" rx="30" ry="26"/><ellipse cx="160" cy="88" rx="48" ry="42"/><ellipse cx="160" cy="88" rx="68" ry="60"/></g>
  <text x="153" y="93" font-size="16" font-weight="700" fill="var(--cold)">L</text>
  <path d="M160 40 A 48 48 0 1 1 118 66" fill="none" stroke="var(--warm)" stroke-width="2" marker-end="url(#mw)"/>
  <text class="wm" x="196" y="40">≥24 hPa / 24 h</text><text class="hi" x="60" y="150">explosive deepening</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/bomb_2018.png" alt="Bomb cyclone 2018-01-04 t850 z500"><div class="cap">ERA5 · 2018-01-04 12Z (Jan 2018 bomb)</div></div>
  <div class="bd"><span class="chip">Synoptic · bombogenesis</span><h3>Bomb cyclone</h3>
  <p class="lead">A cyclone whose central pressure falls at least 24 hPa in 24 hours.</p>
  <dl class="mech"><dt>Cause</dt><dd>Strong baroclinicity, a favorable upper jet/trough, and latent-heat release (over the Gulf Stream) drive explosive deepening.</dd>
  <dt>Affects</dt><dd>Extreme wind, heavy snow, rapid pressure falls over the NE waters and coast.</dd>
  <dt>Leads to</dt><dd>The most intense coastal storms; blizzards and coastal flooding.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> 24-h MSLP tendency, 300-hPa jet, 500-hPa vorticity, SST gradient.</p>
  <p class="ex"><span class="d">4 Jan 2018 · offshore benchmark</span><i>pressure fell &gt; 50 hPa; hurricane-force winds off New England.</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Alberta clipper track">
  <rect width="300" height="168" fill="var(--sky)"/><rect x="0" y="0" width="300" height="90" fill="var(--cold)" opacity=".12"/>
  <path d="M20 34 C 110 44, 200 96, 285 132" stroke="var(--soft)" stroke-width="2" fill="none" stroke-dasharray="6 4" marker-end="url(#mk)"/>
  <g fill="none" stroke="var(--soft)" stroke-width="1.1"><ellipse cx="150" cy="72" rx="12" ry="10"/><ellipse cx="150" cy="72" rx="24" ry="20"/></g>
  <text x="145" y="76" font-size="12" font-weight="700" fill="var(--cold)">L</text>
  <text x="30" y="26" class="hi">fast NW → SE track</text><text class="cl" x="20" y="150">arctic air surges behind</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/clipper_2008.png" alt="Alberta clipper ERA5 t850 z500"><div class="cap">ERA5 · 2008-01-19 12Z</div></div>
  <div class="bd"><span class="chip">Synoptic · fast mover</span><h3>Alberta clipper</h3>
  <p class="lead">A fast, moisture-starved shortwave low diving southeast out of Canada.</p>
  <dl class="mech"><dt>Cause</dt><dd>A quick Canadian shortwave with little Gulf moisture races SE across the northern tier.</dd>
  <dt>Affects</dt><dd>A swath of light, fluffy snow followed by a sharp shot of arctic cold and gusty NW winds.</dd>
  <dt>Leads to</dt><dd>Temperature crashes and wind chill behind the system.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> 500-hPa shortwave speed, thickness fall, post-frontal wind.</p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDBOX&sdate=2008-01-19&edate=2008-01-20&fmt=text">2008-01-19 · Boston (BOX) — source</a></span><i>"a clipper moves across the region Tue… suspect might be a little too optimistic with the high temps."</i></p></div></article>

</div>

<div class="sec-h"><span class="num">V</span><h2>Convective &amp; mesoscale boundaries</h2><span class="sub">outflow, bows, and moisture gradients</span></div>
<div class="grid">

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Gust front cold pool">
  <rect width="300" height="168" fill="var(--sky)"/><rect x="0" y="132" width="300" height="36" fill="var(--land)"/><path d="M0 132 H300" stroke="var(--line)"/>
  <g fill="var(--soft)" opacity=".85"><ellipse cx="210" cy="52" rx="46" ry="20"/><ellipse cx="180" cy="60" rx="26" ry="14"/></g>
  <g stroke="var(--cold)" stroke-width="1.6" opacity=".8"><line x1="185" y1="72" x2="180" y2="120" marker-end="url(#mc)"/><line x1="205" y1="72" x2="200" y2="120" marker-end="url(#mc)"/></g>
  <path d="M170 132 C 130 128, 90 128, 40 130 L40 150 L170 150 Z" fill="var(--cold)" opacity=".4"/>
  <line x1="40" y1="126" x2="40" y2="150" stroke="var(--cold)" stroke-width="2"/><polygon points="40,130 32,135 40,140" fill="var(--cold)"/>
  <text x="150" y="60" fill="var(--panel)">downdraft</text><text class="cl" x="60" y="146">cold pool</text><text class="hi" x="6" y="124">gust front →</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/gustfront_2013.png" alt="Gust front / cold pool ERA5 t850 z500"><div class="cap">ERA5 · 2013-07-08 18Z</div></div>
  <div class="bd"><span class="chip">Storm-scale · outflow</span><h3>Gust front / cold pool</h3>
  <p class="lead">A thunderstorm's rain-cooled downdraft spreads out as a cold, gusty density current.</p>
  <dl class="mech"><dt>Cause</dt><dd>Evaporative cooling in the downdraft builds a cold pool that surges outward.</dd>
  <dt>Affects</dt><dd>An abrupt wind shift, gust, and temperature drop at the leading gust front.</dd>
  <dt>Leads to</dt><dd>New convection along the convergence, and micro-timing of T2m a coarse model smears.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> radar thin-line, pressure jump &amp; temperature drop, mesonet.</p>
  <p class="ex"><span class="d"><a href="https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py?pil=AFDBOX&sdate=2013-07-08&edate=2013-07-09&fmt=text">2013-07-08 · Boston (BOX) — source</a></span><i>"surface analysis shows a weak boundary… perhaps outflow from morning convection is moving through."</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Derecho bow echo">
  <rect width="300" height="168" fill="var(--sky)"/><path d="M70 30 C 140 20, 200 40, 220 84 C 200 128, 140 148, 70 138 C 120 100, 120 68, 70 30 Z" fill="var(--warm)" opacity=".30" stroke="var(--warm)" stroke-width="1.2"/>
  <line x1="285" y1="84" x2="150" y2="84" stroke="var(--cold)" stroke-width="2.6" marker-end="url(#mc)"/>
  <text class="cl" x="196" y="78">rear-inflow jet</text><text class="wm" x="86" y="88">bow echo</text><text class="hi" x="40" y="158">widespread damaging wind →</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/derecho_2012.png" alt="Derecho 2012-06-29 t850 z500"><div class="cap">ERA5 · 2012-06-29 18Z (heat-ridge "ring of fire")</div></div>
  <div class="bd"><span class="chip">Meso-β · progressive MCS</span><h3>Derecho</h3>
  <p class="lead">A long-lived, fast bow-echo complex that produces a swath of straight-line wind damage.</p>
  <dl class="mech"><dt>Cause</dt><dd>An organized MCS with a strong cold pool and a descending <em>rear-inflow jet</em> accelerates as a bow echo, often on the north flank of a heat ridge.</dd>
  <dt>Affects</dt><dd>Widespread 60–100 mph winds along a hundreds-of-km track.</dd>
  <dt>Leads to</dt><dd>Major wind damage and outages.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> radar bow &amp; rear-inflow notch, MUCAPE + deep shear, the 850-hPa ring-of-fire.</p>
  <p class="ex"><span class="d">29 Jun 2012 · DC/Mid-Atlantic (LWX)</span><i>a derecho ran from Indiana to the coast with 80+ mph gusts.</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Dryline">
  <rect width="300" height="168" fill="var(--sky)"/><rect x="150" y="0" width="150" height="168" fill="#3a7d3a" opacity=".16"/><rect x="0" y="0" width="150" height="168" fill="var(--land)" opacity=".22"/>
  <line x1="150" y1="16" x2="150" y2="152" stroke="var(--warm)" stroke-width="2" stroke-dasharray="2 3"/>
  <text x="20" y="150">dry desert air</text><text x="176" y="150" fill="#3a7d3a">moist Gulf air (high Td)</text>
  <g fill="var(--soft)" opacity=".8"><ellipse cx="150" cy="44" rx="16" ry="10"/><ellipse cx="150" cy="70" rx="12" ry="8"/></g><text class="wm" x="122" y="26">dryline</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/dryline_2013.png" alt="Dryline ERA5 t850 z500"><div class="cap">ERA5 · 2013-05-20 21Z (Moore, OK)</div></div>
  <div class="bd"><span class="chip">Mesoscale · moisture boundary</span><h3>Dryline</h3>
  <p class="lead">A sharp moisture gradient in the southern Plains that focuses severe convection.</p>
  <dl class="mech"><dt>Cause</dt><dd>Moist Gulf air meets dry, well-mixed desert air; the boundary mixes east by day, retreats at night.</dd>
  <dt>Affects</dt><dd>Big dewpoint contrast and convergence across a few km.</dd>
  <dt>Leads to</dt><dd>Supercells and tornado outbreaks (a Plains feature — the NE analogue is the sea-breeze / backdoor Td boundary).</dd></dl>
  <p class="diag"><b>Diagnose with:</b> surface dewpoint gradient, 2-m mixing ratio, convergence, cap.</p>
  <p class="ex"><span class="d">Spring · Southern Plains</span><i>the classic severe-weather focus.</i></p></div></article>

</div>

<div class="sec-h"><span class="num">VI</span><h2>Large-scale patterns</h2><span class="sub">the planetary waves that set the stage for days</span></div>
<div class="grid">

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Omega block">
  <rect width="300" height="168" fill="var(--sky)"/>
  <path d="M0 120 C 40 122, 60 128, 78 96 C 96 44, 150 40, 178 60 C 200 76, 214 120, 250 120 C 270 120, 288 116, 300 112" fill="none" stroke="var(--ink)" stroke-width="2.2"/>
  <path d="M0 138 C 44 140, 66 146, 86 118 C 104 74, 150 70, 176 88 C 198 104, 214 138, 252 138 C 274 138, 290 134, 300 130" fill="none" stroke="var(--soft)" stroke-width="1.2"/>
  <text class="wm" x="108" y="60">blocking ridge Ω</text><text class="wm" x="112" y="98">heat / drought</text><text class="cl" x="20" y="112">cool</text><text class="cl" x="256" y="112">cool</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/omegablock_2012.png" alt="Omega block 2012-07-06 t850 z500"><div class="cap">ERA5 · 2012-07-06 12Z (Jul 2012 heat)</div></div>
  <div class="bd"><span class="chip">Planetary · blocking</span><h3>Omega block</h3>
  <p class="lead">A persistent, amplified ridge flanked by two lows — an Ω in the 500-hPa flow.</p>
  <dl class="mech"><dt>Cause</dt><dd>The jet buckles into a stationary high-amplitude ridge with cutoff lows on each side; it locks in for days.</dd>
  <dt>Affects</dt><dd>Prolonged heat and drought under the ridge, cool and wet on the flanks.</dd>
  <dt>Leads to</dt><dd>Heat waves and air-stagnation; multi-day forecast persistence.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> 500-hPa height anomaly, blocking indices, ridge-axis position.</p>
  <p class="ex"><span class="d">Jul 2012 · Northeast heat</span><i>with the ridge overhead, the daily max ran several degrees above normal for a week.</i></p></div></article>

<article class="sys"><div class="fig"><svg viewBox="0 0 300 168" role="img" aria-label="Santa Ana offshore downslope">
  <rect width="300" height="168" fill="var(--sky)"/><polygon points="40,132 120,52 200,132" fill="var(--land)"/><rect x="0" y="132" width="300" height="36" fill="var(--land)"/><path d="M0 132 H300" stroke="var(--line)"/>
  <rect x="0" y="140" width="40" height="28" fill="var(--cold)" opacity=".28"/><text class="cl" x="4" y="158">Pacific</text>
  <text x="150" y="30" class="hi">HIGH (Great Basin)</text>
  <path d="M250 96 C 200 96, 160 66, 120 54" stroke="var(--warm)" stroke-width="1.8" fill="none" marker-end="url(#mw)"/>
  <path d="M120 54 C 90 74, 60 112, 20 124" stroke="var(--warm)" stroke-width="2.4" fill="none" marker-end="url(#mw)"/>
  <rect x="0" y="96" width="60" height="36" fill="var(--warm)" opacity=".2"/>
  <text class="wm" x="6" y="120">hot, dry, fire wx</text><text x="150" y="88">offshore flow · compresses</text></svg></div>
  <div class="realfig"><img src="/images/wx_systems/santaana_2007.png" alt="Santa Ana 2007-10-22 t850 z500"><div class="cap">ERA5 · 2007-10-22 12Z (Oct 2007 CA fires)</div></div>
  <div class="bd"><span class="chip">Synoptic · offshore downslope</span><h3>Santa Ana (offshore) wind</h3>
  <p class="lead">High pressure inland drives dry air <em>offshore</em>, warming and drying as it descends to the coast.</p>
  <dl class="mech"><dt>Cause</dt><dd>A Great-Basin high forces a gradient toward the coast; air sinks down the mountains, compressing and drying.</dd>
  <dt>Affects</dt><dd>Hot, bone-dry, gusty conditions at the CA coast — the <em>opposite</em> of the marine-layer regime.</dd>
  <dt>Leads to</dt><dd>Critical fire weather. The West-Coast contrast to the NE onshore/sea-breeze world.</dd></dl>
  <p class="diag"><b>Diagnose with:</b> offshore MSLP gradient, 850-hPa warm/dry advection, RH &amp; wind.</p>
  <p class="ex"><span class="d">Oct 2007 · Southern California</span><i>the mirror image of the marine layer — downslope wins, and LAX bakes.</i></p></div></article>

</div>

<p style="font-size:12.5px;color:var(--soft);border-top:1px solid var(--line);margin-top:26px;padding-top:14px">
<b>Sources.</b> Case maps: ERA5 reanalysis (1.5°, local archive), 850-hPa temperature and 500-hPa height at the stated time.
Forecaster quotes: NWS Area Forecast Discussions (WFOs Boston/BOX, New York/OKX, Mount Holly/PHI, Baltimore–Washington/LWX)
via the Iowa Environmental Mesonet text archive — each dated case links to its source product. Schematics are hand-drawn (SVG).
</p>

</div>

