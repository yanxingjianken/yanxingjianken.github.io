---
title: "[Paper] Enhance! Why a rain enhancer trained today stumbles on tomorrow's thunderstorms"
excerpt: "A network that sharpens coarse climate-model rain works fine in a warmer world, right up to the last zoom, where the future hides in pixels the coarse input never had.<br/><img src='/images/climate_invariance/fig1_ladder.png' style='max-width: 60%; height: auto;'>"
collection: portfolio
---

{% include base_path %}
<link rel="stylesheet" href="{{ base_path }}/assets/css/journal.css">
<style>
.page__title { display: none; }
.sci .sci-kicker { font-family: var(--jn-sans); font-size: 8.5pt; letter-spacing: 0.06em; text-transform: uppercase; color: var(--jn-ink-2); border-bottom: 1px solid var(--jn-rule); padding-bottom: 4px; margin: 0 0 12px 0; }
.sci h1.sci-title { font-family: var(--jn-serif); font-size: 21pt; line-height: 1.15; margin: 0 0 6px 0; }
.sci .sci-authors { font-family: var(--jn-sans); font-size: 9.5pt; color: var(--jn-ink-2); margin: 0 0 16px 0; }
.sci .sci-lead { font-size: 11pt; font-weight: 700; line-height: 1.45; margin: 0 0 16px 0; }
.sci h2 { font-family: var(--jn-sans); font-size: 11pt; font-weight: 700; margin: 1.6em 0 0.4em 0; }
.sci figure.jn-fig img { width: 100%; height: auto; display: block; border: 0; }
.sci figcaption { font-family: var(--jn-sans); font-size: 8.5pt; line-height: 1.4; text-align: left; }
.sci figcaption b { font-weight: 700; }
.sci .sci-dl { font-family: var(--jn-sans); font-size: 8pt; color: var(--jn-ink-3); }
.sci .sci-box { border-top: 1px solid var(--jn-rule); border-bottom: 1px solid var(--jn-rule); padding: 8px 0; margin: 1.6em 0 0 0; font-family: var(--jn-sans); font-size: 9pt; }
</style>

<div class="jn sci" markdown="0">

<p class="sci-kicker">Preprint &middot; September 2026</p>
<h1 class="sci-title">Enhance! (Offer valid in today&rsquo;s climate only)</h1>
<p class="sci-authors">Xingjian (Ken) Yan, with Anamitra Saha, Erin M. Dougherty and Sai Ravela</p>

<p class="sci-lead">Every crime show has the scene: a blurry photo, a detective, and the order &ldquo;Enhance!&rdquo; Climate scientists do the same thing with rain. We asked whether a network trained to sharpen today&rsquo;s storms can sharpen tomorrow&rsquo;s. Mostly yes, right up to the last zoom.</p>

<h2>One rung per zoom</h2>

<p>Climate models paint rain with a brush 25 to 100 km wide, far too coarse to show the downpour that floods one street. Running a weather model sharp enough to draw individual thunderstorms (about 3 km) for decades of climate is ruinously expensive. So people train a neural network to do the enhancing instead: coarse rain in, fine rain out. That is machine-learned downscaling.</p>

<p>We built a ladder of these networks for Puerto Rico&rsquo;s wettest days, with one rung per zoom: 48 &rarr; 25 &rarr; 12 &rarr; 3 km (Fig. 1). Each rung is a generative adversarial network (GAN), a network that learns to draw realistic detail while a second network tries to catch it faking. The last rung is special. Only on the 3-km grid does the weather model draw thunderstorms (convection) itself, which is what &ldquo;convection resolved&rdquo; means in Fig. 1; on the coarser grids it replaces them with a rule of thumb, a parameterization.</p>

