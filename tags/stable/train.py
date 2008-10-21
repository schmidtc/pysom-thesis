from som import *
import time
### The Training
### Current, 642, 23*28
### Future, 4842, 70*69
def graphTrain(G,type,dims,clusters,testNum):
    s = GraphTopology(G)
    s.Dims = dims
    s.maxN = 0.5
    s.tSteps = 100000
    s.alpha0 = 0.04
    f = ObsFile('../data/trainingData/%dd-%dc-no%d_rs.dat'%(dims,clusters,testNum),'complete')
    print "init"
    s.randInit()
    print "run t=100K"
    s.run(f)
    s.save('../data/trainedSOMs/','%s_%dd-%dc-no%d_100k'%(type,dims,clusters,testNum))
    s.maxN = 0.333
    s.tSteps = 1000000
    s.alpha0 = 0.03
    f.reset()
    print "run t=1M"
    s.run(f)
    s.save('../data/trainedSOMs/','%s_%dd-%dc-no%d_1m'%(type,dims,clusters,testNum))

    f.reset()
    s.map(f)
    s.save('../data/trainedSOMs/','%s_%dd-%dc-no%d_1m'%(type,dims,clusters,testNum))

    f.close()
    return s
### End Training

if __name__=="__main__":

    startGraphs = time.time()
    #build graphs
    geodesic = delaunay.parseDelaunay("geodesic/geodesic_642_delaunay.xyz")
    endGraphGeodesic = time.time()
    sphere = delaunay.parseDelaunay("delaunay/642_delaunay.xyz")
    endGraphSphere = time.time()
    #grid2Rook(row,cols,binary=1)
    g = grid2Rook(23,28,binary=1)
    rook = NX.Graph()
    for node in g:
        for neighbor in g[node][1]:
            rook.add_edge((node,neighbor))
    endGraphRook = time.time()
    hex = hexGraph(23,28)
    endGraphHex = time.time()

    #for i in range(10):
    
    startHex = time.time()
    graphTrain(hex,'hex',3,7,1)
    endHex = time.time()

    startGeodesic = time.time()
    graphTrain(geodesic,'geodesic',3,7,1)
    endGeodesic = time.time()

    startRook = time.time()
    graphTrain(rook,'rook',3,7,1)
    endRook = time.time()

    startSphere = time.time()
    graphTrain(sphere,'graph',3,7,1)
    endSphere = time.time()

    #for i in range(7,10):
    #    graphTrain(rook,'rook',3,8,i)
    #    graphTrain(sphere,'graph',3,8,i)
    #graphTrain(rook,'rook',3,8,8)
    #graphTrain(sphere,'graph',3,8,8)
    #graphTrain(rook,'rook',3,8,9)
    #graphTrain(sphere,'graph',3,8,9)
    
    #graphTrain(rook,'rook',3,7,10)
    #graphTrain(hex,'hex',3,7,0)

    #def bora():
    #    pass
    #def neve():
    #    pass
    #def sheldon():
    #    pass
    #def haar():
    #    pass

    #import socket
    #hostname = socket.gethostname()
    #host = hostname.split('.')[0]
    #dispatch = {'bora':bora,'neve':neve,'haar':haar,'sheldon':sheldon}
    #dispatch[host]()



    #for dims in dimSet:
    #    for clusters in [0,2,5,10,20]:
    #        graphTrain(geodesic,'geodesic',dims,clusters,0)
    print "\n\n\n\n\n\n\n\n\n"
    print "Timings...."
    print "Graph Geod: ", startGraphs - endGraphGeodesic
    print "Graph Sphe: ", endGraphHex - endGraphSphere
    print "Graph Rook: ", endGraphSphere - endGraphRook
    print "Graph  Hex: ", endGraphRook - endGraphHex
    print
    print
    print "Training Geo: ", startGeodesic - endGeodesic
    print "Training Sph: ", startSphere - endSphere
    print "Training Rok: ", startRook - endRook
    print "Training Hex: ", startHex - endHex

