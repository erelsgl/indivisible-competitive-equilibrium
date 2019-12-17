#!python3

"""
Proves the non-existence result for 5 goods and 4 agents
by exhaustively checking all allocations.

The example is based on  Subsection 6.3, Theorem 4,
with an additional "low-value item"
as described in Subsection 6.2, Lemma 4.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
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

prefs_of_Alice = preferences.add_low_value_good(quartets + triplets + ["wx", "wy", "wz", "xy", "w", "xz", "yz", "x", "y", "z"] + empty, low_value_good)
prefs_of_Bob   = preferences.add_low_value_good(quartets + triplets + pairs + ["w", "z", "x", "y"] + empty, low_value_good)
prefs_of_Carl  = preferences.add_low_value_good(quartets + triplets + pairs + ["x", "y", "w", "z"] + empty, low_value_good)
prefs_of_Dana  = preferences.add_low_value_good(quartets + triplets + pairs + singletons + empty, low_value_good)
prefs = [prefs_of_Alice, prefs_of_Bob, prefs_of_Carl, prefs_of_Dana]
budgets = [160, 130, 90, 66]

print("\nWith the preferences in the paper, there are no competitive equilibria:")
ce.display(ce.find_equilibrium(items, prefs, budgets))

print("\nWith only the three highest-income agents, a competitive equilibrium exists:")
ce.display(ce.find_equilibrium(items, prefs[0:3], budgets[0:3]))

print("\nWith the preferences in the paper, even a *personalized* equilibrium does not exist:")
ce.display(ce.find_personalized_equilibrium(items, prefs, budgets))
