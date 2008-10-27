from numpy import array,ones
#from Numeric import *
#from MLab import *
#import LinearAlgebra as LA
#import csv as CSV
#mm = matrixmultiply
#t = transpose

def grid2Rook(nRows,nCols,binary=0):
    """
Module Doc
------
Weights Matrix Utilities for Space-Time Analysis of Regional Systems
----------------------------------------------------------------------
AUTHOR(S):  Mark V. Janikas janikas@users.sourceforge.net  
            Serge Rey sjrey@users.sourceforge.net
----------------------------------------------------------------------
Copyright (c) 2000-2006  Sergio J. Rey
======================================================================
This source code is licensed under the GNU General Public License, 
Version 2.  See the file COPYING for more details.
======================================================================

OVERVIEW:

Methods for generating and working with sparse weigths matrices.
------

    Function doc
    --------

    Creates the sparse dictionary input for the Weights class for PySal based on a standard grid.
    
    Call:       grid2RookTorus(nRows,nCols,binary=0)
    Arguments:  nRows (integer): Number of rows in the grid.
                nCols (integer): Number of columns in the grid.
                binary (integer) (options: 0,1): Construct binary weights matrix.  Default is row
                    standardized.
    Returns:    (dict): Sparse weights dictionary for direct usage or as input
                    into the Weights Class.  Keys are the ids, values are lists with three
                    elements, the first is the number of neighbors (integer), the
                    second is an array (of integers) of neighbor ids, and the third is an
                    array (of floats) of weight values (binary or row standardized).
    Usage:
                >>> sp = grid2Rook(4,4)
                >>> spBinary = grid2Rook(4,4,binary=1) 
    """
    n = nRows * nCols
    neighs = [ [] for i in range(n) ]
    s0 = 0
    final = {}
    for i in range(nRows):
        for j in range(nCols):
            k = i * nCols + j
            # to left
            if j:
                neighs[k].append(k-1)
            # to right
            if j < nCols - 1:
                neighs[k].append(k+1)
            # above
            if i:
                neighs[k].append(k - nCols)
            # below
            if i < nRows - 1:
                neighs[k].append(k + nCols)
            neighs[k].sort()
            nn = len(neighs[k])
            nhs = array(neighs[k])
            vals = ones((1,nn), 'd')[0]
            if binary == 0:
                vals = vals * (1 / (nn*1.)) 
            final[k] = [nn,nhs,vals]
    return final

def rookPts(rows,cols):
    delta = 1.0
    x = 0
    y = 0
    pts = []
    for row in xrange(rows):
        for col in xrange(cols):
            pts.append((x,y))
            x += delta
        y += delta
        x = 0
    return pts
def rookPoly(pts):
    delta=0.5
    polys = []
    for x,y in pts:
        poly = []
        poly.append([x-delta,y+delta])
        poly.append([x+delta,y+delta])
        poly.append([x+delta,y-delta])
        poly.append([x-delta,y-delta])
        polys.append([poly,poly]) #bbox,poly
    return polys
if __name__=='__main__':
    pts = rookPts(23,28)
    polys = rookPoly(pts)
