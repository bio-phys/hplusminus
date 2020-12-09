import os
import pytest
from .. import program

package_dir = os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."), "..")))
examples_dir = os.path.join(package_dir, "examples")

test_cases = [
    "true_model_normalized_residuals.txt",
    "alternative_model_normalized_residuals.txt",
]

@pytest.mark.parametrize("case", test_cases)
def test_program(case):
    input_file = os.path.join(examples_dir, case)
    program.run(args_file_name=input_file)
