#!python3

"""
Proves the non-existence result for 4 goods and 5 agents
by exhaustively checking all allocations.

See Subsection 6.3, Theorem 4 (extended to 5 agents).

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
prefs_of_Others  = quartets + triplets + pairs + singletons + empty
prefs = [prefs_of_Alice, prefs_of_Bob, prefs_of_Carl, prefs_of_Others, prefs_of_Others]
budgets = [16, 11, 9, 6, 5]

print("\nWith the preferences in the paper, there are no competitive equilibria:")
ce.display(ce.find_equilibrium(items, prefs, budgets))

print("\nAs a control, if we change the budgets, there is a competitive equilibrium:")
alternative_budgets = [18, 11, 9, 6, 5]
ce.display(ce.find_equilibrium(items, prefs, alternative_budgets))

print("\nInterestingly, a *personalized* competitive equilibrium exists!")
ce.display(ce.find_personalized_equilibrium(items, prefs, budgets))
# Allocation ['wx', 'z', 'y', '', '']:  equilibrium prices of wxyz=[
#  [11.   5.   9.  11. ]
#  [12.5  3.5  9.  11. ]
#  [ 3.5 12.5  9.  11. ]
#  [ 8.   8.   9.  11. ]
#  [ 8.   8.   9.  11. ]]
