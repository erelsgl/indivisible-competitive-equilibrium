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


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
