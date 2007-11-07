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
def mapClusters(s,f):
    daMap = s.daMap
    f.reset()
    l = f.listolists(comments=True)
    for node,ids in daMap.iteritems():
        c = []
        for id in ids:
            c.append(l[id][0])
        daMap[node] = c
    return daMap
def mapCA(d,size):
    s = '1\n'
    nodes = range(size)
    for node in nodes:
        try:
            ids = d[node]
            if len(set(ids)) > 1:
                s += '98\n'
                print node,ids
            else:
                s += str(set(ids).pop())
                s += '\n'
        except:
            s+= '99\n'
    return s
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
    out = open('q1.txt','a')
    s,f = gload(dims,clusters,testNum,type)
    IV,Groups,Degs = getIVdata(s,f)
    #boxIV(sGroups,sDegs)
    #sys.stdout.write("%d,%d,%d,%s"%(dims,clusters,testNum,type))
    for i,group in enumerate(Groups):
        out.write("%d,%d,%d,%s"%(dims,clusters,testNum,type))
        out.write(",%d,%f,%f\n"%(Degs[i],N.mean(group),N.var(group)))
    #    print "group size: ", sDegs[i]
    #    print "mean: ", N.mean(group)
    #    print "variance: ", N.var(group)
    #sys.stdout.write('\n')
    #sys.stdout.flush()
    out.close()
    return (IV,Groups,Degs)

def q1():
    out = open('q1.txt','w')
    out.write("Dims,Cluster,TestNum,Type,d,m,v\n")
    out.close()
    i = 24
    print i;i-=1
    stats(5,0,0)
    print i;i-=1
    stats(10,0,0)
    print i;i-=1
    stats(20,0,0)
    print i;i-=1

    stats(5,2,0)
    print i;i-=1
    stats(10,2,0)
    print i;i-=1
    stats(20,2,0)
    print i;i-=1

    stats(5,10,0)
    print i;i-=1
    stats(10,10,0)
    print i;i-=1
    stats(20,10,0)
    print i;i-=1

    stats(5,20,0)
    print i;i-=1
    stats(10,20,0)
    print i;i-=1
    stats(20,20,0)
    print i;i-=1


    stats(5,0,0,'rook')
    print i;i-=1
    stats(10,0,0,'rook')
    print i;i-=1
    stats(20,0,0,'rook')
    print i;i-=1

    stats(5,2,0,'rook')
    print i;i-=1
    stats(10,2,0,'rook')
    print i;i-=1
    stats(20,2,0,'rook')
    print i;i-=1

    stats(5,10,0,'rook')
    print i;i-=1
    stats(10,10,0,'rook')
    print i;i-=1
    stats(20,10,0,'rook')
    print i;i-=1

    stats(5,20,0,'rook')
    print i;i-=1
    stats(10,20,0,'rook')
    print i;i-=1
    stats(20,20,0,'rook')
    print i;i-=1

def q1p():
    f = open('q1.txt','r')
    header = f.readline()
    lines = f.readlines()
    lines  = [l.strip().split(',') for l in lines]
    [l.pop(3) for l in lines]
    return lines

if __name__=="__main__":
    q1()
    #data = q1p()
    #a = stats(5,0,0)
    #b = stats(5,0,0,'rook')
    
