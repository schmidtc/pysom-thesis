from utils import dbf
import sys

if len(sys.argv) < 2:
    print "Usage: python visual.py /path/to/som.cod /path/to/som.ib"
else:
    fname = sys.argv[1]

    f = open(fname,'r')
    head = f.readline()
    data = f.readlines()
    f.close()

    dims = int(head.split()[0])
    names = ['ID']
    names.extend(['DIM'+str(i+1) for i in range(dims)])
    specs = [('N', 10, 0)]
    specs.extend([('N', 19, 11) for i in range(dims)])
    
    data = [map(float,l.split(' ')) for l in data]
    records = []
    for i,d in enumerate(data):
        rec = [i]
        rec.extend(d)
        records.append(rec)
    
    if len(sys.argv) > 2:
        ivfile = open(sys.argv[2],'r')
        names.extend(['Size','Degree','IV'])
        specs.extend([('N', 10, 0),('N', 10, 0),('N',19,11)])
        for rec in records:
            rec.extend([0,-99,-99.0])
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
    
    f = open('visual.dbf','wb')
    #names = ['ID','AFIELD','BFIELD','CFIELD','DFIELD','EFIELD','GFIELD']
    #specs = [('N', 10, 0), ('N', 19, 11), ('N', 19, 11), ('N', 19,11), ('N', 19,11), ('N', 19,11), ('N', 19, 11)]
    dbf.dbfwriter(f,names,specs,records)
    f.close()

