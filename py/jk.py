from diagram import *
from time import time
from math import floor
import pickle
from functools import cmp_to_key

class Step (object):
	
	def __init__(self, cc, availablesCount, singlesCount, sparksCount, node):
		self.cc = cc
		self.availablesCount = availablesCount
		self.singlesCount = singlesCount
		self.sparksCount = sparksCount
		self.node = node


class Sol (object):
	
	def __init__(self, tdiff, jkcc, state, text, extended):
		self.tdiff = tdiff
		self.jkcc = jkcc
		self.state = state
		self.text = text
		self.extended = extended
		

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

def sstr(state):
	return " ".join([str(step.cc) + "/" + str(step.availablesCount) + (("(" + str(step.singlesCount) + ")") if step.singlesCount > 0 else (("{" + str(step.sparksCount) + "}") if step.sparksCount > 0 else "")) + ":" + str(step.node) for step in state])

def jk(diagram, lvl = 0, state = []):
	
	diagram.jkcc += 1	

	diagram.measureNodes()

	print()
	print("[state] jk: " + str(diagram.jkcc) + " | lvl: " + str(lvl) + " | » " + sstr(state))
	print("[drawn] looped: " + str(diagram.drawn.looped_count) + " | availables: " + str(len(diagram.drawn.availables)) + " | singles: " + str(len(diagram.drawn.singles)) + " | sparks: " + str(len(diagram.drawn.sparks)) + " | unreachable: " + str(diagram.drawn.unreachable_cycle_count) + " | connected chains: " + " ".join([str(a) + "+" + str(b) for a, b in diagram.connectedChainPairs if a < b]) + " | chain starters: " + " ".join([str(node) for node in diagram.chainStarters]))
				
	if diagram.drawn.looped_count == len(diagram.perms):
		tdiff = time() - diagram.startTime
		text = "[" + str(len(diagram.sols)) + "] lvl: " + str(lvl) + " | " +  sstr(state)
		extended = [step.node for step in state]
		diagram.sols.append(Sol(tdiff, diagram.jkcc, state, text, extended))
		print("\n# Found # @jkcc: " + str(diagram.jkcc) + " | @time: " + tstr(tdiff) + " » " + text)
		
		if len(diagram.sols) > len(diagram.knowns):
			with open("sols."+str(diagram.spClass)+".pkl", 'wb') as outfile:
				pickle.dump(diagram.sols, outfile, 0)
			print("[NEW]")
					
		else: # len(diagram.sols) <= len(diagram.knowns):
			known = diagram.knowns[len(diagram.sols) - 1]
			sol = diagram.sols[-1]			
			if known.jkcc == sol.jkcc and known.text == sol.text: # jkcc & text
				print("[SAME] " + dtstr(sol.tdiff, known.tdiff))
			else:
				knownchain = [step.node for step in known.state]
				solchain = [step.node for step in sol.state]
				if set(knownchain) == set(solchain):
					if knownchain == solchain:
						print(">>> [ABSOLUTED] <<<\n" + dtstr(sol.tdiff, known.tdiff) + "\n" + jkstr(sol.jkcc, known.jkcc) + "\nold » " + " ".join([str(node) for node in knownchain]) + "\nnew » " + " ".join([str(node) for node in knownchain]))
					else:
						print(">>> [REORDERED] <<<\n" + dtstr(sol.tdiff, known.tdiff) + "\n" + jkstr(sol.jkcc, known.jkcc) + "\nold » " + " ".join([str(node) for node in knownchain]) + "\nnew » " + " ".join([str(node) for node in solchain]))
				else:
					print(">>> !!![DIVERGENT]!!! <<<\n" + dtstr(sol.tdiff, known.tdiff) + "\n" + jkstr(sol.jkcc, known.jkcc) + "\nold » " + known.text + "\nnew » " + sol.text)
					assert False
		
		return
					
	if diagram.drawn.unreachable_cycle_count > 0:
		print("[lvl:"+str(lvl)+"] popping for unreachables: " + str(diagram.drawn.unreachable_cycle_count))
		return
		
	singlesCount = len(diagram.drawn.singles)
	sparksCount = len(diagram.drawn.sparks)
	# [~] if sparks then start new chain
	# take linkedChains(a,b) into account when measuring bros
	if singlesCount > 0:
		availables = [sorted(diagram.drawn.singles, key = cmp_to_key(lambda x, y: 0 if x.perm == y.perm else (1 if x.perm > y.perm else -1)))[0]]
		print("[singles] " + " ".join([node.perm for node in diagram.drawn.singles]))
	elif sparksCount > 0:		
		availables = [sorted(diagram.drawn.sparks, key = cmp_to_key(lambda x, y: 0 if x.perm == y.perm else (1 if x.perm > y.perm else -1)))[0]]
		print("[sparks] " + " ".join([node.perm for node in diagram.drawn.sparks]))
	else:
		availables = diagram.drawn.availables
		print("[availables] " + " ".join([node.perm + "§" + str(node.chainID) for node in diagram.drawn.availables]))
		
	availables = [node for node in availables if not node.seen]
	
	lvl_seen = []
			
	# if diagram.jkcc == 9:
	# 	assert False, "jk: " + str(diagram.jkcc)		
		
	cc = 0

	for node in availables:
		if not node.seen:				
			
			diagram.measureNodes()
			lastDrawn = diagram.drawn.clone()
			
			if diagram.extendLoop(node):
				print("[lvl:"+str(lvl)+"] pushing by " + node.perm)
				jk(diagram, lvl + 1, state + [Step(cc, len(availables), singlesCount, sparksCount, node)])
				print("[lvl:"+str(lvl)+"] collapsing back " + node.perm)
				diagram.collapseLoop(node)
				
				diagram.measureNodes()
				assert lastDrawn == diagram.drawn, str(lastDrawn.looped_count) + " » " + str(diagram.drawn.looped_count)
		
			node.seen = True
			for bro in node.loopBrethren:
				bro.seen = True
			lvl_seen.append(node)				
		cc += 1
		
	for node in lvl_seen:
		node.seen = False
		for bro in node.loopBrethren:
			bro.seen = False
	print("[lvl:"+str(lvl)+"] popping normally")
	return			




if __name__ == "__main__":
	
	diagram = Diagram(6)
	diagram.startTime = time()
	diagram.sols = []
	
	# with open('sols.'+str(diagram.spClass)+".pkl", 'wb') as outfile:
	# 	pickle.dump(diagram.sols, outfile, 0)

	with open('sols.'+str(diagram.spClass)+".pkl", 'rb') as infile:
		diagram.knowns = pickle.load(infile)

	print("knowns: " + str(len(diagram.knowns)))
			
	jk(diagram)
	print("---")


