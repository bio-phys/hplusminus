# Copyright (c) 2020 Juergen Koefinger, Max Planck Institute of Biophysics, Frankfurt am Main, Germany
# Released under the MIT Licence, see the file LICENSE.txt.

import numpy as np


def read(file_name, column=1):
    """Read normalized residuals from text file.
    """
    try:
        normalized_residuals = np.loadtxt(file_name)
        if normalized_residuals.ndim == 2:
            normalized_residuals = normalized_residuals[:, column - 1]
        print()
        print("Reading normalized residuals from column %d of file \"%s\"." % (column, file_name))
        print()
        return normalized_residuals
    except:
        msg = "Error reading column %d of file \"%s\"" % (column, file_name)
        raise RuntimeError(msg)


def print_to_screen(res):
    """Print output of hpm.calculate() to screen.
    """
    print()
    print("                                                 p-value ratio    ")
    print("                                p-value          w.r.t chi2-test  ")
    print("------------------------------------------------------------------")

    for test in list(res):
        print("%20s-test:      %3.2e            %2.1e" % (res[test]['label'], res[test]['p'], res[test]['p'] / res['chi2']['p']))

    print("------------------------------------------------------------------")
