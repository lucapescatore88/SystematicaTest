from argparse import ArgumentParser
import random, math, sys
import numpy as np

### Function to create random labyrinths

def fillLabytinth(lab, nblack) :

    nb = 0
    while nb < nblack :
        nn = int(random.random() * lab.shape[0])
        mm = int(random.random() * lab.shape[1])
        
        if labyrinth[nn,mm] == 0 :
            labyrinth[nn,mm] = 1
            nb += 1

## Function to get from a position all the possible paths

def getOptions(pos) :

    opts = []
    #for op in [(-1,-1),(0,-1),(1,-1),(0,1),(-1,0),(-1,1),(1,0),(1,1)] : ## If diagoal paths possible
    for op in [(0,-1),(0,1),(-1,0),(1,0)] :
        if pos[0]+op[0] >= 0 and pos[1]+op[1] >= 0 and pos[0]+op[0] < n and pos[1]+op[1] < m :
            opts.append(op)
    return opts

## Given a path build all the possible paths adding one step with the following rules:
##  -- Use only white cases: not blocked paths
##  -- Check that the case is not already in the path: it's a loop!

def extend(path,labyrinth, verb = False) :

    paths = []
    pos = path[-1]
    opts = getOptions(pos)

    for op in opts :
        
        newn = pos[0]+op[0]
        newm = pos[1]+op[1]

        if verb : print "Going to", (newn,newm),
        ## To start with, don't go back. Or we get nasty loops!
        #if len(path) > 1 :
        #    if newn == path[-2][0] and newm == path[-2][1] : 
        #        if verb : print "Can't go back"
        #        continue
        ## Don't go to places with black squares otherwise add to paths
        if labyrinth[newn,newm] == 1 : 
            if verb : print "Blocked"
            continue
        # Avoid loops
        if (newn,newm) in path : 
            if verb : print "You turned in a loop!!!"
            continue

        if verb : print "Ok let's go!"
        newpath = path[:]
        newpath.append((newn,newm))
        paths.append(newpath)

    return paths

## Extend all possible paths until one hits the exit 
## or util there are no paths left to extend (no exit).
## It returns the shortest path

def exploreLabyrith(start, verb = False) :

    if labyrinth[start[0],start[1]] == 1 :
        if verb : print "Cant go"
        return -1

    paths = extend([start],labyrinth)

    while True :

        newpaths = []
        for p in paths :
            curpaths = extend(p,labyrinth,verb)
            newpaths.extend(curpaths)

        for p in newpaths :
            if p[-1][0] == n-1 and p[-1][1] == m-1:
                if verb : print "Exit!!", p, "Length = ", len(p)
                return len(p)

        paths = newpaths
        if len(paths) == 0 :
            if verb : print "There is no exit"
            return -1


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--size",type=int,default=[3,4],nargs=2,help="Size of the labytinh e.g. --size 6 7)")
    parser.add_argument("--fblack",type=float,default=0.2,help="Fraction of black squared")
    parser.add_argument("--ntoys",type=int,default=10000,help="Number of toys")
    parser.add_argument("--test",action="store_true",help="Shortcut for '-v -ntoys 1'")
    parser.add_argument("-v",action="store_true",help="Verbose")
    args = parser.parse_args()

    if args.test :
        args.ntoys = 1
        args.v = True

    n = args.size[0]
    m = args.size[1]
    nblack = math.floor(args.fblack * n * m)

    noexit = 0  ## Calculate fraction without exit
    avgl   = 0  ## Calculate average length
    for i in range(args.ntoys) :
        print "Processing.....  ", str(float(i+1) / args.ntoys * 100) +'% \r',
        labyrinth = np.zeros((n,m))
        fillLabytinth(labyrinth,nblack)
        if args.v :
            print "Labyrith"
            print labyrinth
        l = exploreLabyrith((0,0),args.v)
        if l > 0 : avgl += l
        else : noexit += 1

    print
    print "Average path = ", avgl / float(args.ntoys - noexit)
    print "Noexit = ", noexit/float(args.ntoys)









