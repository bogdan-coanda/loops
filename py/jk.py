from diagram import *
from time import time, sleep
from math import floor
import pickle
import shutil
from functools import cmp_to_key
import traceback
from common import *
import random
from uicanvas import *


def jk(diagram, lvl = 0, state = [], last_extended_node = None):
	
	if diagram.jkcc % 1000 == 0:
		jkprintstate(diagram, lvl, state)
		show(diagram)
	
	diagram.jkcc += 1

#	if diagram.jkcc > 10000:
#		return

	if len(diagram.rx_singles) > 0:
		availables = [sorted(diagram.mx_singles, key = cmp_to_key(lambda x, y: 0 if x.perm == y.perm else (1 if x.perm > y.perm else -1)))[0]]
		is_normal = False

	else:
		
		diagram.measureNodes(last_extended_node or diagram.startNode)
				
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
		
	#availables = [node for node in availables if node.address[-1] != '0' and node.address[-1] != '5']
	#random.shuffle(availables)
	#availables = availables[:4]
	availables.sort(key = lambda node: node.address[-1] != str(diagram.spClass-1))
	
	if lvl is 0:
		availables = [diagram.nodeByAddress['123005']]
	elif lvl is 1:
		availables = [diagram.nodeByAddress['123025']]
	elif lvl is 2:
		availables = [diagram.nodeByAddress['123045']]
	elif lvl is 3:
		availables = [diagram.nodeByAddress['100014']]
	elif lvl is 4:
		availables = [diagram.nodeByAddress['100125']]
	#elif lvl is 5:
		#availables = [diagram.nodeByAddress['100045']]
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
			#sg, sp, un = len(diagram.mx_singles), len(diagram.mx_sparks), len(diagram.mx_unreachable_cycles)
			diagram.tryMakeUnavailable([node])
			#assert (sg, sp, un) == (len(diagram.mx_singles), len(diagram.mx_sparks), len(diagram.mx_unreachable_cycles))
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
	print("[state] jk: " + str(diagram.jkcc) + " | lvl: " + str(lvl) + " | » " + sstr(state, diagram))	
	print("[drawn] looped: " + str(diagram.rx_looped_count) + " | availables: " + str(len([l for l in diagram.loops if l.availabled])) + " | singles: " + str(len(diagram.rx_singles)) + " | unreachables: " + str(len(diagram.rx_unreachables)))					


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
			assert False, 'found smth'
					
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
						assert False, ">>> [REORDERED] <<<"
				else:
					𝒟 = Diagram(diagram.spClass)
					for step in known.state:
						𝒟.measureNodes(𝒟.startNode)
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
								assert False, ">>> [CONVERGENT] <<<"
								return
						pc += 1
							

def jkinit(diagram):
	diagram.startTime = time()
	diagram.sols = []
	diagram.knowns = []
	
	# with open('sols.'+str(diagram.spClass)+".pkl", 'wb') as outfile:
	# 	pickle.dump(diagram.sols, outfile, 0)

	#diagram.loadKnowns()
	diagram.startTime = time()
			
	
def run():
	diagram = Diagram(7)
			
	jkinit(diagram)
	
	#import cProfile, pstats, io
	#pr = cProfile.Profile()
	#pr.enable()
	# ... do something ...
	
	jk(diagram)
	
	#pr.disable()
	#s = io.StringIO()
	#ps = pstats.Stats(pr, stream=s)
	#ps.strip_dirs()
	#ps.sort_stats('time', 'cumulative')
	#ps.print_stats()
	#print(s.getvalue())
	
	print("=== §§§ ===")

	
if __name__ == "__main__":
	from common import Step, Sol
	run()


