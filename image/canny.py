# Brian Hamrick
# 10/16/08
# Canny Method of edge detection
# Input: A grayscale pgm image which is already smoothed as a command line argument
# Output: A color ppm image which has the original image in grayscale but with edges replaced
#         by pure red. (0xFF0000)
# Process: Compute Gx and Gy the same way as the sobel method. For pixels for which |Gx|+|Gy| exceeds the high threshold value,
#          mark them as edges. For each of these, move in the <-Gy,Gx> direction (parallel to the edge) in both directions.
#          If these pixels' |Gx|+|Gy| value meets the low threshold, mark them as edges. Then, recalculate the direction
#          based on this new edge. By continuing this, we obtain the final set of edge pixels.
# Note: The files pgm.py and ppm.py are not printed for brevity, but they have been printed out for previous assignments.

import sys
import copy
from pgm import pgm
from ppm import ppm

high_threshold = 400
low_threshold = 200

if len(sys.argv) < 2:
	print 'YOU FAIL: NO INPUT FILE'
	sys.exit(0)

infile = sys.argv[1]
outfile = infile[:-4] + '_canny.ppm'

img = pgm()
img.read(infile)
out_img = ppm()
out_img.read(infile)
edges = pgm()
edges.read(infile)

def grad(img, r, c):
	if r <= 0 or c <= 0 or r >= img.height-1 or c >= img.width-1:
		return (0,0)
	gx = img.get_pixel(r-1,c+1) + 2*img.get_pixel(r,c+1) + img.get_pixel(r+1,c+1) - img.get_pixel(r-1,c-1) - 2*img.get_pixel(r,c-1) - img.get_pixel(r+1,c-1)
	gy = img.get_pixel(r+1,c-1) + 2*img.get_pixel(r+1,c) + img.get_pixel(r+1,c+1) - img.get_pixel(r-1,c-1) - 2*img.get_pixel(r-1,c) - img.get_pixel(r-1,c+1)
	return (gx,gy)

if len(sys.argv) >= 3:
	high_threshold = int(sys.argv[2])

if len(sys.argv) >= 4:
	low_threshold = int(sys.argv[3])

queue = []

r = 1
while r < img.height-1:
	c = 1
	while c < img.width-1:
		gx = img.get_pixel(r-1,c+1) + 2*img.get_pixel(r,c+1) + img.get_pixel(r+1,c+1) - img.get_pixel(r-1,c-1) - 2*img.get_pixel(r,c-1) - img.get_pixel(r+1,c-1)
		gy = img.get_pixel(r+1,c-1) + 2*img.get_pixel(r+1,c) + img.get_pixel(r+1,c+1) - img.get_pixel(r-1,c-1) - 2*img.get_pixel(r-1,c) - img.get_pixel(r-1,c+1)
		if abs(gx) + abs(gy) > high_threshold:
			edges.set_pixel(r,c,1)
			queue.append((r,c))
		else:
			edges.set_pixel(r,c,0)
		c+=1
	r+=1

while len(queue) > 0:
	r,c = queue.pop(0)
	gx, gy = grad(img, r, c)
	if gy == 0:
		tang = 0
	else:
		tang = -float(gx)/gy
	if gx == 0:
		norm = 0
	else:
		norm = float(gy)/gx
	
	# rounding sin(pi/8) = 0.382
	if norm > 0.382:
		norm = 1
	elif norm < -0.382:
		norm = -1
	else:
		norm = 0
	# end rounding

	r1,c1 = r+1,int(c+norm)
	gx1, gy1 = grad(img,r1,c1)
	if(abs(gx1)+abs(gy1) > abs(gx) + abs(gy)):
		continue

	r1,c1 = r-1,int(c-norm)
	gx1, gy1 = grad(img,r1,c1)
	if(abs(gx1)+abs(gy1) > abs(gx) + abs(gy)):
		continue

	# rounding sin(pi/8) = 0.382
	if tang > 0.382:
		tang = 1
	elif tang < -0.382:
		tang = -1
	else:
		tang = 0
	# end rounding

	r1,c1 = r+1,int(c+tang)
	gx1, gy1 = grad(img,r1,c1)
	if edges.get_pixel(r1,c1)==0 and abs(gx1) + abs(gy1) > low_threshold:
		edges.set_pixel(r1,c1,1)
		queue.append((r1,c1))
	
	r1,c1 = r-1,int(c-tang)
	gx1, gy1 = grad(img,r1,c1)
	if edges.get_pixel(r1,c1)==0 and abs(gx1) + abs(gy1) > low_threshold:
		edges.set_pixel(r1,c1,1)
		queue.append((r1,c1))

for r in range(img.height):
	for c in range(img.width):
		if edges.get_pixel(r,c) == 1:
			out_img.set_pixel(r,c,0xFF0000)

out_img.write(outfile)
