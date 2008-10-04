""" This program take N, the size of the dissired network as an argument,
    It runs the sxyz_voroni code which results in a few XYZ files,
        one containing the Delaunay trigulation
    
    This program relys on,
        sxyz_voronoi.f90
        stripack.f90
"""


import geosom,os
import sys
from commands import getoutput,getstatusoutput
from math import *

def toXYZ(pt):
    phi,theta = pt
    phi,theta = phi+pi,theta+(pi/2)
    x = 1*sin(theta)*cos(phi)
    y = 1*sin(theta)*sin(phi)
    z = 1*cos(theta)
    return x,y,z

def toLngLat(xyz):
    x,y,z = xyz
    if z == -1 or z == 1:
        phi = 0
    else:
        phi = atan2(y,x)
        if phi > 0:
            phi = phi-pi
        elif phi < 0:
            phi = phi+pi
    theta = acos(z)-(pi/2)
    return phi,theta

s = geosom.som()
n = int(sys.argv[1])
s.Size = n
s.initgeo()
s.grid[0] = (0,s.grid[0][1])
s.grid[-1] = (0,s.grid[-1][1])

xyz = [toXYZ(pt) for pt in s.grid]

o = open("grid.xyz",'w')
#i = 1
for x,y,z in xyz:
    #o.write("%d,%f,%f,%f\n"%(i,x,y,z))
    o.write("%f %f %f\n"%(x,y,z))
    #i+=1
o.close()


out = getstatusoutput('/home/un/m/cschmidt/bin/sxyz_voronoi grid.xyz')
if out[0] == 0:
    print out[1]
else:
    print 'problem'

f = open('voronoi.xyz','r')
tr = open('delaunay.xyz','r')
trLines = tr.readlines()
lines = f.readlines()
f.close()
tr.close()

trVerts = []
verts = []
trEdges = []
edges = []
num = len(lines)
trNum = len(trLines)

for i in xrange(trNum-1):
    line = trLines[i]
    if line[0] == '#':
        pass
    elif len(line) < 5:
        pass
    elif trLines[i-1] == trLines[i+1]:
        line = line.split()
        line = map(float,line)
        trVerts.append(line)
    elif len(line) > 10 and len(trLines[i+1]) > 10:
        line0 = line.split()
        line1 = trLines[i+1].split()
        line0 = map(float,line0)
        line1 = map(float,line1)
        trEdges.append((line0,line1))

for i in xrange(num-1):
    line = lines[i]
    if line[0] == '#':
        pass
    elif len(line) < 5:
        pass
    elif lines[i-1] == lines[i+1]:
        line = line.split()
        line = map(float,line)
        verts.append(line)
    elif len(line) > 10 and len(lines[i+1]) > 10:
        line0 = line.split()
        line1 = lines[i+1].split()
        line0 = map(float,line0)
        line1 = map(float,line1)
        edges.append((line0,line1))

trO = open('%d_delaunay'%n,'w')
trO.write('Cool Header\n')


o = open('%d.txt'%n,'w')
o.write("Polyline\n")
fixedEdges = []
for edge in edges:
    p0,p1 = map(toLngLat,edge)
    p0,p1 = map(degrees,p0),map(degrees,p1)
    #who knew XOR would ever come in handy?
    if ((p0[0] < -90) ^ (p1[0] < -90)) and ((p0[0] >90) ^ (p1[0] > 90)):
        if p0[0] < p1[0]:
            neg = p0
            pos = p1
            x1,y1 = p0
            x2,y2 = p1
        else:
            neg = p1
            pos = p0    
            x1,y1 = p1
            x2,y2 = p0

        x1 = -1*(x1+180.0)
        x2 = 180.0-x2
        deltaY = y1-y2
        deltaX = x1-x2
        m = deltaY/deltaX
        b = y1 - m*x1
        edge1 = (neg,(-180,b))
        edge2 = ((180,b),pos)

        fixedEdges.append(edge1)
        fixedEdges.append(edge2)
    else:
        fixedEdges.append((p0,p1))
        


for i in xrange(len(fixedEdges)):
    p0,p1 = fixedEdges[i]
    o.write('%d 0\n'%i)
    o.write('0 %f %f 0.0 0.0\n'%(p0[0],p0[1]))
    o.write('1 %f %f 0.0 0.0\n'%(p1[0],p1[1]))

o.write('END\n')
o.close()



