from argparse import ArgumentParser
import random
import math

parser = ArgumentParser()
parser.add_argument("--ntoys",type=int,default=10000,help="Number of toys")
parser.add_argument("--r",type=float,default=1.,help="Sphere radius")
args = parser.parse_args()

def getRandomInCircle(r) :
    alpha = random.random()*2*math.pi
    radius = random.random()*r
    #print random.random(), alpha/math.pi, radius
    return radius * math.cos(alpha), radius * math.sin(alpha)

print "Fraction of times where : "

#### Problem 1

l_triangle = math.sqrt(3)*args.r

npass = 0

for i in range(args.ntoys):

    x1,y1 = getRandomInCircle(args.r)
    x2,y2 = getRandomInCircle(args.r)
    d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    if d > l_triangle : npass+=1

avg  = npass/float(args.ntoys)
avge = math.sqrt(avg*(1-avg)/float(args.ntoys))
print " - the distance between two random points in a circle is longer then the inscribed triangle side:",
print "{avg:5.4f} +/- {avge:5.4f}".format(avg=avg,avge=avge)


## Problem 2

### The chord with middle point (xm,ym) is the one perpendicular to the radius passing through (xm,ym).
def calcCordLenRad(xm,ym,r) :

    ### dm = r cos (alpha) where alpha is the angle at the center
    dm = xm**2 + ym**2
    alpha = math.acos( dm / r )
    return 2 * r * math.sin(alpha) 


npass = 0

for i in range(args.ntoys):

    xm,ym = getRandomInCircle(args.r)
    d = calcCordLenRad(xm,ym,args.r)
    if d > l_triangle : npass+=1

avg  = npass/float(args.ntoys)
avge = math.sqrt(avg*(1-avg)/float(args.ntoys))
print " - the chord with middle point (xm,ym) is longer then the inscribed triangle side:",
print "{avg:5.4f} +/- {avge:5.4f}".format(avg=avg,avge=avge)


### Problem 3

def calcCordLen(m,q,r) :

    # Intersection with circle ax^2 + bx + c = (1+m)*x^2 + 2qmx + (q^2-r^2) = 0
    a = (1+m**2)
    b = q*m
    c = (q**2 - r**2)
    delta = b**2 - a*c 
    if delta < 0 :
        print "Something wrong this should not happen" 
        return -1
    
    x1 = (- b - math.sqrt(delta)) / a
    y1 = m * x1 + q
    x2 = (- b + math.sqrt(delta)) / a
    y2 = m * x2 + q
    
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


npass = 0
for i in range(args.ntoys):

    x1,y1 = getRandomInCircle(args.r)
    x2,y2 = getRandomInCircle(args.r)

    # Line passing through two points
    m_cord = (y2 - y1) / (x2 - x1)
    q_cord = y1 - m_cord*x1

    d = calcCordLen(m_cord,q_cord,args.r)
    if d > l_triangle : npass+=1

avg  = npass/float(args.ntoys)
avge = math.sqrt(avg*(1-avg)/float(args.ntoys))
print " - the chord passing by two random points is longer than the inscribed triangle side:",
print "{avg:5.4f} +/- {avge:5.4f}".format(avg=avg,avge=avge)





