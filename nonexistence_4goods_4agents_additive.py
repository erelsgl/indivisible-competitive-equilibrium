#!python3

"""
Proves the non-existence result for 4 goods and 4 agents
by exhaustively checking all allocations.

See Subsection 6.3, Theorem 4.

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
singletons = list(items)
pairs = preferences.pairs(items)
triplets = preferences.triplets(items)
quartets = preferences.quartets(items)

prefs_of_Alice = quartets + triplets + ["wx", "wy", "wz", "xy", "w", "xz", "yz", "x", "y", "z"] + empty
prefs_of_Bob   = quartets + triplets + pairs + ["w", "z", "x", "y"] + empty
prefs_of_Carl  = quartets + triplets + pairs + ["x", "y", "w", "z"] + empty
prefs_of_Dana  = quartets + triplets + pairs + singletons + empty
prefs = [prefs_of_Alice, prefs_of_Bob, prefs_of_Carl, prefs_of_Dana]
budgets = [160, 130, 90, 66]

print("\nWith the preferences in the paper, there are no competitive equilibria:")
ce.display(ce.find_equilibrium(items, prefs, budgets))

print("\nAs a control, with only the three highest-income agents, a competitive equilibrium exists:")
ce.display(ce.find_equilibrium(items, prefs[0:3], budgets[0:3]))

print("\nWith the preferences in the paper, even a *personalized* equilibrium does not exist:")
ce.display(ce.find_personalized_equilibrium(items, prefs, budgets))
