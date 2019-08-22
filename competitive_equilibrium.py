#!python3

"""
Utils for automatically finding competitive equilibria using linear programming.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""


import numpy as np
from scipy.optimize import linprog
from allocations import allocations

trace = lambda *x: None  # To enable tracing, set trace=print

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


def find_equilibrium_prices(all_items: str, preferences: list, budgets: list, allocation: list, slack=0.001, negative_prices:bool=False) ->list:
    """
    Given an allocation, try to find prices with which this allocation is a competitive equilibrium (return None of not found).

    :param items:    a string in which each char represents an item.
    :param budgets:  a list of numbers, each represents the budget of one agent.
    :param preferences:  a list of lists of strings, each list represents the preference-relation of an agent, from best to worst (by the same order as the budgets).
    :param allocation:   a list of strings, each represents the bundle allocated to one agent (by the same order as the budgets).
    :param slack:     the price of preferred bundles must be larger than the agent's budget by at least this amount. Default=0.001
    :param negative_prices: whether to force all prices to be negative (for allocation of bads/chores). Default=False
    :return: the vector of prices, as returned by scipy.linprog

    >>> budgets = [5, 2]
    >>> preferences = [["xy", "x", "y", ""], ["xy", "x", "y", ""]]
    >>> print(find_equilibrium_prices("xy",preferences,budgets,allocation=["x","y"]))
    [5. 2.]
    >>> print(find_equilibrium_prices("xy",preferences,budgets,allocation=["y","x"]))
    None
    >>> print(find_equilibrium_prices("xy",preferences,budgets,allocation=["xy",""], slack=0.001))
    [2.999 2.001]
    >>> print(find_equilibrium_prices("xy",preferences,budgets,allocation=["","xy"]))
    None
    >>> chore_preferences = [reversed(p) for p in preferences]
    >>> chore_budgets = [-2, -5]
    >>> print(find_equilibrium_prices("xy",chore_preferences,chore_budgets,allocation=["y","x"], negative_prices=True))
    [-5. -2.]
    >>> print(find_equilibrium_prices("xy",chore_preferences,chore_budgets,allocation=["x","y"], negative_prices=True))
    None
    >>> print(find_equilibrium_prices("xy",chore_preferences,chore_budgets,allocation=["xy",""], negative_prices=True))
    None
    >>> print(find_equilibrium_prices("xy",chore_preferences,chore_budgets,allocation=["","xy"], negative_prices=True))
    None
    """
    num_agents = len(budgets)
    if num_agents!=len(preferences):
        raise ValueError("Number of budgets ({}) does not match number of preferences ({})".format(len(budgets), len(preferences)))
    if num_agents!=len(allocation):
        raise ValueError("Number of budgets ({}) does not match number of bundles ({})".format(len(budgets), len(allocation)))

    num_items = len(all_items)

    # The variables of the linear program are the prices - one price per item.
    # We do not care about minimization, so we just set the minimization coefficients to zero:
    minimization_coefficients = np.zeros(num_items)
    # Alternatively, we could look for for a price-vector with the smallest sum subject to the constraints:
    # minimization_coefficients = np.ones(num_items)

    # Create the budget constraints (equalities) -   A_equality * prices  ==  b_equality
    A_equality = []
    b_equality = []
    for i in range(num_agents):
        if len(allocation[i])>0 or budgets[i]<0:
            A_equality.append(bundle_to_row(all_items, allocation[i], 1))
            b_equality.append(budgets[i])

    # Create the preference constraints (inequalities) - A_upperbound * prices  <=  b_upperbound
    A_upperbound = []
    b_upperbound = []
    for i in range(num_agents):
        bundle_allocated_to_i = allocation[i]
        # Loop over all bundles, from the best (for i) down to bundle_allocated_to_i:
        for better_bundle in preferences[i]:
            if better_bundle == bundle_allocated_to_i:
                break   # this and all remaining bundles are worse than bundle_allocated_to_i
            A_upperbound.append(bundle_to_row(all_items, better_bundle, -1))
            b_upperbound.append(-budgets[i]-slack)

    bounds = (None, 0) if negative_prices else (0, None)

    if len(b_upperbound)>0:
        result = linprog(minimization_coefficients,
            A_ub=A_upperbound, b_ub=b_upperbound, A_eq=A_equality, b_eq=b_equality,
            bounds=bounds, method='revised simplex')
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
    else:
        return result.x


def find_equilibrium(all_items:str, preferences:list, budgets:list, slack=0.001, negative_prices:bool=False)->(list,list):
    """
    Given budgets and preferences, find an allocation and price-vector t
    that are a competitive equilibrium (return None of not found)

    :param items:    a string in which each char represents an item.
    :param budgets:  a list of numbers, each represents the budget of one agent.
    :param preferences:  a list of lists of strings, each list represents the preference-relation of an agent, from best to worst (by the same order as the budgets).

    :param slack:     the price of preferred bundles must be larger than the agent's budget by at least this amount. Default=0.001
    :param negative_prices: whether to force all prices to be negative (for allocation of bads/chores). Default=False
    :return: a tuple (allocation, prices).

    >>> preferences = [["xy", "x", "y"], ["xy", "x", "y"]]
    >>> print(find_equilibrium("xy", preferences, [5,2]))
    (['x', 'y'], array([5., 2.]))
    >>> print(find_equilibrium("xy", preferences, [2,3]))
    (['y', 'x'], array([3., 2.]))
    >>> print(find_equilibrium("xy", preferences, [4,4]))
    None
    """
    all_items = "".join(sorted(all_items))
    num_agents = len(budgets)
    if num_agents!=len(preferences):
        raise ValueError("Number of budgets ({}) does not match number of preferences ({})".format(len(budgets), len(preferences)))

    allocation_count = 1
    for allocation in allocations(all_items, num_agents):
        prices = find_equilibrium_prices(all_items, preferences, budgets, allocation, slack=slack, negative_prices=negative_prices)
        if prices is  None:
            trace("{}. Allocation {}:  no equilibrium prices".format(allocation_count, allocation))
        else:
            trace("{}. Allocation {}:  equilibrium prices of {}={}".format(allocation_count, allocation, all_items, prices))
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

    # trace = print
    # preferences = [["xy", "x", "y"], ["xy", "x", "y"]]
    # print("\n Equilibrium with different budgets:")
    # find_equilibrium("xy", preferences, [3, 5])
    # print("\n No equilibrium with equal budgets:")
    # find_equilibrium("xy", preferences, [4, 4])
