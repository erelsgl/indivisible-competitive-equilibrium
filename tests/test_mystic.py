#!python3

ineqs = '''
x+y > 3*a
x-y > a
'''
import mystic.symbolic as ms
eqns = ms.simplify(ineqs, variables=list('xya'))
print (eqns)
