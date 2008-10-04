"""
Python Self-Organizing Maps 
----------------------------------------------------------------------
AUTHOR(S):      Charles R. Schmidt cschmidt@rohan.sdsu.edu
----------------------------------------------------------------------
Copyright (c) 2006-2008  Charles R. Schmidt
======================================================================
This source code is probably licensed under the GNU General Public License,
Version 2, you should check.
======================================================================
"""
# Standard Libraries
import random,math,time,sys,os
from math import acos,sqrt,pi,degrees,sin,cos,asin
import pickle

# External Libraries
# http://numpy.scipy.org/
from numpy import array,empty,take,put,zeros
import numpy as N
# https://networkx.lanl.gov/
import networkx as NX

# Local Libraries (part of pySom)
from utils import *
from data import ObsFile

class som:
    ''' Base class for the Self-Organizing Map,
        Each topology will inherit from this class.
        A template is provied in 'Topology'
    '''
    def __init__(self):
        ''' These initial training parameters should be set before training. '''
        self.Dims = 0 # int, the number of dimmension in the input-space
        self.X = 0 # int, optionally the number nurons in the X dimmension
        self.Y = 0 # int, optionally the number nurons in the Y dimmension
        self.Size = 0 # int, total number of neurons
        self.Type = 'none' # str, name of topology type
        self.tSteps = 0 # int, total number of training steps.
        self.maxN = 0.0 # float, initial neighborhood radius, expressed as percentage.
        self.alpha0 = 0.0 # float, initial learning rate

        self.nodes = [] # reference vecotors are stored here.
        self.daMap = {} # mapping of observations to neurons is stored here.

    def load(self,path='',name=None):
        ''' This function loads a saved SOM from disk into memory.
            pySom uses several files to represent the SOM,
            .cod is the Codebook file which represents the reference vectors
            .map represents the mapping of the observations onto the trained SOM
            
            If the path and name are omitted they will be guessed 
            based on the SOM's parameters
        '''
        if not name:
            name = '%ds_%dd_%dr_%fa'%(self.Size,self.Dims,self.tSteps,self.alpha0)
        codname = path+name+'.cod'
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
        Dims,Type,x,y,nType= header.split()
        self.Dims = int(Dims)
        self.Type = Type
        self.X, self.Y = int(x),int(y)
        self.Size = self.X*self.Y
        self.nodes = array([[0.0 for i in xrange(self.Dims)] for j in xrange(self.Size)])
        for i in xrange(self.Size):
            data = dataf.next()
            data = data.split()
            data = map(float,data)
            self.nodes[i] = data

    def save(self,path='',name=None):
        ''' This function saves a SOM to disk.
            pySom uses several files to represent the SOM,
            .cod is the Codebook file which represents the reference vectors
            .map represents the mapping of the observations onto the trained SOM
            
            If the path and name are omitted they will be guessed 
            based on the SOM's parameters
        '''
        if self.X == 0 or self.Y == 0:
            self.X = self.Size
            self.Y = 1
        if not name:
            name = '%ds_%dd_%dr_%fa'%(self.Size,self.Dims,self.tSteps,self.alpha0)
        codname = path+name+'.cod'
        mapname = path+name+'.map'
        if self.daMap:
            mapfile = open(mapname,'w')
            pickle.dump(self.daMap,mapfile)
            mapfile.close()
        outf = open(codname,'w')
        outf.write("%d %s %d %d gaussian\n"%(self.Dims,self.Type,self.X,self.Y))
        for i in xrange(self.Size):
            outf.write(' '.join(str(self.nodes[i].tolist())[1:-1].split(', '))+'\n')
        outf.close()

    def randInit(self):
        ''' This function initializes the reference vectors with values 0 to 1.
            If you are not standardizing your data this function should be overwritten
    
            * Ideally this function would analyze the input data and scale the
              randomization accordingly.  SOM_PAK does something along these lines,
              their code might help find a good solution for this.
        '''
        self.nodes = array([[random.random() for j in xrange(self.Dims)] for i in xrange(self.Size)])

    def findBMU(self,ind,v,ReturnDist = False):
        ''' This function returns the ID of the reference vector that is the closest
            (in Euclidean distance) to input vector v
            
            Optionally this function will also return that distance between the two.
            Overwrite this function if you need something other than Euclidean dist.

            the 'ind' parameter is unused and should be set to None.

            * As written this function does not handle missing values, a previous version
              did, but it was painfully slow. One option would be to remove the distance
              function and pick the appropriate dist function depending on the values present.
        '''
        d = ((self.nodes-v)**2).sum(1)
        minI = d.argmin()
        if ReturnDist:
            minD = d[minI]
            return minI,minD
        else:
            return minI

    def alpha(self,t):
        '''  Returns the learning rate (alpha) as a function of time t.
        '''
        r = self.alpha0 * (1 - (t/float(self.tSteps)))
        if r < 0: r = 0
        return r
    def hci(self, t, dist):
        ''' This kernal function adjust the magnitude with which the observation affects 
            the reference vectors.
        '''
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
            if len(ind) == self.Dims:
                part = self.nodes[nodeID]
                delta = hc*(v-part)
                self.nodes[nodeID] = part+delta
            else:
                part = take(self.nodes[nodeID],ind)
                delta = hc*(v-part)
                put(self.nodes[nodeID],ind,part+delta)

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

