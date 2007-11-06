from utils import dbf
import sys

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

data = [map(float,l.split()) for l in data]
records = []
for i,d in enumerate(data):
    rec = [i]
    rec.extend(d)
    records.append(rec)

if 'graph' in fname:
    f = open('testResults/shapes/graph.dbf','wb')
if 'rook' in fname:
    f = open('testResults/shapes/rook.dbf','wb')
#names = ['ID','AFIELD','BFIELD','CFIELD','DFIELD','EFIELD','GFIELD']
#specs = [('N', 10, 0), ('N', 19, 11), ('N', 19, 11), ('N', 19,11), ('N', 19,11), ('N', 19,11), ('N', 19, 11)]
dbf.dbfwriter(f,names,specs,records)
f.close()

