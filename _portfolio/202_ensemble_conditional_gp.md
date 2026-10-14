---
title: "[Paper] Ensemble-Conditional Gaussian Processes (Ens-CGP): Representation, Geometry, and Inference"
excerpt: "Kriging, regularized least squares, kernel ridge regression and the Kalman update give the same Gaussian estimate; using an ensemble as the prior (Ens-CGP) shows what ensemble methods can and cannot do.<br/><img src='/images/ens_cgp/fig1_ensemble_prior.png' style='max-width: 60%; height: auto;'>"
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
.sci figure.jn-fig.half img { max-width: 480px; }
.sci figcaption { font-family: var(--jn-sans); font-size: 8.5pt; line-height: 1.4; text-align: left; }
.sci figcaption b { font-weight: 700; }
.sci .sci-dl { font-family: var(--jn-sans); font-size: 8pt; color: var(--jn-ink-3); }
.sci .sci-box { border-top: 1px solid var(--jn-rule); border-bottom: 1px solid var(--jn-rule); padding: 8px 0; margin: 1.6em 0 0 0; font-family: var(--jn-sans); font-size: 9pt; }
</style>

<div class="jn sci" markdown="0">

<p class="sci-kicker">Preprint &middot; February 2026</p>
<h1 class="sci-title">Ensemble-Conditional Gaussian Processes (Ens-CGP): Representation, Geometry, and Inference</h1>
<p class="sci-authors">Sai Ravela, Jae Deok Kim, Kenneth Gee, Xingjian Yan, Samson Mercier, Lubna Albarghouty, Anamitra Saha</p>

<p>Much of geoscience comes down to estimating a whole field, such as temperature or rain on a grid, from a few noisy measurements plus prior knowledge, which often comes from an ensemble of model runs. The task goes by several names, taught in different courses: kriging, regularized least squares, kernel ridge regression and the Kalman filter. This preprint lays out why, under Gaussian assumptions, they give the same estimate, and what changes when the prior comes from an ensemble. Here are the four main points.</p>

<h2>1&ensp;Four methods, one formula</h2>

<p>Take a prior, what is believed before the data, for the field \(f\) (a vector of \(n\) values on a grid), with mean \(m\) and covariance \(K\) (how values at different places vary together), and noisy linear measurements \(y = Hf + \varepsilon\), where \(H\) picks out what was observed and the noise \(\varepsilon\) has covariance \(R\). The field given the data, the posterior, is Gaussian with</p>

\[ m_{\rm post} = m + G\,(y - Hm), \qquad K_{\rm post} = K - GHK, \qquad G = KH^{\mathsf T}\,(HKH^{\mathsf T} + R)^{-1}. \]

<p>The gain \(G\) sets how strongly the misfit \(y - Hm\) corrects the prior. Simple kriging, the geostatistics method for interpolating a field from scattered measurements with a known mean, computes exactly this. Regularized least squares, which fits the data while penalizing fields the prior finds unlikely (misfit weighted by \(R^{-1}\), penalty by \(K^{-1}\)), gives the same mean. Kernel ridge regression, which treats \(K\) as a similarity between points, gives it too when its ridge weight equals the noise variance (the same at every observation) and the prior mean is subtracted first. And the update step of the Kalman filter, used throughout data assimilation (combining model forecasts with observations), is the same formula applied each time new observations arrive. The preprint calls the underlying object a conditional Gaussian process (CGP): a Gaussian distribution over whole fields, conditioned on the data.</p>

<h2>2&ensp;Any square root of the covariance gives the same answer</h2>

<p>Write \(K = AA^{\mathsf T}\). The columns of \(A\) can be eigenvectors of \(K\) scaled by the square roots of their eigenvalues, or, when \(K\) is an ensemble covariance, the members minus their mean divided by \(\sqrt{E-1}\) for \(E\) members; any matrix \(B\) with \(BB^{\mathsf T} = K\) gives the same posterior. When \(K\) has low rank \(r\), as an ensemble covariance does, the calculation can use a thin factor with \(n\) rows and only \(r\) columns, without ever forming the full \(n\times n\) matrix.</p>

<h2>3&ensp;With an ensemble as the prior, the data can only move the field in directions the ensemble spans</h2>

