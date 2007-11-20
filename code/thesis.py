import sys
from som import *
from numpy.random import shuffle
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

def q1():
    files = os.listdir('testResults')
    for file in files:
        if '_1m.' in file and '5d-10c' in file and file[-4:] == '.cod':
            type,dcn,rest = file.split('_')
            d,c,n = dcn.split('-')
            d = int(d[:-1])
            c = int(c[:-1])
            n = int(n[2:])
            if os.path.exists('q1Results/%s_%dd_%dc_no%d.iv'%(type,d,c,n)):
                pass
            else:
                stats(d,c,n,type)

class IVName:
    def __init__(self,nameStr):
        print nameStr
        type,dims,clusters,number = nameStr.split('_')
        self.type = type
        self.dims = int(dims[:-1])
        self.clusters = int(clusters[:-1])
        self.number = int(number.split('.')[0][2:])
    def tdcn(self):
        return (self.type,self.dims,self.clusters,self.number)

def q1TableSet2(path='q1Results',dims=5,clusters=10,noMean=False):
    files = os.listdir(path)
    print files.pop(0)
    d = {}
    for fname in files:
        finfo = IVName(fname)
        type,dims,clusters,number = finfo.tdcn()
        if type not in d:
            d[type]={}
        f = open(os.path.join(path,fname),'r')
        data = f.readlines()
        f.close()
        data = [l.strip().split(',') for l in data]
        data = [[int(i[2]),float(i[3])] for i in data]
        data = N.array(data)
        x = data[:,0]
        y = data[:,1]
        if noMean:
            d[type][number] = zip(x,y)
        else:
            d[type][number] = y.mean()
    return d

def q1Joins(path='q1Results',dims=5,clusters=10):
    files = os.listdir(path)
    print files.pop(0)
    d = {}
    for fname in files:
        finfo = IVName(fname)
        type,dims,clusters,number = finfo.tdcn()
        if type not in d:
            if type == 'graph':
                d[type]={5:[],6:[],7:[]}
            else:
                d[type]={2:[],3:[],4:[]}
        f = open(os.path.join(path,fname),'r')
        data = f.readlines()
        f.close()
        data = [l.strip().split(',') for l in data]
        data = [[int(i[2]),float(i[3])] for i in data]
        for dim,iv in data:
            d[type][dim].append(iv)
    for type,data in d.iteritems():
        for dim,l in data.iteritems():
            d[type][dim] = array(l)
    return d

def q1BOX(path='q1Results',ttype='graph'):
    """ This function produces a table. It scans the contents of the q1Results folder, which should contain the internal variance results for all the trained soms.  It calcs the mean IV for each and puts them in a latex table (for the given topology)"""
    files = os.listdir(path)
    d = {}
    for fname in files:
        dims = IVName(fname).dims
        clusters = IVName(fname).clusters
        if IVName(fname).type == ttype:
            if dims not in d:
                d[dims] = {}
            d[dims][clusters] = 0
    for fname in files:
        f = open(os.path.join(path,fname),'r')
        if ttype in fname:
            dims = IVName(fname).dims
            clusters = IVName(fname).clusters
            data = f.readlines()
            f.close()
            data = [l.strip().split(',') for l in data]
            data = [[int(i[2]),float(i[3])] for i in data]
            data = N.array(data)
            x = data[:,0]
            y = data[:,1]
            d[dims][clusters] = y.mean()

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
            try: val += '& %.4f'%(d[dim][c])
            except: val += '& no test'
        print '\\hline'
        print val+' \\\\'
    print '\\hline'
    print "\end{tabular} \end{table}"
        
    return d
    
def rLabelMean(a,b,t=999):
    c = list(a); c.extend(b)
    c = array(c)
    na = len(a)
    nb = len(b)
    deltas = []
    for i in range(t):
        shuffle(c)
        delta = c[:na].mean() - c[na:].mean()
        deltas.append(delta)
    realMean = a.mean()-b.mean()
    deltas.append(realMean)
    deltas.sort()
    i = deltas.index(realMean)
    p = (t+1 - i)/float(t+1)
    return realMean,p

def rLabelTables(topoData):
    degs = topoData.keys()
    degs.sort()
    format = '|'.join(['c' for d in degs])
    print '''\\begin{table}
\\caption{Random Labeling Mean Tests,  delta (p-Value)}
\\label{randomLabelTable}
\\begin{tabular}{|c|%s|}'''%format
    print "&" + "&".join(map(str,degs)) + '\\\\'
    for a in degs:
        s = str(a)
        for b in degs:
            if a==b:
                s+="& "
            else:
                s+='& %f (%f)'%rLabelMean(topoData[a],topoData[b],t=9999)
        print s+'\\\\'
    print "\end{tabular} \end{table}"
            

if __name__=="__main__":
    q1()
    #data = q1p()
    #a = stats(2,10,0)
    #a = stats(2,20,0)
    #b = stats(2,10,0,'rook')
    #b = stats(2,20,0,'rook')
    #graph = q1BOX()
    print
    print
    print
    #rook = q1BOX(ttype='rook')
    #data = q1TableSet2()
    d= q1Joins()
    rLabelTables(d['rook'])
    
