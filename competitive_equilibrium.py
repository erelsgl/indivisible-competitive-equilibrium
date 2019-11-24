#!python3

"""
Utils for automatically finding competitive equilibria using linear programming.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""


import numpy as np
from scipy.optimize import linprog
from allocations import allocations

import logging, sys
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
# To enable tracing, logger.setLevel(logging.INFO)

def bundle_to_row(all_items:str, bundle:str, coefficient:float)->list:
    """
    Given a bundle (as a string),
          construct a row of coefficients that represents this bundle.
    :param all_items:  a string representing all items in a certain fixed order.
    :param bundle:     a string representing a subset of the items.
    :param coefficient: the coefficient to put in the row for each item in the bundle.
    :return:  a list where all locations that correspond to the bundle equal coefficient, and all others equal 0.

    >>> bundle_to_row("wxyz", "wy", 1)
    [1, 0, 1, 0]
    >>> bundle_to_row("wxyz", "", 1)
    [0, 0, 0, 0]
    >>> bundle_to_row("wxyz", "zxyw", -1)
    [-1, -1, -1, -1]
    """
    result = len(all_items) * [0]
    for item in bundle:
        result[all_items.index(item)] = coefficient
    return result


def find_equilibrium_prices(all_items: str, preferences: list, budgets: list, allocation: list,
                            negative_prices: bool = False) ->list:
    """
    Given an allocation, try to find prices with which this allocation is a competitive equilibrium (return None of not found).

    :param items:    a string in which each char represents an item.
    :param budgets:  a list of numbers, each represents the budget of one agent.
    :param preferences:  a list of lists of strings, each list represents the preference-relation of an agent, from best to worst (by the same order as the budgets).
    :param allocation:   a list of strings, each represents the bundle allocated to one agent (by the same order as the budgets).
    :param negative_prices: whether to force all prices to be negative (for allocation of bads/chores). Default=False
    :return: the vector of prices, as returned by scipy.linprog

    >>> budgets = [5, 2]
    >>> preferences = [["xy", "x", "y", ""], ["xy", "x", "y", ""]]
    >>> print(find_equilibrium_prices("xy",preferences,budgets,allocation=["x","y"]))
    [5. 2.]
    >>> print(find_equilibrium_prices("xy",preferences,budgets,allocation=["y","x"]))
    None
    >>> print(find_equilibrium_prices("xy",preferences,budgets,allocation=["xy",""]))
    [2.5 2.5]
    >>> print(find_equilibrium_prices("xy",preferences,budgets,allocation=["","xy"]))
    None
    >>> chore_preferences = [reversed(p) for p in preferences]
    >>> chore_budgets = [-2, -5]
    >>> print(find_equilibrium_prices("xy",chore_preferences,chore_budgets,allocation=["y","x"],negative_prices=True))
    [-5. -2.]
    >>> print(find_equilibrium_prices("xy",chore_preferences,chore_budgets,allocation=["x","y"],negative_prices=True))
    None
    >>> print(find_equilibrium_prices("xy",chore_preferences,chore_budgets,allocation=["xy",""],negative_prices=True))
    None
    >>> print(find_equilibrium_prices("xy",chore_preferences,chore_budgets,allocation=["","xy"],negative_prices=True))
    None
    """
    num_agents = len(budgets)
    if num_agents!=len(preferences):
        raise ValueError("Number of budgets ({}) does not match number of preferences ({})".format(len(budgets), len(preferences)))
    if num_agents!=len(allocation):
        raise ValueError("Number of budgets ({}) does not match number of bundles ({})".format(len(budgets), len(allocation)))

    num_items = len(all_items)

    # The linear program has num_items + 1 variables:
    # * A variable for each item, representing the item price;
    # * A "slack" variable, that represents how higher are the costs of preferred bundles than the budget of the agent.
    # We maximize the value of the slack variable. If the max value is positive, then a solution exists.
    # I am grateful to Inbal Talgam-Cohen for the algorithm idea.

    minimization_coefficients = np.concatenate((np.zeros(num_items), -np.ones(1))) # maximize the slack

    # Create the budget constraints (equalities):
    #      bundle_i   * prices  == budget_i
    #      A_equality * prices  == b_equality
    A_equality = []
    b_equality = []
    for i in range(num_agents):
        if len(allocation[i])>0 or budgets[i]<0:
            row = bundle_to_row(all_items, allocation[i], 1)
            row.append(0)    # the slack is irrelevant for the budget equalities
            A_equality.append(row)
            b_equality.append(budgets[i])

    # Create the preference constraints (inequalities):
    #    better_bundle_i    * prices  >  budget_i
    #    better_bundle_i    * prices  -  slack  >=    budget_i
    #    - better_bundle_i  * prices  +  slack  <=  - budget_i
    #    A_upperbound       * [prices , slack]  <=  b_upperbound

    A_upperbound = []
    b_upperbound = []
    for i in range(num_agents):
        bundle_allocated_to_i = allocation[i]
        # Loop over all bundles, from the best (for i) down to bundle_allocated_to_i:
        for better_bundle in preferences[i]:
            if better_bundle == bundle_allocated_to_i:
                break   # this and all remaining bundles are worse than bundle_allocated_to_i
            row = bundle_to_row(all_items, better_bundle, -1)
            row.append(1)      # coefficient of the slack variable
            A_upperbound.append(row)
            b_upperbound.append(-budgets[i])

    bounds = [(None, 0) if negative_prices else (0, None)] * num_items
    bounds.append((0,None))   # the slack variable is always weakly-positive

    if len(b_upperbound)>0:
        try:
            result = linprog(minimization_coefficients,
                A_ub=A_upperbound, b_ub=b_upperbound, A_eq=A_equality, b_eq=b_equality,
                bounds=bounds, method='revised simplex')
        except ValueError:
            print("Error!")
            print("A_ub=")
            print(A_upperbound)
            print("b_ub=")
            print(b_upperbound)
            return None  # No feasible solution
    else:
        result = linprog(minimization_coefficients,
            A_eq=A_equality, b_eq=b_equality,
            bounds=bounds, method='revised simplex')
    if result.status==1:
        raise ValueError("Iteration limit reached")
    elif result.status == 2:
        return None  # No feasible solution
    elif result.status==4:
        raise ValueError("Numerical difficulties encountered")
    else: # received result
        prices = result.x[0:-1]
        slack = result.x[-1]
        if slack > 0:
            return prices
        else:  # slack=0
            return None


def find_equilibrium(all_items: str, preferences: list, budgets: list, negative_prices: bool = False) ->(list, list):
    """
    Given budgets and preferences, find an allocation and price-vector t
    that are a competitive equilibrium (return None of not found)

    :param items:    a string in which each char represents an item.
    :param budgets:  a list of numbers, each represents the budget of one agent.
    :param preferences:  a list of lists of strings, each list represents the preference-relation of an agent, from best to worst (by the same order as the budgets).

    :param negative_prices: whether to force all prices to be negative (for allocation of bads/chores). Default=False
    :return: a tuple (allocation, prices).

    >>> preferences = [["xy", "x", "y"], ["xy", "x", "y"]]
    >>> print(find_equilibrium("xy",preferences,[5,2]))
    (['x', 'y'], array([5., 2.]))
    >>> print(find_equilibrium("xy",preferences,[2,3]))
    (['y', 'x'], array([3., 2.]))
    >>> print(find_equilibrium("xy",preferences,[4,4]))
    None
    """
    all_items = "".join(sorted(all_items))
    num_agents = len(budgets)
    if num_agents!=len(preferences):
        raise ValueError("Number of budgets ({}) does not match number of preferences ({})".format(len(budgets), len(preferences)))

    allocation_count = 1
    for allocation in allocations(all_items, num_agents):
        prices = find_equilibrium_prices(all_items, preferences, budgets, allocation, negative_prices=negative_prices)
        if prices is  None:
            logger.info("{}. Allocation {}:  no equilibrium prices".format(allocation_count, allocation))
        else:
            logger.info("{}. Allocation {}:  equilibrium prices of {}={}".format(allocation_count, allocation, all_items, prices))
            return (allocation, prices)
        allocation_count += 1
    return None

def display(equilibrium:tuple):
    """
    Pretty-print the result of find_equilibrium
    :param equilibrium: a tuple returned from find_equilibrium.
    :return:
    """
    if equilibrium is None:
        print("No competitive equilibrium")
    else:
        allocation = equilibrium[0]
        prices = equilibrium[1]
        all_items = "".join(sorted("".join(allocation)))
        print("Allocation {}:  equilibrium prices of {}={}".format(allocation, all_items, prices))


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
