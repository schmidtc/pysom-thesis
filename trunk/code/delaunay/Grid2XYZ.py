""" This program take N, the size of the dissired network as an argument,
    It runs the sxyz_voroni code which results in a few XYZ files,
        one containing the Delaunay trigulation
    
    This program relys on,
        sxyz_voronoi.f90
        stripack.f90
"""
import os
import sys
import numpy
from commands import getoutput,getstatusoutput
from math import *
from greatCircle import findIntersetion

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

def rakhmanov(n):
    points = []
    for i in xrange(1,n+1):
        i = float(i)
        N = float(n)
        h = (-1)+((2*(i-1)) / (N-1))
        theta = acos(h)
        if i == 1 or i == N:
            phi = 0
        else:
            phi = (points[int(i)-2][0] + (3.6/sqrt(N)) * (1/sqrt(1-h**2)) ) % (2*pi)
        points.append((phi,theta))
    points = numpy.array([(phi-pi,theta-(pi/2)) for phi,theta in points])
    return points

n = int(sys.argv[1])
grid = rakhmanov(n)
grid[0] = (0,grid[0][1])
grid[-1] = (0,grid[-1][1])

xyz = [toXYZ(pt) for pt in grid]

o = open("temp/grid.xyz",'w')
#i = 1
for x,y,z in xyz:
    #o.write("%d,%f,%f,%f\n"%(i,x,y,z))
    o.write("%f %f %f\n"%(x,y,z))
    #i+=1
o.close()

out = getstatusoutput('sxyz_voronoi temp/grid.xyz')
if out[0] == 0:
    print out[1]
    os.system('mv delaunay.* temp/')
    os.system('mv voronoi.* temp/')
else:
    print 'problem'

f = open('temp/voronoi.xyz','r')
#lines = f.readlines()
#f.close()

verts = []
polys = []

line = f.readline()
c = 0
while line:
    #for i in xrange(num-1):
    if line[0] == '#':
        line = f.readline()
    elif 'center' in line:
        line = f.readline()
        line = line.split()
        line = map(float,line)
        verts.append(line)
        line = f.readline()
    elif 'polygon' in line:
        poly = []
        line = f.readline()
        while 'center' not in line and line:
            line = line.split()
            line = map(float,line)
            poly.append(line)
            line = f.readline()
        polys.append(poly)
    else:
        print "got here"
        line = f.readline()
f.close()
        
o = open('temp/%d.txt'%n,'w')
o.write("POLYGON\n")
fixedEdges = []



def splitPoly(poly):
    poly2 = poly[1:]
    poly2.append(poly[0])
    edges = zip(poly,poly2)
    c = 0
    badEdges = []
    newEdges = []
    edge0 = 0
    edge1 = 0
    newPoly = []
    found = False
    for p0,p1 in edges:
        p0 = toLngLat(p0)
        p1 = toLngLat(p1)
        p0,p1 = map(degrees,p0),map(degrees,p1)
        if ((p0[0] < -90) ^ (p1[0] < -90)) and ((p0[0] >90) ^ (p1[0] > 90)):
            i = findIntersetion(p0[0],p0[1],p1[0],p1[1])
            if (p0[1] < 0) and (p1[1] < 0) and i > 0:
                i = i*-1
            elif (p0[1] > 0) and (p1[1] > 0) and i < 0:
                i = i*-1
            if (p0[0] < 0) and (p1[0] > 0):
                pi0 = [-180.0,i]
                pi1 = [180.00,i]
            else:
                pi0 = [180.0,i]
                pi1 = [-180.00,i]
            badEdges.append((p0,pi0))
            newEdges.append((p0,pi0))
            badEdges.append((pi0,p1))
            newEdges.append((pi0,p1))
            newPoly.append(p0)
            c += 1
            newPoly.append(pi0)
            c += 1
            if found:
                edge1 = c
            else:
                edge0 = c
                found = True
            newPoly.append(pi1)
            c += 1
        else:
            newPoly.append(p0)
            c += 1
            newEdges.append((p0,p1))
    if len(badEdges) == 2:
        #Polar Region
        #print len(badEdges)
        poly = newPoly[:edge0]
        if poly[-1][0] < 0:
            pol = -180.0
        else:
            pol = 180.0
        if poly[-1][1] > 0:
            poly.append([pol,90])
            poly.append([-1*pol,90])
        else:
            poly.append([pol,-90])
            poly.append([-1*pol,-90])
        poly.extend(newPoly[edge0:])
    elif len(badEdges) == 4:
        poly0 = newPoly[:edge0]
        poly0.extend( newPoly[edge1:] )
        poly1 = newPoly[edge0:edge1]
        poly = (poly0,poly1)
        print edge0,edge1
    else:
        poly = newPoly
    return poly
        

polys = map(splitPoly,polys)

c = 0
for poly in polys:
    o.write("%d 0\n"%c)
    if not len(poly) == 2:
        poly.append(poly[0])
        i = 0
        for pt in poly:
            #pt = toLngLat(pt)
            #pt = map(degrees,pt)
            o.write('%s %f %f\n'%(i,pt[0],pt[1]))
            i += 1
    else:
        poly[0].append(poly[0][0])
        poly[1].append(poly[1][0])
        i = 0
        for pt in poly[0]:
            #pt = toLngLat(pt)
            #pt = map(degrees,pt)
            o.write('%s %f %f\n'%(i,pt[0],pt[1]))
            i += 1
        o.write("%d 1\n"%c)
        i = 0
        for pt in poly[1]:
            #pt = toLngLat(pt)
            #pt = map(degrees,pt)
            o.write('%s %f %f\n'%(i,pt[0],pt[1]))
            i += 1
    c += 1
        
o.write('END\n')
o.close()
"""
    for i in xrange(len(poly)):
        p0 = toLngLat(poly[i])
        if i < len(poly):
            p1 = toLngLat(poly[i+1])
        else:
            p1 = toLngLat(poly[0])
        p0,p1 = map(degrees,p0),map(degrees,p1)
        #who knew XOR would ever come in handy?
        if ((p0[0] < -90) ^ (p1[0] < -90)) and ((p0[0] >90) ^ (p1[0] > 90)):
            bad = True
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
            """
"""
    if not bad:
        cleanPolys.append(poly)
            
        


for i in xrange(len(fixedEdges)):
    p0,p1 = fixedEdges[i]
    o.write('%d 0\n'%i)
    o.write('0 %f %f 0.0 0.0\n'%(p0[0],p0[1]))
    o.write('1 %f %f 0.0 0.0\n'%(p1[0],p1[1]))

o.write('END\n')
o.close()


"""
