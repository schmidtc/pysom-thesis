from som import *
# Research Question 1...
# Calculat the internal variance for each nueon in the network.
def pairWiseDist(ids,lines):
    """returns a non-symtric sq. dist matrix, diag = 0, below diag = 0"""
    size = len(ids)
    ivMatrix = zeros((size,size),'float')
    lines = [lines[id] for id in ids]
    for i in xrange(size):
        for j in xrange(i,size):
            ivMatrix[i,j] = sqrt(sum((lines[i]-lines[j])**2))
    return ivMatrix
def getIVdata(s,f):
    """ takes a som and a obsFile """
    if not s.daMap:
        print "Please map first"
        #qerror = s.map(f)
    daMap = s.daMap
    l = f.listolists()
    results = []
    for node,ids in daMap.iteritems():
        degree = s.G.degree(node)
        size = len(ids)
        if size > 1:
            distMatrix = pairWiseDist(ids,l)
            # for a sq. dist martix, the number of the pairWise distances is
            # equal to the totalsize (size in 1d)**2 - the number of diagonals
            # (size) over 2
            averageIV = distMatrix.sum() / (((size**2)-size)/2)
            results.append((node,size,degree,averageIV))
    return results
def boxIV(ivData):
    data = {}
    for node,size,degree,aiv in ivData:
        if degree not in data:
            data[degree] = []
        data[degree].append(aiv)
    degs = data.keys()
    degs.sort()
    l = []
    for deg in degs:
        l.append(data[deg])
    #data = N.array(zip(*l))
    pylab.boxplot(l,positions=degs)
    pylab.show()
    return l,degs
def graphTestMapIV():
    #Load spherical som.
    G = delaunay.parseDelaunay("delaunay/642_delaunay.xyz")
    s = GraphTopology(G)
    s.Dims = 15
    f = ObsFile('testData/15d-40c-no0_scaled.dat','complete')
    s.load('testResults/','graph_1m')

    #Load rook test
    f2 = ObsFile('testData/15d-40c-no0_scaled.dat','complete')
    g = grid2Rook(23,28,binary=1)
    G2 = NX.Graph()
    for node in g:
        for neighbor in g[node][1]:
            G2.add_edge((node,neighbor))
    s2 = GraphTopology(G2)
    s2.Dims = 15
    s2.load('testResults/','rook_1m')

    print "finding IV for sphereical case"
    ivData = getIVdata(s,f)
    #s.save('testResults/','graph_100k')
    print "finding IV for rook case"
    ivData2 = getIVdata(s2,f2)
    #s2.save('testResults/','rook_100k')
    
    return {'sphere':(ivData),'rook':(ivData2)}

if __name__=="__main__":
    ### Step two, find internal variance, plot against degree
    #q1 = graphTestMapIV()
    #ivData = q1['sphere']
    #ivData2 = q1['rook']
    '''
    groups,degrees = boxIV(ivData)
    print "Sphere:"
    for i,group in enumerate(groups):
        print "group size: ", degrees[i]
        print "mean: ", N.mean(group)
        print "variance: ", N.var(group)
    groups2,degrees2 = boxIV(ivData2)
    print "Rook:"
    for i,group in enumerate(groups2):
        print "group size: ", degrees2[i]
        print "mean: ", N.mean(group)
        print "variance: ", N.var(group)
    ''' 
    #f = open('testResults/graph_1m.iv','w')
    #f.write('node,size,degree,averageIV\n')
    #f.writelines([','.join(map(str,line))+'\n' for line in ivData])
    #f.close()
    #f = open('testResults/rook_1m.iv','w')
    #f.write('node,size,degree,averageIV\n')
    #f.writelines([','.join(map(str,line))+'\n' for line in ivData2])
    #f.close()


    #daMap,qerror = graphTestMap()
