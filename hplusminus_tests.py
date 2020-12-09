#!/usr/bin/env python

# Copyright (c) 2020 Juergen Koefinger, Max Planck Institute of Biophysics, Frankfurt am Main, Germany
# Released under the MIT Licence, see the file LICENSE.txt.

"""
Statistical tests for systematic deviations of a model from sequential data
===========================================================================

The script evaluates the chi2, h, hpm, (chi2,h), and (chi2,hpm) statistical tests for given normalized residuals.
Note that the p-value of the chi2-test approximately corresponds to the p-value of a two-sided test.

h and hpm test are independent of the magnitudes of the residuals.
WARNING: chi2, (chi2,h), and (chi2,hpm) test are only meaningful for properly normalized residuals.


INPUT
-----
A text file containing the N normalized residuals r_i/\sigma_i, i=1...N.
Normalized residuals r_i/\sigma_i are given by the difference r_i=f_i-d_i between the model f_i and the noisy data d_i, divided by the standard error of the mean \sigma_i.

OUTPUT
------
P-values of chi2, h, hpm, (chi2,h), and (chi2,hpm) tests.
Ratios of the p-value with respect to the p-value of the chi2 test for easier comparison.

Statistical tests
-----------------

    Name in         Name in
    Output          LateX notation        Description
    -----------------------------------------------------------------------------------------------------------------
    chi2...........$\chi^2$...............Pearson's chi-square value \sum_i r_i^2/\sigma_i^2
    h..............$h$....................Run-length histogram of all runs, independent of their signs
    hpm............$h^\pm=(h^+, h^-)$.....Separate run-length histograms for positive runs, $h^+$, and negative runs $h^-$.
    (chi2,h).......$(\chi^2, h)$..........Combined $\chi^2$ and $h$ test statistic.
    (chi2,hpm).....$(\chi^2, h^\pm)$......Combined $\chi^2$ and $h^\pm$ test statistic.

Reference
---------
Powerful statistical tests for sequential data
Juergen Koefinger and Gerhard Hummer (2020) doi.org/XXXXXXXXXXXXXX
------------------------------------------------------------------

"""

import numpy as np
import scipy
import argparse as argp
from hplusminus import program

parser = argp.ArgumentParser(description=__doc__, formatter_class=argp.RawDescriptionHelpFormatter)
parser.add_argument("file_name", type=str, help="Name of text file containing normalized residuals, reading 1st column per default.")
parser.add_argument("--col", type=int, default=1, help="Column where to find normalized residuals.")
args = parser.parse_args()

program.run(args_file_name=args.file_name, args_col=args.col)

