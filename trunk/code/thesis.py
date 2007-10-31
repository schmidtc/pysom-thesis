import sys
from som import *
# Research Question 1...
# Calculate the internal variance for each nueon in the network.
def pairWiseDist(ids,lines):
    """returns a non-symtric sq. dist matrix, diag = 0, below diag = 0"""
    size = len(ids)
    ivMatrix = zeros((size,size),'float')
    data = [lines[id] for id in ids]
    for i in xrange(size):
        for j in xrange(i,size):
            ivMatrix[i,j] = sqrt(sum((data[i]-data[j])**2))
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
    out = open('q1.txt','w')
    s,f = gload(dims,clusters,testNum)
    sIV,sGroups,sDegs = getIVdata(s,f)
    #boxIV(sGroups,sDegs)
    #sys.stdout.write("%d,%d,%d,%s"%(dims,clusters,testNum,type))
    for i,group in enumerate(sGroups):
        out.write("%d,%d,%d,%s"%(dims,clusters,testNum,type))
        out.write(",%d,%f,%f\n"%(sDegs[i],N.mean(group),N.var(group)))
    #    print "group size: ", sDegs[i]
    #    print "mean: ", N.mean(group)
    #    print "variance: ", N.var(group)
    #sys.stdout.write('\n')
    #sys.stdout.flush()
    out.close()

if __name__=="__main__":
    print "Dims,Cluster,TestNum,Type,d,m,v"#,d2,m2,v2,d3,m3,v3"
    stats(5,0,0)
    stats(10,0,0)
    stats(20,0,0)

    stats(5,2,0)
    stats(10,2,0)
    stats(20,2,0)

    stats(5,10,0)
    stats(10,10,0)
    stats(20,10,0)

    stats(5,20,0)
    stats(10,20,0)
    stats(20,20,0)


    stats(5,0,0,'rook')
    stats(10,0,0,'rook')
    stats(20,0,0,'rook')

    stats(5,2,0,'rook')
    stats(10,2,0,'rook')
    stats(20,2,0,'rook')

    stats(5,10,0,'rook')
    stats(10,10,0,'rook')
    stats(20,10,0,'rook')

    stats(5,20,0,'rook')
    stats(10,20,0,'rook')
    stats(20,20,0,'rook')
