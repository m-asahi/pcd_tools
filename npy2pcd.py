#!/usr/bin/env python

import os
import sys
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

from optparse import OptionParser

def color_map(n, map):
	colmap = plt.get_cmap(map, n)
	npcolmap = np.ndarray([n, 3])
	for i in range(n):
		npcolmap[i] = colmap(i)[0:3]
	z = np.zeros(3).reshape(1,3)
	npcolmap = np.insert(npcolmap, 0, z, axis=0)
	return npcolmap

parser = OptionParser("usage: %prog [options] npy_file\nConvert numpy XYZRGB format to PCD format.")
parser.add_option('-o', '--output', help='output filename', metavar='FILE')

(options, args) = parser.parse_args()
if len(args) == 0:
	parser.print_usage()
	sys.exit(1)

infile, outfile = args[0], options.output
if outfile is None:
	name = os.path.basename(infile)
	name = os.path.splitext(name)[0]
	name = name.replace('.npy_pts', '') # ConvPointのexampleが.npy_pts.txtを出す
	outfile = name + '.pcd'

pts = np.loadtxt(infile)
npcolmap = color_map(options.classes, options.colormap)

points = pts[:, 0:3]
colors = npcolmap[pts[:, 3].astype(int)]

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points.astype(np.float64))
pcd.colors = o3d.utility.Vector3dVector(colors.astype(np.float64))
o3d.io.write_point_cloud(outfile, pcd)