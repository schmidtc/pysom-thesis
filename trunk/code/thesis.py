from som import *
# Research Question 1...
# Calculate the internal variance for each nueon in the network.
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
    """ takes a som """
    if not s.daMap:
        print "Please map first"
        raise "no map"
        #qerror = s.map(f)
    daMap = s.daMap
    f.reset()
    l = f.listolists()
    ivData = []
    for node,ids in daMap.iteritems():
        degree = s.G.degree(node)
        size = len(ids)
        if size > 1:
            distMatrix = pairWiseDist(ids,l)
            # for a sq. dist martix, the number of the pairWise distances is
            # equal to the totalsize (size in 1d)**2 - the number of diagonals
            # (size) over 2
            averageIV = distMatrix.sum() / (((size**2)-size)/2)
            ivData.append((node,size,degree,averageIV))
    
    data = {}
    for node,size,degree,aiv in ivData:
        if degree not in data:
            data[degree] = []
        data[degree].append(aiv)
    degs = data.keys()
    degs.sort()
    groups = []
    for deg in degs:
        groups.append(data[deg])
    return ivData,groups,degs
def boxIV(groups,degs):
    #data = N.array(zip(*l))
    pylab.boxplot(groups,positions=degs)
    pylab.show()

def q2(ivDataList):
    groups = []
    reg = []
    for ivData in ivDataList:
        node,size,degree,averageIV = zip(*ivData)
        groups.append(averageIV)
        reg.append(N.var(degree))
    return groups,reg
    
if __name__=="__main__":
    #Get the data file ready.
    f = ObsFile('testData/15d-40c-no0_scaled.dat','complete')

    #  Load spherical som.
    s = GraphTopology()
    s.load('testResults/','graph_1m')
    # Load rook som.
    s2 = GraphTopology()
    s2.load('testResults/','rook_1m')

    ### Step two, find internal variance, plot against degree
    # map(N.mean,sGroups)
    # map(N.var,sGroups)
    print "finding IV for spherical case"
    sIV,sGroups,sDegs = getIVdata(s,f)
    print "Sphere:"
    for i,group in enumerate(sGroups):
        print "group size: ", sDegs[i]
        print "mean: ", N.mean(group)
        print "variance: ", N.var(group)

    print "finding IV for rook case"
    rIV,rGroups,rDegs = getIVdata(s2,f)
    print "Rook:"
    for i,group in enumerate(rGroups):
        print "group size: ", rDegs[i]
        print "mean: ", N.mean(group)
        print "variance: ", N.var(group)
    #f = open('testResults/graph_1m.iv','w')
    #f.write('node,size,degree,averageIV\n')
    #f.writelines([','.join(map(str,line))+'\n' for line in ivData])
    #f.close()
    #f = open('testResults/rook_1m.iv','w')
    #f.write('node,size,degree,averageIV\n')
    #f.writelines([','.join(map(str,line))+'\n' for line in ivData2])
    #f.close()

    
