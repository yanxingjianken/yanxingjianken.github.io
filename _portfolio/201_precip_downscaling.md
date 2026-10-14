---
title: "[Paper] Convection-permitting scales break climate invariance in machine-learned precipitation downscaling"
excerpt: "Rain-downscaling networks trained on today's climate transfer to a warmer climate at coarse steps, but not at the step to thunderstorm-resolving 3 km, where warming adds most of its energy.<br/><img src='/images/climate_invariance/fig1_ladder.png' style='max-width: 60%; height: auto;'>"
collection: portfolio
---

{% include base_path %}
<link rel="stylesheet" href="{{ base_path }}/assets/css/journal.css">
<style>
.page__title { display: none; }
.sci .sci-kicker { font-family: var(--jn-sans); font-size: 8.5pt; letter-spacing: 0.06em; text-transform: uppercase; color: var(--jn-ink-2); border-bottom: 1px solid var(--jn-rule); padding-bottom: 4px; margin: 0 0 12px 0; }
.sci h1.sci-title { font-family: var(--jn-serif); font-size: 20pt; line-height: 1.15; margin: 0 0 6px 0; }
.sci .sci-authors { font-family: var(--jn-sans); font-size: 9.5pt; color: var(--jn-ink-2); margin: 0 0 16px 0; }
.sci h2 { font-family: var(--jn-sans); font-size: 11pt; font-weight: 700; margin: 1.6em 0 0.4em 0; }
.sci figure.jn-fig img { width: 100%; height: auto; display: block; border: 0; }
.sci figcaption { font-family: var(--jn-sans); font-size: 8.5pt; line-height: 1.4; text-align: left; }
.sci figcaption b { font-weight: 700; }
.sci .sci-dl { font-family: var(--jn-sans); font-size: 8pt; color: var(--jn-ink-3); }
.sci .sci-box { border-top: 1px solid var(--jn-rule); border-bottom: 1px solid var(--jn-rule); padding: 8px 0; margin: 1.6em 0 0 0; font-family: var(--jn-sans); font-size: 9pt; }
</style>

<div class="jn sci" markdown="0">

<p class="sci-kicker">Preprint &middot; September 2026</p>
<h1 class="sci-title">Convection-permitting scales break climate invariance in machine-learned precipitation downscaling</h1>
<p class="sci-authors">Xingjian Yan, Anamitra Saha, Erin M. Dougherty, Sai Ravela</p>

<p>Climate models compute rain on grids 25 to 100 km wide, too coarse for the downpours that flood a neighborhood. Running a weather model fine enough to resolve individual thunderstorms (about 3 km) over decades is far too expensive, so a common shortcut is machine-learned downscaling: train a neural network to turn coarse rain fields into fine ones. Networks are trained on today&rsquo;s climate and then applied to the future, which quietly assumes that the relation between coarse and fine rain does not change as the climate warms. This assumption is known as climate invariance (<a href="https://doi.org/10.1126/sciadv.adj7250">Beucler et al., 2024</a>). We tested it over Puerto Rico and found no detectable change at coarse resolution, but a significant break at the step where thunderstorms start to be resolved.</p>

<h2>1&ensp;One network for each step, 48 &rarr; 25 &rarr; 12 &rarr; 3 km</h2>

<p>Erin selected extreme-rain days from an ensemble of ten climate-model runs (<a href="https://doi.org/10.1029/2025EF007833">Dougherty et al., 2026</a>): 78 days in 2001&ndash;2021 and 77 days in 2041&ndash;2061 under a high-emission scenario (RCP8.5). Each day was simulated for 36 hours with the weather model MPAS at 48, 25, 12 and 3 km, and a separate network, a generative adversarial network (GAN) that learns to draw realistic detail, was trained for each step (Fig. 1). Only the 3-km grid resolves thunderstorms (convection), which is why such grids are called convection-permitting; the coarser grids represent thunderstorms with a simplified rule, a parameterization.</p>

