import pylab
import networkx
from math import sqrt
x = 7
y = 8

deltaX = 1.0
deltaY = sqrt(3.0/4.0)

hexX=0-deltaX
hexY=0
pts = []
grid = []
c = 0
for lcvY in range(y):
    row = []
    for lcvX in range(x):
        hexX+=deltaX
        pts.append([hexX,hexY])
        row.append(c)
        c += 1
    if (lcvY+1)%2:
        hexX=0-(deltaX/2)
    else:
        hexX=0-deltaX
    hexY=hexY+deltaY
    grid.append(row)

x,y = zip(*pts)


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

        
if __name__=='__main__':
    import Tkinter as tk
    root = tk.Tk()
    c = tk.Canvas(root, width=800,height=800)
    c.pack()

    for a,b in g.edges():
        x1,y1 = pts[a]
        x2,y2 = pts[b]
        c.create_line(x1*100+10,y1*100+10,x2*100+10,y2*100+10)

