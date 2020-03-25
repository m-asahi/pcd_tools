#!/usr/bin/env python

import os
import sys
import random
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


def generate_pcd(output, colmap):
	n = len(colmap)
	points = []
	colors = []
	size = 10000
	for x in np.arange(0, n, 1/size):
		r = random.random() + int(x)
		y = random.random()
		points.append([r, y, 0])
		colors.append(npcolmap[int(x)])
	pcd = o3d.geometry.PointCloud()
	pcd.points = o3d.utility.Vector3dVector(np.array(points))
	pcd.colors = o3d.utility.Vector3dVector(np.array(colors))
	o3d.io.write_point_cloud(output, pcd)

parser = OptionParser("usage: %prog [options] npy_txt_file\nConvert numpy XYZ-Label format to PCD format with Colormap.")
parser.add_option('-c', '--classes', help='number of classes (required)', type=int, metavar='CLASSES')
parser.add_option('-o', '--output', help='output filename', metavar='FILE')
parser.add_option('-s', '--show-colormap', help='show colormap', action='store_true')
parser.add_option('--colormap', help='pyplot colormap name', default='Paired', metavar='COLORMAP')

(options, args) = parser.parse_args()
if options.classes is None:
	print('error! --classes is required.')
	sys.exit(1)

if options.show_colormap:
	n = options.classes
	map = options.colormap
	npcolmap = color_map(n, map)
	# print(npcolmap)
	output = options.output or '{0}-{1}.pcd'.format(map, n)
	generate_pcd(output, npcolmap)
	sys.exit(0)

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