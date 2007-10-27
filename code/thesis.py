import sys
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
    

def gload(dims,clusters,testNum=0,type='graph',path='testResults/'):
    f = ObsFile('testData/%sd-%dc-no%d_rs.dat'%(dims,clusters,testNum),'complete')
    s = GraphTopology()
    s.load(path,'%s_%dd-%dc-no%d_1m'%(type,dims,clusters,testNum))
    return s,f
def stats(dims,clusters,testNum=0,type='graph',path='testResults/'):
    s,f = gload(dims,clusters,testNum)
    sIV,sGroups,sDegs = getIVdata(s,f)
    boxIV(sGroups,sDegs)
    #print dims,clusters,testNum,type,
    #for i,group in enumerate(sGroups):
    #    print "group size: ", sDegs[i]
    #    print "mean: ", N.mean(group)
    #    print "variance: ", N.var(group)

if __name__=="__main__":
    stats(5,2,0)
