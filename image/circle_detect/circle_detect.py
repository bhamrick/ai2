# Brian Hamrick
# 10/23/08
# Circle detection
# Input  : A grayscale pgm image supplied as a command line argument
# Output : Three grayscale pgm images. The first, *_centers.pgm
#          displays the normal lines traced out with dark spots at
#          likely centers. The second, *_probs.pgm uses a heuristic
#          of the standard deviation of the radii from a point
#          to reduce the number of possible centers. The third, *_circles.pgm
#          draws the most likely circles on a blank image (darker = more likely)
# Process: First, the canny method of edge detection is run. Then,
#          using the gradient approximations, a line is drawn normal to each edge
#          at each pixel on the edge. After that, *_centers.pgm can be written.
#          Then, using the aforementioned standard deviation heuristic, the
#          possible centers are thinned out. Finally, by floodfilling on the
#          resulting image with a preset threshold and averaging, the final
#          choices of centers are found. Then, taking the mean of the possible
#          radii from that center yields the radius drawn on the image.

import sys
import copy
import math
import Distribution
from pgm import pgm
from ppm import ppm

high_threshold = 400
low_threshold = 200

center_threshold = 220
prob_threshold = 100

if len(sys.argv) < 2:
	print 'YOU FAIL: NO INPUT FILE'
	sys.exit(0)

infile = sys.argv[1]
outfile = infile[:-4] + '_centers.pgm'
probfile = infile[:-4] + '_probs.pgm'
circlefile = infile[:-4] + '_circles.pgm'

img = pgm()
img.read(infile)
out_img = ppm()
out_img.read(infile)
centers = pgm()
centers.read(infile)
edges = pgm()
edges.read(infile)

radii={}

for r in range(centers.height):
	radii[r] = {}
	for c in range(centers.width):
		radii[r][c] = []
		centers.set_pixel(r,c,255)

probs = copy.deepcopy(centers)
circles = copy.deepcopy(centers)

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

for r in range(1,img.height-1):
	for c in range(1,img.width-1):
		if edges.get_pixel(r,c) == 1:
			gx, gy = grad(img,r,c)
			g = abs(gx) + abs(gy)
			gx = float(gx) / g
			gy = float(gy) / g
			r2, c2 = r,c
			while r2 >= 0 and c2 >= 0 and r2 <= img.height-1 and c2 <= img.width-1:
				centers.set_pixel(int(r2),int(c2),max(0,centers.get_pixel(int(r2),int(c2))-1))
				radii[int(r2)][int(c2)].append(math.sqrt((r2-r)*(r2-r)+(c2-c)*(c2-c)))
				oldr2, oldc2 = r2,c2
				while (int(oldr2),int(oldc2)) == (int(r2),int(c2)):
					r2 = r2+gy
					c2 = c2+gx
			r2, c2 = r-gy,c-gx
			while r2 >= 0 and c2 >= 0 and r2 <= img.height-1 and c2 <= img.width-1:
				centers.set_pixel(int(r2),int(c2),max(0,centers.get_pixel(int(r2),int(c2))-1))
				radii[int(r2)][int(c2)].append(math.sqrt((r2-r)*(r2-r)+(c2-c)*(c2-c)))
				oldr2, oldc2 = r2,c2
				while (int(oldr2),int(oldc2)) == (int(r2),int(c2)):
					r2 = r2-gy
					c2 = c2-gx

visited = copy.deepcopy(circles)

for r in range(1,img.height-1):
	for c in range(1,img.width-1):
		circles.set_pixel(r,c,-1)
		visited.set_pixel(r,c,0)

for r in range(1,img.height-1):
	for c in range(1,img.width-1):
		if centers.get_pixel(r,c) < center_threshold:
			probs.set_pixel(r,c,min(int(centers.get_pixel(r,c)*Distribution.stddev(Distribution.remove_outliers(radii[r][c]))),255))
		else:
			probs.set_pixel(r,c,255)

final_centers = []
for r in range(1,img.height-1):
	for c in range(1,img.width-1):
		if probs.get_pixel(r,c) < prob_threshold:
			if visited.get_pixel(r,c)!=0:
				continue
			queue = []
			queue.append((r,c))
			rtot, ctot = 0,0
			num = 0
			while len(queue) > 0:
				r2,c2 = queue.pop(0)
				if visited.get_pixel(r2,c2)!=0:
					continue
				visited.set_pixel(r2,c2,1)
				rtot += r2
				ctot += c2
				num += 1
				if probs.get_pixel(r2+1,c2) < prob_threshold:
					queue.append((r2+1,c2))
				if probs.get_pixel(r2-1,c2) < prob_threshold:
					queue.append((r2-1,c2))
				if probs.get_pixel(r2,c2+1) < prob_threshold:
					queue.append((r2,c2+1))
				if probs.get_pixel(r2,c2-1) < prob_threshold:
					queue.append((r2,c2-1))
				if probs.get_pixel(r2+1,c2+1) < prob_threshold:
					queue.append((r2+1,c2+1))
				if probs.get_pixel(r2+1,c2-1) < prob_threshold:
					queue.append((r2+1,c2-1))
				if probs.get_pixel(r2-1,c2+1) < prob_threshold:
					queue.append((r2-1,c2+1))
				if probs.get_pixel(r2-1,c2-1) < prob_threshold:
					queue.append((r2-1,c2-1))
			visited.set_pixel(rtot/num,ctot/num,2)
			if num >= 4:
				final_centers.append((rtot/num,ctot/num))

while len(final_centers) > 0:
	r, c = final_centers.pop(0)
	rad = Distribution.mean(Distribution.remove_outliers(radii[r][c]))
	p = probs.get_pixel(r,c)
	for i in range(1000):
		circles.set_pixel(int(r+rad*math.sin(2*math.pi*i/1000)),int(c+rad*math.cos(2*math.pi*i/1000)),p)

for r in range(1,img.height-1):
	for c in range(1,img.width-1):
		if circles.get_pixel(r,c)==-1:
			circles.set_pixel(r,c,255)

centers.write(outfile)
probs.write(probfile)
circles.write(circlefile)
