
"""
utils.py — helper functions for effect size on gain scores.

This module is self-contained and has no external dependencies beyond numpy/pandas/math.
"""

from math import sqrt

def pooled_sd(sd1, sd2, n1, n2):
    """Pooled SD for two independent groups."""
    return sqrt(((n1-1)*sd1**2 + (n2-1)*sd2**2) / (n1+n2-2))

def gain_sd(sd0, sd2, r=0.5):
    """SD of gain score given pre/post SDs and assumed pre-post correlation r."""
    return sqrt(sd2**2 + sd0**2 - 2*r*sd0*sd2)

def d_gain(m0_e, m2_e, sd0_e, sd2_e, m0_c, m2_c, sd0_c, sd2_c, n1, n2, r=0.5):
    """
    Standardized effect size on gain scores (Cohen's d approx), with 95% CI.
    d = (ΔEG - ΔCG) / SD_pooled_gain
    """
    delta_e = m2_e - m0_e
    delta_c = m2_c - m0_c

    sdg_e = gain_sd(sd0_e, sd2_e, r=r)
    sdg_c = gain_sd(sd0_c, sd2_c, r=r)
    sdg_pooled = pooled_sd(sdg_e, sdg_c, n1, n2)

    d = (delta_e - delta_c) / sdg_pooled if sdg_pooled != 0 else 0.0
    # SE for d using Hedges & Olkin approximation
    se = sqrt((n1+n2)/(n1*n2) + (d**2)/(2*(n1+n2-2)))
    ci95 = (d - 1.96*se, d + 1.96*se)
    return d, ci95
