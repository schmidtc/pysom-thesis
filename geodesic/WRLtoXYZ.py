import sys

f = open(sys.argv[1],'r')
s = set()
for line in f:
    l = line.strip().strip(',').split()
    if len(l) ==3:
        try:
            l = map(float,l)
            l = tuple(l)
            s.add(l)
        except: pass

#print "%f %f %f"%(l[0],l[1],l[2])
for x,y,z in s:
    print x,y,z
