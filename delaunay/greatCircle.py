from math import cos,sin,radians,sqrt,asin,atan2,degrees
import math
radius = 1.0
class Point:
    def __init__(self,*args):
        if len(args) == 2:
            lat,lon = args
            self.lat = lat
            self.lon = lon
            self.x = radius * cos(radians(lon)) * cos(radians(lat))
            self.y = radius * sin(radians(lon)) * cos(radians(lat))
            self.z = radius * sin(radians(lat))
        elif len(args) == 3:
            x,y,z = args
            self.x = x
            self.y = y
            self.x = x
            self.lat = -degrees(asin(z/radius));
            self.lon = degrees(atan2(y, x));
    def __repr__(self):
        return "<Point: %f, %f>"%(self.lat,self.lon)
class GreatCircle:
    def __init__(self,pt1,pt2):
        self.arc_point = arc_point = [pt1,pt2]

        if (arc_point[0].lon == arc_point[1].lon) or (arc_point[0].lon == arc_point[1].lon + 180.0) or (arc_point[0].lon + 180.0 == arc_point[1].lon):
            self.is_meridian = True

        self.a = (arc_point[0].y * arc_point[1].z) - (arc_point[1].y * arc_point[0].z)
        self.b = (arc_point[1].x * arc_point[0].z) - (arc_point[0].x * arc_point[1].z)
        self.c = (arc_point[0].x * arc_point[1].y) - (arc_point[1].x * arc_point[0].y)
    def computeInflectionPoint(self):
        arc_point = self.arc_point
        a,b,c = self.a, self.b, self.c
        if arc_point[0].lat == arc_point[1].lat and arc_point[0].lon == arc_point[1].lon:
            self.inflection_point = Point(arc_point[0].lat, arc_point[0].lon)
            self.inflection_lat = self.inflection_point.lat
            return None
        
        max_z = sqrt((radius*radius*a*a + radius*radius*b*b) / (c*c+a*a+b*b))
        self.inflection_point = Point((-a*c*max_z)/(a*a+b*b),(-c*max_z + ((a*a*c*max_z)/(a*a+b*b)))/b , max_z)
        self.inflection_lat = self.inflection_point.lat
    def intersectsGreatCircle(self,other):
        a,b,c = self.a, self.b, self.c
        intersect_point = []

        numerator = ((other.a * c) - (other.c * a))
        denominator = ((other.b * a) - (other.a * b))
        g = numerator/denominator

        numerator = ((-g * b) - c)
        h = numerator / a

        numerator = radius**2.0
        denominator = math.pow(h, 2) + math.pow(g, 2) + 1
        w = sqrt(numerator/denominator)

        intersect_point.append(Point(h*w, g*w, w))
        intersect_point.append(Point(-h*w, -g*w, -w))
        return intersect_point

def splitEdge(edge):
    pt1,pt2= edge
    pt1 = Point(*pt1)
    pt2 = Point(*pt2)
    arc = GreatCircle(pt1,pt2)
    antiMeridian = GreatCircle(Point(90,0),Point(89,0))
    a = arc.intersectsGreatCircle(antiMeridian)
    if a[0].lon == 180 or a[0].lon == -180:
        lat = a[0].lat
    else:
        lat = a[1].lat
    print lat



from math import sin,cos,asin,sqrt,radians,degrees
def findIntersection(lat1,lon1,lat2,lon2): 
    lat1, lon1, lat2, lon2 = map(radians,[lat1, lon1, lat2, lon2])
    lambda1, delta1, lambda2, delta2 = lat1, lon1, lat2, lon2
    a = asin( (cos(delta1)*sin(delta2)*sin(lambda1) - cos(delta2)*sin(delta1)*sin(lambda2)) / sqrt( (cos(delta1)**2) * (cos(delta2)**2) * (sin( lambda1 - lambda2)**2) + (cos(delta1)*sin(delta2)*sin(lambda1) - cos(delta2)*sin(delta1)*sin(lambda2))**2))
    return degrees(a)

if __name__=='__main__':
    #pt1 = Point(163.547646,-84.383935)
    #pt2 = Point(-73.198884,-83.514260)
    #pt1 = Point(138.04994128321047, 84.746915392846248)
    #pt2 = Point(-178.39292475883215, 84.268032034802275)
    #arc = GreatCircle(pt1,pt2)
    #antiMeridian = GreatCircle(Point(90,-180),Point(0,-180))
    #a = arc.intersectsGreatCircle(antiMeridian)

    edge = ([163.547646, -84.383935] , [-73.198884, -83.514260])
    #edge = ([138.04994128321047, 84.746915392846248], [-178.39292475883215, 84.268032034802275])
    #splitEdge(edge)
    #a = findIntersection(-178.39292475883215, 84.268032034802275, 138.04994128321047, 84.746915392846248)
    a = findIntersection(163.547646, -84.383935, -73.198884, -83.514260)
