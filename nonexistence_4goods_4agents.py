#!python3

"""
Proves the non-existence result for 4 goods and 4 agents
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

prefs_of_Alice = quartets + triplets + ["wx", "wy", "wz", "xy", "w", "xz", "yz", "x", "y", "z"]
prefs_of_Bob   = quartets + triplets + pairs + ["w", "z", "x", "y"]
prefs_of_Carl  = quartets + triplets + pairs + ["x", "y", "w", "z"]
prefs_of_Dana  = quartets + triplets + pairs + singletons
preferences = [prefs_of_Alice, prefs_of_Bob, prefs_of_Carl, prefs_of_Dana]
budgets = [16, 11, 9, 6]

print("\nWith the preferences in the paper, there are no competitive equilibria:")
competitive_equilibrium.find_equilibrium(items, preferences, budgets)

print("\nAs a control, if we change the budgets, there is a competitive equilibrium:")
alternative_budgets = [18, 11, 9, 6]
competitive_equilibrium.find_equilibrium(items, preferences, alternative_budgets)
