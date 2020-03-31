import random

import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt


def color_map(n, map):
	black      = [0,0,0]
	ground     = [132, 145, 158]
	buildings  = [200, 200, 203]
	roadsign   = [246, 170, 0]
	bollard    = [153, 0, 153]
	trashcan   = [77, 196, 255]
	barrier    = [0, 90, 255]
	pedestrian = [255, 75, 0]
	car        = [255, 241, 0]
	vegetation = [216, 242, 85]
	trees      = [3, 175, 122]
	flowers    = [119, 217, 168]
	artifacts  = [201, 172, 230]

	if map == 'npm3d':
		colmap = [black, ground, buildings, roadsign, bollard, 
			trashcan, barrier, pedestrian, car, vegetation ]
		npcolmap = np.array(colmap)/255

	elif map == 'semantic3d':
		colmap = [black, ground, vegetation, trees, flowers, buildings, 
			barrier, artifacts, car]
		if n == 8:
			# for ConvPoint x Semantic3D
			colmap.pop(0)
		elif n == 9 or n is None:
			pass
		else:
			raise "classes option must be 8 or 9."
		npcolmap = np.array(colmap)/255

	else:
		colmap = plt.get_cmap(map, n)
		npcolmap = np.ndarray([n, 3])
		# npcolmap[0] を黒に設定
		npcolmap[0] = np.zeros(3).reshape(1,3)
		for i in range(n - 1):
			npcolmap[i + 1] = colmap(i)[0:3]

	return npcolmap


def generate_pcd(output, colmap):
	n = len(colmap)
	points = []
	colors = []
	size = 10000
	for x in np.arange(0, n, 1/size):
		r = random.random()
		y = random.random()
		points.append([int(x) + r, y, 0])
		colors.append(colmap[int(x)])
	pcd = o3d.geometry.PointCloud()
	pcd.points = o3d.utility.Vector3dVector(np.array(points))
	pcd.colors = o3d.utility.Vector3dVector(np.array(colors))
	o3d.io.write_point_cloud(output, pcd)



def show_colormap(options):
	n = options.classes
	map = options.colormap
	npcolmap = color_map(n, map)
	n = n or len(npcolmap)
	# print(npcolmap)
	outfile = '{0}-{1}.pcd'.format(map, n)
	print("saving %s..." % outfile)
	generate_pcd(outfile, npcolmap)
