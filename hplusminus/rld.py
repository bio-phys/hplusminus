# Copyright (c) 2020 Juergen Koefinger, Max Planck Institute of Biophysics, Frankfurt am Main, Germany
# Released under the MIT Licence, see the file LICENSE.txt.

import numpy as np
import scipy
import mpmath
# Numba-acceleration turns out slightly beneficial, however it is completely optional:
try:
    from numba import jit
except:
    def jit(**kwargs):
        def wrap(func):
            return func
        return wrap


mpmath.mp.prec = 100


def get_run_length_distributions(sc):
    """
    Given a sequence of signs, we calculate run lengths and run length-histograms. Runs are continous sequences of all signs +1 or all signs -1.

    Parameters
    ----------
    sc: array like
        List of signs (:math:`\pm 1`)
    Returns
    -------
    num: array like
        List of number of runs, number of runs of signs with :math:`s_i=+1`, number of runs of signs with :math:`s_i=-1`.
    run_lengths: dict
        Dictionary of arrays of run length for :math:`s_i=+1` ('plus'), :math:`s_i=-1` ('minus'), and both ('all').
    histo: dict
        Dictionary of histograms of run length for :math:`s_i=+1` ('plus'), :math:`s_i=-1` ('minus'), and both ('all').
    edges: numpy array
        Edges of the histogram bins.
    """
    run_lengths = {}
    histo = {}
    Ns = sc.shape[0]
    keys = ['all', 'minus', 'plus']
    b = np.where(sc[:-1] != sc[1:])[0]
    a = np.zeros(b.shape[0] + 2, dtype=np.int)
    a[0] = -1
    a[-1] = Ns - 1

    a[1:-1] = b
    run_lengths['all'] = a[1:] - a[:-1]
    nc = run_lengths['all'].shape[0]
    dummy = 0
    if sc[0] == 1:
        run_lengths['plus'] = run_lengths['all'][dummy::2]
        run_lengths['minus'] = run_lengths['all'][1 - dummy::2]
    elif sc[0] == -1:
        run_lengths['minus'] = run_lengths['all'][dummy::2]
        run_lengths['plus'] = run_lengths['all'][1 - dummy::2]

    ncPlus = run_lengths['plus'].shape[0]
    nPlus = run_lengths['plus'].sum()
    nMinus = run_lengths['minus'].sum()
    num = [nc, nPlus, ncPlus]

    for k in keys:
        histo[k], edges = np.histogram(run_lengths[k], bins=Ns + 1, range=(0, Ns + 1))
    return num, run_lengths, histo, edges


def log_binomial(N, n):
    """
    Returns
    -------
    float
       The natural logarithm of the binomial coefficient :math:`{N \choose n}`.
    """
    lb = (np.log(np.arange(N - n + 1, N + 1))).sum()
    lb -= (np.log(np.arange(1, n + 1))).sum()
    return lb


@jit(nopython=True)
def log_multinomial_kernel(log_N_vec, nvec, len_nvec):
    lm = 0.
    for i in range(len_nvec):
        for j in range(nvec[i]):
            lm -= log_N_vec[j]
    return lm


def log_multinomial(N, nvec):
    """
    Returns
    -------
    float
        The natural logarithm of the multinomial coefficient :math:`{N \choose \prod_i nvec_i}`.
    """
    x = np.log(np.arange(1, N + 1))
    lm = x.sum()
    lm += log_multinomial_kernel(x, nvec, nvec.shape[0])
    return lm


def SI_number_of_runs(N, nc):
    """
    Parameters
    ----------
    N: int
        Number of signs.
    nc: int
        Number of runs.
    Returns
    -------
    float
        Neg. log-probability of nc runs given N uncorrelated signs.
    """
    if nc > 0 and nc <= N:
        return -log_binomial(N - 1, nc - 1) + (N - 1) * np.log(2)
    else:
        return 0.  # DANGER -log(0)


def SI_number_of_positive_runs(ncPlus, nc, N):
    """
    Parameters
    ----------
    ncPlus: int
        Number of runs with positive sign.
    nc: int
        Total number of runs.
    N: int
        Number of signs.
    Returns
    -------
    float
        Neg. log-probability of observing ncPlus runs of positive sign given the total number of runs nc and the total number of signs N.
    """
    ncMinus = nc - ncPlus
    if nc % 2 == 0:  # and ncPlus==ncMinus:
        return 0.
    elif nc % 2 == 1 and (ncPlus == ncMinus + 1 or ncPlus == ncMinus - 1):  # (ncPlus==(nc+1)/2) or (ncPlus==(nc-1)/2)):
        # return 0.5
        return np.log(2)
    else:
        return 0.  # DANGER -log(0)


