#!python3

"""
A utiltity for generating all allocations of a given set of items
among a given number of agents.
"""
import itertools


def powerset(iterable):
    """
    Returns all subsets of the given iterable.
    Based on code from https://docs.python.org/3.7/library/itertools.html .

    >>> list(powerset([1,2,3]))
    [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
    """
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


def allocations(items:str, num_agents:int):
    """
    :param items [string or set]: the set of items to allocate.
    :param num_agents:  the number of agents to allocate to.
    :return:  A generator that generates, at each iteration, a list of strings (bundles) of size num_agents.

    >>> list(allocations("xyz", 1))
    [['xyz']]

    >>> list(allocations("xyz", 2))
    [['', 'xyz'], ['x', 'yz'], ['y', 'xz'], ['z', 'xy'], ['xy', 'z'], ['xz', 'y'], ['yz', 'x'], ['xyz', '']]

    >>> list(allocations("xy", 3))
    [['', '', 'xy'], ['', 'x', 'y'], ['', 'y', 'x'], ['', 'xy', ''], ['x', '', 'y'], ['x', 'y', ''], ['y', '', 'x'], ['y', 'x', ''], ['xy', '', '']]
    """
    # if isinstance(items,str):
    #     return allocations(set(items), num_agents)
    if num_agents<=0:
        raise ValueError("Must have at least one agent")
    if num_agents==1:
        yield [items]
    else:
        for bundle_of_agent_0 in powerset(items):
            remaining_items = "".join([item for item in items if item not in bundle_of_agent_0])
            for allocation_to_other_agents in allocations(remaining_items, num_agents-1):
                total_allocation = ["".join(bundle_of_agent_0)] + allocation_to_other_agents
                # yield ["".join(bundle) for bundle in total_allocation]
                yield total_allocation

if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
