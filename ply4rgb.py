#!/usr/bin/env python

"""
test_any_model.py が出力した ply ファイルを、クラスごとに明確に色分けした pcd フォーマットに変換する。
変換した pcd ファイルは、CloudCompare で開くことができる。
"""

import os
import sys
import random
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import collections

from plyfile import PlyData, PlyElement
from numpy.lib import recfunctions as rfn
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

parser = OptionParser("usage: %prog [options] ply_file\nConvert PLY format to PCD format with Colormap.")
parser.add_option('-c', '--classes', help='number of classes', type=int, metavar='CLASSES')
parser.add_option('-o', '--output', help='output filename', metavar='FILE')
parser.add_option('-s', '--show-colormap', help='show colormap', action='store_true')
parser.add_option('--colormap', help='pyplot colormap name', default='Paired', metavar='COLORMAP')

(options, args) = parser.parse_args()
if options.classes is None:
	print('error! --classes is required.')
	parser.print_help()
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
	outfile = name + '.pcd'

ply = PlyData.read(infile)
print('ply', ply)
vertex = ply.elements[0]
labels = [prop.name for prop in vertex.properties[3:]]
print(labels)
indices = vertex['preds']

npcolmap = color_map(options.classes, options.colormap)

points = vertex[['x', 'y', 'z']]
print(points)
points = rfn.structured_to_unstructured(points)
colors = npcolmap[indices]

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points.astype(np.float32))
pcd.colors = o3d.utility.Vector3dVector(colors.astype(np.float32))
print("%s saving..." % outfile)
o3d.io.write_point_cloud(outfile, pcd)
