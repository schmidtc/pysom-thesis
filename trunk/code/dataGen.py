import numpy as N
import sys
import pylab
import random
from scaler import scaler


#def gaussian(nDims=10,nClusters=10,minClusterSize=100,maxClusterSize=1000):
#    size = [random.randint(minClusterSize,maxClusterSize) for i in xrange(nClusters)]
#    #Generate mean values
#    mean = [[random.random() for j in xrange(nDims)] for i in xrange(nClusters)]
#    for i in xrange(nClusters):
#        for j in xrange(nDims):
#            #mean[j] = -MAXMU + random.random() * (MAXMU-MINMU);
#            mean[j] = random.random()
        
    
def gen(n,clusters,dims,noise):
    """ 
    eg.
    n = 10000 #Sample size
    clusters = 5 #The number of clusters
    dims = 20 #the number of dimmensions
    noise = 0.05 #5% random noise

    returns a dictionary of lists
    """

    #generate seeds...
    #seedr = [0.1 for i in xrange(clusters)]
    def reject():
        seeds = N.array([[random.random() for i in xrange(dims)] for j in xrange(clusters)])
        seedr = [random.uniform(0,0.2) for i in xrange(clusters)]
        for i in xrange(clusters):
            for j in xrange(i+1,clusters):
                d = N.sqrt(sum((seeds[i]-seeds[j])**2))
                print d
                if d < (seedr[i] + seedr[j]):
                    return False
        return seeds,seedr
    while 1:
        r = reject()
        if r:
            seeds,seedr = r
            break


    data = []
    c = 0
    while c < n:
        pt = N.array([random.random() for i in xrange(dims)])
        d = N.sqrt(((seeds-pt)**2).sum(1))
        center = d.argmin()
        if d.min() < seedr[center]:
            pt = list(pt)
            pt.append(center)
            data.append(pt)
            c += 1
        else:
            if random.random() < noise:
                pt = list(pt)
                pt.append(-1)
                data.append(pt)
                c += 1
        sys.stdout.write("\r%d"%c)
        sys.stdout.flush()
        
    return seeds,data

def geo2006(fname='3d-7c-no%d', testNum=0, rand=True):
    """This function generates the same training data that Wu and Tkatsuka used in Geodesic 2006 paper, there are 3 dims, 7 clusters.

        "Fig. 9. The 3D synthetic data set. We generated a three-dimensional data set which contains seven clusters, as shown in Fig. 9. Each cluster has 500 normally distributed data points. The standard deviation is 1 in each dimension. The centers of the clusters are: (0, 0, 0), (10, 0, 0), (0, 10, 0), (0, 0, 10), (-10, 0, 0), (0, -10, 0), (0, 0, -10)" - Wu.
    """

    rsName = fname%testNum+'_rs.dat'
    fname = fname%testNum+'.dat'

    cores = [(0, 0, 0), (10, 0, 0), (0, 10, 0), (0, 0, 10), (-10, 0, 0), (0, -10, 0), (0, 0, -10)]
    clusters = []
    for i,j,k in cores:
        x = N.random.normal(i,1,3571)
        y = N.random.normal(j,1,3571)
        z = N.random.normal(k,1,3571)
        cluster = zip(x,y,z)
        clusters.append(cluster)
    
    if rand:
        rCluster = []
        cores = N.array(cores)
        while len(rCluster) < 3125:
            xyz = N.random.uniform(-13,13,3)
            dists = N.sqrt(((cores-xyz)**2).sum(1))
            if min(dists) > 1.0:
                rCluster.append(xyz)
            #y = N.random.uniform(-10,10,3125)
            #z = N.random.uniform(-10,10,3125)

        clusters.append(rCluster)
    

    lines = []
    for n,cluster in enumerate(clusters):
        for pt in cluster:
            x,y,z = pt
            lines.append("%f %f %f %d\n"%(x,y,z,n))
    f = open(fname,'w')
    f.write('3\n')

    random.shuffle(lines)
    f.writelines(lines)
    f.close()

    scaler(fname,rsName)


        
if __name__=="__main__":
    for i in range(10):
        geo2006(testNum=i, rand=False)
    #s = gen(10000,7,2,0.00)
    #x = [pt[0] for pt in s[1]]
    #y = [pt[1] for pt in s[1]]

    #pylab.hist(x,10000)
    #pylab.scatter(x,y)
    #pylab.xticks(pylab.arange(0,1.01,0.2))
    #pylab.yticks(pylab.arange(0,1.01,0.2))
    #pylab.show()
