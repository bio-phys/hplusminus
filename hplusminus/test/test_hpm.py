# Copyright (c) 2020 Juergen Koefinger, Max Planck Institute of Biophysics, Frankfurt am Main, Germany
# Released under the MIT Licence, see the file LICENSE.txt.

import os
import pytest
from .. import io, evaluate

package_dir = os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."), "..")))
examples_dir = os.path.join(package_dir, "examples")

test_cases = [
    "true_model_normalized_residuals.txt",
    "alternative_model_normalized_residuals.txt",
]


@pytest.mark.parametrize("case", test_cases)
def test_io(case):
    input_file = os.path.join(examples_dir, case)
    io.read_residuals_from_file(file_name=input_file, column=1)


@pytest.mark.parametrize("case", test_cases)
def test_evaluate(case):
    input_file = os.path.join(examples_dir, case)
    normalized_residuals = io.read_residuals_from_file(file_name=input_file, column=1)
    evaluate.all_statistical_tests(normalized_residuals)


@pytest.mark.parametrize("case", test_cases)
def test_print_to_screen(case):
    input_file = os.path.join(examples_dir, case)
    normalized_residuals = io.read_residuals_from_file(file_name=input_file, column=1)
    results = evaluate.all_statistical_tests(normalized_residuals)
    io.print_pvalues_to_screen(results)


@pytest.mark.parametrize("case", test_cases)
def test_save_to_txt(case):
    input_file = os.path.join(examples_dir, case)
    normalized_residuals = io.read_residuals_from_file(file_name=input_file, column=1)
    results = evaluate.all_statistical_tests(normalized_residuals)
    io.save_to_file(results, "out.txt")


@pytest.mark.parametrize("case", test_cases)
def test_save_to_csv(case):
    input_file = os.path.join(examples_dir, case)
    normalized_residuals = io.read_residuals_from_file(file_name=input_file, column=1)
    results = evaluate.all_statistical_tests(normalized_residuals)
    io.save_to_file(results, "out.csv")
