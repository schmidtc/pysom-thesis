import networkx as NX
from math import *
def toLngLat(xyz):
    x,y,z = xyz
    if z == -1 or z == 1:
        phi = 0
    else:
        phi = atan2(y,x)
        if phi == pi:
            pass
        elif phi > 0:
            phi = phi-pi
        elif phi < 0:
            phi = phi+pi
    theta = acos(z)-(pi/2)
    return phi,theta

def altParseDel(filename):
    xyz = set()
    def line2pt(line):
        pt = line.strip().split()
        pt = map(float,pt)
        xyz.add(tuple(pt))
        pt = toLngLat(pt)
        return pt
    f = open(filename,'r')
    lines = f.readlines()
    G = NX.Graph()
    nodes = {}
    edge = []
    c = 0
    for i,line in enumerate(lines):
        if '#' in line:
            pass
        elif len(line.strip().split()) == 3:
            pt = line2pt(line)
            if pt not in nodes:
                nodes[pt] = c
                c += 1
            if i < len(lines)-1 and len(lines[i+1].strip().split()) == 3:
                G.add_edge(pt,line2pt(lines[i+1]))
    print len(nodes),len(xyz)
    return G,nodes,xyz
    
def parseDelaunay(filename):
    f = open(filename,'r')
    G = NX.Graph()
    nodes = {}
    edge = []
    for line in f:
        try:
            line = line.strip().split()
            line = map(float,line)
            pt = toLngLat(line)
            if pt not in nodes:
                nodes[pt] = len(nodes)
            else:
                edge.append(nodes[pt])

            if len(edge) == 2:
                G.add_edge(edge)
                edge = []
        except:
            pass
    return G
if __name__=="__main__":
    import sys
    import som
    filename = sys.argv[1]
    G = parseDelaunay(filename)

    S = som.GraphTopology(G)

