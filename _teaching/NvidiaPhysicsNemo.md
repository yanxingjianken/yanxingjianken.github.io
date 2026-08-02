---
title: "Nvidia PhysicsNemo Notes"
collection: teaching
type: "Machine Learning"
permalink: /teaching/NvidiaPhysicsNemo
venue: "MIT EAPS"
date: 2026-08-02
location: "Cambridge, MA"
---

{% raw %}
<div class="pnx">

<style>
div.pnx{
  --surface:#F1F4F4; --surface-2:#E4E9EA;
  --ink:#16232B; --ink-2:#3E525C; --ink-3:#5C7078;
  --rule:#C7D0D3; --grid:#9FB0B6;
  --teal:#14666C; --ochre:#B0691F; --ochre-ink:#8F5416; --flag:#A83228;
  --mono:"Cascadia Mono","Cascadia Code",Consolas,"SF Mono",ui-monospace,"Liberation Mono",monospace;
  --serif:"Iowan Old Style",Charter,"Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  color:var(--ink); line-height:1.72;
}
div.pnx *{box-sizing:border-box}
div.pnx p{margin:0 0 1.05em; color:var(--ink)}
div.pnx h2{
  font-size:1.55rem; font-weight:650; line-height:1.28; letter-spacing:-.01em;
  margin:2.6em 0 .2em; padding:0; border:none; color:var(--ink);
}
div.pnx h2:first-of-type{margin-top:1.2em}
div.pnx h3{
  font-size:1.12rem; font-weight:650; margin:2em 0 .5em; padding:0;
  border:none; color:var(--ink);
}
div.pnx h4{
  font-size:.98rem; font-weight:650; margin:1.6em 0 .4em; padding:0;
  border:none; color:var(--ink);
}
div.pnx .kicker{
  font-family:var(--mono); font-size:.72rem; letter-spacing:.14em; text-transform:uppercase;
  color:var(--teal); margin:0 0 .1em; display:flex; align-items:center; gap:10px;
}
div.pnx .kicker::after{content:""; flex:1; height:1px; background:var(--rule)}
div.pnx .lede{
  font-family:var(--serif); font-size:1.13rem; line-height:1.62; color:var(--ink-2);
  border-left:2px solid var(--teal); padding-left:1.1em; margin:0 0 1.6em;
}
div.pnx code{
  font-family:var(--mono); font-size:.85em; background:var(--surface-2);
  padding:.1em .34em; border-radius:2px; color:var(--ink); word-break:break-word;
}
div.pnx a{color:var(--teal); text-decoration:underline; text-underline-offset:2px}
div.pnx a code{color:var(--teal)}
div.pnx .eq{
  font-family:var(--mono); font-size:.95rem; color:var(--teal);
  border-left:2px solid var(--teal); padding:.35em 0 .35em 1em; margin:0 0 1.05em;
}
div.pnx ul{margin:0 0 1.05em; padding-left:1.3em}
div.pnx li{margin:0 0 .4em; color:var(--ink)}
div.pnx .hl{color:var(--teal); font-weight:600}
div.pnx .hl-f{color:var(--flag); font-weight:600}

/* plates */
div.pnx .plate{
  background:var(--surface); border:1px solid var(--rule); border-top:2px solid var(--ink);
  padding:20px 20px 0; margin:1.6em 0 1.8em;
}
div.pnx .plate__head{
  display:flex; align-items:baseline; gap:12px; flex-wrap:wrap;
  padding-bottom:15px; margin-bottom:18px; border-bottom:1px solid var(--rule);
}
div.pnx .plate__no{
  font-family:var(--serif); font-size:.92rem; letter-spacing:.14em;
  color:var(--flag); text-transform:uppercase; white-space:nowrap;
}
div.pnx .plate__title{font-weight:650; font-size:.98rem}
div.pnx .plate__sub{font-family:var(--mono); font-size:.72rem; color:var(--ink-3); margin-left:auto}
div.pnx .grid{display:grid; gap:16px 14px}
div.pnx .grid--5{grid-template-columns:repeat(auto-fit,minmax(158px,1fr))}
div.pnx .grid--3{grid-template-columns:repeat(auto-fit,minmax(215px,1fr))}
div.pnx .panel{display:flex; flex-direction:column; gap:7px; min-width:0}
div.pnx .panel svg{display:block; width:100%; height:auto}
div.pnx .panel__name{font-weight:650; font-size:.87rem; line-height:1.38}
div.pnx .panel__name span{
  font-family:var(--mono); font-weight:400; font-size:.73rem; color:var(--ink-3);
  display:block; letter-spacing:.02em;
}
div.pnx .panel__note{font-size:.8rem; line-height:1.55; color:var(--ink-2); margin:0}
div.pnx .panel__note b{color:var(--flag); font-weight:600}
div.pnx .rowlabel{
  grid-column:1/-1; font-family:var(--mono); font-size:.7rem; letter-spacing:.12em;
  text-transform:uppercase; color:var(--ink-3);
  display:flex; align-items:center; gap:10px; margin:4px 0 0;
}
div.pnx .rowlabel::after{content:""; flex:1; height:1px; background:var(--rule)}
div.pnx figcaption{
  font-family:var(--mono); font-size:.755rem; line-height:1.62; color:var(--ink-3);
  border-top:1px solid var(--rule); margin-top:20px; padding:13px 0 18px;
}
div.pnx figcaption b{color:var(--ink-2); font-weight:400}
div.pnx figure{margin:0}

/* svg strokes */
div.pnx .s-limb{fill:none; stroke:var(--ink); stroke-width:1.4}
div.pnx .s-disk{fill:var(--surface-2); stroke:none}
div.pnx .s-grid{fill:none; stroke:var(--grid); stroke-width:.7}
div.pnx .s-grid-f{fill:none; stroke:var(--grid); stroke-width:.55; opacity:.65}
div.pnx .s-teal{fill:none; stroke:var(--teal); stroke-width:1.5}
div.pnx .s-teal-f{fill:var(--teal); stroke:none}
div.pnx .s-ochre{fill:none; stroke:var(--ochre); stroke-width:1.5}
div.pnx .s-ochre-f{fill:var(--ochre); stroke:none}
div.pnx .s-flag{fill:var(--flag); stroke:none}
div.pnx .s-flag-l{fill:none; stroke:var(--flag); stroke-width:1.5}
div.pnx .s-ink{fill:none; stroke:var(--ink); stroke-width:1.1}
div.pnx .s-ink-f{fill:var(--ink); stroke:none}
div.pnx .t-lab{font-family:var(--mono); font-size:9.5px; fill:var(--ink-3)}
div.pnx .t-lab-f{font-family:var(--mono); font-size:9.5px; fill:var(--flag)}
div.pnx .t-lab-t{font-family:var(--mono); font-size:9.5px; fill:var(--teal)}

