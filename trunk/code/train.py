from som import *
### The Training
### Current, 642, 23*28
### Future, 4842, 70*69
def graphTest(dims,clusters,testNum):
    G = delaunay.parseDelaunay("delaunay/642_delaunay.xyz")
    s = GraphTopology(G)
    s.Dims = 15
    s.maxN = 0.5
    s.tSteps = 100000
    s.alpha0 = 0.04
    f = ObsFile('testData/%dd-%dc-no%d_scaled.dat'%(dims,clusters,testNum),'complete')
    print "init"
    s.randInit()
    print "run t=100K"
    s.run(f)
    s.save('testResults/','graph_%dd-%dc-no%d_100k'%(dims,clusters,testNum))
    s.maxN = 0.333
    s.tSteps = 1000000
    s.alpha0 = 0.03
    f.reset()
    print "run t=1M"
    s.run(f)
    s.save('testResults/','graph_%dd-%dc-no%d_1m'%(dims,clusters,testNum))

    f.reset()
    s.map(f)
    s.save('testResults/','graph_%dd-%dc-no%d_1m'%(dims,clusters,testNum))

    f.close()
    return s
def rookGraphTest(dims,clusters,testNum):
    g = grid2Rook(23,28,binary=1)
    G = NX.Graph()
    for node in g:
        for neighbor in g[node][1]:
            G.add_edge((node,neighbor))
    s = GraphTopology(G)
    s.Dims = 15
    s.maxN = 0.5
    s.tSteps = 100000
    s.alpha0 = 0.04
    f = ObsFile('testData/%dd-%dc-no%d_scaled.dat'%(dims,clusters,testNum),'complete')
    print "init"
    s.randInit()
    print "run t=100K"
    s.run(f)
    s.save('testResults/','rook_%dd-%dc-no%d_100k'%(dims,clusters,testNum))

    s.maxN = 0.333
    s.tSteps = 1000000
    s.alpha0 = 0.03
    f.reset()
    print "run t=1M"
    s.run(f)
    s.save('testResults/','rook_%dd-%dc-no%d_1m'%(dims,clusters,testNum))

    f.reset()
    s.map(f)
    s.save('testResults/','rook_%dd-%dc-no%d_1m'%(dims,clusters,testNum))

    f.close()
    return s
### End Training

if __name__=="__main__":
    ### Step one, train the soms
    graphTest(5,0,0)
    graphTest(5,0,1)
    graphTest(10,0,0)
    graphTest(10,0,1)
    graphTest(20,0,0)
    graphTest(20,0,1)

    graphTest(5,2,0)
    graphTest(5,2,1)
    graphTest(10,2,0)
    graphTest(10,2,1)
    graphTest(20,2,0)
    graphTest(20,2,1)

    rookGraphTest(5,0,0)
    rookGraphTest(5,0,1)
    rookGraphTest(10,0,0)
    rookGraphTest(10,0,1)
    rookGraphTest(20,0,0)
    rookGraphTest(20,0,1)

    rookGraphTest(5,2,0)
    rookGraphTest(5,2,1)
    rookGraphTest(10,2,0)
    rookGraphTest(10,2,1)
    rookGraphTest(20,2,0)
    rookGraphTest(20,2,1)
