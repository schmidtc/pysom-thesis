"""
======================================================================
Python Self-Organizing Maps -- Network Functions
----------------------------------------------------------------------
AUTHOR(S):      Charles R. Schmidt cschmidt@rohan.sdsu.edu
======================================================================
"""

import networkx as NX

def neighborhood(G,n,o):
    """ Returns the neighbors of node n in graph G out to order o,
        Returned as dictionary where the keys are node ids and the
        values are the order of that node,
    """
    base = G[n]
    neighbors = {}
    neighbors[n] = 0
    newNodes = set(neighbors.keys())
    for i in range(1,o+1):
        #for node in neighbors.keys():
        nodes = newNodes.copy()
        newNodes = set()
        for node in nodes:
            branch = G[node]
            for node in branch:
                if node not in neighbors:
                    newNodes.add(node)
                    neighbors[node]=i
    return neighbors

def findWidth(G,seed=None,returnWidths=False):
    """ Returns the maximum width of graph G
        If given a seed will only search from that node.
    """
    widths = []
    if not seed == None:
        nodes = [seed]
    else:
        nodes = G.nodes()
    for node in nodes:
        o = 0
        maxW = 0
        W = len(neighborhood(G,node,o))
        while 1:
            o += 1
            W2 = len(neighborhood(G,node,o))
            if W2 > W:
                W = W2
                maxW = o
            else:
                break
        widths.append(maxW)
    if returnWidths: return widths
    else: return max(widths)

if __name__=='__main__':
    G = NX.Graph()

    G.add_edge(('1','2'))
    G.add_edge(('2','3'))
    G.add_edge(('3','4'))
    G.add_edge(('4','5'))
    G.add_edge(('5','6'))
    G.add_edge(('6','7'))
    G.add_edge(('7','8'))
    G.add_edge(('8','9'))
    G.add_edge(('9','1'))

    print findWidth(G)
    print neighborhood(G,'1',4)
