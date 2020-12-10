# Copyright (c) 2020 Juergen Koefinger, Max Planck Institute of Biophysics, Frankfurt am Main, Germany
# Released under the MIT Licence, see the file LICENSE.txt.

import os
import pytest
from .. import io, hpm

package_dir = os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."), "..")))
examples_dir = os.path.join(package_dir, "examples")

test_cases = [
    "true_model_normalized_residuals.txt",
    "alternative_model_normalized_residuals.txt",
]


@pytest.mark.parametrize("case", test_cases)
def test_io_only(case):
    input_file = os.path.join(examples_dir, case)
    io.read(file_name=input_file, column=1)


@pytest.mark.parametrize("case", test_cases)
def test_io_calculate_print(case):
    input_file = os.path.join(examples_dir, case)
    normalized_residuals = io.read(file_name=input_file, column=1)
    results = hpm.calculate(normalized_residuals)
    io.print_to_screen(results)
