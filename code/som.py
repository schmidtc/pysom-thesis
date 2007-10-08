"""
Python Self-Organizing Maps with Spherical Lattice
----------------------------------------------------------------------
AUTHOR(S):      Charles R. Schmidt cschmidt@rohan.sdsu.edu
----------------------------------------------------------------------
Copyright (c) 2006-2007  Charles R. Schmidt
======================================================================
This source code is probably licensed under the GNU General Public License,
Version 2, you should check.
======================================================================
"""
import random,math,time,sys,os
from numpy import array,empty,take,put,zeros
import numpy as N
from math import acos,sqrt,pi,degrees,sin,cos,asin
import networkx as NX
import pylab
import pickle
from utils import *

class som:
    ''' Base class for the Self-Organizing Map,
        Each topology will inherit from this class.
        A template is provied in 'Topology'
    '''
    def __init__(self):
        self.Dims = 0
        self.Size = 0
        self.tSteps = 0
        self.maxN = 0
        self.alpha0 = 0
        self.nodes = []
        self.daMap = {}

    def load(self,path,name=None):
        if not name:
            name = '%ds_%dd_%dr_%fa'%(self.Size,self.Dims,self.tSteps,self.alpha0)
        codname = path+name+'.txt'
        mapname = path+name+'.map'
        if os.path.exists(mapname):
            try:
                f = open(mapname,'r')
                self.daMap = pickle.load(f)
                f.close()
            except:
                self.daMap = {}
        dataf = open(codname,'r')
        header = dataf.next()
        Dims,Size = header.split()
        self.Dims = int(Dims)
        self.Size = int(Size)
        self.nodes = array([[0.0 for i in xrange(self.Dims)] for j in xrange(self.Size)])
        for i in xrange(self.Size):
            data = dataf.next()
            data = data.split()
            data = map(float,data)
            self.nodes[i] = data

    def save(self,path=None,name=None):
        if not name:
            name = '%ds_%dd_%dr_%fa'%(self.Size,self.Dims,self.tSteps,self.alpha0)
        codname = path+name+'.txt'
        mapname = path+name+'.map'
        if self.daMap:
            mapfile = open(mapname,'w')
            pickle.dump(self.daMap,mapfile)
            mapfile.close()
        outf = open(codname,'w')
        outf.write("%d %d\n"%(self.Dims,self.Size))
        for i in xrange(self.Size):
            outf.write(' '.join(str(self.nodes[i].tolist())[1:-1].split(', '))+'\n')
        outf.close()

    def randInit(self):
        self.nodes = array([[random.random() for j in xrange(self.Dims)] for i in xrange(self.Size)])

    def findBMU(self,ind,v,ReturnDist = False):
        minDist = self.diff(0,ind,v)
        BMU = 0 
        for i in xrange(1,self.Size):
            d = self.diff(i,ind,v)
            if d < minDist:
                minDist = d
                BMU = i 
        if ReturnDist:
            return BMU,minDist
        else:
            return BMU

    def diff(self,nodeid,ind,v):
        node = take(self.nodes[nodeid],ind)
        return sum((node-v)**2)

    def alpha(self,t):
        r = self.alpha0 * (1 - (t/float(self.tSteps)))
        if r < 0: r = 0
        return r
    def hci(self, t, dist):
        sigma = self.kernalWidth(t)
        a = self.alpha(t)
        top = dist**2
        bottom = (2*(float(sigma)**2))
        return a * math.exp(-top/bottom)
    def kernalWidth(self,t):
        """Returns the number of neurons to include at time t
           this should probably return the current order instead,
           which means it should be moved to Topology."""
        r = round((self.Size*self.maxN) * (1 - (t/float(self.tSteps))))
        r = int(r)
        if r == 0: r = 1
        return r

    def merge(self,t,ind,v):
        bmu = self.findBMU(ind,v)
        sigma = self.kernalWidth(t)
        results = self.neighborhood( bmu , sigma )
        alteredNodes = [(results[i],self.hci(t,self.odist(i))) for i in xrange(len(results))]
        for nodeID,hc in alteredNodes:
            part = take(self.nodes[nodeID],ind)
            delta = part+hc*(v-part)
            put(self.nodes[nodeID],ind,delta)

    def run(self,obsf):
        self.neighborhoodCache = {}
        print "####################################"
        print "###        Configuration         ###"
        print "####################################"
        print "  N = %d, maxN = %f"%(self.Size,self.maxN)
        print "  Total runs: %d"%self.tSteps
        print "  initial learning rate = %f"%self.alpha0
        print "  Obs File:%s"%obsf.filename
        print "####################################"
        print "###          End Config          ###"
        print "####################################"
        print ""
        print "Running..."
        t1 = time.time()
        #s = ''
        T = self.tSteps
        for t in xrange(self.tSteps):
            id,ind,v = obsf.stream()
            self.merge(t,ind,v)
            ### 
            #if t%100 == 0:
            #    if len(s) > 60:
            #        print '\r'+s
            #        s = ''
            #    s += '%d...'%t
            #sys.stdout.write("\r%s%d"%(s,t))
            sys.stdout.write("\r%.2f%%"%(100*float(t)/T))
            sys.stdout.flush()
        print "\nRun compleated in %f seconds"%(time.time()-t1)

    def map(self,obsf):
        """ This function needs an overhall #5"""
        qerror = 0
        counter = 0 
        daMap = {} # keys are node ID's, values are lists of observation ID's.
        for id,dimIds,obs in obsf:
            bm,err = self.findBMU(dimIds,obs,ReturnDist=True)
            qerror += err
            if not bm in daMap:
                daMap[bm] = []
            daMap[bm].append(id)
            sys.stdout.write(".%d,%f.\r"%(counter,err))
            sys.stdout.flush()
            counter += 1
        print ""
        qerror = qerror/counter
        self.daMap = daMap
        return qerror

