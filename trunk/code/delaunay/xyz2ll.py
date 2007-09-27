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
    lines = []
    nodes = set()
    for line in f:
        try:
            line = line.strip().split()
            line = map(float,line)
            pt = toLngLat(line)
            print pt
        except:
            print
if __name__=="__main__":
    import sys
    filename = sys.argv[1]
    parseDelaunay(filename)
"""
    
    for i,line in enumerate(lines):
        line = lines[i]
        if line[0] == '#':
            pass
        elif len(line) < 5:
            pass
        elif lines[i-1] == lines[i+1]:
            line = line.split()
            line = map(float,line)
            verts.append(line)
        elif len(line) > 10 and len(lines[i+1]) > 10:
            line0 = line.split()
            line1 = lines[i+1].split()
        line0 = map(float,line0)
        line1 = map(float,line1)
        edges.append((line0,line1))
            
def delauny2W():
    pass
f = open('voronoi.xyz','r')
lines = f.readlines()
f.close()

verts = []
edges = []
num = len(lines)


for i in xrange(num-1):
    line = lines[i]
    if line[0] == '#':
        pass
    elif len(line) < 5:
        pass
    elif lines[i-1] == lines[i+1]:
        line = line.split()
        line = map(float,line)
        verts.append(line)
    elif len(line) > 10 and len(lines[i+1]) > 10:
        line0 = line.split()
        line1 = lines[i+1].split()
        line0 = map(float,line0)
        line1 = map(float,line1)
        edges.append((line0,line1))

o = open('vor.txt','w')
o.write("Polyline\n")
fixedEdges = []
for edge in edges:
    p0,p1 = map(toLngLat,edge)
    p0,p1 = map(degrees,p0),map(degrees,p1)
    #who knew XOR would ever come in handy?
    if ((p0[0] < -90) ^ (p1[0] < -90)) and ((p0[0] >90) ^ (p1[0] > 90)):
        if p0[0] < p1[0]:
            neg = p0
            pos = p1
            x1,y1 = p0
            x2,y2 = p1
        else:
            neg = p1
            pos = p0    
            x1,y1 = p1
            x2,y2 = p0

        x1 = -1*(x1+180.0)
        x2 = 180.0-x2
        deltaY = y1-y2
        deltaX = x1-x2
        m = deltaY/deltaX
        b = y1 - m*x1
        edge1 = (neg,(-180,b))
        edge2 = ((180,b),pos)

        fixedEdges.append(edge1)
        fixedEdges.append(edge2)
    else:
        fixedEdges.append((p0,p1))
        


for i in xrange(len(fixedEdges)):
    p0,p1 = fixedEdges[i]
    o.write('%d 0\n'%i)
    o.write('0 %f %f 0.0 0.0\n'%(p0[0],p0[1]))
    o.write('1 %f %f 0.0 0.0\n'%(p1[0],p1[1]))

o.write('END\n')
o.close()
"""
