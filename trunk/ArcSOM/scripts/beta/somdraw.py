#Martin Lacayo-Emery
#Fall 2006

#This program converts COD files into SHP files and other related formats
#parameters: (COD book file,Shapefile,Data to map onto the COD)

import Image, ImageDraw
from math import sqrt
from dbftool import dbfwriter


isize=(0,0)
dialation=100
border=100
cfilename="E:/arcSOM/test/states.cod"
ifilename="E:/arcSOM/test/cod.png"
ypad=int(border*sqrt(2)/1.5)
classes=256/4
classwidth=1.0/4

def round6(x):
    return round(x,6)

def imageround(x):
    return int(x*dialation)

def pointround(x):
    return [imageround(x[0])+border,imageround(x[1])+ypad]

###################################Process COD###########################

#open files from parameters
inputCOD = open(cfilename,'r')
centroidsDist=1

#get file headerilename
#list of strings of fomatting
formatting=inputCOD.readline().split()
#inputCOD.readline()
#list of strings of column headings
names=[]
for i in range(1,int(formatting[0])+1):
    names.append('att'+str(i))


header='Id,x,y'.split(',')+names
#+inputCOD.readline().strip('#n').split()
#parse cod
#list of strings lists of values
cod=[i.split() for i in inputCOD.readlines()]
print len(cod),"records found\n"
inputCOD.close()

#get formatting
topology=formatting[1]
x=int(formatting[2])
y=int(formatting[3])

isize=(int((x+1.5)*dialation),int((y-1.5)*dialation))
####################################Calculate centroidss####################
centroids=[]
#neurons listed from left to right, top to bottom
if topology=="rect":
    for lcvY in range(y):
        #loop over colomuns
        for lcvX in range(x,0,-1):
            centroids.append([float(lcvX*centroidsDist),float(lcvY*centroidsDist)])
elif topology=='hexa':
    #caluclate the changes for centroids
    deltaY=centroidsDist*sqrt(3.0/4)
    deltaX=centroidsDist*float(1)

    #set the orgin to start at 0,0 for the first point
    hexX=0-deltaX
    hexY=0
    for lcvY in range(y):
        for lcvX in range(x):
            #increment x coordinate
            hexX=hexX+deltaX
            centroids.append([hexX,hexY])

        #offset x coordinate for alternating rows        
        if (lcvY+1)%2:
            hexX=0-(deltaX/2)
        else:
            hexX=0-deltaX
        #increment y coordinate
        hexY=hexY+deltaY


#####################################Calculate Polygons#######################
polygons=[]
if topology=="rect":
    for i in centroids:
        #center point
        pX=i[0]
        pY=i[1]
        #derive extrema
        minX=pX-(0.5*centroidsDist)
        maxX=pX+(0.5*centroidsDist)
        minY=pY-(0.5*centroidsDist)
        maxY=pY+(0.5*centroidsDist)
        #number of parts 
        NumParts=1
        #total number of points
        NumPoints=4
        #bounding box
        Box=[minX,minY,maxX,maxY]
        #index to first point in part
        Parts=0
        #points for all parts
        #starts from top most, left most, and goes clock-wise
        Points=[Box,[[minX,maxY],[maxX,maxY],[maxX,minY],[minX,minY]]]
        polygons.append(Points)

elif topology=='hexa':
    for i in centroids:
  #center point
        pX=i[0]
        pY=i[1]
        #sides numberd in order of min length
        side2=0.5*centroidsDist
        side1=side2/sqrt(3)
        side3=2*side1
        #derive extreama
        minX=pX-side2
        maxX=pX+side2
        minY=pY-side3
        maxY=pY+side3
        #bounding box
        Box=[minX,minY,maxX,maxY]
        #number of parts
        NumParts=1
        #number of points
        NumPoints=6
        #index to first point in part
        Parts=0
        #starts from top most, left most, and goes clock-wise        
        Points=[Box,[[pX,pY+side3],[pX+side2,pY+side1],[pX+side2,pY-side1],[pX,pY-side3],[pX-side2,pY-side1],[pX-side2,pY+side1]]]
        polygons.append(Points)

##########################################
im = Image.new("RGB",isize)
draw = ImageDraw.Draw(im)

for i in range(32):
    for j in range(i,32):
        draw.rectangle([(0,0),im.size],fill=(255,255,255))
        for id,p in enumerate(polygons):
            R=255-int(int(float(cod[id][i])/classwidth)*(255*classwidth))
            #G=255-int(float(cod[id][8])*255)
            B=255-int(int(float(cod[id][j])/classwidth)*(255*classwidth))
            G=255#(R+B)/2
            draw.polygon(map(tuple,map(pointround,p[1])),fill=(R,G,B))
#del draw 

        # write to stdout
        a=str(i)
        b=str(j)
        if i<10:
            a='0'+a
        if j<10:
            b='0'+b
        ifilename="E:/arcSOM/images/"+a+b+".png"
        imagefile=open(ifilename,'wb')
        im.save(imagefile,'PNG')
        imagefile.close()
        print ifilename
del draw