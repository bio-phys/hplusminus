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
    Print p-values for various statistical tests to screen.

    Parameters
    ----------
    res: dict
        Contains Shannon information values, p-values, and test names (labels) for various tests.
    """
    print()
    print("         statistical                        p-value ratio   ")
    print("                test      p-value          w.r.t chi2-test  ")
    print("------------------------------------------------------------------")

    for test in list(res):
        print("%20s      %3.2e            %2.1e" % (res[test]['label'], res[test]['p'], res[test]['p'] / res['chi2']['p']))


def save_to_csv(res, filename):
    """
    Save Shannon information and  p-values for various statistical tests to csv (comma-separated values) file.  Outfile can be read with pandas (import pandas, df = pandas.read_csv(filename))

    Parameters
    ----------
    res: dict
        Contains Shannon information values, p-values, and test names (labels) for various tests.
    filename: str
        Name of output file.
    """
    with open(filename, 'w') as fp:
        fp.write("test,I,p-value\n")
        for test in list(res):
            fp.write("%s,%.10le,%.10le\n" % (test, res[test]["I"], res[test]['p']))
        fp.close()


def save_to_txt(res, filename):
    """
    Save Shannon information and p-values for various statistical tests to text file with three columns (name of the test, Shannon information I, p-value) separated by whitespaces.

    Parameters
    ----------
    res: dict
        Contains Shannon information values, p-values, and test names (labels) for various tests.
    filename: str
        Name of output file.
    """
    with open(filename, 'w') as fp:
        fp.write("# " + "%8s %8s %18s\n" % ("test", "I", "p-value"))
        for test in list(res):
            fp.write("%10s %.10le %.10le\n" % (test, res[test]["I"], res[test]['p']))
        fp.close()


def save_to_file(res, filename):
    """
    Save Shannon information and p-values for various statistical tests either to ".txt" or ".csv" file, depending on filename ending.

    Parameters
    ----------
    res: dict
        Contains Shannon information values, p-values, and test names (labels) for various tests.
    filename: str
        Name of output file. Ends either in ".txt" or ".csv".
    """
    fmt = filename[-4:]
    print()
    if fmt == ".csv":
        print("Saving to \"%s\"." % filename)
        save_to_csv(res, filename)
    elif fmt == ".txt":
        print("Saving to \"%s\"." % filename)
        save_to_txt(res, filename)
    else:
        print("No output written. Format \"%s\" not recognized." % fmt)
        print("Use either \".txt\" or \".csv\".")
    print()
