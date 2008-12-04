# Brian Hamrick
# 10/16/08
# Ellipse detection

import sys
import copy
from math import *
from pgm import pgm
from ppm import ppm

high_threshold = 400
low_threshold = 200

if len(sys.argv) < 2:
	print 'YOU FAIL: NO INPUT FILE'
	sys.exit(0)

infile = sys.argv[1]
outfile = infile[:-4] + '_ellipses.pgm'

img = pgm()
img.read(infile)
edges = pgm()
edges.read(infile)
tmp_img = pgm()
tmp_img.read(infile)
tmpfile = infile[:-4] + '_space.pgm'
outimg = pgm()
outimg.read(infile)

for r in range(outimg.height):
	for c in range(outimg.width):
		outimg.set_pixel(r,c,255)

# Parameterize ellipses as <r,c> = <rc,cc> + <a*cos(theta+phi),b*sin(theta+phi)>

amin = 5
amax = max(img.width,img.height)
agran = 1
bmin = 5
bmax = max(img.width,img.height)
bgran = 1
thetamin = 0
thetamax = 2*pi
thetagran = pi/10

counts = {}

counts_threshold = 5

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

count_threshold=15
possible_ellipses=[]
a = amin
while a <= amax:
	b = bmin
	while b<=bmax:
		counts={}
		for r in range(edges.height):
			for c in range(edges.width):
				if edges.get_pixel(r,c) == 1:
					theta = thetamin
					while theta < thetamax:
						rc=(int(r-a*sin(theta)))
						cc=(int(c-b*cos(theta)))
						tup=(rc,cc,a,b)
						if tup in counts:
							counts[tup]+=1
						else:
							counts[tup]=1
						theta+=thetagran
		for tup in counts:
			if counts[tup]>count_threshold:
				possible_ellipses.append(tup)
		b+=bgran
	a+=agran

print possible_ellipses

vis={}
is_possible_ellipse={}
for tup in possible_ellipses:
	is_possible_ellipse[tup]=True
ellipses=[]

for tup in possible_ellipses:
	if vis.get(tup,False):
		continue
	rtot, ctot, atot, btot = 0,0,0,0
	n = 0
	q = [tup]
	while len(q) > 0:
		t = q.pop(0)
		if vis.get(t,False):
			continue
		vis[t]=True
		r,c,a,b = t
		rtot+=r
		ctot+=c
		atot+=a
		btot+=b
		n+=1
		t1 = (r+1,c,a,b)
		if is_possible_ellipse.get(t1,False):
			q.append(t1)
		t1 = (r,c+1,a,b)
		if is_possible_ellipse.get(t1,False):
			q.append(t1)
		t1 = (r,c,a+1,b)
		if is_possible_ellipse.get(t1,False):
			q.append(t1)
		t1 = (r,c,a,b+1)
		if is_possible_ellipse.get(t1,False):
			q.append(t1)
		t1 = (r-1,c,a,b)
		if is_possible_ellipse.get(t1,False):
			q.append(t1)
		t1 = (r,c-1,a,b)
		if is_possible_ellipse.get(t1,False):
			q.append(t1)
		t1 = (r,c,a-1,b)
		if is_possible_ellipse.get(t1,False):
			q.append(t1)
		t1 = (r,c,a,b-1)
		if is_possible_ellipse.get(t1,False):
			q.append(t1)
	if n > 0:
		ellipses.append((rtot/n,ctot/n,atot/n,btot/n))

print ellipses		

for ellipse in ellipses:
	r, c, a, b = ellipse
	theta = 0
	while theta < 2*pi:
		outimg.set_pixel(int(r+a*sin(theta)),int(c+b*cos(theta)),0)
		theta+=pi/1000
outimg.write(outfile)
