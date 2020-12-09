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
import hplusminus as hpm

parser = argp.ArgumentParser(description=__doc__, formatter_class=argp.RawDescriptionHelpFormatter)
parser.add_argument("file_name", type=str, help="Name of text file containing normalized residuals, reading 1st column per default.")
parser.add_argument("--col", type=int, default=1, help="Column where to find normalized residuals.")
args = parser.parse_args()

# Parameters for gamma distribution used to calcualte p-values
gamma_param = hpm.init()

try:
    normalized_residuals = np.loadtxt(args.file_name)
    if normalized_residuals.ndim == 2:
        normalized_residuals = normalized_residuals[:, args.col - 1]
    print()
    print("Reading normalized residuals from column %d of file \"%s\"." % (args.col, args.file_name))
    print()
except:
    print("Error reading column %d of file \"%s\"" % (args.col, args.file_name))
    print("Exiting.")
    exit(-1)

number_data_points = len(normalized_residuals)

signs = np.sign(normalized_residuals)
chi_square = (normalized_residuals**2).sum()

# Calculate run-length histograms
num, blockLen, histo, edges = hpm.get_run_length_distributions(signs)

# Dictionary for Shannon information for various tests
I = {}
# Dictionary for p-values for various tests
p_value = {}

# Shannon information of $\chi^2$
I['chi2'] = hpm.SI_chi2(chi_square, number_data_points)
# Shannon information of $h$
I['h'] = hpm.SI_h(number_data_points, histo['all'])
# Shannon information of $h^\pm$
I['hpm'] = hpm.SI_hpm(number_data_points, num[1], histo['plus'], histo['minus'])
# Shannon information of $(\chi^2, h)$
I['chi2_h'] = I['h'] + I['chi2']
# Shannon information of $(\chi^2, h^\pm)$
I['chi2_hpm'] = I['hpm'] + I['chi2']

# Calculate p-values for all tests
for test in I:
    p_value[test] = hpm.get_p_value(I[test], number_data_points, test, gamma_param)

test_names = {}
test_names['chi2'] = "chi2"
test_names['h'] = "h"
test_names['hpm'] = "hpm"
test_names['chi2_h'] = "(chi2,h)"
test_names['chi2_hpm'] = "(chi^2,hpm)"

print()
print("                                                 p-value ratio    ")
print("                                p-value          w.r.t chi2-test  ")
print("------------------------------------------------------------------")
tests = ["chi2", "h", "hpm", "chi2_h", "chi2_hpm"]

for test in tests:
    print("%20s-test:      %3.2e            %2.1e" % (test_names[test], p_value[test], p_value[test] / p_value['chi2']))

print("------------------------------------------------------------------")
