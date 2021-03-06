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


parser = OptionParser("usage: %prog [options] ply_file ...\nConvert PLY format to PCD format with Colormap.")
parser.add_option('-c', '--classes', help='number of classes', type=int, metavar='CLASSES')
parser.add_option('-s', '--show-colormap', help='show colormap', action='store_true')
parser.add_option('--colormap', help='specify semantic3d, npm3d or pyplot colormap name', default='Paired', metavar='COLORMAP')

(options, args) = parser.parse_args()

if options.show_colormap:
	show_colormap(options)
	sys.exit(0)

if len(args) == 0:
	parser.print_usage()
	sys.exit(1)



def generate_outfile(infile):
	name = os.path.basename(infile)
	name = os.path.splitext(name)[0]
	return name + '.pcd'


for infile in args:
	ply = PlyData.read(infile)
	vertex = ply.elements[0]
	labels = [prop.name for prop in vertex.properties[3:]]
	indices = vertex['preds']

	npcolmap = color_map(options.classes, options.colormap)

	points = vertex[['x', 'y', 'z']]
	points = rfn.structured_to_unstructured(points)
	colors = npcolmap[indices]

	pcd = o3d.geometry.PointCloud()
	pcd.points = o3d.utility.Vector3dVector(points.astype(np.float32))
	pcd.colors = o3d.utility.Vector3dVector(colors.astype(np.float32))
	outfile = generate_outfile(infile)
	print("saving %s ..." % outfile)
	o3d.io.write_point_cloud(outfile, pcd)
