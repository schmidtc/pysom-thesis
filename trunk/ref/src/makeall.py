import geosom,os
import sys
from commands import getoutput,getstatusoutput
from math import *

Nodes = range(3,1000)
for n in Nodes:
	getoutput('/opt/local/bin/python /home/un/m/cschmidt/src/Grid2XYZ.py %d'%n)
	sys.stdout.write('\r\t%d'%n)
	sys.stdout.flush()


