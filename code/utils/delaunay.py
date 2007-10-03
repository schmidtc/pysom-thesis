import networkx as NX
from math import *
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

