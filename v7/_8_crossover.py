from diagram import *
from uicanvas import *
from common import *
from measurement import *
from itertools import chain
from time import time
from collections import defaultdict
from random import *

def find_min_simple(diagram, unchained_cycles, avtuples):
	min_viable_tuple_count = diagram.spClass
	min_cycle = None
	min_matched_tuples = None
		
	#print("[find_min_blabla] unchained_cycles: " + str(len(unchained_cycles)))
	for cycle in unchained_cycles:
		curr_cycle_tuples = [node.loop.tuple for node in cycle.nodes if node.loop.availabled or node.loop.extended]
		matched_tuples = tuple(sorted([t for t in avtuples if t in curr_cycle_tuples], key = lambda t: t[0].firstNode().ktype))
		
		if len(matched_tuples) < min_viable_tuple_count:
			min_viable_tuple_count = len(matched_tuples)
			min_cycle = cycle
			min_matched_tuples = matched_tuples
				
	return (min_cycle, min_matched_tuples)
			
# ============================================================================================================================================================================== #	

def jump(diagram, old_mx, lvl=0, jump_path=[], jump_tuples=[], jump_nodes=[]):
	global move_index, D, startTime, seed_index
	move_index += 1
	
	if move_index % 1 == 0:
		#show(diagram)			
		print("[-{}-][*{}*][{}][lvl:{}] {}".format(seed_index, move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path])))
		
	new_mx = old_mx.remeasure()
	# if lvl % 36 == 0: # move_index % 10 == 0:
	# 	print("•metric: " + str(new_mx))
	# 	new_mx.reduce()
	# 	print("•reduce: " + str(new_mx))	
	# 	new_mx.measure_viable_tuples()
	# 	print("•viable: " + str(new_mx))	
	mt = new_mx.find_min_simple()
	#diagram.pointers = new_mx.mn; show(diagram); 
	#print("•simple: " + str(new_mx))
	
	if len(diagram.chains) is 1:			
		show(diagram); 
		print("[-{}-][*{}*][{}][lvl:{}] {}".format(seed_index, move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path])));
		print(" ".join([n.address for n in jump_nodes]))
		new_mx.clean()
		input("=== sol ===");
		return

	if new_mx.min_chlen is 0 or len(new_mx.mt) is 0: # can't further connect chains
		# show(diagram)			
		#print("[*{}*][{}][lvl:{}] failed min chlen: 0".format(move_index, tstr(time() - startTime), lvl))		
		new_mx.clean()
		return
		
	assert len(new_mx.avloops) >= new_mx.tobex, "can't join all chains"
		
	# if new_mx.min_chlen is 0:
	# 	diagram.point(); show(diagram); input("--- min_chlen: 0 ---")
	
	#print("[*{}*][{}][lvl:{}]  uc: {} | mx: {}".format(move_index, tstr(time() - startTime), lvl, len(uc), mx))
	
	if lvl > len(D):
		#diagram.point(); show(diagram); 
		D = [n.address for n in jump_nodes]
		print("[-{}-][*{}*][{}][lvl:{}] {}".format(seed_index, move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]))); 
		print(" ".join([n.address for n in jump_nodes])); 
		input("--- ∘ ---");
				
	if len(new_mx.unchained_cycles) is 0: # if all cycles have been looped	
		show(diagram)
		print("[-{}-][*{}*][{}][lvl:{}] {}".format(seed_index, move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path])))
		input("~~~ found smth ~~~")
		new_mx.clean()
	else:							
		# mc, mt = find_min_simple(diagram, new_mx.unchained_cycles, new_mx.avtuples)
		# mn = sorted([n for n in mc.nodes if n.loop.tuple in mt], key = lambda n: n.ktype)
		# mt = [n.loop.tuple for n in mn]
					
		# diagram.pointers = list(itertools.chain(*[itertools.chain(*[l.nodes for l in t]) for t in mt]))
		# show(diagram)
				
		for it, t in enumerate(mt):
				
			#if (lvl == 0 and it != 2):
				#continue
							
			ec = 0
			for lt, l in enumerate(t):
				if diagram.extendLoop(l):
					ec += 1
				else:
					#print("[*{}*][{}][lvl:{}] failed extending it: {}".format(move_index, tstr(time() - startTime), lvl, it))
					break
	
			if ec == len(t): # if we've extended all of the tuple's loops
				jump(diagram, new_mx, lvl+1, jump_path+[(it,len(mt))], jump_tuples+[t], jump_nodes+[new_mx.mn[it]])
	
			for l in reversed(t[:ec]):
				diagram.collapseBack(l)
				
		new_mx.clean()					
					
