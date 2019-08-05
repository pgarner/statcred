#!/usr/bin/env python3
#
# Copyright 2019 by Idiap Research Institute, http://www.idiap.ch
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Phil Garner, August 2019
#
import argparse
import numpy as np
from scipy.stats import ttest_rel
from collections import namedtuple

# Parser. It's just two positional arguments
ap = argparse.ArgumentParser("kaldi-merge")
ap.add_argument("f1", help="First file")
ap.add_argument("f2", help="Second file")
ap.add_argument("-o", help="Output file of differences")
arg = ap.parse_args()

# Read the file into a tuple of values
Result = namedtuple('Result', ['error', 'total', 'rate'])
def readResult(fn):
    # Read as lines
    with open(fn, 'r') as file:
        t = file.readlines()

    # Count up the errors
    d = []
    error = 0
    total = 0
    for i in range(len(t)-1): # Skip the last line
        if i == 0:            # And the first
            continue
        # Fields: ID #Cor #Sub #Del #Ins #Tol
        #          0    1    2    3    4    5
        f = t[i].split()
        err = int(f[2]) + int(f[3]) + int(f[4])
        tot = int(f[5])
        if tot > 0:
            d.append(err/tot)
        error += err
        total += tot
    return Result(error, total, d)

# Read the two files and report stats
r1 = readResult(arg.f1)
r2 = readResult(arg.f2)
print("Error rate 1: {0} / {1} = {2:2.2f}".format(
    r1.error, r1.total, 100.0 * r1.error / r1.total
    ))
print("Error rate 2: {0} / {1} = {2:2.2f}".format(
    r2.error, r2.total, 100.0 * r2.error / r2.total
   ))

# Output the diffs if need be
if arg.o:
    d = np.array(r1.rate) - np.array(r2.rate)
    np.savetxt(arg.o, d)

# This is basically the same as statcred's one sample t-test with mean=0, but
# just to confirm that me and scipy have the same understanding of what's what,
# and since it's so simple...
(t, p) = ttest_rel(r1.rate, r2.rate)
print("p-value: {0:.5f}".format(p))
