from diagram import *
from time import time, sleep
from math import floor
import pickle
import shutil
from functools import cmp_to_key
import traceback

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

def sstr(state):
	return " ".join([str(step.cc) + "/" + str(step.availablesCount) + (("(" + str(step.singlesCount) + ")") if step.singlesCount > 0 else (("{" + str(step.sparksCount) + "}") if step.sparksCount > 0 else "")) + ":" + str(step.perm) for step in state])

def jk(diagram, lvl = 0, state = []):
	
	diagram.jkcc += 1	

	diagram.measureNodes()

	if diagram.rx_looped_count == len(diagram.perms) and len(diagram.drawn.availables) == 0:
			
		tdiff = time() - diagram.startTime
		text = "[" + str(len(diagram.sols)) + "] lvl: " + str(lvl) + " | " +  sstr(state)

		if len(diagram.drawn.chains) != 1:
			#print("\n# [Trojan] # @jkcc: " + str(diagram.jkcc) + " | @time: " + tstr(tdiff) + " » " + text)
			return
		diagram.sols.append(Sol(tdiff, diagram.jkcc, state, text))		

		print()
		print("[state] jk: " + str(diagram.jkcc) + " | lvl: " + str(lvl) + " | » " + sstr(state))
		print("[drawn] looped: " + str(diagram.rx_looped_count) + " | availables: " + str(len(diagram.drawn.availables)) + " | singles: " + str(len(diagram.drawn.singles)) + " | sparks: " + str(len(diagram.drawn.sparks)) + " | unreachable: " + str(len(diagram.drawn.unreachable_cycles)) + " | chains: " + " ".join([str(ch) for ch in diagram.drawn.chains]) + " | connected chains: " + " ".join([str(a) + "+" + str(b) for a, b in diagram.connectedChainPairs if a < b]) + " | chain starters: " + " ".join([str(node) for node in diagram.chainStarters]))					
															
		print()																												
		print("\n# Found # @jkcc: " + str(diagram.jkcc) + " | @time: " + tstr(tdiff) + " » " + text)
		print()
				
		if len(diagram.sols) > len(diagram.knowns):
			with open("sols."+str(diagram.spClass)+".pkl.tmp", 'wb') as outfile:
				try:
					pickle.dump(diagram.sols, outfile, 0)
					shutil.move("sols."+str(diagram.spClass)+".pkl.tmp", "sols."+str(diagram.spClass)+".pkl")
				except:
					traceback.print_exc()
					raise 
			print("[NEW]")
					
		else: # len(diagram.sols) <= len(diagram.knowns):
			known = diagram.knowns[len(diagram.sols) - 1]
			sol = diagram.sols[-1]			
			if known.jkcc == sol.jkcc and known.text == sol.text: # jkcc & text
				print("[SAME] " + dtstr(sol.tdiff, known.tdiff))
			else:
				knownchain = [step.perm for step in known.state]
				solchain = [step.perm for step in sol.state]
				if set(knownchain) == set(solchain):
					if knownchain == solchain:
						print(">>> [ABSOLUTED] <<<\n" + dtstr(sol.tdiff, known.tdiff) + "\n" + jkstr(sol.jkcc, known.jkcc) + "\nold » " + " ".join([str(node) for node in knownchain]) + "\nnew » " + " ".join([str(node) for node in knownchain]))
					else:
						print(">>> [REORDERED] <<<\n" + dtstr(sol.tdiff, known.tdiff) + "\n" + jkstr(sol.jkcc, known.jkcc) + "\nold » " + " ".join([str(node) for node in knownchain]) + "\nnew » " + " ".join([str(node) for node in solchain]))
				else:
					𝒟 = Diagram(diagram.spClass)
					for step in known.state:
						𝒟.measureNodes()
						node = 𝒟.nodeByPerm[step.perm]
						#print("𝒟:" + str(𝒟.drawn.looped_count) + " | extending: " + str(node))
						𝒟.extendLoop(node)
						
					np = diagram.startNode
					op = 𝒟.startNode
					pc = 0
					while True:
						if np.perm != op.perm:
							print("[" + str(pc) + "] diverges at " + str(np) + " | " + str(op) + " from " + str(np.prevLink.node) + " | " + str(op.prevLink.node))
							print(">>> !!![DIVERGENT]!!! <<<\n" + dtstr(sol.tdiff, known.tdiff) + "\n" + jkstr(sol.jkcc, known.jkcc) + "\nold » " + known.text + "\nnew » " + sol.text)			
							assert False
						else:
							np = np.nextLink.next
							op = op.nextLink.next
							if np == diagram.startNode:
								print("converges...")
								print(">>> [CONVERGENT] <<<\n" + dtstr(sol.tdiff, known.tdiff) + "\n" + jkstr(sol.jkcc, known.jkcc) + "\nold » " + known.text + "\nnew » " + sol.text)				
								return
						pc += 1
								
		return
					
	if len(diagram.drawn.unreachable_cycles) > 0:
