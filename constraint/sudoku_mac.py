# Brian Hamrick
# 9/11/08
# Sudoku using constraint solver

import sys
from arccons import backtracking

if len(sys.argv) > 1:
	str_form = sys.argv[1]
else:
	sys.exit(0)

def constraint(loc1, val1, loc2, val2):
	return val1 != val2

domains = {}
assignments = {}
constraints = {}

for i in range(9):
	for j in range(9):
		domains[(i,j)]=[1,2,3,4,5,6,7,8,9]
		constraints[(i,j)]=[]
		for k in range(9):
			for l in range(9):
				if k==i and l==j:
					continue
				if k==i or l==j or (k/3==i/3 and l/3==j/3):
					constraints[(i,j)].append(((k,l),constraint))

for i in range(9):
	for j in range(9):
		if str_form[9*i+j]!='.':
			assignments[(i,j)]=int(str_form[9*i+j])

if not backtracking(domains, assignments, constraints):
	print 'No solution found'
	sys.exit(0)

output = ''
for i in range(9):
	for j in range(9):
		output+=str(assignments[(i,j)])
	output+='\n'
print output
