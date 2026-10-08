---
title: "Special Weather Systems of the Northeastern United States"
excerpt: "A guide for non-specialists to 21 systems that shape the weather of the northeastern United States, each illustrated with a schematic and a reanalysis map of a real case.<br/><img src='/images/wx_systems_v3/noreaster_2015.png' style='max-width: 60%; height: auto;'>"
collection: portfolio
---

{% include base_path %}
<link rel="stylesheet" href="{{ base_path }}/assets/css/journal.css">
<style>
.wx .wx-def { font-size: 11.5pt; margin: 0.3em 0 0.8em 0; }
.wx .wx-sys { margin: 0 0 2.2em 0; }
.wx .wx-box { border: 1px solid #000; border-radius: 0; box-shadow: none; padding: 10px 14px 6px 14px; margin: 1.2em 0 1.6em 0; background: #fff; }
.wx .wx-box h2 { font-size: 11.5pt; margin: 0 0 0.5em 0; }
.wx .wx-box dl { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px 24px; margin: 0; font-size: 10pt; line-height: 1.4; }
.wx .wx-box dl > div { min-width: 0; }
.wx .wx-box dt, .wx .wx-box dd { font-family: "STIX Two Text", "Times New Roman", Times, serif; font-size: 10pt; line-height: 1.4; color: #000; }
.wx .wx-box dt { font-weight: 700; margin: 0; }
.wx .wx-box dd { margin: 0; }
.wx .wx-toc { font-size: 10pt; margin: 0.4em 0 1em 0; padding-left: 1.6em; }
.wx .wx-toc li { margin: 0; }
.wx .wx-tablewrap { width: 100%; overflow-x: auto; margin: 0 0 1.4em 0; }
.wx table.jn-table { display: table; table-layout: auto; }
.wx table.jn-table thead { background: none; border: 0; }
.wx table.jn-table tbody tr { background: none; }
.wx table.jn-table td:first-child { white-space: nowrap; }
.wx .wx-legend { font-family: Helvetica, Arial, sans-serif; font-size: 9pt; border-top: 1px solid #000; border-bottom: 1px solid #000; padding: 6px 0; margin: 0 0 1.6em 0; }
.wx .wx-legend p { margin: 0 0 4px 0; font-family: "STIX Two Text", "Times New Roman", Times, serif; font-size: 9.5pt; }
.wx .wx-legend ul { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 4px 20px; }
.wx .wx-legend li { display: inline-flex; align-items: center; gap: 6px; margin: 0; }
.wx .wx-legend svg { display: inline-block; flex: none; }
.wx figure.jn-fig.wx-schem { display: block; width: 100%; }
.wx figure.jn-fig.wx-schem svg { width: 100%; max-width: 560px; height: auto; display: block; margin: 0 auto; background: #fff; }
.wx figure.jn-fig.wx-schem .wx-two { display: flex; flex-wrap: wrap; gap: 12px 16px; align-items: flex-start; justify-content: center; max-width: 760px; margin: 0 auto; }
.wx figure.jn-fig.wx-schem .wx-two > * { flex: 1 1 260px; max-width: calc(50% - 8px); min-width: 0; }
.wx figure.jn-fig.wx-schem .wx-two svg { max-width: 100%; }
.wx figure.jn-fig.wx-schem .wx-two img { width: 100%; height: auto; display: block; margin: 0 auto; }
.wx figure.jn-fig img { width: 100%; height: auto; border: 0; }
.wx figure.wx-map a, .wx figure.wx-map a:hover { border-bottom: 0; display: block; }
.wx blockquote.wx-afd { border-left: 2px solid #999; border-radius: 0; margin: 0.6em 0 1em 0; padding: 2px 0 2px 12px; font-size: 10pt; font-style: normal; color: #000; background: none; }
.wx blockquote.wx-afd p { font-style: italic; margin: 0 0 4px 0; }
.wx blockquote.wx-afd footer { font-size: 9pt; font-style: normal; color: #333; }
.wx blockquote.wx-afd footer::before { content: none; }
@media (max-width: 700px) {
  .wx .wx-box dl { grid-template-columns: 1fr; }
  .wx .wx-def { font-size: 11pt; }
  .wx table.jn-table { font-size: 9pt; }
  .wx table.jn-table td:first-child { white-space: normal; }
  .wx figure.jn-fig.wx-schem .wx-two > * { max-width: 100%; }
  .wx figcaption { text-align: left; }
}
</style>

<div class="jn wx" markdown="0">

<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
  <marker id="ar-k" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L10,5 L0,9 z" fill="#000000"/></marker>
  <marker id="ar-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L10,5 L0,9 z" fill="#2166ac"/></marker>
  <marker id="ar-r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L10,5 L0,9 z" fill="#b2182b"/></marker>
</defs></svg>

<p class="jn-abstract"><b>Abstract.</b> This page describes 21 weather systems that shape day-to-day weather in the northeastern United States, from the sea breeze and the nor’easter to cold air trapped against the Appalachians. Two systems from elsewhere in the country, the Great Plains dryline and the California Santa Ana wind, are included for contrast. The page is written for readers with a science background but no training in meteorology. Each entry opens with a one-sentence definition and then describes how the system forms, how it changes temperature, wind, cloud and precipitation, and how forecasters recognize it, with reference to published studies. Each is illustrated with a schematic drawn for this page and a map of a real case from a reanalysis of past weather, and most entries quote the National Weather Service forecasters who handled that case.</p>

<ol class="wx-toc">
  <li><a href="#sec-1">Coastal and marine systems</a></li>
  <li><a href="#sec-2">Terrain-forced systems</a></li>
  <li><a href="#sec-3">Boundary layer and radiation</a></li>
  <li><a href="#sec-4">Winter precipitation and rapidly deepening cyclones</a></li>
  <li><a href="#sec-5">Convective and mesoscale boundaries</a></li>
  <li><a href="#sec-6">Large-scale patterns</a></li>
</ol>
<p class="jn-small">Also: <a href="#how-to-read">How to read this page</a> &middot; <a href="#table-1">Table 1</a> &middot; <a href="#methods">Data and methods</a> &middot; <a href="#references">References</a></p>

<div class="wx-box" id="how-to-read">
<h2>How to read this page</h2>
<p class="jn-small">These notes can be skimmed now and consulted later, when a map or a unit is unclear.</p>
<dl>
  <div>
    <dt>Pressure levels as heights</dt>
    <dd>Air pressure falls with height, so meteorologists often name a height by its pressure in hectopascals (hPa; 1 hPa equals 1 millibar, mb). Approximate heights: 1000 hPa, near sea level; 925 hPa, 750 m (2500 ft); 850 hPa, 1.5 km (5000 ft); 700 hPa, 3 km (10&nbsp;000 ft); 500 hPa, 5.5 km (18&nbsp;000 ft), where about half the mass of the atmosphere lies below.</dd>
  </div>
  <div>
    <dt>Heights on upper-level maps</dt>
    <dd>Maps of one pressure level show contours of the height of that pressure surface above sea level, in decameters (dam; 1 dam = 10 m, so 552 dam is 5520 m). Low heights mark troughs and cold air, high heights ridges and warm air. An anomaly is the difference from the long-term average for that place and season.</dd>
  </div>
  <div>
    <dt>Sea-level pressure</dt>
    <dd>Mean sea-level pressure (MSLP) is the pressure measured at a station and adjusted to sea level, so that stations at different elevations can be compared. Lines of equal pressure are called isobars. On maps H marks a center of high pressure and L a center of low pressure.</dd>
  </div>
  <div>
    <dt>Temperature and dewpoint</dt>
    <dd>The 2-m temperature is the air temperature 2 m above the ground, what an ordinary outdoor thermometer reads. The dewpoint is the temperature to which the air would have to cool to become saturated; a higher dewpoint means more water vapor. In the text, surface temperatures are given in &deg;F with &deg;C in parentheses; the maps use &deg;C. Temperature differences on the maps are often given in kelvin (K): a difference of 1&nbsp;K equals 1&nbsp;&deg;C (1.8&nbsp;&deg;F).</dd>
  </div>
  <div>
    <dt>Wind</dt>
    <dd>Winds are named for the direction they blow <i>from</i>: a northeast wind blows from the northeast toward the southwest. Surface wind is measured 10 m above the ground (the 10-m wind). On maps a wind barb's shaft points into the wind; each long feather is 10 knots (kt), a short feather 5 kt and a triangular pennant 50 kt. One knot is about 0.5 m s<sup>&minus;1</sup> or 1.15 mph.</dd>
  </div>
  <div>
    <dt>Ridges, troughs and inversions</dt>
    <dd>A ridge is an elongated area of high pressure and a trough one of low pressure; higher up they appear as northward and southward bends in the jet stream, the band of fastest winds about 9&ndash;12 km up. Temperature normally falls with height; an inversion is a layer where it rises instead, and it acts as a lid on mixing. A sounding is a profile of temperature, humidity and wind against height, measured by an instrument carried up by a weather balloon, usually at 0000 and 1200 UTC.</dd>
  </div>
  <div>
    <dt>Contours and shading</dt>
    <dd>On the maps, lines (contours) join points with equal values of one quantity, and color shading shows a second quantity. Each figure caption says which is which and gives the units. Units with negative powers are rates: m&nbsp;s<sup>&minus;1</sup> is meters per second, mm&nbsp;h<sup>&minus;1</sup> millimeters per hour, and 10<sup>&minus;5</sup>&nbsp;s<sup>&minus;1</sup> (a typical rate at which large-scale winds converge or spin) is 0.00001 per second. Latitude and longitude are given in degrees north of the equator (&deg;N) and west of Greenwich (&deg;W); New England lies at about 41&ndash;47&deg;N.</dd>
  </div>
  <div>
    <dt>ERA5 reanalysis</dt>
    <dd>A reanalysis is a reconstruction of past weather made by combining historical observations with a weather-forecast model. ERA5 gives hourly values from 1940 onward on a grid of 0.25&deg; of latitude and longitude, about 20&ndash;30 km between grid points over the Northeast. Features only a few grid lengths wide, such as a sea-breeze front or a thunderstorm gust front, are smoothed out or missed, so for those the ERA5 map shows the setting, and surface stations and radar show the feature itself.</dd>
  </div>
  <div>
    <dt>Time</dt>
    <dd>Times are given in Coordinated Universal Time (UTC, written &ldquo;Z&rdquo; on weather maps), with local time in parentheses. Eastern Standard Time (EST) is UTC&nbsp;&minus;&nbsp;5&nbsp;h and Eastern Daylight Time (EDT) is UTC&nbsp;&minus;&nbsp;4&nbsp;h, so 1800 UTC is 1&nbsp;p.m. EST in winter and 2&nbsp;p.m. EDT in summer. Central and Pacific daylight times (CDT, PDT) are UTC&nbsp;&minus;&nbsp;5&nbsp;h and UTC&nbsp;&minus;&nbsp;7&nbsp;h.</dd>
  </div>
  <div>
    <dt>Forecaster quotations</dt>
    <dd>National Weather Service (NWS) forecast offices publish an Area Forecast Discussion (AFD) several times a day, a technical note explaining the reasoning behind the forecast. Quotations come from the offices for Boston (BOX, located in Norton, Mass.; older products are headed &ldquo;Taunton&rdquo;), New York (OKX, Upton, N.Y.), Philadelphia (PHI, Mount Holly, N.J.), Baltimore/Washington (LWX, Sterling, Va.) and Buffalo (BUF). Each links to the archived text of the product it is taken from.</dd>
  </div>
  <div>
    <dt>Sources</dt>
    <dd>Published work is cited by author and year, for example <a href="#ref-miller2003">Miller et al. (2003)</a>, and listed with its DOI under <a href="#references">References</a>. Words in quotation marks are quoted exactly from the source; all other text is paraphrase. Forecasting methods described without a citation are standard National Weather Service practice.</dd>
  </div>
</dl>
</div>

<p class="jn-tabcap" id="table-1"><b>Table 1.</b> The 21 systems described on this page. &ldquo;Scale&rdquo; is the typical size; &ldquo;season&rdquo; is when the system is most common or matters most in the Northeast. The dryline and the Santa Ana wind do not occur in the Northeast and are included for contrast.</p>
<div class="wx-tablewrap">
<table class="jn-table">
<thead>
<tr><th>System</th><th>Scale</th><th>Season</th><th>Main effect in the Northeast</th></tr>
</thead>
<tbody>
<tr><td><a href="#sea-breeze">1.1 Sea breeze</a></td><td>Front reaches tens of km inland</td><td>Sunny days, mainly spring and summer</td><td>Cooler, more humid afternoons at the shore; earlier daily high at the coast</td></tr>
<tr><td><a href="#backdoor-front">1.2 Backdoor cold front</a></td><td>Front hundreds of km long; shallow cold air</td><td>Spring and early summer</td><td>Sudden drop of 10&ndash;30 &deg;F (6&ndash;17 &deg;C) on a northeast wind while inland areas can stay warm</td></tr>
<tr><td><a href="#coastal-front">1.3 Coastal front</a></td><td>Hundreds of km long; temperature change across about 10 km</td><td>Late autumn to early spring</td><td>Sharp temperature contrast near the coast, often the line between rain and snow</td></tr>
<tr><td><a href="#marine-layer">1.4 Marine layer and sea fog</a></td><td>Tens to hundreds of km of coast and water</td><td>Late spring and summer</td><td>Fog and low cloud keep the shore cool and gray</td></tr>
<tr><td><a href="#noreaster">1.5 Nor’easter</a></td><td>About 1000 km</td><td>Autumn to spring, most often in winter</td><td>Heavy snow or rain, strong northeast winds, coastal flooding</td></tr>
<tr><td><a href="#miller-b">1.6 Miller type B redevelopment</a></td><td>About 1000 km</td><td>Winter</td><td>A new coastal low takes over from an inland one, making snow totals hard to forecast</td></tr>
<tr><td><a href="#cold-air-damming">2.1 Cold-air damming</a></td><td>Several hundred km along the mountains; cold layer usually under 1 km deep</td><td>Mainly the cool season</td><td>Overcast, cold days with drizzle or fog east of the Appalachians (also east of the southern New England hills); sets up freezing rain</td></tr>
<tr><td><a href="#downslope">2.2 Downslope (lee) warming</a></td><td>Downwind of ridges about 1 km high</td><td>Any season</td><td>A dry, gusty west wind and an afternoon high a few &deg;F higher; can stop the sea breeze</td></tr>
<tr><td><a href="#lake-effect">2.3 Lake-effect snow</a></td><td>Narrow bands downwind of the lakes; snow depth can vary by 100 cm (40 in) within 50 km</td><td>November to January</td><td>Very heavy, localized snow downwind of the Great Lakes, e.g. over 4 ft (1.2 m) near Buffalo in Nov 2014</td></tr>
<tr><td><a href="#radiational-cooling">3.1 Radiational cooling and cold pools</a></td><td>Valleys and low ground, a few km</td><td>Clear, calm nights; strongest over fresh snow</td><td>Temperatures can differ by 10 &deg;F (5&ndash;6 &deg;C) or more over a few miles; frost and fog</td></tr>
<tr><td><a href="#mixing-out">3.2 Morning inversion and mixing out</a></td><td>Lowest few hundred meters</td><td>Any season; mornings after cold nights</td><td>Temperature flat through the morning, then a rise of several degrees within an hour once the inversion breaks</td></tr>
<tr><td><a href="#overrunning">3.3 Overrunning and the midnight high</a></td><td>Hundreds of km ahead of a warm front</td><td>Mainly winter</td><td>Temperatures that rise overnight; about one winter day in five at Boston and one in four at New York has its high in the first or last hour of the day</td></tr>
<tr><td><a href="#low-level-jet">3.4 Nocturnal low-level jet</a></td><td>A band of fast wind a few hundred meters above the ground</td><td>At night, peaking after midnight</td><td>Carries warm, humid air north overnight and can feed nighttime storms; strongest over the Great Plains</td></tr>
<tr><td><a href="#freezing-rain">4.1 Freezing rain and ice storms</a></td><td>Warm layer 1&ndash;3 km up over a shallow freezing layer</td><td>Winter</td><td>Rain at 28&ndash;32 &deg;F that freezes on contact; a quarter inch (6 mm) of ice brings down branches and power lines</td></tr>
<tr><td><a href="#bomb-cyclone">4.2 Bomb cyclone</a></td><td>About 1000 km or more</td><td>Cold season, mainly over the ocean</td><td>Central pressure falls at least about 18&ndash;20 hPa in 24 h; rapidly rising winds, heavy snow or rain, coastal flooding</td></tr>
<tr><td><a href="#alberta-clipper">4.3 Alberta clipper</a></td><td>Small, fast-moving low</td><td>Mostly December and January</td><td>A few inches of light, powdery snow, then gusty northwest winds and sharp cooling</td></tr>
<tr><td><a href="#gust-front">5.1 Gust front and cold pool</a></td><td>Cold pool about 1 km deep, narrower than a model grid</td><td>Thunderstorm season</td><td>Sudden gust and wind shift; temperature can fall more than 10 &deg;F (5.5 &deg;C) within minutes</td></tr>
<tr><td><a href="#derecho">5.2 Derecho</a></td><td>Damage swath at least 400 km (250 mi) long</td><td>Thunderstorm season</td><td>Gusts of 60&ndash;90 mph, fallen trees, long power outages; most occur in the central United States, some reach the Northeast</td></tr>
<tr><td><a href="#dryline">5.3 Dryline</a></td><td>Moisture change across a few to tens of km</td><td>Spring; most often mid- to late May</td><td>Not a Northeast feature; a Great Plains moisture boundary where severe storms and tornadoes form</td></tr>
<tr><td><a href="#omega-block">6.1 Omega block</a></td><td>Several thousand km; lasts a week or more</td><td>Any season</td><td>Persistent weather: clear, warm, dry days under the ridge, cool and showery days under the lows</td></tr>
<tr><td><a href="#santa-ana">6.2 Santa Ana wind</a></td><td>Southern California mountains, passes and coast</td><td>Autumn to early spring</td><td>Not a Northeast feature; hot, very dry, gusty wind and severe fire weather, the opposite of the onshore marine regime</td></tr>
</tbody>
</table>
</div>

<div class="wx-legend">
<p><b>Key to the schematics.</b> The schematics are simplified drawings, not to scale. Cross-sections are vertical slices through the atmosphere; maps have north at the top.</p>
<ul>
  <li><svg width="44" height="16" viewBox="0 0 44 16" aria-hidden="true"><line x1="2" y1="5" x2="42" y2="5" stroke="#2166ac" stroke-width="2"/><polygon points="9,5 17,5 13,13" fill="#2166ac"/><polygon points="25,5 33,5 29,13" fill="#2166ac"/></svg>cold front (triangles point the way it moves)</li>
  <li><svg width="30" height="16" viewBox="0 0 30 16" aria-hidden="true"><line x1="2" y1="8" x2="28" y2="8" stroke="#2166ac" stroke-width="1.6" marker-end="url(#ar-b)"/></svg>cold or cool air moving</li>
  <li><svg width="30" height="16" viewBox="0 0 30 16" aria-hidden="true"><line x1="2" y1="8" x2="28" y2="8" stroke="#b2182b" stroke-width="1.6" marker-end="url(#ar-r)"/></svg>warm air moving</li>
  <li><svg width="30" height="16" viewBox="0 0 30 16" aria-hidden="true"><line x1="2" y1="8" x2="28" y2="8" stroke="#000000" stroke-width="1.2" marker-end="url(#ar-k)"/></svg>other air motion</li>
  <li><svg width="20" height="14" viewBox="0 0 20 14" aria-hidden="true"><rect x="1" y="1" width="18" height="12" fill="#c6dbef" stroke="#000" stroke-width="0.5"/></svg>cold air or sea water</li>
  <li><svg width="20" height="14" viewBox="0 0 20 14" aria-hidden="true"><rect x="1" y="1" width="18" height="12" fill="#fcbba1" stroke="#000" stroke-width="0.5"/></svg>warm air</li>
  <li><svg width="20" height="14" viewBox="0 0 20 14" aria-hidden="true"><rect x="1" y="1" width="18" height="12" fill="#d9d9d9" stroke="#000" stroke-width="0.5"/></svg>land</li>
  <li><svg width="34" height="16" viewBox="0 0 34 16" aria-hidden="true"><text x="2" y="13" font-size="13" font-weight="700" fill="#2166ac" style="fill:#2166ac">H</text><text x="19" y="13" font-size="13" font-weight="700" fill="#b2182b" style="fill:#b2182b">L</text></svg>high- and low-pressure centers</li>
</ul>
</div>

<h2 id="sec-1">1. Coastal and marine systems</h2>
<p>The cold North Atlantic lies beside land that heats and cools much faster than the water. The contrast between them drives the six systems below, from the daily sea breeze to the winter nor’easter.</p>

<section class="wx-sys" id="sea-breeze">
<h3>1.1 Sea breeze</h3>
<p class="wx-def">A sea breeze is a daytime wind that blows from the sea onto the land, set up because the land warms faster than the water.</p>
<p><i>How it forms.</i> In sunshine the land heats faster than the sea, so pressure near the ground falls slightly over the land. Cool marine air flows inland, rises at its leading edge (the sea-breeze front) and returns seaward aloft (Fig. 1; <a href="#ref-miller2003">Miller et al. 2003</a>).</p>
<p>As the front passes, the wind turns onshore and the temperature drops, most sharply in spring when the water is still cold. Marine air is usually more humid than inland air in summer but can be drier over cold spring water. The front can push tens of kilometers inland, and rising air along it can set off showers. A front that arrives a few hours earlier or later than expected can put a coastal forecast high off by 20 °F (11 °C), as in the case below.</p>
<figure class="jn-fig wx-schem" id="fig-1">
  <svg viewBox="0 0 300 168" role="img" aria-labelledby="fig-1-cap">
    <rect x="150" y="100" width="150" height="32" fill="#fcbba1"/>
    <path d="M0,132 L0,100 L150,100 C162,100 172,110 178,132 Z" fill="#c6dbef"/>
    <rect x="0" y="132" width="120" height="36" fill="#c6dbef"/>
    <rect x="120" y="132" width="180" height="36" fill="#d9d9d9"/>
    <line x1="0" y1="132" x2="300" y2="132" stroke="#000" stroke-width="1"/>
    <line x1="120" y1="132" x2="120" y2="138" stroke="#000" stroke-width="1"/>
    <path d="M0,100 L150,100 C162,100 172,110 178,132" fill="none" stroke="#000" stroke-width="0.8"/>
    <line x1="40" y1="122" x2="166" y2="122" stroke="#2166ac" stroke-width="1.8" marker-end="url(#ar-b)"/>
    <line x1="192" y1="126" x2="192" y2="62" stroke="#b2182b" stroke-width="1.8" marker-end="url(#ar-r)"/>
    <line x1="184" y1="52" x2="42" y2="52" stroke="#000" stroke-width="1.2" marker-end="url(#ar-k)"/>
    <line x1="28" y1="58" x2="28" y2="96" stroke="#000" stroke-width="1.2" marker-end="url(#ar-k)"/>
    <path d="M182,47 a7,7 0 0 1 5,-11 a10,10 0 0 1 18,-3 a8,8 0 0 1 9,14 z" fill="#fff" stroke="#000" stroke-width="0.8"/>
    <g stroke="#000" stroke-width="0.8"><circle cx="272" cy="24" r="6" fill="none"/><line x1="272" y1="12" x2="272" y2="8"/><line x1="272" y1="36" x2="272" y2="40"/><line x1="260" y1="24" x2="256" y2="24"/><line x1="284" y1="24" x2="288" y2="24"/><line x1="263.5" y1="15.5" x2="260.7" y2="12.7"/><line x1="280.5" y1="15.5" x2="283.3" y2="12.7"/><line x1="263.5" y1="32.5" x2="260.7" y2="35.3"/><line x1="280.5" y1="32.5" x2="283.3" y2="35.3"/></g>
    <text x="64" y="46" font-size="10">return flow aloft</text>
    <text x="198" y="82" font-size="10">rising air</text>
    <text x="34" y="80" font-size="10">sinking air</text>
    <text x="6" y="114" font-size="10">cool marine air</text>
    <text x="200" y="120" font-size="10">warm air over land</text>
    <text x="80" y="94" font-size="10">sea-breeze front</text>
    <line x1="160" y1="96" x2="170" y2="112" stroke="#000" stroke-width="0.6"/>
    <text x="50" y="154" font-size="10">sea</text>
    <text x="106" y="164" font-size="9">coast</text>
    <text x="220" y="154" font-size="10">land</text>
  </svg>
  <figcaption id="fig-1-cap"><span class="jn-figno">Fig. 1.</span> Schematic vertical cross-section of a sea breeze, with the sea on the left and the land on the right (not to scale). Light blue shading is cool marine air and pink shading is air warmed over the land. The blue arrow is the cool onshore wind near the ground, the red arrow is air rising at the sea-breeze front, and the black arrows are the return flow toward the sea aloft and the air sinking over the water. A cumulus cloud often marks the rising air.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-2">
  <a href="/images/wx_systems_v3/seabreeze_2007.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/seabreeze_2007.png" alt="ERA5 maps for the sea breeze case, 1800 and 2000 UTC 27 March 2007" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 2.</span> Cool ocean air keeps the Massachusetts coast colder than inland, and the sea-breeze front is the blue band of converging wind along the shore in (b) (ERA5, 27 Mar 2007). (a) 2-m temperature (°C) and 10-m wind (barbs, kt) at 1800 UTC (2 p.m. EDT). (b) 10-m divergence (10⁻⁵ s⁻¹; blue: air converging and rising, red: spreading and sinking) and 2-m temperature (contours every 2 °C), 1800 UTC. (c) 2-m temperature change, 1800–2000 UTC (K). Boston is 4 °C cooler than Worcester and cools another 2 °C by 2000 UTC.</figcaption>
</figure>
<p><i>How forecasters identify it.</i> The usual signals at coastal stations are an onshore wind shift and a temperature drop. The two do not always arrive together. When the large-scale wind is already blowing onshore, the change in temperature and humidity can run as much as 15 km ahead of the wind shift (<a href="#ref-miller2003">Miller et al. 2003</a>, citing <a href="#ref-atkins1995">Atkins et al. 1995</a> for Florida). In ERA5 the front of 27 March 2007 is a coastal band of converging wind (Fig. 2). At 1800 UTC (2 p.m. EDT) Boston was 4 °C (7 °F) colder and slightly drier than Worcester.</p>
<blockquote class="wx-afd"><p>&ldquo;Temperatures at 3 PM indicate a typical spring afternoon in southern New England...with readings well into the 60s across much of the region. The exception was across eastern coastal Mass where temps have cooled into the mid 40s courtesy of the seabreeze front.&rdquo;</p>
<footer>NWS Boston (BOX) Area Forecast Discussion, issued 4:35 p.m. EDT 27 Mar 2007 (2035 UTC) (<a href="https://mesonet.agron.iastate.edu/p.php?pid=200703272035-KBOX-FXUS61-AFDBOX">archived text</a>)</footer></blockquote>
</section>

<section class="wx-sys" id="backdoor-front">
<h3>1.2 Backdoor cold front</h3>
<p class="wx-def">A backdoor cold front is a cold front that arrives from the northeast, off the ocean, instead of from the west or northwest as most cold fronts do.</p>
<p>High pressure to the north or northeast, often over Quebec or the Canadian Maritimes, drives a northeast or east wind that carries cool, damp Atlantic air southwest along the coast in a shallow layer (Fig. 3).</p>
<p><i>At the surface.</i> The wind swings to the northeast or east and the temperature can drop 10–30 °F (6–17 °C) within a few hours, often with low cloud, fog or drizzle, while places a few tens of kilometers inland stay warm. Backdoor fronts are most common in spring and early summer, when the ocean is still cold. Coastal forecast highs therefore depend on timing the front, and an error of a few hours can mean a miss of 20 °F (11 °C) or more.</p>
<figure class="jn-fig wx-schem" id="fig-3">
  <svg viewBox="0 0 300 168" role="img" aria-labelledby="fig-3-cap">
    <path d="M0,0 L240,0 C210,40 170,70 140,100 S80,150 60,168 L0,168 Z" fill="#d9d9d9"/>
    <polygon points="89,0 300,0 300,168 268,168" fill="#c6dbef" fill-opacity="0.6"/>
    <polygon points="0,0 89,0 268,168 0,168" fill="#fcbba1" fill-opacity="0.45"/>
    <path d="M240,0 C210,40 170,70 140,100 S80,150 60,168" fill="none" stroke="#000" stroke-width="1"/>
    <line x1="89" y1="0" x2="268" y2="168" stroke="#2166ac" stroke-width="2"/>
    <g fill="#2166ac"><polygon points="127.6,35.9 136.4,44.1 125.8,46.6"/><polygon points="159.6,65.9 168.4,74.1 157.8,76.6"/><polygon points="191.6,95.9 200.4,104.1 189.8,106.6"/><polygon points="223.6,125.9 232.4,134.1 221.8,136.6"/></g>
    <text x="250" y="40" font-size="18" font-weight="700" fill="#2166ac" style="fill:#2166ac">H</text>
    <text x="226" y="56" font-size="10">high pressure</text>
    <line x1="200" y1="28" x2="172" y2="56" stroke="#2166ac" stroke-width="1.6" marker-end="url(#ar-b)"/>
    <line x1="292" y1="96" x2="264" y2="124" stroke="#2166ac" stroke-width="1.6" marker-end="url(#ar-b)"/>
    <line x1="20" y1="150" x2="50" y2="126" stroke="#b2182b" stroke-width="1.6" marker-end="url(#ar-r)"/>
    <text x="198" y="72" font-size="10">northeast wind</text>
    <text x="198" y="86" font-size="10">cool, damp marine air</text>
    <text x="62" y="24" font-size="10">backdoor</text>
    <text x="62" y="36" font-size="10">cold front</text>
    <text x="8" y="108" font-size="10">warm air inland</text>
    <text x="146" y="152" font-size="10">Atlantic Ocean</text>
    <line x1="288" y1="164" x2="288" y2="144" stroke="#000" stroke-width="1" marker-end="url(#ar-k)"/>
    <text x="284" y="140" font-size="10">N</text>
  </svg>
  <figcaption id="fig-3-cap"><span class="jn-figno">Fig. 3.</span> Schematic map, north at the top, of a backdoor cold front moving southwest along the Northeast coast. The black curve is the coastline, with land to the upper left and the Atlantic Ocean to the lower right. Blue shading is the cool marine air behind the front and pink shading the warmer air ahead of it. The blue line with triangles is the front; the triangles point the way it moves. H marks high pressure over the Canadian Maritimes. Blue arrows are the northeast wind behind the front and the red arrow is the southwest wind ahead of it. A typical cold front would instead move southeast from a high over western North America.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-4">
  <a href="/images/wx_systems_v3/backdoor_2018.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/backdoor_2018.png" alt="ERA5 maps for the backdoor cold front case, 2000 and 2300 UTC 26 May 2018" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 4.</span> Cool northeast wind off the Gulf of Maine (blue) pushes southwest over Boston between the two times, while Worcester and the interior stay hot (ERA5, 26 May 2018). 2-m temperature (shading, °C), sea-level pressure (contours every 2 hPa) and 10-m wind (barbs, kt) at (a) 2000 UTC and (b) 2300 UTC (4 and 7 p.m. EDT). Boston cools by about 6 °C, to 22 °C, as its wind turns from southwest to northeast; Worcester cools only to 27 °C. Pressure is higher to the north, toward Quebec City.</figcaption>
</figure>
<p>The front can be followed from station to station by the northeast wind shift and the temperature drop, with pressure rising behind it. The dewpoint can rise or fall, depending on the marine air.</p>
<p>On 26 May 2018 (Fig. 4) Boston&rsquo;s airport cooled from 88 to 67 &deg;F (31 to 19 &deg;C) in two hours after 2054 UTC (4:54 p.m. EDT) as the wind turned northeast. Worcester, 60 km (40 mi) inland, stayed above 80 &deg;F (27 &deg;C), and Boston&rsquo;s dewpoint did not change. ERA5 shows a smaller drop (6.4 &deg;C in 3 h).</p>
<blockquote class="wx-afd"><p>&ldquo;Sea breeze aided backdoor front has already pushed through much of the BOS metro this evening and will continue to push SW through the evening.&rdquo;</p>
<footer>NWS Boston (BOX) Area Forecast Discussion, issued 7:21 p.m. EDT 26 May 2018 (2321 UTC); BOS is Boston&rsquo;s Logan Airport (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201805262321-KBOX-FXUS61-AFDBOX">archived text</a>)</footer></blockquote>
</section>

<section class="wx-sys" id="coastal-front">
<h3>1.3 Coastal front</h3>
<p class="wx-def">A coastal front is a shallow, nearly stationary boundary along or just off the coast in the cold season, between cold air over the land and milder air off the ocean.</p>
<p><i>How it forms.</i> Every front <a href="#ref-bosart1975">Bosart (1975)</a> studied formed with “a pronounced sea level cold anticyclone [high] to the north and east of New England.” Around that high the wind blows from the northeast over the ocean. Over land, the rougher surface slows the wind and turns it to blow more from the north, toward the coast. The two air masses are pushed together at the shore and the boundary between them sharpens (see also <a href="#ref-nielsen1989">Nielsen 1989</a>).</p>
<p>The cold air is usually less than 1 km deep, and the temperature can change by about 5–10 °C (9–18 °F) across 10 km (<a href="#ref-ams2026">AMS 2026</a>). The front often separates snow or ice inland from rain at the coast.</p>
<p><i>Why it matters for forecasts.</i> A small shift in the front moves the rain–snow line across a town, and coastal lows tend to form along it or follow it (AMS 2026).</p>
<figure class="jn-fig wx-schem" id="fig-5">
  <svg viewBox="0 0 300 168" role="img" aria-labelledby="fig-5-cap">
    <path d="M0,60 H300 V140 H172 C130,112 60,98 0,96 Z" fill="#fcbba1"/>
    <path d="M0,140 V96 C60,98 130,112 172,140 Z" fill="#c6dbef"/>
    <rect x="0" y="140" width="170" height="28" fill="#d9d9d9"/>
    <rect x="170" y="140" width="130" height="28" fill="#c6dbef"/>
    <line x1="0" y1="140" x2="300" y2="140" stroke="#000" stroke-width="1"/>
    <path d="M0,96 C60,98 130,112 172,140" fill="none" stroke="#000" stroke-width="1.2"/>
    <g stroke="#000" stroke-width="0.7" stroke-dasharray="2 3"><line x1="82" y1="60" x2="82" y2="138"/><line x1="96" y1="60" x2="96" y2="138"/><line x1="110" y1="60" x2="110" y2="138"/><line x1="124" y1="60" x2="124" y2="138"/></g>
    <path d="M70,58 a10,10 0 0 1 8,-14 a13,13 0 0 1 24,-4 a11,11 0 0 1 20,4 a9,9 0 0 1 6,14 z" fill="#fff" stroke="#000" stroke-width="0.8"/>
    <line x1="286" y1="126" x2="184" y2="126" stroke="#b2182b" stroke-width="1.8" marker-end="url(#ar-r)"/>
    <line x1="178" y1="116" x2="136" y2="88" stroke="#b2182b" stroke-width="1.8" marker-end="url(#ar-r)"/>
    <circle cx="14" cy="124" r="5" fill="none" stroke="#2166ac" stroke-width="1.2"/><circle cx="14" cy="124" r="1.5" fill="#2166ac"/>
    <text x="24" y="128" font-size="10">north wind</text>
    <text x="6" y="111" font-size="10">cold air</text>
    <text x="200" y="88" font-size="10">milder marine air</text>
    <text x="226" y="120" font-size="10">east wind</text>
    <text x="196" y="106" font-size="10">coastal front</text>
    <line x1="198" y1="109" x2="175" y2="136" stroke="#000" stroke-width="0.6"/>
    <text x="60" y="158" font-size="10">land</text>
    <text x="226" y="158" font-size="10">ocean</text>
    <line x1="150" y1="14" x2="40" y2="14" stroke="#000" stroke-width="0.8" marker-end="url(#ar-k)"/>
    <line x1="150" y1="14" x2="260" y2="14" stroke="#000" stroke-width="0.8" marker-end="url(#ar-k)"/>
    <text x="6" y="18" font-size="10">west</text>
    <text x="268" y="18" font-size="10">east</text>
  </svg>
  <figcaption id="fig-5-cap"><span class="jn-figno">Fig. 5.</span> Schematic west&ndash;east cross-section of a coastal front (not to scale). Light blue shading over the land is the shallow layer of cold air, usually less than 1 km deep, and pink shading is milder air that has come off the ocean. The black curve is the front, which reaches the ground near the shoreline and slopes back over the cold air. The circled dot marks a north wind blowing toward the viewer in the cold air; the red arrows show the east wind off the ocean rising over the front, producing cloud and precipitation (dashed lines) that fall into the cold air.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-6">
  <a href="/images/wx_systems_v3/coastalfront_2008.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/coastalfront_2008.png" alt="ERA5 maps for the coastal front case, 1200 UTC 27 January 2008" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 6.</span> The coastal front is the dark red strip in (b) north of Boston, between mild east wind off the ocean and below-freezing north wind over land (ERA5, 1200 UTC [7 a.m. EST] 27 Jan 2008). (a) Air minus sea-surface temperature over water (K; blue: air colder than the sea), 2-m temperature (contours every 1 °C, dashed below 0 °C) and 10-m wind (barbs, kt). (b) Frontogenesis, how fast the wind sharpens the temperature contrast (K per 100 km per 3 h). Boston is −2 °C, Worcester −5 °C, the sea about 4 °C.</figcaption>
</figure>
<p>Comparing inland winds with those at coastal stations and buoys locates the front. <a href="#ref-bosart1975">Bosart (1975)</a> found that the large-scale pressure pattern alone could not create a coastal front; friction and ocean heat were needed. In a 1981 storm, <a href="#ref-keshishian1987">Keshishian and Bosart (1987)</a> found that the observed winds also helped build it. In ERA5 at 1200 UTC 27 January 2008 (7 a.m. EST; Fig. 6) the front lies along the coast north of Boston, between east-southeasterly ocean air and north-northeasterly wind over below-freezing land.</p>
<blockquote class="wx-afd"><p>&ldquo;Caveat: coastal front developing /ESE wind at buoys/ may enhance snowfall rates in NE Mass N of Boston around 6 AM?&rdquo;</p>
<footer>NWS Boston (BOX) Area Forecast Discussion, issued 10:55 p.m. EST 26 Jan 2008 (0355 UTC 27 Jan) (<a href="https://mesonet.agron.iastate.edu/p.php?pid=200801270355-KBOX-FXUS61-AFDBOX">archived text</a>)</footer></blockquote>
</section>

<section class="wx-sys" id="marine-layer">
<h3>1.4 Marine layer and sea fog</h3>
<p class="wx-def">Sea fog forms when warm, moist air flows over colder water and is chilled from below to saturation; the cool, cloudy coastal layer it creates is often called the marine layer.</p>
<p>Off New England, southerly winds carry humid air over cold shelf water and the Gulf of Maine, cooling “the lower layer of air below its dewpoint” (<a href="#ref-ams2026">AMS 2026</a>). The chilled bottom layer, colder than the air above, forms an inversion that traps fog and low, flat stratus cloud (Fig. 7).</p>
<p><i>Effects.</i> The shore is gray, damp and cool while inland is sunny and warm. Fog over land usually thins by late morning but can linger at the beach. It is most common in late spring and summer. The coastal high depends mostly on when the low cloud clears.</p>
<figure class="jn-fig wx-schem" id="fig-7">
  <svg viewBox="0 0 300 168" role="img" aria-labelledby="fig-7-cap">
    <path d="M0,60 H300 V140 H280 C268,124 250,110 232,104 H86 V140 H0 Z" fill="#fcbba1" fill-opacity="0.6"/>
    <path d="M86,140 V104 H232 C250,110 268,124 280,140 Z" fill="#e6e6e6"/>
    <rect x="0" y="140" width="80" height="28" fill="#fcbba1"/>
    <rect x="80" y="140" width="140" height="28" fill="#c6dbef"/>
    <rect x="220" y="140" width="80" height="28" fill="#d9d9d9"/>
    <line x1="0" y1="140" x2="300" y2="140" stroke="#000" stroke-width="1"/>
    <line x1="86" y1="104" x2="234" y2="104" stroke="#000" stroke-width="1.2" stroke-dasharray="5 3"/>
    <line x1="6" y1="126" x2="80" y2="126" stroke="#b2182b" stroke-width="1.8" marker-end="url(#ar-r)"/>
    <line x1="96" y1="124" x2="250" y2="124" stroke="#2166ac" stroke-width="1.8" marker-end="url(#ar-b)"/>
    <g stroke="#000" stroke-width="1" marker-end="url(#ar-k)"><line x1="112" y1="129" x2="112" y2="139"/><line x1="142" y1="129" x2="142" y2="139"/><line x1="172" y1="129" x2="172" y2="139"/><line x1="202" y1="129" x2="202" y2="139"/></g>
    <text x="6" y="116" font-size="10">warm, moist air</text>
    <text x="110" y="118" font-size="10">fog and low cloud</text>
    <text x="120" y="98" font-size="10">inversion (lid)</text>
    <text x="120" y="78" font-size="10">warmer air above</text>
    <text x="4" y="158" font-size="10">warmer water</text>
    <text x="104" y="158" font-size="10">cold shelf water</text>
    <text x="238" y="158" font-size="10">land</text>
    <line x1="150" y1="14" x2="40" y2="14" stroke="#000" stroke-width="0.8" marker-end="url(#ar-k)"/>
    <line x1="150" y1="14" x2="260" y2="14" stroke="#000" stroke-width="0.8" marker-end="url(#ar-k)"/>
    <text x="6" y="18" font-size="10">south</text>
    <text x="266" y="18" font-size="10">north</text>
  </svg>
  <figcaption id="fig-7-cap"><span class="jn-figno">Fig. 7.</span> Schematic south&ndash;north cross-section of sea fog forming in southerly flow along the New England coast (not to scale). Pink at the bottom left is warmer water to the south, light blue is the cold shelf water near the coast and gray is land. Warm, moist air (red arrow, pink shading) moves north over the cold water, loses heat to it (short black arrows) and becomes a layer of fog and low stratus cloud (light gray) that keeps moving onshore (blue arrow). The dashed line is the temperature inversion that caps the layer. Over land the layer thins as the ground warms.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-8">
  <a href="/images/wx_systems_v3/marine_2015.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/marine_2015.png" alt="ERA5 maps for the marine layer and sea fog case, 2000 UTC 10 May 2015" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 8.</span> Warm southwest air crossing cold water south of Rhode Island and Cape Cod is chilled from below into fog and low cloud (white band in a) under a strong inversion (ERA5, 2000 UTC [4 p.m. EDT] 10 May 2015). (a) Low cloud cover (%) and 10-m wind (barbs, kt). (b) Air minus sea-surface temperature (K) and sea-surface temperature (contours every 2 °C). (c) 925-hPa (about 750 m up) minus 2-m temperature (K; positive: inversion). Over the cold water the air is 3–4 °C warmer than the 10 °C sea and nearly saturated.</figcaption>
</figure>
<p>Fog and stratus are tracked on satellite images and in visibility and cloud-base reports from coastal stations and buoys. Fog is likely when the incoming air’s dewpoint is higher than the sea-surface temperature. <a href="#ref-koracin2014">Kora&#269;in et al. (2014)</a> review marine fog worldwide.</p>
<p>On 10 May 2015 (Fig. 8) Boston reached 80&ndash;88 &deg;F (27&ndash;31 &deg;C), while Nantucket, in southwest wind off cold water, stayed at 57&ndash;62 &deg;F (14&ndash;17 &deg;C) in fog most of the afternoon, under cloud bases 200&ndash;300 ft (60&ndash;90 m) up. ERA5 has no fog variable; low cloud stands in for it.</p>
<blockquote class="wx-afd"><p>&ldquo;A narrow sliver of dense fog hugged the south coastal waters all afternoon.&rdquo;</p>
<footer>NWS Boston (BOX) Area Forecast Discussion, issued 4:42 p.m. EDT 10 May 2015 (2042 UTC) (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201505102042-KBOX-FXUS61-AFDBOX">archived text</a>)</footer></blockquote>
</section>

<section class="wx-sys" id="noreaster">
<h3>1.5 Nor’easter</h3>
<p class="wx-def">A nor&rsquo;easter is a strong coastal storm, named for the northeast winds it drives onto the coast north of its center.</p>
<p>In winter, air over the continent is much colder than air over the Gulf Stream. An upper-level trough (a southward dip in the jet stream about 5.5 km up) lifts the air ahead of it, and a low forms or strengthens along the coast, fed by heat released as water vapor condenses. Its counterclockwise winds draw cold air south on its west side and warm, moist air north on its east side (Fig. 9). Snow or rain is heaviest northwest of the track, and northeast winds push water onto east-facing shores. In the blizzard of 26–27 January 2015 (Fig. 10), Boston received 24.4 in (62 cm) and Worcester a record 34.5 in (88 cm).</p>
<p><i>Why it matters for forecasts.</i> Forecasters compare a storm’s track with the “benchmark” at 40°N, 70°W, about 140 km (90 mi) south of Nantucket. Lows passing near it tend to bring heavy snow to eastern New England, and tracks closer to the coast bring rain. In 2015 New York City, at the western edge of the snow band, got about 10 in (25 cm), so a small difference in track separated a blizzard from a moderate snowfall.</p>
<figure class="jn-fig wx-schem" id="fig-9">
  <svg viewBox="0 0 300 168" role="img" aria-labelledby="fig-9-cap">
    <path d="M0,0 H235 C205,40 165,70 140,100 S70,150 45,168 H0 Z" fill="#d9d9d9"/>
    <path d="M235,0 C205,40 165,70 140,100 S70,150 45,168" fill="none" stroke="#000" stroke-width="1"/>
    <ellipse cx="118" cy="62" rx="60" ry="24" transform="rotate(-40 118 62)" fill="#c6dbef" stroke="#2166ac" stroke-width="0.8" stroke-dasharray="3 2"/>
    <g fill="none" stroke="#000" stroke-width="0.8"><ellipse cx="215" cy="112" rx="16" ry="13"/><ellipse cx="215" cy="112" rx="32" ry="26"/><ellipse cx="215" cy="112" rx="48" ry="39"/></g>
    <text x="209" y="118" font-size="16" font-weight="700" fill="#b2182b" style="fill:#b2182b">L</text>
    <line x1="254" y1="60" x2="190" y2="78" stroke="#000" stroke-width="1.8" marker-end="url(#ar-k)"/>
    <line x1="160" y1="94" x2="156" y2="132" stroke="#2166ac" stroke-width="1.8" marker-end="url(#ar-b)"/>
    <line x1="284" y1="160" x2="284" y2="108" stroke="#b2182b" stroke-width="1.8" marker-end="url(#ar-r)"/>
    <text x="90" y="66" font-size="10">heavy snow</text>
    <text x="228" y="32" font-size="10">strong</text>
    <text x="228" y="44" font-size="10">northeast wind</text>
    <text x="104" y="148" font-size="10">cold air</text>
    <text x="196" y="164" font-size="10">warm, moist air</text>
    <line x1="16" y1="46" x2="16" y2="24" stroke="#000" stroke-width="1" marker-end="url(#ar-k)"/>
    <text x="12" y="18" font-size="10">N</text>
  </svg>
  <figcaption id="fig-9-cap"><span class="jn-figno">Fig. 9.</span> Schematic map, north at the top, of a nor’easter off the New England coast. Gray is land and white is ocean. The ellipses are isobars around the low-pressure center L. Air circulates counterclockwise around the low: the black arrow is the strong northeast wind blowing onshore north of the center, the blue arrow is cold air drawn south on the western side, and the red arrow is warm, moist air drawn north on the eastern side. Light blue shading marks where the heaviest snow usually falls, northwest of the low.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-10">
  <a href="/images/wx_systems_v3/noreaster_2015.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/noreaster_2015.png" alt="ERA5 maps for the nor’easter case, 0000 UTC 27 January 2015" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 10.</span> The blizzard’s low (L) lies off the Mid-Atlantic coast under a deep dip in the upper-level flow, driving northeast wind onto New England, with a comma of high cloud wrapped around it (ERA5, 0000 UTC 27 Jan 2015 [7 p.m. EST 26 Jan]). (a) Sea-level pressure (contours every 4 hPa), precipitation rate (mm h⁻¹) and 10-m wind (barbs, kt). (b) 500-hPa height (contours every 6 dam) and spin of the wind (10⁻⁵ s⁻¹; red: counterclockwise). (c) High cloud cover (%) and sea-level pressure. Central pressure is 993 hPa.</figcaption>
</figure>
<p><i>How forecasters identify it.</i> The low is followed on pressure maps and satellite images. <a href="#ref-miller1946">Miller (1946)</a> classified East Coast storms (Section 1.6), and <a href="#ref-kocin2004">Kocin and Uccellini (2004)</a> describe the Northeast’s major snowstorms.</p>
<blockquote class="wx-afd"><p>&ldquo;Coastal front currently west of I95 extending from between BED-BOS to NW RI. As sfc low approaches benchmark late tonight and Tue morning expect this front to move along and just east of the I-95 corridor with temps crashing into the teens and lower 20s in the coastal plain including BOS and PVD.&rdquo;</p>
<footer>NWS Boston (BOX) Area Forecast Discussion, issued 9:28 p.m. EST 26 Jan 2015 (0228 UTC 27 Jan); BED, BOS and PVD are the Bedford, Boston and Providence airports, and &ldquo;sfc&rdquo; means surface (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201501270228-KBOX-FXUS61-AFDBOX">archived text</a>)</footer></blockquote>
</section>

<section class="wx-sys" id="miller-b">
<h3>1.6 Miller type B redevelopment</h3>
<p class="wx-def">A Miller type B storm forms when a low moving in from the west weakens near the Appalachians and a new coastal low takes over.</p>
<p><i>How it forms.</i> <a href="#ref-miller1946">Miller (1946)</a> sorted East Coast snowstorms into two types. In National Weather Service usage, type A develops along the Gulf or East Coast and moves up the coast as one storm; type B comes up the Ohio Valley, loses its compact center near the Appalachians and re-forms near the coast (<a href="#ref-nwsctp">NWS State College n.d.</a>). The new low forms where the lift ahead of an upper-level trough meets the strong temperature contrast at the coast, often sharpened by a coastal front (<a href="#coastal-front">Section 1.3</a>) or by cold air dammed against the mountains (<a href="#cold-air-damming">Section 2.1</a>; Fig. 11).</p>
<p><i>Effects.</i> Precipitation often eases during the handoff, then returns heavily north and west of the new low, so the timing and position of the new low decide which towns get the most snow.</p>
<figure class="jn-fig wx-schem" id="fig-11">
  <svg viewBox="0 0 300 168" role="img" aria-labelledby="fig-11-cap">
    <path d="M0,0 H262 C240,40 215,70 205,100 S170,150 150,168 H0 Z" fill="#d9d9d9"/>
    <polygon points="128,60 222,60 203,100 178,140 56,140" fill="#c6dbef" fill-opacity="0.8"/>
    <path d="M262,0 C240,40 215,70 205,100 S170,150 150,168" fill="none" stroke="#000" stroke-width="1"/>
    <g fill="none" stroke="#000" stroke-width="1"><path d="M38,149 L44,141 L50,149"/><path d="M52,134 L58,126 L64,134"/><path d="M66,119 L72,111 L78,119"/><path d="M80,104 L86,96 L92,104"/><path d="M94,89 L100,81 L106,89"/><path d="M108,74 L114,66 L120,74"/><path d="M122,59 L128,51 L134,59"/><path d="M136,44 L142,36 L148,44"/><path d="M150,29 L156,21 L162,29"/></g>
    <g fill="none" stroke="#666" stroke-width="0.8" stroke-dasharray="3 2"><ellipse cx="50" cy="58" rx="14" ry="11"/><ellipse cx="50" cy="58" rx="28" ry="22"/></g>
    <text x="45" y="63" font-size="14" font-weight="700" fill="#777" style="fill:#777">L</text>
    <line x1="0" y1="88" x2="24" y2="72" stroke="#000" stroke-width="1" stroke-dasharray="4 3" marker-end="url(#ar-k)"/>
    <g fill="none" stroke="#000" stroke-width="0.8"><ellipse cx="232" cy="118" rx="14" ry="11"/><ellipse cx="232" cy="118" rx="28" ry="22"/><ellipse cx="232" cy="118" rx="42" ry="33"/></g>
    <text x="226" y="124" font-size="16" font-weight="700" fill="#b2182b" style="fill:#b2182b">L</text>
    <line x1="252" y1="92" x2="280" y2="40" stroke="#000" stroke-width="1.4" marker-end="url(#ar-k)"/>
    <text x="8" y="24" font-size="10">primary low weakens</text>
    <text x="50" y="110" font-size="9.5" transform="rotate(-47 50 110)">Appalachians</text>
    <text x="108" y="132" font-size="10">cold air</text>
    <text x="196" y="164" font-size="10">new coastal low</text>
    <line x1="12" y1="162" x2="12" y2="142" stroke="#000" stroke-width="1" marker-end="url(#ar-k)"/>
    <text x="8" y="138" font-size="10">N</text>
  </svg>
  <figcaption id="fig-11-cap"><span class="jn-figno">Fig. 11.</span> Schematic map, north at the top, of a Miller type B storm. The primary low (gray L, dashed isobars) approaches from the west (dashed arrow) and weakens west of the Appalachians (row of peaks). A new low (red L, solid isobars) forms on the coast, becomes the main storm and moves northeast (black arrow). Light blue shading is cold air dammed east of the mountains.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-12">
  <a href="/images/wx_systems_v3/millerb_2011.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/millerb_2011.png" alt="ERA5 maps for the Miller type B case, 1200 and 1800 UTC 26 January and 0600 UTC 27 January 2011" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 12.</span> Two weak lows, west of the Appalachians and on the North Carolina coast, give way to one coastal low that deepens as it heads for the 40°N, 70°W benchmark (plus sign) (ERA5, 26–27 Jan 2011). Sea-level pressure (contours every 4 hPa) and its 3-h change (shading, hPa; blue: falling) at (a) 1200 UTC 26 Jan, (b) 1800 UTC 26 Jan and (c) 0600 UTC 27 Jan. By (b) only the coastal low remains, falling 6 hPa in 3 h; by (c) it is 987 hPa.</figcaption>
</figure>
<p>The handoff shows as pressure falling at the coast while it rises at the inland low. The storm of 26–27 January 2011 (Fig. 12) illustrates the handoff, although its first low came from northern Alabama rather than the Ohio Valley. At 1200 UTC 26 January (7 a.m. EST) ERA5 has weak lows west of the Appalachians and on the North Carolina coast; by 1800 UTC only the coastal low remains. The two Philadelphia discussions below, issued under four hours apart, record the same jump, placing the low first over northern Alabama and then over coastal North Carolina.</p>
<blockquote class="wx-afd"><p>&ldquo;Low pressure over northern Alabama early this morning will track northeast and deepen as it moves off the Mid Atlantic coast this evening.&rdquo; (6:58 a.m. EST)</p>
<p>&ldquo;Low pressure over coastal North Carolina this morning will track northeast and deepen as it moves off the Mid Atlantic coast this evening.&rdquo; (10:36 a.m. EST)</p>
<footer>NWS Philadelphia/Mount Holly (PHI) Area Forecast Discussions, 26 Jan 2011, issued 1158 UTC (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201101261158-KPHI-FXUS61-AFDPHI">archived text</a>) and 1536 UTC (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201101261536-KPHI-FXUS61-AFDPHI">archived text</a>)</footer></blockquote>
</section>

<h2 id="sec-2">2. Terrain-forced systems</h2>
<p>Mountains and large lakes change the air that flows over or past them. The Appalachians and the New England hills hold back cold air or warm the air that descends from them, and the Great Lakes supply the heat and moisture for lake-effect snow.</p>

<section class="wx-sys" id="cold-air-damming">
<h3>2.1 Cold-air damming</h3>
<p class="wx-def">Cold-air damming is shallow cold air held against the eastern Appalachians by high pressure to the north, as a dam holds water.</p>
<p><i>How it forms.</i> High pressure to the north drives cold, dense air toward the mountains, where it turns south along the slope (<a href="#ref-ellis2018">Ellis et al. 2018</a>); Earth’s rotation presses it against them. Rain from the warm air above evaporates in the dome, supplying roughly 30% of the cooling in places (<a href="#ref-bell1988">Bell and Bosart 1988</a>).</p>
<p><i>Effects.</i> The dome brings overcast skies, a northeast wind, drizzle and temperatures far below normal. It is most common in Virginia and the Carolinas but also occurs in New England. In a below-freezing dome the rain freezes on contact (<a href="#freezing-rain">Section 4.1</a>).</p>
<p><i>Why it matters for forecasts.</i> Models tend to erode the dome too early, in one case by more than 10 °F (6 °C) (<a href="#ref-riordan2003">Riordan et al. 2003</a>).</p>
<figure class="jn-fig wx-schem" id="fig-13">
  <div class="wx-two">
  <svg viewBox="0 0 300 170" role="img" aria-labelledby="fig-13-cap">
    <path d="M0 150 H18 L58 58 L98 150 H300 V170 H0 Z" fill="#d9d9d9"/>
    <path d="M78.4 105 C140 106 220 128 300 140 V150 H98 Z" fill="#c6dbef"/>
    <path d="M78.4 105 C140 106 220 128 300 140" fill="none" stroke="#2166ac" stroke-width="1"/>
    <path d="M0 150 H18 L58 58 L98 150 H300" fill="none" stroke="#000" stroke-width="1"/>
    <path d="M296 126 C230 116 160 98 106 75" fill="none" stroke="#b2182b" stroke-width="1.5" marker-end="url(#ar-r)"/>
    <g stroke="#000" stroke-width="0.8" stroke-dasharray="2 2">
      <line x1="160" y1="99" x2="160" y2="109"/><line x1="185" y1="107" x2="185" y2="115"/><line x1="210" y1="113" x2="210" y2="120"/>
    </g>
    <circle cx="170" cy="138" r="3.5" fill="none" stroke="#2166ac" stroke-width="1"/><circle cx="170" cy="138" r="1" fill="#2166ac"/>
    <text x="6" y="14" font-size="10">← west</text><text x="262" y="14" font-size="10">east →</text>
    <text x="112" y="62" font-size="10">warm, moist air rises over the dome</text>
    <text x="112" y="141" font-size="10">cold dome</text>
    <text x="177" y="141.5" font-size="10">cold air flows south</text>
    <text x="28" y="164" font-size="10">Appalachians</text>
    <text x="150" y="164" font-size="10">Piedmont and coastal plain</text>
  </svg>
  <img src="/images/wx_systems_v2/schematics/cad_wedge.gif" alt="Cross-section from the Appalachian Mountains east through Staunton, Charlottesville, Manassas and Washington, showing a dome of cold air under clouds, with warm air rising over the dome.">
  </div>
  <figcaption id="fig-13-cap"><span class="jn-figno">Fig. 13.</span> Cold-air damming in a west–east cross-section. (a) Schematic drawn for this page: the cold dome (blue) lies against the eastern slope of the mountains and thins toward the coast; its top (blue line) is an inversion, where temperature increases with height. Warm, moist air (red arrow) rises over the dome, and rain falling from it (short dashes) evaporates into the cold air. The circled dot marks the cold air flowing south along the mountains, toward the reader. (b) The same structure across northern Virginia. Courtesy NWS Baltimore/Washington (LWX); public domain (U.S. Government work).</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-14">
  <a href="/images/wx_systems_v3/cad_2004.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/cad_2004.png" alt="ERA5 maps for the cold-air damming case, 1800 UTC 26 January 2004" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 14.</span> Cold air trapped east of the Appalachians at 1800 UTC (1 p.m. EST) 26 Jan 2004, in ERA5. The isobars bend south in a U along the mountains, and below-freezing air lies under warmer air. (a) Sea-level pressure (contours every 4 hPa), 2-m temperature (shading, °C) and 10-m wind (barbs, kt); the dashed line marks the section in (b). (b) West–east section along 36.5°N of temperature (shading, °C; thick line 0 °C), potential temperature (contours every 3 K) and wind (barbs, kt); terrain is gray.</figcaption>
</figure>
<p><i>How forecasters identify it.</i> Classically, isobars and lines of equal temperature bend south in a U along the mountains (<a href="#ref-bell1988">Bell and Bosart 1988</a>). The dome lies below 850 hPa, so maps at that level barely show it (<a href="#ref-ellis2018">Ellis et al. 2018</a>).</p>
<p>On 26 January 2004 (Fig. 14), high pressure over Quebec pushed cold air south, bending the isobars into a U over Virginia and the Carolinas. At 1 p.m. EST Greensboro, N.C., was 21 °F (−6 °C) in a northeast wind, while Knoxville, Tenn., west of the mountains, was 47 °F (9 °C). At 1.5 km the air was 43 °F (6 °C), so rain froze on contact.</p>
<blockquote class="wx-afd"><p>“Another shot of wintry weather this aftn [afternoon]-tonight...and not the kind that is friendly to power lines or trees. Looking at significant icing (a quarter inch or more) generally east of the Blue Ridge. […] Temps today will struggle to reach 30 [°F]...except outside the wedge. Higher ridges in the SW [southwest] could exceed 40 as 8H [850-hPa] temps rise to +7 [°C].”</p>
<footer>NWS Blacksburg, Va. (RNK) Area Forecast Discussion, issued 3:12 a.m. EST 26 Jan 2004 (<a href="https://mesonet.agron.iastate.edu/p.php?pid=200401260813-KRNK-FXUS61-AFDRNK">archived text</a>)</footer></blockquote>
</section>

<section class="wx-sys" id="downslope">
<h3>2.2 Downslope (lee) warming</h3>
<p class="wx-def">Downslope warming is the heating of air as it sinks down the lee (downwind) side of a mountain range, making places beyond them warmer and drier.</p>
<p><i>How it forms.</i> Sinking air is compressed and warms about 10 °C per kilometer (5.5 °F per 1000 ft). Rising air cools at that rate only until clouds form; then condensation releases heat, so air that rains out upwind reaches the lee warmer and drier. Even without rain, air brought down from ridge height usually arrives warmer than the air near the ground upwind.</p>
<p>The result is a dry, gusty westerly wind, a falling dewpoint and an afternoon high a few degrees above what the air mass alone would give. In New England the westerly wind also holds off the sea breeze (<a href="#sea-breeze">Section 1.1</a>), so even east-facing beaches get hot, and the dry, gusty air raises the risk of brush fires.</p>
<figure class="jn-fig wx-schem" id="fig-15">
  <svg viewBox="0 0 300 168" role="img" aria-labelledby="fig-15-cap">
    <path d="M0 140 H70 L140 50 L210 140 H300 V168 H0 Z" fill="#d9d9d9"/>
    <path d="M0 140 H70 L140 50 L210 140 H300" fill="none" stroke="#000" stroke-width="1"/>
    <path d="M8 128 C60 126 100 92 134 44" fill="none" stroke="#2166ac" stroke-width="1.5" marker-end="url(#ar-b)"/>
    <path d="M146 44 C180 70 215 124 292 128" fill="none" stroke="#b2182b" stroke-width="1.5" marker-end="url(#ar-r)"/>
    <text x="6" y="14" font-size="10">← west</text><text x="262" y="14" font-size="10">east →</text>
    <text x="8" y="100" font-size="10">westerly wind</text>
    <text x="158" y="32" font-size="10">sinking air is compressed</text>
    <text x="158" y="44" font-size="10">and warms 10 °C per km</text>
    <text x="104" y="160" font-size="10">hills and mountains</text>
    <text x="222" y="160" font-size="10">warmer, drier</text>
  </svg>
  <figcaption id="fig-15-cap"><span class="jn-figno">Fig. 15.</span> Schematic west–east cross-section of downslope warming. A westerly wind (blue arrow) rises over the hills and then sinks down the lee slope (red arrow), warming by compression, so the air reaching the plain east of the hills is warmer and drier than the air that started upwind.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-16">
  <a href="/images/wx_systems_v3/downslope_2008.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/downslope_2008.png" alt="ERA5 maps for the downslope warming case, 1800 UTC 8 June 2008" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 16.</span> On a hot day with westerly wind, air sinks down the eastern slopes of the Adirondacks and Catskills (red patches in b) and warms as it is compressed (ERA5, 1800 UTC [2 p.m. EDT] 8 Jun 2008). (a) 2-m temperature (°C), sea-level pressure (contours every 2 hPa) and 10-m wind (barbs, kt). (b) Vertical motion at 850 hPa, about 1.5 km up (hPa h⁻¹; red: sinking, blue: rising), and the 400-m terrain contour. Boston reaches 30 °C, Hartford 33 °C and Philadelphia 34 °C.</figcaption>
</figure>
<p>Forecasters look for westerly or northwesterly wind across the ridges, dewpoints that fall during the afternoon, and warm air near 850 hPa (about 1.5 km up) that mixing can bring down. The heat wave of 8 June 2008 (Fig. 16; 1800 UTC, 2 p.m. EDT) had westerly wind at 850 hPa, sinking air in the lee of the Adirondacks and Catskills and no sea breeze, so Boston reached 87 °F (30 °C). The dewpoint and the air aloft changed little that day.</p>
<blockquote class="wx-afd"><p>“Highs for today were nudged upward a few degrees...since temperatures have not dropped off much overnight and W [westerly] downsloping flow is expected. In addition...many of E [east] coast beaches will be hotter today since we will have enough of a [pressure] gradient to prevent sea breezes from developing.”</p>
<footer>NWS Boston (BOX) Area Forecast Discussion, issued 4:12 a.m. EDT 8 Jun 2008 (<a href="https://mesonet.agron.iastate.edu/p.php?pid=200806080816-KBOX-FXUS61-AFDBOX">archived text</a>)</footer></blockquote>
</section>

<section class="wx-sys" id="lake-effect">
<h3>2.3 Lake-effect snow</h3>
<p class="wx-def">Lake-effect snow falls in narrow, intense bands downwind of the Great Lakes when very cold air blows across lake water that is still unfrozen and much warmer than the air.</p>
<p>Cold air crossing open water is heated from below and gains moisture, so it rises in snow-shower clouds that line up with the wind. The longer the path over water (the fetch), the more heat and moisture the air gathers; an inversion higher up caps the clouds.</p>
<p><i>Snowfall.</i> Snow depth can vary by 100 cm (40 in) within 50 km (30 mi) (<a href="#ref-niziol1987">Niziol 1987</a>). On 18 November 2014 a band off Lake Erie stalled over Buffalo’s southern suburbs; snow fell at about 4 in (10 cm) per hour and passed 4 ft (1.2 m) locally. Because a small shift in wind direction moves the band, one town can get a dusting while the next gets several feet.</p>
<figure class="jn-fig wx-schem" id="fig-17">
  <svg viewBox="0 0 300 180" role="img" aria-labelledby="fig-17-cap">
    <rect x="30" y="150" width="170" height="30" fill="#c6dbef"/>
    <path d="M0 150 H30 V180 H0 Z" fill="#d9d9d9"/>
    <path d="M200 150 L300 136 V180 H200 Z" fill="#d9d9d9"/>
    <path d="M0 150 H200 L300 136" fill="none" stroke="#000" stroke-width="1"/>
    <line x1="0" y1="52" x2="300" y2="52" stroke="#000" stroke-width="1" stroke-dasharray="4 3"/>
    <line x1="8" y1="76" x2="70" y2="76" stroke="#2166ac" stroke-width="1.5" marker-end="url(#ar-b)"/>
    <g stroke="#b2182b" stroke-width="1.2"><line x1="55" y1="146" x2="55" y2="124" marker-end="url(#ar-r)"/><line x1="85" y1="146" x2="85" y2="124" marker-end="url(#ar-r)"/><line x1="115" y1="146" x2="115" y2="124" marker-end="url(#ar-r)"/></g>
    <g fill="#fff" stroke="#000" stroke-width="1"><path d="M145.0 115.0 C142.0 107.0 149.5 102.2 154.0 103.8 C155.5 98.2 166.0 98.2 166.6 103.8 C172.0 101.4 178.0 108.6 175.0 115.0 Z"/><path d="M180.0 114.0 C175.8 97.0 186.3 86.8 192.6 90.2 C194.7 78.3 209.4 78.3 210.2 90.2 C217.8 85.1 226.2 100.4 222.0 114.0 Z"/><path d="M224.0 114.0 C218.6 86.0 232.1 69.2 240.2 74.8 C242.9 55.2 261.8 55.2 262.9 74.8 C272.6 66.4 283.4 91.6 278.0 114.0 Z"/></g>
    <g stroke="#000" stroke-width="0.8" stroke-dasharray="2 3"><line x1="192" y1="114" x2="192" y2="146"/><line x1="206" y1="114" x2="206" y2="146"/><line x1="236" y1="114" x2="236" y2="142"/><line x1="250" y1="114" x2="250" y2="140"/><line x1="264" y1="114" x2="264" y2="138"/></g>
    <text x="6" y="46" font-size="10">inversion caps the clouds</text>
    <text x="8" y="70" font-size="10">very cold air</text>
    <text x="40" y="116" font-size="10">heat and moisture</text>
    <text x="40" y="168" font-size="10">lake water, warmer than the air</text>
    <text x="226" y="168" font-size="10">snow band</text>
  </svg>
  <figcaption id="fig-17-cap"><span class="jn-figno">Fig. 17.</span> Schematic cross-section along the wind across a lake. Very cold air (blue arrow) is heated and moistened by the lake (red arrows); clouds grow deeper downwind until they reach the inversion (dashed line), and snow (dotted lines) falls mostly on the downwind shore.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-18">
  <a href="/images/wx_systems_v3/lakeeffect_2014.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/lakeeffect_2014.png" alt="ERA5 maps for the lake-effect snow case, 2100 UTC 18 November 2014" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 18.</span> Lake Erie and Lake Ontario (red in a) are far warmer than the air 1.5 km up, and the wind blows along Lake Erie toward Buffalo, the arrangement that feeds a lake-effect snow band (ERA5, 2100 UTC [4 p.m. EST] 18 Nov 2014). (a) Lake surface minus 850-hPa temperature (K) and 850-hPa wind (barbs, kt). (b) Precipitation in the past hour (mm) and sea-level pressure (contours every 4 hPa). (c) Depth of the layer stirred by the surface (km). Over Lake Erie the difference is about 23 °C, well above the 13 °C rule of thumb.</figcaption>
</figure>
<p><i>How forecasters identify it.</i> The Buffalo NWS office’s guidance combined low-level temperature and wind, fetch, the turning of the wind with height, and lake temperature (<a href="#ref-niziol1987">Niziol 1987</a>). A common rule of thumb asks for the lake to be at least about 13 °C (23 °F) warmer than the air at 850 hPa, about 1.5 km up (<a href="#ref-niziol1995">Niziol et al. 1995</a>). ERA5’s 25–30 km grid shows the setting of a band but not the band itself. In Fig. 18a, at 2100 UTC (4 p.m. EST) 18 November 2014, the lake was about 23 °C (41 °F) warmer than the air at 850 hPa over Lake Erie, and the wind blew along the lake toward Buffalo.</p>
<blockquote class="wx-afd"><p>“The northern edge of this lake effect band is so sharply defined that snow amounts across the town of Cheektowaga range from just a few inches on the north side...to 4 feet across the southern portion of the town.”</p>
<footer>NWS Buffalo (BUF) Area Forecast Discussion, issued 4:44 p.m. EST 18 Nov 2014 (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201411182144-KBUF-FXUS61-AFDBUF">archived text</a>)</footer></blockquote>
</section>

<h2 id="sec-3">3. Boundary layer and radiation</h2>
<p>The boundary layer is the lowest one to two kilometers of the atmosphere, the part stirred by contact with the ground. How it heats by day and cools by night accounts for much of the error in forecasts of the daily high and low temperature.</p>

<section class="wx-sys" id="radiational-cooling">
<h3>3.1 Radiational cooling and cold pools</h3>
<p class="wx-def">On clear, calm nights the ground loses heat by radiating it to space, the air touching the ground cools, and the coldest air collects in valleys and low spots.</p>
<p>All surfaces radiate heat as infrared light. Clouds and water vapor send some of it back, so under a clear, dry sky the ground loses far more. With light wind an inversion forms and the surface air decouples, meaning that turbulence dies and the layers stop mixing. Dense cold air drains downhill and pools in valleys, and fresh snow deepens the chill.</p>
<p>Temperatures can differ by 10 °F (5–6 °C) over a few miles; hilltops, cities and windy spots stay milder. At 0900 UTC (4 a.m. EST) 6 January 2016 (Fig. 20) the air 400 m up was 5–10 °C warmer than at the ground over much of the interior, and the coldest ERA5 grid box, in the upper Connecticut River valley, was −11 °F (−24 °C).</p>
<p><i>Why it matters for forecasts.</i> At 210 U.S. airports in winter 2019–20, on mostly clear days, the GFS (the NWS global model) ran about 1 °C (2 °F) too warm at night and 2 °C (4 °F) too cold by day (<a href="#ref-patel2021">Patel et al. 2021</a>). In a cloudy cold pool, older versions of the HRRR, an NWS model with a 3-km grid, ran too cold because they made too little low cloud (<a href="#ref-adler2023">Adler et al. 2023</a>).</p>
<figure class="jn-fig wx-schem" id="fig-19">
  <div class="wx-two">
  <svg viewBox="0 0 300 180" role="img" aria-labelledby="fig-19-cap">
    <path d="M80 125 H220 V180 H80 Z" fill="#c6dbef"/>
    <path d="M0 70 C60 80 100 150 150 150 C200 150 240 80 300 70 V180 H0 Z" fill="#d9d9d9"/>
    <path d="M0 70 C60 80 100 150 150 150 C200 150 240 80 300 70" fill="none" stroke="#000" stroke-width="1"/>
    <line x1="93" y1="125" x2="207" y2="125" stroke="#2166ac" stroke-width="1" stroke-dasharray="4 3"/>
    <g stroke="#2166ac" stroke-width="1.5"><line x1="20" y1="64" x2="74" y2="104" marker-end="url(#ar-b)"/><line x1="280" y1="64" x2="226" y2="104" marker-end="url(#ar-b)"/></g>
    <g stroke="#b2182b" stroke-width="1.2"><line x1="115" y1="137" x2="115" y2="95" marker-end="url(#ar-r)"/><line x1="185" y1="137" x2="185" y2="95" marker-end="url(#ar-r)"/></g>
    <text x="8" y="16" font-size="10">clear, calm night</text>
    <text x="8" y="50" font-size="10">cold air drains downhill</text>
    <text x="196" y="50" font-size="10">hilltops stay milder</text>
    <text x="98" y="88" font-size="10">heat radiated to space</text>
    <text x="128" y="136" font-size="10">cold pool</text>
  </svg>
  <img src="/images/wx_systems_v2/schematics/radcool_drainage.jpg" alt="Drawing of a valley at night under a crescent moon, with arrows showing cold air flowing down both slopes into the valley floor.">
  </div>
  <figcaption id="fig-19-cap"><span class="jn-figno">Fig. 19.</span> Radiational cooling and a valley cold pool. (a) Schematic drawn for this page: the ground loses heat to space (red arrows), chilled air drains down the slopes (blue arrows) and collects in the valley (blue); the dashed line marks the top of the cold pool, where the inversion ends. (b) Nighttime drainage of cold air into a valley. From <a href="#ref-schroeder1970">Schroeder and Buck (1970)</a>; public domain (U.S. Government work).</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-20">
  <a href="/images/wx_systems_v3/radcool_2016.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/radcool_2016.png" alt="ERA5 maps for the radiational cooling case, 0900 UTC 6 January 2016" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 20.</span> Radiational cooling before dawn over New England, 0900 UTC (4 a.m. EST) 6 Jan 2016 (ERA5). (a) Total cloud cover (%; dark: clear) and sea-level pressure (contours every 2 hPa). (b) 2-m temperature (°C) and 10-m wind (barbs, kt). (c) Temperature 400 m above the ground minus 2-m temperature (K). Under clear, calm skies the ground cools fastest, so the air a few hundred meters up is 5–10 °C warmer than at the ground across the interior (deep red in c), while the ocean has no inversion. The coldest grid box, in the upper Connecticut River valley, is −24 °C.</figcaption>
</figure>
<p>Forecasts of the overnight low weigh cloud, wind, snow cover and the dewpoint, which sets a floor on the night’s low because dew or fog forms near it.</p>
<blockquote class="wx-afd"><p>“High pressure overhead along with clear skies/light winds was leading to an ideal night of radiational cooling. Low temps across many outlying locations will bottom out well down into the single digits. […] Coldest readings at 9 PM extended from Plymouth...to Falmouth and Marthas Vineyard...where that narrow swath of ocean effect snow cover was assisting in the radiational cooling. Meanwhile...continued mid level warm advection will hold overnight low temps generally in the 15 to 20 degree range across the typical non-decoupling locations of Worcester and Boston.”</p>
<footer>NWS Boston (BOX) Area Forecast Discussion, issued 9:40 p.m. EST 5 Jan 2016 (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201601060241-KBOX-FXUS61-AFDBOX">archived text</a>). Single digits °F are about −17 to −13 °C; 15–20 °F is about −9 to −7 °C. “Mid level warm advection” means warmer air arriving aloft (<a href="#overrunning">Section 3.3</a>).</footer></blockquote>
</section>

<section class="wx-sys" id="mixing-out">
<h3>3.2 Morning inversion and mixing out</h3>
<p class="wx-def">After a cold night, cold air often lies at the ground under warmer air until the sun’s heating stirs the two together, which forecasters call mixing out.</p>
<p>At dawn an inversion often fills the lowest few hundred meters, left by nighttime cooling (<a href="#radiational-cooling">Section 3.1</a>) or by trapped cold or ocean air. Sunlight heats the ground, and rising warm bubbles build a mixed layer that grows into the inversion from below (<a href="#ref-stull1988">Stull 1988</a>). Once it reaches the top, warmer air from above mixes down. The temperature can sit flat under fog or low cloud, then jump several degrees in an hour once it clears. If heating cannot break the inversion, the day stays gray.</p>
<p>The afternoon high therefore depends on when the inversion breaks, a timing that models find hard to predict. Five versions of a high-resolution forecast model, tested against spring balloon soundings in the central United States, all made the morning layer too cool and dry (<a href="#ref-coniglio2013">Coniglio et al. 2013</a>).</p>
<figure class="jn-fig wx-schem" id="fig-21">
  <svg viewBox="0 0 300 190" role="img" aria-labelledby="fig-21-cap">
    <rect x="40" y="120" width="250" height="40" fill="#c6dbef"/>
    <path d="M40 20 V160 H290" fill="none" stroke="#000" stroke-width="1"/>
    <g stroke="#000" stroke-width="1"><line x1="36" y1="160" x2="40" y2="160"/><line x1="36" y1="110" x2="40" y2="110"/><line x1="36" y1="60" x2="40" y2="60"/></g>
    <path d="M70 160 L160 120 L110 20" fill="none" stroke="#2166ac" stroke-width="1.5"/>
    <path d="M130.6 160 L115 140" fill="none" stroke="#000" stroke-width="1.2" stroke-dasharray="4 3"/>
    <path d="M199.6 160 L145 90" fill="none" stroke="#b2182b" stroke-width="1.5"/>
    <text x="32" y="163" font-size="10" text-anchor="end">0</text>
    <text x="32" y="113" font-size="10" text-anchor="end">0.5</text>
    <text x="32" y="63" font-size="10" text-anchor="end">1.0</text>
    <text x="12" y="90" font-size="10" text-anchor="middle" transform="rotate(-90 12 90)">height (km)</text>
    <text x="165" y="180" font-size="10" text-anchor="middle">temperature →</text>
    <text x="44" y="150" font-size="10">6 a.m.</text>
    <text x="134" y="150" font-size="10">9 a.m.</text>
    <text x="204" y="156" font-size="10">1 p.m.</text>
    <text x="192" y="134" font-size="10">dawn inversion layer</text>
    <text x="140" y="58" font-size="10">air above the inversion</text>
  </svg>
  <figcaption id="fig-21-cap"><span class="jn-figno">Fig. 21.</span> Schematic temperature profiles on a morning with a surface inversion (height above ground on the vertical axis). At 6 a.m. (blue) temperature rises with height through the lowest 400 m (shaded). By 9 a.m. (dashed) heating has built a shallow mixed layer that has eroded the lowest part of the inversion. By 1 p.m. (red) the mixed layer extends above the old inversion, and the surface is as warm as air brought down from aloft would be. Within a mixed layer, temperature falls about 10 °C per km.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-22">
  <a href="/images/wx_systems_v3/capping_2012.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/capping_2012.png" alt="ERA5 maps for the morning inversion case, 1200 and 1800 UTC 20 March 2012" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 22.</span> Morning fog over New York City lies under an inversion (red in a) that has mixed out by afternoon (b), and the surface temperature jumps (ERA5, 20 Mar 2012). (a, b) Temperature 400 m above the ground minus 2-m temperature (K; positive: inversion) and the 80% low-cloud contour at (a) 1200 UTC (8 a.m. EDT) and (b) 1800 UTC (2 p.m.). (c) Temperature profile nearest LaGuardia Airport at 1200 UTC (solid) and 1800 UTC (dashed); squares are observations. ERA5’s 2-m temperature rises from 12 to 18 °C, the observed from 11 to 19 °C.</figcaption>
</figure>
<p>The 1200 UTC (8 a.m. EDT) balloon sounding shows the inversion. Forecasters estimate the high from the temperature at the level where mixing should top out, often 925 or 850 hPa, adding about 10 °C for each kilometer the air descends to the ground.</p>
<p>On 20 March 2012 (Fig. 22) fog lay under an inversion over New York City. LaGuardia Airport stayed at 51–52 °F (11 °C) until 9:51 a.m. EDT, rose 7 °F (4 °C) in the hour to 11:51 a.m. as the fog cleared, and reached 72 °F (22 °C) by 2:51 p.m.</p>
<blockquote class="wx-afd"><p>“There is an inversion above the surface up to around 950 mb. Light southeasterly flow helps trap moisture beneath this inversion. […] We start to mix out towards afternoon once inversion breaks. This would promote increased daytime warmth as cloud cover decreases. This timing will be crucial for max temp forecast today...potentially higher or lower depending on when exactly the low clouds and fog scatter out.”</p>
<footer>NWS New York (OKX) Area Forecast Discussion, issued 7:43 a.m. EDT 20 Mar 2012 (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201203201143-KOKX-FXUS61-AFDOKX">archived text</a>). 950 mb is 950 hPa, about 600 m above the ground here; the morning balloon sounding from Upton, N.Y., put the top of the inversion lower, near 300 m.</footer></blockquote>
</section>

<section class="wx-sys" id="overrunning">
<h3>3.3 Overrunning and the midnight high</h3>
<p class="wx-def">Overrunning is warm air flowing over colder air at the ground, usually ahead of a warm front; if warm air keeps arriving overnight, the day’s high can come near midnight.</p>
<p><i>How it forms.</i> A warm front is the leading edge of advancing warm air, which, being lighter, slides up over the cold air. This warm advection (warm air carried in by the wind) continues after sunset. The surface warms when the front passes, or sooner if wind mixes the warm air down.</p>
<p><i>Climatology.</i> In December–February 2000–2023 (hourly airport data), the day’s high came in the last hour of the day on 8% of days at Boston and 10% at New York. Highs in the first hour, followed by falling temperatures (usually behind a cold front), were more common: 12% and 14%. Together, about one winter day in five at Boston (20%) and one in four at New York (24%) had its high within an hour of midnight. A daily-high forecast must therefore cover the whole calendar day, midnight to midnight local standard time.</p>
<figure class="jn-fig wx-schem" id="fig-23">
  <svg viewBox="0 0 300 200" role="img" aria-labelledby="fig-23-cap">
    <path d="M20 18 V68 H150" fill="none" stroke="#000" stroke-width="1"/>
    <path d="M20 26 C40 28 50 40 70 52 S120 60 150 62" fill="none" stroke="#2166ac" stroke-width="1.5"/>
    <path d="M20 60 C60 62 85 50 110 44 S140 26 148 22" fill="none" stroke="#b2182b" stroke-width="1.5"/>
    <text x="24" y="14" font-size="10">temperature</text>
    <text x="14" y="80" font-size="10">midnight</text>
    <text x="85" y="80" font-size="10" text-anchor="middle">noon</text>
    <text x="152" y="80" font-size="10" text-anchor="end">midnight</text>
    <text x="154" y="25" font-size="10">warm front at night</text>
    <text x="154" y="65" font-size="10">cold front by day</text>
    <polygon points="0,95 300,95 300,110 110,185 0,185" fill="#fcbba1"/>
    <polygon points="110,185 300,110 300,185" fill="#c6dbef"/>
    <line x1="110" y1="185" x2="300" y2="110" stroke="#000" stroke-width="1"/>
    <rect x="0" y="185" width="300" height="15" fill="#d9d9d9"/>
    <line x1="0" y1="185" x2="300" y2="185" stroke="#000" stroke-width="1"/>
    <path d="M20 175 C80 175 120 168 200 140 S270 110 292 100" fill="none" stroke="#b2182b" stroke-width="1.5" marker-end="url(#ar-r)"/>
    <g stroke="#000" stroke-width="0.8" stroke-dasharray="2 2"><line x1="230" y1="130" x2="230" y2="142"/><line x1="250" y1="122" x2="250" y2="140"/><line x1="270" y1="116" x2="270" y2="138"/></g>
    <text x="16" y="150" font-size="10">warm air glides up</text>
    <text x="16" y="162" font-size="10">over the cold air</text>
    <text x="240" y="176" font-size="10">cold air</text>
    <text x="4" y="197" font-size="10">← south</text>
    <text x="110" y="197" font-size="10" text-anchor="middle">warm front</text>
    <text x="262" y="197" font-size="10">north →</text>
  </svg>
  <figcaption id="fig-23-cap"><span class="jn-figno">Fig. 23.</span> Overrunning and the midnight high. Top: illustrative (not observed) temperature through one calendar day when a warm front arrives at night (red; the high comes just before midnight) and when a cold front passes in the morning (blue; the high comes just after midnight). Bottom: schematic south–north cross-section of a warm front. Warm air (red shading and arrow) glides up over the wedge of cold air at the ground (blue), producing cloud and steady precipitation (dashes) on the cold side.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-24">
  <a href="/images/wx_systems_v3/warmadv_2022.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/warmadv_2022.png" alt="ERA5 maps for the overrunning case, 0300 UTC 23 February 2022, with Boston temperatures for 22–23 February" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 24.</span> Boston’s warmest reading of 22 February 2022 came just before midnight, because strong south-southwest wind aloft kept carrying warm air north all evening (ERA5, 0300 UTC 23 Feb [10 p.m. EST 22 Feb]). (a) 2-m temperature (°C), sea-level pressure (contours every 2 hPa) and 10-m wind (barbs, kt). (b) Warming by the 850-hPa wind (K h⁻¹; red: warm air arriving), 850-hPa temperature (contours every 2 °C) and wind. (c) Hourly temperature at Boston Logan Airport; gray marks night. Boston sat near 6 °C all afternoon and reached 13 °C (55 °F) at 11:54 p.m. EST.</figcaption>
</figure>
<p>The signal at 925 or 850 hPa is wind blowing from warmer toward colder areas, as in Fig. 24b. Forecasters also track the warm front and any low-level jet (<a href="#low-level-jet">Section 3.4</a>).</p>
<p>On 22 February 2022 (Fig. 24) Boston stayed near 42 °F (6 °C) all afternoon, rose to 53 °F (12 °C) between 6 and 8 p.m. EST as the warm front passed, and kept warming in strong south-southwesterly wind aloft, reaching the day’s high, 55 °F (13 °C), at 11:54 p.m.</p>
<blockquote class="wx-afd"><p>“Lastly, will see non-diurnal temperature trend due to the strong warm air advection as we are within the warm sector. […] Temperatures will increase as the night progresses with most in the 50s after midnight.”</p>
<footer>NWS Boston (BOX) Area Forecast Discussion, issued 3:47 p.m. EST 22 Feb 2022 (<a href="https://mesonet.agron.iastate.edu/p.php?pid=202202222047-KBOX-FXUS61-AFDBOX">archived text</a>). A non-diurnal trend is one that does not follow the usual rise by day and fall at night; the warm sector is the warm air between a low’s warm front and its cold front.</footer></blockquote>
</section>

<section class="wx-sys" id="low-level-jet">
<h3>3.4 Nocturnal low-level jet</h3>
<p class="wx-def">A nocturnal low-level jet is a band of fast wind a few hundred meters above the ground that forms at night while the air at the ground is calm.</p>
<p><i>How it forms.</i> Because Earth rotates, moving air is deflected to the right in the Northern Hemisphere. The geostrophic wind is the wind at which this deflection exactly balances the push from high to low pressure. By day, turbulence acts like friction and holds the low-level wind below that speed. After sunset an inversion (<a href="#radiational-cooling">Section 3.1</a>) cuts the air above it off from the ground. Freed from friction, the wind swings around the geostrophic wind in speed and direction, an inertial oscillation lasting about 18 h at New England’s latitude (12 h divided by the sine of the latitude), and for part of the night the wind is faster than the geostrophic wind (<a href="#ref-blackadar1957">Blackadar 1957</a>; <a href="#ref-vandewiel2010">Van de Wiel et al. 2010</a>).</p>
<p>With southerly flow the jet carries warm, moist air north and can feed storms at night. Its strength in a forecast depends on how the model handles nighttime mixing.</p>
<figure class="jn-fig wx-schem" id="fig-25">
  <svg viewBox="0 0 300 190" role="img" aria-labelledby="fig-25-cap">
    <rect x="40" y="135" width="250" height="25" fill="#c6dbef"/>
    <path d="M40 20 V160 H290" fill="none" stroke="#000" stroke-width="1"/>
    <g stroke="#000" stroke-width="1"><line x1="36" y1="160" x2="40" y2="160"/><line x1="36" y1="110" x2="40" y2="110"/><line x1="36" y1="60" x2="40" y2="60"/></g>
    <line x1="200" y1="20" x2="200" y2="160" stroke="#000" stroke-width="0.8" stroke-dasharray="2 3"/>
    <path d="M40 160 C90 158 150 150 168 132 L172 60 C175 45 190 30 198 20" fill="none" stroke="#000" stroke-width="1" stroke-dasharray="5 3"/>
    <path d="M40 160 C50 158 80 152 140 140 C210 128 262 116 262 104 C262 88 220 70 204 40 L200 20" fill="none" stroke="#000" stroke-width="1.6"/>
    <text x="32" y="163" font-size="10" text-anchor="end">0</text>
    <text x="32" y="113" font-size="10" text-anchor="end">0.5</text>
    <text x="32" y="63" font-size="10" text-anchor="end">1.0</text>
    <text x="12" y="90" font-size="10" text-anchor="middle" transform="rotate(-90 12 90)">height (km)</text>
    <text x="165" y="180" font-size="10" text-anchor="middle">wind speed →</text>
    <text x="210" y="14" font-size="10">geostrophic wind</text>
    <text x="118" y="100" font-size="10">afternoon</text>
    <text x="96" y="132" font-size="10">3 a.m.</text>
    <text x="266" y="107" font-size="10">jet</text>
    <text x="208" y="154" font-size="10">surface inversion</text>
  </svg>
  <figcaption id="fig-25-cap"><span class="jn-figno">Fig. 25.</span> Schematic wind-speed profiles. In the afternoon (dashed) mixing spreads friction through the lowest kilometer and the wind stays below the geostrophic wind (dotted line). At about 3 a.m. (solid) the wind is nearly calm inside the surface inversion (shaded) but exceeds the geostrophic wind a few hundred meters up, forming the jet.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-26">
  <a href="/images/wx_systems_v3/llj_2017.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/llj_2017.png" alt="ERA5 maps for the low-level jet case, 2100 UTC 10 June and 0800 UTC 11 June 2017" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 26.</span> Nocturnal low-level jet at Elmira, N.Y., 10–11 Jun 2017 (ERA5). (a, b) 900-hPa wind speed (shading, kt) and wind (barbs, kt) at (a) 2100 UTC (5 p.m. EDT) and (b) 0800 UTC (4 a.m.). (c) Wind-speed profiles at Elmira at both times, with the 0800 UTC geostrophic wind. Overnight the wind about 600 m above the ground doubles and outruns the geostrophic wind, while the wind at the ground stays light.</figcaption>
</figure>
<p>Forecasters compare wind profiles of the lowest 1–2 km, from Doppler radar, wind profilers (upward-pointing wind radars), lidar (laser radar) or balloons, with the geostrophic wind.</p>
<p>On the clear night of 10–11 June 2017 (Fig. 26), ERA5’s wind at Elmira, N.Y., 600 m above the ground rose from 19 kt at 2100 UTC (5 p.m. EDT) to 38 kt at 0800 UTC (4 a.m.), faster than the geostrophic wind (27 kt); at the ground it stayed near 8 kt.</p>
<blockquote class="wx-afd"><p>“Mostly clear night foreseen, with decoupling wind at the surface as southwesterly low level jet develops just aloft.” […] “...a developing 34-38 knot low level jet around 2 kft agl out of the west-southwest as warm air overspreads the region.”</p>
<footer>NWS Binghamton, N.Y. (BGM) Area Forecast Discussion, issued 2:52 p.m. EDT 10 Jun 2017 (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201706101852-KBGM-FXUS61-AFDBGM">archived text</a>); the second passage is from its aviation section. Decoupling means the air at the ground is cut off from the faster wind above; 2 kft agl is 2000 ft (600 m) above ground level.</footer></blockquote>
</section>

<h2 id="sec-4">4. Winter precipitation and rapidly deepening cyclones</h2>
<p>In winter, thin layers of air a little above or below freezing decide whether precipitation reaches the ground as snow, sleet, freezing rain or rain. The strongest winter storms also deepen unusually fast.</p>

<section class="wx-sys" id="freezing-rain">
<h3>4.1 Freezing rain and ice storms</h3>
<p class="wx-def">Freezing rain is rain that falls through shallow below-freezing air near the ground and freezes on contact with cold surfaces, coating them in ice.</p>
<p>Falling snow melts in a layer warmer than 0 °C (32 °F), the warm nose, usually 1–3 km up. Below lies a shallow below-freezing layer, often cold air dammed against the Appalachians (<a href="#cold-air-damming">Section 2.1</a>). If that layer is thin, the drops cool below 0 °C but stay liquid (supercooled) and freeze on contact. If it is deeper, they refreeze into ice pellets (sleet).</p>
<p><i>Effects.</i> Rain falls at 28–32 °F (−2 to 0 °C) and freezes on every surface; a quarter inch (6 mm) or more brings down branches and power lines. A change of a degree or two in either layer can turn freezing rain into sleet or plain rain.</p>
<figure class="jn-fig wx-schem" id="fig-27">
  <svg viewBox="0 0 300 200" role="img" aria-labelledby="fig-27-cap">
    <rect width="300" height="200" fill="#fff"/>
    <polygon points="120,80 150,100 120,132" fill="#fcbba1"/>
    <polygon points="120,132 100,170 120,170" fill="#c6dbef"/>
    <rect x="40" y="170" width="250" height="12" fill="#d9d9d9"/>
    <line x1="40" y1="170" x2="290" y2="170" stroke="#000" stroke-width="1"/>
    <line x1="120" y1="16" x2="120" y2="170" stroke="#000" stroke-width="0.8" stroke-dasharray="3 3"/>
    <text x="120" y="12" font-size="10" text-anchor="middle">0 °C (32 °F)</text>
    <path d="M85 18 L105 70 L150 100 L120 132 L100 170" fill="none" stroke="#000" stroke-width="1.8"/>
    <line x1="28" y1="170" x2="28" y2="22" stroke="#000" stroke-width="1" marker-end="url(#ar-k)"/>
    <text transform="translate(22 96) rotate(-90)" font-size="10" text-anchor="middle">height</text>
    <line x1="70" y1="192" x2="190" y2="192" stroke="#000" stroke-width="1" marker-end="url(#ar-k)"/>
    <text x="196" y="195" font-size="10">temperature</text>
    <text x="158" y="48" font-size="10">snow (below 0 °C)</text>
    <text x="156" y="98" font-size="10">warm layer (warm nose):</text>
    <text x="156" y="110" font-size="10">snow melts to rain</text>
    <text x="128" y="148" font-size="10">shallow cold layer:</text>
    <text x="128" y="160" font-size="10">drops supercool</text>
    <text x="128" y="180" font-size="9">rain freezes on ground below 0 °C</text>
  </svg>
  <figcaption id="fig-27-cap"><span class="jn-figno">Fig. 27.</span> Schematic temperature profile for freezing rain. The black curve is air temperature (horizontal axis) against height (vertical axis); the dashed line marks 0 °C. Where the curve lies right of the dashed line (red shading) the air is above freezing and falling snow melts. In the shallow below-freezing layer near the ground (blue shading) the rain cools below 0 °C without freezing, then freezes on contact with the ground, trees and wires. A deeper cold layer would refreeze the drops in the air as sleet.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-28">
  <a href="/images/wx_systems_v3/freezingrain_2008.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/freezingrain_2008.png" alt="ERA5 maps for the freezing rain case, 0900 UTC 12 December 2008" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 28.</span> Air about 1–3 km up is well above freezing (red in a) over below-freezing ground in southern New Hampshire, so rain freezes on contact (ERA5, 0900 UTC [4 a.m. EST] 12 Dec 2008). (a) Warmest temperature aloft (°C), where the ground is below 0 °C, and 2-m temperature (contours every 2 °C; thick: 0 °C). (b) Melting energy of the warm layer, PA (J kg⁻¹), and refreezing energy of the cold layer, NA (dashed: −25, −50, −100 J kg⁻¹). (c) Temperature and dewpoint above Manchester, N.H.: 9 °C aloft, −2 °C at the ground.</figcaption>
</figure>
<p><i>How forecasters identify it.</i> The precipitation type is read from the sounding, which <a href="#ref-bourgouin2000">Bourgouin (2000)</a> reduced to two numbers: a melting energy for the warm layer (PA, for positive area) and a refreezing energy for the cold layer (NA, negative area), which together indicate the type (Fig. 28b). <a href="#ref-birk2021">Birk et al. (2021)</a> revised the method to use the wet-bulb temperature (the temperature air reaches when water evaporates into it) and to give probabilities. In the ice storm of December 2008, Worcester reported freezing rain at 30–31 °F (about −1 °C) for ten hours from the afternoon of 11 December. ERA5 at 0900 UTC (4 a.m. EST) 12 December (Fig. 28) has a warm nose of up to 9 °C (48 °F) above below-freezing air over southern New Hampshire.</p>
<blockquote class="wx-afd"><p>“Low pressure moving northeastward from the southeast states will bring lots of precipitation with it...which will fall into the low level cold air. This will result in an ice storm for portions of interior southern New England tonight.”</p>
<footer>NWS Boston (BOX) Area Forecast Discussion, issued 6:40 p.m. EST 11 Dec 2008 (2340 UTC) (<a href="https://mesonet.agron.iastate.edu/p.php?pid=200812112340-KBOX-FXUS61-AFDBOX">archived text</a>)</footer></blockquote>
</section>

<section class="wx-sys" id="bomb-cyclone">
<h3>4.2 Bomb cyclone</h3>
<p class="wx-def">A bomb cyclone is a storm whose central pressure falls unusually fast: by about 24 hPa in 24 hours at 60° latitude, and by less at lower latitudes, about 18–20 hPa at New England’s latitude.</p>
<p><i>How it forms.</i> Off the East Coast in winter, cold continental air lies beside warm air over the Gulf Stream. A strong jet stream removes air from the top of the storm faster than it flows in below, so the surface pressure drops, and heat released by condensing water vapor speeds this up. <a href="#ref-sanders1980">Sanders and Gyakum (1980)</a> set the threshold at 60°N, the latitude of southern Greenland, and lowered it toward the equator, where the same wind comes with a smaller pressure difference (the threshold is 24 hPa × sin latitude / sin 60°).</p>
<p>Winds rise quickly, and the storm brings heavy snow or rain and coastal flooding.</p>
<figure class="jn-fig wx-schem" id="fig-29">
  <svg viewBox="0 0 300 168" role="img" aria-labelledby="fig-29-cap">
    <rect width="300" height="168" fill="#fff"/>
    <g fill="none" stroke="#000" stroke-width="0.9">
      <circle cx="70" cy="86" r="16"/><circle cx="70" cy="86" r="32"/><circle cx="70" cy="86" r="48"/>
      <circle cx="220" cy="86" r="10"/><circle cx="220" cy="86" r="16"/><circle cx="220" cy="86" r="22"/><circle cx="220" cy="86" r="28"/><circle cx="220" cy="86" r="34"/>
      <circle cx="220" cy="86" r="40"/><circle cx="220" cy="86" r="46"/><circle cx="220" cy="86" r="52"/><circle cx="220" cy="86" r="58"/><circle cx="220" cy="86" r="64"/>
    </g>
    <text x="70" y="91" font-size="13" text-anchor="middle">L</text>
    <text x="220" y="91" font-size="13" text-anchor="middle">L</text>
    <line x1="121" y1="86" x2="150" y2="86" stroke="#000" stroke-width="1.2" marker-end="url(#ar-k)"/>
    <text x="135" y="80" font-size="10" text-anchor="middle">24 h</text>
    <text x="70" y="152" font-size="10" text-anchor="middle">start: center ≈ 1000 hPa</text>
    <text x="220" y="163" font-size="10" text-anchor="middle">24 h later: center ≈ 972 hPa</text>
    <text x="6" y="14" font-size="10">isobars every 4 hPa</text>
    <text x="294" y="14" font-size="10" text-anchor="end">closer isobars, stronger wind</text>
  </svg>
  <figcaption id="fig-29-cap"><span class="jn-figno">Fig. 29.</span> Schematic map view of a bomb cyclone. Circles are isobars (lines of equal sea-level pressure, every 4 hPa) around the storm center (L). In 24 h the central pressure falls by 28 hPa, more than the 18–20 hPa threshold at New England’s latitude (<a href="#ref-sanders1980">Sanders and Gyakum 1980</a>). The isobars crowd together as the storm deepens, and the winds strengthen accordingly.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-30">
  <a href="/images/wx_systems_v3/bomb_2018.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/bomb_2018.png" alt="ERA5 maps for the bomb cyclone case, 1200 UTC 4 January 2018, with central pressure for 3–5 January" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 30.</span> The storm’s central pressure fell 51 hPa in 24 hours (c), 3.5 times the rate that defines a bomb at its latitude; the deep blue patch in (a) is where pressure fell most (ERA5, 3–5 Jan 2018). (a) Sea-level pressure at 1200 UTC 4 Jan (contours every 4 hPa) and its 24-h change (hPa); dots mark the low every 6 h from 1200 UTC 3 Jan. (b) 300-hPa wind speed, about 9 km up (kt), and 500-hPa height (contours every 6 dam). (c) Central pressure, hourly; gray marks the fall from 1009 to 958 hPa.</figcaption>
</figure>
<p><i>How forecasters identify it.</i> The test is the 24-h fall in central pressure compared with the threshold. In ERA5 (Fig. 30) the central pressure of the January 2018 storm fell 51 hPa in 24 h, from 1009 hPa (close to the average sea-level pressure of 1013 hPa) to 958 hPa, between 1200 UTC (7 a.m. EST) 3 and 4 January. Most of the fall came off the Southeast coast, at an average latitude of about 31°N (near the Georgia–Florida border), where the threshold is about 14 hPa, so the storm deepened about 3.5 times faster than the threshold. Passing New England, it pushed the Boston tide gauge to its highest level since records began in 1921 (<a href="https://www.bostonglobe.com/metro/2018/01/05/official-boston-breaks-tide-record/UPbwDxgF0QXNOWvB9bcQ7L/story.html">Boston Globe, 5 Jan 2018</a>).</p>
<blockquote class="wx-afd"><p>“…a massive bombing surface low taking shape up the E coast, lowering down to around 950 mb offshore of New England as it quickly races NNE into SE Canada Thursday morning.”</p>
<footer>NWS Boston (BOX) Area Forecast Discussion, issued 5:04 p.m. EST 3 Jan 2018 (2204 UTC) (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201801032204-KBOX-FXUS61-AFDBOX">archived text</a>)</footer></blockquote>
</section>

<section class="wx-sys" id="alberta-clipper">
<h3>4.3 Alberta clipper</h3>
<p class="wx-def">An Alberta clipper is a small, fast-moving low that forms east of the Canadian Rockies and races southeast toward the Great Lakes and the Northeast, bringing light snow followed by a surge of arctic air.</p>
<p>Pacific air descending the Canadian Rockies forms a low-pressure trough on their sheltered (lee) side. A small disturbance in the jet stream (a short-wave trough) turns it into a low, which strong northwest winds aloft carry quickly southeast. Of 177 clippers in <a href="#ref-thomas2007">Thomas and Martin (2007)</a>, most occurred in December and January and tracked toward or just north of Lake Superior; fewer than 10% passed south of the Great Lakes.</p>
<p>A clipper brings a few inches (under 10 cm) of light, powdery snow from cold, dry air, then gusty northwest winds and sharp cooling.</p>
<figure class="jn-fig wx-schem" id="fig-31">
  <svg viewBox="0 0 300 168" role="img" aria-labelledby="fig-31-cap">
    <rect width="300" height="168" fill="#fff"/>
    <ellipse cx="112" cy="72" rx="24" ry="7" fill="#c6dbef" stroke="#000" stroke-width="0.7"/>
    <text x="112" y="90" font-size="9" text-anchor="middle">Lake Superior</text>
    <ellipse cx="212" cy="66" rx="40" ry="11" fill="#c6dbef" opacity="0.6"/>
    <path d="M18 26 C 60 34, 95 46, 130 54 C 170 62, 220 70, 282 80" fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="6 4" marker-end="url(#ar-k)"/>
    <text x="10" y="17" font-size="10">Alberta</text>
    <circle cx="180" cy="62" r="8" fill="#fff" stroke="#000" stroke-width="0.8"/>
    <text x="180" y="67" font-size="12" text-anchor="middle">L</text>
    <circle cx="146" cy="56" r="6" fill="#fff"/>
    <text x="146" y="60" font-size="12" text-anchor="middle">×</text>
    <text x="128" y="38" font-size="10">× = spin maximum aloft (500 hPa)</text>
    <text x="196" y="90" font-size="10">light snow</text>
    <line x1="104" y1="96" x2="132" y2="122" stroke="#2166ac" stroke-width="1.6" marker-end="url(#ar-b)"/>
    <line x1="74" y1="100" x2="102" y2="126" stroke="#2166ac" stroke-width="1.6" marker-end="url(#ar-b)"/>
    <text x="40" y="146" font-size="10">arctic air follows the low</text>
    <text x="256" y="104" font-size="10" text-anchor="middle">New England</text>
    <line x1="288" y1="38" x2="288" y2="16" stroke="#000" stroke-width="1" marker-end="url(#ar-k)"/>
    <text x="288" y="50" font-size="10" text-anchor="middle">N</text>
  </svg>
  <figcaption id="fig-31-cap"><span class="jn-figno">Fig. 31.</span> Schematic map of an Alberta clipper. The dashed arrow is a clipper's track from the lee of the Rockies in Alberta, passing just north of Lake Superior toward New England. L is the surface low and × the strongest spin in the winds at 500 hPa (about 5.5 km up), which stays west of the surface low (<a href="#ref-thomas2007">Thomas and Martin 2007</a>). Light blue shading is the band of light snow; blue arrows show arctic air moving in behind the low.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-32">
  <a href="/images/wx_systems_v3/clipper_2008.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/clipper_2008.png" alt="ERA5 maps for the Alberta clipper case, 0000 UTC 23 January 2008" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 32.</span> The clipper’s surface low (L) lies east of the strongest spin aloft (dark red over southern Ontario), and colder air follows behind it (blue in b) (ERA5, 0000 UTC 23 Jan 2008 [7 p.m. EST 22 Jan]). (a) Spin of the wind at 500 hPa, about 5.5 km up (10⁻⁵ s⁻¹), and sea-level pressure (contours every 4 hPa). (b) 1000–500-hPa thickness, which shrinks as the air cools (contours every 6 dam), and its 12-h change (dam). (c) 2-m temperature (°C) and 10-m wind (barbs, kt). The spin maximum is about 450 km west of the low.</figcaption>
</figure>
<p><i>How forecasters identify it.</i> The short-wave trough is found on 500-hPa maps, together with falling thickness (the depth of a layer of air, which shrinks as the air cools). In the <a href="#ref-thomas2007">Thomas and Martin</a> composite, the strongest spin of the winds at 500 hPa stays west of the surface low once the clipper leaves the Rockies, so the surface low runs ahead of the disturbance aloft that drives it. A clipper reached the New York–Quebec border at 7 p.m. EST on 22 January 2008 (0000 UTC 23 January; Fig. 32), with the strongest spin aloft 450 km west. That afternoon Worcester and Hartford had light snow and Boston light rain.</p>
<blockquote class="wx-afd"><p>“A clipper moves across the region Tue and Tue night. … Reinforcing shot of cold air flows into region behind this system.”</p>
<footer>NWS Boston (BOX) Area Forecast Discussion, issued 5:21 p.m. EST 19 Jan 2008 (2221 UTC) (<a href="https://mesonet.agron.iastate.edu/p.php?pid=200801192221-KBOX-FXUS61-AFDBOX">archived text</a>)</footer></blockquote>
</section>

<h2 id="sec-5">5. Convective and mesoscale boundaries</h2>
<p>Thunderstorms create boundaries tens to hundreds of kilometers long, and other boundaries set thunderstorms off. Most are too narrow to appear clearly in a reanalysis with a 25–30 km grid, so the maps for these cases show the setting rather than the boundary itself.</p>

<section class="wx-sys" id="gust-front">
<h3>5.1 Gust front and cold pool</h3>
<p class="wx-def">A gust front is the leading edge of the cool air that spreads out from under a thunderstorm; when it passes, the wind gusts and changes direction and the temperature drops within minutes.</p>
<p><i>How it forms.</i> Rain evaporating below a thunderstorm cools the air. The denser air sinks as a downdraft and spreads along the ground as a cold pool about 1 km deep, a flow of dense fluid under lighter fluid called a gravity current (<a href="#ref-charba1974">Charba 1974</a>). Its leading edge is the gust front.</p>
<p>Behind the gust front the temperature can fall more than 10 °F (5.5 °C), and a low shelf cloud often accompanies it. New storms tend to form where it lifts the humid air ahead.</p>
<figure class="jn-fig wx-schem" id="fig-33">
  <svg viewBox="0 0 300 168" role="img" aria-labelledby="fig-33-cap">
    <rect width="300" height="168" fill="#fff"/>
    <ellipse cx="215" cy="38" rx="62" ry="22" fill="#f2f2f2" stroke="#000" stroke-width="0.8"/>
    <ellipse cx="195" cy="56" rx="36" ry="11" fill="#f2f2f2" stroke="#000" stroke-width="0.8"/>
    <text x="215" y="36" font-size="10" text-anchor="middle">thunderstorm</text>
    <path d="M250 142 L250 122 C 200 116, 130 114, 80 120 C 62 123, 54 132, 52 142 Z" fill="#c6dbef" stroke="#2166ac" stroke-width="1"/>
    <line x1="196" y1="70" x2="193" y2="118" stroke="#2166ac" stroke-width="1.6" marker-end="url(#ar-b)"/>
    <line x1="222" y1="70" x2="220" y2="118" stroke="#2166ac" stroke-width="1.6" marker-end="url(#ar-b)"/>
    <text x="232" y="88" font-size="10">rain-cooled</text>
    <text x="232" y="100" font-size="10">downdraft</text>
    <line x1="170" y1="134" x2="88" y2="134" stroke="#2166ac" stroke-width="1.6" marker-end="url(#ar-b)"/>
    <text x="178" y="138" font-size="10">cold pool</text>
    <path d="M4 132 L38 132 C 48 130, 54 112, 62 80" fill="none" stroke="#b2182b" stroke-width="1.8" marker-end="url(#ar-r)"/>
    <text x="6" y="40" font-size="10">warm, humid air is</text>
    <text x="6" y="52" font-size="10">lifted at the gust front;</text>
    <text x="6" y="64" font-size="10">new storms can form</text>
    <rect x="0" y="142" width="300" height="26" fill="#d9d9d9"/>
    <line x1="0" y1="142" x2="300" y2="142" stroke="#000" stroke-width="1"/>
    <line x1="52" y1="142" x2="52" y2="148" stroke="#000" stroke-width="1"/>
    <text x="52" y="158" font-size="10" text-anchor="middle">gust front</text>
    <text x="294" y="158" font-size="10" text-anchor="end">ground</text>
  </svg>
  <figcaption id="fig-33-cap"><span class="jn-figno">Fig. 33.</span> Schematic vertical cross-section through a thunderstorm and its outflow. Blue arrows under the cloud are the downdraft of air cooled by evaporating rain; on reaching the ground it spreads out as the cold pool (blue shading), here moving to the left. The gust front is the leading edge of the cold pool. The red arrow shows warm, humid air ahead of the storm being forced upward over the cold pool, where new storm cells can form. Not to scale: the cold pool is roughly 1 km deep and may extend tens of kilometers from the storm.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-34">
  <a href="/images/wx_systems_v3/gustfront_2013.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/gustfront_2013.png" alt="ERA5 maps for the gust front case, 1800 UTC 8 July 2013" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 34.</span> Cooler air lies north of a boundary across Vermont, New Hampshire and Maine (arrow in a), under the area where morning storms rained (b); the gust front itself, only a few kilometers wide, is too narrow for the reanalysis (ERA5, 1800 UTC [2 p.m. EDT] 8 Jul 2013). (a) 2-m temperature (°C) and 10-m wind (barbs, kt). (b) Rain from 0600 to 1500 UTC (mm) and 1800 UTC 2-m temperature (contours at 24 and 28 °C). Along 72°W the temperature falls from 26 to 20 °C across about 170 km.</figcaption>
</figure>
<p><i>How forecasters identify it.</i> Radar often shows a gust front as a thin line of weak echo (signal reflected back to the radar), and surface stations record the pressure jump, cooling and wind shift. <a href="#ref-wakimoto1982">Wakimoto (1982)</a> traced the life cycle of gust fronts with Doppler radar and weather balloons. Gust fronts are easily confused with backdoor and sea-breeze fronts (<a href="#backdoor-front">Sections 1.2</a> and <a href="#sea-breeze">1.1</a>), as on 8 July 2013. At 10:37 a.m. EDT the Boston office described a boundary moving south as possible outflow from morning storms; by 2:38 p.m. it called the same boundary a “back door cold front/sea breeze” (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201307081838-KBOX-FXUS61-AFDBOX">archived text</a>). ERA5 shows the cooler air north of the boundary at 1800 UTC (2 p.m. EDT; Fig. 34).</p>
<blockquote class="wx-afd"><p>“Surface analysis show[s] that a weak boundary...perhaps outflow from morning convection is moving southward towards SNE [southern New England]. In fact winds are out of the NE at MHT/LWM and BVY.”</p>
<footer>NWS Boston (BOX) Area Forecast Discussion, issued 10:37 a.m. EDT 8 Jul 2013 (1437 UTC); MHT, LWM and BVY are airports in Manchester, N.H., Lawrence and Beverly, Mass. (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201307081437-KBOX-FXUS61-AFDBOX">archived text</a>)</footer></blockquote>
</section>

<section class="wx-sys" id="derecho">
<h3>5.2 Derecho</h3>
<p class="wx-def">A derecho is a long-lived windstorm produced by a fast-moving line or cluster of thunderstorms, whose straight-line winds damage a swath at least 400 km (250 mi) long.</p>
<p><i>How it forms.</i> New storms keep forming at the leading edge of a thunderstorm cluster’s strong cold pool, so the system moves faster than the winds around it. Air flowing in from behind, the rear-inflow jet, descends toward the ground and pushes the middle of the line ahead of its ends, bowing it into a bow echo on radar. The strongest winds are at the apex of the bow. Most derechos occur in the central United States.</p>
<p>Gusts reach 60–90 mph (27–40 m s⁻¹), felling trees and power lines.</p>
<figure class="jn-fig wx-schem" id="fig-35">
  <svg viewBox="0 0 300 168" role="img" aria-labelledby="fig-35-cap">
    <rect width="300" height="168" fill="#fff"/>
    <path d="M70 28 C 140 18, 200 40, 222 84 C 200 128, 140 150, 70 140 C 112 104, 112 64, 70 28 Z" fill="#d9d9d9" stroke="#000" stroke-width="0.8"/>
    <path d="M70 28 C 140 18, 200 40, 222 84 C 200 128, 140 150, 70 140" fill="none" stroke="#000" stroke-width="2.2"/>
    <line x1="12" y1="84" x2="206" y2="84" stroke="#2166ac" stroke-width="2.2" marker-end="url(#ar-b)"/>
    <text x="10" y="76" font-size="10">rear-inflow jet</text>
    <text x="150" y="13" font-size="10" text-anchor="middle">bow echo (line of storms seen on radar)</text>
    <text x="230" y="80" font-size="10">strongest</text>
    <text x="230" y="92" font-size="10">winds</text>
    <line x1="200" y1="156" x2="262" y2="156" stroke="#000" stroke-width="1.2" marker-end="url(#ar-k)"/>
    <text x="194" y="160" font-size="10" text-anchor="end">storm motion</text>
    <line x1="288" y1="40" x2="288" y2="18" stroke="#000" stroke-width="1" marker-end="url(#ar-k)"/>
    <text x="288" y="52" font-size="10" text-anchor="middle">N</text>
  </svg>
  <figcaption id="fig-35-cap"><span class="jn-figno">Fig. 35.</span> Schematic map view of a bow echo in a derecho, moving east (to the right). Gray shading is the area of rain seen by radar; the heavy black edge is the line of intense storms at its leading edge. The blue arrow is the rear-inflow jet, which enters from behind the line, descends, and reaches the ground near the apex of the bow, where the strongest straight-line winds occur.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-36">
  <a href="/images/wx_systems_v3/derecho_2012.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/derecho_2012.png" alt="ERA5 maps for the derecho case, 1800 UTC 29 June 2012, with cooling from 2000 to 2300 UTC" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 36.</span> The derecho’s bow-shaped line of storms is too small for ERA5, which instead shows very unstable air (dark red in b) along the northern edge of the heat ridge (a) and the swath of sudden cooling the storms left behind (blue in c) (ERA5, 29 Jun 2012). (a) 850-hPa temperature (°C) and 500-hPa height (contours every 3 dam), 1800 UTC (2 p.m. EDT). (b) CAPE, the energy available to rising air (J kg⁻¹), and 10-m to 500-hPa wind difference (barbs, kt), 1800 UTC. (c) 2-m temperature change, 2000–2300 UTC (K), and the 2 mm h⁻¹ rain contour.</figcaption>
</figure>
<p>Forecasters look for a bowing line on radar and large instability (energy available to rising air). <a href="#ref-johns1987">Johns and Hirt (1987)</a> revived the term; <a href="#ref-corfidi2016">Corfidi et al. (2016)</a> and <a href="#ref-squitieri2025">Squitieri et al. (2025)</a> revised its definition. The Storm Prediction Center also requires gusts of at least 58 mph along the swath, several of them 75 mph or more (<a href="https://www.spc.noaa.gov/misc/AbtDerechos/derechofacts.htm">SPC</a>). On 29 June 2012 a derecho crossed about 700 mi (1100 km) in 12 h, from northern Indiana at about 1800 UTC (2 p.m. EDT) to the Delaware and New Jersey coast, with gusts to 91 mph at Fort Wayne, Ind. (<a href="https://www.spc.noaa.gov/misc/AbtDerechos/casepages/jun292012page.htm">SPC case page</a>). Because the storms were far smaller than ERA5’s grid, its strongest gust that afternoon (Fig. 36) is only 34 kt (39 mph).</p>
</section>

<section class="wx-sys" id="dryline">
<h3>5.3 Dryline</h3>
<p class="wx-def">A dryline is a boundary, usually over the southern and central Great Plains in spring, between humid air from the Gulf of Mexico and very dry air from the desert Southwest; thunderstorms often form along it.</p>
<p>Humid Gulf air spreads north in a shallow layer; to the west, where the land rises, the air is hot and dry. By day, mixing brings dry air down through the thin western edge of the humid layer, so the dryline moves east; at night it drifts back west (<a href="#ref-schaefer1974">Schaefer 1974</a>). The Northeast has no dryline. It is included for contrast with the sea-breeze and backdoor fronts (<a href="#sea-breeze">Sections 1.1</a> and <a href="#backdoor-front">1.2</a>): those separate cool air from warm air, while the dryline separates mainly moist air from dry air.</p>
<p><i>At the surface.</i> Crossing the line westward, the dewpoint can fall 20 °F (11 °C) or more. Rising air along the dryline starts many of the Plains’ spring severe storms and tornadoes.</p>
<figure class="jn-fig wx-schem" id="fig-37">
  <svg viewBox="0 0 300 168" role="img" aria-labelledby="fig-37-cap">
    <rect width="300" height="168" fill="#fff"/>
    <rect x="0" y="18" width="150" height="150" fill="#fcbba1" opacity="0.5"/>
    <rect x="150" y="18" width="150" height="150" fill="#c7e9c0"/>
    <path d="M150 18 C 140 55, 160 95, 148 168" fill="none" stroke="#000" stroke-width="1.6" stroke-dasharray="5 3"/>
    <text x="150" y="13" font-size="10" text-anchor="middle">dryline</text>
    <text x="8" y="13" font-size="10">west ←</text>
    <text x="292" y="13" font-size="10" text-anchor="end">→ east</text>
    <ellipse cx="150" cy="52" rx="14" ry="8" fill="#fff" stroke="#000" stroke-width="0.8"/>
    <ellipse cx="154" cy="98" rx="14" ry="8" fill="#fff" stroke="#000" stroke-width="0.8"/>
    <text x="172" y="78" font-size="10">storms form along it</text>
    <text x="10" y="70" font-size="10">hot, dry air</text>
    <text x="10" y="82" font-size="10">from the desert</text>
    <text x="10" y="94" font-size="10">(low dewpoint)</text>
    <text x="172" y="126" font-size="10">warm, humid air</text>
    <text x="172" y="138" font-size="10">from the Gulf of Mexico</text>
    <text x="172" y="150" font-size="10">(high dewpoint)</text>
    <line x1="90" y1="150" x2="132" y2="150" stroke="#000" stroke-width="1.2" marker-end="url(#ar-k)"/>
    <text x="86" y="153" font-size="10" text-anchor="end">by day</text>
    <line x1="214" y1="36" x2="172" y2="36" stroke="#000" stroke-width="1.2" marker-end="url(#ar-k)"/>
    <text x="218" y="39" font-size="10">at night</text>
  </svg>
  <figcaption id="fig-37-cap"><span class="jn-figno">Fig. 37.</span> Schematic map view of a dryline over the southern Plains. Shading shows dry desert air to the west (pale red) and humid Gulf air to the east (green); the dashed line is the dryline, where thunderstorms (white ovals) tend to form. Arrows show the typical daily movement: east during the day as mixing erodes the shallow humid layer from the west, back west at night.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-38">
  <a href="/images/wx_systems_v3/dryline_2013.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/dryline_2013.png" alt="ERA5 maps for the dryline case, 2100 UTC 20 May 2013" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 38.</span> Dryline over the southern Plains, 2100 UTC (4 p.m. CDT) 20 May 2013 (ERA5). (a) 2-m dewpoint (°C) and 10-m wind (barbs, kt). (b) 10-m divergence (10⁻⁵ s⁻¹; blue: converging air) and 2-m moisture (contours at 6, 10 and 14 g kg⁻¹). (c) CAPE (J kg⁻¹) and the energy barrier rising air must first overcome (dashed contours). The dryline is the sharp edge between dry (pale) and humid (dark blue) air in (a), across which the dewpoint jumps about 20 °C. The humid air east of it is very unstable (c), and the Moore storm formed there.</figcaption>
</figure>
<p>On surface maps the dryline lies along the tightest dewpoint gradient, where winds converge. In 30 years of observations, <a href="#ref-hoch2005">Hoch and Markowski (2005)</a> found a dryline on 32% of April–June days, most often in mid- to late May, usually near 101°W (through the Texas Panhandle and western Kansas). On 20 May 2013 storms formed along the Oklahoma dryline; one produced the Moore tornado at about 1956 UTC (2:56 p.m. CDT), an hour after the discussion below. ERA5 at 2100 UTC (Fig. 38) spreads the dryline’s 20 °C (36 °F) dewpoint jump over several grid boxes.</p>
<blockquote class="wx-afd"><p>“Rapid thunderstorm development is expected over the next hour or two along the dryline and stationary boundary.”</p>
<footer>NWS Norman, Okla. (OUN) Area Forecast Discussion, issued 1:52 p.m. CDT 20 May 2013 (1852 UTC) (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201305201852-KOUN-FXUS64-AFDOUN">archived text</a>)</footer></blockquote>
</section>

<h2 id="sec-6">6. Large-scale patterns</h2>
<p>The last two systems are set by the large-scale flow. An omega block spans several thousand kilometers and can hold the Northeast’s weather in place for a week. The Santa Ana wind of Southern California, driven by high pressure over the Great Basin, is included as the dry, offshore opposite of the Northeast’s sea breeze and marine layer.</p>

<section class="wx-sys" id="omega-block">
<h3>6.1 Omega block</h3>
<p class="wx-def">An omega block is a large, nearly stationary pattern in the winds about 5–6 km up: a high-pressure ridge between two lows, shaped like the Greek letter Ω, that holds the weather in place for days.</p>
<p>The jet stream normally carries weather systems west to east every few days. Sometimes its meanders grow until a ridge pushes far north and lows are cut off on either side. The jet then splits and flows around the block, and the systems that would normally push the pattern east are steered around it instead, so the block can persist for a week or more. <a href="#ref-rex1950">Rex (1950)</a> first described blocking systematically.</p>
<p>Under the ridge, sinking air warms and dries, so clouds dissolve and days are clear, warm and dry (in summer, heat waves and stagnant air). Under the lows, cool, showery days follow one another. Week-ahead forecasts hinge on when a block forms and when it breaks down.</p>
<figure class="jn-fig wx-schem" id="fig-39">
  <svg viewBox="0 0 300 200" role="img" aria-labelledby="fig-39-cap">
    <rect width="300" height="200" fill="#fff"/>
    <path d="M0 92 C 22 92, 26 150, 60 150 C 96 150, 84 40, 150 34 C 216 40, 204 150, 240 150 C 274 150, 278 92, 300 92" fill="none" stroke="#000" stroke-width="1.6"/>
    <ellipse cx="150" cy="78" rx="34" ry="24" fill="#fcbba1" stroke="#000" stroke-width="1"/>
    <ellipse cx="58" cy="124" rx="14" ry="12" fill="#c6dbef" stroke="#000" stroke-width="1"/>
    <ellipse cx="242" cy="124" rx="14" ry="12" fill="#c6dbef" stroke="#000" stroke-width="1"/>
    <text x="150" y="83" font-size="14" text-anchor="middle">H</text>
    <text x="58" y="129" font-size="13" text-anchor="middle">L</text>
    <text x="242" y="129" font-size="13" text-anchor="middle">L</text>
    <line x1="136" y1="35" x2="166" y2="35" stroke="#000" stroke-width="1.2" marker-end="url(#ar-k)"/>
    <line x1="4" y1="80" x2="28" y2="80" stroke="#000" stroke-width="1.2" marker-end="url(#ar-k)"/>
    <line x1="272" y1="80" x2="296" y2="80" stroke="#000" stroke-width="1.2" marker-end="url(#ar-k)"/>
    <text x="150" y="122" font-size="10" text-anchor="middle">blocking high:</text>
    <text x="150" y="134" font-size="10" text-anchor="middle">warm, dry, settled</text>
    <text x="58" y="168" font-size="10" text-anchor="middle">cut-off low:</text>
    <text x="58" y="180" font-size="10" text-anchor="middle">cool, wet</text>
    <text x="242" y="168" font-size="10" text-anchor="middle">cut-off low:</text>
    <text x="242" y="180" font-size="10" text-anchor="middle">cool, wet</text>
    <text x="6" y="14" font-size="10">500-hPa height contours (about 5.5 km up)</text>
    <text x="150" y="196" font-size="10" text-anchor="middle">west ← → east</text>
    <line x1="288" y1="44" x2="288" y2="22" stroke="#000" stroke-width="1" marker-end="url(#ar-k)"/>
    <text x="288" y="56" font-size="10" text-anchor="middle">N</text>
  </svg>
  <figcaption id="fig-39-cap"><span class="jn-figno">Fig. 39.</span> Schematic map of an omega block. Lines are contours of the height of the 500-hPa pressure surface (about 5.5 km above sea level); the winds blow along them from west to east (arrows), with lower heights to the left of the flow. The main contour forms the Ω shape around a closed high (H, red) flanked by two cut-off lows (L, blue). Weather beneath each feature stays nearly the same while the block persists.</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-40">
  <a href="/images/wx_systems_v3/omegablock_2016.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/omegablock_2016.png" alt="ERA5 maps for the omega block case, 1200 UTC 15, 16 and 17 April 2016" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 40.</span> Omega block, 15–17 Apr 2016 (ERA5). 500-hPa height, about 5.5 km up (contours every 6 dam), and its departure from the 1991–2020 mid-April average (shading, dam) at 1200 UTC on (a) 15, (b) 16 and (c) 17 Apr. A high over the Great Lakes (H) with a closed low on each side bends the contours into the Greek letter Ω (thick 570-dam line), and the pattern barely moves over the three days. Over the high, heights are up to about 30 dam above average.</figcaption>
</figure>
<p><i>How forecasters identify it.</i> On 500-hPa maps a block appears as a high that has stopped moving, flanked by closed lows. Normally the height of the 500-hPa surface decreases toward the pole. The index of <a href="#ref-tibaldi1990">Tibaldi and Molteni (1990)</a> flags a block where, near 60°N, the height increases toward the pole instead; they used it to test how well a forecast model predicted blocks.</p>
<p>In April 2016 a closed high sat over the Great Lakes from 15 to 18 April, flanked from 16 April by cut-off lows over the southern Rockies and the western Atlantic (Fig. 40). The block had broken down by 19&ndash;20 April.</p>
<blockquote class="wx-afd"><p>“Quiet weather continues as an omega blocking pattern aloft remains in place, with the ridge across the eastern half of the country, and high pressure at the surface remaining in control as well.”</p>
<footer>NWS Philadelphia/Mount Holly (PHI) Area Forecast Discussion, issued 12:26 a.m. EDT 18 Apr 2016 (0426 UTC) (<a href="https://mesonet.agron.iastate.edu/p.php?pid=201604180426-KPHI-FXUS61-AFDPHI">archived text</a>)</footer></blockquote>
</section>

<section class="wx-sys" id="santa-ana">
<h3>6.2 Santa Ana wind</h3>
<p class="wx-def">The Santa Ana is a hot, very dry, gusty wind that blows from the interior deserts through mountain passes and canyons to the Southern California coast, mostly from autumn to early spring.</p>
<p>High pressure over the Great Basin and cold, dense desert air make pressure higher inland than at the coast. <a href="#ref-hughes2010">Hughes and Hall (2010)</a> found that “unless synoptic [large-scale] conditions force strongly onshore winds, the local thermodynamic forcing [the desert–ocean temperature contrast] is the primary control on Santa Ana variability.” As the air descends the mountains to the coast it is compressed and warms about 10 °C per km, and its relative humidity drops, often below 10%, although no water is removed.</p>
<p><i>Effects.</i> Northeast winds gust to 25–50 mph in passes and canyons, and the coast turns hot with very low humidity. Coming after the dry summer, these winds bring Southern California’s worst fire weather.</p>
<figure class="jn-fig wx-schem" id="fig-41">
  <div class="wx-two">
  <svg viewBox="0 0 300 168" role="img" aria-labelledby="fig-41-cap">
    <rect width="300" height="168" fill="#fff"/>
    <rect x="0" y="142" width="48" height="26" fill="#c6dbef"/>
    <polygon points="48,142 95,122 130,62 168,100 300,100 300,168 48,168" fill="#d9d9d9"/>
    <polyline points="0,142 48,142 95,122 130,62 168,100 300,100" fill="none" stroke="#000" stroke-width="1"/>
    <path d="M292 72 C 240 66, 180 56, 140 52" fill="none" stroke="#2166ac" stroke-width="2" marker-end="url(#ar-b)"/>
    <path d="M128 56 C 112 72, 90 104, 54 132" fill="none" stroke="#b2182b" stroke-width="2.2" marker-end="url(#ar-r)"/>
    <text x="296" y="16" font-size="10" text-anchor="end">high pressure over the Great Basin</text>
    <text x="296" y="92" font-size="10" text-anchor="end">cool, dry desert air</text>
    <text x="4" y="70" font-size="10">air sinks and warms</text>
    <text x="4" y="82" font-size="10">by compression</text>
    <text x="150" y="124" font-size="10" text-anchor="middle">coastal mountains</text>
    <text x="4" y="159" font-size="10">Pacific</text>
    <text x="54" y="159" font-size="10">hot, dry, gusty winds at the coast</text>
    <text x="4" y="14" font-size="10">west ← → east</text>
  </svg>
  <img src="/images/wx_systems_v2/schematics/santaana_westernwinds.jpg" alt="Hand-drawn map of the western United States with arrows marking the East, North, Mono, Santa Ana and Chinook winds." loading="lazy">
  </div>
  <figcaption id="fig-41-cap"><span class="jn-figno">Fig. 41.</span> (a) Schematic drawn for this page: a west–east cross-section through Southern California. Cool, dry air from the desert interior (blue arrow) flows toward the coast, crosses the coastal mountains, and descends their western slopes (red arrow), warming by compression; it reaches the coast hot, dry and gusty. (b) The main downslope winds of the western United States, including the Santa Ana. From Schroeder and Buck, <i>Fire Weather</i>, USDA Agriculture Handbook 360 (1970), republished by the National Wildfire Coordinating Group as PMS 425-1. Courtesy USDA Forest Service (public domain).</figcaption>
</figure>
<figure class="jn-fig wx-map" id="fig-42">
  <a href="/images/wx_systems_v3/santaana_2007.png" title="Open the full-size figure"><img src="/images/wx_systems_v3/santaana_2007.png" alt="ERA5 maps for the Santa Ana wind case, 0900 UTC 22 October 2007" loading="lazy"></a>
  <figcaption><span class="jn-figno">Fig. 42.</span> High pressure over the Great Basin (H) drives desert air to the coast, where it arrives very dry (yellow in c), warmed by sinking down the mountains rather than by warm air blown in (ERA5, 0900 UTC [2 a.m. PDT] 22 Oct 2007). (a) Sea-level pressure (contours every 2 hPa), 2-m temperature (°C) and 10-m wind (barbs, kt). (b) Warming or cooling by the 850-hPa wind (K h⁻¹; blank: 850 hPa below ground) and 850-hPa temperature (contours every 2 °C). (c) 2-m relative humidity (%). Pressure is 13 hPa higher at Tonopah, Nev., than at Los Angeles.</figcaption>
</figure>
<p><i>How forecasters identify it.</i> The standard measure is the pressure difference between Los Angeles airport (LAX) and Daggett (DAG), in the Mojave Desert; a negative value means higher pressure inland. The Santa Ana Wildfire Threat Index (<a href="#ref-rolinski2016">Rolinski et al. 2016</a>) combines wind, humidity and vegetation dryness. At 850 hPa (1.5 km) forecasters look for northeast winds carrying cold air over the interior (cold-air advection), the same air that reaches the coast hot after its descent. ERA5 at 0900 UTC 22 October 2007 (2 a.m. PDT; Fig. 42) shows the Great Basin high and this cold-air advection. During the fires that week, LAX reached 84–94 °F (29–34 °C) on 22–24 October, 10–20 °F (6–11 °C) above normal.</p>
<blockquote class="wx-afd"><p>“The big story continues to be the current Santa Ana wind event. The strong offshore flow continues with an incredibly strong LAX-DAG pressure gradient dipping below -10 mb earlier today.”</p>
<footer>NWS Los Angeles/Oxnard, Calif. (LOX) Area Forecast Discussion, issued 3:15 p.m. PDT 22 Oct 2007 (<a href="https://mesonet.agron.iastate.edu/p.php?pid=200710222224-KLOX-FXUS66-AFDLOX">archived text</a>)</footer></blockquote>
</section>


<h2 id="methods">Data and methods</h2>
<p>The case maps use the ERA5 reanalysis produced by the European Centre for Medium-Range Weather Forecasts (ECMWF) for the Copernicus Climate Change Service (<a href="#ref-hersbach2020">Hersbach et al. 2020</a>). Hourly fields on the 0.25&deg; grid were read from Google's Analysis-Ready, Cloud-Optimized copy of ERA5 (<a href="https://github.com/google-research/arco-era5">ARCO-ERA5</a>) and plotted with Python (xarray and Matplotlib). Each map shows the fields named in its caption at the stated time.</p>
<p>Forecaster quotations come from National Weather Service Area Forecast Discussions held in the <a href="https://mesonet.agron.iastate.edu/wx/afos/">Iowa Environmental Mesonet text archive</a>. Each quotation links to the exact product it is taken from. Examples given without a link are paraphrased.</p>
<p>The schematics were drawn for this page. Where a published public-domain drawing adds information, it is reproduced beside the schematic and credited in the caption.</p>
<p>Statements about how forecasters recognize each system summarize the cited papers, drawn from a reading of 53 peer-reviewed papers on these systems and on model temperature forecasts, supplemented by the AMS Glossary of Meteorology. Identification methods given without a citation reflect standard National Weather Service forecasting practice. The counts of midnight highs in Section 3.3 were made for this page from hourly airport observations.</p>

<h2 id="acknowledgments">Acknowledgments</h2>
<p>Generated using Copernicus Climate Change Service information (2026); neither the European Commission nor ECMWF is responsible for any use of this information. The ARCO-ERA5 copy is hosted by Google Cloud Public Datasets, and the text archive is maintained by the Iowa Environmental Mesonet at Iowa State University. Reproduced schematics are credited to their sources in the figure captions.</p>

<h2 id="references">References</h2>
<ol class="wx-refs">
<li id="ref-adler2023">Adler, B., J. M. Wilczak, J. Kenyon, L. Bianco, I. V. Djalalova, J. B. Olson, and D. D. Turner, 2023: Evaluation of a cloudy cold-air pool in the Columbia River basin in different versions of the High-Resolution Rapid Refresh (HRRR) model. <i>Geosci. Model Dev.</i>, <b>16</b>, 597–619, <a href="https://doi.org/10.5194/gmd-16-597-2023">https://doi.org/10.5194/gmd-16-597-2023</a>.</li>
<li id="ref-ams2026">AMS, 2026: <i>Glossary of Meteorology</i>. Amer. Meteor. Soc., entries &ldquo;Backdoor cold front,&rdquo; &ldquo;Coastal front&rdquo; and &ldquo;Sea fog,&rdquo; accessed 8 October 2026, <a href="https://glossary.ametsoc.org/wiki/Welcome">https://glossary.ametsoc.org/wiki/Welcome</a>.</li>
<li id="ref-atkins1995">Atkins, N. T., R. M. Wakimoto, and T. M. Weckwerth, 1995: Observations of the sea-breeze front during CaPE. Part II: Dual-Doppler and aircraft analysis. <i>Mon. Wea. Rev.</i>, <b>123</b>, 944&ndash;969, <a href="https://doi.org/10.1175/1520-0493(1995)123&lt;0944:OOTSBF&gt;2.0.CO;2">https://doi.org/10.1175/1520-0493(1995)123&lt;0944:OOTSBF&gt;2.0.CO;2</a>.</li>
<li id="ref-bell1988">Bell, G. D., and L. F. Bosart, 1988: Appalachian cold-air damming. <i>Mon. Wea. Rev.</i>, <b>116</b>, 137–161, <a href="https://doi.org/10.1175/1520-0493(1988)116&lt;0137:ACAD&gt;2.0.CO;2">https://doi.org/10.1175/1520-0493(1988)116&lt;0137:ACAD&gt;2.0.CO;2</a>.</li>
<li id="ref-birk2021">Birk, K., E. Lenning, K. Donofrio, and M. T. Friedlein, 2021: A revised Bourgouin precipitation-type algorithm. <i>Wea. Forecasting</i>, <b>36</b>, 425–438, <a href="https://doi.org/10.1175/WAF-D-20-0118.1">https://doi.org/10.1175/WAF-D-20-0118.1</a>.</li>
<li id="ref-blackadar1957">Blackadar, A. K., 1957: Boundary layer wind maxima and their significance for the growth of nocturnal inversions. <i>Bull. Amer. Meteor. Soc.</i>, <b>38</b>, 283–290, <a href="https://doi.org/10.1175/1520-0477-38.5.283">https://doi.org/10.1175/1520-0477-38.5.283</a>.</li>
<li id="ref-bosart1975">Bosart, L. F., 1975: New England coastal frontogenesis. <i>Quart. J. Roy. Meteor. Soc.</i>, <b>101</b>, 957&ndash;978, <a href="https://doi.org/10.1002/qj.49710143016">https://doi.org/10.1002/qj.49710143016</a>.</li>
<li id="ref-bourgouin2000">Bourgouin, P., 2000: A method to determine precipitation types. <i>Wea. Forecasting</i>, <b>15</b>, 583–592, <a href="https://doi.org/10.1175/1520-0434(2000)015&lt;0583:AMTDPT&gt;2.0.CO;2">https://doi.org/10.1175/1520-0434(2000)015&lt;0583:AMTDPT&gt;2.0.CO;2</a>.</li>
<li id="ref-charba1974">Charba, J., 1974: Application of gravity current model to analysis of squall-line gust front. <i>Mon. Wea. Rev.</i>, <b>102</b>, 140–156, <a href="https://doi.org/10.1175/1520-0493(1974)102&lt;0140:AOGCMT&gt;2.0.CO;2">https://doi.org/10.1175/1520-0493(1974)102&lt;0140:AOGCMT&gt;2.0.CO;2</a>.</li>
<li id="ref-coniglio2013">Coniglio, M. C., J. Correia Jr., P. T. Marsh, and F. Kong, 2013: Verification of convection-allowing WRF model forecasts of the planetary boundary layer using sounding observations. <i>Wea. Forecasting</i>, <b>28</b>, 842–862, <a href="https://doi.org/10.1175/WAF-D-12-00103.1">https://doi.org/10.1175/WAF-D-12-00103.1</a>.</li>
<li id="ref-corfidi2016">Corfidi, S. F., M. C. Coniglio, A. E. Cohen, and C. M. Mead, 2016: A proposed revision to the definition of “derecho.” <i>Bull. Amer. Meteor. Soc.</i>, <b>97</b>, 935–949, <a href="https://doi.org/10.1175/BAMS-D-14-00254.1">https://doi.org/10.1175/BAMS-D-14-00254.1</a>.</li>
<li id="ref-ellis2018">Ellis, A. W., M. L. Marston, and D. A. Nelson, 2018: An air mass-derived cool season climatology of synoptically forced Appalachian cold-air damming. <i>Int. J. Climatol.</i>, <b>38</b>, 530–542, <a href="https://doi.org/10.1002/joc.5189">https://doi.org/10.1002/joc.5189</a>.</li>
<li id="ref-hersbach2020">Hersbach, H., and Coauthors, 2020: The ERA5 global reanalysis. <i>Quart. J. Roy. Meteor. Soc.</i>, <b>146</b>, 1999&ndash;2049, <a href="https://doi.org/10.1002/qj.3803">https://doi.org/10.1002/qj.3803</a>.</li>
<li id="ref-hoch2005">Hoch, J., and P. Markowski, 2005: A climatology of springtime dryline position in the U.S. Great Plains region. <i>J. Climate</i>, <b>18</b>, 2132–2137, <a href="https://doi.org/10.1175/JCLI3392.1">https://doi.org/10.1175/JCLI3392.1</a>.</li>
<li id="ref-hughes2010">Hughes, M., and A. Hall, 2010: Local and synoptic mechanisms causing Southern California’s Santa Ana winds. <i>Climate Dyn.</i>, <b>34</b>, 847–857, <a href="https://doi.org/10.1007/s00382-009-0650-4">https://doi.org/10.1007/s00382-009-0650-4</a>.</li>
<li id="ref-johns1987">Johns, R. H., and W. D. Hirt, 1987: Derechos: Widespread convectively induced windstorms. <i>Wea. Forecasting</i>, <b>2</b>, 32–49, <a href="https://doi.org/10.1175/1520-0434(1987)002&lt;0032:DWCIW&gt;2.0.CO;2">https://doi.org/10.1175/1520-0434(1987)002&lt;0032:DWCIW&gt;2.0.CO;2</a>.</li>
<li id="ref-keshishian1987">Keshishian, L. G., and L. F. Bosart, 1987: A case study of extended East Coast frontogenesis. <i>Mon. Wea. Rev.</i>, <b>115</b>, 100&ndash;117, <a href="https://doi.org/10.1175/1520-0493(1987)115&lt;0100:ACSOEE&gt;2.0.CO;2">https://doi.org/10.1175/1520-0493(1987)115&lt;0100:ACSOEE&gt;2.0.CO;2</a>.</li>
<li id="ref-kocin2004">Kocin, P. J., and L. W. Uccellini, 2004: <i>Northeast Snowstorms</i>. Meteor. Monogr., No. 54, Amer. Meteor. Soc., <a href="https://doi.org/10.1007/978-1-878220-32-5">https://doi.org/10.1007/978-1-878220-32-5</a>.</li>
<li id="ref-koracin2014">Kora&#269;in, D., C. E. Dorman, J. M. Lewis, J. G. Hudson, E. M. Wilcox, and A. Torregrosa, 2014: Marine fog: A review. <i>Atmos. Res.</i>, <b>143</b>, 142&ndash;175, <a href="https://doi.org/10.1016/j.atmosres.2013.12.012">https://doi.org/10.1016/j.atmosres.2013.12.012</a>.</li>
<li id="ref-miller1946">Miller, J. E., 1946: Cyclogenesis in the Atlantic coastal region of the United States. <i>J. Meteor.</i>, <b>3</b>, 31&ndash;44, <a href="https://doi.org/10.1175/1520-0469(1946)003&lt;0031:CITACR&gt;2.0.CO;2">https://doi.org/10.1175/1520-0469(1946)003&lt;0031:CITACR&gt;2.0.CO;2</a>.</li>
<li id="ref-miller2003">Miller, S. T. K., B. D. Keim, R. W. Talbot, and H. Mao, 2003: Sea breeze: Structure, forecasting, and impacts. <i>Rev. Geophys.</i>, <b>41</b>, 1011, <a href="https://doi.org/10.1029/2003RG000124">https://doi.org/10.1029/2003RG000124</a>.</li>
<li id="ref-nielsen1989">Nielsen, J. W., 1989: The formation of New England coastal fronts. <i>Mon. Wea. Rev.</i>, <b>117</b>, 1380&ndash;1401, <a href="https://doi.org/10.1175/1520-0493(1989)117&lt;1380:TFONEC&gt;2.0.CO;2">https://doi.org/10.1175/1520-0493(1989)117&lt;1380:TFONEC&gt;2.0.CO;2</a>.</li>
<li id="ref-niziol1987">Niziol, T. A., 1987: Operational forecasting of lake effect snowfall in western and central New York. <i>Wea. Forecasting</i>, <b>2</b>, 310–321, <a href="https://doi.org/10.1175/1520-0434(1987)002&lt;0310:OFOLES&gt;2.0.CO;2">https://doi.org/10.1175/1520-0434(1987)002&lt;0310:OFOLES&gt;2.0.CO;2</a>.</li>
<li id="ref-niziol1995">Niziol, T. A., W. R. Snyder, and J. S. Waldstreicher, 1995: Winter weather forecasting throughout the eastern United States. Part IV: Lake effect snow. <i>Wea. Forecasting</i>, <b>10</b>, 61–77, <a href="https://doi.org/10.1175/1520-0434(1995)010&lt;0061:WWFTTE&gt;2.0.CO;2">https://doi.org/10.1175/1520-0434(1995)010&lt;0061:WWFTTE&gt;2.0.CO;2</a>.</li>
<li id="ref-nwsctp">NWS State College, n.d.: Snow storm types. National Weather Service, State College, Pa., accessed 8 October 2026, <a href="https://www.weather.gov/ctp/SnowStormTypes">https://www.weather.gov/ctp/SnowStormTypes</a>.</li>
<li id="ref-patel2021">Patel, R. N., S. E. Yuter, M. A. Miller, S. R. Rhodes, L. Bain, and T. W. Peele, 2021: The diurnal cycle of winter season temperature errors in the operational Global Forecast System (GFS). <i>Geophys. Res. Lett.</i>, <b>48</b>, e2021GL095101, <a href="https://doi.org/10.1029/2021GL095101">https://doi.org/10.1029/2021GL095101</a>.</li>
<li id="ref-rex1950">Rex, D. F., 1950: Blocking action in the middle troposphere and its effect upon regional climate. <i>Tellus</i>, <b>2</b>, 196–211, <a href="https://doi.org/10.1111/j.2153-3490.1950.tb00331.x">https://doi.org/10.1111/j.2153-3490.1950.tb00331.x</a>.</li>
<li id="ref-riordan2003">Riordan, A. J., G. M. Lackmann, and L. Xie, 2003: Improving forecasts of topographically-forced weather systems in the Carolinas and Virginia. Final Scientific Progress Report, NOAA CSTAR Award NA07WA0206, North Carolina State University, 17 pp. Project report; not peer reviewed. <a href="https://www.weather.gov/media/rah/science/NCSU_CSTAR_I_Final_Report.pdf">https://www.weather.gov/media/rah/science/NCSU_CSTAR_I_Final_Report.pdf</a>.</li>
<li id="ref-rolinski2016">Rolinski, T., S. B. Capps, R. G. Fovell, Y. Cao, B. J. D’Agostino, and S. Vanderburg, 2016: The Santa Ana wildfire threat index: Methodology and operational implementation. <i>Wea. Forecasting</i>, <b>31</b>, 1881–1897, <a href="https://doi.org/10.1175/WAF-D-15-0141.1">https://doi.org/10.1175/WAF-D-15-0141.1</a>.</li>
<li id="ref-sanders1980">Sanders, F., and J. R. Gyakum, 1980: Synoptic-dynamic climatology of the “bomb.” <i>Mon. Wea. Rev.</i>, <b>108</b>, 1589–1606, <a href="https://doi.org/10.1175/1520-0493(1980)108&lt;1589:SDCOT&gt;2.0.CO;2">https://doi.org/10.1175/1520-0493(1980)108&lt;1589:SDCOT&gt;2.0.CO;2</a>.</li>
<li id="ref-schaefer1974">Schaefer, J. T., 1974: The life cycle of the dryline. <i>J. Appl. Meteor.</i>, <b>13</b>, 444–449, <a href="https://doi.org/10.1175/1520-0450(1974)013&lt;0444:TLCOTD&gt;2.0.CO;2">https://doi.org/10.1175/1520-0450(1974)013&lt;0444:TLCOTD&gt;2.0.CO;2</a>.</li>
<li id="ref-schroeder1970">Schroeder, M. J., and C. C. Buck, 1970: <i>Fire Weather: A Guide for Application of Meteorological Information to Forest Fire Control Operations</i>. Agriculture Handbook 360, U.S. Department of Agriculture, Forest Service. Reprinted as NWCG PMS 425-1, <a href="https://www.nwcg.gov/publications/pms425-1">https://www.nwcg.gov/publications/pms425-1</a>.</li>
<li id="ref-squitieri2025">Squitieri, B. J., A. R. Wade, and I. L. Jirak, 2025: On a modified definition of a derecho. Part I: Construction of the definition and quantitative criteria for identifying future derechos over the contiguous United States. <i>Bull. Amer. Meteor. Soc.</i>, <b>106</b>, E84–E110, <a href="https://doi.org/10.1175/BAMS-D-24-0015.1">https://doi.org/10.1175/BAMS-D-24-0015.1</a>.</li>
<li id="ref-stull1988">Stull, R. B., 1988: <i>An Introduction to Boundary Layer Meteorology</i>. Kluwer Academic, <a href="https://doi.org/10.1007/978-94-009-3027-8">https://doi.org/10.1007/978-94-009-3027-8</a>.</li>
<li id="ref-thomas2007">Thomas, B. C., and J. E. Martin, 2007: A synoptic climatology and composite analysis of the Alberta clipper. <i>Wea. Forecasting</i>, <b>22</b>, 315–333, <a href="https://doi.org/10.1175/WAF982.1">https://doi.org/10.1175/WAF982.1</a>.</li>
<li id="ref-tibaldi1990">Tibaldi, S., and F. Molteni, 1990: On the operational predictability of blocking. <i>Tellus</i>, <b>42A</b>, 343–365, <a href="https://doi.org/10.3402/tellusa.v42i3.11882">https://doi.org/10.3402/tellusa.v42i3.11882</a>.</li>
<li id="ref-vandewiel2010">Van de Wiel, B. J. H., A. F. Moene, G. J. Steeneveld, P. Baas, F. C. Bosveld, and A. A. M. Holtslag, 2010: A conceptual view on inertial oscillations and nocturnal low-level jets. <i>J. Atmos. Sci.</i>, <b>67</b>, 2679–2689, <a href="https://doi.org/10.1175/2010JAS3289.1">https://doi.org/10.1175/2010JAS3289.1</a>.</li>
<li id="ref-wakimoto1982">Wakimoto, R. M., 1982: The life cycle of thunderstorm gust fronts as viewed with Doppler radar and rawinsonde data. <i>Mon. Wea. Rev.</i>, <b>110</b>, 1060–1082, <a href="https://doi.org/10.1175/1520-0493(1982)110&lt;1060:TLCOTG&gt;2.0.CO;2">https://doi.org/10.1175/1520-0493(1982)110&lt;1060:TLCOTG&gt;2.0.CO;2</a>.</li>
</ol>

</div>

