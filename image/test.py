import sys
from pgm import pgm

infile = sys.argv[1]
outfile = sys.argv[2]

img = pgm()
img.read(infile)
for r in range(img.height):
	for c in range(img.width):
		img.set_pixel(r,c,img.get_pixel(r,c)/2)
img.write(outfile)
