# Brian Hamrick
# 10/2/08
# Gaussian Smoothing

#  Input: a pgm or ppm image to be smoothed. The filename
#         should be the first command line argument.
# Output: a pgm (grayscale) image which is the original
#         image after applying Gaussian Smoothing.
#Process: Each pixel is replaced by a weighted average
#         of itself and its 8 neighbors with the weights
#         described to the right   1 2 1
#         where the pixel is in    2 4 2
#         the center of the grid.  1 2 1

import sys
import copy
from pgm import pgm

if len(sys.argv) < 2:
	print 'YOU FAIL: NO INPUT FILE'
	sys.exit(0)

infile = sys.argv[1]
outfile = infile[:-4]+'_smooth.pgm'

img = pgm()
img.read(infile)
outimg = copy.deepcopy(img)

w = img.width
h = img.height

r = 1
while r < h-1:
	c = 1
	while c < w-1:
		outimg.set_pixel(r,c,(img.get_pixel(r-1,c-1)
			+ img.get_pixel(r-1,c+1)
			+ img.get_pixel(r+1,c-1)
			+ img.get_pixel(r+1,c+1)
			+ 2*img.get_pixel(r-1,c)
			+ 2*img.get_pixel(r+1,c)
			+ 2*img.get_pixel(r,c-1)
			+ 2*img.get_pixel(r,c+1)
			+ 4*img.get_pixel(r,c))/16)
		c+=1
	r+=1
outimg.write(outfile)
