import networkx
from math import sqrt

def hexGraph(rows, cols):
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

def hexPts(cols,rows):
    """ Draw the pts for a hex topology, modified from Martin's CODtoSHP.py """
    x = rows
    y = cols
    deltaX = 1.0
    deltaY = sqrt(3.0/4.0)
    hexX=0-deltaX
    hexY=0
    pts = []
    for lcvY in range(y):
        for lcvX in range(x):
            hexX+=deltaX
            pts.append([hexX,hexY])
        if (lcvY+1)%2:
            hexX=0-(deltaX/2)
        else:
            hexX=0-deltaX
        hexY=hexY+deltaY
    return pts

def rookPoly(pts):
    """ Draw the polygons for a rook topology """
    deltaX = 1.0
    deltaY = 1.0
    centroidsDist = 1.0
    polygons = []
    for i in pts:
        pX = i[0]
        pY = i[1]
        poly =[ 0,
                [(pX-(deltaX/2),pY+(deltaY/2)), 
                (pX+(deltaX/2),pY+(deltaY/2)),
                (pX+(deltaX/2),pY-(deltaY/2)),
                (pX-(deltaX/2),pY-(deltaY/2)),
                (pX-(deltaX/2),pY+(deltaY/2)) ]]
        polygons.append(poly)
    return polygons
def hexPoly(pts):
    """ Draw the polygons for a hex topology, modified from Martin's CODtoSHP.py """
    deltaX = 1.0
    deltaY = sqrt(3.0/4.0)
    centroidsDist = 1.0
    polygons = []
    for i in pts:
        #center point
        pX=i[0]
        pY=i[1]
        #sides numberd in order of min length
        side2=0.5*centroidsDist
        side1=side2/sqrt(3)
        side3=2*side1
        #derive extreama
        minX=pX-side2
        maxX=pX+side2
        minY=pY-side3
        maxY=pY+side3
        #bounding box
        Box=[minX,minY,maxX,maxY]
        #number of parts
        NumParts=1
        #number of points
        NumPoints=6
        #index to first point in part
        Parts=0
        #starts from top most, left most, and goes clock-wise        
        Points=[Box,[[pX,pY+side3],[pX+side2,pY+side1],[pX+side2,pY-side1],[pX,pY-side3],[pX-side2,pY-side1],[pX-side2,pY+side1]]]
        polygons.append(Points)
    return polygons
def writePoly(fName,polys):
    f = open(fName,'w')
    f.write('POLYGON\n')
    for i,poly in enumerate(polys):
        f.write('%d 0\n'%(i))
        poly = poly[1]
        poly = ['%d %f %f\n'%(i,pt[0],pt[1]) for i,pt in enumerate(poly)]
        f.writelines(poly)
        f.write('%d'%(i+1)+poly[0][1:]) #close the loop
    f.write('END\n')
    f.close()

def drawPts(g,pts,w=False):
    scale = 25
    margin = 20
    radius = 2
    for a,b in g.edges():
        x1,y1 = pts[a]
        x2,y2 = pts[b]
        x1,y1,x2,y2 = x1*scale+margin,y1*scale+margin,x2*scale+margin,y2*scale+margin
        c.create_line(x1,y1,x2,y2)
    for i,pt in enumerate(pts):
        if w:
            radius = w[i]*50
        x1,y1 = pt
        x1,y1 = x1*scale+margin,y1*scale+margin
        c.create_oval(x1-radius,y1+radius,x1+radius,y1-radius,fill='red',outline='red')
def drawPoly(polys):
    scale = 40
    margin = 50
    for poly in polys:
        poly = poly[1]
        poly = [[x*scale+margin,y*scale+margin] for x,y in poly]
        c.create_polygon(poly,fill='#eeeeee',outline='black',activefill='blue')


if __name__=='__main__':
    import Tkinter as tk
    import networkx as nx
    root = tk.Tk()
    c = tk.Canvas(root, width=800,height=600)
    c.pack()
    
    #g = hexGraph(23,28)
    pts = hexPts(6,5)
    #cc = nx.centrality.closeness_centrality(g)
    #drawPts(g,pts)
    drawPoly(hexPoly(pts[5:]))

    pts = [(i,j-0.5) for i in range(6,6+6) for j in range(1,1+5)]
    drawPoly(rookPoly(pts[5:]))


