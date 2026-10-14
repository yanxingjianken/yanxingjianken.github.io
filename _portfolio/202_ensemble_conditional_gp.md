---
title: "[Paper] One Gaussian, four hats: Ensemble-Conditional Gaussian Processes (Ens-CGP)"
excerpt: "Kriging, least squares, kernel ridge regression and the Kalman update are one Gaussian wearing four hats. Give it an ensemble as its prior and you learn what ensembles can, and cannot, imagine.<br/><img src='/images/ens_cgp/fig1_ensemble_prior.png' style='max-width: 60%; height: auto;'>"
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
.sci figure.jn-fig.half img { max-width: 480px; }
.sci figcaption { font-family: var(--jn-sans); font-size: 8.5pt; line-height: 1.4; text-align: left; }
.sci figcaption b { font-weight: 700; }
.sci .sci-dl { font-family: var(--jn-sans); font-size: 8pt; color: var(--jn-ink-3); }
.sci .sci-box { border-top: 1px solid var(--jn-rule); border-bottom: 1px solid var(--jn-rule); padding: 8px 0; margin: 1.6em 0 0 0; font-family: var(--jn-sans); font-size: 9pt; }
</style>

<div class="jn sci" markdown="0">

<p class="sci-kicker">Preprint &middot; February 2026</p>
<h1 class="sci-title">One Gaussian, four hats</h1>
<p class="sci-authors">Sai Ravela, Jae Deok Kim, Kenneth Gee, Xingjian Yan, Samson Mercier, Lubna Albarghouty and Anamitra Saha</p>

<p class="sci-lead">Geoscientists keep estimating whole maps from a handful of noisy measurements, and over the decades the job has picked up four names, taught in four different classrooms: kriging, regularized least squares, kernel ridge regression and the Kalman filter. Our preprint points out that, under Gaussian assumptions, they are one formula wearing four hats. Then it asks what happens when the prior comes from an ensemble.</p>

<h2>Four hats</h2>

<p>Start with a prior guess of the field: a mean \(m\) and a covariance \(K\), which says how values at different places tend to move together. Take noisy linear measurements of the field \(f\), \(y = Hf + \varepsilon\), where \(H\) picks out what you observed and the noise \(\varepsilon\) has covariance \(R\). Ask for the field given the data. The answer, called the posterior, is a Gaussian with mean and covariance</p>

\[ m_{\rm post} = m + G\,(y - Hm), \qquad K_{\rm post} = K - GHK, \qquad G = KH^{\mathsf T}\,(HKH^{\mathsf T} + R)^{-1}. \]

<p>The gain \(G\) decides how hard the misfit \(y - Hm\) pushes the estimate. Simple kriging, the geostatistician&rsquo;s interpolator, computes exactly this. Regularized least squares, which fits the data while penalizing fields the prior finds implausible, lands on the same mean (misfit weighted by \(R^{-1}\), penalty by \(K^{-1}\)). So does kernel ridge regression, which reads \(K\) as a measure of similarity between points. And the update step of the Kalman filter, a workhorse of weather forecasting, is this formula with a time stamp. We call the object behind all four a conditional Gaussian process (CGP): a Gaussian over whole maps rather than single numbers, conditioned on the data.</p>

<h2>The ensemble can only imagine what it has seen</h2>

<p>In practice nobody hands you \(K\). What you have is an ensemble: a few dozen model runs that disagree in instructive ways. Ens-CGP (the ensemble-conditional Gaussian process) takes the ensemble&rsquo;s mean and spread as the prior and then conditions exactly, with no further approximation. Write \(K = AA^{\mathsf T}\), where the columns of \(A\) are the members minus their mean, divided by \(\sqrt{E-1}\) for \(E\) members. Any correction is then a mix of those columns. Any other matrix \(B\) with \(BB^{\mathsf T} = K\) gives the same answer, so the ensemble is just a cheap way to hold \(K\). The data can only nudge the field in directions the ensemble already imagined (Fig. 1).</p>

