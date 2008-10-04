#!/usr/local/bin/python
import sys,random
def randgen(dims,obs):
    data = [[random.random() for j in xrange(dims)] for i in xrange(obs)]
    return data    
def toStr(data):
    data = [' '.join(map(str,line)) for line in data]
    data = '\n'.join(data)
    return data

if __name__=='__main__':
    dims = int(sys.argv[1])
    l = int(sys.argv[2])
    o = sys.argv[3]
    d = randgen(dims,l)
    o = open(o,'w')
    o.write('%d\n'%dims)
    o.writelines(toStr(d))
    o.write('\n')
    o.close()
