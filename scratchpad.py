from genericFunctions import quatToInertial
import numpy as np

u = np.array([0.0, 1.0, 0.0])

q = quatToInertial( u )

print(q)
f = open('data/test.dat', 'w')
for i in range(100):
    data = [i, i, i, i]
    f.write(" ".join( data ))
