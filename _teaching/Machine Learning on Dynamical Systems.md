---
title: "Machine Learning on Dynamical Systems"
collection: teaching
type: "EAPS course notes"
permalink: /teaching/Machine_Learning_on_Dynamical_Systems
venue: "MIT EAPS"
date: 2025-01-31
location: "Cambridge, MA"
---

I've started taking an off-cycle course [12.S592](https://dols.mit.edu/) on machine learning taught by [Sai Ravela](https://essg.mit.edu/), with a focus on (non-Gaussian) dynamical systems. My desired final project is on extratropical cyclone downscaling, using a reduced stochastic model. Here are some PSet notes and schematic solutions, because they are very interesting problems to think about. 

---
Loading using Google Colab is recommended.

### [L0 vs L1 Problem: Particle Tracking in Non-Gaussian Flow. Hungarian Algo (L0 Method), and Sinkhorn Algo (Doubly Stochastic)](https://colab.research.google.com/drive/1X27758UFuUIUhd7kbmvfKwkWhieA8NlB?usp=sharing)

### [Subset Selection Problem: What to do when nonlinear functional mapping is expensive? (Resampling and mapping approximation, to identify most damaging cyclones from massive input features)](https://colab.research.google.com/drive/1JIthPVkOei6DWFemKd0ZphxuljEVayyW?usp=sharing)

### [Sparse Recovery: How to identify particles with spike in wavelength spectra, convoluted and added by noises, as siganls received in telescopes? Retrieving 4 particles from a 1000by1000 space and identify their weight!](https://colab.research.google.com/drive/1EXrucdL-V_WH3sdnk6Wwl1BV0m4ge5ZK?usp=sharing)

### [Earthquake Sourcing: How to identify source location and onset time for multiple earthqukes (with spurious noises like local ppl stamping on the groud!)](https://colab.research.google.com/drive/1kTmrBh5s_eMqY0nIrPF6gHS3Y7I09v61?usp=sharing)

### [Simplest Regression: Can we get accurate polynomial coefficients? Vandermonde matrix, multicolinearity problem](https://colab.research.google.com/drive/1j9INii85vboQ91cyDQCt04NkxVumMWns?usp=sharing)

### [Quadratic Programming and Gaussian Belief Propagation: revisit nodes correspondence](https://colab.research.google.com/drive/1cUxbVqLHp0NTcAAWYlXIyEYajkCAClVQ?usp=sharing)

### [Gaussian Belief Propagation under a Bayesian viewpoint](https://colab.research.google.com/drive/1Z8abJuUg4y2SRAofLWjHi9CzD9L7QpZN?usp=sharing)

### [Regularization: Ridge, Lasso, Tikhonov, Ivanov, Morozov, Mixed-Integer Quadratic Programming (MIQP), Mixed-Integer Linear Programming (MILP), GUROBI]

### [Proof that each MLQP corresponds to a unique MILP (vice versa). Fortet (compact) linearization](https://colab.research.google.com/drive/1TL8uYGcGp1EzninOdolbwFtZJ4TYGWHE?usp=sharing)

### [Generative Adversarial Networks, & Conditional Gaussian Process Notes](https://www.overleaf.com/read/zjmncnpvckbm#473de2)

---

Meanwhile, Sai has some preferred naming of the above psets, which I've also included here:

- L0 vs L1 Problem: Correspodent Problem
- Subset Selection Problem: Where's Waldo
- Sparse Recovery: All mixed up
- Earthquake Sourcing: Boom!
- MIQP ~ MILP, Paper by [Zhu et al., 2020 PNAS](https://www.pnas.org/doi/10.1073/pnas.2014241117)
- Downscaling, Paper by [Saha and Ravela, 2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS003860)

![image](https://github.com/user-attachments/assets/5902780d-25d9-4b4e-9b6d-71b2cba42d87)

