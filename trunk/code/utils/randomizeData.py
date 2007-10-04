import sys,random

fname = sys.argv[1]
f = open(fname,'r')
dims = f.readline()
lines = f.readlines()
f.close()


random.shuffle(lines)

o = open(fname,'w')
o.write(dims)
o.writelines(lines)

o.close()


