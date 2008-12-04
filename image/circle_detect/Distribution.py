# Brian Hamrick
# 10/9/08
# FILE: Distribution.py
# Statistics for lists of numbers

import math

def mean(l):
	tot = 0
	for i in l:
		tot+=i
	return float(tot)/len(l)

def rms(l):
	tot = 0
	for i in l:
		tot+=i*i
	return math.sqrt(float(tot)/len(l))

def stddev(l):
	mu = mean(l)
	tot = 0
	for i in l:
		tot+=(i-mu)*(i-mu)
	return math.sqrt(float(tot)/len(l))

def median(l):
	sl = sorted(l)
	if (len(sl)/2)*2 == len(sl):
		return (sl[len(sl)/2-1]+sl[len(sl)/2])/2
	else:
		return sl[len(sl)/2]

def q1(l):
	sl = sorted(l)
	return sl[len(sl)/4]

def q3(l):
	sl = sorted(l)
	return sl[3*len(sl)/4]

def remove_outliers(l):
	ans = []
	fq = q1(l)
	tq = q3(l)
	qr = tq-fq
	med = median(l)
	for i in l:
		if 2*abs(i-med) < 3*qr:
			ans.append(i)
	return ans
