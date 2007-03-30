def result2kml(inFileName,outFileName):
        header = """<?xml version="1.0" encoding="utf-8" ?>
<kml xmlns="http://earth.google.com/kml/2.0">
<Document>\n"""

        folderH = "<Folder><name>%s</name>\n"
        folderF = "</Folder>\n"
        footer = "</Document></kml>"
        place = """
  <Placemark>
    <LookAt>
      <longitude>%s</longitude>
      <latitude>%s</latitude>
      <range>8000000</range>
    </LookAt>
    <description><![CDATA[
      <b>node:</b> <i>%s</i><br />
      <b>qerror:</b> <i>%s</i><br />
    ]]></description>
    <Point><coordinates>%s,%s</coordinates></Point>
  </Placemark>"""
        f = open(inFileName,'r')
        f.readline() #skip head
        o = open(outFileName,'w')
        o.write(header)
        c = 0
        for line in f:
                line = line.split()
                lng = line[0]
                lat = line[1]
                #err = line[2]
                err = 0
                o.write(place%(lng,lat,c,err,lng,lat))
                o.write(place%(lng,lat,c,err,lng,lat))
                c+=1
        o.write(footer)
        o.close()
        f.close()
if __name__=="__main__":
        import sys
        infile = sys.argv[1]
        outfile = sys.argv[2]
        result2kml(infile,outfile)
