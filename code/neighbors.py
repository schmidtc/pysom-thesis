import numpy as N
import scipy as S
import scipy.sparse
import networkx as NX

class graph:
    def __init__(self,size):
        self.G = S.sparse.dok_matrix(size)
        #self.G.setdiag(N.ones(self.G.shape[0]))
        self.nodes = {}
        self.ids = {}
        self.order = 1
        self.A = self.G
        self.S = S.sparse.dok_matrix(size)
        
    def set_order(self,order):
        if not self.order == order:
            self.order = order
            self.A = self.G
            for i in range(order-1):
                self.A = self.A * self.G
                # Use S to sum non-zero element.
                
    def add_node(self,node):
        if node not in self.nodes:
            id = len(self.nodes)
            self.nodes[node] = id
            self.ids[id] = node
    def add_edge(self,edge):
        """edge == tuple('node1','node2')
            nodes added as necessary"""
        n1,n2 = edge
        self.add_node(n1)
        self.add_node(n2)
        self.G[self.nodes[n1],self.nodes[n2]]=1
        self.G[self.nodes[n2],self.nodes[n1]]=1
    def neighbors(self,node,order=1):
        self.set_order(order)
        row = self.A[:,self.nodes[node]]
        result = []
        for id,dist in enumerate(row.todense()):
            if id in self.ids:
                nodeName = self.ids[id]
                if nodeName==node:
                    pass
                else:
                    result.append((nodeName,dist))
        return result


if __name__=='__main__':
#    G = graph((6,6))
#    for i in range(1,7):
#        G.add_node(str(i))
    G = NX.Graph()
    
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
    

    G.add_edge(('1','2'))
    G.add_edge(('1','4'))
    G.add_edge(('1','5'))
    G.add_edge(('4','2'))
    G.add_edge(('4','5'))
    G.add_edge(('2','5'))
    G.add_edge(('5','3'))
    G.add_edge(('3','6'))




