import sys

#folder without last \
folder=sys.argv[1]
#boolean
if sys.argv[2]=="true":
    pause=1
else:
    pause=0


mapinit=open(folder+"\\scripts\\mapinit.bat",'w')
visual=open(folder+"\\scripts\\visual.bat",'w')
vsom=open(folder+"\\scripts\\vsom.bat",'w')

#mapinit
mapinit.write("@"+folder+"\\ArcSOM\\SOM_PAK\\mapinit.exe -din %1 -cout %2 -topol %3 -neigh %4 -xdim %5 -ydim %6 -init %7\n")
if pause:
    mapinit.write("@pause\n")
mapinit.close()

#visual
visual.write("@Echo visial.exe script for Arcgis\n")
visual.write("@if not %4 == \"true\" goto skip\n")
visual.write("@if not %5 == \"#\" goto buffer\n")
visual.write("\n")
visual.write("@Echo no optional parameters passed\n")
visual.write("@Echo begining visual.exe\n")
visual.write("@"+folder+"\\ArcSOM\\SOM_PAK\\visual.exe -din %1 -cin %2 -dout %3\n")
visual.write("@goto end\n")
visual.write("\n")
visual.write(":skip\n")
visual.write("@if not %5 == \"#\" goto skipbuffer\n")
visual.write("@Echo vector no skip mode \n")
visual.write("@Echo begining visual.exe\n")
visual.write("@"+folder+"\\ArcSOM\\SOM_PAK\\visual.exe -din %1 -cin %2 -dout %3 -noskip\n")
visual.write("@goto end\n")
visual.write("\n")
visual.write(":buffer\n")
visual.write("@Echo read buffer mode\n")
visual.write("@Echo begining visual.exe\n")
visual.write("@"+folder+"\\ArcSOM\\SOM_PAK\\visual.exe -din %1 -cin %2 -dout %3 -buffer %5\n")
visual.write("@goto end\n")
visual.write("\n")
visual.write(":skipbuffer\n")
visual.write("@Echo vector no skip and read buffer mode\n")
visual.write("@Echo begining visual.exe\n")
visual.write("@"+folder+"\\ArcSOM\\SOM_PAK\\visual.exe -din %1 -cin %2 -dout %3 -noskip -buffer %5\n")
visual.write("@goto end\n")
visual.write("\n")
visual.write(":end \n")
if pause:
    visual.write("@pause\n")
visual.close()

#vsom
vsom.write("@"+folder+"\\ArcSOM\\SOM_PAK\\vsom.exe -din %1 -cin %2 -cout %3 -rlen %4 -alpha %5 -radius %6\n")
if pause:
    vsom.write("@pause\n")
vsom.close()