#!python3

from sympy import *
from sympy.abc import a,b,x,y
from sympy.solvers.solveset import linsolve

# print(solveset([x > 2, x-1 < 3], x, S.Reals))
print(solveset(x-1 < 3, x, S.Reals))     # (-oo, 4)
print(solveset(x-1 <= 3, x, S.Reals))     # (-oo, 4]
print(solveset(x-1 < x-2, x, S.Reals))   # empty set
print(solveset(x-1 < y+2, x, S.Reals))   # x<y+3??

xy_sol = linsolve([x+y - 3*a, x-y - a], x,y)
xy = next(iter(xy_sol))
print ("x={}".format(xy[0]))
print(xy[0].subs(a,5))
