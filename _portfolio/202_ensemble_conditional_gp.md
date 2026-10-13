---
title: "[Paper] Ensemble-Conditional Gaussian Processes (Ens-CGP): Representation, Geometry, and Inference"
excerpt: "Under Gaussian assumptions, kriging, regularized least squares, kernel regression and the Kalman update give the same estimate from one conditional Gaussian law; using an ensemble as its prior gives Ens-CGP, and shows what ensemble methods can and cannot do.<br/><img src='/images/ens_cgp/fig1_ensemble_prior.png' style='max-width: 60%; height: auto;'>"
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
.sci figure.jn-fig.half img { max-width: 480px; }
.sci figcaption { font-family: var(--jn-sans); font-size: 8.5pt; line-height: 1.4; text-align: left; }
.sci figcaption b { font-weight: 700; }
.sci .sci-dl { font-family: var(--jn-sans); font-size: 8pt; color: var(--jn-ink-3); }
.sci ol.sci-refs { font-size: 9.5pt; padding-left: 1.6em; }
.sci ol.sci-refs li { margin: 0 0 4px 0; }
.sci .sci-eq { font-family: var(--jn-serif); text-align: center; margin: 0.4em 0 0.8em 0; overflow-x: auto; }
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

<p class="sci-kicker">Research article &middot; Preprint &middot; Estimation theory</p>
<h1 class="sci-title">Ensemble-Conditional Gaussian Processes (Ens-CGP): Representation, Geometry, and Inference</h1>
<p class="sci-authors">Sai Ravela, Jae Deok Kim, Kenneth Gee, Xingjian Yan, Samson Mercier, Lubna Albarghouty, Anamitra Saha</p>
<p class="sci-affil">Earth Signals and Systems Group, Department of Earth, Atmospheric and Planetary Sciences, Massachusetts Institute of Technology, Cambridge, MA, USA.</p>

<p class="sci-abstract">Earth scientists estimate whole fields, such as temperature or rain on a grid, from a few noisy measurements combined with a prior, what is believed about the field before the data, which often comes from an ensemble, a collection of model simulations. Four methods are usually taught separately for this task: Gaussian conditioning, as in kriging (interpolation in geostatistics) and Gaussian-process regression; regularized least squares, which fits the data while penalizing implausible fields; kernel regression, which does the same with a similarity function between points; and the update step of the Kalman filter, which corrects weather forecasts with observations. When the prior is Gaussian and each measurement is a linear function of the field plus Gaussian noise, all four give the same estimate, the mean of one object: the distribution of the field given the data (the posterior), here called a conditional Gaussian process (CGP), a Gaussian process being a Gaussian distribution over a whole field. Gaussian conditioning and the Kalman update also give its covariance. The paper lays out these classical equivalences in one thread on a finite grid. Its new step is to treat the mean and covariance of an ensemble as a Gaussian prior and condition it exactly: the ensemble-conditional Gaussian process (Ens-CGP). Ensemble Kalman filters, which run the Kalman update with an ensemble, and iterative ensemble schemes, which update an ensemble repeatedly, then become ways of computing, or departing from, this one object, which shows what ensemble methods can and cannot do.</p>

<div class="sci-box">Preprint: <a href="https://arxiv.org/abs/2602.13871">arXiv:2602.13871</a>, 14 February 2026. This page gives the four main messages; definitions and proofs are in the preprint. The two figures are illustrations made for this page on a synthetic one-dimensional example.</div>

<nav class="sci-glance" aria-label="Messages at a glance">
<a href="#m1"><span class="n">1</span><span class="h">One object, four names</span><span class="t">Gaussian conditioning, regularized least squares, kernel regression and the Kalman update give the same estimate.</span></a>
<a href="#m2"><span class="n">2</span><span class="h">Any square root, same answer</span><span class="t">Any matrix <i>A</i> with <i>AA</i><sup>T</sup> equal to the prior covariance gives the same posterior.</span></a>
<a href="#m3"><span class="n">3</span><span class="h">The ensemble is the prior</span><span class="t">Ens-CGP can change the estimate only along directions the ensemble spans.</span></a>
<a href="#m4"><span class="n">4</span><span class="h">Reused data is not new data</span><span class="t">Using the same data again shrinks the stated uncertainty, not the error.</span></a>
</nav>

<h2 id="m1">1&ensp;One object behind four methods</h2>

<p>Write the unknown field on a grid as a vector \(f\) of \(n\) values. The prior is Gaussian with mean \(m\) and covariance \(K\), an \(n\times n\) matrix of how the values vary together. The data are \(y = Hf + \varepsilon\), where the observation operator \(H\) is a matrix that, for example, picks the observed grid points, and \(\varepsilon\) is zero-mean Gaussian noise with covariance \(R\), independent of \(f\). Then \(f\) given \(y\), the posterior, is Gaussian with mean \(m_{\rm post}\) and covariance \(K_{\rm post}\):</p>

\[ m_{\rm post} = m + G\,(y - Hm), \qquad K_{\rm post} = K - GHK, \qquad G = KH^{\mathsf T}\,(HKH^{\mathsf T} + R)^{-1}. \]

