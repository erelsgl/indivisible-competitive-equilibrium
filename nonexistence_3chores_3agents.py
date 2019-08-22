#!python3

"""
Proves the non-existence result for 3 chores and 3 agents
by exhaustively checking all allocations.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""


import itertools
import competitive_equilibrium
competitive_equilibrium.trace = print
import preferences

items = "xyz"


prefs_of_any_agent = ["", "x","y","xy", "z", "zx","zy","zxy"]
preferences = [prefs_of_any_agent, prefs_of_any_agent, prefs_of_any_agent]
budgets = [-7, -8, -9]

print("\nWith budgets as in the paper, there are no competitive equilibria:")
competitive_equilibrium.find_equilibrium(items, preferences, budgets)

print("\nAs a control, if we change the budgets, there is a competitive equilibrium:")
alternative_budgets = [-3, -7, -15]
competitive_equilibrium.find_equilibrium(items, preferences, alternative_budgets)
