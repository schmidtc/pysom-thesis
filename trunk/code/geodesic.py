"""This script will process the txt files form the Geodesic som_pak implimentation that Skupin's CS student completed

The format of those files is
'Latitude = 90.000000 Longitude = 0.000000'
....

it will return a valid networkX structure. in theory"""

import networkx
import random
import sys
import os
from math import pi,cos,sin


def toXYZ(pt):
    """ ASSUMPTION: pt = (lng,lat)
        REASON: pi = 180 degress,
                theta+(pi/2)....
                theta = 90 degrees,
                180 =  90+180/2"""
    phi,theta = pt
    phi,theta = phi+pi,theta+(pi/2)
    x = 1*sin(theta)*cos(phi)
    y = 1*sin(theta)*sin(phi)
    z = 1*cos(theta)
    return x,y,z


def txtGeo2grid(filename):
    """This function parses the original text file"""
    f = open(filename,'r')
    data = []
    for line in f:
        line = line.strip()
        line = line.split()
        lat = float(line[2])
        long = float(line[5])
        data.append((long,lat))
    return data
    
def grid2delaunay(g):
    """Before we can generate a networkx structure we need to generate an XYZ file to feed into SXYZ_voronio, which will calc the edges of our graph."""
    grid = map(toXYZ,g)
    grid = [' '.join(map(str,l)) for l in grid]
    grid = '\n'.join(grid)
    fname = os.tmpnam()
    o = open(fname,'w')
    o.write(grid)
    o.close()
    
    trigXYZ = os.tmpnam()

    os.system('sxyz_voronoi %s'%fname)
    #os.system('rm voronoi.eps')
    os.system('rm voronoi.xyz')
    #os.system('rm delaunay.eps')
    os.system('rm %s'%fname)
    


if __name__=='__main__':
    geodesic = sys.argv[1]
    grid = txtGeo2grid(geodesic)
    grid2delaunay(grid)
    
    
