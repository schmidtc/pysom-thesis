import sys
import networkx as nx
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
def avgQE(node,ids,lines):
    qe = 0
    for id in ids:
        line = lines[id]
        qe += sqrt(sum((node-line)**2))
    aqe = (qe/float(len(lines)))
    return aqe
def getCluster(ids,c):
    clust = [c[id] for id in ids]
    clust.sort()
    dclust = {}
    for i in clust:
        if i not in dclust:
            dclust[i] = 0
        dclust[i] += 1
    keys = dclust.keys()
    keys.sort()
    counts = [dclust[key] for key in keys]
    scounts = float(sum(counts))
    pcounts = [i/scounts for i in counts]
    i = pcounts.index(max(pcounts))
    return (keys[i],pcounts[i])
    
        
        
def getIVdata(s,f):
    """ takes a som """
    if not s.daMap:
        print "Please map first"
        raise "no map"
        #qerror = s.map(f)
    daMap = s.daMap
    f.reset()
    l = f.listolists()
    #c = f.listolists(comments=True)
    #if c[0]:
    #    c = [i[0] for i in c]
    #    c = map(int,c)
    #else:
    #    c = False
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
            #averageIV = distMatrix.max()
            #averageIV = avgQE(s.nodes[node],ids,l)
            #if c:
            #    cluster,pclust = getCluster(ids,c)
            #else:
            #    cluster,pclust = 0,0
            ivData.append((node,size,degree,averageIV))
            #ivData.append((node,size,degree,cluster,pclust))
    
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
    return ivData


def gload(dims,clusters,testNum=0,type='graph',path='../data/trainedSOMs/'):
    """ Utility Function for loading a SOM that uses the networkx Graph Topology"""
    f = ObsFile('../data/trainingData/%sd-%dc-no%d_rs.dat'%(dims,clusters,testNum),'complete')
    s = GraphTopology()
    s.load(path,'%s_%dd-%dc-no%d_1m'%(type,dims,clusters,testNum))
    return s,f
def stats(dims,clusters,testNum=0,type='graph',path='../data/trainedSOMs/'):
    """ Utility function Called by q1 
        this function wraps getIVdata function."""
    print type,dims,clusters
    s,f = gload(dims,clusters,testNum,type)
    IV = getIVdata(s,f)
    f.close()

    f = open('../data/ivFiles/%s_%dd_%dc_no%d.iv'%(type,dims,clusters,testNum),'w')
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
    files = os.listdir('../data/trainedSOMs')
    for file in files:
        #if '_1m.' in file and '5d-10c' in file and file[-4:] == '.cod':
        if '_1m.' in file and file[-4:] == '.cod':
            #print file
            type,dcn,rest = file.split('_')
            d,c,n = dcn.split('-')
            d = int(d[:-1])
            c = int(c[:-1])
            n = int(n[2:])
            if os.path.exists('../data/ivFiles/%s_%dd_%dc_no%d.iv'%(type,d,c,n)):
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

