import classes as c

poly = c.Polynomial('x', [1, 5, 0, -3])
exp = c.Exponential('x', 2, 2)
sin = c.Trigonometric('x', 2, 's')

for x in [poly, exp, sin]:
    print(x)

f = poly + exp
print(f.structure)