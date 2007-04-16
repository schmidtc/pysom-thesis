#input file
ifile="z:/svn/data/example/BMUdata.txt"
ofile="z:/svn/data/example/segs/bmustate"

i=open(ifile,'r')

h=i.readline()

lines=i.readlines()
i.close()

lines2=[]
for m in range(49):
    for n in range(10):
        l=lines[m+(49*n)]
        l=l.strip().split(' ')
        l[2]=str(1900+(n*10))
        l=' '.join(l)+'\n'        
        lines2.append(l)

lines=lines2

for m in range(49):
    for n in range (9):
        o=open(ofile+str(m)+'-'+str(n)+'.txt','w')
        o.write(h)
        o.write(lines[m+(49*n)])
        o.write(lines[m+(49*(n+1))])
        o.close()  
      
        
    

    
