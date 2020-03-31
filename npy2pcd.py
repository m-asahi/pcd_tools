#!/usr/bin/env python

"""
X,Y,Z,ラベル番号の情報を含む（numpy.savetxtで出力された）テキストファイルを、pcdフォーマットに変換する。
テキストの１行のはじめの３つの数値を点の位置  x,y,z 、次の数値をラベル番号とみなす。
これは ConvPoint で識別された *.npy_pts.txt 形式のファイルに対応している。
"""

import os
import sys
import numpy as np
import open3d as o3d

from optparse import OptionParser

from pcdlib import color_map, generate_pcd, show_colormap

parser = OptionParser("usage: %prog [options] npy_txt_file\nConvert numpy XYZ-Label format to PCD format with Colormap.")
parser.add_option('-c', '--classes', help='number of classes', type=int, metavar='CLASSES')
parser.add_option('-s', '--show-colormap', help='show colormap', action='store_true')
parser.add_option('--colormap', help='specify pyplot colormap name', default='Paired', metavar='COLORMAP')

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
	name = name.replace('.npy_pts', '') # ConvPointのexampleが.npy_pts.txtを出す
	outfile = name + '.pcd'

pts = np.loadtxt(infile)
npcolmap = color_map(options.classes, options.colormap)

points = pts[:, 0:3]
colors = npcolmap[pts[:, 3].astype(int)]

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points.astype(np.float64))
pcd.colors = o3d.utility.Vector3dVector(colors.astype(np.float64))
print("%s saving..." % outfile)
o3d.io.write_point_cloud(outfile, pcd)
