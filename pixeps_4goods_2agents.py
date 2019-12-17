#!python3

"""
Tries to automatically find pixeps in the case of 4 goods and 2 additive identical agents
"""

import symbolic_picking_sequences, sys, logging
if len(sys.argv)<2 or sys.argv[1]!="quiet":
    symbolic_picking_sequences.logger.setLevel(logging.INFO)

from symbolic_picking_sequences import analyze_sequence
from sympy import symbols

budget_vars = symbols("a,b")
price_vars = symbols("p4,p3,p2,p1")

analyze_sequence("AAAA", [], price_vars, budget_vars)
analyze_sequence("AAAB", [], price_vars, budget_vars)
analyze_sequence("AABA", [], price_vars, budget_vars)
analyze_sequence("AABB", ["3:21","4:21"], price_vars, budget_vars)
analyze_sequence("ABAA", ["3:21"], price_vars, budget_vars)
analyze_sequence("ABAB", ["4:31"], price_vars, budget_vars)
analyze_sequence("ABBA", ["4:32"], price_vars, budget_vars)
analyze_sequence("ABBB", ["4:21","4:31","4:32"], price_vars, budget_vars)
analyze_sequence("BAAA", ["4:21"], price_vars, budget_vars)
analyze_sequence("BAAA", ["4:31"], price_vars, budget_vars)
analyze_sequence("BAAA", ["4:32"], price_vars, budget_vars)
analyze_sequence("BAAB", ["4:32"], price_vars, budget_vars)



"""
RESULTS (trimmed):

ABAA
a - b    b    b    0:      handles 3:21, 1:0.     Requires a in Interval.open(2, oo)
a - b    b    b/2    b/2:      handles 3:21, 2:1.     Requires a in Interval.open(2, oo)
a - b    b    b    0:      handles 3:21, 3:2.     Requires a in Interval.open(2, oo)

ABAB
b    b    a - b    0:      handles 4:31, 1:0.     Requires a in Interval.open(1, 2)
b    -a + 2*b    a - b    a - b:      handles 4:31, 2:1.     Requires a in Interval.open(1, 3/2)
b    a - b    a - b    -a + 2*b:      handles 4:31, 3:2.     Requires a in Interval.open(3/2, 2)
b    b    a - b    0:      handles 4:31, 4:3.     Requires a in Interval.open(1, 2)

ABBA
b    -a + 2*b    a - b    a - b:      handles 4:32, 2:1.     Requires a in Interval.open(1, 3/2)
b    b/2    b/2    a - b:      handles 4:32, 3:2.     Requires a in Interval.open(1, 3/2)

ABBB

BAAA
b    a - b    b/2    b/2:      handles 4:21, 2:1.     Requires a in Interval.open(3/2, 2)
b    a - b    a - b    -a + 2*b:      handles 4:21, 3:2.     Requires a in Interval.open(3/2, 2)

BAAA
b    b    a - b    0:      handles 4:31, 1:0.     Requires a in Interval.open(1, 2)
b    -a + 2*b    a - b    a - b:      handles 4:31, 2:1.     Requires a in Interval.open(1, 3/2)
b    a - b    a - b    -a + 2*b:      handles 4:31, 3:2.     Requires a in Interval.open(3/2, 2)
b    b    a - b    0:      handles 4:31, 4:3.     Requires a in Interval.open(1, 2)

BAAA
b    -a + 2*b    a - b    a - b:      handles 4:32, 2:1.     Requires a in Interval.open(1, 3/2)
b    b/2    b/2    a - b:      handles 4:32, 3:2.     Requires a in Interval.open(1, 3/2)



INTERPRETATION: can use two pixeps:

a > 2b:

A            B     A      A
(a - b)++    b-    b--    0+


2b > a > b: 

A     B     A           B
b+    b-    (a - b)-    0+     

"""
