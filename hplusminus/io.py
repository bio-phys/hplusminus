# Copyright (c) 2020 Juergen Koefinger, Max Planck Institute of Biophysics, Frankfurt am Main, Germany
# Released under the MIT Licence, see the file LICENSE.txt.


import numpy as np

def read_residuals_from_file(file_name, column=1):
    """
    Read normalized residuals from text file.

    Parameters
    ----------
    file_name: str
        Name of text file containing normalized residuals
    column: int 
        Number of the column from which normalized residuals are read
    Returns
    -------
    normalized_residuals: array
        1d array containing normalized residuals
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


def print_pvalues_to_screen(res):
    """
    Print output of hpm.calculate() to screen.

    Parameters
    ----------
    res: dict
        Contains Shannon infomration values, p-values, and test names (labels) for various tests.
    """
    print()
    print("         statistical                        p-value ratio   ")
    print("                test      p-value          w.r.t chi2-test  ")
    print("------------------------------------------------------------------")

    for test in list(res):
        print("%20s      %3.2e            %2.1e" % (res[test]['label'], res[test]['p'], res[test]['p'] / res['chi2']['p']))

    print("------------------------------------------------------------------")