# ============================================================================================================================================================================== #	

if __name__ == "__main__":

	move_index = -1
	D = []
	startTime = 0
	seed_index = -1

	# ============================================================================================================================================================================ #
				
	def run(__seed__, __miss__, __blue__=False):
		global move_index, D, startTime
		
		diagram = Diagram(8, 1)	
			
		seed(__seed__)	
				
		S = '0014247 0034250 0011563 0131532 0032367 0211263 0032147 0002437 0123015 0033516 0002507 0010521 0023517 0002167 0134120 0123033 0122421 0122442 0131560 0034246 0010444 1033324 0034301 0121125 0011257 0121524 0020067 0121030 0001205 0122134 0032507 0033564 0024507 0134063 0131304 0001214 1123251 0001547 0011417 0010554 0010027 0020117 0001223 0001232 0123042 0113234 0010512 0033057 0010217 0023323 0032417 0002227 0024427 0112047 0112255 0023407 0224542 0023047 0122412 0034201 0011027 0011554 0034352 0121142 0134153 0131540 0134002 0001250 0113116 0011354 1123201 0001337 0032237 0033207 1033520 0033337 0024027 0002327 0023314 0014127 0010117 0134243 0010462 0034211 0134252 0001057 0002057 0033427 0034330 0122542 0001427 0032056 1033246 0033520 0010304 0010347 0010502 0011117 0023147 0034017 0034225 0121060 1033331 0024332 0024305 0024366 0023200 0113222 0024323 0112247 0112517 0023240 0134426 0134314 0113023 0134260 0024147 0112407 0121407'.split(' ')
		
		if __blue__:
			B = sample([addr for addr in S if addr[-1] == '7'], __miss__)
			print("B: " + str(len(B)) + " | " + str(B))
			T = [addr for addr in S if addr not in B]
			print("T: " + str(len(T)) + " | " + str(T))			
		else:
			T = sample(S, len(S) - __miss__)			

		print("[__sample__] remaining {} out of {}".format(len(T), len(S)))
					
		D = S
				
		taddrs = T
		laddrs = []
										
		# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
								
		sol_tuples = [diagram.nodeByAddress[addr].loop.tuple for addr in taddrs]
		sol_loops = [diagram.nodeByAddress[addr].loop for addr in laddrs]
		
		for i,t in enumerate(sol_tuples):
			for j,l in enumerate(t):
				assert diagram.extendLoop(l)
		for j,l in enumerate(sol_loops):
			assert diagram.extendLoop(l)
									
		# ========================================================================================================================================================================== #	
						
		startTime = time()
		move_index = -1
		sols = []
		sols_file = "__8__sols__xxx__"
			
		# mc, mt = find_min_simple(diagram, mx.unchained_cycles, mx.avtuples)
		# mn = sorted([n for n in mc.nodes if n.loop.tuple in mt], key = lambda n: n.address)
		# print("mc: " + mc.address + " | mt: (" + str(len(mt)) + ") " + " ".join([n.address for n in mn]))
		# diagram.pointers = list(itertools.chain(*[itertools.chain(*[l.nodes for l in t]) for t in mt]))
		# show(diagram)

		mx = Measurement(diagram)
		print(str(mx))
		print("overlap: " + str(len([c for c in diagram.cycles if len([n for n in c.nodes if n.loop.extended]) > 1])))
		print(" [~] need to remove overlapping tuples (all tuples involved) as it seems solutions have low overlap")
		# show(diagram)
		# input()	
																		
		# ========================================================================================================================================================================== #	
		
		mx = Measurement(diagram)
		
		jump(diagram, mx, len(sol_tuples), [('§', len(sol_tuples))], list(sol_tuples), [diagram.nodeByAddress[addr] for addr in taddrs])	
		
		print("=== seed: " + str(__seed__) + " / miss: " + str(__miss__) + " ===")
		print("D: {} {}\n{}".format(len(D), "" if D is not S else "(same)", " ".join(D)))
		return D is not S
		
# ============================================================================================================================================================================== #	
	
	for i in range(0, 1296):
		seed_index = i
		if run(i, 59):
			break
	print("=== === ===")

