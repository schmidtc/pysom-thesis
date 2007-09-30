from math import *
from geosom import som

n = 400
rEarth = 6372.795
s = som()
s.Size = n
s.initgeo()

dists = [] 
for pt in s.grid:
	for pt2 in s.grid:
		d = s.sdist(pt,pt2)
		if not d==0:
			dists.append((d,pt,pt2))

dists.sort()
d = min(dists)
d = d[0]
print d
print degrees(d)
