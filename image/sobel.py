# Brian Hamrick
# 10/9/08
# Sobel Method of edge detection
# Input: A filename of either a pgm or a ppm file (it will convert to grayscale automatically)
# Output: A black and white pgm file marking whether or not a pixel was an edge in the original image.
#         This version does _not_ include the original image underneath the edges
# Process: Consider a sort of gradient defined by applying two weighted averages to the intensities with the following masks:
#               1 0 -1        1  2  1
#          gx = 2 0 -2  gy =  0  0  0
#               1 0 -1       -1 -2 -1
#          If the sum |gx| + |gy| is above a set threshold (default 300), then the pixel is marked as an edge.

import sys
import copy
from pgm import pgm

threshold = 300

if len(sys.argv) < 2:
	print 'YOU FAIL: NO INPUT FILE'
	sys.exit(0)

infile = sys.argv[1]
outfile = infile[:-4] + '_edge.pgm'

img = pgm()
img.read(infile)
out_img = copy.deepcopy(img)

if len(sys.argv) >= 3:
	threshold = int(sys.argv[2])

r = 1
while r < img.height-1:
	c = 1
	while c < img.width-1:
		gx = img.get_pixel(r-1,c+1) + 2*img.get_pixel(r,c+1) + img.get_pixel(r+1,c+1) - img.get_pixel(r-1,c-1) - 2*img.get_pixel(r,c-1) - img.get_pixel(r+1,c-1)
		gy = img.get_pixel(r+1,c-1) + 2*img.get_pixel(r+1,c) + img.get_pixel(r+1,c+1) - img.get_pixel(r-1,c-1) - 2*img.get_pixel(r-1,c) - img.get_pixel(r-1,c+1)
		if abs(gx) + abs(gy) > threshold:
			out_img.set_pixel(r,c,0)
		else:
			out_img.set_pixel(r,c,255)
		c+=1
	r+=1
out_img.write(outfile)
