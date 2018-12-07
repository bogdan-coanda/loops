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
		print("[jump][returning] can't further connect chains | new_mx.min_chlen: " + str(new_mx.min_chlen) + " | len(new_mx.mt): " + str(len(new_mx.mt)))
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
		print("--- ∘ ---");
				
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
					print("[*{}*][{}][lvl:{}] failed extending it: {} | mc: {}".format(move_index, tstr(time() - startTime), lvl, it, new_mx.mc))
					break
	
			if ec == len(t): # if we've extended all of the tuple's loops
				jump(diagram, new_mx, lvl+1, jump_path+[(it,len(mt))], jump_tuples+[t], jump_nodes+[new_mx.mn[it]])
	
			for l in reversed(t[:ec]):
				diagram.collapseBack(l)
				
		new_mx.clean()					
	print("[jump][returning] @end")
					
# ============================================================================================================================================================================== #	

if __name__ == "__main__":

	move_index = -1
	D = []
	startTime = 0
	seed_index = -1
	overlapped = True
	min_uc = 99999999999

	S = '0011257 0113234 0023047 0113116 0010462 0001057 0023147 0024305 0224502 0011007 0131246 0011467 0010135 0112247 0121106 0033030 0010357 0010153 0010110 0010444 0011502 0014014 0023527 0024261 0032065 0113213 0122232 0113135 0113126 0024167 0131412 0023457 0014147 0001223 0001327 0002430 0002455 0121464 0121554 0224001 0034330 0010160 0134255 0010057 0024443 0020006 0112027 0112517 0002202 0002214 0001100 0001430 0001421 0001464 0001455 0010502 0023207 0024027 0032557 0011167 0001546 0010267 0131567 0001412 0033245 0032321 0034030 0034211 0034245 0002241 0002250 0033013 0211364 0123103 0122563 0032417'.split(' ')
		
	#S = S[12:]
		
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
				
	def run(__seed__, __miss__, __blue__=False, __over__=False, __skip__=0):
		global move_index, D, startTime
		
		diagram = Diagram(8, 1)	
			
		seed(__seed__)				
		
		P = (O if __over__ else S)[__skip__:]

		if __blue__:
			C = sample([addr for addr in P if addr[-1] == '7'], __miss__)
		else:
			C  = sample(P, __miss__)				
	
		T = [addr for addr in P if addr not in C]
			
		print("[__sample__] remaining [T]:{} out of [P]:{} ([S]:{})".format(len(T), len(P), len(S)))
					
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
		return False #D is not S
		
# ============================================================================================================================================================================== #	
	
	for i in range(0, 1):
		seed_index = i
		with open("__8__xo__", 'a', encoding="utf8") as log:
			log.write('--- seed:{} ---\n'.format(seed_index))					
		if run(i, 0):#20, False, False, 12):
			break
	print("=== === ===")
	with open("__8__xo__", 'a', encoding="utf8") as log:
		log.write('=== === ===\n')				