#class Topology(som):
#    """ Template class for topology Copy this class to create a new topology for som"""
#    def __init__(self):
#        som.__init__(self)
#    def save(self,path,name):
#        som.save(self,path,name)
#    def load(self,path,name):
#        som.load(self,path,name)
#    def randInit(self):
#        som.randInit(self)
#    def kernalWidth(self,t):
#        """
#        You should overwrite this, see note above...
#        kernalWidth returns the width of the neighborhood in terms of order
#        """
#        pass
#    def odist(n):
#        """
#        n is the nth neuron in the in neighborhood, return's order
#        example the 3rd neuron in the set is 1 order from the 0th.
#        """
#        pass
#    def neighborhood(self,bmu,kernalWidth):
#        """
#        This function must return the ID's of the nodes inside the neighborhood, 
#        NumNeighbors is defined by kernalWidth and is expressed as an order.
#        bmu is the id of the best match, or neighborhood center.
#        """
#        pass
    
class GraphTopology(som):
    """ Template class for topology Copy this class to create a new topology for som"""
    def __init__(self,G=None,Type='Graph'):
        som.__init__(self)
        self.Type = Type
        if G:
            self.G = G
            self.Size = G.order()
            # if findWidth is not given a seed it will brute force the total network
            # width, this could take a long time. For the spherical network, one of
            # the polls should yield the correct width. Or possibly the node with
            # lowest degree.
            self.Width = nf.findWidth(G,G.nodes()[-1]) 

    def save(self,path,name):
        som.save(self,path,name)
        if not name:
            name = '%ds_%dd_%dr_%fa'%(self.Size,self.Dims,self.tSteps,self.alpha0)
        graphFile = path+name+'.graph'
        f = open(graphFile,'w')
        pickle.dump(self.G,f)
        f.close()
    def load(self,path,name):
        som.load(self,path,name)
        if not name:
            name = '%ds_%dd_%dr_%fa'%(self.Size,self.Dims,self.tSteps,self.alpha0)
        graphFile = path+name+'.graph'
        if os.path.exists(graphFile):
            f = open(graphFile,'r')
            self.G = G = pickle.load(f)
            self.Size = G.order()
            self.Width = nf.findWidth(G,G.nodes()[-1]) 
            f.close()

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

    def hci2(self, sigma, a, dist):
        top = dist**2
        bottom = (2*(sigma**2))
        return a * math.exp(-top/bottom)
    def merge(self,t,ind,v):
        """
        imporved neighborhood function eliminates the need for odist function.
        """
        bmu = self.findBMU(ind,v)
        a = self.alpha(t)
        sigma = self.kernalWidth(t)
        results = self.neighborhood( bmu , sigma )
        sigma = float(sigma)
        alteredNodes = [(node,(v-self.nodes[node])*(a*math.exp(-(odist*odist)/(2*sigma*sigma)))) for node,odist in results.iteritems()]
        #alteredNodes = [(node,(v-self.nodes[node])*self.hci2(sigma,a,odist)) for node,odist in results.iteritems()]
        for nodeID,node in alteredNodes:
            self.nodes[nodeID] += node

class Sphere(som):
    def __init__(self):
        som.__init__(self)
        # The Cache only works if the Neighborhood size is decreasing!
        # If you increase the maxN clear the cache!
        self.neighborhoodCache = {}
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
