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

def betacred(k, n, j, p):
    r = (1.0-p/100)/2
    a = 1
    if j:
        a = 0.5
    l = betaincinv(k+a, n-k+a, r)
    u = betaincinv(k+a, n-k+a, 1.0-r)
    return (l, u)



import argparse
ap = argparse.ArgumentParser("statcred")
ap.add_argument("-k", type=int, default=0, help="number of successes")
ap.add_argument("-n", type=int, default=0, help="number of trials")
ap.add_argument("-j", action="store_true", help="use the Jeffreys interval")
ap.add_argument("-p", type=float, default=95, help="pertinent percentage")
arg = ap.parse_args()

(l, u) = betacred(arg.k, arg.n, arg.j, arg.p)

print("{0:.1f}% limits: {1:1.3f} {2:1.3f}".format(arg.p, l, u))

# print(arg)
