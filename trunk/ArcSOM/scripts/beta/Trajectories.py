import sys

files = sys.argv[1].split(';')
shpfile = sys.argv[2]

print
print "You selected output "+shpfile
for f in files:
    print "You selected file "+f