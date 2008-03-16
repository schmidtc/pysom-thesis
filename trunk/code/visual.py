from utils import dbf
import sys

def read(fname,ivfileName,pre=''):
    f = open(fname,'r')
    head = f.readline()
    data = f.readlines()
    f.close()

    dims = int(head.split()[0])
    names = [pre+'ID']
    names.extend([pre+'DIM'+str(i+1) for i in range(dims)])
    specs = [('N', 10, 0)]
    specs.extend([('N', 19, 11) for i in range(dims)])
    
    data = [map(float,l.split(' ')) for l in data]
    records = []
    for i,d in enumerate(data):
        rec = [i]
        rec.extend(d)
        records.append(rec)
    
    if 1:
        ivfile = open(ivfileName,'r')
        names.extend([pre+'Size',pre+'Degree',pre+'IV'])
        specs.extend([('N', 11, 0),('N', 10, 0),('N',19,11)])
        for i in xrange(len(records)):
            records[i].extend([0,-99,-99.0])
        for line in ivfile:
            nid,size,deg,iv = line.split(',')
            nid = int(nid)
            size = int(size)
            deg = int(deg)
            iv = float(iv)
            records[nid][-3] = size
            records[nid][-2] = deg
            records[nid][-1] = iv
        ivfile.close()
    
    return names,specs,records

def write(names,specs,records):
    f = open('visual.dbf','wb')
    #names = ['ID','AFIELD','BFIELD','CFIELD','DFIELD','EFIELD','GFIELD']
    #specs = [('N', 10, 0), ('N', 19, 11), ('N', 19, 11), ('N', 19,11), ('N', 19,11), ('N', 19,11), ('N', 19, 11)]
    dbf.dbfwriter(f,names,specs,records)
    f.close()



if __name__=="__main__":
    if len(sys.argv) < 2:
        print "Usage: python visual.py /path/to/som.cod /path/to/som.iv"
    else:
        fname = sys.argv[1]
        ivfile = sys.argv[2]

        if '*' not in fname:
            write(*read(fname,ivfile))
        else:
            fn = fname.replace('*',str(0))
            iv = ivfile.replace('*',str(0))
            names,specs,recs = read(fn,iv,pre='no%d_'%0)
            #outNames = names[:1]
            outNames = ['Node_ID']
            outNames.append(names[-1])
            outSpecs = specs[:1]
            outSpecs.append(specs[-1])
            outRecs = []
            for r in recs:
                outRecs.append([r[0],r[-1]])
            
            for i in range(1,10):
                fn = fname.replace('*',str(i))
                iv = ivfile.replace('*',str(i))
                names,specs,recs = read(fn,iv,pre='no%d_'%i)
                outNames.append(names[-1])
                outSpecs.append(specs[-1])
                for i,r in enumerate(recs):
                    outRecs[i].append(r[-1])
            write(outNames,outSpecs,outRecs)
