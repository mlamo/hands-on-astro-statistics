**Authors:** Sonia El Hedri and Mathieu Lamoureux, APC/CNRS

This repository was initially prepared in the context of the [ACME Neutrino Astronomy Bootcamp](https://acme-nu-astro.sciencesconf.org/). It is organised by the ACME project, funded from the European Union's Horizon Europe Research and Innovation programme under Grant Agreement No 101131928.

## Hands-on structure

There are three notebooks corresponding to different exercises:
- Part 1: sampling of random variables
- Part 2: how to run a simple likelihood analysis (point-source case)
- Part 3: small project to run
- Extra 1: extra exercices on various topics (fitting additional parameters, systematic uncertainties, different sensitivity definitions)
- Extra 2: how to run a point-source Bayesian analysis

## Setup

The following packages are required:

- **matplotlib**: simple plots, histograms, customizing figures (also 2D contour plots in appendix of tutorial)
- **numpy**: 
    - arrays handling: vectorization, concatenation, mean, search for minimum/maximum
    - random generation module: generation of random variables with uniform, normal and Poisson distributions
- **scipy**:
    - statistics: evaluate probability density functions (PDFs), cumulative distributions (CDFs), survival functions (SF), generate random variables (random variable sampling = rvs)
    - optimization: 1D and nD minimizer, root finding
    - special functions: error function and its inverse, Gamma function
    - integration: 1D integration
- **time**: runtime computation
- **tqdm**: progress bar