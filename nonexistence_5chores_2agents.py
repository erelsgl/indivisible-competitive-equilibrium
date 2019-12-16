#!python3

"""
Proves the non-existence result for 5 chores and 2 agents
by exhaustively checking all allocations.

The example is based on Section 7, Theorem 5;
it is converted from goods to chores using the duality theorem.
See Subsection 8.1, Theorem 6.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""


import preferences
import competitive_equilibrium as ce
import sys, logging
if len(sys.argv)<2 or sys.argv[1]!="quiet":
    ce.logger.setLevel(logging.INFO)

items = "vwxyz"

empty = [""]
singletons = list(items)
pairs = preferences.pairs(items)
triplets = preferences.triplets(items)
quartets = preferences.quartets(items)
quintuplets = [items]

triplets_except_xyz = preferences.list_difference(triplets, ["xyz"])
triplets_except_vwx_vwy_vwz_xyz = preferences.list_difference(triplets, ["vwx","vwy","vwz","xyz"])
pairs_except_vw = preferences.list_difference(pairs, ["vw"])

prefs_of_Alice = preferences.goods_to_chores(items, quintuplets + quartets + ["vwx","vwy","vwz","vw","xyz"] + triplets_except_vwx_vwy_vwz_xyz + pairs_except_vw + singletons + empty)
prefs_of_Bob   = preferences.goods_to_chores(items, quintuplets + quartets + triplets_except_xyz + ["vx","vy","vz","wx","wy","wz","xyz","vw","w","v","xy","xz","yz","x","y","z"] + empty)
budgets = [-10,-12]

print("\nWith the preferences in the paper, there are no competitive equilibria:")
ce.display(ce.find_equilibrium(items, [prefs_of_Alice, prefs_of_Bob], budgets, negative_prices=True))

print("\nAs a control, if we slightly change the preferences of Alice, there is a competitive equilibrium:")
alternative_prefs_of_Alice = preferences.goods_to_chores(items, quintuplets + quartets + ["vwx","vwy","vwz","xyz"] + triplets_except_vwx_vwy_vwz_xyz + pairs + singletons + [""])
alternative_prefs_of_Bob   = prefs_of_Bob
ce.display(
    ce.find_equilibrium(items, [alternative_prefs_of_Alice, alternative_prefs_of_Bob], budgets, negative_prices=True))

print("\nWith the original preferences, even a *personalized* competitive equilibrium does not exist.")
ce.display(ce.find_personalized_equilibrium(items, [prefs_of_Alice, prefs_of_Bob], budgets, negative_prices=True))
