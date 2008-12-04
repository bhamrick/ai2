from random import choice,shuffle

def backtracking(domains, assignments, constraints):
	if len(assignments) == len(domains):
		return True # Everything assigned
	next_var = choice([node for node in domains if node not in assignments]) # Choose a domain to assign
	shuffle(domains[next_var])
	for possible_val in domains[next_var]:
		for constraint_pair in constraints[next_var]:
			nbr,constraint = constraint_pair
			if nbr not in assignments:
				continue # Can't evaluate constraint
			if not constraint(next_var,possible_val,nbr,assignments[nbr]): # Constraint fail?
				break # This assignment can't work
		else: # If you made it through every constraint
			assignments[next_var]=possible_val
			if backtracking(domains,assignments,constraints): # Try this assignment
				return True
			else:
				del assignments[next_var] # NOPE
#	print 'Backtracking' # Failed to find a valid assignment
	return False
