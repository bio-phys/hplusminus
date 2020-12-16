# Copyright (c) 2020 Juergen Koefinger, Max Planck Institute of Biophysics, Frankfurt am Main, Germany
# Released under the MIT Licence, see the file LICENSE.txt.

import os
import shutil
from glob import glob
from setuptools import setup
from distutils.command.clean import clean


package_name = "hplusminus"
package_base_dir = os.path.dirname(os.path.abspath(__file__))
gsp_directory_rel = os.path.join(package_name, "gsp")
gsp_directory_abs = os.path.join(package_base_dir, gsp_directory_rel)


class custom_clean(clean):
    def run(self):
        # standard clean action
        super().run()
        # custom extra clean action
        for dir in ("build", "dist", ".eggs", "hplusminus.egg-info", "hplusminus/__pycache__", "hplusminus/test/__pycache__"):
            dir_abs = os.path.join(package_base_dir, dir)
            if os.path.exists(dir_abs):
                print("remove " + dir_abs)
                shutil.rmtree(dir_abs)


setup(
    name=package_name,
    url="https://github.com/bio-phys/hplusminus",
    author="Juergen Koefinger (MPI for Biophysics), Klaus Reuter (Max Planck Computing and Data Facility)",
    author_email="juergen.koefinger@biophys.mpg.de",
    version="1.0.1",
    description="evaluate test statistics for normalized residuals",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    requires=["numpy", "scipy", "mpmath"],
    extras_require={"jupyter": ["jupyter", ], "pytest": ["pytest", ], },
    packages=[package_name, package_name + ".test" ],
    package_data={package_name : ['gsp/*', ]},
    scripts=["hplusminus_tests.py", ],
    cmdclass={"clean": custom_clean, },
    setup_requires=["pytest-runner", ],
    tests_require=["pytest", ],
)