<p>The gain \(G\) sets how far the misfit \(y - Hm\) between data and prior moves the estimate. This is Gaussian conditioning, the computation behind kriging and Gaussian-process regression (<span class="cite">1</span>). The same \(m_{\rm post}\) is also obtained by</p>
<p>(i) regularized least squares: among candidate fields \(g\), the minimizer of</p>

\[ J(g) = \tfrac12\,\lVert y - Hg\rVert^2_{R^{-1}} + \tfrac12\,\lVert g - m\rVert^2_{K^{+}}, \qquad \lVert v\rVert^2_{W} = v^{\mathsf T} W\, v, \]

<p>a data misfit plus a penalty on fields the prior finds unlikely, where \(K^{+}\) is the inverse of \(K\), or its pseudoinverse when \(K\) is singular (then \(g - m\) is restricted to the range of \(K\)); this minimizer is the most probable field (maximum a posteriori, MAP);</p>
<p>(ii) kernel regression: the same \(J\) with \(K\) read as a kernel, a function giving the covariance of the field between any two points; the penalty term is then what kernel methods call the norm of a reproducing-kernel Hilbert space (RKHS), a measure of how rough a field is relative to the kernel (<span class="cite">2</span>);</p>
<p>(iii) the update step of the Kalman filter (its analysis step), which corrects a forecast (here, the prior) with observations and gives \(K_{\rm post}\) as well (<span class="cite">3</span>). The full Kalman filter repeats this step in time, with a forecast model carrying the estimate from one set of observations to the next.</p>

<h2 id="m2">2&ensp;Any square root of the covariance gives the same answer</h2>

<p>Factor the covariance as \(K = AA^{\mathsf T}\); \(A\), an \(n\times r\) matrix, is a square root of \(K\). Its columns are fields: for example the eigenvectors of \(K\) scaled by the square roots of their eigenvalues (spectral modes) or, as in section 3, the members of an ensemble minus their mean. Read row by row, \(A\) gives each grid point a feature vector, and \(K_{ij}\) is the inner product of the feature vectors of points \(i\) and \(j\): \(K\) is the Gram matrix of the rows, which is how kernels are built from features. This is the geometry of the title: covariance is an inner product. Every such factor spans the same subspace, the range of \(K\), and gives the same posterior. In practice one can therefore compute with an \(n\times r\) factor, with \(r\) much smaller than \(n\), without ever forming the \(n\times n\) matrix \(K\); an ensemble is one such factor, which is why it can serve directly as the prior.</p>

<h2 id="m3">3&ensp;Ens-CGP: the ensemble is the prior</h2>

<p>Given \(E\) ensemble members \(f^{(1)},\dots,f^{(E)}\), Ens-CGP takes their mean \(\bar f\) as \(m\) and their sample covariance \(K = AA^{\mathsf T}\) as the prior covariance, where the columns of \(A = [f^{(1)} - \bar f,\ \dots,\ f^{(E)} - \bar f]/\sqrt{E-1}\) are the member anomalies (members minus their mean). It then applies the formulas of section 1 without further approximation. Because the anomalies sum to zero, \(K\) has rank at most \(E - 1\); the gain still exists because the noise covariance \(R\) is invertible. The correction \(m_{\rm post} - \bar f\) is a combination of the anomalies: what the ensemble cannot represent, the data cannot change (Fig. 1). In the example, the posterior mean from 40 members has a root-mean-square error of 0.20 against the truth over the whole interval, and its &plusmn;2 standard-deviation band contains the truth at 100% of the grid points. With 4 members (drawn from the same prior), whose anomalies span only 3 directions, the error is 0.58, and the band, though narrow, contains the truth at only 21% of the points. Under the same linear-Gaussian assumptions the Ens-CGP mean equals, up to sampling error, the mean update of the ensemble Kalman filter (EnKF), which updates each member with a gain computed from the ensemble (<span class="cite">4</span>): the EnKF is one way of computing Ens-CGP. Localization (suppressing ensemble covariances between distant points) and inflation (enlarging the ensemble spread), common EnKF adjustments, change the prior covariance and so change the Ens-CGP being computed.</p>

<figure class="jn-fig" id="fig-1">
  <img src="{{ base_path }}/images/ens_cgp/fig1_ensemble_prior.png" alt="Three panels of curves on the interval 0 to 1: a 40-member ensemble with its mean and band; the posterior from 40 members following the truth; the posterior from 4 members missing it.">
  <figcaption><b>Fig. 1. The ensemble is the prior.</b> Synthetic example: a smooth random field on the interval 0 to 1 (dashed, the truth) observed at 9 points with noise of standard deviation 0.1 (dots; bars, &plusmn;2 standard deviations of the noise). (<b>A</b>) Prior from 40 ensemble members (gray): mean (black) and &plusmn;2 standard deviations (shading). (<b>B</b>) Ens-CGP posterior mean (blue) and &plusmn;2 standard deviations from this prior; the band stays wide in the gap between 0.5 and 0.75, where there are no data. (<b>C</b>) The same with 4 members (gray): the correction must be a combination of 3 patterns, so the mean (orange) cannot follow the data, while the band is narrow because the prior has no variance outside those patterns, so it misses the truth. <span class="sci-dl"><a href="{{ base_path }}/images/ens_cgp/fig1_ensemble_prior.pdf">PDF</a></span></figcaption>
