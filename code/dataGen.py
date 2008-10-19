import numpy as N
import sys
import pylab
import random
from scaler import scaler

def geo2006(fname='3d-7c-no%d', testNum=0, rand=True):
    """This function generates the same training data that Wu and Tkatsuka used in Geodesic 2006 paper, there are 3 dims, 7 clusters.

        "Fig. 9. The 3D synthetic data set. We generated a three-dimensional data set which contains seven clusters, as shown in Fig. 9. Each cluster has 500 normally distributed data points. The standard deviation is 1 in each dimension. The centers of the clusters are: (0, 0, 0), (10, 0, 0), (0, 10, 0), (0, 0, 10), (-10, 0, 0), (0, -10, 0), (0, 0, -10)" - Wu and Tkatsuka 2006.
    """

    rsName = fname%testNum+'_rs.dat'
    fname = fname%testNum+'.dat'

    cores = [(0, 0, 0), (10, 0, 0), (0, 10, 0), (0, 0, 10), (-10, 0, 0), (0, -10, 0), (0, 0, -10)]
    clusters = []
    obsPerCore = 3571 # *7 = 24,997
    if rand: obsPerCore = 3125 # *8 = 25,000
    for i,j,k in cores:
        x = N.random.normal(i,1,obsPerCore)
        y = N.random.normal(j,1,obsPerCore)
        z = N.random.normal(k,1,obsPerCore)
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
