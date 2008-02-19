from som import *
### The Training
### Current, 642, 23*28
### Future, 4842, 70*69
def graphTrain(G,type,dims,clusters,testNum):
    s = GraphTopology(G)
    s.Dims = dims
    s.maxN = 0.5
    s.tSteps = 100000
    s.alpha0 = 0.04
    f = ObsFile('testData/%dd-%dc-no%d_rs.dat'%(dims,clusters,testNum),'complete')
    print "init"
    s.randInit()
    print "run t=100K"
    s.run(f)
    s.save('testResults/','%s_%dd-%dc-no%d_100k'%(type,dims,clusters,testNum))
    s.maxN = 0.333
    s.tSteps = 1000000
    s.alpha0 = 0.03
    f.reset()
    print "run t=1M"
    s.run(f)
    s.save('testResults/','%s_%dd-%dc-no%d_1m'%(type,dims,clusters,testNum))

    f.reset()
    s.map(f)
    s.save('testResults/','%s_%dd-%dc-no%d_1m'%(type,dims,clusters,testNum))

    f.close()
    return s
### End Training

if __name__=="__main__":
    from hex import hexGraph

    #build graphs
    geodesic = delaunay.parseDelaunay("geodesic/geodesic_642_delaunay.xyz")
    sphere = delaunay.parseDelaunay("delaunay/642_delaunay.xyz")
    g = grid2Rook(23,28,binary=1)
    rook = NX.Graph()
    for node in g:
        for neighbor in g[node][1]:
            rook.add_edge((node,neighbor))
    hex = hexGraph(23,28)

    #graphTrain(sphere,'Sphere',5,10,0)
    #graphTrain(rook,'Rook',5,10,0)
    #graphTrain(hex,'Hex',5,10,0)

    def bora():
        #graphTrain(geodesic,'geodesic',5,10,0)
        graphTrain(geodesic,'geodesic',5,10,1)
        graphTrain(geodesic,'geodesic',5,10,2)
    def neve():
        graphTrain(geodesic,'geodesic',5,10,3)
        graphTrain(geodesic,'geodesic',5,10,4)
    def sheldon():
        graphTrain(geodesic,'geodesic',5,10,5)
        graphTrain(geodesic,'geodesic',5,10,6)
        graphTrain(geodesic,'geodesic',5,10,7)
    def haar():
        graphTrain(geodesic,'geodesic',5,10,8)
        graphTrain(geodesic,'geodesic',5,10,9)


    import socket
    hostname = socket.gethostname()
    host = hostname.split('.')[0]
    dispatch = {'bora':bora,'neve':neve,'haar':haar,'sheldon':sheldon}
    dimSet = dispatch[host]()



    #for dims in dimSet:
    #    for clusters in [0,2,5,10,20]:
    #        graphTrain(geodesic,'geodesic',dims,clusters,0)

