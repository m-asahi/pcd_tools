#!/usr/bin/env ruby

# Velodyne LIDAR によるbinファイルをtxtフォーマットに変換する。
#
# xxxxx.bin を与えると、カレントフォルダに xxxxx.txt を出力する。
#
# bin フォーマットについて
# 32bit float（リトルエンディアン）４つで一つのボクセル
# x, y, z, refrectance information(反射率情報)
# https://github.com/yanii/kitti-pcl/blob/master/KITTI_README.TXT
# Velodyne #D laser scan data の項による
#
#
# txt フォーマットについて
# Semantic3D の使っているテキストフォーマット。
# x, y, z, intensity, r, g, b
# http://www.semantic3d.net/view_dbase.php?chi=2 
# 
# binファイルには色情報がないので一律白にする


require "optparse"

# IO インスタンスに点群を txt フォーマットで書き出す。
# @param [IO] out 出力先の IO(File) インスタンス
# @param [Array of Float Array] points 点群(x,y,z,reflectance informationの4つのFloatで一つの点)
def put_txt(out, points)
  out.puts "DATA ascii"
  points.each do |a|
    out.printf("%f %f %f %f 255 255 255\n", *a)
  end
end

params = ARGV.getopts('', 'help')
if params['help']
  puts "usage: #{$PROGRAM_NAME} bin_file ... "
  puts "\tconvert .bin files of Velodyne LiDAR to .txt files"
  exit
end

ARGV.each do |filename|
  bin = open(filename) { |f| f.read(f.size) }
  floats = bin.unpack('e*')
  points = floats.each_slice(4).to_a
  txtfile = File.basename(filename, '.*') << '.txt'
  puts txtfile
  open(txtfile, 'w') do |out|
    put_txt out, points
  end
end