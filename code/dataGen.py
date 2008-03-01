import numpy as N
import sys
import pylab
import random


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

        
if __name__=="__main__":
    s = gen(10000,7,2,0.00)
    x = [pt[0] for pt in s[1]]
    y = [pt[1] for pt in s[1]]

    #pylab.hist(x,10000)
    pylab.scatter(x,y)
    pylab.xticks(pylab.arange(0,1.01,0.2))
    pylab.yticks(pylab.arange(0,1.01,0.2))
    pylab.show()
