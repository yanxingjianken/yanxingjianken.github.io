---
title: "Various of Decompositions on a fluid field"
collection: notes
type: "misc."
permalink: /teaching/decompositions
venue: "misc."
date: 2025-07-01
location: "Cambridge, MA"
---

Time-mean decomposition, high-low frequency decomposition, Helmholtz decomposition,... everything you'll need to analyze a fluid field!

---
This page is under construction...

## Time-mean decomposition

### 30-day running mean

### Seasonal mean

### Calendar-date mean

### zonal mean of time mean

## Propagation-Intensification decomposition

Metho: See [TK17 Appendix B](https://journals.ametsoc.org/view/journals/atsc/74/2/jas-d-16-0122.1.xml?tab_body=pdf)

## High-low frequency decomposition
### Lanczos Filtering
When we need to separate fast-evovling field (such as synoptic cyclones) from (quasi-)stationary fields (such as slowly varying Rossby Waves), we could either do a FFT and 
cutoff at a 5-day of temporal frequency, or we can use a Lanczos filter that is even faster on large datasets. 

Method: See this [link](https://github.com/liv0505/Lanczos-Filter/blob/master/lanczosbp.py)

## Helmholtz decomposition
When we need to decompose a 2D wind field into rotating part (div-free) and a irrotational part (straining only, curl-free), we could use a helmholtz decomposition.

Method: See this [link](https://github.com/Xunius/py_helmholtz/blob/master/helmholtz.py)


