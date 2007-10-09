from som import *
### The Training
### Current, 642, 23*28
### Future, 4842, 70*69
def graphTest():
    G = delaunay.parseDelaunay("delaunay/642_delaunay.xyz")
    s = GraphTopology(G)
    s.Dims = 15
    s.maxN = 0.5
    s.tSteps = 100000
    s.alpha0 = 0.04
    f = ObsFile('testData/15d-40c-no0_scaled.dat','complete')
    print "init"
    s.randInit()
    print "run t=100K"
    s.run(f)
    s.save('testResults/','graph_100k')
    s.maxN = 0.333
    s.tSteps = 1000000
    s.alpha0 = 0.03
    f.reset()
    print "run t=1M"
    s.run(f)
    s.save('testResults/','graph_1m')

    f.reset()
    s.map(f)
    s.save('testResults/','graph_1m')

    f.close()
    return s
def rookGraphTest():
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
    f = ObsFile('testData/15d-40c-no0_scaled.dat','complete')
    print "init"
    s.randInit()
    print "run t=100K"
    s.run(f)
    s.save('testResults/','rook_100k')

    s.maxN = 0.333
    s.tSteps = 1000000
    s.alpha0 = 0.03
    f.reset()
    print "run t=1M"
    s.run(f)
    s.save('testResults/','rook_1m')

    f.reset()
    s.map(f)
    s.save('testResults/','rook_1m')

    f.close()
    return s
### End Training

if __name__=="__main__":
    ### Step one, train the soms
    g = graphTest()
    r = rookGraphTest()
