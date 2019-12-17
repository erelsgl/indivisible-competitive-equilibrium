#!python3

"""
Utils for automatically finding competitive equilibria using linear programming.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""


import numpy as np
from scipy.optimize import linprog
from allocations import allocations
from agents import Agent

import logging, sys
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
# To enable tracing, logger.setLevel(logging.INFO)




def is_equilibrium_price(all_items: str, preferences: list, budgets: list, allocation: list, prices:list)->bool:
    """
    Check if the given price-vector satisfies the CE conditions for all agents.

    :param all_items:    a string in which each char represents an item.
    :param budgets:      a list of numbers, each represents the budget of one agent.
    :param preferences:  a list of lists of strings, each list represents the preference-relation of an agent, from best to worst (by the same order as the budgets).
    :param allocation:   a list of strings, each represents the bundle allocated to one agent (by the same order as the budgets).
    :param prices:       the price-vector to check; one price per item.

    :return: True or False

    >>> prefs = 2*[["xy", "x", "y", ""]]
    >>> is_equilibrium_price("xy", prefs, [5,2], ["x","y"], prices=[5,2])
    True
    >>> is_equilibrium_price("xy", prefs, [5,2], ["x","y"], prices=[5,3])
    False
    >>> is_equilibrium_price("xy", prefs, [5,2], ["y","x"], prices=[5,2])
    False
    >>> prefs = 2*[["xyo", "xy", "xo", "x", "yo", "y", "o", ""]]
    >>> is_equilibrium_price("xyo", prefs, [5,2], ["x","yo"], prices=[5, 1.5, 0.5])
    True
    >>> is_equilibrium_price("xyo", prefs, [5,2], ["x","oy"], prices=[5, 1.5, 0.5])
    True
    >>> is_equilibrium_price("xyo", prefs, [5,2], ["xo","y"], prices=[4.5, 2, 0.5])
    True
    >>> is_equilibrium_price("xyo", prefs, [5,2], ["ox","y"], prices=[4.5, 2, 0.5])
    True
    """
    agents = Agent.profile(preferences)
    num_agents = len(agents)

    for i in range(num_agents):
        bundle_of_i = allocation[i]
        budget_of_i = budgets[i]
        bundle_of_i_price = _bundle_price(all_items, bundle_of_i, prices)

        # Check CE condition 1 - budget condition:
        if bundle_of_i_price!=budgets[i]:
           logger.info("The bundle of agent %d costs %f while his budget is %f", i, bundle_of_i_price, budget_of_i)
           return False

        # Check CE condition 2 - preference condition:
        if not _is_condition_2_satisfied_for_agent(all_items, agents[i], budget_of_i, bundle_of_i, prices):
            return False

    return True



def is_equilibrium_price_for_agent(all_items: str, preferences: list, budgets: list, allocation: list, prices:list, agent_index:int)->bool:
    """
    Check if the given price-vector is a "personalized competitive equilibrium" for the given agent.
    This means that condition 1 should be satisfied for all agents, but condition 2 may be satisfied only for the given agent.

    :param all_items:    a string in which each char represents an item.
    :param budgets:      a list of numbers, each represents the budget of one agent.
    :param preferences:  a list of lists of strings, each list represents the preference-relation of an agent, from best to worst (by the same order as the budgets).
    :param allocation:   a list of strings, each represents the bundle allocated to one agent (by the same order as the budgets).
    :param prices:       the price-vector to check; one price per item.
    :param agent_index:  the checked agent.

    :return: True or False

    >>> prefs = 2*[["xy", "x", "y", ""]]
    >>> is_equilibrium_price_for_agent("xy", prefs, [5,2], ["x","y"], prices=[5,2], agent_index=0)
    True
    >>> is_equilibrium_price_for_agent("xy", prefs, [5,2], ["x","y"], prices=[5,2], agent_index=1)
    True
    >>> is_equilibrium_price_for_agent("xy", prefs, [5,2], ["x","y"], prices=[5,3], agent_index=0)
    False
    >>> is_equilibrium_price_for_agent("xy", prefs, [5,2], ["x","y"], prices=[5,3], agent_index=1)
    False
    >>> is_equilibrium_price_for_agent("xy", prefs, [5,2], ["y","x"], prices=[2,5], agent_index=0)
    False
    >>> is_equilibrium_price_for_agent("xy", prefs, [5,2], ["y","x"], prices=[2,5], agent_index=1)
    True
    >>> prefs = 2*[["xyo", "xy", "xo", "x", "yo", "y", "o", ""]]
    >>> is_equilibrium_price_for_agent("xyo", prefs, [5,2], ["x","yo"], prices=[5, 1.5, 0.5], agent_index=0)
    True
    >>> is_equilibrium_price_for_agent("xyo", prefs, [5,2], ["xo","y"], prices=[4.5, 2, 0.5], agent_index=0)
    True
    >>> is_equilibrium_price_for_agent("xyo", prefs, [5,2], ["ox","y"], prices=[4.5, 2, 0.5], agent_index=0)
    True
    """
    agents = Agent.profile(preferences)
    num_agents = len(agents)

    for i in range(num_agents):
        bundle_of_i = allocation[i]
        budget_of_i = budgets[i]
        bundle_of_i_price = _bundle_price(all_items, bundle_of_i, prices)

        # Check CE condition 1 - budget condition:
        if bundle_of_i_price!=budgets[i]:
           logger.info("The bundle of agent %d costs %f while his budget is %f", i, bundle_of_i_price, budget_of_i)
           return False

    # Check CE condition 2 - preference condition - only for agent_index:
    if not _is_condition_2_satisfied_for_agent(all_items, agents[agent_index], budgets[agent_index], allocation[agent_index], prices):
        return False

    return True




def find_equilibrium(all_items: str, preferences: list, budgets: list, negative_prices: bool = False) ->(list, list):
    """
    Given budgets and preferences, find an allocation and price-vector p
    that are a competitive equilibrium (return None of not found)

    :param all_items:    a string in which each char represents an item.
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

    agents = Agent.profile(preferences)
    num_agents = len(agents)
    if num_agents!=len(budgets):
        raise ValueError("Number of budgets ({}) does not match number of preferences ({})".format(len(budgets), len(preferences)))

    allocation_count = 1
    for allocation in allocations(all_items, num_agents):
        prices = find_equilibrium_prices(all_items, agents, budgets, allocation, negative_prices=negative_prices)
        if prices is  None:
            logger.info("%d. Allocation %s:  no equilibrium prices", allocation_count, allocation)
        else:
            logger.info("%d. Allocation %s:  equilibrium prices of %s=%s", allocation_count, allocation, all_items, prices)
            return (allocation, prices)
        allocation_count += 1
    return None



