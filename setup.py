import os
from glob import glob
from setuptools import setup

# not necessary for the actual installation
#data_files=[("examples", glob(os.path.join("examples", "*"))), ("gamma_spline_parameters", glob(os.path.join("gamma_spline_parameters", "*")))],

setup(
    name="hplusminus",
    version="0.0.1",
    author="Juergen Koefinger",
    description="evaluate test statistics for normalized residuals",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    packages=["hplusminus",],
)
