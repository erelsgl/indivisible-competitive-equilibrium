#!python3

"""
Proves the non-existence result for 5 goods and 3 agents
by exhaustively checking all allocations.

See Appendix D, Theorem 8.

This is a generalization of the proof for 5 goods and 2 agents; see Appendix D.

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

triplets_except_xyz = [t for t in triplets if t!="xyz"]

prefs_of_Alice = quintuplets + quartets + ["vwx","vwy","vwz","vw","xyz"] + triplets + pairs + singletons + empty
prefs_of_Bob   = quintuplets + quartets + triplets_except_xyz + ["vx","vy","vz","wx","wy","wz","xyz","vw","w","v","xy","xz","yz","x","y","z"] + empty
prefs_of_Carl  = quintuplets + quartets + triplets + pairs + singletons + empty
prefs = [prefs_of_Alice, prefs_of_Bob, prefs_of_Carl]
budgets = [12, 10, 1]  # or any other a,b,c such that a > b+c and > 3(a+c)/4

print("\nWith the preferences in the paper, there are no competitive equilibria:")
ce.display(ce.find_equilibrium(items, prefs, budgets))

print("\nAs a control, if we slightly change the preferences of Alice, there is a competitive equilibrium:")
alternative_prefs_of_Alice = quintuplets + quartets + ["vwx","vwy","vwz","vw"] + triplets + pairs + singletons
alternative_prefs_of_Bob   = prefs_of_Bob
ce.display(ce.find_equilibrium(items, [alternative_prefs_of_Alice, alternative_prefs_of_Bob, prefs_of_Carl], budgets))