<p>Ens-CGP (the ensemble-conditional Gaussian process) uses the ensemble mean as \(m\) and the ensemble&rsquo;s sample covariance as \(K\), with the columns of \(A\) being the \(E\) members minus their mean, divided by \(\sqrt{E-1}\), and then conditions exactly. Every correction is a combination of those columns, so the data can only change the field in directions the ensemble already spans (a combination can still go outside the range of the individual members). Fig. 1 shows a one-dimensional test made for this page: a smooth field on the interval from 0 to 1, observed at 9 points with noise of standard deviation 0.1. With 40 members, the posterior mean has a root-mean-square error of 0.20 across the interval and its &plusmn;2-standard-deviation band contains the truth at 100% of points. With 4 members there are only 3 directions (subtracting the mean costs one), and the error rises to 0.58. Because the uncertainty also lives only in those directions, which the 9 observations pin down, the band is narrow and covers the truth at only 21% of points. The ensemble Kalman filter (Evensen, <i>Ocean Dynamics</i>, 2003), which gives each member its own copy of the data perturbed with random noise, is a randomized way of computing Ens-CGP: its mean matches up to that randomness.</p>

<figure class="jn-fig" id="fig-1">
  <img src="{{ base_path }}/images/ens_cgp/fig1_ensemble_prior.png" alt="Three panels of curves on the interval 0 to 1: a 40-member ensemble with its mean and band; the posterior from 40 members following the truth; the posterior from 4 members missing it.">
  <figcaption><b>Fig. 1. The ensemble is the prior.</b> A synthetic one-dimensional example made for this page: the truth (dashed) and 9 noisy observations (dots; noise standard deviation 0.1, bars &plusmn;2 standard deviations). (<b>A</b>) Prior from 40 ensemble members (gray), with its mean and &plusmn;2-standard-deviation band. (<b>B</b>) Ens-CGP posterior from those members (blue): close to the truth, and wide where there are no data (<i>x</i> between 0.5 and 0.75). (<b>C</b>) Posterior from 4 members (gray: the members; orange: the posterior): it misses the truth with a narrow band. <span class="sci-dl"><a href="{{ base_path }}/images/ens_cgp/fig1_ensemble_prior.pdf">PDF</a></span></figcaption>
</figure>

<h2>4&ensp;Reusing the same data is not new information</h2>

<p>Some iterative ensemble schemes, which refine an estimate step by step, feed the same observations back in at every iteration. That is equivalent to treating one measurement as \(k\) independent ones, i.e. replacing the noise covariance \(R\) by \(R/k\). The stated uncertainty then keeps shrinking while the error does not (Fig. 2): after 1000 uses, our example claims an uncertainty of 0.0032 at the observation sites, while its actual error there is 0.124, 39 times larger. Such schemes are better viewed as optimization that needs a stopping rule; they remain correct probability (Bayesian) updates only if each pass brings new data, or if the noise is inflated so that all passes together add up to a single update.</p>

<figure class="jn-fig half" id="fig-2">
  <img src="{{ base_path }}/images/ens_cgp/fig2_reuse.png" alt="Log-log plot: the stated posterior standard deviation falls in a straight line as the same data are reused, while the actual error levels off near the noise level.">
  <figcaption><b>Fig. 2. Reused data shrinks the stated uncertainty, not the error.</b> The posterior of Fig. 1B recomputed as if the same 9 observations had been made <i>k</i> times. Blue: posterior standard deviation. Orange: error of the posterior mean against the truth, which levels off near the noise in these particular observations (0.124). Both are root mean squares over the observation sites. Dotted: noise standard deviation. <span class="sci-dl"><a href="{{ base_path }}/images/ens_cgp/fig2_reuse.pdf">PDF</a></span></figcaption>
</figure>

<p>Ens-CGP underlies several projects in the group: in <a href="{{ base_path }}/portfolio/201_precip_downscaling/">precipitation downscaling</a> it estimates fine rain from coarse rain; in magnetotelluric inversion, which maps underground electrical resistivity from surface measurements, it provides the first guess that a neural network then corrects (<a href="https://arxiv.org/abs/2610.03225">Kim, Ravela and Evans, 2026</a>); and it is a natural first guess for the <a href="{{ base_path }}/portfolio/203_boosting_ladder/">boosting ladder</a>, a sequence of learned corrections.</p>

<p class="sci-box">Preprint: S. Ravela, J. D. Kim, K. Gee, X. Yan, S. Mercier, L. Albarghouty, A. Saha, &ldquo;Ensemble-Conditional Gaussian Processes (Ens-CGP): Representation, Geometry, and Inference,&rdquo; <a href="https://arxiv.org/abs/2602.13871">arXiv:2602.13871</a> (2026).</p>

</div>
