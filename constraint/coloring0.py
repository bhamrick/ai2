from backtracking1 import *
from copy import copy

def diff_color(A,a,B,b):
	return a!=b

mp={}
domains = {}
constraints = {}
colors=['red','blue','green','purple']
text=open('unitedstates.csv').read().replace('"','').split('\n')[:-1]
for edge in text:
	if ',' in edge:
		a,b = edge.split(',')

		if a not in mp:
			mp[a]=[]
		mp[a]+=[b]
		if b not in mp:
			mp[b]=[]
		mp[b]+=[a]
	else:
		mp[edge]=[] # island
	
for node in mp:
	domains[node]=copy(colors)
	constraints[node]=[]
	for neighbor in mp[node]:
		constraints[node] += [[neighbor,diff_color]]
	
assignments = {}
backtracking(domains,assignments,constraints)

print
for node in mp.keys():
	print node+': ' + ', '.join(mp[node])
	print assignments[node]+': '+', '.join([assignments[n] for n in mp[node]])
	print

