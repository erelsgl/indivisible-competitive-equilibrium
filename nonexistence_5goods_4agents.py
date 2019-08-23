#!python3

"""
Proves the non-existence result for 5 goods and 4 agents
by exhaustively checking all allocations.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""

import preferences
import competitive_equilibrium as ce
import sys
if len(sys.argv)<2 or sys.argv[1]!="quiet":
    ce.trace = print


high_value_goods = "wxyz"
low_value_good = "o"
all_items = high_value_goods + low_value_good
empty = [""]
singletons = list(high_value_goods)
pairs = preferences.pairs(high_value_goods)
triplets = preferences.triplets(high_value_goods)
quartets = preferences.quartets(high_value_goods)

prefs_of_Alice = preferences.add_low_value_good(quartets + triplets + ["wx", "wy", "wz", "xy", "w", "xz", "yz", "x", "y", "z"] + empty, low_value_good)
prefs_of_Bob   = preferences.add_low_value_good(quartets + triplets + pairs + ["w", "z", "x", "y"] + empty, low_value_good)
prefs_of_Carl  = preferences.add_low_value_good(quartets + triplets + pairs + ["x", "y", "w", "z"] + empty, low_value_good)
prefs_of_Dana  = preferences.add_low_value_good(quartets + triplets + pairs + singletons + empty, low_value_good)
prefs = [prefs_of_Alice, prefs_of_Bob, prefs_of_Carl, prefs_of_Dana]
budgets = [16, 11, 9, 6]

print("\nWith the preferences in the paper, there are no competitive equilibria:")
ce.display(ce.find_equilibrium(all_items, prefs, budgets))

print("\nAs a control, if we change the budgets, there is a competitive equilibrium:")
alternative_budgets = [18, 11, 9, 6]
ce.display(ce.find_equilibrium(all_items, prefs, alternative_budgets))
