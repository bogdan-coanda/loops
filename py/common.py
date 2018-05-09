from math import floor


class Step (object):
	
	def __init__(self, cc, availablesCount, singlesCount, sparksCount, perm):
		self.cc = cc
		self.availablesCount = availablesCount
		self.singlesCount = singlesCount
		self.sparksCount = sparksCount
		self.perm = perm


class Sol (object):
	
	def __init__(self, tdiff, jkcc, state, text):
		self.tdiff = tdiff
		self.jkcc = jkcc
		self.state = state
		self.text = text
		

def tstr(s):
	return "" + str(int(floor(s / 60))) + "m" + str(int(floor(s)) % 60) + "s." + str(int(s * 1000) % 1000)

def dtstr(new, old):
	if new == old:		
		return "@time: " + tstr(new) + " same as before"
	if new < old:
		return "@time: " + tstr(new) + " faster by " + tstr(old - new) + " (" + str(int(100*new/old)) + "%) than " + tstr(old)
	else:
		return "@time: " + tstr(new) + " slower by " + tstr(new - old) + " (" + str(int(100*old/new)) + "%) than " + tstr(old)
		
def jkstr(new, old):
	if new == old:		
		return "@jkcc: " + str(new) + " same as before"
	if new < old:
		return "@jkcc: " + str(new) + " faster by " + str(old - new) + " (" + str(int(100*new/old)) + "%) than " + str(old)
	else:
		return "@jkcc: " + str(new) + " slower by " + str(new - old) + " (" + str(int(100*old/new)) + "%) than " + str(old)

def sstr(state, diagram = None):
	return " ".join([str(step.cc) + "/" + str(step.availablesCount) + (("(" + str(step.singlesCount) + ")") if step.singlesCount > 0 else (("{" + str(step.sparksCount) + "}") if step.sparksCount > 0 else "")) + ":" + str(step.perm if diagram is None else diagram.nodeByPerm[step.perm]) for step in state])
	
