# Brian Hamrick
# 9/30/08
# Sobel Method of edge detection

import sys
import copy
from pgm import pgm
from ppm import ppm

threshold = 300

if len(sys.argv) < 2:
	print 'YOU FAIL: NO INPUT FILE'
	sys.exit(0)

infile = sys.argv[1]
outfile = infile[:-4] + '_edge.ppm'

img = pgm()
img.read(infile)
out_img = ppm()
out_img.read(infile)

if len(sys.argv) >= 3:
	threshold = int(sys.argv[2])

r = 1
while r < img.height-1:
	c = 1
	while c < img.width-1:
		gx = img.get_pixel(r-1,c+1) + 2*img.get_pixel(r,c+1) + img.get_pixel(r+1,c+1) - img.get_pixel(r-1,c-1) - 2*img.get_pixel(r,c-1) - img.get_pixel(r+1,c-1)
		gy = img.get_pixel(r+1,c-1) + 2*img.get_pixel(r+1,c) + img.get_pixel(r+1,c+1) - img.get_pixel(r-1,c-1) - 2*img.get_pixel(r-1,c) - img.get_pixel(r-1,c+1)
		if abs(gx) + abs(gy) > threshold:
			out_img.set_pixel(r,c,0xFF0000)
		c+=1
	r+=1
out_img.write(outfile)
