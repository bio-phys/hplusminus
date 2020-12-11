# Copyright (c) 2020 Juergen Koefinger, Max Planck Institute of Biophysics, Frankfurt am Main, Germany
# Released under the MIT Licence, see the file LICENSE.txt.

import os
import numpy as np
from scipy.stats import gamma as gamma_dist
import scipy


def _get_package_gsp():
    """
    Return the directory path containing gamma spline parameter files that come bundled with the package.

    -------
    gsp_dir: str
        directory path containing gamma spline parameter files
    """
    package_dir = os.path.dirname(os.path.abspath(__file__))
    gsp_dir = os.path.join(package_dir, "gsp")
    if not os.path.exists(gsp_dir):
        raise RuntimeError("gamma spline parameter directory not found at " + gsp_dir)
    else:
        return gsp_dir


def load_spline_parameters(ipath, tests=['h', 'both', 'h_simple', 'both_simple']):
    """
    Load knots and coefficients for B-splines representing :math:`\alpha`, :math:`\beta`, :math:`\matcal{I}_o` paramters of the shifted gamma disributions as functions of :math:`\log_{10} N`, where :math:`N` is the number of data points.

    Parameters
    ----------
    ipath: str
        Input path.
    tests: List of str (optional)
        Names of tests, for which paramaters are read in. Names identify the corresponding files.
    Returns
    -------
    spline_par: dict
        Dictionary containing knots and coefficients of B-splines for all tests and parameters of the shifted gamma disributions.
    """
    spline_par = {}
    for k in tests:
        spline_par[k] = {}
        for na in ["alpha", "beta", "I0"]:
            spline_par[k][na] = {}
            for tmp in ["knots", "coeffs"]:
                iname = "%s_%s_%s.npy" % (tmp, k, na)
                spline_par[k][na][tmp] = np.load(os.path.join(ipath, iname))
    return spline_par


def cumulative_SID_gamma(SI, alpha, beta, I0):
    """
    Returns cumulative distribution function of the Shannon information given by gamma distribution.

    Parameters
    ----------
    SI: float or array-like
        Shannon information
    alpha: float
        Shape parameter of the gamma disribution.
    beta: float
        Inverser scale parameter of the gamma disribution.
    I0: float
        Shift (location) parameter of the gamma distribution.
    Returns
    -------
    cdf: float
        Value of Shannon information
    """
    cdf = 1. - gamma_dist.cdf(SI, alpha, scale=1. / beta, loc=I0)
    return cdf


def get_spline(spline_par, tests=['h', 'both', 'h_simple', 'both_simple']):
    """
    Returns spline function objects for the data size dependence of the parameters of the gamma distributions representing cumulative Shannon information distribution functions.

    Parameters
    ----------
    spline_par: dict
        Dictionary containing knots and coefficients of B-splines for all tests and parameters of the shifted gamma disributions. Ouput of load_spline_parameters().
    tests: List of str (optional)
        Names of tests.
    Returns
    -------
    spline_func: dict
        Dictionary of spline functions.
    """
    nam = ["alpha", "beta", "I0"]
    spline_func = {}
    for k in tests:
        spline_func[k] = {}
        for i in range(3):
            spline_func[k][nam[i]] = scipy.interpolate.BSpline(t=spline_par[k][nam[i]]["knots"], c=spline_par[k][nam[i]]["coeffs"], k=3)
    return spline_func


def get_gamma_parameters(Ns, test, spline_func):
    """
    Returns parameters of shifted gamma distributions for given number of data points.
    Parameters
    ----------
    Ns: int
       Number of data points.
    test: str
        Name of test.
    spline_func: dict
        Dictionary of spline functions. Output of get_spline() or init().
    Returns
    -------
    alpha: float
        Shape parameter of the gamma disribution.
    beta: float
        Inverser scale parameter of the gamma disribution.
    I0: float
        Shift (location) parameter of the gamma distribution.
    """
    log_Ns = np.log10(Ns)
    alpha = spline_func[test]["alpha"](log_Ns)
    beta = spline_func[test]["beta"](log_Ns)
    I0 = spline_func[test]["I0"](log_Ns)
    return alpha, beta, I0


def init(gamma_params_ipath=_get_package_gsp()):
    """
    Initialises spline function object.

    Parameters
    ----------
    gamma_params_ipath: str
        Input path.
    Returns
    -------
    spline_func: dict
        Dictionary of spline functions. Output of get_spline() or init().

    """
    spline_par = load_spline_parameters(gamma_params_ipath)
    spline_func = get_spline(spline_par)
    return spline_func


def cumulative(SI, number_data_points, test, spline_func):
    """
    Calculate p-values for given test using gamma disribuiton approximation of Shannon information distribution.

    Parameters
    ----------
    SI: float
        Shannon information value.
    number_data_points: int
        Number of data points.
    test: str
        Name of statistical test.
    spline_func: dict
        Dictionary of spline functions. Output of get_spline() or init().
    Returns
    -------
    p-value: float
        P-value for given test.
    """
    #tests = ['chi2', 'h', 'hpm', 'chi2_h', 'chi2_hp']
    if test == "chi2":
        alpha = 0.5
        beta = 1.
        I0 = -np.log(scipy.stats.chi2.pdf(number_data_points - 2, number_data_points))
        p_value = cumulative_SID_gamma(SI, alpha, beta, I0)
    elif test == "h":
        alpha, beta, I0 = get_gamma_parameters(number_data_points, "h_simple", spline_func)
        p_value = cumulative_SID_gamma(SI, alpha, beta, I0)
    elif test == "hpm":
        alpha, beta, I0 = get_gamma_parameters(number_data_points, "h", spline_func)
        p_value = cumulative_SID_gamma(SI, alpha, beta, I0)
    elif test == "chi2_h":
        alpha, beta, I0 = get_gamma_parameters(number_data_points, "both_simple", spline_func)
        p_value = cumulative_SID_gamma(SI, alpha, beta, I0)
    elif test == "chi2_hpm":
        alpha, beta, I0 = get_gamma_parameters(number_data_points, "both", spline_func)
        p_value = cumulative_SID_gamma(SI, alpha, beta, I0)
    else:
        print("Error: Test \"%s\" not available!")
        print("Exiting. Returning -1.")
        return -1.
    return p_value


def get_p_value(SI, number_data_points, test, spline_func):
    """
    Calculate p-values for given test using the gamma distribution approximation of the Shannon information distribution.
    Wrapper function for function cumulative(SI, number_data_points, test, spline_func)

    Parameters
    ----------
    SI: float
        Shannon information value.
    number_data_points: int
        Number of data points.
    test: str
        Name of statistical test.
    spline_func: dict
        Dictionary of spline functions. Output of get_spline() or init().
    Returns
    -------
    p-value: float
        P-value for given test.
    """
    p_value = cumulative(SI, number_data_points, test, spline_func)
    return p_value
