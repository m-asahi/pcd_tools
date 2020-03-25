#!/usr/bin/env python
"""
ply ファイルのヘッダを表示する
"""

import sys
from plyfile import PlyData, PlyElement

print(sys.argv)
infile = sys.argv[1]
ply = PlyData.read(infile)
print(ply)
