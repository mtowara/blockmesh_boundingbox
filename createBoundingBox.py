#! /usr/bin/python

import sys
from math import ceil
import argparse
from numpy import matrix, maximum, minimum, array, cross
from numpy.linalg import norm

def ascii_foam_vector(v):
    sv = [str(d) for d in v]
    return "( " + ' '.join(sv) + ' )'

# Commandline argument parser
parser = argparse.ArgumentParser(description='Create bounding box blockMeshDict for provided stl.')
parser.add_argument('filename', type=str, help='filename.stl')
parser.add_argument('--extra-margin', '-e', dest="eps", metavar="eps", type=float, nargs='?', default=0.01, help='Additional space added to the bounding box (fraction of edge size)')
parser.add_argument('--spacing', '-d', metavar="d", type=float, nargs='?', default=1.0, help='Spacing')

args = parser.parse_args()
filename = args.filename
spacing = args.spacing
eps = args.eps

block_min = array([2**60,2**60,2**60])
block_max = array([-2**60,-2**60,-2**60])

try:
    for l in open(filename,'r'):
        if "vertex" in l:
            v = [float(s) for s in l.strip('\n').split(' ')[-3:]]
            # update max
            block_max = maximum(block_max,v)
            # update min
            block_min = minimum(block_min,v)

    if (eps>0):
        delta = eps*(block_max - block_min)
        block_max += delta
        block_min -= delta

except IOError as e:
    print "Exception: ",e
    exit(1)

vertices = ''
vertices += "    " + ascii_foam_vector([block_min[0],block_min[1],block_min[2]]) + '\n'
vertices += "    " + ascii_foam_vector([block_max[0],block_min[1],block_min[2]]) + '\n'
vertices += "    " + ascii_foam_vector([block_max[0],block_max[1],block_min[2]]) + '\n'
vertices += "    " + ascii_foam_vector([block_min[0],block_max[1],block_min[2]]) + '\n'

vertices += "    " + ascii_foam_vector([block_min[0],block_min[1],block_max[2]]) + '\n'
vertices += "    " + ascii_foam_vector([block_max[0],block_min[1],block_max[2]]) + '\n'
vertices += "    " + ascii_foam_vector([block_max[0],block_max[1],block_max[2]]) + '\n'
vertices += "    " + ascii_foam_vector([block_min[0],block_max[1],block_max[2]]) + '\n'

n_cells = ascii_foam_vector([int(ceil((block_max[0]-block_min[0])/spacing)), \
                             int(ceil((block_max[1]-block_min[1])/spacing)), \
                             int(ceil((block_max[2]-block_min[2])/spacing))])
try:
    template = open('blockMeshDict.template','r').read()
    print template.replace('$vertices',vertices.strip('\n')) \
                  .replace('$nCells',n_cells)
except IOError as e:
    print "Exception: ",e
