#!python3

"""
Tries to automatically find pixeps in the case of 5 goods and 2 additive identical agents.
"""


from find_pixep_symbolic import *


budget_vars = symbols("a,b")
price_vars = symbols('p5,p4,p3,p2,p1')


def analyze_sequence(sequence:str, undetermined_switches:list, price_vars:list, budget_vars:list):
    print(sequence)
    budget_eqs = budget_equalities(sequence, price_vars, budget_vars)
    if len(undetermined_switches)>=3:
        for switch_triplets in combinations(undetermined_switches, 3):
            show_prices(sequence, price_vars, budget_eqs, switch_triplets)
    else: # len(undetermined_switches)==2:
        for constraint in ["5:4","4:3","3:2","2:1","1:0"]:
            show_prices(sequence, price_vars, budget_eqs, undetermined_switches+[constraint])
    print()


# analyze_sequence("ABABA", ["5:42","51:42","4:31"], price_vars, budget_vars)
# analyze_sequence("ABABA", ["5:42","4:31"], price_vars, budget_vars)
# analyze_sequence("ABABA", ["51:42","4:31"], price_vars, budget_vars)
# analyze_sequence("ABABA", ["51:42","5:42"], price_vars, budget_vars)

# analyze_sequence("ABBAA", ["5:43", "51:43", "52:43", "3:21", "4:21"], price_vars, budget_vars)
analyze_sequence("ABBAA", ["5:43", "3:21"], price_vars, budget_vars)
analyze_sequence("ABBAA", ["5:43", "4:21"], price_vars, budget_vars)
analyze_sequence("ABBAA", ["52:43", "3:21"], price_vars, budget_vars)
analyze_sequence("ABBAA", ["52:43", "4:21"], price_vars, budget_vars)

# analyze_sequence("BAABA", ["5:31", "5:41", "5:43", "52:43"], price_vars, budget_vars)
# analyze_sequence("BAAAB", ["5:43", "5:42", "51:43", "51:42", "5:32"], price_vars, budget_vars)
# analyze_sequence("ABBBA", ["5:43", "5:42", "5:32", "5:432"], price_vars, budget_vars)
# analyze_sequence("ABBBA", ["5:432","5:4","4:3","3:2","2:1","1:0"], price_vars, budget_vars)