<figure class="jn-fig" id="fig-1">
  <img src="{{ base_path }}/images/climate_invariance/fig1_ladder.png" alt="Rain over Puerto Rico for one hour at 48, 25, 12 and 3 km grid spacing, with arrows between the grids; the spiral rain bands become sharper at each step.">
  <figcaption><b>Fig. 1. The downscaling ladder.</b> One hour of one current-climate extreme-rain day, from four separate MPAS simulations at 48, 25, 12 and 3 km grid spacing (<b>A</b> to <b>D</b>), on one color scale. Each arrow is one downscaling step with its own network. <span class="sci-dl"><a href="{{ base_path }}/images/climate_invariance/fig1_ladder.pdf">PDF</a></span></figcaption>
</figure>

<h2>2&ensp;Networks trained in two climates, given the same input</h2>

<p>Every step was trained twice, once on current-climate days and once on near-future days. To see whether the learned relation depends on climate, we gave both versions the same future input and compared their output with the simulation on the finer grid (Fig. 2). By eye the two outputs look much alike; the difference shows up in the statistics of many hours (Fig. 3).</p>

<figure class="jn-fig" id="fig-2">
  <img src="{{ base_path }}/images/climate_invariance/fig2_two_climates.png" alt="Four rain maps: a blocky 12-km input, the outputs of the future-trained and the current-trained networks, and the 3-km simulation.">
  <figcaption><b>Fig. 2. Same input, two training climates.</b> (<b>A</b>) Rain at 12 km for one hour of a future day not used in training. 3-km rain produced from A by the network trained on (<b>B</b>) future days and (<b>C</b>) current days. (<b>D</b>) The 3-km simulation of the same hour. The color scale ends at 1.34 mm h<sup>&minus;1</sup> so that light rain stays visible. <span class="sci-dl"><a href="{{ base_path }}/images/climate_invariance/fig2_two_climates.pdf">PDF</a></span></figcaption>
</figure>

<h2>3&ensp;No detectable climate dependence at the coarse steps; a significant one at 12 &rarr; 3 km</h2>

<p>We took 468 hours (36 per simulated day) from 13 future days held out of training, split the rain into spatial patterns ranked by how much variability they carry, and plotted the variance of each pattern, largest first (an eigenspectrum, as in principal component analysis; Fig. 3). For the coarse steps the two networks agree: the ratio of their total variance is 1.09, with no detectable difference from 1 (<i>P</i> = 0.36). At 12 &rarr; 3 km, the future-trained network recovers 56% of the simulated variance (downscaling networks tend to be too smooth), and the current-trained network only 42%, a quarter less (ratio 0.75, <i>P</i> = 0.025). Even with the correct future input, the network trained on today&rsquo;s storms underestimates the variability of future storms more than the network trained on future storms does.</p>

<figure class="jn-fig" id="fig-3">
  <img src="{{ base_path }}/images/climate_invariance/fig3_eigenspectra.png" alt="Two log-log plots of variance against pattern rank. Left, the three curves overlap. Right, the current-trained curve lies below the future-trained curve, which lies below the simulation.">
  <figcaption><b>Fig. 3. Eigenspectra of the future test rain.</b> Variance carried by each of the 60 largest spatial patterns: simulation (black), future-trained network (orange, dashed), current-trained network (blue), both networks fed the same inputs. Shading: &plusmn;1.5 standard deviations over 200 resamplings of the hours. (<b>A</b>) The two coarse networks chained together, 48 &rarr; 25 &rarr; 12 km. (<b>B</b>) The step 12 &rarr; 3 km. <i>P</i> tests the ratio of total variance, paired day by day, so it can be small where the per-pattern shading overlaps. <span class="sci-dl"><a href="{{ base_path }}/images/climate_invariance/fig3_eigenspectra.pdf">PDF</a></span></figcaption>
</figure>

