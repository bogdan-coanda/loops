from diagram import *
from time import time, sleep
from math import floor
import pickle
import shutil
from functools import cmp_to_key
import traceback
from common import *


def jk(diagram, lvl = 0, state = [], last_extended_node = None):
	
	diagram.jkcc += 1	

	if len(diagram.mx_singles) > 0:
		availables = [sorted(diagram.mx_singles, key = cmp_to_key(lambda x, y: 0 if x.perm == y.perm else (1 if x.perm > y.perm else -1)))[0]]
		is_normal = False

	elif len(diagram.mx_sparks) > 0:
		availables = [sorted(diagram.mx_sparks, key = cmp_to_key(lambda x, y: 0 if x.perm == y.perm else (1 if x.perm > y.perm else -1)))[0]]
		is_normal = False

	else:
		
		diagram.measureNodes(last_extended_node or diagram.startNode)
		#jkprintstate(diagram, lvl, state)
				
		if diagram.rx_looped_count == len(diagram.perms) and len(diagram.drawn.availables) == 0:			
			if len(diagram.drawn.chains) != 1:
				#print("\n# [Trojan] # @jkcc: " + str(diagram.jkcc) + " | @time: " + tstr(tdiff) + " » " + text)
				return
				
			tdiff = time() - diagram.startTime
			text = "[" + str(len(diagram.sols)) + "] lvl: " + str(lvl) + " | " +  sstr(state)
			
			diagram.sols.append(Sol(tdiff, diagram.jkcc, state, text))				
			jkprintstate(diagram, lvl, state)
			jkprintsol(diagram)								
			return
							
		availables = diagram.drawn.availables
		is_normal = True
		#diagram.log("lvl:"+str(lvl)+"|availables", " ".join([str(node) for node in diagram.drawn.availables]))
		
	lvl_seen = []		
	cc = 0

	for node in availables:
									
		if diagram.extendLoop(node):
			#diagram.log("lvl:"+str(lvl), "pushing by " + str(node))
			if len(diagram.mx_unreachable_cycles) == 0: # we don't bother pushing just to come back
				jk(diagram, 
						lvl + 1, 
						state + [Step(cc, len(availables), len(diagram.mx_singles), len(diagram.mx_sparks), node.perm)],
						node if is_normal and node.chainID == 0 else last_extended_node
					)
			#diagram.log("lvl:"+str(lvl), "collapsing back " + str(node))
			diagram.collapseLoop(node)
				
			#assert node.loop.availabled
			node.loop.availabled = False
			for nn in node.loop.nodes:
				nn.cycle.available_loops_count -= 1
			lvl_seen.append(node)				
		cc += 1
		
	for node in lvl_seen:
		node.loop.availabled = True
		for nn in node.loop.nodes:
			nn.cycle.available_loops_count += 1					
										
	#diagram.log("lvl:"+str(lvl), "popping normally")
	#return			


def jkprintstate(diagram, lvl, state):
	print()
	print("[state] jk: " + str(diagram.jkcc) + " | lvl: " + str(lvl) + " | » " + sstr(state))
	print("[drawn] looped: " + str(diagram.rx_looped_count) + " | availables: " + str(len(diagram.drawn.availables)) + " | singles: " + str(len(diagram.mx_singles)) + " | sparks: " + str(len(diagram.mx_sparks)) + " | unreachables: " + str(len(diagram.mx_unreachable_cycles)) + " | chains: " + " ".join([str(ch) for ch in diagram.drawn.chains]) + " | connected chains: " + " ".join([str(a) + "+" + str(b) for a, b in diagram.connectedChainPairs if a < b]) + " | chain starters: " + " ".join([str(node) for node in diagram.chainStarters]))					


def jkprintsol(diagram):
		print()																												
		print("\n# Found # @jkcc: " + str(diagram.jkcc) + " | @time: " + tstr(diagram.sols[-1].tdiff) + " » " + diagram.sols[-1].text)
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
						print(">>> [ABSOLUTED] <<<\n | " + dtstr(sol.tdiff, known.tdiff) + "\n | " + jkstr(sol.jkcc, known.jkcc))
					else:
						print(">>> [REORDERED] <<<\n" + dtstr(sol.tdiff, known.tdiff) + "\n" + jkstr(sol.jkcc, known.jkcc) + "\nold » " + " ".join([str(node) for node in knownchain]) + "\nnew » " + " ".join([str(node) for node in solchain]))
				else:
					𝒟 = Diagram(diagram.spClass)
					for step in known.state:
						𝒟.measureNodes()
						node = 𝒟.nodeByPerm[step.perm]
						#print("𝒟:" + str(𝒟.rx_looped_count) + " | extending: " + str(node))
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
							

def jkinit(diagram):
	diagram.startTime = time()
	diagram.sols = []
	diagram.knowns = []
	
	# with open('sols.'+str(diagram.spClass)+".pkl", 'wb') as outfile:
	# 	pickle.dump(diagram.sols, outfile, 0)

	diagram.loadKnowns()
	diagram.startTime = time()
			
	
def run():
	diagram = Diagram(6)
			
	jkinit(diagram)
	jk(diagram)
	
	print("=== §§§ ===")

	
if __name__ == "__main__":
	from common import Step, Sol
	run()


