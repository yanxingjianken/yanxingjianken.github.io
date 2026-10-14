---
title: "Successive correction of a generative downscaling ensemble: correct the member mean, rescale the perturbations"
excerpt: "A generative downscaler draws several equally likely fine fields per hour. Their mean is corrected by a linear model and then by boosting stages, each a model of what the earlier ones miss; each member's deviation from the mean is kept and only rescaled. Worked box by box on a one-dimensional example, with movies.<br/><img src='/images/successive_correction/fig8_write.png' style='max-width: 60%; height: auto;'>"
collection: portfolio
redirect_from:
  - /portfolio/203_boosting_ladder/
  - /files/boosting_ladder/
---

{% include base_path %}
<link rel="stylesheet" href="{{ base_path }}/assets/css/journal.css">
<style>
.page__title { display: none; }
.sci .sci-kicker { font-family: var(--jn-sans); font-size: 8.5pt; letter-spacing: 0.06em; text-transform: uppercase; color: var(--jn-ink-2); border-bottom: 1px solid var(--jn-rule); padding-bottom: 4px; margin: 0 0 12px 0; }
.sci h1.sci-title { font-family: var(--jn-serif); font-size: 20pt; line-height: 1.15; margin: 0 0 8px 0; }
.sci .sci-authors { font-family: var(--jn-sans); font-size: 10pt; margin: 0 0 2px 0; }
.sci .sci-affil { font-family: var(--jn-sans); font-size: 8.5pt; color: var(--jn-ink-2); margin: 0 0 14px 0; }
.sci .sci-abstract { font-size: 10.5pt; font-weight: 700; line-height: 1.45; margin: 0 0 16px 0; }
.sci h2 { font-family: var(--jn-sans); font-size: 11pt; font-weight: 700; margin: 1.7em 0 0.4em 0; }
.sci h3 { font-family: var(--jn-sans); font-size: 10pt; font-style: normal; font-weight: 700; margin: 1.2em 0 0.3em 0; }
.sci h3 .box-kind { font-weight: 400; color: var(--jn-ink-3); font-size: 8.5pt; margin-left: 0.4em; }
.sci .cite { font-style: italic; }
.sci figure.jn-fig img { width: 100%; height: auto; display: block; border: 0; }
.sci figure.jn-fig.flow img { max-width: 760px; margin: 0 auto; }
.sci figure.jn-fig a { border-bottom: 0; }
.sci .narrow-only { display: none; }
.sci .narrow-only img { margin: 0 0 10px 0; }
@media (max-width: 600px) { .sci .wide-only { display: none; } .sci .narrow-only { display: block; } }
.sci figcaption { font-family: var(--jn-sans); font-size: 8.5pt; line-height: 1.4; text-align: left; }
.sci figcaption b { font-weight: 700; }
.sci .sci-dl { font-family: var(--jn-sans); font-size: 8pt; color: var(--jn-ink-3); }
.sci ol.sci-refs { font-size: 9.5pt; padding-left: 1.6em; }
.sci ol.sci-refs li { margin: 0 0 4px 0; }
.sci .sci-eq { font-family: var(--jn-serif); text-align: center; margin: 0.4em 0 0.8em 0; overflow-x: auto; }
.sci .tbl { overflow-x: auto; margin: 0.6em 0 1.2em 0; }
.sci .tbl table.jn-table { font-size: 9pt; margin: 0; }
.sci .tbl .jn-tabcap { font-family: var(--jn-sans); font-size: 8.5pt; line-height: 1.4; }
.sci table.jn-table td, .sci table.jn-table th { padding: 3px 6px; }
.sci figure.jn-movie canvas { width: 100%; display: block; background: #fff; }
.sci .jn-movie-ctl { font-family: var(--jn-sans); font-size: 8.5pt; display: flex; gap: 10px; align-items: center; margin: 4px 0 2px 0; flex-wrap: wrap; }
.sci .jn-movie-ctl input[type=range] { flex: 1 1 140px; min-width: 100px; }
.sci .jn-movie-ctl span { color: var(--jn-ink-2); flex: 1 1 100%; }
@media (min-width: 700px) { .sci .jn-movie-ctl span { flex: 0 1 auto; min-width: 16em; } }
@media (max-width: 600px) { .sci .tbl table.jn-table { font-size: 8pt; } .sci table.jn-table td, .sci table.jn-table th { padding: 3px 4px; } }
</style>

<div class="jn sci" markdown="0" data-movies="{{ base_path }}/files/successive_correction/data.json">

<p class="sci-kicker">Research article &middot; Estimation theory and machine learning</p>
<h1 class="sci-title">Successive correction of a generative downscaling ensemble: correct the member mean, rescale the perturbations</h1>
<p class="sci-authors">Xingjian Yan</p>
<p class="sci-affil">Department of Earth, Atmospheric and Planetary Sciences, Massachusetts Institute of Technology, Cambridge, MA, USA.</p>

<p class="sci-abstract">A generative downscaling model turns one coarse weather forecast into several equally likely fine fields for each hour, called members. A correction fitted by squared error, applied to each member, pulls every member toward the same average field and removes what makes the members differ. This article describes a chain that corrects only the mean of the members, in successive orders: a linear model with a memory of past hours (order 1), then boosting stages, each a small model of what the orders before it miss (orders 2 to <i>N</i>, the last order). Each member's deviation from the mean, its perturbation, is kept and only rescaled, one band of spatial scales at a time. The chain is followed box by box on a constructed one-dimensional example with 8 members per hour, whose simulated 72-hour cases (runs) are split into runs that fit the models, validation runs that choose the number of orders and the step, and test runs scored once. On 60 validation runs the root-mean-square error of the member mean falls from 0.591 to 0.427 after order 1 and to 0.363 after 18 orders, and a score of the whole ensemble (the fair continuous ranked probability score, lower is better) falls from 0.292 to 0.176; correcting each member separately with order 1 instead keeps 23% of the members' spread (how far the members differ from their mean). On 60 test runs the member-mean error is 0.370 and the score 0.178. The chain for real forecasts of six variables is being built; only the example is shown here.</p>

<p>A weather model run on a coarse grid misses what a finer grid resolves: rain cells, sharp fronts, winds shaped by terrain. Running the fine grid costs far more, so downscaling estimates the fine field from the coarse forecast alone. The target here is the Weather Research and Forecasting model (WRF) run on two nested grids, a coarse outer grid of 27-km cells (called d01) and a fine inner grid of 3-km cells (d03): from a 72-hour d01 forecast, the goal is the d03 fields, hour by hour, for six variables: rain rate; pressure anomaly (pressure minus the model's reference pressure); the two components of the wind 10 m above the ground; and temperature and relative humidity 2 m above the ground.</p>

<p>Generative models produce such fine fields as samples. CorrDiff (<span class="cite">1</span>) combines a regression network, which predicts the mean fine field from the coarse one, with a diffusion model, a generative network that turns random noise into a sample of the fine-scale detail around that mean. Each sample is a member, and the members of one hour form an ensemble: where they agree the estimate is confident, and where they differ (for instance in exactly where a rain cell sits) the differences express the uncertainty. The chain is built on CorrDiff &mu;_v2: the CorrDiff variant that starts from the Ens-CGP mean &mu;<sub><i>t</i></sub> instead of a regression network and whose members read their own two previous hours; &ldquo;v2&rdquo; is its version label. The Ens-CGP mean is the mean of an Ensemble-Conditional Gaussian Process (<span class="cite">2</span>): the mean of the fine fields given the coarse forecast when both are treated as jointly Gaussian, with their statistics taken from a large set of training hours. The diffusion model of &mu;_v2 draws each member as &mu;<sub><i>t</i></sub> plus a generated deviation; besides its own previous hours, each member also reads the coarse forecast's recent hours and the large-scale wind that steers the weather, taken from the Global Forecast System (GFS), so that its detail moves from hour to hour.</p>

<p>The members still have errors that a correction model could learn, such as a response that builds up hours after its cause. The obvious fix, a correction fitted by squared error and applied to every member, fails for a basic reason. A model fitted by squared error converges to the conditional mean of the truth given its inputs (the average truth over all cases with the same inputs), the single best estimate for that loss; applied to each member, it moves every member toward that same estimate, so each member loses its perturbation <i>d<sub>k</sub></i>, its deviation from the mean of the members, and the ensemble collapses onto one smooth field. The chain studied here therefore corrects only the member mean, where squared error is the right loss, and gives each member back its own perturbation, rescaled by a factor &alpha; that is fitted with a score of the whole ensemble: the fair continuous ranked probability score (CRPS), the members' mean distance from the truth minus half their mean distance from one another (Materials and Methods). It is low when the members are close to the truth and differ from one another about as much as they differ from the truth. The plain ensemble CRPS penalizes small ensembles; the fair version is the estimate whose expected value equals the score of the distribution the members are drawn from, so it does not depend on the number of members.</p>

<p>The corrections are successive. Gradient boosting (<span class="cite">3</span>) builds a predictor as a sum of simple models, each fitted to what the sum so far still gets wrong, each added at a fraction &nu; of its size, and stops when the error on data not used for fitting stops falling. The chain uses a linear model first (order 1) and then boosting stages (orders 2 to <i>N</i>). Because the error of a forecast persists from one hour to the next, every correcting order (1 to <i>N</i>) also has a memory, a filter that carries information over from past hours. Figure 1 is the plan of the chain, box by box. The chain for real forecasts is being built; this article shows only a constructed one-dimensional example that runs every box, and its numbers say nothing yet about real weather.</p>

<figure class="jn-fig flow" id="fig-1">
  <a class="wide-only" href="{{ base_path }}/images/successive_correction/fig1_flowchart.svg"><img src="{{ base_path }}/images/successive_correction/fig1_flowchart.png" alt="Flowchart in two panels. A, use, every hour of one forecast run: start, set t to 1, read hour t, order 0 draws 8 members from their own uncorrected previous hours (open loop), split into member mean and perturbations, order 1, set n to 2, order n, decision n less than N looping back to order n, perturbation scaling, write the 8 members, decision t less than 72 looping back to read hour t, end. B, fitting, once: generate members on training and validation runs, each member run forward on its own uncorrected previous hours, split, fit order 1, set n to 2, fit order n, decision validation error still falling looping back, choose N and nu, fit alpha, score validation runs, test runs scored once, end."></a>
  <div class="narrow-only"><a href="{{ base_path }}/images/successive_correction/fig1_flowchart.svg"><img src="{{ base_path }}/images/successive_correction/fig1_flowchart_A.png" alt="Flowchart panel A, use: every hour of one forecast run"></a><a href="{{ base_path }}/images/successive_correction/fig1_flowchart.svg"><img src="{{ base_path }}/images/successive_correction/fig1_flowchart_B.png" alt="Flowchart panel B, fitting: once, in this order"></a></div>
  <figcaption><b>Fig. 1. Successive correction of generative downscaling members, for hourly six-variable downscaling from WRF d01 (27 km) to d03 (3 km).</b> (<b>A</b>) Use. For every hour <i>t</i> of a 72-hour forecast run, order 0 (CorrDiff &mu;_v2) draws 8 members; their mean <i>x&#772;</i> is corrected by order 1 (linear) and by the boosting stages 2 to <i>N</i>, each a model of what the orders before it miss (the residual, truth minus the corrected mean); the members' deviations from their mean (the perturbations <i>d</i>) are kept and only rescaled per scale band. Memory filters (averages over past hours) and lags (values of earlier hours) carry information from hour <i>t</i> &minus; 1 to hour <i>t</i>; order 0 reads its own uncorrected members of the previous hours, never the corrected output (open loop); the hour loop closes at the bottom. Symbols: <i>u<sub>t</sub></i>, the coarse forecast (d01) at hour <i>t</i>; <i>x</i><sub><i>k</i>,<i>t</i></sub>, member <i>k</i>; <i>x&#772;</i><sub><i>t</i></sub>, their mean; <i>d</i><sub><i>k</i>,<i>t</i></sub>, the perturbations; <i>x&#772;</i><sup>(<i>n</i>)</sup><sub><i>t</i></sub>, the mean after order <i>n</i>; <i>e&#770;</i><sup>(<i>n</i>)</sup><sub><i>t</i></sub>, the correction of stage <i>n</i>, made by a random-feature network (one layer of hidden units whose input weights are drawn at random and fixed; only the output weights are fitted); &nu;, the step (the fraction of each correction that is added); <i>y</i><sub><i>k</i>,<i>t</i></sub>, output member <i>k</i>. In panel B, <i>y</i> without a member index is the truth, the fine field the orders are fitted to. A scale band <i>b</i> is a range of spatial wavelengths, <i>P<sub>b</sub></i> keeps band <i>b</i> of a field, <i>z</i><sub><i>b</i>,<i>t</i></sub>, <i>m</i><sub><i>b</i>,<i>t</i></sub>, &beta;<sub><i>b</i></sub> and &phi; are order 1's inputs, the same inputs after its memory filter, its weights and its memory constant (&phi; = 0: no memory), and &alpha;<sub><i>b</i></sub>(lead) is a perturbation scale per band and forecast hour (lead). (<b>B</b>) Fitting. The same parts are fitted once, in the same order, on training runs; the number of orders <i>N</i> and the step &nu; are chosen on validation runs; test runs are scored once at the end. &ldquo;Existing checkpoint&rdquo;: the already trained CorrDiff &mu;_v2 network is used as it is. &ldquo;5 episode folds&rdquo;: the training runs form five groups (folds), each holding whole weather episodes (multi-day weather events); a quantity is out-of-fold when it comes from a fit that did not use the run's group, and in-sample when it comes from a model that was fitted on those same runs. &ldquo;Error, CRPS, spread&rdquo;: the three scores of Materials and Methods. Select the chart (on a phone, either panel) to open it at full size. Shapes: rounded box, start or end; rectangle, process; rectangle with double sides, a model run as one block; slanted box, input or output; diamond, decision; bracket, a note on the box it points to. The gray label after each heading below names the shape of that box. <span class="sci-dl"><a href="{{ base_path }}/images/successive_correction/fig1_flowchart.pdf">PDF</a> &middot; <a href="{{ base_path }}/images/successive_correction/fig1_flowchart.svg">SVG</a></span></figcaption>
</figure>

<div class="tbl" id="table-1">
<p class="jn-tabcap"><b>Table 1. Each box of Fig. 1 on real forecasts and in the worked example.</b></p>
<table class="jn-table">
<thead><tr><th>box</th><th>real forecasts (being built)</th><th>worked example (shown here)</th></tr></thead>
<tbody>
<tr><td>Start: one forecast run</td><td>a 72-hour WRF forecast</td><td>one run: 73 hourly values (hours 0 to 72) of one variable on a line</td></tr>
<tr><td>Read hour <i>t</i></td><td>WRF d01 <i>u<sub>t</sub></i>, <i>u</i><sub><i>t</i>&minus;1</sub>, <i>u</i><sub><i>t</i>&minus;2</sub> (six variables, 27-km grid); GFS steering wind; Ens-CGP mean &mu;<sub><i>t</i></sub></td><td>one coarse series <i>u<sub>t</sub></i> on 32 cells of 27 km (and <i>u</i><sub><i>t</i>&minus;1</sub> through the hourly change); no steering wind, no Ens-CGP mean</td></tr>
<tr><td>Order 0</td><td>CorrDiff &mu;_v2: 8 members <i>x</i><sub><i>k</i>,<i>t</i></sub>; each member reads its own two previous hours, uncorrected (open loop)</td><td>a toy generator: 8 members, each a linear map of the input plus a random part that keeps a fraction of its own previous hour's value (one hour, not two; open loop); stated defect: the random part changes faster from hour to hour than the truth's small scales</td></tr>
<tr><td>Split</td><td>member mean <i>x&#772;</i><sub><i>t</i></sub>, perturbations <i>d</i><sub><i>k</i>,<i>t</i></sub> = <i>x</i><sub><i>k</i>,<i>t</i></sub> &minus; <i>x&#772;</i><sub><i>t</i></sub></td><td>the same</td></tr>
<tr><td>Order 1</td><td>linear, per variable and scale band; inputs: the current <i>x&#772;</i>, d01 and their hourly change, through a memory filter</td><td>linear, per scale band; inputs: the input at 5 points, <i>x&#772;</i> and the hourly change of the input, through a memory filter</td></tr>
<tr><td>Order <i>n</i></td><td>random-feature network on local <i>x&#772;</i><sup>(<i>n</i>&minus;1)</sup>, the coarse forecast (d01) and &mu;<sub><i>t</i></sub>, with its own memory filter and lags</td><td>random-feature network on local <i>x&#772;</i><sup>(<i>n</i>&minus;1)</sup>, the input and its hourly change, with its own memory filter</td></tr>
<tr><td>Perturbation scaling</td><td>&alpha;<sub><i>b</i></sub>(lead) per variable and band</td><td>&alpha;<sub><i>b</i></sub>(lead) per band (one variable)</td></tr>
<tr><td>Write the members</td><td>8 members, six variables, 3 km</td><td>8 members, one variable, 3-km points</td></tr>
<tr><td>Fitting: runs and folds</td><td>training, validation and test runs; 5 folds of whole weather episodes</td><td>240 training, 60 validation and 60 test runs; 5 folds of runs (run number modulo 5)</td></tr>
</tbody>
</table>
</div>

<h2>Results: using the chain, every hour <i>t</i> of one forecast run (Fig. 1A)</h2>

<h3>The worked example</h3>
<p>The example is a constructed test problem with a known truth. A periodic line of 864 km (its right end joins its left end) is seen by a coarse model in 32 cells of 27 km and by a fine model at 288 points 3 km apart, hourly from hour 0 to hour 72. One run is one such realization. The values have no units. The fine truth <i>y</i> (written without a member index; <i>y</i><sub><i>k</i>,<i>t</i></sub> with an index is an output member, an estimate of it) is, by design, the sum of three parts, <i>y</i> = <i>L</i> + <i>M</i> + <i>S</i> (Table 2 and fig. S1). Each part stands for one kind of predictability and so tests one part of the chain: <i>L</i> can be predicted from the same hour of the coarse input, <i>M</i> mostly from its past, and <i>S</i> not at all, only its statistics. On real forecasts the truth (the d03 field) is not split into such parts; in Fig. 1 the truth appears only in panel B, where the orders are fitted to it (&ldquo;Fit order 1 on <i>y</i> &minus; <i>x&#772;</i>&rdquo;).</p>

<div class="tbl" id="table-2">
<p class="jn-tabcap"><b>Table 2. The three parts of the example's truth <i>y</i> = <i>L</i> + <i>M</i> + <i>S</i>.</b> <i>t</i> is the hour; the forcing <i>g</i> = max(<i>L</i>, 0)<sup>2</sup> is the positive part of <i>L</i>, squared. Formulas in Materials and Methods.</p>
<table class="jn-table">
<thead><tr><th>part</th><th>what it is</th><th>predictable from</th><th>boxes of Fig. 1 it tests</th></tr></thead>
<tbody>
<tr><td><i>L</i></td><td>large travelling waves: 3 waves with wavelengths of 288 to 864 km, each with a random speed between &minus;25 and 25 km h<sup>&minus;1</sup></td><td>the same hour of the input</td><td>Read hour <i>t</i>; Order 0 (a map from the same hour)</td></tr>
<tr><td><i>M</i></td><td>a lagged response to the forcing <i>g</i>, that is to <i>L</i> where <i>L</i> is positive: <i>M<sub>t</sub></i> = <i>a M</i><sub><i>t</i>&minus;1</sub> + (1 &minus; <i>a</i>) <i>g<sub>t</sub></i> with <i>a</i> = e<sup>&minus;1/6</sup> &asymp; 0.85, an average of past forcing that forgets on a 6-hour time scale, so <i>M</i> peaks hours after <i>g</i></td><td>mostly the past of the input (the current hour's forcing enters with weight 1 &minus; <i>a</i> &asymp; 0.15)</td><td>the memory filters of Order 1 and Order <i>n</i> (on real forecasts also their lags); the square, a nonlinearity, is for the boosting stages of Order <i>n</i></td></tr>
<tr><td><i>S</i></td><td>a small-scale part with wavelengths of 14 to 43 km, too short for the coarse cells (a grid needs at least two cells per wavelength, 54 km here); each hour it keeps a fraction 0.7 of its previous pattern and adds new random detail; its size is 0.15 + 0.35 max(<i>L</i>, 0)</td><td>its size, from <i>L</i>; its pattern, from nothing</td><td>Split (the members' perturbations <i>d<sub>k</sub></i>); Perturbation scaling</td></tr>
</tbody>
</table>
</div>

<p>The coarse input <i>u</i> is the average over each 27-km cell of <i>L</i> + 0.5<i>g</i>, plus an error of its own that changes slowly from hour to hour. It therefore sees the forcing <i>g</i> at once and at half strength, not the lagged full response <i>M</i>, and none of <i>S</i>. There are 360 runs: 240 training runs fit every model, 60 validation runs choose the number of orders and the step (the other constants are fitted on the training runs), and 60 test runs are scored once, at the end. Errors are root-mean-square errors (RMSE): the square root of the mean squared difference from the truth over all points, hours and runs (over one run when a figure prints it). Every figure shows the same run, the first validation run, and its 1-D panels show the field along the line at hour 36, marked by triangles on the Hovm&ouml;ller diagrams, maps of the field with position along the line across and the hour upward; a feature that travels along the line appears there as a slanted stripe. The hour-to-hour correlation of a pattern, used below, is the correlation along the line between the field at one hour and at the next, averaged over hours and runs: 1 means the pattern does not change. Each figure of a box shows that box's input (the field the box receives), its change (output minus input), its output, the truth, and the error before and after the box (estimate minus truth), all on the same two color scales in every figure. A residual is the opposite, truth minus estimate: what a correction has to add.</p>

<h3>Start: one forecast run<span class="box-kind">start / end</span></h3>
<p>The chain starts from one coarse forecast run, hours 1 to 72 on real forecasts. The example's runs also have the initial hour 0, so they have 73 hourly values, and the chain processes all of them.</p>

<h3><i>t</i> &larr; 1<span class="box-kind">process</span></h3>
<p>The hour counter starts at the first hour, <i>t</i> = 1 on real forecasts and <i>t</i> = 0 in the example, where the loop runs over hours 0 to 72. The memory filter of each correcting order starts from that first hour: before it there is no past, so the filter's state is set to the first hour's inputs.</p>

<h3>Read hour <i>t</i><span class="box-kind">input / output</span></h3>
<p>The chain reads the coarse input of hour <i>t</i> and of the hours before it. In the example that is the coarse value <i>u<sub>t</sub></i> of each 27-km cell; the boxes below use it as interpolated linearly between the centers of the cells to the 3-km points (Fig. 2). The interpolated input already follows the large waves <i>L</i>, but it misses the lagged response <i>M</i>, which peaks after the input does, and the small-scale part <i>S</i>: its validation RMSE is 0.621.</p>

<figure class="jn-fig" id="fig-2">
  <picture><source media="(max-width: 600px)" srcset="{{ base_path }}/images/successive_correction/fig2_read_narrow.png"><img src="{{ base_path }}/images/successive_correction/fig2_read.png" alt="Coarse input as steps and its interpolation along the line at hour 36 with the truth; Hovmöller diagrams of the coarse input, its interpolation, the truth and their errors"></picture>
  <figcaption><b>Fig. 2. Read hour <i>t</i>.</b> (<b>A</b>) The field along the line at hour 36 of the first validation run: the coarse input <i>u</i> on its 27-km cells (gray steps), the same input on the 3-km points (orange) and the truth <i>y</i> (black). (<b>B</b> to <b>G</b>) Hovm&ouml;ller diagrams (position across, hours 0 to 72 upward) of the box's input (B), its change, output minus input (C), its output (D), the truth (E), and the error before (input minus truth, F) and after (output minus truth, G); the RMSE of this run is printed in F and G. The change C is small: interpolation only smooths the steps. B, D and E share one color scale, C, F and G another, and both are the same in every figure. Triangles mark hour 36. <span class="sci-dl"><a href="{{ base_path }}/images/successive_correction/fig2_read.pdf">PDF</a></span></figcaption>
</figure>

<h3>Order 0: CorrDiff &mu;_v2 &rarr; 8 members<span class="box-kind">model run as one block</span></h3>
<p>On real forecasts order 0 is CorrDiff &mu;_v2. In the example it is a toy generator fitted on the training runs: each member is <i>x<sub>k</sub></i> = <i>A u</i> + <i>q</i> + &eta;<sub><i>k</i></sub>, <i>k</i> = 1, &hellip;, 8. The mean part <i>A u</i> + <i>q</i> is the least-squares linear map of the coarse input of the same hour (validation RMSE 0.556); the random part &eta;<sub><i>k</i></sub>, different for every member, has the spatial structure and the hour-to-hour correlation of what that map misses on the training runs. The toy generator is given one defect on purpose: its random part gets a weaker hour-to-hour correlation than it was fitted with, so its fine detail changes faster from hour to hour than the truth's. At wavelengths below 30 km, where <i>S</i> mostly lies, the hour-to-hour correlation of the members' pattern on the validation runs is 0.59, against 0.69 for the truth (Table 3). A single member carries detail everywhere, which makes its RMSE (0.797) larger than that of the smooth interpolated input (Fig. 3): a member is one equally likely sample, and the best single estimate is their mean (next box).</p>
<p>Order 0 runs open loop: a member's next hour is built from its own uncorrected previous hours, never from the corrected output <i>y</i><sub><i>k</i>,<i>t</i></sub>. The corrections of the boxes below therefore never enter order 0's step from one hour to the next: the members carried forward are order 0's own, and each correcting order carries forward only its own memory filter and lags. That is why all members of all hours can be generated first (panel B) and the orders fitted afterwards. Feeding the corrected output back (closed loop) would keep errors already removed by the orders out of the next hour. It is not used because the generator learned from its own outputs, so corrected inputs would be unlike its training inputs, and because every fitted order would require generating the members again.</p>

<figure class="jn-fig" id="fig-3">
  <picture><source media="(max-width: 600px)" srcset="{{ base_path }}/images/successive_correction/fig3_order0_narrow.png"><img src="{{ base_path }}/images/successive_correction/fig3_order0.png" alt="The members around the truth along the line at hour 36; Hovmöller diagrams of members 1 and 2 against the interpolated input and the truth"></picture>
  <figcaption><b>Fig. 3. Order 0.</b> (<b>A</b>) At hour 36: the input on the 3-km points (gray), the 8 members <i>x<sub>k</sub></i> (blue, thin) and the truth (black). (<b>B</b> to <b>G</b>) Member 1 and (<b>H</b> to <b>M</b>) member 2, with columns as in Fig. 2: input, change, output, truth, error before and after. The two members share the same smooth part and differ in their detail. <span class="sci-dl"><a href="{{ base_path }}/images/successive_correction/fig3_order0.pdf">PDF</a></span></figcaption>
</figure>

<div class="tbl" id="table-3">
<p class="jn-tabcap"><b>Table 3. Hour-to-hour correlation of the pattern, per scale band.</b> The correlation along the line between a band's field at one hour and at the next, averaged over hours and runs (1: the pattern does not change). The toy generator's random part is given a weaker correlation on purpose. Below 30 km, where the members are almost all perturbation, the scaling leaves the correlation as order 0 made it; in the larger bands the output members come closer to the truth's correlation, because their mean part is now the corrected mean and &alpha; &lt; 1 shrinks the perturbations there.</p>
<table class="jn-table">
<thead><tr><th>band</th><th class="num">truth, validation</th><th class="num">order-0 members, validation</th><th class="num">output members, validation</th><th class="num">truth, test</th><th class="num">output members, test</th></tr></thead>
<tbody>
<tr><td>above 300 km</td><td class="num">0.99</td><td class="num">0.98</td><td class="num">0.99</td><td class="num">0.99</td><td class="num">0.99</td></tr>
<tr><td>30 to 300 km</td><td class="num">0.93</td><td class="num">0.89</td><td class="num">0.92</td><td class="num">0.94</td><td class="num">0.93</td></tr>
<tr><td>below 30 km</td><td class="num">0.69</td><td class="num">0.59</td><td class="num">0.59</td><td class="num">0.69</td><td class="num">0.59</td></tr>
</tbody>
</table>
</div>

<h3>Split: member mean and perturbation<span class="box-kind">process</span></h3>
<p>The members of hour <i>t</i> are split into their mean <i>x&#772;</i><sub><i>t</i></sub> = (1/8) &Sigma;<sub><i>k</i></sub> <i>x</i><sub><i>k</i>,<i>t</i></sub> and the perturbations <i>d</i><sub><i>k</i>,<i>t</i></sub> = <i>x</i><sub><i>k</i>,<i>t</i></sub> &minus; <i>x&#772;</i><sub><i>t</i></sub>, each member's deviation from the mean (Fig. 4). Averaging removes most of the detail that differs between members, so the mean is closer to the truth than any one member: validation RMSE 0.591 for <i>x&#772;</i> against 0.797 for member 1. The random parts of 8 members do not cancel completely: their mean keeps 1/8 of their variance. From here on the corrections act on <i>x&#772;</i> only; the perturbations are kept unchanged until the perturbation scaling box.</p>

<figure class="jn-fig" id="fig-4">
  <picture><source media="(max-width: 600px)" srcset="{{ base_path }}/images/successive_correction/fig4_split_narrow.png"><img src="{{ base_path }}/images/successive_correction/fig4_split.png" alt="Members, their mean and the truth at hour 36; the perturbations around zero; Hovmöller diagrams from member 1 to the member mean"></picture>
  <figcaption><b>Fig. 4. Split.</b> (<b>A</b>) At hour 36: the members (gray), their mean <i>x&#772;</i> (blue) and the truth (black). (<b>B</b>) The 8 perturbations <i>d<sub>k</sub></i> = <i>x<sub>k</sub></i> &minus; <i>x&#772;</i> at the same hour. (<b>C</b> to <b>H</b>) From member 1 (input) to the member mean (output), columns as in Fig. 2; the change, <i>x&#772;</i> &minus; <i>x</i><sub>1</sub>, is the negative of member 1's perturbation. <span class="sci-dl"><a href="{{ base_path }}/images/successive_correction/fig4_split.pdf">PDF</a></span></figcaption>
</figure>

<h3>Order 1 (linear, per variable and band <i>b</i>)<span class="box-kind">process</span></h3>
<p>Order 1 is a linear model of the residual of the member mean, <i>y</i> &minus; <i>x&#772;</i>. It works separately in three bands of spatial scales: <i>P<sub>b</sub></i> keeps the scales of band <i>b</i> of a field, wavelengths above 300 km, 30 to 300 km, and below 30 km, and the three parts add up to the field. Its inputs in band <i>b</i>, <i>z</i><sub><i>b</i>,<i>t</i></sub>, are band <i>b</i> of the coarse input at the point and at one and two cells to either side, of the current <i>x&#772;</i><sub><i>t</i></sub>, and of the hourly change of the input (Materials and Methods). The inputs pass through a memory filter, <i>m</i><sub><i>b</i>,<i>t</i></sub> = &phi; <i>m</i><sub><i>b</i>,<i>t</i>&minus;1</sub> + (1 &minus; &phi;) <i>z</i><sub><i>b</i>,<i>t</i></sub>, an average over past hours in which an hour <i>h</i> hours ago counts with weight proportional to &phi;<sup><i>h</i></sup>; &phi; = 0 means no memory, and with &phi; &lt; 1 an error made at one hour fades instead of growing. The corrected mean is</p>
<p class="sci-eq"><i>x&#772;</i><sup>(1)</sup><sub><i>t</i></sub> = <i>x&#772;</i><sub><i>t</i></sub> + &Sigma;<sub><i>b</i></sub> &beta;<sub><i>b</i></sub> &middot; <i>m</i><sub><i>b</i>,<i>t</i></sub>,</p>
<p>with weights &beta;<sub><i>b</i></sub> and the constant &phi; of each band fitted in panel B (Table 4). It lowers the validation RMSE of the member mean from 0.591 to 0.427; without memory (&phi; = 0 in every band) it reaches only 0.471. In Fig. 5 its correction removes part of the slanted stripes of the lagged response <i>M</i>.</p>

<figure class="jn-fig" id="fig-5">
  <picture><source media="(max-width: 600px)" srcset="{{ base_path }}/images/successive_correction/fig5_order1_narrow.png"><img src="{{ base_path }}/images/successive_correction/fig5_order1.png" alt="Member mean before and after order 1 with the truth at hour 36; Hovmöller diagrams of the order-1 correction"></picture>
  <figcaption><b>Fig. 5. Order 1.</b> (<b>A</b>) At hour 36: the member mean <i>x&#772;</i> (input, gray), <i>x&#772;</i><sup>(1)</sup> (output, blue) and the truth (black). (<b>B</b> to <b>G</b>) From <i>x&#772;</i> to <i>x&#772;</i><sup>(1)</sup>, columns as in Fig. 2. <span class="sci-dl"><a href="{{ base_path }}/images/successive_correction/fig5_order1.pdf">PDF</a></span></figcaption>
</figure>

<h3><i>n</i> &larr; 2<span class="box-kind">process</span></h3>
<p>The loop over boosting stages starts at order 2, the first order after the linear one.</p>

<h3>Order <i>n</i> (boosting stage)<span class="box-kind">process</span></h3>
<p>Order 1 is linear, but the lagged response is not: it follows the square of the waves. Each boosting stage <i>n</i> adds a nonlinear model of the residual of orders 1 to <i>n</i> &minus; 1,</p>
<p class="sci-eq"><i>x&#772;</i><sup>(<i>n</i>)</sup><sub><i>t</i></sub> = <i>x&#772;</i><sup>(<i>n</i>&minus;1)</sup><sub><i>t</i></sub> + &nu; <i>e&#770;</i><sup>(<i>n</i>)</sup><sub><i>t</i></sub>,</p>
<p>where the correction <i>e&#770;</i><sup>(<i>n</i>)</sup><sub><i>t</i></sub> comes from a random-feature network: 32 hidden units, each the positive part, max(0, &middot;), of a weighted sum of 7 local inputs (the input at 5 points, <i>x&#772;</i><sup>(<i>n</i>&minus;1)</sup><sub><i>t</i></sub> and the hourly change of the input), with weights drawn at random once and then fixed; only the output weights are fitted, by ridge regression (least squares with a small penalty on the size of the weights), on the hidden units' outputs passed through the stage's own memory filter. Each correction is added at the step &nu;, the fraction of it that is added. The stage reads its own past outputs through that filter, never the true past error, which is not known when the chain is used. The first stage lowers the validation RMSE of the member mean from 0.427 to 0.382; all stages up to <i>N</i> = 18, each added in full (&nu; = 1), lower it to 0.363 (Fig. 6). The broad slanted stripes of the lagged response <i>M</i> are gone; what remains are the fine streaks of the small-scale part <i>S</i>.</p>

<figure class="jn-fig" id="fig-6">
  <picture><source media="(max-width: 600px)" srcset="{{ base_path }}/images/successive_correction/fig6_ordern_narrow.png"><img src="{{ base_path }}/images/successive_correction/fig6_ordern.png" alt="Member mean after order 1 and after order 18 with the truth at hour 36; Hovmöller diagrams of the summed boosting corrections"></picture>
  <figcaption><b>Fig. 6. Order <i>n</i>, <i>n</i> = 2 to <i>N</i> = 18.</b> (<b>A</b>) At hour 36: <i>x&#772;</i><sup>(1)</sup> (input, gray), <i>x&#772;</i><sup>(<i>N</i>)</sup> with <i>N</i> = 18 (output, blue) and the truth (black). (<b>B</b> to <b>G</b>) From <i>x&#772;</i><sup>(1)</sup> to <i>x&#772;</i><sup>(<i>N</i>)</sup>, columns as in Fig. 2; the change is the sum of the 17 stage corrections &nu;<i>e&#770;</i><sup>(<i>n</i>)</sup>. The streaks left in G are the small-scale part <i>S</i>. Movie 1 shows the stages one at a time. <span class="sci-dl"><a href="{{ base_path }}/images/successive_correction/fig6_ordern.pdf">PDF</a></span></figcaption>
</figure>

<h3><i>n</i> &lt; <i>N</i> ?<span class="box-kind">decision</span></h3>
<p>If <i>n</i> &lt; <i>N</i>, the counter moves to <i>n</i> + 1 and the next stage corrects the output of this one. <i>N</i> = 18 and &nu; = 1 were chosen on the validation runs (panel B, Table 5). Movie 1 runs this loop for the example: <i>M</i>'s stripes fade over the first stages, <i>S</i>'s streaks stay, and later stages change the error little.</p>

<figure class="jn-fig jn-movie" id="movie-orders">
  <canvas role="img" aria-label="Animation over the boosting stages: error map of the corrected member mean, and the corrected mean against the truth at hour 36"></canvas>
  <div class="jn-movie-ctl"><button type="button">Play</button><input type="range" aria-label="Order shown in movie 1"><span></span></div>
  <figcaption><b>Movie 1. The loop over orders, <i>n</i> = 1 to 18.</b> (<b>A</b>) Error of the corrected member mean, <i>x&#772;</i><sup>(<i>n</i>)</sup> &minus; <i>y</i>, for the first validation run, on the difference color scale of the figures (blue, too low; vermilion, too high). (<b>B</b>) At hour 36 (triangle in A): <i>x&#772;</i><sup>(<i>n</i>)</sup> (blue), the previous order <i>x&#772;</i><sup>(<i>n</i>&minus;1)</sup> (gray, from frame 2 on) and the truth (black). The label gives the RMSE of this run after order <i>n</i>; frame 1 is order 1, the input of the loop.</figcaption>
</figure>

<h3>Perturbation scaling<span class="box-kind">process</span></h3>
<p>Each member gets its own perturbation back, rescaled band by band:</p>
<p class="sci-eq"><i>y</i><sub><i>k</i>,<i>t</i></sub> = <i>x&#772;</i><sup>(<i>N</i>)</sup><sub><i>t</i></sub> + &Sigma;<sub><i>b</i></sub> &alpha;<sub><i>b</i></sub>(lead) &middot; <i>P<sub>b</sub></i> <i>d</i><sub><i>k</i>,<i>t</i></sub>,</p>
<p>where lead is the forecast hour <i>t</i> and &alpha;<sub><i>b</i></sub>(lead) is one factor per band and hour, fitted in panel B (Table 6). The perturbations of the 8 members sum to zero, so the mean of the output members is <i>x&#772;</i><sup>(<i>N</i>)</sup> itself; the scaling sets only how far the members spread around it. Each output member, a sample, has a larger RMSE than the corrected mean (0.522 for member 1 against 0.363; Fig. 7), but the ensemble as a whole scores better than the corrected mean alone (Table 7). The perturbations keep order 0's defect (Table 3): rescaling changes the size of a perturbation and leaves its hour-to-hour behavior as it was.</p>

<figure class="jn-fig" id="fig-7">
  <picture><source media="(max-width: 600px)" srcset="{{ base_path }}/images/successive_correction/fig7_scaling_narrow.png"><img src="{{ base_path }}/images/successive_correction/fig7_scaling.png" alt="The output members around the corrected mean and the truth at hour 36; Hovmöller diagrams of members 1 and 2 built from the corrected mean"></picture>
  <figcaption><b>Fig. 7. Perturbation scaling.</b> (<b>A</b>) At hour 36: the output members <i>y<sub>k</sub></i> (blue, thin), their mean <i>x&#772;</i><sup>(<i>N</i>)</sup> (input, dark blue) and the truth (black). (<b>B</b> to <b>G</b>) Member 1 and (<b>H</b> to <b>M</b>) member 2, from <i>x&#772;</i><sup>(<i>N</i>)</sup> (input) to <i>y<sub>k</sub></i> (output), columns as in Fig. 2; the change is the member's rescaled perturbation, &Sigma;<sub><i>b</i></sub> &alpha;<sub><i>b</i></sub> <i>P<sub>b</sub></i> <i>d<sub>k</sub></i>. <span class="sci-dl"><a href="{{ base_path }}/images/successive_correction/fig7_scaling.pdf">PDF</a></span></figcaption>
</figure>

<h3>Write the 8 members<span class="box-kind">input / output</span></h3>
<p>The 8 members <i>y</i><sub><i>k</i>,<i>t</i></sub> of hour <i>t</i> are written out. Figure 8 compares what is written with what order 0 produced: each member keeps its own detail, while the member mean, now <i>x&#772;</i><sup>(<i>N</i>)</sup>, has lost most of the lagged response's error (validation RMSE of the member mean 0.591 for order 0, 0.363 written).</p>

<figure class="jn-fig" id="fig-8">
  <picture><source media="(max-width: 600px)" srcset="{{ base_path }}/images/successive_correction/fig8_write_narrow.png"><img src="{{ base_path }}/images/successive_correction/fig8_write.png" alt="Order-0 members and written members with the truth at hour 36; Hovmöller diagrams from order 0 to the written members for member 1 and the member mean"></picture>
  <figcaption><b>Fig. 8. Write the members: the whole chain.</b> At hour 36: (<b>A</b>) the order-0 members <i>x<sub>k</sub></i> and (<b>B</b>) the written members <i>y<sub>k</sub></i> (blue, thin), with the truth (black). (<b>C</b> to <b>H</b>) Member 1, from <i>x<sub>k</sub></i> (input) to <i>y<sub>k</sub></i> (output), and (<b>I</b> to <b>N</b>) the member mean, from <i>x&#772;</i> to <i>x&#772;</i><sup>(<i>N</i>)</sup>, columns as in Fig. 2. <span class="sci-dl"><a href="{{ base_path }}/images/successive_correction/fig8_write.pdf">PDF</a></span></figcaption>
</figure>

<h3><i>t</i> &lt; 72 ?<span class="box-kind">decision</span></h3>
<p>If <i>t</i> &lt; 72, the counter moves to <i>t</i> + 1 and the chain reads the next hour. The memory filters keep their state from hour to hour; together with the lags and order 0's own uncorrected previous hours (open loop), they carry information from hour <i>t</i> &minus; 1 to hour <i>t</i>. Movie 2 runs this loop for the example, hour by hour, through the main boxes.</p>

<figure class="jn-fig jn-movie" id="movie-hours">
  <canvas role="img" aria-label="Animation over the hours of one run: order-0 members and their mean, the corrected mean, and the output members, each against the truth"></canvas>
  <div class="jn-movie-ctl"><button type="button">Play</button><input type="range" aria-label="Hour shown in movie 2"><span></span></div>
  <figcaption><b>Movie 2. The loop over hours, <i>t</i> = 0 to 72, for the first validation run.</b> (<b>A</b>) Order 0 and Split: the 8 members <i>x</i><sub><i>k</i>,<i>t</i></sub> (light blue) and their mean <i>x&#772;</i><sub><i>t</i></sub> (blue). (<b>B</b>) Orders 1 to 18: <i>x&#772;</i><sub><i>t</i></sub> (gray) and the corrected mean <i>x&#772;</i><sup>(<i>N</i>)</sup><sub><i>t</i></sub> (blue). (<b>C</b>) Perturbation scaling: the output members <i>y</i><sub><i>k</i>,<i>t</i></sub> (light blue) around <i>x&#772;</i><sup>(<i>N</i>)</sup><sub><i>t</i></sub> (blue). The truth <i>y</i> is black in every panel.</figcaption>
</figure>

<h3>End<span class="box-kind">start / end</span></h3>
<p>The run's output is complete: 8 members for each of its hours.</p>

<h2>Fitting: once, in this order (Fig. 1B)</h2>
<p>All parts are fitted once, before the chain is used, in the order in which they run.</p>

<h3>Start<span class="box-kind">start / end</span></h3>
<p>Fitting needs the coarse input and the truth of every run in the three sets.</p>

<h3>Generate CorrDiff &mu;_v2, 8 members, on the training and validation runs, each member run forward on its own uncorrected hours<span class="box-kind">model run as one block</span></h3>
<p>Order 0 is run on every training and validation run, each member run forward hour by hour on its own uncorrected previous hours (open loop, so this can be done once, before any order is fitted): on real forecasts the already trained CorrDiff &mu;_v2, in the example the toy generator. (For convenience the example also generates the test-run members here, from their input only; the chart generates them in its last box, where they are first needed.) CorrDiff &mu;_v2 was trained on the training runs, so its members there are in-sample, produced by a model fitted on those same runs, and closer to the truth than on new runs. The example's generator is likewise fitted on all training runs. Corrections fitted on in-sample members may come out too small. The chain is nevertheless fitted on the in-sample members, as it will be on real forecasts, where the generator is used as trained. To measure the effect, the toy generator was refitted 5 times, each time without one group of training runs, which gives out-of-fold members, and order 1 was fitted once on each kind (Fig. 9). On the same training runs the RMSE of the member mean is 0.5970 in-sample against 0.6043 out-of-fold; on the validation runs the correction of the in-sample fit is 1.3% smaller in RMS (root-mean-square) size overall and 5.5% smaller below 30 km, and the validation RMSE after order 1 is 0.4273 against 0.4271. The effect is small here because the toy generator has few fitted coefficients; a neural network with many more fitted parameters may fit its training runs more closely, and then the effect on real forecasts would be larger; the validation runs will show it.</p>

<figure class="jn-fig" id="fig-9">
  <picture><source media="(max-width: 600px)" srcset="{{ base_path }}/images/successive_correction/fig9_insample_narrow.png"><img src="{{ base_path }}/images/successive_correction/fig9_insample.png" alt="Order-1 outputs fitted on in-sample and on out-of-fold members, nearly identical, at hour 36; Hovmöller diagrams of both corrections"></picture>
  <figcaption><b>Fig. 9. In-sample members.</b> (<b>A</b>) At hour 36: the member mean <i>x&#772;</i> (gray), <i>x&#772;</i><sup>(1)</sup> from order 1 fitted on in-sample members (blue) and on out-of-fold members (vermilion, dashed), and the truth (black); the two outputs nearly coincide. (<b>B</b> to <b>G</b>) Order 1 fitted on in-sample and (<b>H</b> to <b>M</b>) on out-of-fold members, applied to the same validation run, columns as in Fig. 2; the RMS size of each correction is printed in C and I. <span class="sci-dl"><a href="{{ base_path }}/images/successive_correction/fig9_insample.pdf">PDF</a></span></figcaption>
</figure>

<h3>Split every hour into <i>x&#772;</i> and <i>d<sub>k</sub></i><span class="box-kind">process</span></h3>
<p>As in use, every hour of every run is split into the member mean and the perturbations.</p>

<h3>Fit order 1 on <i>y</i> &minus; <i>x&#772;</i><span class="box-kind">process</span></h3>
<p>Order 1 is fitted to the residual of the member mean, <i>y</i> &minus; <i>x&#772;</i>, on the training runs, not to the residual of each member. Figure 10 shows why. Fitted by squared error to the residual of every member, <i>y</i> &minus; <i>x<sub>k</sub></i>, with the member itself among its inputs, the same model learns to remove the member: its weight on the member is between &minus;1.03 and &minus;0.99 in every band, so each corrected member is rebuilt from the coarse input alone. The alternative is order 1 fitted to the residual of the mean, with the perturbations rescaled afterwards by an &alpha; fitted as in panel B (the chain without boosting stages). Over all validation runs, correcting each member keeps 23% of the members' spread, the typical difference of the members from their mean (Materials and Methods), against 82% for correcting the mean, and its fair CRPS is worse, 0.267 against 0.213. Member 1's RMSE is lower after correcting each member, 0.462 against 0.607 after correcting the mean; this reflects the collapse, since a member without its perturbation lies close to the mean. Figure 10 prints the values of its one run, which are close to these (member 1's RMSE after correcting each member rounds to 0.462 on that run too). Fitted to the mean, order 1 also gives <i>x&#772;</i> a strongly negative weight (&minus;0.80 to &minus;0.94, Table 4): it partly replaces the member mean by its own estimate from the input and its memory. For the mean this is harmless, because the perturbations are added back afterwards; applied to each member, a weight near &minus;1 removes the member's own detail.</p>
<p>The constant &phi; of each band is chosen from {0, 0.3, 0.5, 0.7, 0.8, 0.85, 0.9, 0.95} by out-of-fold error: the training runs form 5 groups, each group is predicted by weights fitted on the other groups, and the &phi; with the lowest error on these predictions is kept (Table 4). Every training run's correction is computed the same way, out-of-fold, so that the next order learns from errors that were not fitted already: an in-sample correction would make the residual on the training runs look smaller than it is on new runs. Memory helps at large scales (&phi; = 0.8 and 0.85); below 30 km the out-of-fold error is lowest without it (&phi; = 0).</p>

<figure class="jn-fig" id="fig-10">
  <picture><source media="(max-width: 600px)" srcset="{{ base_path }}/images/successive_correction/fig10_trap_narrow.png"><img src="{{ base_path }}/images/successive_correction/fig10_trap.png" alt="Members after correcting each member, collapsed, and after correcting the mean, spread out, at hour 36; Hovmöller diagrams of both variants"></picture>
  <figcaption><b>Fig. 10. Correct the mean, not each member.</b> At hour 36, the 8 members (blue, thin) and the truth (black) after (<b>A</b>) order 1 fitted to the residual of every member and applied to each, and (<b>B</b>) order 1 fitted to the residual of the mean, with the perturbations rescaled. (<b>C</b> to <b>H</b>) Member 1 and (<b>I</b> to <b>N</b>) the member mean for each-member correction; (<b>O</b> to <b>T</b>) member 1 and (<b>U</b> to <b>Z</b>) the member mean for mean-only correction; columns as in Fig. 2, inputs are order 0. The notes in E and Q give this run's spread and fair CRPS before and after. <span class="sci-dl"><a href="{{ base_path }}/images/successive_correction/fig10_trap.pdf">PDF</a></span></figcaption>
</figure>

<div class="tbl" id="table-4">
<p class="jn-tabcap"><b>Table 4. Order 1 per scale band.</b> &phi; chosen out-of-fold on the training runs; validation RMSE of the band's part of the member mean before (<i>x&#772;</i>) and after order 1 (<i>x&#772;</i><sup>(1)</sup>); the weight on <i>x&#772;</i> shows that order 1 damps the member mean and rebuilds the field from the input and its memory.</p>
<table class="jn-table">
<thead><tr><th>band</th><th class="num">&phi;</th><th class="num">weight on <i>x&#772;</i></th><th class="num">RMSE <i>x&#772;</i></th><th class="num">RMSE <i>x&#772;</i><sup>(1)</sup></th></tr></thead>
<tbody>
<tr><td>above 300 km</td><td class="num">0.8</td><td class="num">&minus;0.80</td><td class="num">0.369</td><td class="num">0.182</td></tr>
<tr><td>30 to 300 km</td><td class="num">0.85</td><td class="num">&minus;0.89</td><td class="num">0.326</td><td class="num">0.234</td></tr>
<tr><td>below 30 km</td><td class="num">0</td><td class="num">&minus;0.94</td><td class="num">0.328</td><td class="num">0.308</td></tr>
</tbody>
</table>
</div>

<h3><i>n</i> &larr; 2<span class="box-kind">process</span></h3>
<p>The stages are fitted one after another, starting with order 2, each on what the orders before it miss.</p>

<h3>For each step &nu; of a grid: fit order <i>n</i> on the out-of-fold residual of order <i>n</i> &minus; 1<span class="box-kind">process</span></h3>
<p>Stage <i>n</i> is fitted on the training runs to the residual <i>y</i> &minus; <i>x&#772;</i><sup>(<i>n</i>&minus;1)</sup>, where <i>x&#772;</i><sup>(<i>n</i>&minus;1)</sup> is out-of-fold. Its random input weights are drawn once; its output weights and its &phi; are fitted as for order 1, with the stage run on its own past outputs, exactly as in use. It is then added with step &nu;. The grid of steps here has two values, &nu; = 1 (each correction added in full) and &nu; = 0.3; for each, up to 30 orders were fitted.</p>

<h3>Validation error still falling?<span class="box-kind">decision</span></h3>
<p>After each stage the validation RMSE of the member mean is computed. The chart stops at the first rise; the example instead fits all 30 orders for each step and keeps the lowest, which also shows what happens after it (Table 5). With &nu; = 1 the validation error falls until order 18 and then rises, and the size of each stage's correction shrinks only until order 10 and then grows. The out-of-fold training error, the RMSE of the out-of-fold corrected mean on the training runs, is lowest at order 8 (0.3728) and then rises, to 0.4897 at order 30, far above the validation RMSE there (0.3906). A likely reason: out-of-fold corrections keep the training residual as large as it would be on new runs, but they come from 5 fits, one per fold, that differ slightly. On the training runs the residual that the next stage sees therefore contains, besides the real error, the differences between these fits; the stage learns part of them and adds them back, and with full steps the following stages repeat this, so the training error grows. On the validation runs every correction comes from the one fit on all training runs, so these differences do not arise there. The effect is largest above 300 km, where the corrections are large (order 1 alone lowers that band's validation RMSE from 0.369 to 0.182, Table 4) and the error left at the end is small (0.067), so slight differences between the fold fits are large compared with it. With &nu; = 0.3 each stage adds only part of its correction: the corrections shrink by about a factor of ten from order 2 to order 30, with their smallest at order 25, the validation error is still falling slowly at order 30, and the out-of-fold training error stays close to it (0.3755 against 0.3677 at order 30). Within 30 orders the small step behaves much better, although 30 orders cannot show that it converges.</p>

<h3><i>N</i>, &nu; &larr; lowest validation error (all &nu;)<span class="box-kind">process</span></h3>
<p>The lowest validation RMSE over both steps is kept: &nu; = 1 with <i>N</i> = 18 (0.4273 after order 1, 0.3635 after order 18). The small step at <i>N</i> = 30 is within 1.2% of it.</p>

<div class="tbl" id="table-5">
<p class="jn-tabcap"><b>Table 5. Choosing <i>N</i> and &nu; on the validation runs.</b> RMSE of the member mean; &ldquo;out-of-fold training&rdquo; is the error of the out-of-fold corrections on the training runs; correction size is the RMS of a stage's added correction, &nu;<i>e&#770;</i><sup>(<i>n</i>)</sup>, on the validation runs.</p>
<table class="jn-table">
<thead><tr><th>step &nu;</th><th class="num">lowest validation RMSE (at order)</th><th class="num">validation RMSE at order 30</th><th class="num">lowest out-of-fold training RMSE (at order)</th><th class="num">correction size, order 2 &rarr; 30</th><th class="num">smallest correction at order</th></tr></thead>
<tbody>
<tr><td>1</td><td class="num">0.3635 (18)</td><td class="num">0.3906</td><td class="num">0.3728 (8)</td><td class="num">0.1827 &rarr; 0.1034</td><td class="num">10</td></tr>
<tr><td>0.3</td><td class="num">0.3677 (30)</td><td class="num">0.3677</td><td class="num">0.3747 (22)</td><td class="num">0.0548 &rarr; 0.0056</td><td class="num">25</td></tr>
</tbody>
</table>
</div>

<h3>Fit &alpha;<sub><i>b</i></sub>(lead) per variable and band by fair CRPS on the training runs<span class="box-kind">process</span></h3>
<p>For each band and each forecast hour, &alpha;<sub><i>b</i></sub> minimizes the fair CRPS of the band's part of the members, <i>P<sub>b</sub></i>&thinsp;<i>x&#772;</i><sup>(<i>N</i>)</sup> + &alpha;<sub><i>b</i></sub> <i>P<sub>b</sub></i>&thinsp;<i>d<sub>k</sub></i>, against the band's part of the truth on the training runs, with the out-of-fold <i>x&#772;</i><sup>(<i>N</i>)</sup>. Each band is scored on its own, because the score of the whole field fixes only the total spread at each point, not how it divides among the bands. Within one band the score is convex in &alpha;, so it has a single minimum, and the fitted factors change smoothly with the hour (Table 6). &alpha; shrinks the large-scale perturbations most; below 30 km it stays near 1, because order 0's fine detail already has about the right size there and no order can predict it.</p>
<p>The spread-to-error ratio checks the result: the members' spread divided by the RMSE of their mean. For these members, the corrected mean plus perturbations centered on it, a ratio of 1 means the spread matches the error (for order 0's members, which are averaged into their own mean, the ideal is 0.94 instead; Materials and Methods). On the training runs, where &alpha; was fitted, the ratio is 1.02, close to 1 although a fair-CRPS fit can lean higher (for a Gaussian error the fair CRPS is lowest at a ratio of 1.23; Materials and Methods). On the validation runs it is 1.10 overall but 2.54 above 300 km. The reason is the rise of the out-of-fold training error described above: &alpha; is fitted on the training runs so that the members' spread matches the error of the out-of-fold <i>x&#772;</i><sup>(<i>N</i>)</sup> there, and above 300 km that training error (0.142) is about twice the validation error (0.067). The members' spread is about the same on both sets of runs, so the training ratio in that band, 1.19, becomes about 1.19 &times; 0.142/0.067 &asymp; 2.5 on the validation runs.</p>

<div class="tbl" id="table-6">
<p class="jn-tabcap"><b>Table 6. Perturbation scale &alpha;<sub><i>b</i></sub>(lead) per band.</b> Mean, minimum and maximum over the 73 hours; mean change from one hour to the next; spread-to-error ratio of the output members on the training runs (where &alpha; was fitted) and on the validation runs.</p>
<table class="jn-table">
<thead><tr><th>band</th><th class="num">&alpha; mean</th><th class="num">&alpha; range</th><th class="num">hourly change</th><th class="num">spread/error, training</th><th class="num">spread/error, validation</th></tr></thead>
<tbody>
<tr><td>above 300 km</td><td class="num">0.47</td><td class="num">0.35&ndash;0.49</td><td class="num">0.0063</td><td class="num">1.19</td><td class="num">2.54</td></tr>
<tr><td>30 to 300 km</td><td class="num">0.69</td><td class="num">0.65&ndash;0.72</td><td class="num">0.0062</td><td class="num">1.09</td><td class="num">1.16</td></tr>
<tr><td>below 30 km</td><td class="num">0.96</td><td class="num">0.94&ndash;0.97</td><td class="num">0.0056</td><td class="num">0.95</td><td class="num">0.97</td></tr>
</tbody>
</table>
</div>

<h3>Score the validation runs (error, CRPS, spread)<span class="box-kind">process</span></h3>
<p>With every part fixed, the chain is scored on the validation runs (Table 7), with the three scores named in the box: the error (RMSE), the fair CRPS and the spread (as the spread-to-error ratio). The RMSE of the member mean falls from order 0 to order 1 to order 18. The output members have the lowest fair CRPS: 0.176, against 0.292 for the order-0 members, 0.248 for the corrected mean used alone as a single estimate, and 0.185 for the corrected mean plus the unscaled perturbations (&alpha; = 1).</p>

<h3>Test runs: generate 8 members, score once<span class="box-kind">input / output</span></h3>
<p>The test runs are read once, after everything else is fixed; no choice depends on them. They repeat the validation results (Table 7): the RMSE of the member mean falls from 0.619 (order 0) to 0.439 (order 1) and 0.370 (order 18), the fair CRPS from 0.302 to 0.178, and the band above 300 km again has too much spread (spread-to-error ratio 2.46). The hour-to-hour correlations repeat those of the validation runs (Table 3).</p>

<div class="tbl" id="table-7">
<p class="jn-tabcap"><b>Table 7. Scores on the validation runs and, once, on the test runs.</b> RMSE of one member or of the member mean; fair CRPS of the members (of a single estimate, its mean absolute error); spread-to-error ratio of the members.</p>
<table class="jn-table">
<thead><tr><th>after box</th><th>field</th><th class="num">validation</th><th class="num">test</th></tr></thead>
<tbody>
<tr><td>Read hour <i>t</i></td><td>RMSE, input on the 3-km points</td><td class="num">0.621</td><td class="num">0.664</td></tr>
<tr><td>Order 0</td><td>RMSE, member 1</td><td class="num">0.797</td><td class="num">0.804</td></tr>
<tr><td>Split</td><td>RMSE, member mean <i>x&#772;</i></td><td class="num">0.591</td><td class="num">0.619</td></tr>
<tr><td>Order 1</td><td>RMSE, <i>x&#772;</i><sup>(1)</sup></td><td class="num">0.427</td><td class="num">0.439</td></tr>
<tr><td>Order <i>N</i> = 18</td><td>RMSE, <i>x&#772;</i><sup>(<i>N</i>)</sup></td><td class="num">0.363</td><td class="num">0.370</td></tr>
<tr><td>Perturbation scaling</td><td>RMSE, member 1</td><td class="num">0.522</td><td class="num">0.526</td></tr>
<tr><td>Read hour <i>t</i></td><td>fair CRPS, input alone</td><td class="num">0.399</td><td class="num">0.416</td></tr>
<tr><td>Order 0</td><td>fair CRPS, members</td><td class="num">0.292</td><td class="num">0.302</td></tr>
<tr><td>Order <i>N</i> = 18</td><td>fair CRPS, <i>x&#772;</i><sup>(<i>N</i>)</sup> alone</td><td class="num">0.248</td><td class="num">0.250</td></tr>
<tr><td>Perturbation scaling</td><td>fair CRPS, output members</td><td class="num">0.176</td><td class="num">0.178</td></tr>
<tr><td>Order 0</td><td>spread/error, members</td><td class="num">0.96</td><td class="num">0.91</td></tr>
<tr><td>Perturbation scaling</td><td>spread/error, output members</td><td class="num">1.10</td><td class="num">1.08</td></tr>
<tr><td>Perturbation scaling</td><td>spread/error, above 300 km</td><td class="num">2.54</td><td class="num">2.46</td></tr>
</tbody>
</table>
</div>

<h3>End<span class="box-kind">start / end</span></h3>
<p>The example runs every box of Fig. 1 and supports the design: correct the mean, keep the perturbations, choose <i>N</i> and &nu; on runs not used for fitting. It also shows three things to watch on real forecasts. The in-sample effect of order 0's training runs can be larger for a neural network than for the toy generator. &alpha; inherits any gap between the out-of-fold training error and the validation error, band by band, as above 300 km here. And the scaling sets the size of the perturbations but leaves their behavior in time as order 0 made it: order 0's defect reaches the written members.</p>

<h2>Materials and Methods</h2>
<h3>The example's truth and input</h3>
<p>The line has 288 points 3 km apart (period 864 km); a coarse cell is the average of 9 points. At position <i>s</i> and hour <i>t</i>, <i>L</i>(<i>s</i>, <i>t</i>) = &Sigma;<sub><i>j</i>=1</sub><sup>3</sup> &kappa;<sub><i>j</i></sub> cos(2&pi;<i>j</i>(<i>s</i> &minus; <i>c<sub>j</sub> t</i>)/864 km + &theta;<sub><i>j</i></sub>), with amplitude &kappa;<sub><i>j</i></sub> uniform between 0.6/&radic;<i>j</i> and 1.4/&radic;<i>j</i>, speed <i>c<sub>j</sub></i> uniform between &minus;25 and 25 km h<sup>&minus;1</sup> and phase &theta;<sub><i>j</i></sub> uniform. With <i>g</i> = max(<i>L</i>, 0)<sup>2</sup>, <i>M<sub>t</sub></i> = <i>a M</i><sub><i>t</i>&minus;1</sub> + (1 &minus; <i>a</i>) <i>g<sub>t</sub></i>, <i>a</i> = e<sup>&minus;1/6</sup>, <i>M</i><sub>0</sub> = <i>g</i><sub>0</sub>. <i>S</i> = (0.15 + 0.35 max(<i>L</i>, 0)) &zeta;, where &zeta; is a Gaussian random field (random values along the line with a normal distribution and a prescribed distribution of variance over wavelengths) with unit variance and equal power at wavenumbers (wavelengths per period) 20 to 60, renewed as &zeta;<sub><i>t</i></sub> = 0.7 &zeta;<sub><i>t</i>&minus;1</sub> + (1 &minus; 0.7<sup>2</sup>)<sup>1/2</sup> &xi;<sub><i>t</i></sub> with fresh random fields &xi;<sub><i>t</i></sub>. The coarse input is <i>u</i> = cell average of (<i>L</i> + 0.5 <i>g</i>) + &epsilon;, where the cell error &epsilon; has standard deviation 0.1 and keeps a fraction 0.9 of itself from one hour to the next. The bands are: above 300 km, wavenumbers 0 to 2; 30 to 300 km, 3 to 28; below 30 km, 29 to 144; <i>P<sub>b</sub></i> keeps the Fourier coefficients of band <i>b</i>, the amplitudes of the cosine and sine waves that make up the field.</p>
<h3>Order 0</h3>
<p><i>A</i> = <i>C<sub>yu</sub></i>(<i>C<sub>uu</sub></i> + &lambda;<i>I</i>)<sup>&minus;1</sup> and <i>q</i> = &lang;<i>y</i>&rang; &minus; <i>A</i>&lang;<i>u</i>&rang;, from the training-run means &lang;&middot;&rang; and covariances <i>C</i> of the fine truth and the coarse input (<i>A</i> maps the 32 cell values of <i>u</i> to the 288 points; <i>I</i> is the identity matrix), with &lambda; = 10<sup>&minus;3</sup> times the mean variance of the input. The random part &eta;<sub><i>k</i></sub> has, at each wavenumber, the power of the training residual <i>y</i> &minus; (<i>A u</i> + <i>q</i>) and evolves in time as a first-order autoregressive process (each hour keeps a fraction &rho; of the previous hour's value and adds fresh noise); &rho; is the residual's hour-to-hour correlation at that wavenumber, multiplied by a factor below 1 in each band (the stated defect), smallest at the finest scales. The same random numbers are used for every refit.</p>
<h3>Order 1 and the boosting stages</h3>
<p>Order 1's inputs at each point are the coarse input interpolated to the point and to the points one and two cells to either side (5 values), the field being corrected, the hourly change of the interpolated input (zero at the first hour) and a constant (in the largest-scale band only), each projected on band <i>b</i>. A stage's inputs are 7 local values, standardized to zero mean and unit variance (the 5 input values, <i>x&#772;</i><sup>(<i>n</i>&minus;1)</sup> and the hourly change of the input); with <b>r</b> the vector of these inputs, its 32 hidden units are max(0, <b>w</b><sub><i>i</i></sub>&middot;<b>r</b> + <i>o<sub>i</sub></i>) with weight vectors <b>w</b><sub><i>i</i></sub> and offsets <i>o<sub>i</sub></i> drawn once from a normal distribution, plus a constant. In both, with <i>z<sub>t</sub></i> the inputs (order 1) or the hidden units' outputs (a stage) at hour <i>t</i>, the correction is <i>e&#770;<sub>t</sub></i> = &beta;&middot;<i>m<sub>t</sub></i> with <i>m<sub>t</sub></i> = &phi;<i>m</i><sub><i>t</i>&minus;1</sub> + (1 &minus; &phi;)<i>z<sub>t</sub></i> and <i>m</i><sub>0</sub> = <i>z</i><sub>0</sub>. This equals the recursion <i>e&#770;<sub>t</sub></i> = &phi;<i>e&#770;</i><sub><i>t</i>&minus;1</sub> + (1 &minus; &phi;)&beta;&middot;<i>z<sub>t</sub></i> run on its own outputs, so for a fixed &phi; the fit is a ridge regression on the filtered inputs (penalty 10<sup>&minus;3</sup> times the mean, over inputs, of the sum of squares of a filtered input); &phi; is chosen from {0, 0.3, 0.5, 0.7, 0.8, 0.85, 0.9, 0.95} by out-of-fold error over 5 groups of runs (run number modulo 5).</p>
<h3>Scores</h3>
<p>RMSE is the root of the mean squared difference from the truth over all points, hours and runs. The fair CRPS of <i>K</i> members <i>x</i><sub>1</sub>, &hellip;, <i>x<sub>K</sub></i> against the truth <i>y</i> at one point is (1/<i>K</i>) &Sigma;<sub><i>k</i></sub> |<i>x<sub>k</sub></i> &minus; <i>y</i>| &minus; &Sigma;<sub><i>i</i>&lt;<i>j</i></sub> |<i>x<sub>i</sub></i> &minus; <i>x<sub>j</sub></i>| / (<i>K</i>(<i>K</i> &minus; 1)), averaged over points, hours and runs; the first term rewards members close to the truth, the second rewards spread. Dividing the pair sum by <i>K</i>(<i>K</i> &minus; 1) rather than <i>K</i><sup>2</sup> makes its expected value the score of the distribution the members are drawn from, whatever the number of members; the plain ensemble CRPS, with <i>K</i><sup>2</sup>, penalizes small ensembles. For one estimate (<i>K</i> = 1) only the first term is kept: the mean absolute error. The spread is the square root of the mean, over points, hours and runs, of the members' variance about their mean, with the sum of squares divided by <i>K</i> &minus; 1; the spread-to-error ratio divides it by the RMSE of the member mean. For the order-0 members, independent draws averaged into their mean, the ideal ratio is (<i>K</i>/(<i>K</i> + 1))<sup>1/2</sup> = 0.94 (validation: 0.96); for the output members, the corrected mean plus perturbations centered on it, it is 1. A fair-CRPS fit of &alpha; can lean above 1. With the truth at a Gaussian distance &delta; ~ N(0, 1) from the corrected mean and members at &sigma;(&omega;<sub><i>k</i></sub> &minus; &omega;&#772;) from it, &omega;<sub><i>k</i></sub> ~ N(0, 1) independent with mean &omega;&#772;, the expected fair CRPS is (2/&pi;)<sup>1/2</sup>[((<i>K</i> &minus; 1)&sigma;<sup>2</sup>/<i>K</i> + 1)<sup>1/2</sup> &minus; &sigma;/2<sup>1/2</sup>], since <i>x<sub>k</sub></i> &minus; <i>y</i> and <i>x<sub>i</sub></i> &minus; <i>x<sub>j</sub></i> are Gaussian with variances (<i>K</i> &minus; 1)&sigma;<sup>2</sup>/<i>K</i> + 1 and 2&sigma;<sup>2</sup>. It is smallest at &sigma; = <i>K</i>/[(<i>K</i> &minus; 1)(<i>K</i> &minus; 2)]<sup>1/2</sup>, and &sigma; is the spread-to-error ratio: 1.23 for <i>K</i> = 8. The hour-to-hour correlation of a pattern is the correlation along the line between a band's field at consecutive hours, averaged over hours and runs.</p>

<h2>Glossary</h2>
<table class="jn-table">
<tbody>
<tr><td>downscaling</td><td>estimating a fine-grid field from a coarse-grid forecast</td></tr>
<tr><td>WRF, d01, d03</td><td>Weather Research and Forecasting model; its coarse outer grid (27 km) and fine inner grid (3 km)</td></tr>
<tr><td>GFS, steering wind</td><td>Global Forecast System; the large-scale wind that moves weather systems along</td></tr>
<tr><td>member, ensemble</td><td>one equally likely sample of the fine field; the set of members of one hour</td></tr>
<tr><td>CorrDiff, CorrDiff &mu;_v2</td><td>a generative downscaling model: a regression network for the mean plus a diffusion model for the detail (<span class="cite">1</span>); the CorrDiff variant used here, which starts from the Ens-CGP mean &mu;<sub><i>t</i></sub> instead of a regression network and whose members read their own two previous hours (&ldquo;v2&rdquo; is its version label)</td></tr>
<tr><td>Ens-CGP mean &mu;<sub><i>t</i></sub></td><td>mean of an Ensemble-Conditional Gaussian Process: the fine fields' mean given the coarse forecast, both treated as jointly Gaussian, statistics from a large set of training hours (<span class="cite">2</span>)</td></tr>
<tr><td><i>u<sub>t</sub></i>, <i>y</i></td><td>coarse input at hour <i>t</i>; fine truth (no member index)</td></tr>
<tr><td>error, residual</td><td>estimate minus truth; truth minus estimate, what a correction has to add</td></tr>
<tr><td><i>L</i>, <i>M</i>, <i>S</i>, <i>g</i></td><td>the example's truth <i>y</i> = <i>L</i> + <i>M</i> + <i>S</i>: large travelling waves; lagged response to the forcing <i>g</i> = max(<i>L</i>, 0)<sup>2</sup>; small-scale part</td></tr>
<tr><td><i>x</i><sub><i>k</i>,<i>t</i></sub>, <i>x&#772;</i><sub><i>t</i></sub>, <i>d</i><sub><i>k</i>,<i>t</i></sub></td><td>order-0 member <i>k</i> at hour <i>t</i>; mean of the members; perturbation <i>x</i><sub><i>k</i>,<i>t</i></sub> &minus; <i>x&#772;</i><sub><i>t</i></sub></td></tr>
<tr><td>order <i>n</i>, <i>x&#772;</i><sup>(<i>n</i>)</sup><sub><i>t</i></sub></td><td>level <i>n</i> of the successive correction (0: generator, 1: linear model, 2 to <i>N</i>: boosting stages); the member mean after order <i>n</i></td></tr>
<tr><td>open loop, closed loop</td><td>open loop: order 0 builds each member's next hour from its own uncorrected previous hours, never from the corrected output, so the corrections do not enter order 0's step in time (used here); closed loop: the corrected output would be fed back instead</td></tr>
<tr><td>boosting stage, <i>e&#770;</i><sup>(<i>n</i>)</sup><sub><i>t</i></sub>, &nu;, <i>N</i></td><td>one order from 2 on, a model of the residual left by the orders before it; its correction; the fraction of it added; the last order</td></tr>
<tr><td>random-feature network</td><td>a network with one layer of hidden units whose input weights are drawn at random and fixed; only its output weights are fitted</td></tr>
<tr><td>ridge regression</td><td>least squares with a small penalty on the size of the weights</td></tr>
<tr><td>memory filter <i>m<sub>t</sub></i>, memory constant &phi;</td><td><i>m<sub>t</sub></i> = &phi;<i>m</i><sub><i>t</i>&minus;1</sub> + (1 &minus; &phi;)<i>z<sub>t</sub></i>, an average over past hours; &phi; &lt; 1, so a past error fades as &phi;<sup><i>h</i></sup> after <i>h</i> hours</td></tr>
<tr><td><i>z</i><sub><i>b</i>,<i>t</i></sub>, &beta;<sub><i>b</i></sub></td><td>inputs of order 1 in band <i>b</i>; their fitted weights</td></tr>
<tr><td>scale band, <i>P<sub>b</sub></i>, wavenumber</td><td>a range of wavelengths (above 300, 30 to 300, below 30 km); keeps that range of a field; number of wavelengths per period of the line</td></tr>
<tr><td>&alpha;<sub><i>b</i></sub>(lead), lead</td><td>perturbation scale for band <i>b</i>; the forecast hour <i>t</i></td></tr>
<tr><td><i>y</i><sub><i>k</i>,<i>t</i></sub></td><td>output member <i>k</i> at hour <i>t</i></td></tr>
<tr><td>training, validation, test runs</td><td>runs that fit the models; runs that choose the number of orders and the step; runs scored once at the end</td></tr>
<tr><td>fold, out-of-fold, in-sample, out-of-fold training error</td><td>one of the groups the training runs are split into; predicted by a fit that did not use the run's fold; predicted by a fit that used the run itself; RMSE of the out-of-fold corrected mean on the training runs</td></tr>
<tr><td>RMSE, RMS</td><td>root-mean-square error; root mean square</td></tr>
<tr><td>fair CRPS</td><td>fair continuous ranked probability score of an ensemble; lower is better (Materials and Methods)</td></tr>
<tr><td>spread, spread-to-error ratio</td><td>how far the members differ from their mean; spread divided by the RMSE of the member mean</td></tr>
<tr><td>Hovm&ouml;ller diagram</td><td>a map of a field with position across and time upward</td></tr>
<tr><td>hour-to-hour correlation</td><td>correlation along the line between a field at one hour and at the next; 1: the pattern does not change</td></tr>
</tbody>
</table>

<h2>References and Notes</h2>
<ol class="sci-refs">
<li>M. Mardani, N. Brenowitz, Y. Cohen, J. Pathak, C. Y. Chen, C. C. Liu, A. Vahdat, K. Kashinath, J. Kautz, M. Pritchard, Generative residual diffusion modeling for km-scale atmospheric downscaling. <a href="https://arxiv.org/abs/2309.15214">arXiv:2309.15214</a> (2023).</li>
<li>S. Ravela, J. D. Kim, K. Gee, X. Yan, S. Mercier, L. Albarghouty, A. Saha, Ensemble-conditional Gaussian processes (Ens-CGP): Representation, geometry, and inference. <a href="https://arxiv.org/abs/2602.13871">arXiv:2602.13871</a> (2026).</li>
<li>J. H. Friedman, Greedy function approximation: A gradient boosting machine. <i>Ann. Stat.</i> <b>29</b>, 1189&ndash;1232 (2001). <a href="https://doi.org/10.1214/aos/1013203451">doi:10.1214/aos/1013203451</a></li>
</ol>

<h2>Supplementary Materials</h2>
<figure class="jn-fig" id="fig-s1">
  <picture><source media="(max-width: 600px)" srcset="{{ base_path }}/images/successive_correction/figS1_problem_narrow.png"><img src="{{ base_path }}/images/successive_correction/figS1_problem.png" alt="The parts L, M and S and the truth along the line at hour 36; Hovmöller diagrams of the coarse input, L, M, S, the truth and the error of the input"></picture>
  <figcaption><b>Fig. S1. The parts of the example's truth, first validation run.</b> (<b>A</b>) At hour 36: the large waves <i>L</i> (orange), the lagged response <i>M</i> (blue), the small-scale part <i>S</i> (gray) and their sum, the truth <i>y</i> (black). (<b>B</b> to <b>G</b>) Hovm&ouml;ller diagrams of the coarse input <i>u</i> on its cells (B), <i>L</i> (C), <i>M</i> (D), <i>S</i> (E), the truth (F) and the error of the input on the 3-km points (G). <i>M</i> peaks after the positive crests of <i>L</i> have passed; <i>S</i> is strongest where <i>L</i> &gt; 0. <i>S</i> (E) and the error (G) use the difference color scale. <span class="sci-dl"><a href="{{ base_path }}/images/successive_correction/figS1_problem.pdf">PDF</a></span></figcaption>
</figure>

</div>
<script src="{{ base_path }}/files/successive_correction/movies.js" defer></script>
