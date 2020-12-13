# Copyright (c) 2020 Juergen Koefinger, Max Planck Institute of Biophysics, Frankfurt am Main, Germany
# Released under the MIT Licence, see the file LICENSE.txt.

from collections import OrderedDict
import numpy as np
import scipy
from . import rld
from . import sid


def all_statistical_tests(normalized_residuals):
    """
    Calculates p-values for the chi2, h, hpm, (chi2, h), and (chi2, hpm) tests.

    Parameters
    ----------
    normalized_residuals: array
        1d array containing the residuals divided by the standard error of the mean.

    Returns
    -------
    res: dict
        The Shannon information values and p-values for all test statistics.
    """
    # Parameters for gamma distribution used to calculate p-values
    gamma_param = sid.init()

    number_data_points = len(normalized_residuals)

    signs = np.sign(normalized_residuals)
    chi_square = (normalized_residuals**2).sum()

    # Calculate run-length histograms
    num, blockLen, histo, edges = rld.get_run_length_distributions(signs)

    # Single dictionary containing all results
    res = OrderedDict()

    res['chi2'] = {"label": "chi2", }
    res['h'] = {"label": "h", }
    res['hpm'] = {"label": "hpm", }
    res['chi2_h'] = {"label": "(chi2,h)", }
    res['chi2_hpm'] = {"label": "(chi^2,hpm)", }

    # Shannon information of $\chi^2$
    res['chi2']['I'] = rld.SI_chi2(chi_square, number_data_points)
    # Shannon information of $h$
    res['h']['I'] = rld.SI_h(number_data_points, histo['all'])
    # Shannon information of $h^\pm$
    res['hpm']['I'] = rld.SI_hpm(number_data_points, num[1], histo['plus'], histo['minus'])
    # Shannon information of $(\chi^2, h)$
    res['chi2_h']['I'] = res['h']['I'] + res['chi2']['I']
    # Shannon information of $(\chi^2, h^\pm)$
    res['chi2_hpm']['I'] = res['hpm']['I'] + res['chi2']['I']

    # Calculate p-values for all tests
    for test in list(res):
        res[test]['p'] = sid.get_p_value(res[test]['I'], number_data_points, test, gamma_param)

    return res
