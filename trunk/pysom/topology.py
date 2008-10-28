"""
======================================================================
Python Self-Organizing Maps -- Topology
----------------------------------------------------------------------
AUTHOR(S):      Charles R. Schmidt cschmidt@rohan.sdsu.edu
======================================================================
"""

import networkx
from utils.grid2rook import grid2Rook

def rookGraph(rows, cols):
    ''' Create a rectangular graph topology '''
    rook = grid2Rook(rows,cols,binary=1)
    G = networkx.Graph()
    for node in rook:
        for neighbor in rook[node][1]:
            G.add_edge((node,neighbor))
    return G
def hexGraph(rows, cols):
    ''' Create a hexagonal graph topology '''
    x = cols
    y = rows
    grid = []
    c = 0
    for i in range(y):
        row = []
        for j in range(x):
            row.append(c)
            c += 1
        grid.append(row)
    g = networkx.Graph()
    for i,row in enumerate(grid):
        # L * * *
        # R  * * *
        # L * * *
        for j,ptID in enumerate(row):
            if i%2: # R, can never be first row.
                g.add_edge(ptID,grid[i-1][j]) #my upper neighbor
                if j < len(row) - 1: #not last column
                    g.add_edge(ptID,grid[i][j+1]) #my right neighbor
                    g.add_edge(ptID,grid[i-1][j+1]) #my upper right neighbor
                if i < len(grid) -1: #not last row
                    g.add_edge(ptID,grid[i+1][j]) #my lower neighbor
                    if j < len(row) - 1: #not last column
                        g.add_edge(ptID,grid[i+1][j+1]) #my lower right neighbor
            else: # L
                if j < len(row)-1:
                    g.add_edge(ptID,grid[i][j+1]) #my right neighbor
    return g
