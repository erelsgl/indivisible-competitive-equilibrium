#!python3

"""
Proves the non-equilibrium result for 4 goods and 2 agents.

See Appendix A.3, Lemma 9.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""

import preferences
import competitive_equilibrium as ce
import sys, logging
from agents import Agent

if len(sys.argv)<2 or sys.argv[1]!="quiet":
    ce.logger.setLevel(logging.INFO)

items = "wxyz"
singletons = list(items)
pairs = preferences.pairs(items)
triplets = preferences.triplets(items)
quartets = preferences.quartets(items)

prefs_of_any_agent = quartets + triplets + ["wx","wy","wz","xy","xz","w","yz","x","y","z",""]
preferences = [prefs_of_any_agent, prefs_of_any_agent]
budgets = [9, 7]  # or any other  a,b such that 2a/3 < b < a

allocation = ["wx","yz"]
print("\nFor the allocation in the appendix {}, there are no CE prices:".format(allocation))
print(ce.find_equilibrium_prices(items, preferences, budgets, allocation))

another_allocation = ["wy","xz"]
print("\nAs a control, for another allocation {}, there are CE prices:".format(another_allocation))
print(ce.find_equilibrium_prices(items, preferences, budgets, another_allocation))
