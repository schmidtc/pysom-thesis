import sys
from som import *
# Research Question 1...
# Calculate the internal variance for each nueon in the network.
# Need to group all neurons by their topology and by their degree.

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
    
    #data = {}
    #for node,size,degree,aiv in ivData:
    #    if degree not in data:
    #        data[degree] = []
    #    data[degree].append(aiv)
    #degs = data.keys()
    #degs.sort()
    #groups = []
    #for deg in degs:
    #    groups.append(data[deg])
    #return ivData,groups,degs
    return ivData,None,None
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
    #out = open('q1.txt','a')
    print type,dims,clusters
    s,f = gload(dims,clusters,testNum,type)
    IV,Groups,Degs = getIVdata(s,f)
    f.close()

    f = open('q1Results/%s_%dd_%dc_no%d.iv'%(type,dims,clusters,testNum),'w')
    data = [map(str,line) for line in IV]
    data = [','.join(line) for line in data]
    data = '\n'.join(data)+'\n'
    f.write(data)
    f.close()
    #boxIV(Groups,Degs)
    #for i,group in enumerate(Groups):
    #    out.write("%d,%d,%d,%s"%(dims,clusters,testNum,type))
    #    out.write(",%d,%f,%f\n"%(Degs[i],N.mean(group),N.var(group)))
    #out.close()
    #return (IV,Groups,Degs)

def q1():
    #out = open('q1.txt','w')
    #out.write("Dims,Cluster,TestNum,Type,d,m,v\n")
    #out.close()
    
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

def q1p():
    f = open('q1.txt','r')
    header = f.readline()
    lines = f.readlines()
    lines  = [l.strip().split(',') for l in lines]
    [l.pop(3) for l in lines]
    return lines

class SomName:
    def __init__(self,nameStr):
        type,dims,clusters,number = nameStr.split('_')
        self.type = type
        self.dims = int(dims[:-1])
        self.clusters = int(clusters[:-1])

def q1BOX(path='q1Results',ttype='graph'):
    files = os.listdir(path)

 
    d = {}
    for fname in files:
        dims = SomName(fname).dims
        clusters = SomName(fname).clusters
        if dims not in d:
            d[dims] = {}
        d[dims][clusters] = 0
    for fname in files:
        f = open(os.path.join(path,fname),'r')
        if ttype in fname:
            dims = SomName(fname).dims
            clusters = SomName(fname).clusters
            data = f.readlines()
            f.close()
            data = [l.strip().split(',') for l in data]
            data = [[int(i[2]),float(i[3])] for i in data]
            data = N.array(data)
            x = data[:,0]
            y = data[:,1]
            d[dims][clusters] = y.mean()
            #print fname,y.mean()
        #return x,y

        #pylab.scatter(x,y)
    
    dims = d.keys()
    dims.sort()
    line = ['\\multicolumn{1}{c}{\\textbf{%d}}'%dim for dim in dims]
    line[-1] = '\\multicolumn{1}{c|}{\\textbf{%d}}'%dims[-1]
    print '''\\begin{table}
\\caption{Mean Internal Variane for the entire som %s}
\\label{ivtable1}
\\begin{tabular}{|c||c|c|c|c|}
\\hline
&\\multicolumn{4}{c|}{\\textbf{Dimmensions}}\\\\'''%ttype.upper()
    print '\\textbf{Clusters} & '+' & '.join(line) + '\\\\'
    print '\\hline'
    clusters = [0,2,5,10,20]
    for c in clusters:
        val = '\\textbf{%d} '%c
        for dim in dims:
            try: val += '& %.3f'%(d[dim][c])
            except: val += '& no test'
        print '\\hline'
        print val+' \\\\'
    print '\\hline'
    print "\end{tabular} \end{table}"
        
    return d
    
    #for tType,d in topos.iteritems():
    #    degs = d.keys()
    #    degs.sort()
    #    groups = []
    #    for deg in degs:
    #        groups.append(d[deg])
    #    boxIV(groups,degs)
    #return topos

        

if __name__=="__main__":
    pass
    #q1()
    #data = q1p()
    #a = stats(2,2,0)
    #b = stats(2,2,0,'rook')
    graph = q1BOX()
    print
    print
    print
    rook = q1BOX(ttype='rook')
    
