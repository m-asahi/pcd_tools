#!/usr/bin/env python

"""
つくば市内のLiDERデータのbinファイルから、velobin2txt.rb で生成した txt ファイルを ply フォーマットに変換する。
.ply ファイルは、test_any_model.py を NPM3D モデルで動かすときに読み込めるフォーマットなので、
KPConv/Data/NPM3D/test_points に置くこと。
"""

import os
import sys
import numpy as np
from plyfile import PlyData, PlyElement
from optparse import OptionParser

parser = OptionParser("usage: %prog [options] txt_file\nConvert Velodyne TXT format to PLY format.")
parser.add_option('-o', '--output', help='output filename', metavar='FILE')

(options, args) = parser.parse_args()
if len(args) == 0:
	parser.print_usage()
	sys.exit(1)


infile, outfile = args[0], options.output
if outfile is None:
	name = os.path.basename(infile)
	name = os.path.splitext(name)[0]
	outfile = name + '.ply'

points = np.loadtxt(infile, dtype="float")

# [xyz]_originを挿入
points = np.insert(points, [3], np.zeros(len(points)*3, dtype=np.float32).reshape(len(points), 3), axis=1)
# GPS_timeを挿入
points = np.insert(points, [6], np.zeros(len(points), dtype=np.float64).reshape(len(points), 1), axis=1)

dtype = np.dtype([
	('x', np.float32), 
	('y', np.float32), 
	('z', np.float32), 
	('x_origin', np.float32), 
	('y_origin', np.float32), 
	('z_origin', np.float32), 
	('GPS_time', np.float64), 
	('reflectance', np.float32)
	])

vertex = np.array([tuple(p) for p in points[:, 0:8]], dtype=dtype)
# print(vertex.dtype)
# print(vertex)


ply = PlyData([
	PlyElement.describe(vertex, 'vertex', val_types={
		'x': np.float32,
		'y': np.float32,
		'z': np.float32,
		'x_origin': np.float32,
		'y_origin': np.float32,
		'z_origin': np.float32,
		'GPS_time': np.float64,
		'reflectance': np.float32
		})])
print(ply)
ply.write(outfile)
