# Brian Hamrick
# 9/11/08
# N-Queens program using the constraint solver

import sys
from backtracking1 import backtracking

def constraint(row1, col1, row2, col2):
	# Precondition: col1 != col2
	return col1 != col2 and col1+row1 != col2+row2 and col1-row1 != col2-row2

def disp(n, assignments):
	str = ""
	for row in range(n):
		for col in range(n):
			if ((row+col)&1)==0:
				str += "\033[43;31;1m"
			else:
				str += "\033[46;31;1m"
			if col == assignments[row]:
				str += "Q"
			else:
				str += " "
			str+="\033[0m"
		str += "\n"
	str += "\033[0m"
	print str


n = 8
if len(sys.argv) > 1:
	n = int(sys.argv[1])

domains = {}
assignments = {}
constraints = {}

for i in range(n):
	domains[i]=range(n)

for i in range(n):
	for j in range(n):
		if i != j:
			if not i in constraints:
				constraints[i]=[]
			constraints[i].append((j,constraint))

backtracking(domains,assignments,constraints)

disp(n,assignments)
