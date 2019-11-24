#!python3

"""
Utils for automatically finding pixeps using symbolic computation.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""


from sympy import *
from sympy.abc import a,b,x,y
from sympy.solvers.solveset import linsolve
from itertools import combinations

import logging, sys
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
# To enable tracing, logger.setLevel(logging.INFO)


def budget_equalities(sequence:str, price_vars:list, budget_vars:list)->list:
    """
    Given a picking-sequence, create symbolic equalities determining that the
    total price of each agent's bundle equals the agent's budget.
    Currently works only for 2 agents.

    :param sequence:  a string determining the picking-sequence, e.g. "ABA".
    :param price_vars:    a list of symbols, e.g. symbols('p3,p2,p1')
    :param budgets:   a list of symbols, e.g. symbols('a,b')
    :return: a list of constraints, as expressions that should be equal to 0.

    >>> budgets = symbols("a,b")
    >>> price_vars = symbols('p5,p4,p3,p2,p1')
    >>> budget_equalities("ABABA", price_vars, budgets)
    [a - p1 - p3 - p5, b - p2 - p4]
    >>> budget_equalities("AABBB", price_vars, budgets)
    [a - p4 - p5, b - p1 - p2 - p3]
    """
    num_agents = len(budget_vars)
    if num_agents!=2:
        raise ValueError("Currently only 2 agents are supported")

    price_equality_a = budget_vars[0]
    price_equality_b = budget_vars[1]
    for i in range(len(sequence)):
        picker = sequence[i]
        if picker=="A":
            price_equality_a -= price_vars[i]
        elif picker=="B":
            price_equality_b -= price_vars[i]
        else:
            raise ValueError("Found picker {} but only two agents are supported".format(picker))
    return [price_equality_a,price_equality_b]



def switch_equality(bundle1:str, bundle2:str, prices:list):
    """
    Given two bundles, create a symbolic equality determining that the
    price of these bundles should be equal.

    :param bundle1, bundle2: strings representing bundles, e.g. "21", "4".
    :param prices:  a list of symbols, e.g. symbols('p3,p2,p1')
    :return: a symbolic expressions that should be equal to 0.

    >>> prices = symbols('p5,p4,p3,p2,p1')
    >>> switch_equality("5","42", prices)
    -p2 - p4 + p5
    >>> switch_equality("42","5", prices)
    p2 + p4 - p5
    """
    itemcount = len(prices)
    eq = 0
    for item in bundle1:
        if int(item)>0:
            eq += prices[itemcount-int(item)]
    for item in bundle2:
        if int(item)>0:
            eq -= prices[itemcount-int(item)]
    return eq

def switch_equalities(switches:list, prices:list)->list:
    """
    Given a list of pairs of bundles, create a list of symbolic equalities determining that the
    prices of these bundles should be equal.

    :param switches: a list of strings
    :param prices:  a list of symbols, e.g. symbols('p3,p2,p1')
    :return: a list of constraints, as expressions that should be equal to 0.

    >>> prices = symbols('p5,p4,p3,p2,p1')
    >>> switch_equalities(["5:42", "4:31"], prices)
    [-p2 - p4 + p5, -p1 - p3 + p4]
    """
    eqs = []
    for switch in switches:
        bundle1,bundle2 = switch.split(":")
        eqs.append(switch_equality(bundle1,bundle2,prices))
    return eqs

def budget_range(prices:list):
    """
    Given a list of symbolic expressions of prices,
    returns an interval determining the range of budgets
    by which these prices are decreasing.

    :param prices a list of expressions representing prices, e.g.  [a-b,b]
    :return an interval for the first budget (a), assuming the  second budget (b) equals 1.

    >>> budget_range([a-b,b])  # a > 2b
    Interval.open(2, oo)

    >>> budget_range([a-b,a-b,b/2])
    Interval.open(3/2, oo)

    >>> budget_range([b,a-b,b/2])
    Interval.open(3/2, 2)

    >>> budget_range([b,a-b])
    Interval.open(1, 2)
    """
    result = solveset(a>1, a, S.Reals)
    prices_b1 = [p.subs(b,1) for p in prices] + [0]
    for i in range(len(prices_b1)-1):
        if prices_b1[i] == prices_b1[i+1]:
            continue
        inequality = prices_b1[i] > prices_b1[i+1]
        try:
            solution   = solveset(inequality, a, S.Reals)
        except TypeError:
            print("WARNING: cannot solve inequality {} for a".format(inequality))
            continue
        # print ("{} > {}: {}".format(prices_b1[i], prices_b1[i+1], solution))
        result = result.intersect(solution)
    return result


def show_prices(sequence:str, price_vars:list, budget_eqs:list, switches:list):
    switch_eqs = switch_equalities(switches, price_vars)
    prices_sol = linsolve(budget_eqs + switch_eqs, price_vars).args
    if len(prices_sol)==0:
        logger.info("{}, {}: No prices!".format(sequence, switches))
        return
    prices = prices_sol[0]
    possible_budgets = budget_range(prices)
    if possible_budgets.is_EmptySet:
        logger.info("{}, {}: {}, No budget!".format(sequence, switches, prices))
        return
    else:
        switches_str = ", ".join([str(s) for s in switches])
        print("{}:      handles {}.     Requires a in {}".format("    ".join([str(p) for p in prices]), switches_str, possible_budgets))


def analyze_sequence(sequence:str, undetermined_switches:list, price_vars:list, budget_vars:list):
    print(sequence)
    budget_eqs = budget_equalities(sequence, price_vars, budget_vars)
    num_items = len(price_vars)
    for i in range(num_items):
        added_constraint = "{}:{}".format(i+1,i) # add an equality constraint on two adjacent positions
        show_prices(sequence, price_vars, budget_eqs, undetermined_switches+[added_constraint])
    print()


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
