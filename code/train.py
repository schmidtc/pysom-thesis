from som import *
### The Training
### Current, 642, 23*28
### Future, 4842, 70*69
def graphTest(dims,clusters,testNum):
    G = delaunay.parseDelaunay("delaunay/642_delaunay.xyz")
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
    s.Dims = dims
    s.maxN = 0.5
    s.tSteps = 100000
    s.alpha0 = 0.04
    f = ObsFile('testData/%dd-%dc-no%d_rs.dat'%(dims,clusters,testNum),'complete')
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
def Test():
    #g = grid2Rook(23,28,binary=1)
    G = NX.Graph()
    G.add_edge(0,1)
    G.add_edge(1,2)
    G.add_edge(2,3)
    G.add_edge(3,4)
    G.add_edge(4,5)
    G.add_edge(5,6)
    G.add_edge(6,7)
    G.add_edge(7,8)
    G.add_edge(8,9)
    #G.add_edge(9,0)
    s = GraphTopology(G)
    s.Dims = 4
    s.maxN = 0.5
    s.tSteps = 100000
    s.alpha0 = 0.04
    f = ObsFile('testData/test.dat','complete')
    print "init"
    s.randInit()
    print "run t=100K"
    s.run(f)
    s.save('testResults/','testl_100k')

    s.maxN = 0.5
    s.tSteps = 1000000
    s.alpha0 = 0.03
    f.reset()
    print "run t=1M"
    #s.run(f)
    #s.save('testResults/','test_1m')

    f.reset()
    s.map(f)
    #s.save('testResults/','test_1m')

    f.close()
    return s

def neve():
    print "running neve training"
    graphTest(5,10,0)
    graphTest(5,10,1)
    graphTest(5,10,2)
    graphTest(5,10,3)
    graphTest(5,10,4)
    graphTest(5,10,5)
    graphTest(5,10,6)
def haar():
    print "running haar training"
    rookGraphTest(5,10,0)
    rookGraphTest(5,10,1)
    rookGraphTest(5,10,2)
    rookGraphTest(5,10,3)
    rookGraphTest(5,10,4)
    rookGraphTest(5,10,5)
def bora():
    print "running bora training"
    graphTest(5,10,7)
    graphTest(5,10,8)
    graphTest(5,10,9)
    rookGraphTest(5,10,6)
    rookGraphTest(5,10,7)
    rookGraphTest(5,10,8)
    rookGraphTest(5,10,9)
if __name__=="__main__":
    import socket
    hostname = socket.gethostname()
    host = hostname.split('.')[0]
    dispatch = {'bora':bora,'neve':neve,'haar':haar}
    dispatch[host]()
