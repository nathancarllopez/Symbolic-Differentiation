import basicfunctions

f = basicfunctions.Exponential('x', 3, 5)
g = basicfunctions.Polynomial('x', [2,0,3,-1])
h = f+g
hTree = h.structure
print(hTree)
k = h+h
print()
kTree = k.structure
print(kTree)
print()
print(kTree.get_subtrees_below_root())