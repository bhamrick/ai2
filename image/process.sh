#/bin/bash
time (time python grayscale.py $1.ppm; time python smooth.py $1.pgm; time python sobel.py ${1}_smooth.pgm $2; time python sobel_color.py ${1}_smooth.pgm $2; time python canny.py ${1}_smooth.pgm $3 $2)
