#!python3

"""
Proves the non-existence result for 3 goods and 3 agents (Appendix D),
by exhaustively checking all allocations.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""

import preferences
import competitive_equilibrium as ce
import sys
if len(sys.argv)<2 or sys.argv[1]!="quiet":
    ce.trace = print


items = "xyz"
prefs_of_Alice = ["xyz", "xy","yz","xz", "x","y","z", ""]
prefs_of_Bob   = ["xyz", "xy","xz","yz", "y","x","z", ""]
prefs_of_Carl  = preferences.triplets(items) + preferences.pairs(items) + list(items) + [""]
budget_of_Alice = budget_of_Bob = 4;  budget_of_Carl = 2   # or any other a,b,c such that a=b > c

print("\nWith only Alice and Bob, no competitive equilibria exists:")
ce.display(ce.find_equilibrium(items, [prefs_of_Alice, prefs_of_Bob], [budget_of_Alice,budget_of_Bob]))

print("\nWith all three agents, a competitive equilibrium exists:")
ce.display(ce.find_equilibrium(items, [prefs_of_Alice, prefs_of_Bob, prefs_of_Carl], [budget_of_Alice,budget_of_Bob,budget_of_Carl]))
