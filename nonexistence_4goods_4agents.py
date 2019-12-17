#!python3

"""
Proves the non-existence result for 4 goods and 4 monotonically-increasing agents
by exhaustively checking all allocations.

See Subsection 6.2, Theorem 3.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""


import preferences
import competitive_equilibrium as ce
import sys, logging
if len(sys.argv)<2 or sys.argv[1]!="quiet":
    ce.logger.setLevel(logging.INFO)

items = "wxyz"

empty = [""]
singletons = list(items)               # all singleton subsets in an arbitrary order
pairs = preferences.pairs(items)       # all pairs of items in an arbitrary order
triplets = preferences.triplets(items) # all triplets of items in an arbitrary order
quartets = preferences.quartets(items) # all quartets of items in an arbitrary order

prefs_of_Alice = quartets + triplets + ["wx", "yz", "wy", "xz", "wz", "xy"] + singletons + empty
prefs_of_Bob   = quartets + triplets + pairs + ["w", "x", "y", "z"] + empty
prefs_of_others = quartets + triplets + pairs + singletons + empty
prefs = [prefs_of_Alice, prefs_of_Bob, prefs_of_others, prefs_of_others]
budgets = [20, 11, 8, 1]

print("\nWith the preferences in the paper, there are no competitive equilibria:")
ce.display(ce.find_equilibrium(items, prefs, budgets))

print("\nAs a control, if we change Alice's preferences, there is a competitive equilibrium:")
alternative_prefs_of_Alice = quartets + triplets + ["wx", "wy", "wz", "xy", "xz", "yz"] + singletons
# print(alternative_prefs_of_Alice)
ce.display(ce.find_equilibrium(items, [alternative_prefs_of_Alice, prefs_of_Bob, prefs_of_others, prefs_of_others], budgets))

print("\nWith the original preferences, even a *personalized* competitive equilibrium does not exist.")
ce.display(ce.find_personalized_equilibrium(items, prefs, budgets))
