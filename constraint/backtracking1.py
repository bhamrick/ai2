# Brian Hamrick
# 9/11/08
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

def backtracking(domains,assignments,constraints):
	for var in assignments:
		val = assignments[var]
		for nbr,constraint in constraints[var]:
			for nbr_val in domains[nbr]:
				if not constraint(var,val,nbr,nbr_val):
					domains[nbr].remove(nbr_val)
#					print 'Removing value ' + str(nbr_val) + ' from domain ' + str(nbr)
	return backtracking_backend(domains,assignments,constraints)

def backtracking_backend(domains, assignments, constraints):
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
	for possible_val in domains[next_var]:
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
			killed = {}
			for constraint_pair in constraints[next_var]:
				nbr,constraint = constraint_pair
				if nbr in assignments:
					continue
				killed[nbr]=[]
				for nbr_val in domains[nbr]:
					if not constraint(next_var,possible_val,nbr,nbr_val):
						domains[nbr].remove(nbr_val)
						killed[nbr].append(nbr_val)
#			print 'Assigning ' + str(next_var) + ' ' + str(possible_val)
			if backtracking_backend(domains,assignments,constraints): # Try this assignment
				return True
			else:
				for constraint_pair in constraints[next_var]:
					nbr,constraint = constraint_pair
					if nbr in assignments:
						continue
#					print 'Restoring ' + str(killed[nbr]) + ' to ' + str(nbr)
					domains[nbr] += killed[nbr]
				del assignments[next_var] # NOPE
#	print 'Backtracking' # Failed to find a valid assignment
	return False
