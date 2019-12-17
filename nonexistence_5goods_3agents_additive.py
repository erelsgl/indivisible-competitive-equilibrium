#!python3

"""
Proves the non-existence result for 5 goods and 3 additive agents
by exhaustively checking all allocations.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-12
"""

import preferences
import competitive_equilibrium as ce
import sys, logging
if len(sys.argv)<2 or sys.argv[1]!="quiet":
    ce.logger.setLevel(logging.INFO)


high_value_goods = "wxyz"
low_value_good = "o"
items = high_value_goods + low_value_good
empty = [""]
singletons = list(high_value_goods)
pairs = preferences.pairs(high_value_goods)
triplets = preferences.triplets(high_value_goods)
quartets = preferences.quartets(high_value_goods)

prefs_of_Alice_4goods = quartets + triplets + ["wx", "wy", "wz", "xy", "w", "xz", "yz", "x", "y", "z"] + empty
prefs_of_Bob_4goods   = quartets + triplets + pairs + ["w", "z", "x", "y"] + empty
prefs_of_Carl_4goods  = quartets + triplets + pairs + ["x", "y", "w", "z"] + empty
prefs_4goods = [prefs_of_Alice_4goods, prefs_of_Bob_4goods, prefs_of_Carl_4goods]

prefs_5goods = [preferences.add_low_value_good(prefs,low_value_good) for prefs in prefs_4goods]
print(prefs_5goods)
budgets = [16, 13, 9]

print("\nWith the preferences in the paper, there are no competitive equilibria:")
ce.display(ce.find_equilibrium(items, prefs_5goods, budgets))

print("\nAs a control, with only the four high-value goods, a CE exists:")
ce.display(ce.find_equilibrium(high_value_goods, prefs_4goods, budgets))

print("\nWith the preferences in the paper, even a *personalized* equilibrium does not exist:")
ce.display(ce.find_personalized_equilibrium(items, prefs_5goods, budgets))
