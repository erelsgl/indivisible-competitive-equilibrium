#!python3

from scipy.optimize import linprog


c = [-1, 4]
A = [[-3, 1], [1, 2]]
b = [6, 4]
x0_bounds = (None, None)
x1_bounds = (-3, None)

# Minimize: c * x
# Subject to: A_ub * x <= b_ub
# A_eq * x == b_eq
res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds])
print(res)
print()


res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds], method='revised simplex')
print(res)
print()


res = linprog([0,0], A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds], method='revised simplex')
print(res)
print()
