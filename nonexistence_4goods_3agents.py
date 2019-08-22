#!python3

"""
Proves the non-existence result for 4 goods and 3 agents
by exhaustively checking all allocations.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""


import itertools
import competitive_equilibrium
competitive_equilibrium.trace = print
import preferences

items = "wxyz"

singletons = list(items)
pairs = preferences.pairs(items)
triplets = preferences.triplets(items)
quartets = preferences.quartets(items)

prefs_of_Alice = quartets + triplets + ["wx", "yz", "wy", "xz", "wz", "xy"] + singletons
prefs_of_Bob   = quartets + triplets + pairs + ["w", "x", "y", "z"]
prefs_of_Carl  = quartets + triplets + pairs + singletons
preferences = [prefs_of_Alice, prefs_of_Bob, prefs_of_Carl]
budgets = [20, 11, 8]

print("\nWith the preferences in the paper, there are no competitive equilibria:")
competitive_equilibrium.find_equilibrium(items, preferences, budgets)

print("\nAs a control, if we change Alice's preferences, there is a competitive equilibrium:")
alternative_prefs_of_Alice = quartets + triplets + ["wx", "wy", "wz", "xy", "xz", "yz"] + singletons
print(alternative_prefs_of_Alice)
competitive_equilibrium.find_equilibrium(items, [alternative_prefs_of_Alice, prefs_of_Bob, prefs_of_Carl], budgets)
