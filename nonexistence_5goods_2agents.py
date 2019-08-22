#!python3

"""
Proves the non-existence result for 5 goods and 2 agents
by exhaustively checking all allocations.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""


import itertools
import competitive_equilibrium
competitive_equilibrium.trace = print
import preferences

items = "vwxyz"


singletons = list(items)
pairs = preferences.pairs(items)
triplets = preferences.triplets(items)
quartets = preferences.quartets(items)
quintuplets = [items]

triplets_except_xyz = [t for t in triplets if t!="xyz"]

prefs_of_Alice = quintuplets + quartets + ["vwx","vwy","vwz","vw","xyz"] + triplets + pairs + singletons
prefs_of_Bob   = quintuplets + quartets + triplets_except_xyz + ["vx","vy","vz","wx","wy","wz","xyz","vw","w","v","xy","xz","yz","x","y","z"]
preferences = [prefs_of_Alice, prefs_of_Bob]
budgets = [12,10]  # or any other a,b such that a > b > 3a/4

print("\nWith the preferences in the paper, there are no competitive equilibria:")
competitive_equilibrium.find_equilibrium(items, preferences, budgets)

print("\nAs a control, if we slightly change the preferences of Alice, there is a competitive equilibrium:")
alternative_prefs_of_Alice = quintuplets + quartets + ["vwx","vwy","vwz","vw"] + triplets + pairs + singletons
alternative_prefs_of_Bob   = prefs_of_Bob
competitive_equilibrium.find_equilibrium(items, [alternative_prefs_of_Alice, alternative_prefs_of_Bob], budgets)
