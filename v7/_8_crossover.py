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
	global move_index, D, startTime, seed_index, min_uc#, __choices__
	move_index += 1
	
	if move_index % 1 == 0:
		#show(diagram)			
		print("[-{}-][*{}*][{:>11}][lvl:{}][uc:{}] {}".format(seed_index, move_index, tstr(time() - startTime), lvl, len(old_mx.unchained_cycles), ".".join([str(x)+upper(t) for x,t in jump_path])))
		
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
	
	if len(new_mx.unchained_cycles) <= min_uc:
		min_uc = len(new_mx.unchained_cycles)
		with open("__8__xo__", 'a', encoding="utf8") as log:
			log.write("[-{}-][*{}*][{:>11}][lvl:{}][uc:{}] {}\n".format(seed_index, move_index, tstr(time() - startTime), lvl, len(new_mx.unchained_cycles), ".".join([str(x)+upper(t) for x,t in jump_path])))
			log.write(" ".join([n.address for n in jump_nodes])+'\n')
			
					
	if len(diagram.chains) is 1:			
		show(diagram); 
		print("[-{}-][*{}*][{:>11}][lvl:{}][uc:{}] {}".format(seed_index, move_index, tstr(time() - startTime), lvl, len(new_mx.unchained_cycles), ".".join([str(x)+upper(t) for x,t in jump_path])));
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
		print("[-{}-][*{}*][{:>11}][lvl:{}][uc:{}] {}".format(seed_index, move_index, tstr(time() - startTime), lvl, len(new_mx.unchained_cycles), ".".join([str(x)+upper(t) for x,t in jump_path]))); 
		print(" ".join([n.address for n in jump_nodes])); 
		input("--- ∘ ---");
				
	if len(new_mx.unchained_cycles) is 0: # if all cycles have been looped	
		show(diagram)
		print("[-{}-][*{}*][{:>11}][lvl:{}][uc:{}] {}".format(seed_index, move_index, tstr(time() - startTime), lvl, len(new_mx.unchained_cycles), ".".join([str(x)+upper(t) for x,t in jump_path])))
		input("~~~ found smth ~~~")
		new_mx.clean()
	else:							
		# mc, mt = find_min_simple(diagram, new_mx.unchained_cycles, new_mx.avtuples)
		# mn = sorted([n for n in mc.nodes if n.loop.tuple in mt], key = lambda n: n.ktype)
		# mt = [n.loop.tuple for n in mn]
					
		# diagram.pointers = list(itertools.chain(*[itertools.chain(*[l.nodes for l in t]) for t in mt]))
		# show(diagram)
								
		for it, t in enumerate(mt):
			# if len(__choices__) > lvl-60:
			# 	it = __choices__[lvl-60]
			# 	t = mt[it]
					
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
	overlapped = True
	min_uc = 99999999999

	S = '0011563 0131532 0032367 0002437 0123015 0033516 0010521 0023517 0134120 0123033 0122421 0131560 0034246 1033324 0011257 0121030 0001205 0122134 0032507 0131304 0001214 1123251 0001547 0010027 0001223 0001232 0113234 0010512 0032417 0024427 0112047 0224542 0023047 0121142 0134002 0001250 0113116 0011354 0001337 0033337 0024027 0014127 0134243 0010462 0001057 0032056 0010502 0011117 0023147 0034225 0024332 0024305 0024366 0023200 0113222 0112517 0023240 0134426 0134314 0121407 0033427 0001407 0113023 0002007 0121554 0010357 0010433 0010207 0010444 0023234 0113153 0224040 0023404 0224220 0224241 0023417 0010110 0224426 0224130 0224502 0224511 1033333 1033133 0034251 0002247 0002157 0002337 0034260 0002547 0024540 0024532 0014227 0011007 0023263 0122547 0024314 0131246 0024127 0020047 0024504 0024563 0020157 0034035 0011467 0011554 0033216 0033022 0032237 0033226 0033251 0033263 1123447 0121307'.split(' ')
		
	#__choices__ = [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0]
		
	if overlapped:
		diagram = Diagram(8, 1)			
		ts = [diagram.nodeByAddress[addr].loop.tuple for addr in S]
		for i,t in enumerate(ts):
			for j,l in enumerate(t):
				assert diagram.extendLoop(l)
		oc = [c for c in diagram.cycles if len([n for n in c.nodes if n.loop.extended]) > 1]
		print("overlapping cycles: " + str(len(oc)))
		ot = set(itertools.chain(*[[n.loop.tuple for n in c.nodes if n.loop.extended] for c in oc]))
		print("overlapping tuples: " + str(len(ot)))
		on = list(itertools.chain(*[itertools.chain(*[[n.address for n in l.nodes] for l in t]) for t in ot]))
		O = [addr for addr in S if addr in on]
						
						
	# ============================================================================================================================================================================ #
				
	def run(__seed__, __miss__, __blue__=False, __over__=False):
		global move_index, D, startTime
		
		diagram = Diagram(8, 1)	
			
		seed(__seed__)				
		
		if __blue__:
			C = sample([addr for addr in (O if __over__ else S) if addr[-1] == '7'], __miss__)
		else:
			C  = sample(O if __over__ else S, __miss__)				
	
		T = [addr for addr in S if addr not in C]
			
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
		sols_file = "__8__sols__xo__"
			
		# mc, mt = find_min_simple(diagram, mx.unchained_cycles, mx.avtuples)
		# mn = sorted([n for n in mc.nodes if n.loop.tuple in mt], key = lambda n: n.address)
		# print("mc: " + mc.address + " | mt: (" + str(len(mt)) + ") " + " ".join([n.address for n in mn]))
		# diagram.pointers = list(itertools.chain(*[itertools.chain(*[l.nodes for l in t]) for t in mt]))
		# show(diagram)

		# mx = Measurement(diagram)
		# print(str(mx))
		# print("overlap: " + str(len([c for c in diagram.cycles if len([n for n in c.nodes if n.loop.extended]) > 1])))
		# print(" [~] need to remove overlapping tuples (all tuples involved) as it seems solutions have low overlap")
		# 
		# overlaps = set(itertools.chain(*[[n.loop.tuple for n in c.nodes if n.loop.extended] for c in diagram.cycles if len([n for n in c.nodes if n.loop.extended]) > 1]))
		# print(str(len(overlaps)) + "/" + str(len(set(sol_tuples))))
		# assert set(sol_tuples).issuperset(overlaps)
		
		# show(diagram)
		# input()	
																		
		# ========================================================================================================================================================================== #	
		
		mx = Measurement(diagram)
		
		jump(diagram, mx, len(sol_tuples), [('§', len(sol_tuples))], list(sol_tuples), [diagram.nodeByAddress[addr] for addr in taddrs])	
		
		print("=== seed: " + str(__seed__) + " / miss: " + str(__miss__) + " ===")
		print("D: {} {}\n{}".format(len(D), "" if D is not S else "(same)", " ".join(D)))
		return D is not S
		
# ============================================================================================================================================================================== #	
	
	for i in range(0, 24):
		seed_index = i
		with open("__8__xo__", 'a', encoding="utf8") as log:
			log.write('--- seed:{} ---\n'.format(seed_index))					
		if run(i, 24):
			break
	print("=== === ===")
	with open("__8__xo__", 'a', encoding="utf8") as log:
		log.write('=== === ===\n')				

