# Brian Hamrick
# 9/25/08
# Backtracking Constraint Solver
# Input: Three hash maps: domains, assignments, and constraints
#            passed as arguments
#        domains:   Key: a variable
#                 Value: a list of possible values to assign it
#    assignments:   (Empty when called)
#                   Key: a variable which has already been assigned
#                 Value: the value to which the variable is assigned
#    constraints:   Key: a variable, let's say X
#                 Value: a list of pairs (nbr,constraint) where
#                            nbr is another variable and
#                            constraint is a function which evaluates
#                            to true exactly when X and nbr do not have conflicting
#                            assignments when called as constraint(X, X_val, nbr, nbr_val)
# Output: assigments contains a satisfying assignment given the domains and constraints
# Process: recursively check all possible assignments, but use forward checking and
#          at each step attempt to assign a value to the variable with the minimal
#          number of possible values remaining (determined with a linear search).
#          In the event of a tie, this program uses the heuristic that it should choose
#          the variable with the most number of constraints in the constraint list
#          (this corresponds to the degree heuristic for map coloring but not in general)
#          This now implements arc-consistency in the mac function (maintain arc consistency)
#          using the AC-3 algorithm described in the book

import copy

def kill_debug(var,val):
	print 'Killing ' + str(val) + ' from ' + str(var)

def mac(domains,assignments,constraints,dconstraints):
	print 'Entering mac'
	queue=[]
	in_queue={}
	length=0
	for var in domains:
		for nbr,constraint in constraints[var]:
			if nbr in domains:
				queue.append((var,nbr,constraint))
				in_queue[(var,nbr,constraint)]=True
				length=length+1
	while length>0:
		tup = queue.pop(0)
		var1,var2,constraint = tup
		in_queue[tup]=False
		length=length-1
		i = 0
		while i < len(domains[var1]):
			val1 = domains[var1][i]
			for val2 in domains[var2]:
				if constraint(var1,val1,var2,val2):
					i+=1
					break
			else:
#				print 'mac: Killing ' + str(val1) + ' from ' + str(var1)
				kill_debug(var1,val1)
				domains[var1].remove(val1)
				for v in domains:
					for c in dconstraints[v][var1]:
						if not in_queue[(v,var1,c)]:
							queue.append((var1,v,c))
							in_queue[(v,var1,c)]=True
							length=length+1

def backtracking(domains,assignments,constraints):
	for var in assignments:
		val = assignments[var]
		domains[var]=[val]
		for nbr,constraint in constraints[var]:
			for nbr_val in domains[nbr]:
				if not constraint(var,val,nbr,nbr_val):
					domains[nbr].remove(nbr_val)
#					print 'Removing value ' + str(nbr_val) + ' from domain ' + str(nbr)
	killed={}
	dconstraints={}
	for v1 in domains:
		dconstraints[v1]={}
		for v2 in domains:
			dconstraints[v1][v2]=[]
	for var in domains:
		for nbr,constraint in constraints[var]:
			dconstraints[var][nbr].append(constraint)
	mac(domains,assignments,constraints,dconstraints)
	return backtracking_backend(domains,assignments,constraints,dconstraints)

def backtracking_backend(domains, assignments, constraints, dconstraints):
	if len(assignments) == len(domains):
		return True # Everything assigned
	next_var = None
	next_var_domains = -1
	for node in domains:
		if node not in assignments:
			if next_var_domains == -1:
				next_var = node
				next_var_domains = len(domains[next_var])
			elif len(domains[node]) < next_var_domains:
				next_var = node
				next_var_domains = len(domains[next_var])
			elif len(domains[node]) == next_var_domains and len(constraints[node]) > len(constraints[next_var]):
				next_var = node
				next_var_domains = len(domains[next_var])
	if len(domains[next_var])==0:
		return False
	olddomain = copy.copy(domains[next_var])
	olddomains = {}
	for var in domains:
		olddomains[var]=copy.copy(domains[var])
	mac(domains,assignments,constraints,dconstraints)
	for possible_val in olddomain:
		# This loop should not be necessary due to forward checking,
		# but it is still present in order to account for the possibility
		# of nonsymmetric constraints. (However, this would be the fault
		# of the program calling this process)
		for constraint_pair in constraints[next_var]:
			nbr,constraint = constraint_pair
			if nbr not in assignments:
				continue # Can't evaluate constraint
			if not constraint(next_var,possible_val,nbr,assignments[nbr]): # Constraint fail?
				break # This assignment can't work
		else: # If you made it through every constraint
			assignments[next_var]=possible_val
			for constraint_pair in constraints[next_var]:
				nbr,constraint = constraint_pair
				if nbr in assignments:
					continue
				for nbr_val in domains[nbr]:
					if not constraint(next_var,possible_val,nbr,nbr_val):
						domains[nbr].remove(nbr_val)
#						kill_debug(nbr,nbr_val)
#			print 'Assigning ' + str(next_var) + ' ' + str(possible_val)
			if backtracking_backend(domains,assignments,constraints,dconstraints): # Try this assignment
				return True
			else:
				for var in olddomains:
					domains[var]=copy.copy(olddomains[var])
				del assignments[next_var] # NOPE
#	print 'Backtracking' # Failed to find a valid assignment
	return False
