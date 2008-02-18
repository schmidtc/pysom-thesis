"""This script will process the txt files form the Geodesic som_pak implimentation that Skupin's CS student completed

The format of those files is
'Latitude = 90.000000 Longitude = 0.000000'
....

it will return a valid networkX structure. in theory"""

import networkx
import random
import sys
import os
from math import pi,cos,sin,asin,


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
    

def geodesic(f):
    RADIUS = 1
    diff = 0 #assumption
    points = []
    #f = frequency of tessleation
    noc = f * f * 10 + 2
    newnoc = f * f * 10 + 2
    if f==1:
        angle = 72
        angle_d = [0 for i in range(noc)]
        if noc <= 6:
            numsp = noc
        else:
            numsp = 6
            numinner = noc-numsp
        for i in range(5):
            angle_d[i] = (angle + diff) * pi / 180
            diff += angle
    else: #f>1
        angle = 72
        angle_d = [0 for i in range(5)]
        angle_nd = [0 for i in range(6)]
        for i in range(5):
            angle_d[i]  = (angle+diff) * pi/180
        diff = 0
        angle = 60
        for i in range(6):
            angle_nd[i] = (angle+diff)* pi/180
        numsp = 6*f
        numinner = 6
        numremain = noc - numsp - numinner
        numremain -= 1
    circum = 2 * pi * RADIUS
    initial_distance = circum / numsp
    distance = initial_distance
    totald = circum/6.0

    j = 0
    latitude = [0 for i in range(noc*2)]
    longitude = [0 for i in range(noc*2)]
    latitude[j] = 90.0
    longitude[j] = 0
    j+=1
    noc -= 1
    
    if f==1:
        diff_upper = 0
        diff_lower = 36
        for i in range(5):
            lat = (90 * pi/180)
            lon = (0 * pi/180)
        
            degree = asin(sin(lat)*cos(distance)+cos(lat)*sin(distance)*cos(angle))
            latitude[j] = degree*180/pi
            longitude[j] = diff_lower
            j += 1
            noc -= 1

            if noc == 0:
                break
        if diff_upper < 144 and diff_lower >= 0:
            diff_upper += 72
        elif diff_upper == 144:
            diff_upper = -72
        elif diff_upper > -144 and diff_upper < 0:
            diff_upper += -72

        if diff_lower<180 and diff_lower >= 0:
            diff_lower += 72
        elif diff_lower==180:
            diff_lower=-36
        elif diff_lower>-180 and diff_lower<0:
            diff_lower += -72



    
    


#if __name__=='__main__':
#    geodesic = sys.argv[1]
#    grid = txtGeo2grid(geodesic)
#    grid2delaunay(grid)
    
    