class Topology(som):
    """ Template class for topology Copy this class to create a new topology for som"""
    def __init__(self):
        som.__init__(self)
    def save(self,path,name):
        som.save(self,path,name)
    def load(self,path,name):
        som.load(self,path,name)
    def randInit(self):
        som.randInit(self)
    def kernalWidth(self,t):
        """
        You should overwrite this, see note above...
        kernalWidth returns the width of the neighborhood in terms of order
        """
        pass
    def odist(n):
        """
        n is the nth neuron in the in neighborhood, return's order
        example the 3rd neuron in the set is 1 order from the 0th.
        """
        pass
    def neighborhood(self,bmu,kernalWidth):
        """
        This function must return the ID's of the nodes inside the neighborhood, 
        NumNeighbors is defined by kernalWidth and is expressed as an order.
        bmu is the id of the best match, or neighborhood center.
        """
        pass
    
class GraphTopology(som):
    """ Template class for topology Copy this class to create a new topology for som"""
    def __init__(self,G):
        som.__init__(self)
        self.G = G
        self.Size = G.order()

        # if findWidth is not given a seed it will brute force the total network
        # width, this could take a long time. For the spherical network, one of
        # the polls should yeild the correct width. Or possible the node with
        # lowest degree.
        self.Width = nf.findWidth(G,G.nodes()[-1]) 
        self.maxN = 0.5

    def save(self,path,name):
        som.save(self,path,name)
    def load(self,path,name):
        som.load(self,path,name)
    def randInit(self):
        som.randInit(self)
    def kernalWidth(self,t):
        """
        kernalWidth returns the width of the neighborhood in terms of order
        """
        r = round((self.Width*self.maxN) * (1 - (t/float(self.tSteps))))
        r = int(r)
        if r == 0: r = 1
        return r
    def odist(n):
        """
        n is the nth neuron in the in neighborhood, return's order
        example the 3rd neuron in the set is 1 order from the 0th.
        """
        raise "not implemented"
    def neighborhood(self,bmu,kernalWidth):
        """
        This function returns a dictionary containing the neighbors of bmu as
        keys and their dist (as an order) as values.
        """
        return nf.neighborhood(self.G,bmu,kernalWidth)
    def merge(self,t,ind,v):
        """
        imporved neighborhood function eliminates the need for odist function.
        """
        bmu = self.findBMU(ind,v)
        sigma = self.kernalWidth(t)
        results = self.neighborhood( bmu , sigma )
        alteredNodes = [(node,self.hci(t,odist)) for node,odist in results.iteritems()]
        #alteredNodes = [(results[i],self.hci(t,self.odist(i))) for i in xrange(len(results))]
        for nodeID,hc in alteredNodes:
            part = take(self.nodes[nodeID],ind)
            delta = part+hc*(v-part)
            put(self.nodes[nodeID],ind,delta)