<figure class="jn-fig" id="fig-1">
  <img src="{{ base_path }}/images/climate_invariance/fig1_ladder.png" alt="Rain over Puerto Rico for one hour at 48, 25, 12 and 3 km grid spacing, with arrows between the grids; at 3 km a spiral rain band appears.">
  <figcaption><b>Fig. 1. One rainy hour, four zoom levels.</b> The same current-climate extreme-rain hour, from four separate simulations of the weather model MPAS at 48, 25, 12 and 3 km grid spacing (<b>A</b> to <b>D</b>), on one color scale. Each arrow is one enhancement step with its own network. <span class="sci-dl"><a href="{{ base_path }}/images/climate_invariance/fig1_ladder.pdf">PDF</a></span></figcaption>
</figure>

<h2>Same input, two upbringings</h2>

<p>Here is the catch: networks learn from the past, but we want them for the future. Using a network trained on today&rsquo;s weather for 2050 quietly assumes that the rule linking coarse rain to fine rain will not change as the planet warms. Call it climate invariance (<a href="https://doi.org/10.1126/sciadv.adj7250">Beucler et al., 2024</a>). To test it, we raised every rung twice: once on 78 extreme days from 2001&ndash;2021, and once on 77 from 2041&ndash;2061 in a high-emission scenario (RCP8.5). The days come from an ensemble of ten runs of a climate model, picked by Erin&rsquo;s extreme-event method (<a href="https://doi.org/10.1029/2025EF007833">Dougherty et al., 2026</a>). Then we handed both versions the exact same future input (Fig. 2).</p>

<figure class="jn-fig" id="fig-2">
  <img src="{{ base_path }}/images/climate_invariance/fig2_two_climates.png" alt="Four rain maps: a blocky 12-km input, the outputs of the future-trained and the current-trained networks, and the 3-km simulation.">
  <figcaption><b>Fig. 2. Same input, two upbringings.</b> (<b>A</b>) Rain at 12 km for one hour of a future day that neither network saw in training. (<b>B</b>) What the network raised on future storms makes of it at 3 km, and (<b>C</b>) what the one raised on today&rsquo;s storms makes of it. (<b>D</b>) What the 3-km simulation actually did. The color scale stops at 1.34 mm h<sup>&minus;1</sup> so that the drizzle stays visible. <span class="sci-dl"><a href="{{ base_path }}/images/climate_invariance/fig2_two_climates.pdf">PDF</a></span></figcaption>
</figure>

<h2>Twins at coarse scales, strangers at 3 km</h2>

<p>By eye, B and C look like siblings, so we asked the statistics. We took 468 hours (36 per simulated day) from 13 future days that neither network saw in training, split the rain into spatial patterns ranked from most to least variability, and measured how much each pattern carries (an eigenspectrum, Fig. 3). On the coarse rungs the two networks look like twins: the ratio of their total variance is 1.09, with no detectable difference from 1 (<i>P</i> = 0.36). The last rung, 12 &rarr; 3 km, humbles both networks: the one raised on future storms recovers 56% of the simulation&rsquo;s variance (downscaling networks are known to draw too smoothly). The one raised on today&rsquo;s storms recovers only 42%, a quarter less than that (ratio 0.75, <i>P</i> = 0.025). Even with the right future input, it paints future storms too tame.</p>

<figure class="jn-fig" id="fig-3">
  <img src="{{ base_path }}/images/climate_invariance/fig3_eigenspectra.png" alt="Two log-log plots of variance against pattern rank. Left, the three curves overlap. Right, the current-trained curve lies below the future-trained curve, which lies below the simulation.">
  <figcaption><b>Fig. 3. Twins at coarse scales, strangers at 3 km.</b> Variance carried by each of the 60 largest spatial patterns of the future test rain: simulation (black), future-trained network (orange, dashed), current-trained network (blue), both networks fed the same inputs. Shading: &plusmn;1.5 standard deviations over 200 resamplings of the hours. (<b>A</b>) The two coarse rungs, 48 &rarr; 25 &rarr; 12 km. (<b>B</b>) The last rung, 12 &rarr; 3 km. <i>P</i> tests the ratio of total variance, paired day by day, so it can be small even where the per-pattern shading overlaps. <span class="sci-dl"><a href="{{ base_path }}/images/climate_invariance/fig3_eigenspectra.pdf">PDF</a></span></figcaption>
