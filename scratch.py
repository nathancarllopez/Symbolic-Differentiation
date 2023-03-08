import basicfunctions

f = basicfunctions.Exponential('x', 3, 5)
g = basicfunctions.Polynomial('x', [2,0,3,-1])
h = f+g
hTree = h.structure
print(hTree)