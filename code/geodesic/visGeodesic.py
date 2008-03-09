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

######################
def splitPoly(poly):
    poly2 = poly[1:]
    poly2.append(poly[0])
    edges = zip(poly,poly2)
    c = 0
    badEdges = []
    edge0 = 0
    edge1 = 0
    newPoly = []
    found = False
    l = []
    for p0,p1 in edges:
        if ((p0[0] < -90) ^ (p1[0] < -90)) and ((p0[0] >90) ^ (p1[0] > 90)):
            i = findIntersetion(p0[0],p0[1],p1[0],p1[1])
            l.append(i)
    for p0,p1 in edges:
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
            badEdges.append((pi0,p1))
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
        elif ((p0[0]== 180.0) or (p0[0] == -180.0)) and l:
            pi0 = (-1*p0[0],p0[1])
            newPoly.append(p0)
            c += 1
            if found:
                edge1 = c
            else:
                edge0 = c
                found = True
            newPoly.append(pi0)
            c += 1
            badEdges.append((p0,pi0))
            
        else:
            newPoly.append(p0)
            c += 1

    if len(badEdges) == 2:
        #Posible Polar Region
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
        print edge0,edge1
    elif len(badEdges) == 4:
        poly0 = newPoly[:edge0]
        poly0.extend( newPoly[edge1:] )
        poly1 = newPoly[edge0:edge1]
        poly = (poly0,poly1)
        print edge0,edge1
    else:
        if len(badEdges) > 0:
            print "this special case is not handled"
        poly = newPoly
    return poly
###########################

def toXYZ(pt):
    lng,lat = pt
    lng,lat = lng+pi,lat+(pi/2)
    x = 1*sin(lat)*cos(lng)
    y = 1*sin(lat)*sin(lng)
    z = 1*cos(lat)
    return x,y,z

def toLngLat(xyz):
    x,y,z = xyz
    if z == -1 or z == 1:
        lng = 0
    else:
        lng = atan2(y,x)
        if lng > 0:
            lng = lng-pi
        elif lng < 0:
            lng = lng+pi
    lat = acos(z)-(pi/2)
    return degrees(lng),degrees(lat)

def read(fname = 'voronoi.xyz'):
    f = open(fname,'r')
    verts = []
    polys = []

    line = f.readline()
    while line:
        if line[0] == '#':
            line = f.readline()
        elif 'center' in line:
            line = f.readline()
            line = line.split()
            line = map(float,line)
            line = toLngLat(line)
            verts.append(line)
            line = f.readline()
        elif 'polygon' in line:
            poly = []
            line = f.readline()
            while 'center' not in line and line:
                line = line.split()
                line = map(float,line)
                line = toLngLat(line)
                poly.append(line)
                line = f.readline()
            polys.append(poly)
        else:
            print "got here"
            line = f.readline()
    f.close()
    return polys

def write(polys,fname='poly.txt'):
    o = open(fname,'w')
    o.write("POLYGON\n")

    c = 0
    for poly in polys:
        o.write("%d 0\n"%c)
        if len(poly) == 2:
            for i,pt in enumerate(poly[0]):
                o.write("%d %f %f\n"%(i,pt[0],pt[1]))
            o.write("%d %f %f\n"%(i+1,poly[0][0][0],poly[0][0][1]))
            o.write("%d 1\n"%c)
            for i,pt in enumerate(poly[1]):
                o.write("%d %f %f\n"%(i,pt[0],pt[1]))
            o.write("%d %f %f\n"%(i+1,poly[1][0][0],poly[1][0][1]))
        else:
            for i,pt in enumerate(poly):
                o.write("%d %f %f\n"%(i,pt[0],pt[1]))
            o.write("%d %f %f\n"%(i+1,poly[0][0],poly[0][1]))
        c+= 1
    o.write("END\n")
    o.close()

def validate(poly):
    """ Validate checks to see if points on the meridian should really be on the anti-meridian
    This only works on one point in the poly, if there is an edge on the meridian, you must run the polygon
    through validate twice, no harm is done in always running it twice"""
    if len(poly)==2:
        return poly
    lng = [p[0] for p in poly]
    lat = [p[1] for p in poly]
    if 0.0 in lng:
        i = lng.index(0.0)
        if lng[i-1] < -90:
            poly[i] = (-180.0,lat[i])
        elif lng[i-1] > 90:
            poly[i] = (180.0,lat[i])
    return poly



if __name__=="__main__":
    polys = read('temp/voronoi.xyz')
    vpolys = map(validate,polys)
    vpolys = map(validate,vpolys)
    spolys = map(splitPoly,vpolys)
    write(spolys,'temp/poly.txt')
