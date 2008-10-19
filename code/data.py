"""
======================================================================
Python Self-Organizing Maps -- Data Tools
----------------------------------------------------------------------
AUTHOR(S):      Charles R. Schmidt cschmidt@rohan.sdsu.edu
----------------------------------------------------------------------
* Copyright (c) 2006-2008, Charles R. Schmidt
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
*     * Redistributions of source code must retain the above copyright
*       notice, this list of conditions and the following disclaimer.
*     * Redistributions in binary form must reproduce the above copyright
*       notice, this list of conditions and the following disclaimer in the
*       documentation and/or other materials provided with the distribution.
*     * Neither the name of the San Diego State University nor the
*       names of its contributors may be used to endorse or promote products
*       derived from this software without specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY Charles R. Schmidt ''AS IS'' AND ANY
* EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL Charles R. Schmidt BE LIABLE FOR ANY
* DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
* ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
* SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
======================================================================
"""

from numpy import array,empty

class ObsFile:
    ''' ObsFile provides an interface to your Observation Data File.
        The File should be formated as follows:
        The first line should contain only the number of dimmension in the data set.
        Each subsequant line should contain one observation, each value should be seperated
        a space.
    '''
    def __init__(self,filename,fileType = 'complete'):
        ''' Opens the file '''
        self.filename = filename
        self.fileObj = open(filename,'r')
        self.fileType = fileType
        self.reset()
    def __iter__(self):
        ''' Create an interator '''
        return self
    def listolists(self,comments=False):
        ''' Returns the entire data file as a list of lists '''
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
        ''' Returns the next line of a "sparse" data file.
            A sparse data file is one that contains missing values
        '''
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
        ''' Return the next line of a "complete" data file.
            A complete data file is one without any missing values.
        '''
        line = self.fileObj.next()
        line = line.split()
        id = self.nextLine
        for n in xrange(0,self.Dims):
            self.values[n] = float(line[n])
        self.nextLine+=1
        return id,self.indices,self.values
    def reset(self):
        ''' Resets the file such that the next line returned is the first line '''
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
        ''' Loops of the records, always returns a line, if the end of file is reached, 
            the file is seeked back to that start.
        '''
        try:
            return self.next()
        except:
            self.reset()
            return self.next()
    def close(self):
        ''' Close the file '''
        self.fileObj.close()