/* tables */
div.pnx .scroller{overflow-x:auto; border:1px solid var(--rule); background:#fff; margin:1.1em 0 1.6em}
div.pnx table{border-collapse:collapse; width:100%; min-width:760px; font-size:.82rem; margin:0}
div.pnx th, div.pnx td{
  text-align:left; padding:8px 12px; border-bottom:1px solid var(--rule);
  vertical-align:top; font-variant-numeric:tabular-nums; line-height:1.5;
}
div.pnx thead th{
  font-family:var(--mono); font-size:.69rem; letter-spacing:.07em; text-transform:uppercase;
  color:var(--ink-3); font-weight:400; border-bottom:1.5px solid var(--ink);
  white-space:nowrap; background:var(--surface);
}
div.pnx tbody th{font-weight:650; color:var(--ink); white-space:nowrap}
div.pnx tbody th small, div.pnx td small{
  display:block; font-family:var(--mono); font-weight:400; font-size:.71rem; color:var(--ink-3);
}
div.pnx tbody tr:last-child th, div.pnx tbody tr:last-child td{border-bottom:none}
div.pnx td code{background:none; padding:0; color:var(--ink-2)}
div.pnx .y{color:var(--teal); font-weight:650}
div.pnx .n{color:var(--flag); font-weight:650}
div.pnx .p{color:var(--ochre-ink); font-weight:650}

/* verdict list */
div.pnx .verdict{border-top:2px solid var(--ink); margin:1.2em 0 1.6em}
div.pnx .verdict__row{
  display:grid; grid-template-columns:minmax(0,8.5em) 1fr; gap:18px;
  padding:14px 0; border-bottom:1px solid var(--rule);
}
div.pnx .verdict__key{
  font-family:var(--mono); font-size:.72rem; letter-spacing:.08em; text-transform:uppercase;
  color:var(--teal); padding-top:.35em;
}
div.pnx .verdict__row p{margin:0; font-size:.92rem; color:var(--ink-2)}
@media (max-width:620px){
  div.pnx .verdict__row{grid-template-columns:1fr; gap:5px}
  div.pnx .plate{padding:16px 12px 0}
}
</style>

<p class="lede">Notes on <a href="https://github.com/NVIDIA/physicsnemo">NVIDIA PhysicsNeMo</a>, read straight from the <code>main</code> branch as of 2 August 2026. Everything below is grounded in the source and docstrings of <a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather"><code>examples/weather</code></a> and <a href="https://github.com/NVIDIA/torch-harmonics">torch-harmonics</a> rather than in the documentation prose. The organising idea: <em>the sphere refuses a regular grid</em>, and every model in the package is a different way of paying that debt.</p>

<p class="kicker">Section 1</p>
<h2>Geometry: what the sphere costs you</h2>

<p>Before any architecture, one structural fact determines the shape of every design in this package. It is worth stating precisely, because it explains why two apparently unrelated grids &mdash; the cubed sphere and HEALPix &mdash; carry exactly the same number of defects.</p>

<h3>1.1 &nbsp;Discretization</h3>

<p>Tile the sphere with quadrilaterals. Euler's formula gives <code>V &minus; E + F = 2</code>, and every face having four edges gives <code>4F = 2E</code>, hence <code>V = F + 2</code>. Summing the degree deficit over all vertices:</p>

<p class="eq">&Sigma;<sub>v</sub> (4 &minus; deg v) = 4V &minus; 2E = 4(F+2) &minus; 4F = <b>8</b></p>

<p>No quadrilateral mesh on a sphere can have every vertex of degree four. The total deficit is always exactly 8. A <a href="https://www.gfdl.noaa.gov/fv3/">cubed sphere</a> pays it as eight three-valent corners. <a href="https://healpix.sourceforge.io/">HEALPix</a>, whose twelve base pixels form a rhombic-dodecahedron topology (12 faces, 24 edges, 14 vertices &mdash; 8 of degree 3 and 6 of degree 4), pays exactly the same eight. An equirectangular latitude&ndash;longitude grid dumps all eight onto the two poles, buying regular indexing at the price of unbounded anisotropy. The triangular analogue is <code>&Sigma;(6 &minus; deg v) = 12</code>, which is why every icosahedral refinement carries exactly twelve pentagonal vertices, forever.</p>

<p>The five discretizations that appear in PhysicsNeMo, and where each one lives in the code:</p>

<div class="scroller">
<table>
<thead><tr><th>Discretization</th><th>Property that matters</th><th>Where it lives</th><th>Reference</th></tr></thead>
<tbody>
<tr><th>Equirectangular lat&ndash;lon<small>721 x 1440 at 0.25 deg</small></th>
<td>Zonal spacing <code>R&middot;cos&phi;&middot;&Delta;&lambda;</code> collapses at the poles. A fixed 3&times;3 kernel covers about one sixth the physical area at 80&deg;N that it does at the equator.</td>
<td><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/dataset_download"><code>examples/weather/dataset_download</code></a>, <a href="https://github.com/NVIDIA/physicsnemo/tree/main/physicsnemo/datapipes/climate"><code>physicsnemo/datapipes/climate</code></a></td>
<td><a href="https://doi.org/10.1002/qj.3803">ERA5 (Hersbach et al. 2020)</a></td></tr>

<tr><th>Gaussian / reduced Gaussian<small>Legendre-root latitudes</small></th>
<td>Exact quadrature for spherical-harmonic transforms up to a given degree; the reduced variant drops longitudes as <code>cos&phi;</code> for near-uniform spacing.</td>
<td>Grid support in <a href="https://github.com/NVIDIA/torch-harmonics/blob/main/torch_harmonics/quadrature.py"><code>torch_harmonics/quadrature.py</code></a></td>
<td><a href="https://www.ecmwf.int/en/publications/ifs-documentation">ECMWF IFS documentation</a></td></tr>

<tr><th>Cubed sphere<small>6 faces x N x N</small></th>
<td>Regular inside a face, no polar singularity; <b>8 three-valent corners</b>; the coordinate basis rotates across face seams, so vector fields must be re-projected.</td>
<td><a href="https://github.com/NVIDIA/physicsnemo/tree/main/physicsnemo/models/dlwp"><code>physicsnemo/models/dlwp</code></a>, remapping via <a href="https://github.com/ClimateGlobalChange/tempestremap">TempestRemap</a>, curation in <a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/dlwp/data_curation"><code>examples/weather/dlwp/data_curation</code></a></td>
<td><a href="https://doi.org/10.1029/2020MS002109">Weyn et al. 2020</a>, <a href="https://www.gfdl.noaa.gov/wp-content/uploads/2020/02/FV3-Technical-Description.pdf">FV3 technical description</a></td></tr>

<tr><th>HEALPix<small>12 base pixels, nside subdivision</small></th>
<td><b>Exactly equal area</b> by construction, iso-latitude rings, four-fold nested subdivision (each pixel splits into exactly four children, so U-Net pooling aligns for free). Still 8 three-valent vertices.</td>
<td><a href="https://github.com/NVIDIA/physicsnemo/tree/main/physicsnemo/models/dlwp_healpix"><code>physicsnemo/models/dlwp_healpix</code></a>, <a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/models/dlwp_healpix/layers/healpix_blocks.py"><code>layers/healpix_blocks.py</code></a>, datapipe <a href="https://github.com/NVIDIA/physicsnemo/tree/main/physicsnemo/datapipes/healpix"><code>physicsnemo/datapipes/healpix</code></a></td>
<td><a href="https://doi.org/10.1086/427976">G&oacute;rski et al. 2005</a>, <a href="https://doi.org/10.1029/2023MS004021">Karlbauer et al. 2024</a></td></tr>

<tr><th>Icosahedral multi-mesh<small>graph, not grid</small></th>
<td>Quasi-uniform, no poles, but <b>12 five-valent vertices</b> always. Used as a message-passing graph rather than a convolution domain, so cell-area uniformity matters much less.</td>
<td><a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/models/graphcast/utils/icosahedral_mesh.py"><code>models/graphcast/utils/icosahedral_mesh.py</code></a>, <a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/models/graphcast/graph_cast_net.py"><code>graph_cast_net.py</code></a></td>
<td><a href="https://arxiv.org/abs/2212.12794">GraphCast (Lam et al. 2023)</a></td></tr>
</tbody>
</table>
</div>

<figure class="plate">
  <div class="plate__head">
    <span class="plate__no">Plate I</span>
    <span class="plate__title">Five discretizations: on the sphere, and in the tensor</span>
    <span class="plate__sub">orthographic, viewpoint 25N / 30W</span>
  </div>
  <div class="grid grid--5">
    <p class="rowlabel">A &mdash; on the sphere (<span style="color:#A83228">red = topological defect</span>)</p>
    <div class="panel"><svg id="g-latlon" viewBox="0 0 190 190" role="img" aria-label="Equirectangular grid on the sphere"></svg>
      <p class="panel__name">Equirectangular<span>lat-lon</span></p>
      <p class="panel__note">Zonal spacing goes to zero at the pole. At 80&deg;N a 3&times;3 kernel spans <b>one sixth</b> the equatorial footprint.</p></div>
    <div class="panel"><svg id="g-gauss" viewBox="0 0 190 190" role="img" aria-label="Gaussian grid on the sphere"></svg>
      <p class="panel__name">Gaussian / reduced<span>Legendre roots</span></p>
      <p class="panel__note">Rings sit on Legendre roots so quadrature is <span class="hl">exact</span>; the reduced form thins longitudes as cos&nbsp;&phi;.</p></div>
    <div class="panel"><svg id="g-cube" viewBox="0 0 190 190" role="img" aria-label="Cubed sphere grid"></svg>
      <p class="panel__name">Cubed sphere<span>FV3 / DLWP</span></p>
      <p class="panel__note">Regular per face, poles ordinary, but <b>8 three-valent corners</b> and a basis rotation at every seam.</p></div>
    <div class="panel"><svg id="g-hpx" viewBox="0 0 190 190" role="img" aria-label="HEALPix grid"></svg>
      <p class="panel__name">HEALPix<span>12 base pixels</span></p>
      <p class="panel__note">Strictly <span class="hl">equal-area</span> with iso-latitude rings. Rhombic-dodecahedron topology, so again <b>8 three-valent vertices</b>.</p></div>
    <div class="panel"><svg id="g-ico" viewBox="0 0 190 190" role="img" aria-label="Icosahedral mesh"></svg>
      <p class="panel__name">Icosahedral<span>multi-mesh</span></p>
      <p class="panel__note">Quasi-uniform, pole-free, but always <b>12 five-valent vertices</b>. GraphCast sidesteps this by treating it as a graph.</p></div>

    <p class="rowlabel">B &mdash; the memory layout the model actually sees</p>
    <div class="panel"><svg id="t-latlon" viewBox="0 0 190 108" role="img" aria-label="Lat-lon tensor layout"></svg>
      <p class="panel__note"><code>(721, 1440)</code>, one image. The top and bottom edges are <b>not</b> periodic &mdash; but an FFT assumes they are.</p></div>
    <div class="panel"><svg id="t-gauss" viewBox="0 0 190 108" role="img" aria-label="Gaussian tensor layout"></svg>
      <p class="panel__note"><code>(nlat, nlon)</code>, unevenly spaced in latitude. The reduced grid needs ragged storage or padding.</p></div>
    <div class="panel"><svg id="t-cube" viewBox="0 0 190 108" role="img" aria-label="Cubed sphere tensor layout"></svg>
      <p class="panel__note"><code>(6, 64, 64)</code>. Convolution inside a face is a plain 2-D conv; seams need halo exchange.</p></div>
    <div class="panel"><svg id="t-hpx" viewBox="0 0 190 108" role="img" aria-label="HEALPix tensor layout"></svg>
      <p class="panel__note"><code>(12, N, N)</code>. Nested indexing splits each pixel into exactly four, so pooling aligns for free.</p></div>
    <div class="panel"><svg id="t-graph" viewBox="0 0 190 108" role="img" aria-label="Graph layout"></svg>
      <p class="panel__note"><code>(V, E)</code> adjacency. No image at all; convolution is replaced by message passing.</p></div>
  </div>
  <figcaption><b>How to read this:</b> the two rows are the same object seen twice. The top row sets geometric fidelity; the bottom row sets whether it runs efficiently on a GPU, and every engineering trade in this package happens in the gap between them. Great-circle arcs for the cubed sphere and icosahedron are drawn exactly; the HEALPix panel is the projection-plane tessellation inverted back onto the sphere, and its base-pixel side corners land at latitude 41.81 deg (z = 2/3), exactly the zone boundary where three pixels meet.</figcaption>
</figure>

<h4>Cross-check: is HEALPix consistent with GFDL X-SHiELD?</h4>

<p><strong>No &mdash; they are different tilings, and the mismatch is worth understanding before anyone tries to train a HEALPix model on X-SHiELD output.</strong></p>

<p><a href="https://www.gfdl.noaa.gov/shield/">SHiELD</a> is powered by <a href="https://www.gfdl.noaa.gov/fv3/">FV3</a>, the Finite-Volume <em>Cubed-Sphere</em> dynamical core. Its storm-resolving configuration, X-SHiELD, runs a <b>3.25 km global domain on a C3072 cubed sphere</b> with 79 hybrid-sigma-pressure layers &mdash; a figure visible even in the DYAMOND archive path, <code>20200120.00Z.C3072.L79x2</code>. So X-SHiELD's geometry belongs to the same family as PhysicsNeMo's <a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/dlwp"><code>dlwp</code></a> example, not its <a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/dlwp_healpix"><code>dlwp_healpix</code></a> one.</p>

<p>What the two grids share is exactly the topology established above: both are quadrilateral tilings, and both carry precisely eight three-valent corners. What they do not share:</p>

<ul>
<li><b>Equal area.</b> HEALPix is equal-area by construction. FV3's gnomonic cubed sphere is not &mdash; cell areas vary between face centre and corner by roughly a factor of two for the equidistant gnomonic variant, and about 1.3 to 1.5 for the equiangular one.</li>
<li><b>Cell orientation.</b> This is the decisive one for machine learning. <a href="https://doi.org/10.1029/2023MS004021">Karlbauer et al. (2024)</a> moved DLWP from the cubed sphere to HEALPix precisely because every HEALPix cell shares a consistent east&ndash;west orientation, which permits a single location-invariant convolution kernel across the whole globe. On the cubed sphere the polar faces are oriented differently from the equatorial ones, so one shared kernel does not transport patterns correctly across them.</li>
<li><b>Iso-latitude rings.</b> HEALPix has them, which is why it was designed for CMB spherical-harmonic analysis in the first place; the cubed sphere does not.</li>
<li><b>Local refinement.</b> FV3 supports stretched and nested grids &mdash; C-SHiELD, T-SHiELD and Tele-SHiELD all use nests down to 1.4 km. HEALPix has no equivalent; its refinement is globally uniform.</li>
</ul>

<p>The practical consequence: X-SHiELD output must be <em>conservatively remapped</em> before a HEALPix model can consume it. That is exactly the class of operation <a href="https://github.com/ClimateGlobalChange/tempestremap">TempestRemap</a> exists for, and PhysicsNeMo already ships it in the DLWP pipeline (there it runs lat&ndash;lon to cubed sphere; the same tool handles cubed sphere to HEALPix).</p>

<p>One informative data point on what practitioners actually chose. GFDL's own collaboration with <a href="https://allenai.org/blog/ai2-climate-emulator">Ai2 Climate Modeling</a> to emulate X-SHiELD did <em>not</em> go to HEALPix. <a href="https://www.nature.com/articles/s41612-025-01090-0">ACE2</a> coarse-grains to a roughly 1&deg; lat&ndash;lon grid and uses a <a href="https://arxiv.org/abs/2306.03838">Spherical Fourier Neural Operator</a>; <a href="https://arxiv.org/abs/2512.18224">HiRO-ACE</a> trains on a decade of X-SHiELD for emulation and downscaling on the same footing. The lesson generalises to the next subsection: if the <em>operator</em> is properly spherical, you no longer need a clever grid to fix the poles.</p>

<h3>1.2 &nbsp;Operators, and which discretization each one requires</h3>

<p>A grid is only a set of sample points. What actually determines geometric fidelity is how the operator is defined. The dividing line is whether it lives on <span class="hl-f">tensor indices</span> or on the <span class="hl">continuous sphere, discretized by quadrature</span>. The second kind gets two properties for free: resolution-agnosticism (change the grid without changing the architecture) and approximate SO(3) equivariance, because the Haar measure is rotation-invariant.</p>

<p>This pairing is what the rest of the package is built on &mdash; not every operator can run on every grid:</p>

<div class="scroller">
<table>
<thead><tr><th>Operator</th><th>Discretization it requires</th><th>Also runs on</th><th>Why the constraint</th></tr></thead>
<tbody>
<tr><th>Planar 2-D convolution<small>U-Net, ConvNeXt, ConvGRU</small></th>
<td>Any rectangular index array</td>
<td>lat-lon; cubed-sphere <code>(6,N,N)</code>; HEALPix <code>(12,N,N)</code></td>
<td>Needs a regular index neighbourhood only. Faces need halo padding &mdash; PhysicsNeMo hides this behind <a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/models/dlwp_healpix/layers/healpix_blocks.py"><code>enable_healpixpad</code></a>.</td></tr>

<tr><th><a href="https://openreview.net/pdf?id=EXHG-A3jlM">AFNO</a> / <a href="https://arxiv.org/abs/2410.18904">ModAFNO</a><small>planar FFT</small></th>
<td><b>Equirectangular only</b></td>
<td>&mdash;</td>
<td>A 2-D FFT needs uniform sampling and periodicity in both axes. Longitude is periodic; latitude is not, so the transform silently stitches the north pole to the south.</td></tr>

<tr><th><a href="https://arxiv.org/abs/2306.03838">SFNO</a> spectral convolution<small>SHT</small></th>
<td><b>Quadrature-compatible lat-lon</b> (equiangular or Legendre&ndash;Gauss)</td>
<td>Any grid admitting an accurate SHT</td>
<td>The forward and inverse spherical-harmonic transforms need a quadrature rule. Cannot be applied to a cubed-sphere or HEALPix face array directly.</td></tr>

<tr><th><a href="https://arxiv.org/abs/2209.13603">DISCO</a> convolution<small>discrete-continuous</small></th>
<td><b>Any grid with quadrature weights</b></td>
<td>equiangular, Gaussian, HEALPix, unstructured</td>
<td>The filter is a compactly supported basis expansion integrated by sparse quadrature; the grid only supplies sample locations and weights.</td></tr>

<tr><th><a href="https://github.com/NVIDIA/torch-harmonics/blob/main/torch_harmonics/attention/attention.py">AttentionS2</a> / NeighborhoodAttentionS2<small>spherical attention</small></th>
<td><b>Any grid with quadrature weights</b></td>
<td>same as DISCO</td>
<td>Log-quadrature-weights are added to the pre-softmax scores, turning attention into a discretized continuous integral over the sphere.</td></tr>

<tr><th>Message-passing GNN<small>encoder-processor-decoder</small></th>
<td><b>Any point set</b></td>
<td>icosahedral mesh, station networks, unstructured triangulations</td>
<td>Only needs an adjacency and relative-position edge features. The price is no analytic equivariance.</td></tr>

<tr><th>Ragged pixel cross-attention<small>HealDA</small></th>
<td>HEALPix padded XY plus irregular observations</td>
<td>&mdash;</td>
<td>Attends from grid pixels to a variable-length set of nearby observations; see <a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/experimental/models/healda/kernels/pixel_attention.py"><code>kernels/pixel_attention.py</code></a>.</td></tr>
</tbody>
</table>
</div>

<p>Note what this implies about the package layout. <b>Spherical attention, SFNO, DISCO and the SHT are not in PhysicsNeMo at all.</b> They live in <a href="https://github.com/NVIDIA/torch-harmonics">torch-harmonics</a> &mdash; <a href="https://github.com/NVIDIA/torch-harmonics/blob/main/torch_harmonics/attention/attention.py"><code>attention/attention.py</code></a>, <a href="https://github.com/NVIDIA/torch-harmonics/blob/main/torch_harmonics/disco/convolution.py"><code>disco/convolution.py</code></a>, <a href="https://github.com/NVIDIA/torch-harmonics/blob/main/torch_harmonics/spectral_convolution.py"><code>spectral_convolution.py</code></a> and <a href="https://github.com/NVIDIA/torch-harmonics/blob/main/torch_harmonics/sht.py"><code>sht.py</code></a>. PhysicsNeMo has no <code>models/sfno</code> directory; SFNO enters its <a href="https://github.com/NVIDIA/physicsnemo/blob/main/pyproject.toml">model registry</a> through an entry point once <a href="https://github.com/NVIDIA/makani">makani</a> is installed, which is how the <a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/unified_recipe"><code>unified_recipe</code></a> example trains it. The three attention modules that <em>are</em> in PhysicsNeMo are not spherical operators: <a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/experimental/models/healda/attention_layers.py"><code>healda/attention_layers.py</code></a> is ragged local cross-attention with Triton grouped-query kernels, <a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/experimental/nn/flare_attention.py"><code>flare_attention.py</code></a> is low-rank attention routing for <a href="https://arxiv.org/abs/2402.02366">Transolver</a>, and <a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/nn/module/physics_attention.py"><code>physics_attention.py</code></a> belongs to the same family.</p>

<figure class="plate">
  <div class="plate__head">
    <span class="plate__no">Plate II</span>
    <span class="plate__title">Six operator families: receptive field and kernel structure</span>
    <span class="plate__sub">same sphere, same viewpoint</span>
  </div>
  <div class="grid grid--3">
    <div class="panel"><svg id="o-cnn" viewBox="0 0 210 200" role="img" aria-label="Planar convolution kernel distortion"></svg>
      <p class="panel__name">Planar CNN (index space)<span>DLWP, DLWP-HEALPix, U-Net</span></p>
      <p class="panel__note">3&times;3 is constant in the index, not on the sphere. On lat-lon the high-latitude stencil smears into a band, so <b>one weight learns different physical scales at different latitudes</b>. Cubed sphere and HEALPix compress this to about 1.5&times;, at the cost of seams.</p></div>
    <div class="panel"><svg id="o-afno" viewBox="0 0 210 200" role="img" aria-label="AFNO global Fourier receptive field"></svg>
      <p class="panel__name">AFNO (planar FFT)<span><a href="https://github.com/NVIDIA/physicsnemo/tree/main/physicsnemo/models/afno">models/afno</a></span></p>
      <p class="panel__note">Global in a single layer at O(N&nbsp;log&nbsp;N), and by far the easiest to engineer. The price: the latitude FFT <b>implicitly assumes periodicity</b>, sewing the north pole to the south. Polar aliasing is a common source of long-rollout drift.</p></div>
    <div class="panel"><svg id="o-sfno" viewBox="0 0 210 200" role="img" aria-label="SFNO spherical harmonic mode"></svg>
      <p class="panel__name">SFNO (spherical harmonics)<span><a href="https://github.com/NVIDIA/torch-harmonics/blob/main/torch_harmonics/spectral_convolution.py">spectral_convolution.py</a></span></p>
      <p class="panel__note">The spectral multiplier depends only on degree &ell; and is diagonal in <em>m</em>, so the kernel is isotropic and the layer is <span class="hl">exactly SO(3)-equivariant</span>. Poles are ordinary points. Cost is about O(N<sup>3/2</sup>).</p></div>
    <div class="panel"><svg id="o-disco" viewBox="0 0 210 200" role="img" aria-label="DISCO geodesic disk kernel"></svg>
      <p class="panel__name">DISCO convolution<span><a href="https://github.com/NVIDIA/torch-harmonics/blob/main/torch_harmonics/disco/convolution.py">disco/convolution.py</a></span></p>
      <p class="panel__note">A compactly supported filter written as a learnable combination of fixed basis functions, integrated by sparse quadrature at <b>O(N)</b>. Locality and equivariance together. The kernel shape is fixed after training.</p></div>
    <div class="panel"><svg id="o-nas2" viewBox="0 0 210 200" role="img" aria-label="Spherical neighborhood attention"></svg>
      <p class="panel__name">NeighborhoodAttentionS2<span><a href="https://github.com/NVIDIA/torch-harmonics/tree/main/torch_harmonics/attention">torch_harmonics/attention</a></span></p>
      <p class="panel__note">The same geodesic disk <code>d(x,x') &le; &theta;</code> in great-circle distance, but the weights inside it are <b>set by the data</b> rather than by a fixed basis. O(kN), and the only local operator here with an adaptive kernel.</p></div>
    <div class="panel"><svg id="o-mesh" viewBox="0 0 210 200" role="img" aria-label="Multi-mesh message passing edges"></svg>
      <p class="panel__name">Multi-mesh message passing<span><a href="https://github.com/NVIDIA/physicsnemo/tree/main/physicsnemo/models/graphcast">models/graphcast</a></span></p>
      <p class="panel__note">Edges from every refinement level are stacked into one graph, so a single hop can cross a hemisphere. Geometry enters through <b>relative-position edge features</b>; no analytic equivariance, but the least fussy about grid shape.</p></div>
  </div>
  <figcaption><b>Teal = points reachable within one layer; ochre = relative kernel weight.</b> The SFNO panel plots a genuine spherical harmonic Y(6,3) evaluated by associated-Legendre recurrence. The DISCO and NeighborhoodAttentionS2 disks are great-circle distance contours. AttentionS2 is the theta to pi limit of the neighbourhood version, which graphically is just the whole sphere lit up.</figcaption>
</figure>

<h4>Equivariance</h4>

<p>Atmospheric dynamics has no preferred longitude origin. An operator satisfying <code>K[R&middot;f] = R&middot;K[f]</code> has that symmetry written into the architecture rather than learned from data, which is a direct source of sample efficiency and rollout stability.</p>

<figure class="plate">
  <div class="plate__head">
    <span class="plate__no">Plate III</span>
    <span class="plate__title">The commuting square: rotate then act, or act then rotate</span>
    <span class="plate__sub">K = operator, R in SO(3)</span>
  </div>
  <svg id="equiv" viewBox="0 0 700 348" role="img" aria-label="Equivariance commuting diagram"></svg>
  <figcaption><b>Closes:</b> SFNO's spectral convolution, because the multiplier is diagonal in <em>m</em>; DISCO with an isotropic basis; AttentionS2 and NeighborhoodAttentionS2 up to quadrature error. <b>Does not close:</b> AFNO, planar CNNs, and cubed-sphere or HEALPix convolutions &mdash; their weights are bound to indices and face seams, and rotating the earth moves the seams. GraphCast sits in between: no analytic guarantee, but relative-position edge features make it fairly insensitive. <b>Caveat:</b> enabling <code>bias=True</code> in <code>SpectralConvS2</code> adds a spectral bias that does depend on <em>m</em>, which relaxes strict equivariance.</figcaption>
</figure>

<h4>The full comparison</h4>

<div class="scroller">
<table>
<thead><tr>
<th>Scheme</th><th>Receptive field</th><th>Cost / layer</th><th>Cell uniformity</th>
<th>Poles</th><th>SO(3) equivariant</th><th>Resolution-agnostic</th><th>Adaptive kernel</th><th>Hierarchical pooling</th>
</tr></thead>
<tbody>
<tr><th>Lat-lon CNN</th><td>local</td><td>O(N)</td><td class="n">~ cos&phi;, to 0</td><td class="n">singular</td><td class="n">no</td><td class="n">no</td><td class="n">no</td><td class="y">trivial</td></tr>
<tr><th>Cubed-sphere CNN<small>DLWP</small></th><td>local</td><td>O(N)</td><td class="p">~1.3-2x</td><td class="y">ordinary</td><td class="n">no</td><td class="n">no</td><td class="n">no</td><td class="y">trivial</td></tr>
<tr><th>HEALPix CNN<small>DLWP-HEALPix</small></th><td>local</td><td>O(N)</td><td class="y">exactly equal</td><td class="y">ordinary</td><td class="n">no</td><td class="n">no</td><td class="n">no</td><td class="y">4-fold nested</td></tr>
<tr><th>AFNO<small>planar FFT</small></th><td class="y">global</td><td class="y">O(N log N)</td><td class="n">~ cos&phi;</td><td class="n">falsely stitched</td><td class="n">no</td><td class="n">no</td><td class="p">gating only</td><td>needs interpolation</td></tr>
<tr><th>SFNO<small>spectral conv</small></th><td class="y">global</td><td class="p">~O(N<sup>3/2</sup>)</td><td>set by quadrature grid</td><td class="y">ordinary</td><td class="y">strict</td><td class="y">yes</td><td class="n">no (fixed)</td><td class="y">spectral truncation</td></tr>
<tr><th>DISCO conv</th><td>local (geodesic disk)</td><td class="y">O(N)</td><td>any grid</td><td class="y">ordinary</td><td class="y">strict<small>isotropic basis</small></td><td class="y">yes</td><td class="n">no (fixed)</td><td class="y">resampling</td></tr>
<tr><th>NeighborhoodAttentionS2</th><td>local (geodesic disk)</td><td class="p">O(kN)</td><td>any grid</td><td class="y">ordinary</td><td class="p">approximate</td><td class="y">yes</td><td class="y">yes</td><td class="y">resampling</td></tr>
<tr><th>AttentionS2</th><td class="y">global</td><td class="n">O(N&sup2;)</td><td>any grid</td><td class="y">ordinary</td><td class="p">approximate</td><td class="y">yes</td><td class="y">yes</td><td class="y">resampling</td></tr>
<tr><th>Multi-mesh GNN<small>GraphCast</small></th><td class="y">multi-scale</td><td>O(E)</td><td class="p">quasi-uniform</td><td class="y">ordinary</td><td class="n">no<small>edge features soften it</small></td><td class="p">graph must be rebuilt</td><td class="p">gated</td><td class="y">multigrid</td></tr>
</tbody>
</table>
</div>

<h4>Which is best for the sphere</h4>

<div class="verdict">
  <div class="verdict__row"><div class="verdict__key">Best geometry</div><div>
    <p><b>NeighborhoodAttentionS2 on a HEALPix or Gaussian quadrature grid.</b> Local, approximately equivariant, resolution-agnostic, O(kN), and the kernel adapts to the data &mdash; something neither SFNO nor DISCO offers. The cost is a torch-harmonics dependency, CUDA-kernel availability, and the memory for precomputed neighbourhoods.</p></div></div>
  <div class="verdict__row"><div class="verdict__key">Best rollout</div><div>
    <p><b><a href="https://arxiv.org/abs/2306.03838">SFNO</a>.</b> Strict equivariance plus the absence of polar aliasing is the structural reason it holds together over long autoregressive rollouts, not a tuning artefact; spectral truncation also damps small-scale blow-up. The cost is O(N<sup>3/2</sup>) and a quadrature-compatible grid.</p></div></div>
  <div class="verdict__row"><div class="verdict__key">Best grid</div><div>
    <p><b>HEALPix.</b> The only one that is simultaneously equal-area, iso-latitude (so spherical harmonics stay cheap), four-fold nested (so U-Nets pool cleanly), and consistently oriented (so one convolution kernel works everywhere). The cost is special-casing eight three-valent vertices and the face-padding machinery.</p></div></div>
  <div class="verdict__row"><div class="verdict__key">Cheapest</div><div>
    <p><b>AFNO or a lat-lon CNN.</b> The data already arrives on this grid, no remapping, and FFTs are fast. Least faithful geometrically, but positional encodings, static fields and enough data get you a long way. Entirely adequate for prototypes, diagnostic models and downscaling.</p></div></div>
  <div class="verdict__row"><div class="verdict__key">Grid-agnostic</div><div>
    <p><b>Multi-mesh GNN.</b> When the data is not on a regular grid at all &mdash; station observations, unstructured meshes, regional nests &mdash; a graph is the only option that skips remapping entirely. Give up analytic equivariance, gain complete indifference to geometry.</p></div></div>
  <div class="verdict__row"><div class="verdict__key">Counterpoint</div><div>
    <p>More equivariance is not strictly better. The real atmosphere <b>has</b> preferred axes: rotation, land&ndash;sea contrast, orography. A strictly SO(3)-equivariant operator cannot express the fact that the tropics and the poles behave differently, which is why SFNO-class models still feed static fields and cosine zenith angle back in to <em>break</em> the symmetry. Treat equivariance as a good prior, not a destination.</p></div></div>
</div>

<p class="kicker">Section 2</p>
<h2>Global medium-range emulators (autoregressive, mostly deterministic)</h2>

<p>Six examples in <a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather"><code>examples/weather</code></a> map an atmospheric state to its successor and iterate. They differ far less in "CNN versus transformer" than in which discretization from &sect;1.1 they commit to.</p>

<h3><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/fcn_afno">fcn_afno</a> &mdash; FourCastNet v1</h3>
<p>A <a href="https://arxiv.org/abs/2010.11929">vision transformer</a> whose self-attention is replaced by <a href="https://openreview.net/pdf?id=EXHG-A3jlM">AFNO</a>: token mixing happens in the Fourier domain with a block-diagonal MLP and soft thresholding, dropping the cost from O(N&sup2;) to O(N&nbsp;log&nbsp;N). Trained on a 20-channel ERA5 subset at 0.25&deg;, step 6 h, autoregressive. A week-long forecast takes under two seconds. Paper: <a href="https://arxiv.org/abs/2202.11214">Pathak et al. 2022</a>. Model code: <a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/models/afno/afno.py"><code>models/afno/afno.py</code></a>.</p>

<h3><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/graphcast">graphcast</a></h3>
<p>A re-implementation of <a href="https://arxiv.org/abs/2212.12794">GraphCast</a>. Encoder, processor, decoder over an icosahedral multi-mesh: the lat-lon grid is encoded onto a mesh built by repeated subdivision, a deep message-passing network propagates information across edges spanning several scales at once, and the decoder maps back to the grid. 73 ERA5 channels, step 6 h, with up to 12 steps of autoregressive fine-tuning. A synthetic-dataset switch (<code>synthetic_dataset=true</code>) lets you smoke-test without ERA5. Code: <a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/models/graphcast/graph_cast_net.py"><code>graph_cast_net.py</code></a>, mesh construction in <a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/models/graphcast/utils/icosahedral_mesh.py"><code>icosahedral_mesh.py</code></a>, loss in <a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/metrics/climate/graphcast_loss.py"><code>graphcast_loss.py</code></a>.</p>

<h3><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/pangu_weather">pangu_weather</a></h3>
<p>A re-implementation of <a href="https://arxiv.org/abs/2211.02556">Pangu-Weather</a>. A 3-D Earth-Specific Transformer treats pressure levels as a genuine third dimension for windowed attention and adds a position-dependent earth-specific bias per window. Inputs come in three blocks: 4 surface channels (t2m, 10u, 10v, msl), 5 upper-air variables on 13 pressure levels (65 channels), and 3 static fields (land-sea mask, soil type, topography). Requires <a href="https://github.com/NVIDIA/apex">NVIDIA Apex</a> for the optimizer. Code: <a href="https://github.com/NVIDIA/physicsnemo/tree/main/physicsnemo/models/pangu"><code>models/pangu</code></a>.</p>

<h3><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/dlwp">dlwp</a> &mdash; cubed sphere</h3>
<p>A CNN mapping u(t) to u(t+6h) on a cubed sphere, 6 faces of 64&times;64, remapped from ERA5 with <a href="https://github.com/ClimateGlobalChange/tempestremap">TempestRemap</a>. U-Net with skip connections, 7 ERA5 variables, 18 input and 14 output channels in the shipped config. At 1.4&deg; it produces 320-member six-week ensembles in minutes. Papers: <a href="https://doi.org/10.1029/2020MS002109">Weyn et al. 2020</a> and <a href="https://doi.org/10.1029/2021MS002502">Weyn et al. 2021</a>.</p>

<h3><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/dlwp_healpix">dlwp_healpix</a> &mdash; HEALPix, and a coupled ocean</h3>
<p>The same idea on the HEALPix mesh, with a recurrent U-Net built from <a href="https://arxiv.org/abs/2201.03545">ConvNeXt</a> blocks and ConvGRU cells (<a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/models/dlwp_healpix/HEALPixRecUNet.py"><code>HEALPixRecUNet.py</code></a>). The distinguishing feature is atmosphere-ocean coupling: a <b>DLOM</b> (Deep Learning Ocean Model) forecasts sea-surface temperature on a slower 48-hour step and is trained jointly with the 6-hour atmospheric model, configured through <code>config_hpx32_coupled_dlwp</code> and <code>config_hpx32_coupled_dlom</code>. Coupling logic in <a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/datapipes/healpix/couplers.py"><code>datapipes/healpix/couplers.py</code></a>. Paper: <a href="https://arxiv.org/abs/2311.06253">Karlbauer et al. 2024</a>; original reference implementation: <a href="https://github.com/CognitiveModeling/dlwp-hpx">CognitiveModeling/dlwp-hpx</a>.</p>

<h3>Data plumbing</h3>
<p><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/dataset_download"><code>dataset_download</code></a> pulls ERA5 through the <a href="https://cds.climate.copernicus.eu/">Copernicus CDS API</a> into Zarr (a resumable checkpoint format) and then into HDF5 split across <code>train/</code>, <code>test/</code>, <code>out_of_sample/</code> and <code>stats/</code>. Fixed at 0.25&deg;; <code>dt</code> must divide 24; roughly 15 GB per variable per year. It does not handle invariant fields, so land-sea mask and orography must be sourced separately.</p>
<p><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/unified_recipe"><code>unified_recipe</code></a> is a single training scaffold: pull from <a href="https://github.com/google-research/arco-era5">ARCO-ERA5</a>, curate and regrid to Zarr, then swap configs to train AFNO, GraphCast or <a href="https://arxiv.org/abs/2306.03838">SFNO</a>. SFNO requires <a href="https://github.com/NVIDIA/makani">makani</a>, which registers the model through PhysicsNeMo's entry-point registry. This is the right starting point for architecture comparisons on identical data.</p>

<p class="kicker">Section 3</p>
<h2>Regional downscaling and generative high resolution (two-stage regression plus diffusion)</h2>

<p>Both examples here share one design: <b>a deterministic regression U-Net predicts the conditional mean, and a diffusion model learns only the residual.</b> That split matters. A pure diffusion model must learn the large-scale mean and the small-scale texture at once, which trains poorly; absorbing the mean into an L2 regression leaves the diffusion model a zero-mean, much lower-variance target, cutting both sample count and instability. The price is two training runs, and the fact that regression bias propagates into the diffusion stage. Both use <a href="https://arxiv.org/abs/2206.00364">EDM</a> preconditioning over <a href="https://arxiv.org/abs/2011.13456">SongUNet</a> backbones (<a href="https://github.com/NVIDIA/physicsnemo/tree/main/physicsnemo/models/diffusion_unets"><code>models/diffusion_unets</code></a>).</p>

<h3><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/corrdiff">corrdiff</a> &mdash; km-scale downscaling</h3>
<p><a href="https://arxiv.org/abs/2309.15214">CorrDiff</a> maps coarse ERA5 or GEFS onto a high-resolution regional target. Three dataset configurations, and the differences between them are easy to get wrong:</p>
<ul>
<li><b>Taiwan / CWA</b> (<a href="https://github.com/NVIDIA/physicsnemo/blob/main/examples/weather/corrdiff/conf/base/dataset/cwb.yaml"><code>cwb.yaml</code></a>): 12 input channels to a 448&times;448 target at 4&times; downscaling. The four output channels are <b>maximum radar reflectivity, 10u, 10v and t2m</b> &mdash; confirmed by the normalisation constants in <a href="https://github.com/NVIDIA/physicsnemo/blob/main/examples/weather/corrdiff/datasets/cwb.py"><code>datasets/cwb.py</code></a>. There is no precipitation channel in this configuration.</li>
<li><b>GEFS-HRRR / CONUS</b> (<a href="https://github.com/NVIDIA/physicsnemo/blob/main/examples/weather/corrdiff/conf/base/dataset/gefs_hrrr.yaml"><code>gefs_hrrr.yaml</code></a>): this is where precipitation lives. Outputs are <code>u10m, v10m, t2m, precip</code> plus <b>four precipitation-type probabilities</b> (snow, ice, freezing rain, rain). Hence the <code>lt_aware_ce_regression</code> variant &mdash; cross-entropy for the categorical phase, and a lead-time embedding over 9 forecast steps because the input is a GEFS forecast rather than a reanalysis.</li>
<li><b>HRRR-Mini</b>: a deliberately small network and dataset (about 10 A100-hours) for learning the codebase; outputs only 10u and 10v. Available on <a href="https://catalog.ngc.nvidia.com/orgs/nvidia/teams/modulus/resources/modulus_datasets-hrrr_mini">NGC</a>.</li>
</ul>
<p>A <code>patched_diffusion</code> variant tiles a large domain and runs multi-diffusion with 100 learnable positional channels, which is what makes training on a 1057&times;1796 domain tractable.</p>

<h3><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/stormcast">stormcast</a> &mdash; convection-allowing emulation</h3>
<p><a href="https://arxiv.org/abs/2408.10958">StormCast</a> emulates NOAA's 3 km <a href="https://rapidrefresh.noaa.gov/hrrr/">HRRR</a> autoregressively. The regression model predicts the next HRRR step from the previous HRRR state plus an ERA5 background; the diffusion model corrects it. The crucial contrast with CorrDiff: <b>StormCast advances in time (1-hour autoregressive rollout), CorrDiff does single-frame spatial downscaling.</b> Domain 512&times;640, roughly 100 variables (u/v/t/q on many model levels plus surface fields and reflectivity). The same recipe also trains <b>Stormscope</b> (<a href="https://arxiv.org/abs/2601.17268">arXiv:2601.17268</a>), which drops the regression stage for a diffusion-only <a href="https://arxiv.org/abs/2212.09748">DiT</a> and nowcasts clouds and precipitation from GOES radiances and MRMS radar. Config: <a href="https://github.com/NVIDIA/physicsnemo/blob/main/examples/weather/stormcast/config/model/stormscope.yaml"><code>config/model/stormscope.yaml</code></a>.</p>

<p class="kicker">Section 4</p>
<h2>Diagnostics, post-processing and ensembling</h2>

<h3><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/diagnostic">diagnostic</a></h3>
<p>A <em>diagnostic</em> model does not advance time; it infers an extra variable from the simultaneous atmospheric state. The shipped example is an <a href="https://openreview.net/pdf?id=EXHG-A3jlM">AFNO</a> with 27 input channels &mdash; the 20 ERA5 variables from <a href="https://arxiv.org/abs/2202.11214">Pathak et al. 2022</a>, plus cosine zenith angle, geopotential, land-sea mask and four lat/lon encoding channels &mdash; producing one output, <code>tp06</code> (6-hour accumulated precipitation). This is FourCastNet's precipitation module as a standalone, and the template for bolting a diagnostic head onto any backbone. Config: <a href="https://github.com/NVIDIA/physicsnemo/blob/main/examples/weather/diagnostic/config/diagnostic_precip.yaml"><code>diagnostic_precip.yaml</code></a>.</p>

<h3><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/temporal_interpolation">temporal_interpolation</a></h3>
<p>AI forecast models step natively at 6 hours; this one interpolates to 1 hour. <a href="https://arxiv.org/abs/2410.18904">ModAFNO</a> takes both endpoint states plus auxiliary fields such as orography, and an embedding network converts the conditioning variable into shift and scale parameters for each AFNO block &mdash; FiLM-style modulation. It is deterministic, trained with a latitude-weighted L2 loss, and approximates the conditional expectation of the intermediate state given both endpoints and the offset. The released model used 73 variables, about 100 TB of data and 64 H100s. A pretrained wrapper exists in <a href="https://nvidia.github.io/earth2studio/modules/generated/models/px/earth2studio.models.px.InterpModAFNO.html">Earth2Studio</a>. Code: <a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/models/afno/modafno.py"><code>models/afno/modafno.py</code></a>.</p>

<h3><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/mixture_of_experts">mixture_of_experts</a> &mdash; MoWE</h3>
<p>Mixture of Weather Experts. Forecast fields from <a href="https://www.nature.com/articles/s41586-025-09005-y">Aurora</a>, <a href="https://arxiv.org/abs/2211.02556">Pangu-Weather</a> and <a href="https://arxiv.org/abs/2507.12144">FourCastNet 3</a> are stacked as a multi-channel image; a <a href="https://arxiv.org/abs/2212.09748">Diffusion Transformer</a> acts as the gating network, conditioned on lead time (sampled between 6 hours and 2 days during training), and emits per-expert weights and a bias so that the blended forecast is a weighted sum of the experts. A probabilistic variant additionally consumes a noise vector and trains with a <a href="https://doi.org/10.1175/MWR2904.1">CRPS</a> loss. All expert forecasts must be generated offline first with <a href="https://github.com/NVIDIA/earth2studio">Earth2Studio</a> &mdash; multiple TB. DiT code: <a href="https://github.com/NVIDIA/physicsnemo/tree/main/physicsnemo/models/dit"><code>models/dit</code></a>.</p>

<p class="kicker">Section 5</p>
<h2>Data assimilation</h2>

<h3><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/regen">regen</a> &mdash; score-based DA</h3>
<p>The trick is that no conditional model is ever trained. An <em>unconditional</em> diffusion model is fit to <a href="https://rapidrefresh.noaa.gov/hrrr/">HRRR</a> over a 128&times;128 Oklahoma window with channels <code>10u, 10v, tp</code>. At inference, <a href="https://arxiv.org/abs/2306.10574">score-based data assimilation</a> modifies only the sampling loop: at each denoising step the current estimate is passed through an observation operator, compared against real station data, and the resulting posterior score &mdash; the prior score plus the likelihood score &mdash; steers the next update. Observations come from NOAA's <a href="https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database">Integrated Surface Database</a>. Assimilating 40 stations lowers RMSE at held-out stations by about 10% relative to HRRR itself, the first demonstration of this at kilometre scale. Paper: <a href="https://arxiv.org/abs/2406.16947">Manshausen et al. 2024</a>.</p>

<h3><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/healda">healda</a> &mdash; stateless DA on HEALPix</h3>
<p>Marked <em>under active construction</em> in the repository. The goal is <b>stateless</b> assimilation: no background-forecast cycle, just conventional and satellite observations (ATMS, MHS, conventional) in, one global ERA5-compatible analysis out, on a HEALPix level-6 padded XY grid. The example directory holds only a README, normalisation statistics and requirements; the model and datapipe live in <a href="https://github.com/NVIDIA/physicsnemo/tree/main/physicsnemo/experimental/models/healda"><code>experimental/models/healda</code></a> and <a href="https://github.com/NVIDIA/physicsnemo/tree/main/physicsnemo/experimental/datapipes/healda"><code>experimental/datapipes/healda</code></a>. Architecturally it is a video DiT with temporal self-attention plus ragged pixel-to-observation cross-attention, backed by Triton grouped-query-attention kernels (<a href="https://github.com/NVIDIA/physicsnemo/blob/main/physicsnemo/experimental/models/healda/kernels/pixel_attention.py"><code>pixel_attention.py</code></a>) and <a href="https://arxiv.org/abs/2212.09748">adaLN</a> conditioning. Most of the README is a guide to plugging in your own observation loader and transform.</p>

<p class="kicker">Section 6</p>
<h2>Hydrology</h2>

<h3><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/flood_modeling/hydrographnet">flood_modeling/hydrographnet</a></h3>
<p>A physics-informed graph neural network surrogate for the shallow-water equations. Encoder, processor, decoder message passing on an unstructured mesh autoregressively predicts increments of water depth and volume with residual connections. Three design choices carry the result: a <b>mass-conservation loss</b> built from volume-continuity inequalities (no automatic differentiation required), the <b>pushforward trick</b> to suppress autoregressive error accumulation, and <a href="https://arxiv.org/abs/2404.19756">Kolmogorov-Arnold Networks</a> replacing MLPs for interpretability. Node features mix static attributes (elevation, slope, roughness) with dynamic history, plus global forcings from the inflow hydrograph and precipitation. Validated on the White River near Muncie, Indiana: 4,787 nodes, ground truth from <a href="https://www.hec.usace.army.mil/software/hec-ras/">HEC-RAS</a>, dataset auto-downloaded from <a href="https://zenodo.org/record/14969507">Zenodo</a>. Paper: <a href="https://doi.org/10.1111/mice.13484">Taghizadeh et al. 2025</a>.</p>

<p class="kicker">Quick reference</p>
<h2>One line each</h2>

<div class="scroller">
<table>
<thead><tr><th>Directory</th><th>Principle</th><th>What it does</th><th>Discretization</th></tr></thead>
<tbody>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/fcn_afno">fcn_afno</a></th><td>ViT plus AFNO Fourier mixing</td><td>Global 0.25 deg medium-range forecast</td><td>lat-lon</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/graphcast">graphcast</a></th><td>Multi-scale GNN on icosahedral mesh</td><td>Global 0.25 deg medium-range forecast</td><td>icosahedral</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/pangu_weather">pangu_weather</a></th><td>3-D Earth-Specific Transformer</td><td>Global 0.25 deg medium-range forecast</td><td>lat-lon</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/dlwp">dlwp</a></th><td>CNN U-Net on cubed sphere</td><td>Global 1.4 deg large-ensemble and subseasonal</td><td>cubed sphere</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/dlwp_healpix">dlwp_healpix</a></th><td>ConvNeXt plus ConvGRU U-Net on HEALPix</td><td>Global forecast with coupled ocean (SST)</td><td>HEALPix</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/unified_recipe">unified_recipe</a></th><td>Unified data and training scaffold</td><td>Train AFNO / GraphCast / SFNO on one pipeline</td><td>configurable</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/corrdiff">corrdiff</a></th><td>Regression U-Net plus EDM diffusion residual</td><td>Spatial downscaling (Taiwan: reflectivity, wind, temperature; CONUS: wind, temperature, precipitation and phase)</td><td>regional lat-lon</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/stormcast">stormcast</a></th><td>Regression plus diffusion, autoregressive; or DiT only</td><td>3 km regional CAM emulation, satellite-radar nowcasting</td><td>HRRR grid</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/diagnostic">diagnostic</a></th><td>AFNO diagnostic head</td><td>Infer precipitation from atmospheric state</td><td>lat-lon</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/temporal_interpolation">temporal_interpolation</a></th><td>ModAFNO conditional modulation</td><td>6 h to 1 h temporal interpolation</td><td>lat-lon</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/mixture_of_experts">mixture_of_experts</a></th><td>DiT gating network</td><td>Blend Aurora / Pangu / FCN3 forecasts</td><td>lat-lon</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/regen">regen</a></th><td>Unconditional diffusion plus SDA posterior score</td><td>Assimilate sparse station observations at km scale</td><td>HRRR window</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/healda">healda</a></th><td>Stateless DA, video DiT plus pixel cross-attention</td><td>Observations straight to a global analysis</td><td>HEALPix L6</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/flood_modeling/hydrographnet">hydrographnet</a></th><td>Physics-constrained GNN plus KAN</td><td>Flood depth and volume forecasting</td><td>unstructured mesh</td></tr>
<tr><th><a href="https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/dataset_download">dataset_download</a></th><td>CDS API to Zarr to HDF5</td><td>ERA5 data preparation</td><td>lat-lon</td></tr>
</tbody>
</table>
</div>

<p style="font-family:var(--mono); font-size:.78rem; line-height:1.75; color:var(--ink-3); border-top:1px solid var(--rule); padding-top:16px; margin-top:2.5em;">
Sources: <a href="https://github.com/NVIDIA/physicsnemo">NVIDIA/physicsnemo</a> and <a href="https://github.com/NVIDIA/torch-harmonics">NVIDIA/torch-harmonics</a> <code>main</code> branch source and docstrings, read 2 August 2026; <a href="https://www.gfdl.noaa.gov/shield/">GFDL SHiELD</a> configuration tables for the X-SHiELD cross-check.
</p>

<script>
(() => {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const D2R = Math.PI / 180, TAU = Math.PI * 2;

  const sub = (a,b) => [a[0]-b[0], a[1]-b[1], a[2]-b[2]];
  const cross = (a,b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];
  const dot = (a,b) => a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
  const norm = a => { const n = Math.hypot(a[0],a[1],a[2]) || 1; return [a[0]/n,a[1]/n,a[2]/n]; };
  const sph = (lat,lon) => [Math.cos(lat)*Math.cos(lon), Math.cos(lat)*Math.sin(lon), Math.sin(lat)];

  function rotAxis(axis, ang){
    const [x,y,z] = norm(axis), c = Math.cos(ang), s = Math.sin(ang), t = 1-c;
    return v => [
      (t*x*x+c)*v[0]     + (t*x*y-s*z)*v[1] + (t*x*z+s*y)*v[2],
      (t*x*y+s*z)*v[0]   + (t*y*y+c)*v[1]   + (t*y*z-s*x)*v[2],
      (t*x*z-s*y)*v[0]   + (t*y*z+s*x)*v[1] + (t*z*z+c)*v[2]
    ];
  }

  function camera(lat0, lon0){
    const c = sph(lat0*D2R, lon0*D2R);
    const right = norm(cross([0,0,1], c));
    const up = cross(c, right);
    return { c, right, up };
  }
  const CAM = camera(25, -30);

  function project(v, R, cx, cy, cam){
    cam = cam || CAM;
    return { x: cx + dot(v, cam.right)*R, y: cy - dot(v, cam.up)*R, vis: dot(v, cam.c) > 0.0 };
  }

  function el(tag, attrs){
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }
  function add(parent, tag, attrs){ const e = el(tag, attrs); parent.appendChild(e); return e; }

  function arc(g, pts3, R, cx, cy, cls){
    let run = [];
    const flush = () => {
      if (run.length > 1) add(g, "polyline", { points: run.join(" "), class: cls });
      run = [];
    };
    for (const v of pts3){
      const p = project(v, R, cx, cy);
      if (p.vis) run.push(p.x.toFixed(2) + "," + p.y.toFixed(2));
      else flush();
    }
    flush();
  }

  function gcArc(a, b, n){
    n = n || 24;
    const out = [];
    for (let i = 0; i <= n; i++){
      const t = i/n;
      out.push(norm([a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t, a[2]+(b[2]-a[2])*t]));
    }
    return out;
  }

  function globe(svgId, R, cx, cy){
    const svg = document.getElementById(svgId);
    if (!svg) return null;
    const g = add(svg, "g", {});
    add(g, "circle", { cx: cx, cy: cy, r: R, class: "s-disk" });
    return g;
  }
  function limb(g, R, cx, cy){ add(g, "circle", { cx: cx, cy: cy, r: R, class: "s-limb" }); }

  function dotAt(g, v, R, cx, cy, cls, r){
    const p = project(v, R, cx, cy);
    if (p.vis) add(g, "circle", { cx: p.x.toFixed(2), cy: p.y.toFixed(2), r: (r === undefined ? 2.6 : r), class: cls });
  }

  function smallCircle(c, th, n){
    n = n || 96;
    const u = norm(Math.abs(c[2]) < 0.9 ? cross(c, [0,0,1]) : cross(c, [1,0,0]));
    const w = cross(c, u);
    const out = [];
    for (let i = 0; i <= n; i++){
      const a = i/n*TAU, st = Math.sin(th), ct = Math.cos(th);
      out.push(norm([
        ct*c[0] + st*(Math.cos(a)*u[0] + Math.sin(a)*w[0]),
        ct*c[1] + st*(Math.cos(a)*u[1] + Math.sin(a)*w[1]),
        ct*c[2] + st*(Math.cos(a)*u[2] + Math.sin(a)*w[2])
      ]));
    }
    return out;
  }

  function sampleSphere(step){
    step = step || 7;
    const pts = [];
    for (let lat = -87; lat <= 87; lat += step){
      const cl = Math.cos(lat*D2R);
      const nlon = Math.max(6, Math.round(360/step*cl));
      for (let j = 0; j < nlon; j++) pts.push(sph(lat*D2R, j/nlon*TAU));
    }
    return pts;
  }

  function plm(l, m, x){
    let pmm = 1;
    if (m > 0){
      const s = Math.sqrt(Math.max(0, 1 - x*x));
      let f = 1;
      for (let i = 1; i <= m; i++){ pmm *= -f*s; f += 2; }
    }
    if (l === m) return pmm;
    let pmmp1 = x*(2*m + 1)*pmm;
    if (l === m + 1) return pmmp1;
    let pll = 0;
    for (let ll = m + 2; ll <= l; ll++){
      pll = ((2*ll - 1)*x*pmmp1 - (ll + m - 1)*pmm)/(ll - m);
      pmm = pmmp1; pmmp1 = pll;
    }
    return pll;
  }

  function fieldDots(g, pts, valFn, R, cx, cy, rmax){
    rmax = rmax === undefined ? 2.5 : rmax;
    let mx = 1e-9;
    const vals = pts.map(v => { const s = valFn(v); mx = Math.max(mx, Math.abs(s)); return s; });
    pts.forEach((v, i) => {
      const p = project(v, R, cx, cy);
      if (!p.vis) return;
      const a = vals[i]/mx;
      add(g, "circle", {
        cx: p.x.toFixed(2), cy: p.y.toFixed(2),
        r: (0.5 + rmax*Math.abs(a)*0.85).toFixed(2),
        class: a >= 0 ? "s-ochre-f" : "s-teal-f",
        opacity: (0.25 + 0.7*Math.abs(a)).toFixed(2)
      });
    });
  }

  /* ---------- PLATE I, row A ---------- */
  const R1 = 74, C1 = 95, CY1 = 96;

  (() => {
    const g = globe("g-latlon", R1, C1, CY1); if (!g) return;
    for (let lon = 0; lon < 360; lon += 15){
      const pts = [];
      for (let lat = -90; lat <= 90; lat += 3) pts.push(sph(lat*D2R, lon*D2R));
      arc(g, pts, R1, C1, CY1, "s-grid");
    }
    for (let lat = -75; lat <= 75; lat += 15){
      const pts = [];
      for (let lon = 0; lon <= 360; lon += 3) pts.push(sph(lat*D2R, lon*D2R));
      arc(g, pts, R1, C1, CY1, "s-grid");
    }
    const cell = (lat, lon, cls) => {
      const p = [];
      for (let t = 0; t <= 1.0001; t += 1/8) p.push(sph((lat)*D2R, (lon + 15*t)*D2R));
      for (let t = 0; t <= 1.0001; t += 1/8) p.push(sph((lat + 15*t)*D2R, (lon + 15)*D2R));
      for (let t = 0; t <= 1.0001; t += 1/8) p.push(sph((lat + 15)*D2R, (lon + 15 - 15*t)*D2R));
      for (let t = 0; t <= 1.0001; t += 1/8) p.push(sph((lat + 15 - 15*t)*D2R, lon*D2R));
      arc(g, p, R1, C1, CY1, cls);
    };
    cell(15, -30, "s-teal");
    cell(75, -45, "s-flag-l");
    dotAt(g, [0,0,1], R1, C1, CY1, "s-flag", 3.4);
    limb(g, R1, C1, CY1);
    const lp = project(sph(88*D2R, -30*D2R), R1, C1, CY1);
    add(g.ownerSVGElement, "text", { x: lp.x + 6, y: lp.y - 4, class: "t-lab-f" }).textContent = "pole";
  })();

  (() => {
    const g = globe("g-gauss", R1, C1, CY1); if (!g) return;
    const n = 18, lats = [];
    for (let j = 1; j <= n; j++) lats.push(Math.PI/2 - (j - 0.25)*Math.PI/(n + 0.5));
    for (const la of lats){
      const pts = [];
      for (let lon = 0; lon <= 360; lon += 3) pts.push(sph(la, lon*D2R));
      arc(g, pts, R1, C1, CY1, "s-grid-f");
      const nlon = Math.max(6, Math.round(40*Math.cos(la)));
      for (let k = 0; k < nlon; k++) dotAt(g, sph(la, k/nlon*TAU), R1, C1, CY1, "s-teal-f", 1.25);
    }
    limb(g, R1, C1, CY1);
    add(g.ownerSVGElement, "text", { x: 8, y: 178, class: "t-lab-t" }).textContent = "points per ring ~ cos lat";
  })();

  (() => {
    const g = globe("g-cube", R1, C1, CY1); if (!g) return;
    const faces = [
      { o:[1,0,0],  u:[0,1,0],  v:[0,0,1] },
      { o:[-1,0,0], u:[0,-1,0], v:[0,0,1] },
      { o:[0,1,0],  u:[-1,0,0], v:[0,0,1] },
      { o:[0,-1,0], u:[1,0,0],  v:[0,0,1] },
      { o:[0,0,1],  u:[1,0,0],  v:[0,1,0] },
      { o:[0,0,-1], u:[1,0,0],  v:[0,-1,0] }
    ];
    const N = 4;
    for (const f of faces){
      for (let i = 0; i <= N; i++){
        const s = -1 + 2*i/N;
        const lineU = [], lineV = [];
        for (let k = 0; k <= 20; k++){
          const t = -1 + 2*k/20;
          lineU.push(norm([f.o[0]+f.u[0]*s+f.v[0]*t, f.o[1]+f.u[1]*s+f.v[1]*t, f.o[2]+f.u[2]*s+f.v[2]*t]));
          lineV.push(norm([f.o[0]+f.u[0]*t+f.v[0]*s, f.o[1]+f.u[1]*t+f.v[1]*s, f.o[2]+f.u[2]*t+f.v[2]*s]));
        }
        const edge = (i === 0 || i === N);
        arc(g, lineU, R1, C1, CY1, edge ? "s-ink" : "s-grid-f");
        arc(g, lineV, R1, C1, CY1, edge ? "s-ink" : "s-grid-f");
      }
    }
    for (const sx of [-1,1]) for (const sy of [-1,1]) for (const sz of [-1,1])
      dotAt(g, norm([sx,sy,sz]), R1, C1, CY1, "s-flag", 3.2);
    limb(g, R1, C1, CY1);
    add(g.ownerSVGElement, "text", { x: 8, y: 178, class: "t-lab-f" }).textContent = "8 three-valent corners";
  })();

  function hpxToSph(x, y){
    const P4 = Math.PI/4;
    let z, lon;
    if (Math.abs(y) <= P4){
      z = 8*y/(3*Math.PI);
      lon = x;
    } else {
      const s = 2 - 4*Math.abs(y)/Math.PI;
      z = (1 - s*s/3)*Math.sign(y);
      const q = Math.floor(x/(Math.PI/2));
      const xc = (Math.PI/2)*q + P4;
      lon = s < 1e-7 ? xc : xc + (x - xc)/s;
    }
    z = Math.max(-1, Math.min(1, z));
    return sph(Math.asin(z), lon);
  }
  const HPX_CENTRES = (() => {
    const P4 = Math.PI/4, out = [];
    for (let k = 0; k < 4; k++){
      out.push([P4 + k*Math.PI/2,  P4]);
      out.push([k*Math.PI/2,        0]);
      out.push([P4 + k*Math.PI/2, -P4]);
    }
    return out;
  })();
  (() => {
    const g = globe("g-hpx", R1, C1, CY1); if (!g) return;
    const P4 = Math.PI/4, nside = 4;
    for (const c of HPX_CENTRES){
      const cx0 = c[0], cy0 = c[1];
      for (let i = 0; i <= nside; i++){
        const t = -1 + 2*i/nside;
        const l1 = [], l2 = [];
        for (let k = 0; k <= 26; k++){
          const u = -1 + 2*k/26;
          l1.push(hpxToSph(cx0 + (t + u)*P4/2, cy0 + (t - u)*P4/2));
          l2.push(hpxToSph(cx0 + (u + t)*P4/2, cy0 + (u - t)*P4/2));
        }
        const edge = (i === 0 || i === nside);
        arc(g, l1, R1, C1, CY1, edge ? "s-ink" : "s-grid-f");
        arc(g, l2, R1, C1, CY1, edge ? "s-ink" : "s-grid-f");
      }
    }
    for (let k = 0; k < 4; k++){
      dotAt(g, hpxToSph(k*Math.PI/2,  P4), R1, C1, CY1, "s-flag", 3.2);
      dotAt(g, hpxToSph(k*Math.PI/2, -P4), R1, C1, CY1, "s-flag", 3.2);
    }
    limb(g, R1, C1, CY1);
    add(g.ownerSVGElement, "text", { x: 8, y: 178, class: "t-lab-f" }).textContent = "8 three-valent vertices";
  })();

  const ICO = (() => {
    const p = (1 + Math.sqrt(5))/2, V = [];
    for (const s1 of [-1,1]) for (const s2 of [-1,1]){
      V.push(norm([0, s1, s2*p])); V.push(norm([s1, s2*p, 0])); V.push(norm([s2*p, 0, s1]));
    }
    const edges = [], minD = 2/Math.sqrt(p*p + 1) * 0.999;
    for (let i = 0; i < V.length; i++) for (let j = i+1; j < V.length; j++){
      const d = Math.hypot(V[i][0]-V[j][0], V[i][1]-V[j][1], V[i][2]-V[j][2]);
      if (d < minD*1.05) edges.push([i,j]);
    }
    const adj = V.map(() => new Set());
    for (const e of edges){ adj[e[0]].add(e[1]); adj[e[1]].add(e[0]); }
    const faces = [];
    for (let i = 0; i < V.length; i++) for (const j of adj[i]) for (const k of adj[j])
      if (k > j && j > i && adj[i].has(k)) faces.push([i,j,k]);
    return { V: V, edges: edges, faces: faces };
  })();
  (() => {
    const g = globe("g-ico", R1, C1, CY1); if (!g) return;
    const mid = (a,b) => norm([(a[0]+b[0])/2, (a[1]+b[1])/2, (a[2]+b[2])/2]);
    for (const f of ICO.faces){
      const A = ICO.V[f[0]], B = ICO.V[f[1]], C = ICO.V[f[2]];
      const ab = mid(A,B), bc = mid(B,C), ca = mid(C,A);
      arc(g, gcArc(ab, bc, 10), R1, C1, CY1, "s-grid-f");
      arc(g, gcArc(bc, ca, 10), R1, C1, CY1, "s-grid-f");
      arc(g, gcArc(ca, ab, 10), R1, C1, CY1, "s-grid-f");
    }
    for (const e of ICO.edges) arc(g, gcArc(ICO.V[e[0]], ICO.V[e[1]], 16), R1, C1, CY1, "s-ink");
    for (const v of ICO.V) dotAt(g, v, R1, C1, CY1, "s-flag", 3.2);
    limb(g, R1, C1, CY1);
    add(g.ownerSVGElement, "text", { x: 8, y: 178, class: "t-lab-f" }).textContent = "12 five-valent vertices";
  })();

  /* ---------- PLATE I, row B ---------- */
  const box = (id) => { const s = document.getElementById(id); return s ? add(s, "g", {}) : null; };

  (() => {
    const g = box("t-latlon"); if (!g) return;
    const x0 = 12, y0 = 16, w = 166, h = 74;
    add(g, "rect", { x: x0, y: y0, width: w, height: h, class: "s-limb", fill: "none" });
    for (let i = 1; i < 12; i++) add(g, "line", { x1: x0+w*i/12, y1: y0, x2: x0+w*i/12, y2: y0+h, class: "s-grid-f" });
    for (let j = 1; j < 6; j++) add(g, "line", { x1: x0, y1: y0+h*j/6, x2: x0+w, y2: y0+h*j/6, class: "s-grid-f" });
    add(g, "line", { x1: x0, y1: y0, x2: x0+w, y2: y0, class: "s-flag-l" });
    add(g, "line", { x1: x0, y1: y0+h, x2: x0+w, y2: y0+h, class: "s-flag-l" });
    add(g, "text", { x: x0, y: 11, class: "t-lab-f" }).textContent = "FFT assumes these edges join";
    add(g, "text", { x: x0, y: y0+h+15, class: "t-lab" }).textContent = "(721, 1440)";
  })();

  (() => {
    const g = box("t-gauss"); if (!g) return;
    const x0 = 12, y0 = 16, w = 166, h = 74, n = 13;
    add(g, "rect", { x: x0, y: y0, width: w, height: h, class: "s-limb", fill: "none" });
    for (let j = 0; j < n; j++){
      const th = (j + 0.75)*Math.PI/(n + 0.5);
      const y = y0 + h*(0.5 - 0.5*Math.cos(th));
      const cnt = Math.max(3, Math.round(22*Math.sin(th)));
      for (let k = 0; k < cnt; k++)
        add(g, "circle", { cx: (x0 + 4 + (w - 8)*(k + 0.5)/cnt).toFixed(1), cy: y.toFixed(1), r: 1.5, class: "s-teal-f" });
    }
    add(g, "text", { x: x0, y: 11, class: "t-lab-t" }).textContent = "uneven rows, varying widths";
    add(g, "text", { x: x0, y: y0+h+15, class: "t-lab" }).textContent = "(nlat, nlon) or ragged";
  })();

  (() => {
    const g = box("t-cube"); if (!g) return;
    const s = 34, x0 = 16, y0 = 18;
    const names = ["+x","-x","+y","-y","+z","-z"];
    for (let i = 0; i < 6; i++){
      const cx = x0 + (i % 3)*(s + 12), cy = y0 + Math.floor(i/3)*(s + 8);
      add(g, "rect", { x: cx, y: cy, width: s, height: s, class: "s-limb", fill: "none" });
      for (let k = 1; k < 4; k++){
        add(g, "line", { x1: cx + s*k/4, y1: cy, x2: cx + s*k/4, y2: cy + s, class: "s-grid-f" });
        add(g, "line", { x1: cx, y1: cy + s*k/4, x2: cx + s, y2: cy + s*k/4, class: "s-grid-f" });
      }
      add(g, "text", { x: cx + s + 2, y: cy + 8, class: "t-lab" }).textContent = names[i];
    }
    add(g, "text", { x: x0, y: 11, class: "t-lab" }).textContent = "6 faces, seams need halos";
    add(g, "text", { x: x0, y: 104, class: "t-lab" }).textContent = "(6, 64, 64)";
  })();

  (() => {
    const g = box("t-hpx"); if (!g) return;
    const u = 20, ox = 22, oy = 52;
    const dm = (cx, cy) => {
      add(g, "polygon", {
        points: cx + "," + (cy-u) + " " + (cx+u) + "," + cy + " " + cx + "," + (cy+u) + " " + (cx-u) + "," + cy,
        class: "s-limb", fill: "none"
      });
      add(g, "line", { x1: cx-u/2, y1: cy-u/2, x2: cx+u/2, y2: cy+u/2, class: "s-grid-f" });
      add(g, "line", { x1: cx-u/2, y1: cy+u/2, x2: cx+u/2, y2: cy-u/2, class: "s-grid-f" });
    };
    for (let k = 0; k < 4; k++){
      dm(ox + u + k*2*u, oy - u);
      dm(ox + k*2*u,     oy);
      dm(ox + u + k*2*u, oy + u);
    }
    for (let k = 0; k < 4; k++){
      add(g, "circle", { cx: ox + k*2*u, cy: oy - u, r: 2.6, class: "s-flag" });
      add(g, "circle", { cx: ox + k*2*u, cy: oy + u, r: 2.6, class: "s-flag" });
    }
    add(g, "text", { x: 10, y: 11, class: "t-lab-f" }).textContent = "red = only three pixels meet";
    add(g, "text", { x: 10, y: 100, class: "t-lab" }).textContent = "(12, N, N), 4-fold nested";
  })();

  (() => {
    const g = box("t-graph"); if (!g) return;
    const N = 26, pts = [];
    let seed = 7;
    const rnd = () => (seed = (seed*1103515245 + 12345) % 2147483648) / 2147483648;
    for (let i = 0; i < N; i++) pts.push([18 + rnd()*154, 22 + rnd()*62]);
    for (let i = 0; i < N; i++){
      const d = pts.map((p,j) => [Math.hypot(p[0]-pts[i][0], p[1]-pts[i][1]), j])
                   .sort((a,b) => a[0]-b[0]).slice(1,4);
      for (const dd of d)
        add(g, "line", { x1: pts[i][0].toFixed(1), y1: pts[i][1].toFixed(1),
                         x2: pts[dd[1]][0].toFixed(1), y2: pts[dd[1]][1].toFixed(1), class: "s-grid" });
    }
    for (let k = 0; k < 3; k++){
      const a = pts[k*7 % N], b = pts[(k*7 + 13) % N];
      add(g, "line", { x1: a[0].toFixed(1), y1: a[1].toFixed(1), x2: b[0].toFixed(1), y2: b[1].toFixed(1), class: "s-ochre" });
    }
    for (const p of pts) add(g, "circle", { cx: p[0].toFixed(1), cy: p[1].toFixed(1), r: 2.2, class: "s-teal-f" });
    add(g, "text", { x: 12, y: 11, class: "t-lab" }).textContent = "ochre = long-range edges";
    add(g, "text", { x: 12, y: 100, class: "t-lab" }).textContent = "(V, E) adjacency";
  })();

  /* ---------- PLATE II ---------- */
  const R2 = 78, C2 = 105, CY2 = 96;

  function graticule(g, R, cx, cy, cls){
    cls = cls || "s-grid-f";
    for (let lon = 0; lon < 360; lon += 30){
      const p = []; for (let lat = -90; lat <= 90; lat += 4) p.push(sph(lat*D2R, lon*D2R));
      arc(g, p, R, cx, cy, cls);
    }
    for (let lat = -60; lat <= 60; lat += 30){
      const p = []; for (let lon = 0; lon <= 360; lon += 4) p.push(sph(lat*D2R, lon*D2R));
      arc(g, p, R, cx, cy, cls);
    }
  }
  function caption(svgId, txt, cls){
    const s = document.getElementById(svgId); if (!s) return;
    add(s, "text", { x: 10, y: 190, class: cls || "t-lab" }).textContent = txt;
  }

  (() => {
    const g = globe("o-cnn", R2, C2, CY2); if (!g) return;
    graticule(g, R2, C2, CY2);
    const stencil = (lat0, lon0, dotCls, ringCls) => {
      for (let i = -1; i <= 1; i++) for (let j = -1; j <= 1; j++){
        const v = sph((lat0 + i*9)*D2R, (lon0 + j*9)*D2R);
        dotAt(g, v, R2, C2, CY2, dotCls, i === 0 && j === 0 ? 3.1 : 2.2);
      }
      const ring = [];
      for (let t = 0; t <= 1.0001; t += 1/10) ring.push(sph((lat0-13.5)*D2R, (lon0-13.5+27*t)*D2R));
      for (let t = 0; t <= 1.0001; t += 1/10) ring.push(sph((lat0-13.5+27*t)*D2R, (lon0+13.5)*D2R));
      for (let t = 0; t <= 1.0001; t += 1/10) ring.push(sph((lat0+13.5)*D2R, (lon0+13.5-27*t)*D2R));
      for (let t = 0; t <= 1.0001; t += 1/10) ring.push(sph((lat0+13.5-27*t)*D2R, (lon0-13.5)*D2R));
      arc(g, ring, R2, C2, CY2, ringCls);
    };
    stencil(5, -30, "s-teal-f", "s-teal");
    stencil(72, -55, "s-flag", "s-flag-l");
    limb(g, R2, C2, CY2);
    caption("o-cnn", "3x3: compact low, smeared high", "t-lab-f");
  })();

  (() => {
    const g = globe("o-afno", R2, C2, CY2); if (!g) return;
    fieldDots(g, sampleSphere(8), v => {
      const lat = Math.asin(v[2]), lon = Math.atan2(v[1], v[0]);
      return Math.cos(4*lon)*Math.cos(3*lat);
    }, R2, C2, CY2, 2.2);
    const seam = [];
    for (let lat = 62; lat <= 90; lat += 2) seam.push(sph(lat*D2R, -30*D2R));
    for (let lat = 90; lat >= 62; lat -= 2) seam.push(sph(lat*D2R, 150*D2R));
    arc(g, seam, R2, C2, CY2, "s-flag-l");
    dotAt(g, [0,0,1], R2, C2, CY2, "s-flag", 3.6);
    limb(g, R2, C2, CY2);
    caption("o-afno", "red: the false seam across the pole", "t-lab-f");
  })();

  (() => {
    const g = globe("o-sfno", R2, C2, CY2); if (!g) return;
    fieldDots(g, sampleSphere(6), v => {
      const lat = Math.asin(v[2]), lon = Math.atan2(v[1], v[0]);
      return plm(6, 3, Math.sin(lat))*Math.cos(3*lon);
    }, R2, C2, CY2, 2.6);
    limb(g, R2, C2, CY2);
    caption("o-sfno", "real harmonic Y(6,3), poles fine", "t-lab-t");
  })();

  (() => {
    const g = globe("o-disco", R2, C2, CY2); if (!g) return;
    graticule(g, R2, C2, CY2);
    const c = sph(18*D2R, -28*D2R);
    for (const th of [10, 20, 30]) arc(g, smallCircle(c, th*D2R), R2, C2, CY2, th === 30 ? "s-teal" : "s-grid");
    for (const v of sampleSphere(5)){
      const d = Math.acos(Math.max(-1, Math.min(1, dot(v, c))));
      if (d > 30*D2R) continue;
      const w = Math.cos(d/(30*D2R)*Math.PI/2);
      const p = project(v, R2, C2, CY2);
      if (p.vis) add(g, "circle", { cx: p.x.toFixed(2), cy: p.y.toFixed(2), r: (0.7 + 2.4*w).toFixed(2), class: "s-ochre-f", opacity: 0.85 });
    }
    dotAt(g, c, R2, C2, CY2, "s-teal-f", 3.2);
    limb(g, R2, C2, CY2);
    caption("o-disco", "weight = f(great-circle distance)", "t-lab-t");
  })();

  (() => {
    const g = globe("o-nas2", R2, C2, CY2); if (!g) return;
    graticule(g, R2, C2, CY2);
    const c = sph(18*D2R, -28*D2R);
    arc(g, smallCircle(c, 30*D2R), R2, C2, CY2, "s-teal");
    let seed = 11;
    const rnd = () => (seed = (seed*1103515245 + 12345) % 2147483648) / 2147483648;
    for (const v of sampleSphere(5)){
      const d = Math.acos(Math.max(-1, Math.min(1, dot(v, c))));
      if (d > 30*D2R) continue;
      const w = Math.pow(rnd(), 1.7);
      const p = project(v, R2, C2, CY2);
      if (!p.vis) continue;
      add(g, "circle", { cx: p.x.toFixed(2), cy: p.y.toFixed(2), r: (0.6 + 3.2*w).toFixed(2), class: "s-ochre-f", opacity: (0.3 + 0.65*w).toFixed(2) });
      if (w > 0.72){
        const pc = project(c, R2, C2, CY2);
        add(g, "line", { x1: pc.x.toFixed(2), y1: pc.y.toFixed(2), x2: p.x.toFixed(2), y2: p.y.toFixed(2), class: "s-ochre", "stroke-width": 0.8, opacity: 0.75 });
      }
    }
    dotAt(g, c, R2, C2, CY2, "s-teal-f", 3.2);
    limb(g, R2, C2, CY2);
    caption("o-nas2", "same disk, weights set by content", "t-lab-t");
  })();

  (() => {
    const g = globe("o-mesh", R2, C2, CY2); if (!g) return;
    const mid = (a,b) => norm([(a[0]+b[0])/2, (a[1]+b[1])/2, (a[2]+b[2])/2]);
    for (const f of ICO.faces){
      const A = ICO.V[f[0]], B = ICO.V[f[1]], C = ICO.V[f[2]];
      const ab = mid(A,B), bc = mid(B,C), ca = mid(C,A);
      const segs = [[ab,bc],[bc,ca],[ca,ab],[A,ab],[ab,B],[B,bc],[bc,C],[C,ca],[ca,A]];
      for (const sg of segs) arc(g, gcArc(sg[0], sg[1], 8), R2, C2, CY2, "s-grid");
    }
    for (const e of ICO.edges) arc(g, gcArc(ICO.V[e[0]], ICO.V[e[1]], 16), R2, C2, CY2, "s-teal");
    const src = ICO.V[0];
    for (const t of [3, 6, 9]) arc(g, gcArc(src, ICO.V[t], 24), R2, C2, CY2, "s-ochre");
    dotAt(g, src, R2, C2, CY2, "s-flag", 3.4);
    limb(g, R2, C2, CY2);
    caption("o-mesh", "ochre: one hop across a hemisphere", "t-lab");
  })();

  /* ---------- PLATE III ---------- */
  (() => {
    const svg = document.getElementById("equiv"); if (!svg) return;
    const defs = add(svg, "defs", {});
    const mk = add(defs, "marker", { id: "pnx-ah", viewBox: "0 0 10 10", refX: "9", refY: "5",
      markerWidth: "7", markerHeight: "7", orient: "auto" });
    add(mk, "path", { d: "M0,0 L10,5 L0,10 z", class: "s-ink-f" });

    const g = add(svg, "g", {});
    const R = 50, ROW = [96, 252], COL = [104, 400];
    const inv = rotAxis([0.35, 0.55, 1], -62*D2R);

    const a1 = sph(28*D2R, -50*D2R), a2 = sph(-22*D2R, 12*D2R);
    const ang = (v, a) => Math.acos(Math.max(-1, Math.min(1, dot(v, a))));
    const lobes = (w1, w2, amp) => v =>
      amp*(1.15*Math.exp(-Math.pow(ang(v,a1)/w1, 2)) - Math.exp(-Math.pow(ang(v,a2)/w2, 2)));
    const base = lobes(0.55, 0.42, 1);
    const smoothed = lobes(0.88, 0.72, 0.72);

    const panel = (cx, cy, valFn, label, sub, subCls) => {
      add(g, "circle", { cx: cx, cy: cy, r: R, class: "s-disk" });
      graticule(g, R, cx, cy);
      fieldDots(g, sampleSphere(9), valFn, R, cx, cy, 2.3);
      add(g, "circle", { cx: cx, cy: cy, r: R, class: "s-limb" });
      add(g, "text", { x: cx, y: cy + R + 17, class: "t-lab", "text-anchor": "middle", style: "font-size:11.5px" }).textContent = label;
      if (sub) add(g, "text", { x: cx, y: cy + R + 30, class: subCls || "t-lab", "text-anchor": "middle" }).textContent = sub;
    };

    panel(COL[0], ROW[0], base,                  "f",      "input field");
    panel(COL[1], ROW[0], v => base(inv(v)),     "R . f",  "rotate first");
    panel(COL[0], ROW[1], smoothed,              "K[ f ]", "apply operator first");
    panel(COL[1], ROW[1], v => smoothed(inv(v)), "K[ R.f ]  =  R . K[ f ]", "both paths land on one figure", "t-lab-t");

    const arrow = (x1, y1, x2, y2, lab, dx, dy) => {
      add(g, "line", { x1: x1, y1: y1, x2: x2, y2: y2, class: "s-ink", "marker-end": "url(#pnx-ah)" });
      add(g, "text", { x: (x1+x2)/2 + (dx||0), y: (y1+y2)/2 + (dy||0), class: "t-lab", "text-anchor": "middle" }).textContent = lab;
    };
    arrow(COL[0]+R+12, ROW[0], COL[1]-R-12, ROW[0], "rotate R", 0, -8);
    arrow(COL[0]+R+12, ROW[1], COL[1]-R-12, ROW[1], "rotate R", 0, -8);
    arrow(COL[0], ROW[0]+R+40, COL[0], ROW[1]-R-10, "operator K", -30, 4);
    arrow(COL[1], ROW[0]+R+40, COL[1], ROW[1]-R-10, "operator K", -30, 4);

    const LX = 500;
    add(g, "text", { x: LX, y: 92,  class: "t-lab-t", style: "font-size:12.5px" }).textContent = "square closes";
    add(g, "text", { x: LX, y: 112, class: "t-lab-t", style: "font-size:12.5px" }).textContent = "K[R.f] = R.K[f]";
    add(g, "text", { x: LX, y: 138, class: "t-lab" }).textContent = "SFNO spectral conv (strict)";
    add(g, "text", { x: LX, y: 154, class: "t-lab" }).textContent = "DISCO isotropic basis (strict)";
    add(g, "text", { x: LX, y: 170, class: "t-lab" }).textContent = "S2 attention (approximate)";
    add(g, "line", { x1: LX, y1: 186, x2: LX + 165, y2: 186, class: "s-grid" });
    add(g, "text", { x: LX, y: 206, class: "t-lab-f", style: "font-size:12.5px" }).textContent = "square does not close";
    add(g, "text", { x: LX, y: 226, class: "t-lab-f" }).textContent = "AFNO, planar CNN";
    add(g, "text", { x: LX, y: 242, class: "t-lab-f" }).textContent = "cubed-sphere / HEALPix conv";
    add(g, "text", { x: LX, y: 258, class: "t-lab-f" }).textContent = "(weights bound to indices, seams)";
  })();
})();
</script>

</div>
{% endraw %}
