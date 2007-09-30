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

if __name__=='__main__':
#    G = graph((6,6))
#    for i in range(1,7):
#        G.add_node(str(i))
    G = NX.Graph()
    
    

    G.add_edge(('1','2'))
    G.add_edge(('1','4'))
    G.add_edge(('1','5'))
    G.add_edge(('4','2'))
    G.add_edge(('4','5'))
    G.add_edge(('2','5'))
    G.add_edge(('5','3'))
    G.add_edge(('3','6'))




