import random,math,time,sys,os
from Numeric import *
from math import acos,sqrt,pi,degrees,sin,cos,asin

class som:
	def __init__(self):
		self.Dims = 0
		self.Size = 0
		self.tSteps = 0
		self.maxN = 0
		self.alpha0 = 0
		self.nodes = []

	def load(self,path,name):
		dataf = open(path+name+'.txt','r')
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

	def save(self,path,name):
		outf = open(path+name+'.txt','w')
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
		for t in xrange(self.tSteps):
			id,ind,v = obsf.stream()
			self.merge(t,ind,v)
		print "\nRun compleated in %f seconds"%(time.time()-t1)

	def map(self,obsf,outFileName):
		outf = file(outFileName,'w')
		pts = []
		qerror = 0
		counter = 0 
		for id,obs in obsf:
			bm,err = self.findBMU(obs,ReturnDist=True)
			qerror += err
			pt = self.grid[bm]
			outf.write("%d %f %f %f\n"%(bm,degrees(pt[0]),degrees(pt[1]),err))
			sys.stdout.write(".%d,%f.\r"%(counter,err))
			sys.stdout.flush()
			counter += 1
		qerror = qerror/counter
		outf.close()
		return qerror



class Topology(som):
	"""Template class for topology"""
	def __init__(self):
		som.__init__(self)
	def save(self,path,name):
		som.save(self,path,name)
	def load(self,path,name):
		som.load(self,path,name)
	def randInit(self):
		som.randInit(self)
	def kernalWidth(self,t):
		""" You should overwrite this, see note above...
		   kernalWidth returns the width of the neighborhood in terms of order"""
		pass
	def odist(n):
		"""n is the nth neuron in the in neighborhood, return's order
		   example the 3rd neuron in the set is 1 order from the 0th."""
		pass
	def neighborhood(self,bmu,kernalWidth):
		"""
		This function must return the ID's of the nodes inside the neighborhood, 
		NumNeighbors is defined by kernalWidth and is express in number of neurons.
		bmu is the id of the best match
		"""
		pass
	
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
			self.grid = zeros((self.Size,2),typecode='f')
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
	def Snext(self):
		line = self.fileObj.next()
		id,line = line.split(':')
		line = line.split(',')
		Num = len(line)/2
		indices = empty(Num,typecode='s')
		values = empty(Num,typecode='f')
		c = 0
		for n in xrange(0,Num*2,2):
			indices[c] = int(line[n])-1
			values[c] = float(line[n+1])
			c += 1
		return id,indices,values
	def Cnext(self):
		line = self.fileObj.next()
		line = line.split()
		id = self.nextLine
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
			self.indices = array(range(self.Dims),typecode='s') #typecode 's' is Int16
			self.values = empty(self.Dims,typecode='f') #typecode 'f' is Float32
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

if __name__=="__main__":
	import sys,time
        s = Sphere()
        s.Size = 1000
        s.Dims = 10
        s.maxN = 0.5 
        s.tSteps = 10000
        s.alpha0 = 0.5
        f = ObsFile('testData/10d-10c-no0_scaled.dat','complete')
        print "init"
        s.randInit()
        print "save"
        s.save('testResults/','test-10d-10c-no0_rand')
        print "run t=10K"
        s.run(f)
        print "save"
        s.save('testResults/','test-10d-10c-no0_10K')

        f.close()
