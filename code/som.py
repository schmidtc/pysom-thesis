import random,math,time,sys
from Numeric import *
from math import acos,sqrt,pi,degrees,sin,cos,asin

class som:
	def __init__(self):
		self.Dims = 0
		self.Size = 0
		self.tSteps = 0
		self.maxN = 0
		self.alpha0 = 0
		self.grid = []
		self.nodes = []
		# The Cache cache only works if the Neighborhood size is decreasing!
		# If you increase the maxN clear the cache!
		self.neighborhoodCache = {}
	def load(self,path,name):
		dataf = open(path+name+'.txt','r')
		try:
			geof = open(path+name+'_geo.txt','r')
			geof.next()
		except:
			geof = False
		header = dataf.next()
		Dims,Size = header.split()
		self.Dims = int(Dims)
		self.Size = int(Size)
		self.nodes = array([[0.0 for i in xrange(self.Dims)] for j in xrange(self.Size)])
		self.grid = array([[0.0 for i in xrange(2)] for j in xrange(self.Size)])

		for i in xrange(self.Size):
			if geof:
				geo = geof.next()
				geo = geo.split()
				geo = (math.radians(float(geo[0])),math.radians(float(geo[1])))
				self.grid[i] = geo
			
			data = dataf.next()
			data = data.split()
			data = map(float,data)
			self.nodes[i] = data

	def save(self,path,name):
		outf = open(path+name+'.txt','w')
		geof = open(path+name+'_geo.txt','w')
		outf.write("%d %d\n"%(self.Dims,self.Size))
		geof.write("%d %d\n"%(self.Dims,self.Size))
		for i in xrange(self.Size):
			outf.write(' '.join(str(self.nodes[i].tolist())[1:-1].split(', '))+'\n')
			geof.write("%f %f\n"%(degrees(self.grid[i][0]),degrees(self.grid[i][1])))
		outf.close()
		geof.close()
	def randInit(self):
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
	        self.nodes = array([[random.random() for j in xrange(self.Dims)] for i in xrange(self.Size)])

	def sdist(self,pt1,pt2):
		phi1,theta1 = pt1
		phi2,theta2 = pt2
		dphi = phi2 - phi1
		dtheta = theta2 - theta1
		a = sin(dtheta/2)**2 + (cos(theta1) * cos(theta2) * sin(dphi/2)**2)
		c = 2 * asin(min(1,sqrt(a)))
		return c
	def neighborhood(self,bmu,NumNeighbors):
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
#	def MatchAll(self,obs,ReturnDist = False):
#		bmList = [(0,0) for i in xrange(self.Size)]
#		for i in xrange(self.Size):
#			d = self.diff(self.nodes[i],obs)
#			bmList[i] = (d,i)
#		bmList.sort()
#		return bmList

	def diff(self,nodeid,ind,v):
		node = take(self.nodes[nodeid],ind)	
		return sum((node-v)**2)
#	def diff(self,node,dictObs):
#	        diff = 0
#	        for key in dictObs:
#	                diff += (node[key]-dictObs[key])**2
#	        #return math.sqrt(diff)
#	        return diff

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
		r = round((self.Size*self.maxN) * (1 - (t/float(self.tSteps))))
		r = int(r)
		if r == 0: r = 1
		return r

	def merge(self,t,ind,v):
#		t1 = time.time()
		bmu = self.findBMU(ind,v)
#		print "\tFound BMU: %d in %f seconds"%(bmu,time.time()-t1)
#		t2 = time.time()
		sigma = self.kernalWidth(t)
		results = self.neighborhood( bmu , sigma )
#		print "\tFound neighborhood in %f seconds"%(time.time()-t2)
#		t2 = time.time()
		## Nodes = (nodeID, hci)
		alteredNodes = [(results[i],self.hci(t,i)) for i in xrange(len(results))]
		for nodeID,hc in alteredNodes:
			part = take(self.nodes[nodeID],ind)
			delta = part+hc*(v-part)
			put(self.nodes[nodeID],ind,delta)
#		print "\tUpdated %d neighbors in %f seconds"%(sigma,time.time()-t2)
#		print "\tt in %f seconds"%(time.time()-t1)

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

#	def bmap(self,obsf,outFileName):
#		o = file(outFileName,'w')
#		o.write("ID,BMU\n")
#		for id,obs in obsf:
#			try:
#				bm = self.findBMU(obs)
#			except:
#				print id
#			o.write("%s,%d\n"%(id,bm))
#		o.close()


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
class ObsFile:
	def __init__(self,filename,fileType = 'complete'):
		self.filename = filename
		self.fileObj = file(filename,'r')
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
		obs = dict([(n,float(line[n])) for n in xrange(self.Dims)])
		self.nextLine+=1
		return obs
	def reset(self):
		self.fileObj.seek(0)
		self.nextLine = 0 #Zero Base
		if self.fileType == 'complete':
			self.next = self.Cnext
			self.Dims = int(self.fileObj.next())
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
        sys.stdout = open('numeric_log.txt','w',0)
        s = som()
        s.Size = 1000
        s.Dims = 17770
        s.maxN = 0.5 
        s.tSteps = 1000000
        s.alpha0=0.5
        f = ObsFile('/Volumes/Mac_HD_2/charlie/som_data/bigGuys.dat','sparse')
        print "init"
        s.randInit()
        print "save"
        s.save('../cod_files/','bigGuys_1k_cod')
        print "run t=1M"
        s.run(f)
        print "save"
        s.save('../cod_files/','bigGuys_1k_cod')

        f.close()
