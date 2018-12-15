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
		new_mx.clean()
		# print("[jump][returning] can't further connect chains | new_mx.min_chlen: " + str(new_mx.min_chlen) + " | len(new_mx.mt): " + str(len(new_mx.mt)))
		#diagram.pointers = [new_mx.mc]; 
		#diagram.point()
		#show(diagram); input(" === @ can't {},{} === ".format(new_mx.min_chlen, len(new_mx.mt))) 		
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
					# print("[*{}*][{}][lvl:{}] failed extending it: {} | mc: {}".format(move_index, tstr(time() - startTime), lvl, it, new_mx.mc))
					break
	
			if ec == len(t): # if we've extended all of the tuple's loops
				jump(diagram, new_mx, lvl+1, jump_path+[(it,len(mt))], jump_tuples+[t], jump_nodes+[new_mx.mn[it]])
	
			for l in reversed(t[:ec]):
				diagram.collapseBack(l)
				
		new_mx.clean()					
		
	print("[-{}-][*{}*][{:>11}][lvl:{}][uc:{}] {}".format(seed_index, move_index, tstr(time() - startTime), lvl, len(new_mx.unchained_cycles), ".".join([str(x)+upper(t) for x,t in jump_path]))); 
	print(" ".join([n.address for n in jump_nodes]));		
	#diagram.pointers = [new_mx.mc]; show(diagram); 
	with open("__8__xo__", 'a', encoding="utf8") as log:
		log.write(" === @ end | mc: "+str(new_mx.mc)+" === ")	
	input(" === @ end | mc: "+str(new_mx.mc)+" === ")
	# print("[jump][returning] @end")
					
# ============================================================================================================================================================================== #	

if __name__ == "__main__":

	move_index = -1
	D = []
	startTime = 0
	seed_index = -1
	overlapped = True
	min_uc = 99999999999

	S = '0001007 0001407 0001517 0002007 0002157 0002507 0010037 0010307 0010547 0010127 0010217 0010453 0010462 0010435 0014107 0014227 0020007 0020117 0011007 0011157 0011207 0011427 0011507 0023047 0023157 0023207 0023337 0023407 0023517 0032467 0032047 0032307 0024037 0024307 0024457 0024547 0112037 0112527 0113007 0113147 0113237 0033137 0033536 0033516 0033544 0034346 0130037 0121311 0001337 0001237 0034352 0002322 0032247 0112407 1123106 0002331 0134036 0122337 0122546 0131547 0112256 1033565 0112107 0131417 0112343 0024137 0131137 0131007 0131207 0130327 0224563 0002365 0032537 0034007 0122123 0122457 0122047'.split(' ')
		
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
	
	for i in range(7, 8):
		
		# === @ end | mc: ⟨cycle:1322@012126⟩ === 		
		S.append('012126'+str(i))
		
		seed_index = i
		with open("__8__xo__", 'a', encoding="utf8") as log:
			log.write('--- seed:{} ---\n'.format(seed_index))					
		if run(i, 0):#20, False, False, 12):
			break
	print("=== === ===")
	with open("__8__xo__", 'a', encoding="utf8") as log:
		log.write('=== === ===\n')				
