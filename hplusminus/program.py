import numpy as np
import scipy
from . import rld
from . import SID_gamma

def run(args_file_name, args_col=1):
    # Parameters for gamma distribution used to calculate p-values
    gamma_param = SID_gamma.init()

    try:
        normalized_residuals = np.loadtxt(args_file_name)
        if normalized_residuals.ndim == 2:
            normalized_residuals = normalized_residuals[:, args_col - 1]
        print()
        print("Reading normalized residuals from column %d of file \"%s\"." % (args_col, args_file_name))
        print()
    except:
        print("Error reading column %d of file \"%s\"" % (args_col, args_file_name))
        print("Exiting.")
        exit(-1)

    number_data_points = len(normalized_residuals)

    signs = np.sign(normalized_residuals)
    chi_square = (normalized_residuals**2).sum()

    # Calculate run-length histograms
    num, blockLen, histo, edges = rld.get_run_length_distributions(signs)

    # Dictionary for Shannon information for various tests
    I = {}
    # Dictionary for p-values for various tests
    p_value = {}

    # Shannon information of $\chi^2$
    I['chi2'] = rld.SI_chi2(chi_square, number_data_points)
    # Shannon information of $h$
    I['h'] = rld.SI_h(number_data_points, histo['all'])
    # Shannon information of $h^\pm$
    I['hpm'] = rld.SI_hpm(number_data_points, num[1], histo['plus'], histo['minus'])
    # Shannon information of $(\chi^2, h)$
    I['chi2_h'] = I['h'] + I['chi2']
    # Shannon information of $(\chi^2, h^\pm)$
    I['chi2_hpm'] = I['hpm'] + I['chi2']

    # Calculate p-values for all tests
    for test in I:
        p_value[test] = SID_gamma.get_p_value(I[test], number_data_points, test, gamma_param)

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
