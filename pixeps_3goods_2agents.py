#!python3

"""
Tries to automatically find pixeps in the case of 3 goods and 2 additive identical agents.
"""


from symbolic_picking_sequences import analyze_sequence
from sympy import symbols

budget_vars = symbols("a,b")
price_vars = symbols("p3,p2,p1")

# find_pixep_symbolic.trace = print
analyze_sequence("AAA", [], price_vars, budget_vars)
analyze_sequence("AAB", [], price_vars, budget_vars)
analyze_sequence("ABA", [], price_vars, budget_vars)
analyze_sequence("ABB", ["3:21"], price_vars, budget_vars)
analyze_sequence("BAA", ["3:21"], price_vars, budget_vars)
analyze_sequence("BAB", [], price_vars, budget_vars)
analyze_sequence("BBA", [], price_vars, budget_vars)
analyze_sequence("BBB", [], price_vars, budget_vars)

"""
RESULTS (trimmed):

AAB
a - b    b    b:      handles 2:1.     Requires a in Interval.open(2, oo)
a/2    a/2    b:      handles 3:2.     Requires a in Interval.open(2, oo)

ABA
a    b    0:      handles 1:0.     Requires a in Interval.open(1, oo)
a - b    b    b:      handles 2:1.     Requires a in Interval.open(2, oo)
b    b    a - b:      handles 3:2.     Requires a in Interval.open(1, 2)

INTERPRETATION: can use one pixep:
A     B    A 
a-    b    0+
"""
