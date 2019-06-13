#! /usr/bin/python

import sys
from math import ceil
import argparse
from numpy import matrix, maximum, minimum, array, cross
from numpy.linalg import norm

def ascii_foam_vector(v):
    sv = [str(d) for d in v]
    return "( " + ' '.join(sv) + ' )'

parser = argparse.ArgumentParser(description='Create bounding box blockMeshDict for provided stl.')
parser.add_argument('filename', type=str, help='filename.stl')
parser.add_argument('--epsilon', '-e', metavar="eps", type=float, nargs='?', default=0.01, help='Additional space added to the bounding box (fraction of edge size)')
parser.add_argument('--spacing', '-d', metavar="d", type=float, nargs='?', default=1.0, help='Spacing')
parser.add_argument('--direction1','-d1', metavar="f", type=float, nargs=3, default=[1.0,0.0,0.0], help='Base')
parser.add_argument('--direction2','-d2', type=float, nargs=3, default=[0.0,1.0,0.0], help='Base')

args = parser.parse_args()
filename = args.filename
spacing = args.spacing
eps = args.epsilon

d1 = array(args.direction1)
d2 = array(args.direction2)
d1 /= norm(d1)
d2 /= norm(d2)
d3 = cross(d1,d2)

minB = array([2**60,2**60,2**60])
maxB = array([-2**60,-2**60,-2**60])

try:
    for l in open(filename,'r'):
        if "vertex" in l:
            v = [float(s) for s in l.strip('\n').split(' ')[-3:]]
            # update max
            maxB = maximum(maxB,v)
            # update min
            minB = minimum(minB,v)

    delta = eps*(maxB - minB)
    maxB += delta
    minB -= delta

except IOError as e:
    print "Exception: ",e
    exit(1)

vertices = ''
vertices += "    " + ascii_foam_vector([minB[0],minB[1],minB[2]]) + '\n'
vertices += "    " + ascii_foam_vector([maxB[0],minB[1],minB[2]]) + '\n'
vertices += "    " + ascii_foam_vector([maxB[0],maxB[1],minB[2]]) + '\n'
vertices += "    " + ascii_foam_vector([minB[0],maxB[1],minB[2]]) + '\n'

vertices += "    " + ascii_foam_vector([minB[0],minB[1],maxB[2]]) + '\n'
vertices += "    " + ascii_foam_vector([maxB[0],minB[1],maxB[2]]) + '\n'
vertices += "    " + ascii_foam_vector([maxB[0],maxB[1],maxB[2]]) + '\n'
vertices += "    " + ascii_foam_vector([minB[0],maxB[1],maxB[2]]) + '\n'

grading = ascii_foam_vector([int(ceil((maxB[0]-minB[0])/spacing)), \
                             int(ceil((maxB[1]-minB[1])/spacing)), \
                             int(ceil((maxB[2]-minB[2])/spacing))])
try:
    template = open('bb_template','r').read()
    print template.replace('$vertices',vertices.strip('\n')) \
                  .replace('$grading',grading)
except IOError as e:
    print "Exception: ",e