def find_equilibrium_prices(all_items: str, preferences: list, budgets: list, allocation: list,
                            negative_prices: bool = False) ->list:
    """
    Given an allocation, try to find prices with which this allocation is a competitive equilibrium (return None of not found).

    :param all_items:    a string in which each char represents an item.
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
    >>> chore_preferences = [list(reversed(p)) for p in preferences]
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
    agents = Agent.profile(preferences)
    # print([a.preferences for a in agents])
    num_agents = len(agents)
    if num_agents!=len(budgets):
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
    bounds = _price_bounds(num_items, negative_prices)

    # Create the budget constraints (equalities):
    #      bundle_i   * prices  == budget_i
    #      A_equality * prices  == b_equality
    (A_equality, b_equality) = _budget_constraints(all_items, budgets, allocation)

    # Create the preference constraints (inequalities):
    #    better_bundle_i    * prices  >  budget_i
    #    better_bundle_i    * prices  -  slack  >=    budget_i
    #    - better_bundle_i  * prices  +  slack  <=  - budget_i
    #    A_upperbound       * [prices , slack]  <=  b_upperbound
    (A_upperbound, b_upperbound) = _preference_constraints(all_items, agents, budgets, allocation)

    result = _solve_linear_program(minimization_coefficients, A_equality, b_equality, A_upperbound, b_upperbound, bounds)
    if result is None:
        return None
    prices = result.x[0:-1]
    slack = result.x[-1]
    if slack > 0:
        return prices
    else:
        logger.info("The slack is zero - so no solution exists")
        return None






def find_personalized_equilibrium(all_items: str, preferences: list, budgets: list, negative_prices: bool = False) ->(list, list):
    """
    Given budgets and preferences, find an allocation and n price-vectors p1,...,pn,
    such that for each agent i, (X,pi) looks like a competitive equilibrium.

    A personalized CE has all the fairness properties of a CE, but does not have its efficiency properties.

    :param items:    a string in which each char represents an item.
    :param budgets:  a list of numbers, each represents the budget of one agent.
    :param preferences:  a list of lists of strings, each list represents the preference-relation of an agent, from best to worst (by the same order as the budgets).

    :param negative_prices: whether to force all prices to be negative (for allocation of bads/chores). Default=False
    :return: a tuple (allocation, prices).

    >>> preferences = [["xy", "x", "y"], ["xy", "x", "y"]]
    >>> allocation,prices = find_personalized_equilibrium("xy",preferences,[5,2])
    >>> allocation
    ['x', 'y']
    >>> print(prices)
    [array([5., 2.]), array([5., 2.])]
    >>> allocation,prices = find_personalized_equilibrium("xy",preferences,[2,3])
    >>> allocation
    ['y', 'x']
    >>> print(prices)
    [array([3., 2.]), array([3., 2.])]
    >>> print(find_personalized_equilibrium("xy",preferences,[4,4]))
    None
    """
    all_items = "".join(sorted(all_items))

    agents = Agent.profile(preferences)
    num_agents = len(agents)
    if num_agents!=len(budgets):
        raise ValueError("Number of budgets ({}) does not match number of preferences ({})".format(len(budgets), len(preferences)))

    allocation_count = 1
    for allocation in allocations(all_items, num_agents):
        prices = find_personalized_equilibrium_prices(all_items, agents, budgets, allocation, negative_prices=negative_prices)
        agents_with_valid_prices = [i for i in range(num_agents) if prices[i] is not None]
        if len(agents_with_valid_prices)<num_agents:
            logger.info("%d. Allocation %s:  personalized equilibrium prices only for %s", allocation_count, allocation, agents_with_valid_prices)
        else:
            logger.info("%d. Allocation %s:  personalized equilibrium prices for all agents: p(%s)=%s", allocation_count, allocation, all_items, prices)
            return (allocation, prices)
        allocation_count += 1
    return None



def find_personalized_equilibrium_prices(all_items: str, preferences: list, budgets: list, allocation: list,
                                         negative_prices: bool = False) ->list:
    """
    Given an allocation, try to find prices with which this allocation is a "personal competitive equilibrium".
    a personal-CE is a relaxation of CE in which, for each agent, there may be a different price-vector that satisfies the CE conditions.
    A personal-CE satisfies all the fairness properties of CE, but does not necessarily satisfy its Pareto-efficiency properties.

    return None of not found
    :param all_items:    a string in which each char represents an item.
    :param budgets:      a list of numbers, each represents the budget of one agent.
    :param preferences:  a list of lists of strings, each list represents the preference-relation of an agent, from best to worst (by the same order as the budgets).
    :param allocation:   a list of strings, each represents the bundle allocated to one agent (by the same order as the budgets).
    :param negative_prices: whether to force all prices to be negative (for allocation of bads/chores). Default=False
    :return: a list of size num_agents, where element i is the price-vector of agent i or None.

    >>> budgets = [5, 2]
    >>> preferences = [["xy", "x", "y", ""], ["xy", "x", "y", ""]]
    >>> print(find_personalized_equilibrium_prices("xy",preferences,budgets,allocation=["x","y"]))
    [array([5., 2.]), array([5., 2.])]
    >>> print(find_personalized_equilibrium_prices("xy",preferences,budgets,allocation=["y","x"]))
    [None, array([2., 5.])]
    >>> print(find_personalized_equilibrium_prices("xy",preferences,budgets,allocation=["xy",""]))
    [array([0., 5.]), array([2.5, 2.5])]
    >>> print(find_personalized_equilibrium_prices("xy",preferences,budgets,allocation=["","xy"]))
    [None, array([0., 2.])]
    >>> chore_preferences = [list(reversed(p)) for p in preferences]
    >>> chore_budgets = [-2, -5]
    >>> print(find_personalized_equilibrium_prices("xy",chore_preferences,chore_budgets,allocation=["y","x"],negative_prices=True))
    [array([-5., -2.]), array([-5., -2.])]
    >>> print(find_personalized_equilibrium_prices("xy",chore_preferences,chore_budgets,allocation=["x","y"],negative_prices=True))
    [None, array([-2., -5.])]
    >>> print(find_personalized_equilibrium_prices("xy",chore_preferences,chore_budgets,allocation=["xy",""],negative_prices=True))
    [None, None]
    >>> print(find_personalized_equilibrium_prices("xy",chore_preferences,chore_budgets,allocation=["","xy"],negative_prices=True))
    [None, None]
    """
    agents = Agent.profile(preferences)
    num_agents = len(agents)
    if num_agents!=len(budgets):
        raise ValueError("Number of budgets ({}) does not match number of preferences ({})".format(len(budgets), len(preferences)))
    if num_agents!=len(allocation):
        raise ValueError("Number of budgets ({}) does not match number of bundles ({})".format(len(budgets), len(allocation)))
    num_items = len(all_items)

    # The minimization coefficients, bounds, and budget constraints, are the same for all agents,
    #     and they are identical to the standard CE:
    minimization_coefficients = np.concatenate((np.zeros(num_items), -np.ones(1)))
    bounds = _price_bounds(num_items, negative_prices)
    (A_equality, b_equality) = _budget_constraints(all_items, budgets, allocation)

    prices = []
    for i in range(num_agents):
        # The preference constraints are personal for each agent:
        (A_upperbound, b_upperbound) = _personal_preference_constraints(all_items, agents[i], budgets[i], allocation[i])
        result = _solve_linear_program(minimization_coefficients, A_equality, b_equality, A_upperbound, b_upperbound, bounds)
        if result is None:
            prices.append(None)
        else:
            prices_for_i = result.x[0:-1]
            slack_for_i = result.x[-1]
            if slack_for_i > 0:
                prices.append(prices_for_i)
            else:
                # logger.info("The slack for agent %d is zero - so no solution exists", i)
                prices.append(None)
    return prices


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







########## INTERNAL FUNCTIONS


def _bundle_to_row(all_items:str, bundle:str, coefficient:float)->list:
    """
    Given a bundle (as a string),
          construct a row of coefficients that represents this bundle.
    :param all_items:  a string representing all items in a certain fixed order.
    :param bundle:     a string representing a subset of the items.
    :param coefficient: the coefficient to put in the row for each item in the bundle.
    :return:  a list where all locations that correspond to the bundle equal coefficient, and all others equal 0.

    >>> _bundle_to_row("wxyz", "wy", 1)
    [1, 0, 1, 0]
    >>> _bundle_to_row("wxyz", "", 1)
    [0, 0, 0, 0]
    >>> _bundle_to_row("wxyz", "zxyw", -1)
    [-1, -1, -1, -1]
    """
    result = len(all_items) * [0]
    for item in bundle:
        result[all_items.index(item)] = coefficient
    return result

def _bundle_price(all_items:str, bundle:str, prices:list)->float:
    """
    Calculate the price of the given bundle with the given price-vector.
    :param all_items:  a string representing all items in a certain fixed order.
    :param bundle:     a string representing a subset of the items.
    :param prices:     a vector of prices, a price per item.
    :return: the price of the bundle with this price-vector.
    """
    quantities = _bundle_to_row(all_items, bundle, 1)
    return sum([prices[i] * quantities[i] for i in range(len(all_items))])


MAX_SLACK=1000  # it should be infinity, but infinity causes problems with linprog.
def _price_bounds(num_items: int, negative_prices:bool)->list:
    """
    Returns a list of bounds on the prices.
    For each item, there is a pair (0,None) if the prices are positive, (None,0) it they are negative.
    The slack is always positive and in (0,MAX_SLACK).
    :return:
    """
    bounds = [(None, 0) if negative_prices else (0, None)] * num_items
    bounds.append ((0,MAX_SLACK))  # the slack variable is always weakly-positive
    return bounds


def _budget_constraints(all_items: str, budgets: list, allocation: list)->tuple:
    """
    Create the budget constraints (equalities) of a CE.
         bundle_i   * [prices,slack]  == budget_i
         A_equality * [prices,slack]  == b_equality

    :param all_items:    a string in which each char represents an item.
    :param budgets:  a list of numbers, each represents the budget of one agent.
    :param allocation:   a list of strings, each represents the bundle allocated to one agent (by the same order as the budgets).

    :return: (A_equality, b_equality)

    >>> (A_eq,b_eq) = _budget_constraints("wxyz", [5,2], ["xz","y"])
    >>> A_eq
    [[0, 1, 0, 1, 0], [0, 0, 1, 0, 0]]
    >>> b_eq
    [5, 2]
    """
    num_agents = len(budgets)
    A_equality = []
    b_equality = []
    for i in range(num_agents):
        if len(allocation[i])>0 or budgets[i]<0:
            row = _bundle_to_row(all_items, allocation[i], 1)
            row.append(0)    # the slack is irrelevant for the budget equalities
            A_equality.append(row)
            b_equality.append(budgets[i])
    return (A_equality, b_equality)


def _preference_constraints(all_items: str, agents: list, budgets: list, allocation: list)->tuple:
    """
    Create the preference constraints (inequalities):
       better_bundle_i    * prices  >  budget_i
       better_bundle_i    * prices  -  slack  >=    budget_i
       - better_bundle_i  * prices  +  slack  <=  - budget_i
       A_upperbound       * [prices , slack]  <=  b_upperbound

    :param all_items:    a string in which each char represents an item.
    :param budgets:  a list of numbers, each represents the budget of one agent.
    :param agents:   a list of Agent objects.
    :param allocation:   a list of strings, each represents the bundle allocated to one agent (by the same order as the budgets).

    :return: (A_upperbound, b_upperbound)

    >>> agent = Agent(["xy", "x", "y", ""])
    >>> (A_ub,b_ub) = _preference_constraints("xy", [agent, agent], [5,2], ["x","y"])
    >>> A_ub
    array([[-1, -1,  1],
           [-1, -1,  1],
           [-1,  0,  1]])
    >>> b_ub
    array([-5, -2, -2])
    """
    num_agents = len(budgets)
    i=0
    A_ub_stack = []
    b_ub_stack = []
    for i in range(num_agents):
        (A_ub, b_ub) = _personal_preference_constraints(all_items, agents[i], budgets[i], allocation[i])
        if len(A_ub)>0 and len(b_ub)>0:
            A_ub_stack.append(A_ub)
            b_ub_stack.append(b_ub)
    logger.debug("A_ub_stack %s", A_ub_stack)
    logger.debug("B_ub_stack %s", b_ub_stack)
    if len(A_ub_stack)>0 and len(b_ub_stack)>0:
        return (np.vstack(A_ub_stack), np.concatenate(b_ub_stack))
    else:
        return ([], [])



def _personal_preference_constraints(all_items: str, agent: Agent, agent_budget: float, agent_bundle: str)->tuple:
    """
    Create the preference constraints (inequalities) for a single agent:
       better_bundle_i    * prices  >  budget_i
       better_bundle_i    * prices  -  slack  >=    budget_i
       - better_bundle_i  * prices  +  slack  <=  - budget_i
       A_upperbound       * [prices , slack]  <=  b_upperbound

    :param all_items:    a string in which each char represents an item.
    :param agent_budget: the budget of this agent.
    :param agent:        an Agent object, with a strict-preferences list.
    :param agent_bundle:   a string representing the bundle allocated to the agent.

    :return: (A_upperbound, b_upperbound)

    >>> agent = Agent(["xy", "x", "y", ""])
    >>> (A_ub,b_ub) = _personal_preference_constraints("xy", agent, 5, "x")
    >>> A_ub
    [[-1, -1, 1]]
    >>> b_ub
    [-5]
    >>> (A_ub,b_ub) = _personal_preference_constraints("xy", agent, 2, "y")
    >>> A_ub
    [[-1, -1, 1], [-1, 0, 1]]
    >>> b_ub
    [-2, -2]
    """
    A_upperbound = []
    b_upperbound = []
    # Loop over all bundles, from the best (for i) down to agent_bundle:
    for preferred_bundle in agent.bundles_preferred_to(agent_bundle):
        row = _bundle_to_row(all_items, preferred_bundle, -1)
        row.append(1)      # coefficient of the slack variable
        A_upperbound.append(row)
        b_upperbound.append(-agent_budget)
    return (A_upperbound, b_upperbound)




def _is_condition_2_satisfied_for_agent(all_items: str, agent: Agent, agent_budget: float, agent_bundle: str, prices:list)->bool:
    """
    Check if the given price-vector satisfies the CE condition 2 for the given agent.
    CE condition 2 means that all bundles that the agent prefers to his bundle cost more than his budget.

    :param all_items:    a string in which each char represents an item.
    :param agent_budget: the budget of this agent.
    :param agent:        an Agent object, with a strict-preferences list.
    :param agent_bundle:   a string representing the bundle allocated to the agent.

    :return: True or False

    >>> agent = Agent(["xy", "x", "y", ""])
    >>> _is_condition_2_satisfied_for_agent("xy", agent, 5, "y", prices=[7,5])
    True
    >>> _is_condition_2_satisfied_for_agent("xy", agent, 5, "y", prices=[2,5])
    False
    >>> _is_condition_2_satisfied_for_agent("xy", agent, 5, "x", prices=[2,5])
    True
    """
    # Loop over all bundles, from the best (for i) down to agent_bundle:
    for preferred_bundle in agent.bundles_preferred_to(agent_bundle):
        preferred_bundle_price = _bundle_price(all_items, preferred_bundle, prices)
        if preferred_bundle_price <= agent_budget:
            logger.info("The agent can afford %s since it costs only %f", preferred_bundle, preferred_bundle_price)
            return False

    logger.info("The agent cannot afford any bundle better than %s", agent_bundle)
    return True   # The remaining bundles are worse than agent_bundle



def _solve_linear_program(minimization_coefficients, A_equality, b_equality, A_upperbound, b_upperbound, bounds):
    """
    Solve the given linear program and return the resulting price-vector (if the slack is positive), or None (if the slack is zero).
    Parameters are passed to scipy.linprog
    :return: result, or None if there is no solution.
    """
    logger.debug("A_equality = \n%s", A_equality)
    logger.debug("b_equality = %s", b_equality)
    logger.debug("A_upperbound = \n%s", A_upperbound)
    logger.debug("b_upperbound = %s", b_upperbound)
    if len(b_upperbound)>0:
        result = linprog(minimization_coefficients,
            A_ub=A_upperbound, b_ub=b_upperbound,
            A_eq=A_equality, b_eq=b_equality,
            bounds=bounds, method='revised simplex')
    else:
        result = linprog(minimization_coefficients,
            A_eq=A_equality, b_eq=b_equality,
            bounds=bounds, method='revised simplex')
    if result.status==1:
        raise ValueError("Iteration limit reached")
    elif result.status == 2:
        logger.debug("linprog returned no feasible solution")
        return None  #
    elif result.status==4:
        raise ValueError("Numerical difficulties encountered")
    else: # received result
        logger.debug("linprog returned %s", result)
        return result



if __name__ == "__main__":
    # logger.setLevel(logging.INFO)
    # budgets = [5, 2]
    # preferences = [["xy", "x", "y", ""], ["xy", "x", "y", ""]]
    # logger.info("\n")
    # print(find_equilibrium_prices("xy",preferences,budgets,allocation=["xy",""]))
    # print(find_personalized_equilibrium_prices("xy",preferences,budgets,allocation=["x","y"]))
    # logger.info("\n")
    # print(find_personalized_equilibrium_prices("xy",preferences,budgets,allocation=["xy",""]))
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
