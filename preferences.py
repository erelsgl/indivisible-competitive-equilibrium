#!python3

"""
Utilities for creating monotonic preferences (total order on bundles).
"""

import itertools

def bundles_of_size(items:str, size:int)->list:
    return ["".join(bundle) for bundle in  itertools.combinations(items, size)]

def pairs(items:str)->list:
    """
    >>> pairs("xyz")
    ['xy', 'xz', 'yz']
    """
    return bundles_of_size(items, 2)

def triplets(items:str)->list:
    """
    >>> triplets("wxyz")
    ['wxy', 'wxz', 'wyz', 'xyz']
    """
    return bundles_of_size(items, 3)

def quartets(items:str)->list:
    """
    >>> quartets("wxyz")
    ['wxyz']
    """
    return bundles_of_size(items, 4)

def quintuplets(items:str)->list:
    """
    >>> quintuplets("vwxyz")
    ['vwxyz']
    """
    return bundles_of_size(items, 5)

def list_difference(list1:list, list2:list)->list:
    return [item for item in list1 if item not in list2]


def goods_to_chores(items:str, preferences_on_goods:list)->list:
    """
    Converts preferences on goods to preferences on chores.
    :param items: the set of all items
    :param preferences_on_goods: a list of strings representing bundles of goods,  in decreasing order of preference.
    :return: a list of strings representing bundles of goods,  in decreasing order of preference.

    >>> goods_to_chores("xyz", ["xyz","xy","xz",""])
    ['', 'z', 'y', 'xyz']
    """
    items_set = set(items)
    return [
        "".join(sorted(items_set.difference(set(bundle))))
        for bundle in preferences_on_goods
    ]


def add_low_value_good(preferences:list, new_item:str)->list:
    """
    Given preferences on m items,
    add a new item that is "low valued".
    :param preferences: a list of strings representing bundles of goods,  in decreasing order of preference.
    :param new_item: the name of the new item to add.
    :return: the new preference-list.

    >>> add_low_value_good(["xyz","xy","xz",""], "o")
    ['xyzo', 'xyz', 'xyo', 'xy', 'xzo', 'xz', 'o', '']
    """
    result = []
    for bundle in preferences:
        result.append(bundle+new_item)
        result.append(bundle)
    return result

if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