def SI_number_of_positive_signs(N, nPlus, nc, ncPlus):
    """
    Parameters
    ----------
    N: int
        Total number of signs.
    nPlus: int
        Number of positive signs.
    nc: int
        Number of runs.
    ncPlus: int
        Number of runs with positive signs.
    Returns
    -------
    float
        Neg. log-probability observing nPlus signs with +1, given N signs, nc runs, and ncPlus runs with signs +1.
    """

    ncMinus = nc - ncPlus
    nMinus = N - nPlus
    if nc > 1:
        if ncMinus > 1:
            h2f1 = -mpmath.log(mpmath.hyp2f1(ncPlus, ncPlus + ncMinus - N, 1 + ncPlus - N, 1))
            norm = -log_binomial(N - 1 - ncPlus, ncMinus - 1) + h2f1
        else:
            norm = -log_binomial(N - 1, ncPlus - 1) - np.log((N - ncPlus) / float(ncPlus))

        res = -log_binomial(nPlus - 1, ncPlus - 1) - log_binomial(nMinus - 1, ncMinus - 1) - norm
        return res
    elif nc == 1:
        return 0.
    else:
        return 0.


def SI_RLD_conditional(histo, Ns):
    """
    Shannon informatin (neg. log-probability) of observing a histogram given a number of runs nc and the number of signs Ns within these runs.

    Parameters
    ----------
    histo: array
        Run-length histogram.
    Ns:
        Number of data points.
    Returns
    -------
    float
        Neg. log-probability to observe a histogram given a number of runs nc and the number of signs Ns within these runs.
    """
    nc = histo.sum()
    if nc > 0:
        SI = -log_multinomial(nc, histo)
        SI += log_binomial(Ns - 1, nc - 1)
    elif nc == 0:
        SI = 0.
    else:
        SI = 0
    return SI


def SI_hpm(N, nPlus, histoPlus, histoMinus, qHisto=True):
    """
    The total Shannon information (neg. log-probability) of observing run-length histograms :math:`h^\pm=(h^+,`h^-)`. :math:`h^+` and  :math:`h^-` are the run-length histograms for posive and negative runs, repectively

    Parameters
    ----------
    N: int
        Number of signs.
    nPlus: int
        Number of positive runs.
    histoPlus: array
        Run-length histogram for posivitve runs.
    histoMinus: array
        Run-length histogram for negative runs.
    qHisto: bool, optional
        If true (default), total Shannon information :math:`-\ln p(h)` is evaluated. If false, Shannon information for numbers of positive/negative/total numbers of signs and numbers of positive/negative runs is evaluated. Used for validation and consistency checks.

    Returns
    -------
    SI: float
        The total Shannon information (neg. log-probability) of observing run-length histograms :math:`h^\pm=(h^+,`h^-)`.    """
    ncPlus = histoPlus.sum()
    ncMinus = histoMinus.sum()
    nc = ncPlus + ncMinus
    q_debug = False
    if q_debug:
        a = SI_number_of_runs(N, nc)
        b = SI_number_of_positive_signs(N, nPlus, nc, ncPlus)
        c = SI_RLD_conditional(histoPlus, nPlus) + SI_RLD_conditional(histoMinus, N - nPlus)
        d = SI_number_of_positive_runs(ncPlus, nc, N)
        print("a", a)
        print("b", b)
        print("c", c)
        print("d", d)

    SI = SI_number_of_runs(N, nc) + SI_number_of_positive_signs(N, nPlus, nc, ncPlus)
    if qHisto == True:

        SI += SI_RLD_conditional(histoPlus, nPlus) + SI_RLD_conditional(histoMinus, N - nPlus)

    SI += SI_number_of_positive_runs(ncPlus, nc, N)
    return float(SI)


def SI_h(N, histo, qHisto=True):
    """
    The Shannon information (neg. log-probability) of observing histograms histo.

    Parameters
    ----------
    N: int
        Number of data points (signs)
    histo: array
        Counts of the run lengths
    qHisto: bool, optional
        If true (default), total Shannon information :math:`-\ln p(h)` is evaluated. If false, Shannon information for numbers of positive/negative/total numbers of signs and numbers of positive/negative runs is evaluated. Used for validation and consistency checks.
    Returns
    -------
    float
        The Shannon information (neg. log-probability) of observing histograms histo.
    """
    nc = histo.sum()
    if qHisto == True:
        SI = (N - 1) * np.log(2)
        SI -= (np.log(np.arange(1, nc + 1))).sum()
        indices = np.where(histo > 0)[0]
        for i in indices:
            SI += (np.log(np.arange(1, histo[i] + 1))).sum()
    else:
        SI = -1
    return SI


def SI_chi2(chi_square, number_data_points):
    SI = -np.log(scipy.stats.chi2.pdf(chi_square, number_data_points))
    return SI
