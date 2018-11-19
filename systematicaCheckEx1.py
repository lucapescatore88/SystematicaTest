from math import factorial as fact
from argparse import ArgumentParser
import random, math, sys

parser = ArgumentParser()
parser.add_argument("--ntoys",type=int,default=10000,help="Number of toys")
parser.add_argument("--n",type=int,default=4,help="Number of iterations")
parser.add_argument("--N0",type=int,default=2,help="Number of total balls at beginning")
parser.add_argument("--r",type=int,default=3,help="Number of red balls")
parser.add_argument("--r0",type=int,default=1,help="Number of red balls at beginning")
parser.add_argument("-v",action="store_true",help="Verbose")
args = parser.parse_args()

#### Validation

if args.N0 < 0 or args.n < 0 or args.r < 0 or args.r0 < 0 :
    print "Inputs do not meet the requirements: n, N0, r and r0 > 0"
    sys.exit()
if args.N0 < args.r0 :
    print "N0 cannot be lower than r0, please retry"
    sys.exit()
if args.n+args.N0 < args.r:
    print "r cannot be higher than n+N0, please retry"
    sys.exit()

#### Function to calculate probability obtained in exercise

def calcProb(n,r,N0,r0) :
    
    ## Divide in many terms to avoid computing problems with very large factorials
    term1 = fact(n) / float(fact(n-r+r0)) / float(fact(r-r0))
    term2 = fact(r-1) / fact(r0-1)
    term3 = fact(N0+n-r-1) / float(fact(N0-r0-1))
    term4 = fact(N0-1) / float(fact(N0+n-1))

    return term1*term2*term3*term4

def printStatus(n,r,pr,pick = None) :
    print "Ntot = {n}, Nred = {r},".format(n=n,r=r),
    if pick is not None :
        print "probred = {pr:5.4f}".format(pr=pr),
        if pick : print "---> pick red",
        else : print "---> pick yellow",
    print

## Run some toys to get the result empirically

avg = 0
nt = 0
while nt < args.ntoys :

    if args.v : print "------ New toy"
    
    nballs = args.N0
    rballs = args.r0
    for i in range(args.n) :
        probred = rballs / float(nballs)
        pickred = random.random() <= probred
        
        if args.v : printStatus(nballs,rballs,probred,pickred)

        if pickred : rballs += 1
        nballs += 1
    
    if args.v : printStatus(nballs,rballs,probred)
    if rballs == args.r : avg += 1
    nt+=1

### Compare the toys result and the calculated one

avg /= float(args.ntoys)
avge = math.sqrt(avg*(1-avg)/float(args.ntoys))
calc = calcProb(args.n,args.r,args.N0,args.r0)

print "The probability to have {r} red balls after {n} iterations starting".format(r=args.r,n=args.n),
print "with {n0} balls of which {r0} red is: {avg:6.5f} +/- {avge:6.5f}".format(r0=args.r0,n0=args.N0,avg=avg,avge=avge)
print "The calculated probability for this to happen is: ", calc
if abs(calc-avg) < 5*avge :
    print "Values are compatible within 5 sigma"







