import networkx as NX

def neighborhood(G,n,o):
    base = G[n]
    neighbors = {}
    neighbors[n] = 0
    for i in range(1,o+1):
        for node in neighbors.keys():
            branch = G[node]
            for node in branch:
                if node not in neighbors:
                    neighbors[node]=i
    return neighbors

def findWidth(G,seed=None,returnWidths=False):
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
#    G = graph((6,6))
#    for i in range(1,7):
#        G.add_node(str(i))
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
"""
    G.add_edge(('1','2'))
    G.add_edge(('1','4'))
    G.add_edge(('1','5'))
    G.add_edge(('4','2'))
    G.add_edge(('4','5'))
    G.add_edge(('2','5'))
    G.add_edge(('5','3'))
    G.add_edge(('3','6'))
"""