</figure>

<h2>Why the last rung? More fuel, smaller scales</h2>

<p>To find out, we went small and simple: an idealized squall line, a line of thunderstorms in a box (<a href="https://doi.org/10.1175/1520-0493(1982)110%3C0504:TDONSC%3E2.0.CO;2">Weisman and Klemp, 1982</a>), warmed by 0 to 8 K. We split its energy budget by wavelength (<a href="https://doi.org/10.1175/JAS-D-12-0281.1">Augier and Lindborg, 2013</a>; Fig. 4). The punchline: warming does not make the storm engine more efficient, it just pours in more fuel. The fuel tap is condensation heating, the moist energy source <i>G</i> in Fig. 4. With 4 K of warming it runs 168% harder at wavelengths below 25 km but only 52% harder above, so about 75% of the extra fuel lands at the small scales. The share of fuel turned into motion does not go up (0.57 today, 0.51 at +4 K).</p>

<p>The motion then trades energy between scales, and every trade that changes steadily with warming involves the small scales. A cutoff wavelength of 25 km is almost exactly where a 12-km grid goes blind: the shortest wave it can draw is twice its spacing, 24 km. The future signal hides in pixels the coarse input does not have, so a network has to fill them in from what it learned in training, and the one raised on today&rsquo;s storms learned today&rsquo;s. You cannot enhance what is not there.</p>

<figure class="jn-fig" id="fig-4">
  <img src="{{ base_path }}/images/climate_invariance/fig4_energy.png" alt="Three 11 by 11 matrices of kinetic-energy transfer between wavelength bands with bar charts beside them; in the difference panel the bars grow toward short wavelengths and the dotted cells all involve bands shorter than 25 km.">
  <figcaption><b>Fig. 4. Warming feeds the small scales.</b> Energy budget of the idealized 3-km squall line in roughly the lowest 7 km of the atmosphere: (<b>A</b>) today, (<b>B</b>) 4 K warmer, (<b>C</b>) the difference. Matrices: how fast kinetic energy (energy of motion) moves from a giver wavelength band (column) to a receiver band (row), the transfer <i>T<sub>K</sub></i>. Red means the receiver gains (in C, gains more with warming). Each trade shows up twice, as mirror cells of opposite color. Bars: condensation heating <i>G</i> (pink) and its conversion into motion <i>C</i> (green) in each band. Dashed lines: 25 km. Dots: the 13 band pairs whose trade changes the same way at every 2-K step. All in 10<sup>&minus;3</sup> W kg<sup>&minus;1</sup>. <span class="sci-dl"><a href="{{ base_path }}/images/climate_invariance/fig4_energy.pdf">PDF</a></span></figcaption>
</figure>

<h2>So what?</h2>

<p>In our test, the coarse rungs of the ladder could be reused in a warmer world, but the rung into thunderstorm-resolving scales could not: it needs retraining on future data, or at least a hint about which climate it is working in. And because the error depends on scale, a single fudge factor, such as scaling all rain by the textbook 7% per degree of warming (warmer air holds about 7% more water vapor per degree), is unlikely to fix it. A few warmed squall lines are cheap, and they already point to the rung worth worrying about. (The preprint also tries a simpler statistical enhancer, the <a href="{{ base_path }}/portfolio/202_ensemble_conditional_gp/">ensemble-conditional Gaussian process</a>. The conclusion is the same.)</p>

<p>Big thanks to my coauthors: Anamitra Saha (IIT Hyderabad), who developed the downscaling networks; Erin Dougherty (NSF NCAR), who picked the extreme days and ran the weather simulations; and Sai Ravela (MIT).</p>

<p class="sci-box">Preprint: X. Yan, A. Saha, E. M. Dougherty, S. Ravela, &ldquo;Convection-permitting scales break climate invariance in machine-learned precipitation downscaling,&rdquo; Research Square (2026), <a href="https://doi.org/10.21203/rs.3.rs-10899014/v1">doi:10.21203/rs.3.rs-10899014/v1</a>.</p>

</div>