<h2>4&ensp;A likely reason: warming adds energy at scales a 12-km grid cannot carry</h2>

<p>To find the physical reason we simulated an idealized squall line, a line of thunderstorms in a simplified setting (<a href="https://doi.org/10.1175/1520-0493(1982)110%3C0504:TDONSC%3E2.0.CO;2">Weisman and Klemp, 1982</a>), with the surface warmed by 0 to 8 K in 2-K steps, and split its energy budget by wavelength (<a href="https://doi.org/10.1175/JAS-D-12-0281.1">Augier and Lindborg, 2013</a>; Fig. 4). Condensation heating (<i>G</i>) is the energy input, part of it is converted into motion (<i>C</i>), and the motion exchanges kinetic energy between scales. Warming does not make the conversion more efficient (the fraction of <i>G</i> turned into motion is 0.57 today and 0.51 at +4 K); it supplies more heating.</p>

<p>With 4 K of warming, <i>G</i> grows by 168% at wavelengths below 25 km but by 52% above, so about 75% of the extra input lands at the small scales. Every exchange between scales that changes steadily with warming also involves those small scales. A 12-km grid cannot represent waves shorter than 24 km, twice its spacing, and 25 km is the nearest band edge. This points to the climate signal entering through scales absent from the coarse input, which a network can only supply from what it learned in training.</p>

<figure class="jn-fig" id="fig-4">
  <img src="{{ base_path }}/images/climate_invariance/fig4_energy.png" alt="Three 11 by 11 matrices of kinetic-energy transfer between wavelength bands with bar charts beside them; in the difference panel the bars grow toward short wavelengths and the dotted cells all involve bands shorter than 25 km.">
  <figcaption><b>Fig. 4. Warming adds energy mostly at wavelengths below 25 km.</b> Energy budget of the idealized 3-km squall line in roughly the lowest 7 km of the atmosphere: (<b>A</b>) current surface temperature, (<b>B</b>) 4 K warmer, (<b>C</b>) the difference. Matrices: rate at which kinetic energy moves from a giver wavelength band (column) to a receiver band (row), the transfer <i>T<sub>K</sub></i>; red, the receiver gains (in C, gains more with warming); each exchange appears twice, as mirror cells of opposite color. Bars: condensation heating <i>G</i> (pink) and its conversion into kinetic energy <i>C</i> (green) in each band. Dashed lines: 25 km. Dots: the 13 band pairs (each shown twice) whose exchange changes the same way at every 2-K step. Units 10<sup>&minus;3</sup> W kg<sup>&minus;1</sup>. <span class="sci-dl"><a href="{{ base_path }}/images/climate_invariance/fig4_energy.pdf">PDF</a></span></figcaption>
</figure>

<p>In short, the coarse steps of a downscaling chain could be reused in a warmer climate in our test, but the step into thunderstorm-resolving scales needs retraining or explicit information about the climate. Because the error depends on scale, a single correction factor, such as scaling rain by about 7% per degree of warming (roughly how much more water vapor warmer air can hold), is unlikely to fix it. The preprint also tests a simpler statistical method, the <a href="{{ base_path }}/portfolio/202_ensemble_conditional_gp/">ensemble-conditional Gaussian process</a>, with the same conclusion.</p>

<p>Thanks to my coauthors: Anamitra Saha (IIT Hyderabad), who developed the downscaling networks; Erin Dougherty (NSF NCAR), who selected the extreme days and ran the MPAS simulations; and Sai Ravela (MIT).</p>

<p class="sci-box">Preprint: X. Yan, A. Saha, E. M. Dougherty, S. Ravela, &ldquo;Convection-permitting scales break climate invariance in machine-learned precipitation downscaling,&rdquo; Research Square (2026), <a href="https://doi.org/10.21203/rs.3.rs-10899014/v1">doi:10.21203/rs.3.rs-10899014/v1</a>.</p>

</div>
