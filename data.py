"""
Python Self-Organizing Maps -- Data Tools
----------------------------------------------------------------------
AUTHOR(S):      Charles R. Schmidt cschmidt@rohan.sdsu.edu
----------------------------------------------------------------------
Copyright (c) 2006-2008  Charles R. Schmidt
======================================================================
This source code is probably licensed under the GNU General Public License,
Version 2, you should check.
======================================================================
"""
from numpy import array,empty

class ObsFile:
    def __init__(self,filename,fileType = 'complete'):
        self.filename = filename
        self.fileObj = open(filename,'r')
        self.fileType = fileType
        self.reset()
    def __iter__(self):
        return self
    def listolists(self,comments=False):
        self.fileObj.seek(0)
        lines = self.fileObj.readlines()
        dims = lines.pop(0)
        dims = int(dims)
        lines = [line.split() for line in lines]
        if not comments:
            lines = [line[:dims] for line in lines]
            lines = [array(map(float,line),'float') for line in lines]
        else:
            lines = [line[dims:] for line in lines]
        return lines
    def Snext(self):
        line = self.fileObj.next()
        id,line = line.split(':')
        line = line.split(',')
        Num = len(line)/2
        indices = empty(Num,'int16')
        values = empty(Num,'float')
        c = 0
        for n in xrange(0,Num*2,2):
            indices[c] = int(line[n])-1
            values[c] = float(line[n+1])
            c += 1
        return id,indices,values
    def Cnext(self):
        line = self.fileObj.next()
        line = line.split()
        id = self.nextLine
        for n in xrange(0,self.Dims):
            self.values[n] = float(line[n])
        self.nextLine+=1
        return id,self.indices,self.values
    def reset(self):
        self.fileObj.seek(0)
        self.nextLine = 0 #Zero Base
        if self.fileType == 'complete':
            self.next = self.Cnext
            self.Dims = int(self.fileObj.next())
            self.indices = array(range(self.Dims),'int16') 
            self.values = empty(self.Dims,'float') 
        elif self.fileType == 'sparse':
            self.next = self.Snext
        else:
            raise "fileTypeError"
    def stream(self):
        try:
            return self.next()
        except:
            self.reset()
            return self.next()
    def close(self):
        self.fileObj.close()