class Sphere(som):
    def __init__(self):
        som.__init__(self)
        # The Cache cache only works if the Neighborhood size is decreasing!
        # If you increase the maxN clear the cache!
        self.neighborhoodCache = {}
        self.maxN = 0.5
    def clearCache(self):
        self.neighborhoodCache = {}
    def randInit(self):
        som.randInit(self)
        N = self.Size
        points = []
        for i in xrange(1,N+1):
            i = float(i)
            N = float(N)
            h = (-1)+((2*(i-1)) / (N-1))
            theta = acos(h)
            if i == 1 or i == N:
                phi = 0
            else:
                phi = (points[int(i)-2][0] + (3.6/sqrt(N)) * (1/sqrt(1-h**2)) ) % (2*pi)
            points.append((phi,theta))
        points = array([(phi-pi,theta-(pi/2)) for phi,theta in points])
        self.grid = points

        size = self.Size * self.maxN
        maxW = 0
        W = 0
        while size >= (1+(3*maxW)*(maxW-1)):
            maxW += 1
        self.maxW = maxW

    def odist(self,n):
        d = 1
        while n >= (1+(3*d)*(d-1)):
            d+=1
        return d-1
    def save(self,path,name):
        som.save(self,path,name)
        geof = open(path+name+'_geo.txt','w')
        geof.write("%d %d\n"%(self.Dims,self.Size))
        for i in xrange(self.Size):
            geof.write("%f %f\n"%(degrees(self.grid[i][0]),degrees(self.grid[i][1])))
        geof.close()
    def load(self,path,name):
        som.load(self,path,name)
        if os.path.exists(path+name+'_geo.txt'):
            geof = open(path+name+'_geo.txt','r')
            header = geof.next()
            self.grid = zeros((self.Size,2),'float')
            for i in xrange(self.Size):
                geo = geof.next()
                geo = geo.split()
                geo = (math.radians(float(geo[0])),math.radians(float(geo[1])))
                self.grid[i] = geo
        else:
            pass
    def sdist(self,pt1,pt2):
        phi1,theta1 = pt1
        phi2,theta2 = pt2
        dphi = phi2 - phi1
        dtheta = theta2 - theta1
        a = sin(dtheta/2)**2 + (cos(theta1) * cos(theta2) * sin(dphi/2)**2)
        c = 2 * asin(min(1,sqrt(a)))
        return c
    def kernalWidth(self,t):
        r = round((self.maxW) * (1 - (t/float(self.tSteps))))
        r = int(r)
        if r == 0: r = 1
        return r
    def neighborhood(self,bmu,sigma):
        NumNeighbors = (1+(3*sigma)*(sigma-1))
        try:
            return self.neighborhoodCache[bmu][:NumNeighbors]
        except:
            pt0 = self.grid[bmu]
            dists = {}
            for i in xrange(self.Size):
                dists[self.sdist(self.grid[i],pt0)] = i
            keys = dists.keys()
            keys.sort() 
            pts = [dists[keys[i]] for i in xrange(NumNeighbors)]
            self.neighborhoodCache[bmu] = pts
            return pts

class SphereTopoTest(Sphere):
    def __init__(self):
        Sphere.__init__(self)
    def randInit(self):
        Sphere.randInit(self)
        self.nodes = zeros((int(self.Size),1))
    def neighborhood(self,bmu,sigma):
        NumNeighbors = sigma
        pt0 = self.grid[bmu]
        dists = {}
        for i in xrange(self.Size):
            dists[self.sdist(self.grid[i],pt0)] = i
        keys = dists.keys()
        keys.sort() 
        pts = [dists[keys[i]] for i in xrange(NumNeighbors)]
        return pts
    def hci(self,dist):
        if dist == 0:
            return 1.0
        else:
            return 0.5
    def merge(self,nodeID):
        results = self.neighborhood( nodeID , 7 ) # 1 for me plus 6 neighbors
        alteredNodes = [(results[i],self.hci(i)) for i in xrange(len(results))]
        for nodeID,hc in alteredNodes:
            part = self.nodes[nodeID][0]
            delta = part+hc*(2)  # 2 is the value we through at the grid
            put(self.nodes[nodeID],0,delta)
    def run(self):
        print "Running..."
        t1 = time.time()
        for nodeID in xrange(self.Size):
            self.merge(nodeID)
        print "\nRun compleated in %f seconds"%(time.time()-t1)


