# Brian Hamrick
# 10/7/08
# FILE: pgm.py

# This file is a library to read, write, and modify
# pgm and ppm files to be outputted as a grayscale
# pgm file. It supports reading and writing to/from
# files along with getting and setting individual pixel
# values. Output is in binary mode rather than ASCII.
# Pixel values are simply an int with the intensity.

from Numeric import array
import sys

class pgm:
	def __init__(self):
		self.fmt_str='P5\n'
		self.width=0
		self.height=0
		self.max_intensity=255
		self.pixels=array([],'i')
	def read(self, filename):
		fin = open(filename,"r")
		line = fin.readline()
		type = line
		line = fin.readline()
		if line[0]=='#':
			line = fin.readline()
		dim = line.split()
		self.width = int(dim[0])
		self.height = int(dim[1])
		self.max_intensity = int(fin.readline())
		image = fin.read()
		foo=[]
		if type == 'P5\n':
			for c in image:
				foo.append(ord(c))
		elif type == 'P6\n':
			i = 0
			while i+2 < len(image):
				red = ord(image[i])
				green = ord(image[i+1])
				blue = ord(image[i+2])
				foo.append(int(0.3*red+0.59*green+0.11*blue))
				i+=3
		self.pixels=array(foo,'i')
		fin.close()
	def write(self, filename):
		fout = open(filename,"w")
		fout.write(self.fmt_str)
		fout.write(str(self.width) + ' ' + str(self.height) + '\n')
		fout.write(str(self.max_intensity)+'\n')
		outstr=''
		for i in self.pixels:
			outstr+=chr(min(i,255))
		fout.write(outstr)
		fout.close()
	def get_pixel(self, r, c):
		if r < 0 or c < 0 or r > self.height-1 or c > self.width-1:
			return -1
		return self.pixels[r*self.width+c]
	def set_pixel(self, r, c, v):
		if r < 0 or c < 0 or r > self.height-1 or c > self.width-1:
			return
		self.pixels[r*self.width+c] = v
