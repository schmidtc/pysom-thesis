#input file
ifile="z:/svn/data/example/bmustate.txt"
ofile="z:/svn/data/example/segs/bmustate"

i=open(ifile,'r')

h=i.readline()

lines=i.readlines()
i.close()
for m in range(49):
    for n in range (9):
        o=open(ofile+str(m)+'-'+str(n)+'.txt','w')
        o.write(h)
        o.write(lines[m+(49*n)])
        o.write(lines[m+(49*n)+1])
        o.close()  
      
        
    

    
