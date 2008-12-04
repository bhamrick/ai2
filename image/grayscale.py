# Brian Hamrick
# 9/30/08
# Convert a ppm file to a grayscale pgm file

import sys
import copy

if len(sys.argv) < 2:
	print 'YOU FAIL: NO INPUT FILE'
	sys.exit(0)

inname=sys.argv[1]
outname=inname[:-4]+'.pgm'

fin = open(inname,"r")
fout = open(outname,"w")

line1 = fin.readline()
line2 = fin.readline()
if line2[0]=='#':
	line2 = fin.readline()
line3 = fin.readline()

image = fin.read()
gimage = ''

i = 0
while i+2 < len(image):
	intensity = 0.3*ord(image[i]) + 0.59*ord(image[i+1]) + 0.11*ord(image[i+2])
	gimage += chr(int(intensity))
	i += 3

fout.write('P5\n')
fout.write(line2)
fout.write(line3)
fout.write(gimage)
fin.close()
fout.close()