</figure>

<h2 id="m4">4&ensp;Reusing the same data is not new information</h2>

<p>Iterative ensemble inversion schemes, used to infer unknown fields from indirect data, update an ensemble again and again until its predicted observations \(Hf\) match the data; they often use the same observations \(y\) at every iteration. Treating one realization of \(y\) as \(k\) independent observations is the same as applying section 1 once with the noise covariance \(R\) replaced by \(R/k\) (\(k = 1\) is section 1 itself): the data are trusted \(k\) times more than they deserve. As \(k\) grows, the stated uncertainty at the observation sites shrinks toward zero, while the mean is pulled onto the noisy observations, so its error there levels off at the size of the noise in these particular observations instead of falling. For the 40-member prior of Fig. 1A, the stated standard deviation at the observation sites is already slightly smaller than the actual error at \(k = 1\) (0.093 versus 0.116 in this single example); after 1000 uses it is 0.0032, 39 times smaller than the actual error, 0.124 (Fig. 2). Such schemes therefore minimize a cost like \(J\) of section 1 with the data term weighted more and more, which is regularized optimization; that is why they need stopping rules (when to end the iteration) and damping (smaller steps). They are Bayesian updates, correct updates of probability, only if each iteration brings new information.</p>

<figure class="jn-fig half" id="fig-2">
  <img src="{{ base_path }}/images/ens_cgp/fig2_reuse.png" alt="Log-log plot: the stated posterior standard deviation falls in a straight line as the same data are reused, while the actual error stays flat near the noise level.">
  <figcaption><b>Fig. 2. Reused data shrinks the stated uncertainty, not the error.</b> The posterior of Fig. 1B recomputed as if the same 9 observations had been made <i>k</i> times independently (<i>k</i> = 1 is Fig. 1B itself). Blue, posterior standard deviation; orange, error of the posterior mean against the truth, which rises slightly, from 0.116 to 0.124, toward the root-mean-square noise of these 9 observations (0.124); both root mean square over the observation sites, so they are not directly comparable with the whole-interval errors of section 3. Dotted, the noise standard deviation. <span class="sci-dl"><a href="{{ base_path }}/images/ens_cgp/fig2_reuse.pdf">PDF</a></span></figcaption>
</figure>

<h2>Where it is used</h2>

<p>Ens-CGP is the common backbone of several inverse problems (inferring unknown fields from indirect data) and learning problems in the group. In downscaling, which estimates fine-grid fields from coarse model output, the field stacks a coarse and a fine version of the same rain, <i>H</i> picks the coarse part, and the posterior mean is the fine field given the coarse one (<span class="cite">5</span>, <span class="cite">6</span>; see the <a href="{{ base_path }}/portfolio/201_precip_downscaling/">downscaling paper</a>). In magnetotelluric inversion, which infers underground electrical resistivity from electromagnetic measurements at the surface, it provides the first estimate that a neural network then corrects (<span class="cite">7</span>). It is also a natural first guess for the <a href="{{ base_path }}/portfolio/203_boosting_ladder/">boosting ladder</a>, a sequence of learned corrections.</p>

<h2>References and Notes</h2>
<ol class="sci-refs">
<li>C. E. Rasmussen, C. K. I. Williams, <i>Gaussian Processes for Machine Learning</i> (MIT Press, 2005).</li>
<li>G. Wahba, <i>Spline Models for Observational Data</i>, CBMS-NSF Regional Conference Series in Applied Mathematics (Society for Industrial and Applied Mathematics, 1990).</li>
<li>R. E. Kalman, A new approach to linear filtering and prediction problems. <i>J. Basic Eng.</i> <b>82</b>, 35&ndash;45 (1960).</li>
<li>G. Evensen, The Ensemble Kalman Filter: Theoretical formulation and practical implementation. <i>Ocean Dyn.</i> <b>53</b>, 343&ndash;367 (2003).</li>
<li>A. Saha, S. Ravela, Statistical-physical adversarial learning from data and models for downscaling rainfall extremes. <i>J. Adv. Model. Earth Syst.</i> <b>16</b>, e2023MS003860 (2024). <a href="https://doi.org/10.1029/2023MS003860">doi:10.1029/2023MS003860</a></li>
<li>X. Yan, A. Saha, E. M. Dougherty, S. Ravela, Convection-permitting scales break climate invariance in machine-learned precipitation downscaling. Research Square [preprint] (2026). <a href="https://doi.org/10.21203/rs.3.rs-10899014/v1">doi:10.21203/rs.3.rs-10899014/v1</a></li>
<li>J. D. Kim, S. Ravela, R. L. Evans, The Neuro-Physical Inverter: A modular framework for magnetotelluric inversion coupling ensemble conditioning with residual learning. <a href="https://arxiv.org/abs/2610.03225">arXiv:2610.03225</a> (2026).</li>
</ol>

</div>
