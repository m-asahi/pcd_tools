#!/usr/bin/env python

import os
import sys
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from optparse import OptionParser

parser = OptionParser("usage: %prog [options] pcd_file\nConvert PCD format to numpy XYZRGB format.")
parser.add_option('-o', '--output', help='output filename', metavar='FILE')

(options, args) = parser.parse_args()
if len(args) == 0:
	parser.print_usage()
	sys.exit(1)


pcdfile, outfile = args[0], options.output
if outfile is None:
	name = os.path.basename(infile)
	name = os.path.splitext(name)[0]
	outfile = name + '.npy'

pcd = o3d.io.read_point_cloud(pcdfile, print_progress=True)
points = np.asarray(pcd.points)
colors = np.asarray(pcd.colors)
npy = np.insert(points, [3], colors, axis=1)
np.save(outfile, npy)