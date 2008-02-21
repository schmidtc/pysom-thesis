import sys
from som import *
from numpy.random import shuffle
import pylab
# Research Question 1...
# Calculate the internal variance for each nueon in the network.
# Need to group all neurons by their topology and by their degree.

def pairWiseDist(ids,lines):
    """returns a non-symtric sq. dist matrix, diag = 0, below diag = 0
    utility function called by getIVdata"""
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


def q2(ivDataList):
    groups = []
    reg = []
    for ivData in ivDataList:
        node,size,degree,averageIV = zip(*ivData)
        groups.append(averageIV)
        reg.append(N.var(degree))
    return groups,reg
    

def gload(dims,clusters,testNum=0,type='graph',path='testResults/'):
    """ Utility Function for loading a SOM that uses the networkx Graph Topology"""
    f = ObsFile('testData/%sd-%dc-no%d_rs.dat'%(dims,clusters,testNum),'complete')
    s = GraphTopology()
    s.load(path,'%s_%dd-%dc-no%d_1m'%(type,dims,clusters,testNum))
    return s,f
def stats(dims,clusters,testNum=0,type='graph',path='testResults/'):
    """ Utility function Called by q1 
        this function wraps getIVdata function."""
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
    """Calculating the IV of each neuron is rather time consuming.
        This function simply ensures that the IV has been calculated
        and saved in the q1Results folder.
    """
    files = os.listdir('testResults')
    for file in files:
        #if '_1m.' in file and '5d-10c' in file and file[-4:] == '.cod':
        if '_1m.' in file and file[-4:] == '.cod':
            #print file
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
        #print nameStr
        type,dims,clusters,number = nameStr.split('_')
        self.type = type
        self.dims = int(dims[:-1])
        self.clusters = int(clusters[:-1])
        self.number = int(number.split('.')[0][2:])
    def tdcn(self):
        return (self.type,self.dims,self.clusters,self.number)

def q1TableSet2(path='q1Results',dims=5,clusters=10,noMean=False):
    """ This function produces a latex Table showing the mean IV for each som by topology and test number.

    It returns a dictionary object containing these mean IV values organizing by, topology and test number.  This may be useful in the future."""
    files = os.listdir(path)
    print files.pop(0)
    d = {}
    for fname in files:
        finfo = IVName(fname)
        type,dim,c,number = finfo.tdcn()
        if dim == dims and c == clusters:
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

    table = """\\begin{table}
\\centering
\\caption{Mean IV for each simulation, by topology}
\\label{ivtable3}
\\begin{tabular}{|c||%(formating)s|}
\\hline
\\textbf{Simulation Number} & %(header)s \\\\
\\hline
\\hline
%(table_data)s
\\hline
\\end{tabular} \\end{table}"""
    values = {}
    types = d.keys()
    types.sort()
    tests = d[types[0]].keys()
    values['formating'] = "|".join(['c' for type in types])
    values['header'] = ' & '.join([type.title() for type in types])
    values['table_data'] = "\n\\hline\n".join( ['\\textbf{%d} & '%(test+1) + ' & '.join(['%.4f'%d[type][test] for type in types]) +' \\\\' for test in tests])
    
    print table%values


    return d

def q1Joins(path='q1Results',dims=5,clusters=10):
    """ This function creates the main data structure for questions related to
        research question 1.

        The structure is a dictionary keys by topology type, and dim size."""
    files = os.listdir(path)
    print files.pop(0)
    d = {}
    for fname in files:
        finfo = IVName(fname)
        type,dim,c,number = finfo.tdcn()
        if dim == dims and c == clusters:
            if type not in d:
                d[type] = {}
            f = open(os.path.join(path,fname),'r')
            data = f.readlines()
            f.close()
            data = [l.strip().split(',') for l in data]
            data = [[int(i[2]),float(i[3])] for i in data]
            for deg,iv in data:
                if deg not in d[type]:
                    d[type][deg] = []
                d[type][deg].append(iv)
    for type,data in d.iteritems():
        for deg,l in data.iteritems():
            d[type][deg] = array(l)
    return d