<p>With 40 members the posterior tracks the truth: a root-mean-square error of 0.20 across the interval, with the truth inside its &plusmn;2-standard-deviation band at 100% of points. With 4 members there are only 3 directions to move in (subtracting the mean costs one). The error jumps to 0.58, and worse, the uncertainty also lives only in those 3 directions, and 9 observations pin all of them down, so the posterior sees nothing left to doubt. Its band is narrow and covers the truth at only 21% of points. The ensemble Kalman filter (Evensen, <i>Ocean Dynamics</i>, 2003) turns out to be a randomized way of computing Ens-CGP: it gives each member its own copy of the data jittered with fake noise, so its mean matches up to that randomness.</p>

<figure class="jn-fig" id="fig-1">
  <img src="{{ base_path }}/images/ens_cgp/fig1_ensemble_prior.png" alt="Three panels of curves on the interval 0 to 1: a 40-member ensemble with its mean and band; the posterior from 40 members following the truth; the posterior from 4 members missing it.">
  <figcaption><b>Fig. 1. The ensemble can only imagine what it has seen.</b> A synthetic one-dimensional example made for this page: the truth (dashed) and 9 noisy observations (dots; noise standard deviation 0.1, bars &plusmn;2 standard deviations). (<b>A</b>) A prior from 40 ensemble members (gray), with its mean and &plusmn;2-standard-deviation band. (<b>B</b>) The Ens-CGP posterior from those members (blue): close to the truth, and honestly wide where there are no data (<i>x</i> between 0.5 and 0.75). (<b>C</b>) The posterior from only 4 members (gray: the 4 members; orange: the posterior): wrong, and confidently so. <span class="sci-dl"><a href="{{ base_path }}/images/ens_cgp/fig1_ensemble_prior.pdf">PDF</a></span></figcaption>
</figure>

<h2>Hearing the same joke twice</h2>

<p>Some iterative ensemble schemes, which refine a model&rsquo;s unknowns step by step, feed the same observations back in at every iteration. Mathematically that is like pretending you measured \(k\) times when you measured once: the noise covariance \(R\) quietly becomes \(R/k\). The posterior grows ever more sure of itself while drifting, if anything, slightly farther from the truth (Fig. 2). After using the data 1000 times, our toy posterior claims an uncertainty of 0.0032 at the observation sites, while its actual error there is 0.124, 39 times larger. Hearing the same joke a thousand times does not make it funnier; it only makes you surer you got it. Such schemes keep pushing toward the data instead of weighing it honestly, so someone has to decide when to stop. They become honest updates again only if each pass brings new data, or if the noise is inflated so that all the passes add up to one update.</p>

<figure class="jn-fig half" id="fig-2">
  <img src="{{ base_path }}/images/ens_cgp/fig2_reuse.png" alt="Log-log plot: the stated posterior standard deviation falls in a straight line as the same data are reused, while the actual error stays flat near the noise level.">
  <figcaption><b>Fig. 2. Same data, more confidence, no more accuracy.</b> The posterior of Fig. 1B recomputed as if the same 9 observations had been made <i>k</i> times. Blue: the uncertainty the posterior claims (its standard deviation). Orange: its actual error against the truth, which levels off near the noise in these particular observations (0.124). Both are root mean squares over the observation sites. Dotted: the noise standard deviation. <span class="sci-dl"><a href="{{ base_path }}/images/ens_cgp/fig2_reuse.pdf">PDF</a></span></figcaption>
</figure>

<h2>Where it shows up</h2>

<p>Ens-CGP pops up all over our group&rsquo;s work. In <a href="{{ base_path }}/portfolio/201_precip_downscaling/">rain downscaling</a> it estimates fine rain from coarse rain by conditioning the fine field on the coarse one. In magnetotelluric inversion, which maps electrical resistivity underground from measurements at the surface, it gives the first guess that a neural network then corrects (<a href="https://arxiv.org/abs/2610.03225">Kim, Ravela and Evans, 2026</a>). It also makes a natural first guess for the <a href="{{ base_path }}/portfolio/203_boosting_ladder/">boosting ladder</a>, a stack of learned corrections in which each one fixes what the previous ones missed.</p>

<p class="sci-box">Preprint: S. Ravela, J. D. Kim, K. Gee, X. Yan, S. Mercier, L. Albarghouty, A. Saha, &ldquo;Ensemble-Conditional Gaussian Processes (Ens-CGP): Representation, Geometry, and Inference,&rdquo; <a href="https://arxiv.org/abs/2602.13871">arXiv:2602.13871</a> (2026).</p>

</div>
