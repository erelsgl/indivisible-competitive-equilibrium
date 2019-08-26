# Indivisible Competitive Equilibrium
Algorithms related to competitive equilibrium in a market of indivisible items.

To verify the non-existence results from
 the paper
 [Competitive Equilibrium for Almost All Incomes](https://arxiv.org/abs/1705.04212),
run the corresponding scripts starting with nonexistence_, for example:

    python3 nonexistence_4goods_3agents.py

verifies the non-existence result regarding 4 goods and 3 agents.

The code closely follows the description of the examples in the paper,
but it uses specific numeric budgets. 
By editing the code and re-running, 
you can see to what extent the non-existence is sensitive to changes in the budgets or preferences. 

The code for finding CE prices in the `competitive_equilibrium.py`:

* The function `find_equilibrium_prices` accepts preferences, budgets and allocations,
and looks for a price-vector with which this allocation is a CE. The check is done using a linear program
in which the variables are the prices, and the constraints are budget equalities and preference inequalities.
* The function  `find_equilibrium` accepts preferences and budgets, and runs `find_equilibrium_prices` 
on all the allocations, until a price-vector is found for one of the allocations.