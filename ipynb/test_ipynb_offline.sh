#!/bin/bash

set -e

for NB in hplusminus_statistical_power.ipynb hplusminus_tests.ipynb
do
    TMPNB="tmp__${NB}"
    cp -v $NB $TMPNB
    jupyter nbconvert --to notebook --inplace --execute $TMPNB
    rm -f $TMPNB
done
