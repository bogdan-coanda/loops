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
			
			
if __name__ == "__main__":

	# ============================================================================================================================================================================ #
		
	diagram = Diagram(8, 1)

	# ============================================================================================================================================================================ #	

	seed(0)	
	# 
	# S0 = set('0001002 0001101 0001117 0001011 0001025 0001204 0001063 0001252 0001265 0001300 0001355 0001046 0001055 0010062 0010005 0001360 0001463 0032464 0001431 0001440 0001557 0010544 0001325 0001331 0001240 0001226 0001232 0001420 0010153 0010330 0002002 0002064 0002136 0032025 0033546 0002037 0002115 0002213 0002220 0002143 0002422 0020067 0011222'.split(' ')) # len:43
	# 
	# S0a = set(sample(S0, len(S0)//3)) # len:21
	# S0b = S0.difference(S0a) # len:22
	# 
	# S0a.update('0001201 0001266 0001306 0001313 0001343 0211043 0001047 0001331 0001241 0001132 0002000 0033333 0002154 0002330 0001356 0002144 0033325 0002163 0002253 0010014 0020116 0001447 0032403 0010430 0032026 0023526 0034344 0033434 0032522 0121051 0011431 0032235 0002510 0002555 0011516 0002045 0020026'.split(' ')) # len:51
	# S0b.update('0001557 0010062 0001463 0002220 0002421 0002507 0024053 0001012 0001021 0001223 0001234 0033504 0121224 0002465 0011304 0010350 0010535 0002136 0011014 0011213 0011123 0011420 0011507 0023314 0010524 0010134 0032535 0020102 0033103 0011054 0011041'.split(' ')) # len:60
	# 
	# S1a = set(sample(S0a, len(S0a)//2)) # len:30
	# S1b = S0b.difference(S1a) # len:30
			
	S = '0023207 0001407 0033207 0011507 0134042 0002247 0010127 0121252 0034301 0034211 0112217 0113237 0121047 0023337 0010217 0034246 0123447 0023157 0130037 0033553 1033063 0001107 0024457 0024547 0113147 0033564 0001207 0134242 0001007 0121157 0002537 0010547 0023517 0112047 0010037 0023407 0121223 0134031 0112107 0024301 1033315 0024357 0034067 0020117 0014227 0123017 0033337 0033007 0112307 0032547 0034352 1033165 0032227 0033536 0121526 0121206 0032467 0011157 0011007 1033034 0032307 0002317 0024257 0134525 0024037 0020007 0001307 0033427 0033544 0023047 0014032 0002157 0010307 0014107 0034346 0033516 0112407 0010462 0123107 0002417 0113007 0011207 0034201 0002007 0032047 0010453 0024107 0034250 0001502 0001527 0011417 0032167 0033117 1033426 0112554 0134101 0121231'.split(' ')
	
	T = sample(S, len(S) - 32)
	D = S
			
	taddrs = T
	laddrs = []
									
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
							
	sol_tuples = [diagram.nodeByAddress[addr].loop.tuple for addr in taddrs]
	sol_loops = [diagram.nodeByAddress[addr].loop for addr in laddrs]
	
	for i,t in enumerate(sol_tuples):
		for j,l in enumerate(t):
			assert diagram.extendLoop(l)
	for j,l in enumerate(sol_loops):
		assert diagram.extendLoop(l)
								
	# ============================================================================================================================================================================ #	

	def jump(diagram, old_mx, lvl=0, jump_path=[], jump_tuples=[], jump_nodes=[]):
		global move_index, D
		move_index += 1
		
		if move_index % 1 == 0:
			#show(diagram)			
			print("[*{}*][{}][lvl:{}] {}".format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path])))
			
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
			print("[*{}*][{}][lvl:{}] {}".format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path])));
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
			print("[*{}*][{}][lvl:{}] {}".format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]))); print(" ".join([n.address for n in jump_nodes])); print("--- ∘ ---");
					
		if len(new_mx.unchained_cycles) is 0: # if all cycles have been looped	
			show(diagram)
			print("[*{}*][{}][lvl:{}] {}".format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path])))
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
		
	# ============================================================================================================================================================================ #	
					
	startTime = time()
	move_index = -1
	sols = []
	sols_file = "__8__sols__xxx__"
		
	# mc, mt = find_min_simple(diagram, mx.unchained_cycles, mx.avtuples)
	# mn = sorted([n for n in mc.nodes if n.loop.tuple in mt], key = lambda n: n.address)
	# print("mc: " + mc.address + " | mt: (" + str(len(mt)) + ") " + " ".join([n.address for n in mn]))
	# diagram.pointers = list(itertools.chain(*[itertools.chain(*[l.nodes for l in t]) for t in mt]))
	# show(diagram)
	
					
	# ============================================================================================================================================================================ #	
	'''
	mx = Measurement(diagram)
	# print("•metric: " + str(mx))
	# mx.reduce()
	# print("•reduce: " + str(mx))	
	# mx.measure_viable_tuples()
	# print("•viable: " + str(mx))	
	# mt = mx.find_min_simple()
	# print("•simple: " + str(mx))					
	# diagram.pointers = mx.mn; show(diagram); 
	
	lvl = len(taddrs)
	jump_path = []
	jump_tuples = []
	jump_nodes = []
	
	mx = mx.remeasure()
	mt = mx.find_min_simple()		
	print("[*{}*][{}][lvl:{}] {}".format(move_index, tstr(time() - startTime), lvl, mx))												
				
	while True:
		move_index += 1		
		print("[*{}*][{}][lvl:{}] {}".format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path])))																
				
		if mx.min_chlen is 0 or len(mt) is 0:
			break	
	
		isValid = False		
		for it, t in enumerate(mt):
								
			ec = 0
			for lt, l in enumerate(t):
				if diagram.extendLoop(l):
					ec += 1
				else:
					print("[*{}*][{}][lvl:{}] failed extending it: {}".format(move_index, tstr(time() - startTime), lvl, it))
					break
	
			if ec == len(t): # if we've extended all of the tuple's loops
				new_mx = mx.remeasure()
				new_mt = new_mx.find_min_simple()						
				if new_mx.min_chlen is not 0 and len(new_mt) is not 0:
					isValid = True
						
			if isValid:
				lvl += 1
				jump_path += [(it,len(mt))]
				jump_tuples += [t]
				jump_nodes += [mx.mn[it]]
				mx = new_mx
				mt = new_mt
				print("[*{}*][{}][lvl:{}] {}".format(move_index, tstr(time() - startTime), lvl, mx))																
				break
			else:
				for l in reversed(t[:ec]):
					diagram.collapseBack(l)
				#mx.avtuples.remove(t)
				
		if not isValid:
			break

	diagram.pointers = ([mx.mc] if mx.mc else []) + jump_nodes
	show(diagram)
	print("[*{}*][{}][lvl:{}] {}".format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path])))												
	print(" ".join([n.address for n in jump_nodes]))
	'''
	# ============================================================================================================================================================================ #	
	
	# diagram.point()
	# show(diagram)						
	#input("~~~")
	
	# mx0 = Measurement(diagram)	
	# print(mx0)
	# mx0.reduce()
	# print(mx0)	
	# mx0.measure_viable_tuples()
	# print(mx0)	
	# mt0 = mx0.find_min_simple()
	# diagram.pointers = mx0.mn; show(diagram); input(mx0)
	
	mx = Measurement(diagram)
	
	jump(diagram, mx, len(sol_tuples), [('§', len(sol_tuples))], list(sol_tuples), [diagram.nodeByAddress[addr] for addr in taddrs])	
	
	print("===")
	print("D: {} {}\n{}".format(len(D), "" if D is not S else "(same)", " ".join(D)))