#		diagram.log("lvl:"+str(lvl), "popping for unreachables: " + str(len(diagram.drawn.unreachable_cycles)))
		return
		
	singlesCount = len(diagram.drawn.singles)
	sparksCount = len(diagram.drawn.sparks)
	# [~] if sparks then start new chain
	# take linkedChains(a,b) into account when measuring bros
	if singlesCount > 0:
		availables = [sorted(diagram.drawn.singles, key = cmp_to_key(lambda x, y: 0 if x.perm == y.perm else (1 if x.perm > y.perm else -1)))[0]]
#		diagram.log("lvl:"+str(lvl)+"|singles", " ".join([str(node) for node in diagram.drawn.singles]))
	elif sparksCount > 0:		
		availables = [sorted(diagram.drawn.sparks, key = cmp_to_key(lambda x, y: 0 if x.perm == y.perm else (1 if x.perm > y.perm else -1)))[0]]
#		diagram.log("lvl:"+str(lvl)+"|sparks", " ".join([str(node) for node in diagram.drawn.sparks]))
	else:
		availables = diagram.drawn.availables
#		diagram.log("lvl:"+str(lvl)+"|availables", " ".join([str(node) for node in diagram.drawn.availables]))
		
	availables = [node for node in availables if not node.loop.seen]
	lvl_seen = []		
	cc = 0

	for node in availables:
						
		if diagram.extendLoop(node):
#				diagram.log("lvl:"+str(lvl), "pushing by " + str(node))
			jk(diagram, lvl + 1, state + [Step(cc, len(availables), singlesCount, sparksCount, node.perm)])
#				diagram.log("lvl:"+str(lvl), "collapsing back " + str(node))
			diagram.collapseLoop(node)
				
			node.loop.seen = True
			lvl_seen.append(node)				
		cc += 1
		
	for node in lvl_seen:
		node.loop.seen = False
#	diagram.log("lvl:"+str(lvl), "popping normally")
	return			


def jkinit(diagram):
	diagram.startTime = time()
	diagram.sols = []
	diagram.knowns = []
	
	# with open('sols.'+str(diagram.spClass)+".pkl", 'wb') as outfile:
	# 	pickle.dump(diagram.sols, outfile, 0)

	with open('sols.'+str(diagram.spClass)+".pkl", 'rb') as infile:
		diagram.knowns = pickle.load(infile)
		
	for i in range(len(diagram.knowns)):
		if type(diagram.knowns[i]) is tuple:
			diagram.knowns[i] = Sol(diagram.knowns[i][0], diagram.knowns[i][1], [Step(step[0], step[1], step[2], 0, step[3]) for step in diagram.knowns[i][2]], diagram.knowns[i][3])
			
	print("[jk:init] knowns: " + str(len(diagram.knowns)))
	
def run():
	diagram = Diagram(6)
			
	jkinit(diagram)
	jk(diagram)
	
	print("=== §§§ ===")

	
if __name__ == "__main__":
	run()


