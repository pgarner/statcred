#!/usr/bin/env python3
#
# Copyright 2019 by Philip N. Garner
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Phil Garner, April 2019
#

from scipy.special import betainc
from scipy.special import betaincinv

def betacred(k, n, j):
    p = 1
    if j:
        p = 0.5
    l = betaincinv(k+p, n-k+p, 0.025)
    u = betaincinv(k+p, n-k+p, 1.0-0.025)
    return (l, u)
    
import argparse
ap = argparse.ArgumentParser("statcred")
ap.add_argument("-k", type=int, help="number of successes")
ap.add_argument("-n", type=int, help="number of trials")
ap.add_argument("-j", action="store_true", help="use the Jeffreys interval")
arg = ap.parse_args()

(l, u) = betacred(arg.k, arg.n, arg.j)

print("95% limits are: {0:1.3f} {1:1.3f}".format(l, u))
