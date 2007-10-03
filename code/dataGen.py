import numpy as N
import sys
import pylab
import random
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
    seeds = N.array([[random.random() for i in xrange(dims)] for j in xrange(clusters)])
    seedr = [random.uniform(0,0.2) for i in xrange(clusters)]
    seedr = [0.1 for i in xrange(clusters)]
    data = []
    c = 0
    while c < n:
        pt = N.array([random.random() for i in xrange(dims)])
        d = ((seeds-pt)**2).sum(1)
        center = d.argmin()
        bigestDiff = max(abs(seeds[center]-pt))
        if bigestDiff < seedr[center]:
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
    s = gen(10000,4,2,0.01)
    x = [pt[0] for pt in s[1]]
    y = [pt[1] for pt in s[1]]

    #pylab.hist(x,10000)
    pylab.scatter(x,y)
    pylab.xticks(pylab.arange(0,1.01,0.2))
    pylab.yticks(pylab.arange(0,1.01,0.2))
    pylab.show()
