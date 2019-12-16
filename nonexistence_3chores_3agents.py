#!python3

"""
Proves the non-existence result for 3 chores and 3 agents
by exhaustively checking all allocations.

See Subsection 8.2, Theorem 7.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""


import competitive_equilibrium as ce
import sys, logging
if len(sys.argv)<2 or sys.argv[1]!="quiet":
    ce.logger.setLevel(logging.INFO)

items = "xyz"

prefs_of_any_agent = ["", "x","y","xy", "z", "zx","zy","zxy"]
prefs = [prefs_of_any_agent, prefs_of_any_agent, prefs_of_any_agent]
budgets = [-7, -8, -9]

print("\nWith budgets as in the paper, there are no competitive equilibria:")
ce.display(ce.find_equilibrium(items, prefs, budgets, negative_prices=True))

print("\nAs a control, if we change the budgets, there is a competitive equilibrium:")
alternative_budgets = [-3, -7, -15]
ce.display(ce.find_equilibrium(items, prefs, alternative_budgets, negative_prices=True))

print("\nEven a *personalized* competitive equilibrium does not exist:")
ce.display(ce.find_personalized_equilibrium(items, prefs, budgets, negative_prices=True))
