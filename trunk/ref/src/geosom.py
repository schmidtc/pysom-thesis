import random,math,time,sys
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

		for i in xrange(self.Size):
			if geof:
				geo = geof.next()
				geo = geo.split(',')
				geo = (math.radians(float(geo[1])),math.radians(float(geo[2])))
				self.grid.append(geo)
			
			data = dataf.next()
			data = data.split()
			data = map(float,data)
			self.nodes.append(data)

	def savegeo(self,path,name):
		geof = open(path+name+'_geo.txt','w')
		geof.write("id,lng,lat\n")
		for i in xrange(self.Size):
			geof.write("%d,%f,%f\n"%(i+1,degrees(self.grid[i][0]),degrees(self.grid[i][1])))
		geof.close()
	def initgeo(self):
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
		points = [(phi-pi,theta-(pi/2)) for phi,theta in points]
		points[0] = (0,points[0][1])
		points[-1] = (0,points[-1][1])
		self.grid = points

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

	def findBMU(self,obs,ReturnDist = False):
	        minDist = self.diff(self.nodes[0],obs)
	        BMU = 0 
	        for i in xrange(1,self.Size):
	                d = self.diff(self.nodes[i],obs)
	                if d < minDist:
	                        minDist = d
	                        BMU = i 
		if ReturnDist:
			return BMU,minDist
		else:
	        	return BMU

	def diff(self,node,dictObs):
	        diff = 0
	        for key in dictObs:
	                diff += (node[key]-dictObs[key])**2
	        #return math.sqrt(diff)
	        return diff

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

	def merge(self,t,obs):
#		t1 = time.time()
		bmu = self.findBMU(obs)
#		print "\tFound BMU: %d in %f seconds"%(bmu,time.time()-t1)
#		t2 = time.time()
		sigma = self.kernalWidth(t)
		results = self.neighborhood( bmu , sigma )
#		print "\tFound neighborhood in %f seconds"%(time.time()-t2)
#		t2 = time.time()
		## Nodes = (nodeID, hci)
		alteredNodes = [(results[i],self.hci(t,i)) for i in xrange(len(results))]
		for node in alteredNodes:
			for n in obs:
				self.nodes[node[0]][n] = self.nodes[node[0]][n] + node[1]*(obs[n]-self.nodes[node[0]][n])
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
			sys.stdout.write('\r\t%d'%t)
			sys.stdout.flush()
			id,obs = obsf.stream()
			self.merge(t,obs)
		print "\nRun compleated in %f seconds"%(time.time()-t1)

	def bmap(self,obsf,outFileName):
		o = file(outFileName,'w')
		o.write("ID,BMU\n")
		for id,obs in obsf:
			try:
				bm = self.findBMU(obs)
				o.write("%s,%d\n"%(id,bm))
			except:
				print id
		o.close()


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
		obs = dict([(int(line[n])-1,float(line[n+1])) for n in xrange(0,len(line),2)])
		return id,obs
	def Cnext(self):
		line = self.fileObj.next()
		line = line.split()
		obs = dict([(n,float(line[n])) for n in xrange(self.Dims)])
		self.nextLine+=1
		return self.nextLine,obs
	def reset(self):
		self.fileObj.seek(0)
		self.nextLine = 0 #Zero Base
		if self.fileType == 'complete':
			self.next = self.Cnext
			self.Dims = int(self.fileObj.next())
			#self.nextLine += 1
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

