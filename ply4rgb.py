#!/usr/bin/env python

"""
test_any_model.py が出力した ply ファイルを、クラスごとに明確に色分けした pcd フォーマットに変換する。
変換した pcd ファイルは、CloudCompare で開くことができる。
"""

import os
import sys
import numpy as np
import open3d as o3d
import collections

from plyfile import PlyData, PlyElement
from numpy.lib import recfunctions as rfn
from optparse import OptionParser

from pcdlib import color_map, generate_pcd, show_colormap


parser = OptionParser("usage: %prog [options] ply_file\nConvert PLY format to PCD format with Colormap.")
parser.add_option('-c', '--classes', help='number of classes', type=int, metavar='CLASSES')
parser.add_option('-o', '--output', help='output filename', metavar='FILE')
parser.add_option('-s', '--show-colormap', help='show colormap', action='store_true')
parser.add_option('--colormap', help='pyplot colormap name', default='Paired', metavar='COLORMAP')

(options, args) = parser.parse_args()

if options.show_colormap:
	show_colormap(options)
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