class ObsFile:
    def __init__(self,filename,fileType = 'complete'):
        self.filename = filename
        self.fileObj = open(filename,'r')
        self.fileType = fileType
        self.reset()
    def __iter__(self):
        return self
    def listolists(self):
        self.fileObj.seek(0)
        lines = self.fileObj.readlines()
        dims = lines.pop(0)
        dims = int(dims)
        lines = [line.split() for line in lines]
        lines = [line[:dims] for line in lines]
        lines = [array(map(float,line),'float') for line in lines]
        return lines
    def Snext(self):
        line = self.fileObj.next()
        id,line = line.split(':')
        line = line.split(',')
        Num = len(line)/2
        indices = empty(Num,'int16')
        values = empty(Num,'float')
        c = 0
        for n in xrange(0,Num*2,2):
            indices[c] = int(line[n])-1
            values[c] = float(line[n+1])
            c += 1
        return id,indices,values
    def Cnext(self):
        line = self.fileObj.next()
        line = line.split()
        id = self.nextLine-1
        for n in xrange(0,self.Dims):
            self.values[n] = float(line[n])
        self.nextLine+=1
        return id,self.indices,self.values
    def reset(self):
        self.fileObj.seek(0)
        self.nextLine = 0 #Zero Base
        if self.fileType == 'complete':
            self.next = self.Cnext
            self.Dims = int(self.fileObj.next())
            self.indices = array(range(self.Dims),'int16') 
            self.values = empty(self.Dims,'float') 
            self.nextLine += 1
        elif self.fileType == 'sparse':
            self.next = self.Snext
        else:
            raise "fileTypeError"
    def stream(self):
        try:
            return self.next()
        except:
            self.reset()
            return self.next()
    def close(self):
        self.fileObj.close()


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
        print "no map"
        #qerror = s.map(f)
    else: 
        qerror = None
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

### The Training
def graphTest():
    G = delaunay.parseDelaunay("delaunay/642_delaunay.xyz")
    s = GraphTopology(G)
    s.Dims = 15
    s.maxN = 0.5
    s.tSteps = 100000
    s.alpha0 = 0.04
    f = ObsFile('testData/15d-40c-no0_scaled.dat','complete')
    print "init"
    s.randInit()
    print "run t=100K"
    s.run(f)
    s.save('testResults/','graph_100k')
    s.maxN = 0.333
    s.tSteps = 1000000
    s.alpha0 = 0.03
    f.reset()
    print "run t=1M"
    s.run(f)
    s.save('testResults/','graph_1m')

    f.reset()
    s.map(f)
    s.save('testResults/','graph_1m')

    f.close()
    return s
def rookGraphTest():
    g = grid2Rook(23,28,binary=1)
    G = NX.Graph()
    for node in g:
        for neighbor in g[node][1]:
            G.add_edge((node,neighbor))
    s = GraphTopology(G)
    s.Dims = 15
    s.maxN = 0.5
    s.tSteps = 100000
    s.alpha0 = 0.04
    f = ObsFile('testData/15d-40c-no0_scaled.dat','complete')
    print "init"
    s.randInit()
    print "run t=100K"
    s.run(f)
    s.save('testResults/','rook_100k')

    s.maxN = 0.333
    s.tSteps = 1000000
    s.alpha0 = 0.03
    f.reset()
    print "run t=1M"
    s.run(f)
    s.save('testResults/','rook_1m')

    f.reset()
    s.map(f)
    s.save('testResults/','rook_1m')

    f.close()
    return s
### End Training

if __name__=="__main__":
    ### Step one, train the soms
    #g = graphTest()
    #r = rookGraphTest()
    #s = sphereTest() # This is probably no good anymore (or ever)

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
