---
title: "[Paper] Convection-permitting scales break climate invariance in machine-learned precipitation downscaling"
excerpt: "A rain-downscaling network trained on today's climate still works at coarse steps but fails at the step to 3 km, where thunderstorms are resolved and warming adds most of its energy.<br/><img src='/images/climate_invariance/fig1_ladder.png' style='max-width: 60%; height: auto;'>"
collection: portfolio
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
.sci h2 { font-family: var(--jn-sans); font-size: 11pt; font-weight: 700; margin: 1.6em 0 0.4em 0; }
.sci .cite { font-style: italic; }
.sci figure.jn-fig img { width: 100%; height: auto; display: block; border: 0; }
.sci figcaption { font-family: var(--jn-sans); font-size: 8.5pt; line-height: 1.4; text-align: left; }
.sci figcaption b { font-weight: 700; }
.sci .sci-dl { font-family: var(--jn-sans); font-size: 8pt; color: var(--jn-ink-3); }
.sci ol.sci-refs { font-size: 9.5pt; padding-left: 1.6em; }
.sci ol.sci-refs li { margin: 0 0 4px 0; }
.sci .sci-box { border: 1px solid var(--jn-rule); padding: 8px 12px; margin: 1em 0 1.4em 0; font-family: var(--jn-sans); font-size: 9.5pt; }
.sci .sci-box a { font-weight: 700; }
.sci .sci-glance { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0; border-top: 2px solid var(--jn-rule); border-bottom: 1px solid var(--jn-rule); margin: 0 0 1.4em 0; font-family: var(--jn-sans); }
.sci .sci-glance a { display: block; padding: 8px 10px 10px 10px; border: 0; border-left: 1px solid var(--jn-rule-light); color: var(--jn-ink); }
.sci .sci-glance a:first-child { border-left: 0; padding-left: 0; }
.sci .sci-glance a:hover { background: #f4f4f4; }
.sci .sci-glance .n { display: block; font-size: 15pt; font-weight: 700; line-height: 1; margin-bottom: 4px; }
.sci .sci-glance .h { display: block; font-size: 9pt; font-weight: 700; line-height: 1.25; margin-bottom: 3px; }
.sci .sci-glance .t { display: block; font-size: 8.5pt; line-height: 1.35; color: var(--jn-ink-2); }
@media (max-width: 760px) {
  .sci .sci-glance { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .sci .sci-glance a:nth-child(3) { border-left: 0; padding-left: 0; }
  .sci .sci-glance a:nth-child(n+3) { border-top: 1px solid var(--jn-rule-light); }
}
@media (max-width: 420px) {
  .sci .sci-glance { grid-template-columns: 1fr; }
  .sci .sci-glance a { border-left: 0; padding-left: 0; }
  .sci .sci-glance a:nth-child(n+2) { border-top: 1px solid var(--jn-rule-light); }
}
</style>

<div class="jn sci" markdown="0">

<p class="sci-kicker">Research article &middot; Preprint &middot; Machine learning for climate downscaling</p>
<h1 class="sci-title">Convection-permitting scales break climate invariance in machine-learned precipitation downscaling</h1>
<p class="sci-authors">Xingjian Yan<sup>1</sup>, Anamitra Saha<sup>1,2</sup>, Erin M. Dougherty<sup>3</sup>, Sai Ravela<sup>1</sup></p>
<p class="sci-affil"><sup>1</sup>Department of Earth, Atmospheric, and Planetary Sciences, Massachusetts Institute of Technology, Cambridge, MA, USA. <sup>2</sup>Department of Climate Change, Indian Institute of Technology Hyderabad, Hyderabad, India. <sup>3</sup>NSF National Center for Atmospheric Research, Boulder, CO, USA.</p>

<p class="sci-abstract">Climate models compute rain on grids of about 25 to 100 km, too coarse for the downpours that cause floods. Machine-learned downscaling, a neural network that turns coarse rain fields into fine ones, is far cheaper than running a fine-grid weather model, and a network trained on today's climate is often applied to future projections. That assumes the relation between coarse and fine rain does not change as the climate warms (climate invariance). We test this assumption over Puerto Rico with 78 current-climate and 77 near-future extreme-rain days simulated at 48, 25, 12 and 3 km. Networks trained in the two climates agree at the coarse steps but disagree at the step from 12 to 3 km, the step into convection-permitting scales, where the grid is fine enough to resolve thunderstorms. Simulations of an idealized storm, a generic line of thunderstorms in a simplified setting, explain why: with the surface 4 K warmer, about 75% of the extra energy supplied by condensation goes to spatial scales (wavelengths) shorter than about 25 km, which a 12-km input cannot represent.</p>

<div class="sci-box">Preprint: Research Square, posted 23 September 2026, <a href="https://doi.org/10.21203/rs.3.rs-10899014/v1">doi:10.21203/rs.3.rs-10899014/v1</a> (CC BY 4.0). This page gives the four main findings; methods, statistics and the full reference list are in the preprint.</div>

<nav class="sci-glance" aria-label="Findings at a glance">
<a href="#f1"><span class="n">1</span><span class="h">One network per step</span><span class="t">Rain simulated at 48, 25, 12 and 3 km; a separate network learns each step.</span></a>
<a href="#f2"><span class="n">2</span><span class="h">Two climates, same input</span><span class="t">Networks trained on current and on future days get the same future input.</span></a>
<a href="#f3"><span class="n">3</span><span class="h">Invariance breaks at 12&rarr;3 km</span><span class="t">Coarse-step networks work in both climates; at 12&rarr;3 km the current-trained network gives 25% less rain variance than the future-trained one.</span></a>
<a href="#f4"><span class="n">4</span><span class="h">Warming feeds scales &lt; 25 km</span><span class="t">With the surface 4 K warmer, an idealized storm&rsquo;s energy input from condensation grows 168% at wavelengths below 25 km but only 52% above. A 12-km input cannot carry those small scales.</span></a>
</nav>

<h2 id="f1">1&ensp;A ladder of downscaling steps, one network for each</h2>

<p>The extreme-rain days were selected, by their rain averaged over the region, from an ensemble of ten simulations of a high-resolution climate model, run with historical and then high-emission greenhouse-gas levels (the scenario RCP8.5, Representative Concentration Pathway 8.5), in two periods: 2001&ndash;2021 (current) and 2041&ndash;2061 (near future) (<span class="cite">1</span>, <span class="cite">2</span>). Each day was then simulated with the weather model MPAS (Model for Prediction Across Scales) (<span class="cite">3</span>) for 36 hours in four separate runs, with grid spacings of 48, 25, 12 and 3 km, giving 36 hourly rain fields per day at each spacing (Fig. 1). Only the 3-km grid resolves thunderstorms (convection), which is why such grids are called convection-permitting; the coarser grids represent the net effect of thunderstorms by a parameterization, a simplified formula. For each step, 48&rarr;25, 25&rarr;12 and 12&rarr;3 km, a separate network was trained: a generative adversarial network (GAN), which learns to produce realistic fine detail by competing against a second network that tries to tell its output from simulated fields (<span class="cite">4</span>). Each step was trained twice, once on current-climate days and once on near-future days.</p>

<figure class="jn-fig" id="fig-1">
  <img src="{{ base_path }}/images/climate_invariance/fig1_ladder.png" alt="Rain over Puerto Rico for one hour at 48, 25, 12 and 3 km grid spacing, with arrows between the grids; at 3 km a spiral rain band appears.">
  <figcaption><b>Fig. 1. The downscaling ladder.</b> Rain rate for one hour of one current-climate extreme-rain day, from four separate MPAS simulations with (<b>A</b>) 48, (<b>B</b>) 25, (<b>C</b>) 12 and (<b>D</b>) 3 km grid spacing, on one color scale; the finer runs are not simply sharper copies of the coarser ones. Each arrow is one downscaling step, learned by its own network. Thunderstorms are parameterized on the grids of A to C and resolved on the grid of D. <span class="sci-dl"><a href="{{ base_path }}/images/climate_invariance/fig1_ladder.pdf">PDF</a></span></figcaption>
</figure>

<h2 id="f2">2&ensp;The same coarse input, two networks trained in different climates</h2>

<p>To isolate the effect of climate on what the network has learned, both 12&rarr;3-km networks receive the same future-climate input, and their outputs are compared with the 3-km simulation of the same hour (Fig. 2). Both add storm-scale detail that the 12-km input lacks. Whether they add the right amount is a statistical question, answered over all test hours in Fig. 3.</p>

<figure class="jn-fig" id="fig-2">
  <img src="{{ base_path }}/images/climate_invariance/fig2_two_climates.png" alt="Four rain maps: a blocky 12-km input, the outputs of the future-trained and the current-trained networks, and the 3-km simulation.">
  <figcaption><b>Fig. 2. Same input, two networks.</b> (<b>A</b>) Rain at 12 km for one hour of a near-future test day, a day not used in training. 3-km rain produced from A by the network trained on (<b>B</b>) near-future days and (<b>C</b>) current-climate days. (<b>D</b>) The 3-km MPAS simulation of the same hour. One color scale, white for no rain; it ends at 1.34 mm h<sup>&minus;1</sup>, the largest 95th percentile of the three 3-km fields, so that light rain stays visible (this hour is much lighter than that of Fig. 1), and higher rates are drawn in the darkest color. The 12-km input comes from a separate 12-km simulation, which here rains more than the 3-km simulation; the networks learn the relation between the two. <span class="sci-dl"><a href="{{ base_path }}/images/climate_invariance/fig2_two_climates.pdf">PDF</a></span></figcaption>
</figure>

<h2 id="f3">3&ensp;Coarse steps transfer between climates; the 12&rarr;3-km step does not</h2>

<p>We take the 468 downscaled hourly fields of the 13 near-future test days (36 hours each, none used in training), decompose them into spatial patterns, the eigenmodes of their covariance (principal components), and plot the variance each of the 60 largest patterns carries, largest first; this curve is the eigenspectrum (Fig. 3). For the two coarse steps applied in sequence (48&rarr;25&rarr;12 km), the eigenspectra of the two networks coincide with each other and with the simulation: the total variance of the current-trained network's output divided by that of the future-trained network's is 1.09, not significantly different from 1 (<i>P</i> = 0.36). For 12&rarr;3 km the current-trained network produces 25% less variance than the future-trained one (ratio 0.75, <i>P</i> = 0.025). Given the correct future input, the network trained on today's storms still underestimates the variability of future storms. Both networks fall below the simulation at this step, a known tendency of downscaling networks to produce too-smooth fields; the test of climate invariance is the gap between the two networks, which receive identical inputs.</p>

<figure class="jn-fig" id="fig-3">
  <img src="{{ base_path }}/images/climate_invariance/fig3_eigenspectra.png" alt="Two log-log plots of variance against pattern rank. Left, the three curves overlap. Right, the current-trained curve lies below the future-trained curve, which lies below the simulation.">
  <figcaption><b>Fig. 3. Climate invariance holds at the coarse steps and breaks at the convection-permitting step.</b> Eigenspectra of the near-future test hours: the variance carried by each of the 60 largest spatial patterns of the rain fields, for the MPAS simulation (black) and for the outputs of the future-trained (orange, dashed) and current-trained (blue) networks, the two networks fed the same inputs. Shading, &plusmn;1.5 standard deviations over 200 resamplings of the hours at random with replacement; it shows the spread of each pattern's variance, whereas <i>P</i> tests the ratio of total variance, paired day by day, which is far more precise. (<b>A</b>) The two steps 48&rarr;25&rarr;12 km applied in sequence. (<b>B</b>) The step 12&rarr;3 km. Numbers in each panel: total variance of the current-trained output divided by that of the future-trained output; <i>P</i> from a jackknife test that leaves out one test day at a time. <span class="sci-dl"><a href="{{ base_path }}/images/climate_invariance/fig3_eigenspectra.pdf">PDF</a></span></figcaption>
</figure>

<h2 id="f4">4&ensp;Why: warming adds energy at scales a 12-km input cannot carry</h2>

<p>To find the physical cause we simulated an idealized squall line, a generic line of thunderstorms in a simplified setting rather than a real case (<span class="cite">5</span>), on a 3-km grid with the surface warmed by 0, 2, 4, 6 and 8 K, and computed its energy budget for each band of wavelengths (<span class="cite">6</span>). Three rates matter, each per unit mass of air, for each wavelength band (the spatial scale of the motion): condensation of water vapor heats the air and so creates available potential energy, the energy stored in temperature differences (moist source <i>G</i>); buoyancy turns it into kinetic energy, the energy of motion (conversion <i>C</i>); and the motion itself carries kinetic energy from one wavelength band (the giver) to another (the receiver) (transfer <i>T<sub>K</sub></i>) (Fig. 4). With the surface 4 K warmer, <i>G</i> grows by 168% at wavelengths shorter than 25 km but by 52% at longer ones (<i>C</i>: 157% versus 43%), so about 75% of the added <i>G</i> lies below 25 km. What one band gives, another receives, so each exchange appears twice in the matrix of Fig. 4, as mirror cells of opposite color. All 13 band pairs whose exchange changes with the same sign at every 2-K warming step involve a band shorter than 25 km, although only 34 of all 55 pairs do. The 25-km band edge sits next to 24 km, twice the 12-km grid spacing and so the shortest wave a 12-km field can represent. This extra energy is therefore missing from the coarse input: the future-trained network can learn it only because its 3-km training fields contain it, and the current-trained network never sees it.</p>

<figure class="jn-fig" id="fig-4">
  <img src="{{ base_path }}/images/climate_invariance/fig4_energy.png" alt="Three 11 by 11 matrices of kinetic-energy transfer between wavelength bands with bar charts beside them; in the difference panel the bars grow toward short wavelengths and the dotted cells all involve bands shorter than 25 km.">
  <figcaption><b>Fig. 4. Warming adds energy at wavelengths below 25 km.</b> Energy budget of the idealized 3-km squall line, averaged over roughly the lowest 7 km of the atmosphere (surface to the 412-hPa pressure level), (<b>A</b>) at the current surface temperature, (<b>B</b>) with the surface 4 K warmer and (<b>C</b>) their difference. Matrices: rate at which kinetic energy passes from the giver wavelength band (column) to the receiver band (row); red, the receiver gains, blue, it loses (in panel C: gains more, gains less with warming); each exchange appears twice, as mirror cells of opposite color; the diagonal (a band to itself) is left blank. Tick labels are band centers. Bars: moist source <i>G</i> (pink) and conversion <i>C</i> (green) in each wavelength band. Dashed lines: the band edge at 25 km. Dots in panel C: exchanges that change with the same sign at every 2-K step from 0 to 8 K (13 band pairs, each drawn twice). All rates per unit mass, in 10<sup>&minus;3</sup> W kg<sup>&minus;1</sup>. <span class="sci-dl"><a href="{{ base_path }}/images/climate_invariance/fig4_energy.pdf">PDF</a></span></figcaption>
</figure>

<h2>What it means</h2>

<p>Part of the climate-change signal in local rain enters through scales that the coarse input does not contain. Climate invariance (<span class="cite">7</span>) is therefore a property of the scale step, not only of the network: networks for the coarse steps can be reused across climates, while the step into the convection-permitting range needs retraining on future-climate data, fine-tuning (continued training on a smaller set of future data) or an extra input that tells the network the climate state. A single scalar correction, such as scaling all rain by a factor tied to temperature, cannot repair an error that depends on wavelength. Cheap idealized warming experiments like the squall line above can show where a downscaling network's invariance will fail before it is used for flood-risk projections.</p>

<p>The preprint also tests a simpler statistical method in place of the GAN, the ensemble-conditional Gaussian process, which predicts fine rain from coarse rain with Gaussian statistics estimated from the training data (see <a href="{{ base_path }}/portfolio/202_ensemble_conditional_gp/">Ens-CGP</a>); the preprint's conclusions do not depend on which method is used.</p>

<h2>References and Notes</h2>
<ol class="sci-refs">
<li>E. M. Dougherty, A. F. Prein, P. A. O&rsquo;Gorman, Future changes to rainfall extremes over Puerto Rico in a convection-permitting model. <i>Earth&rsquo;s Future</i> <b>14</b> (2026). <a href="https://doi.org/10.1029/2025EF007833">doi:10.1029/2025EF007833</a></li>
<li>F. Castruccio, P. Chang, G. Danabasoglu, D. Fu, N. Rosenbloom, Q. Zhang, T. King, X. Liu, MESACLIP: A 10-member ensemble of CESM HR historical (1920&ndash;2005) and RCP 8.5 (2006&ndash;2100) simulations. NSF National Center for Atmospheric Research (2024). <a href="https://doi.org/10.5065/7N1X-K278">doi:10.5065/7N1X-K278</a>, <a href="https://doi.org/10.5065/PNCR-5S34">doi:10.5065/PNCR-5S34</a></li>
<li>W. C. Skamarock, J. B. Klemp, M. G. Duda, L. D. Fowler, S.-H. Park, T. D. Ringler, A multiscale nonhydrostatic atmospheric model using centroidal Voronoi tesselations and C-grid staggering. <i>Mon. Weather Rev.</i> <b>140</b>, 3090&ndash;3105 (2012). <a href="https://doi.org/10.1175/MWR-D-11-00215.1">doi:10.1175/MWR-D-11-00215.1</a></li>
<li>A. Saha, S. Ravela, Statistical-physical adversarial learning from data and models for downscaling rainfall extremes. <i>J. Adv. Model. Earth Syst.</i> <b>16</b> (2024). <a href="https://doi.org/10.1029/2023MS003860">doi:10.1029/2023MS003860</a></li>
<li>M. L. Weisman, J. B. Klemp, The dependence of numerically simulated convective storms on vertical wind shear and buoyancy. <i>Mon. Weather Rev.</i> <b>110</b>, 504&ndash;520 (1982). <a href="https://doi.org/10.1175/1520-0493(1982)110%3C0504:TDONSC%3E2.0.CO;2">doi:10.1175/1520-0493(1982)110&lt;0504:TDONSC&gt;2.0.CO;2</a></li>
<li>P. Augier, E. Lindborg, A new formulation of the spectral energy budget of the atmosphere, with application to two high-resolution general circulation models. <i>J. Atmos. Sci.</i> <b>70</b>, 2293&ndash;2308 (2013). <a href="https://doi.org/10.1175/JAS-D-12-0281.1">doi:10.1175/JAS-D-12-0281.1</a></li>
<li>T. Beucler, P. Gentine, J. Yuval, A. Gupta, L. Peng, J. Lin, S. Yu, S. Rasp, F. Ahmed, P. A. O&rsquo;Gorman, J. D. Neelin, N. J. Lutsko, M. Pritchard, Climate-invariant machine learning. <i>Sci. Adv.</i> <b>10</b> (2024). <a href="https://doi.org/10.1126/sciadv.adj7250">doi:10.1126/sciadv.adj7250</a></li>
</ol>

</div>
