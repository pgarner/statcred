#!/usr/bin/env python3
#
# Copyright 2019 by Philip N. Garner
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Phil Garner, April 2019
#

import numpy as np
from scipy.stats import ttest_ind
from scipy.special import betainc
from scipy.special import betaincinv

def betacred(k, n, j, p):
    """
    Returns the upper and lower bounds of the credible interval based on a beta
    distribution.
    """
    r = (1.0-p/100)/2
    a = 1
    if j:
        a = 0.5
    l = betaincinv(k+a, n-k+a, r)
    u = betaincinv(k+a, n-k+a, 1.0-r)
    return (l, u)


def doBeta(arg):
    (l, u) = betacred(arg.k, arg.n, arg.j, arg.p)
    print("{0:.1f}% limits: {1:1.3f} {2:1.3f}".format(arg.p, l, u))

def doT(arg):
    if not arg.f:
        raise Exception("t-test needs two files")
    f = []
    for i in range(len(arg.f)):
        f.append(np.loadtxt(arg.f[i]))
    if (len(f) != 2):
        raise Exception("Must be two files for a t-test")

    # Two-sample equal-variance two-tailed t-test
    (s, p) = ttest_ind(f[0], f[1])
    print("p = {0:.3f}".format(p))

# Argument error handler
def doError(arg):
    print("Please specify a command; try -h")


#
# Everything above is just functions,
# the main program starts here with the argument parser
#
# There are subparsers for each distinct test type.
# Each should set a func= to call the appropriate handler
#
import argparse
ap = argparse.ArgumentParser("statcred")
sp = ap.add_subparsers(help="The tests supported in this program")
ap.set_defaults(func=doError)

# The subparsers
apB = sp.add_parser("beta", help="credible interval based on a beta dist.")
apT = sp.add_parser("t", help="t-tests; the data are normally distributed")
apZ = sp.add_parser("z", help="z-tests; the data are approx. normal")

# Beta credibility args
apB.add_argument("-k", type=int, default=0, help="number of successes")
apB.add_argument("-n", type=int, default=0, help="number of trials")
apB.add_argument("-j", action="store_true", help="use the Jeffreys interval")
apB.add_argument("-p", type=float, default=95, help="pertinent percentage")
apB.set_defaults(func=doBeta)

# T args
apT.add_argument("-f", nargs="+",
                 help="data file(s) to be read using numpy.loadtxt")
apT.set_defaults(func=doT)

# All set up, parse it all and call the right handler
arg = ap.parse_args()
arg.func(arg)

# All done; just drop out
# print("Args:", arg)