def q1TableSet2(path='../data/ivFiles',dims=5,clusters=10,noMean=False):
    """ T his function produces a latex Table showing the mean IV for each som by topology and test number.

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

def q1Joins(path='../data/ivFiles',dims=5,clusters=10):
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

    

def q1BOX(path='../data/ivFiles',ttype='graph'):
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
            if number == 0: #If we have mutiple test numbers, only use test 0!
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
&\\multicolumn{4}{c|}{\\textbf{Dimensions}}\\\\'''%ttype.upper()
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
    
def rLabelMean(a,b,t=9999,var=False):
    c = list(a); c.extend(b)
    c = array(c)
    na = len(a)
    nb = len(b)
    deltas = []
    for i in range(t):
        shuffle(c)
        if var:
            delta = abs(c[:na].var()**(0.5) - c[na:].var()**(0.5))
        else:
            delta = abs(c[:na].mean() - c[na:].mean())
        deltas.append(delta)
    if var:
        realMean = abs(a.var()**(0.5)-b.var()**(0.5))
    else:
        realMean = abs(a.mean()-b.mean())
    deltas.append(realMean)
    deltas.sort()
    i = deltas.index(realMean)
    p = (t+1 - i)/float(t+1)
    return realMean,p

def rLabelTables(topoData,tname,var=False,keys=[]):
    degs = topoData.keys()
    if keys:
        degs = keys
    else:
        degs.sort()
    format = '|'.join(['c' for d in degs])
    print '''
\\subtable[%s]{
  \\begin{table}
  \\label{rlt:%s}
  \\begin{tabular}{|c||%s|}'''%(tname.title(),tname,format)

    print '  \\hline'
    print "  " + "&".join(map(str,degs)) + '\\\\\\hline'
    print '  \\hline'
    #for a in degs:
    for i in xrange(len(degs)):
        a = degs[i]
        s = '  '
        s += str(a)
        #for b in degs:
        for j in xrange(len(degs)):
            b = degs[j]
            if i==j:
                pass
            elif i>j:
                s+="& "
            else:
                #s+='& %.4f (%.4f)'%rLabelMean(topoData[a],topoData[b],t=999)
                if var:
                    delta,p = rLabelMean(topoData[a],topoData[b],t=9999,var=True)
                else:
                    delta,p = rLabelMean(topoData[a],topoData[b],t=9999)
                if p <= 0.01:
                    s+= '& \\textbf{%.6f} ***'%delta
                elif p <= 0.05:
                    s+= '& \\textbf{%.6f} **'%delta
                elif p <= 0.10:
                    s+= '& \\textbf{%.6f} *'%delta
                else:
                    s+= '& %.6f'%delta
        print s+'\\\\\\hline'
    print "  \end{tabular}"
    print "}"
            
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
    tableValues['header2']= ' & '.join(['N & Mean (Var)' for topo in topos])

    rows = ""
    for deg in degs:
        row = str(deg)
        for topo in topos:
            try:
                n = len(data[topo][deg])
                m = data[topo][deg].mean()
                v = data[topo][deg].var()
                row += '& %d'%n
                row += '& %.4f (%.4f)'%(m,v)
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
        v = nodes.var()
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


##############################################################################
""" Switching to quetion 2 """
##############################################################################
def q1Data2q2Data(q1Data):
    d = {}
    d2 = {}
    for topo in q1Data:
        l = []
        l2 = []
        for deg in q1Data[topo]:
            l.extend(q1Data[topo][deg])
            l2.extend([deg for i in xrange(len(q1Data[topo][deg]))])
        d[topo] = N.array(l)
        d2[topo] = N.array(l2)
        
    return d,d2


def q2Joins(path='../data/ivFiles',dims=5,clusters=10):
    """ This function creates the main data structure for questions related to
        research question 2.
        node,size,degree,averageIV """
    files = os.listdir(path)
    print files.pop(0)
    d = {}
    for fname in files:
        finfo = IVName(fname)
        type,dim,c,number = finfo.tdcn()
        if dim == dims and c == clusters:
            if type not in d:
                d[type] = {'nid':[],'size':[],'deg':[],'iv':[]}
            f = open(os.path.join(path,fname),'r')
            data = f.readlines()
            f.close()
            data = [l.strip().split(',') for l in data]
            data = [(int(i[0]),int(i[1]),int(i[2]),float(i[3])) for i in data]
            for nid,size,deg,iv in data:
                d[type]['nid'].append(nid)
                d[type]['size'].append(size)
                d[type]['deg'].append(deg)
                d[type]['iv'].append(iv)
    for type,data in d.iteritems():
        #d[type]['nid'] = array(d[type]['nid'])
        #d[type]['size'] = array(d[type]['size'])
        #d[type]['deg'] = array(d[type]['deg'])
        d[type]['iv'] = array(d[type]['iv'])
    return d



if __name__=="__main__":
    #This function should always be run.
    # It does nothing unless the IV files have been removed,
    # or new test cases have been added.
    q1() 

    #####
    """ Create Mean Instanl Variance Table, 4.1 """
    #####
    #graph = q1BOX(ttype='graph')
    #rook = q1BOX(ttype='rook')
    #hex = q1BOX(ttype='hex')
    #geodesic = q1BOX(ttype='geodesic')
    #####
    #####

    #####
    """ Create Mean IV for each simulation table, 4.2 """
    #####
    data = q1TableSet2(dims=3,clusters=7)
    #####
    #####

    #####
    """ Create data structure for research question 1 functions """
    #####
    q1Data = q1Joins(dims=3,clusters=7)
    #####
    #####

    #####
    """ Create box plots for question 1, Figure 4.1 """
    #####
    createBoxPlots(q1Data)
    #####
    #####

    #####
    """ Create Mean and Var IV grouped by degree, Table 4.3 """
    #####
    createGroupBasedMeanIVTable(q1Data)
    #####
    #####

    #####
    """ Create differance table, 4.4 """
    #####
    rLabelTables(q1Data['rook'],'rook')
    rLabelTables(q1Data['hex'],'hex')
    rLabelTables(q1Data['graph'],'graph')
    rLabelTables(q1Data['geodesic'],'geodesic')
    #####
    #####

    ##############################################################################
    """ Switching to quetion 2 """
    ##############################################################################
    #q2Data,q2Degs = q1Data2q2Data(q1Data)
    #q2Data = q2Joins()
    #build graphs
    #geodesic = delaunay.parseDelaunay("geodesic/geodesic_642_delaunay.xyz")
    #sphere = delaunay.parseDelaunay("delaunay/642_delaunay.xyz")
    #g = grid2Rook(23,28,binary=1)
    #rook = NX.Graph()
    #for node in g:
    #    for neighbor in g[node][1]:
    #        rook.add_edge((node,neighbor))
    #hex = hexGraph(23,28)

    #topo = ['geodesic','rook','graph','hex']
    #names = {'geodesic':'Geodesic','rook':'Rook','graph':'Spherical','hex':'Hexagonal'}
    #graphs = {'geodesic':geodesic,'rook':rook,'graph':sphere,'hex':hex}

    #for t in topo:
    #    n = names[t]
    #    g = N.array(graphs[t].degree()).var()
    #    print "%s & %0.4f & %0.4f (%0.4f)"%(n,g,q2Data[t].mean(),q2Data[t].var())
        
    #print "Geodesic &",N.array(geodesic.degree()).var(),"&",q2Data['geodesic'].mean(),' (%f)\\'%q2Data['geodesic'].var()
    #print "Rook &",N.array(rook.degree()).var(),"&",q2Data['rook'].mean(),' (%f)\\'%q2Data['rook'].var()
    #print "Spherical &",N.array(sphere.degree()).var(),"&",q2Data['graph'].mean(),' (%f)\\'%q2Data['graph'].var()
    #print "Hexagonal &",N.array(hex.degree()).var(),"&",q2Data['hex'].mean(),' (%f)\\'%q2Data['hex'].var()

    #rLabelTables(q2Data,"all",var=True,keys=topo)
    #g = []
    #for t in topo:
    #    g.append(q2Data[t])
    #pylab.boxplot(g,notch=1)
    
        

    #cc = nx.centrality.closeness_centrality(hexG)
    #l = []
    #for nid in q2Data['hex']['nid']:
    #    l.append(cc[nid])
    #pylab.scatter(q2Data['hex']['deg'],q2Data['hex']['iv'])
    #pylab.scatter(l,q2Data['hex']['iv'])
    