def q1BOX(path='q1Results',ttype='graph'):
    """ This function produces a table. It scans the contents of the q1Results folder, which should contain the internal variance results for all the trained soms.  It calcs the mean IV for each and puts them in a latex table (for the given topology)"""
    files = os.listdir(path)
    files.pop(0)
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
            number = IVName(fname).number
            dims = IVName(fname).dims
            clusters = IVName(fname).clusters
            data = f.readlines()
            f.close()
            data = [l.strip().split(',') for l in data]
            data = [[int(i[2]),float(i[3])] for i in data]
            data = N.array(data)
            x = data[:,0]
            y = data[:,1]
            if number == 0:
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
        delta = abs(c[:na].mean() - c[na:].mean())
        deltas.append(delta)
    realMean = abs(a.mean()-b.mean())
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
\\begin{tabular}{|c||%s|}'''%format
    print '\\hline'
    print "&" + "&".join(map(str,degs)) + '\\\\'
    print '\\hline'
    print '\\hline'
    for a in degs:
        s = str(a)
        for b in degs:
            if a==b:
                s+="& "
            else:
                s+='& %f (%f)'%rLabelMean(topoData[a],topoData[b],t=999)
        print s+'\\\\'
        print '\\hline'
    print "\end{tabular} \end{table}"
            
def createBoxPlots(q1DataStruct):
    """This function will creat the box plots for question one."""
    c = 1
    for topo in q1DataStruct:
        pylab.figure(c)
        print "Creating box plot for topology type: ",topo
        degs = q1DataStruct[topo].keys()
        degs.sort()
        groups = [q1DataStruct[topo][deg] for deg in degs]
        pylab.boxplot(groups,notch=1,positions=degs)
        c += 1
    pylab.show()

def createGroupBasedMeanIVTable(q1DataStruct):
    data = q1DataStruct
    topos = data.keys()
    print topos
    topos.sort()
    degs = set()
    for topo in topos:
        for deg in data[topo].keys():
            degs.add(deg)
    degs = list(degs)
    degs.sort()

    tableValues = {}
    tableValues['format'] = '||'.join(['|'.join(['c' for i in range(2)]) for topo in topos])
    s = ["\\multicolumn{2}{c||}{\\textbf{%s}}"%topo.title() for topo in topos]
    tableValues['header'] = ' & '.join(s)
    tableValues['header2']= ' & '.join(['N & MeanIV' for topo in topos])

    rows = ""
    for deg in degs:
        row = str(deg)
        for topo in topos:
            try:
                n = len(data[topo][deg])
                m = data[topo][deg].mean()
                #v = data[topo][deg].var()
                row += '& %d'%n
                row += '& %.4f'%m
                #row += '& %.4f'%v
            except:
                row += '&&'
        row += '\\\\ \n'
        rows += row

    rows += '\\hline \n'
    row = 'Combined'
    for topo in topos:
        nodes = []
        for deg,values in data[topo].iteritems():
            nodes.extend(list(values))
        nodes = N.array(nodes)
        n = len(nodes)
        m = nodes.mean()
        #v = nodes.var()
        row += '& %d'%n
        row += '& %.4f'%m
        #row += '& %.4f'%v
    
    rows += row + '\\\\ \n'


    tableValues['rows'] = rows
    table= """
\\begin{table}
\\caption{Mean IV grouped by a neurons degree for each topology}
\\label{meanvar1}
\\begin{tabular}{|c||%(format)s|}
\\hline
\\textbf{Degree Size} & %(header)s \\\\
\\hline
& %(header2)s \\\\
\\hline
%(rows)s\\hline
\\end{tabular} \\end{table}
"""
    print table%tableValues


if __name__=="__main__":
    #This function should always be run.
    # It does nothing unless the IV files have been removed,
    # or new test cases have been added.
    #q1() 



    #data = q1p()
    #a = stats(2,10,0)
    #a = stats(2,20,0)
    #b = stats(2,10,0,'rook')
    #b = stats(2,20,0,'rook')
    #graph = q1BOX()
    print
    print
    print
    #graph = q1BOX(ttype='graph')
    #rook = q1BOX(ttype='rook')
    #hex = q1BOX(ttype='hex')
    #geodesic = q1BOX(ttype='geodesic')
    #data = q1TableSet2()
    q1Data = q1Joins()
    createGroupBasedMeanIVTable(q1Data)
    #createBoxPlots(q1Data)
    #rLabelTables(d['rook'])
    #rLabelTables(d['graph'])
    #rLabelTables(d['hex'])
    #rLabelTables(q1Data['geodesic'])
    
