#!python3

"""
Proves the non-existence result for 5 goods and 2 agents
by exhaustively checking all allocations.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""


import preferences
import competitive_equilibrium as ce
import sys
if len(sys.argv)<2 or sys.argv[1]!="quiet":
    ce.trace = print

items = "vwxyz"


empty = [""]
singletons = list(items)
pairs = preferences.pairs(items)
triplets = preferences.triplets(items)
quartets = preferences.quartets(items)
quintuplets = [items]

triplets_except_xyz = preferences.list_difference(triplets, ["xyz"])
triplets_except_vwx_vwy_vwz_xyz = preferences.list_difference(triplets, ["vwx","vwy","vwz","vw","xyz"])
pairs_except_vw = preferences.list_difference(pairs, ["vw"])

prefs_of_Alice = quintuplets + quartets + ["vwx","vwy","vwz","vw","xyz"] + triplets_except_vwx_vwy_vwz_xyz + pairs_except_vw + singletons + empty
prefs_of_Bob   = quintuplets + quartets + triplets_except_xyz + ["vx","vy","vz","wx","wy","wz","xyz","vw","w","v","xy","xz","yz","x","y","z"] + empty
budgets = [12,10]  # or any other a,b such that a > b > 3a/4

print("\nWith the preferences in the paper, there are no competitive equilibria:")
ce.display(ce.find_equilibrium(items, [prefs_of_Alice, prefs_of_Bob], budgets))

print("\nAs a control, if we slightly change the preferences of Alice, there is a competitive equilibrium:")
alternative_prefs_of_Alice = quintuplets + quartets + ["vwx","vwy","vwz","xyz"] + triplets_except_vwx_vwy_vwz_xyz + pairs + singletons
alternative_prefs_of_Bob   = prefs_of_Bob
ce.display(ce.find_equilibrium(items, [alternative_prefs_of_Alice, alternative_prefs_of_Bob], budgets))
