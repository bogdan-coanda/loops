from diagram import *
#from uicanvas import *
from common import *
from itertools import chain
from time import time
from collections import defaultdict


def find_min_blabla(diagram, avtuples):
	min_viable_tuple_count = diagram.spClass
	min_cycle = None
	min_matched_tuples = None
	
	all_min_cycles = []
	all_min_matched_tuples = set()
	
	unchained_cycles = [cycle for cycle in diagram.cycles if len(cycle.chain.cycles) is 1]
	print("[find_min_blabla] unchained_cycles: " + str(len(unchained_cycles)))
	for cycle in unchained_cycles:
		curr_cycle_tuples = [node.loop.tuple for node in cycle.nodes if node.loop.availabled or node.loop.extended]
		matched_tuples = tuple(sorted([t for t in avtuples if t in curr_cycle_tuples], key = lambda t: t[0].firstAddress()))
		
		if len(matched_tuples) < min_viable_tuple_count:
			min_viable_tuple_count = len(matched_tuples)
			min_cycle = cycle
			min_matched_tuples = matched_tuples
			all_min_cycles = [cycle]
			all_min_matched_tuples = set([min_matched_tuples])
		elif len(matched_tuples) == min_viable_tuple_count:
			all_min_cycles.append(cycle)
			all_min_matched_tuples.add(min_matched_tuples)
			
	print("[find_min_blabla] min viable tuple count: " + str(min_viable_tuple_count) + " | min cycle: " + str(min_cycle) + " | matched tuples:\n| " + "\n| ".join([str(t) for t in matched_tuples]))
	print("[find_min_blabla] all min cycles: " + str(len(all_min_cycles)) + "\n| " + "\n| ".join([str(c) for c in all_min_cycles]))
	
	return (min_cycle, min_matched_tuples, all_min_cycles, all_min_matched_tuples)
	

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
			
			
class Measurement (object):
	
	__slots__ = ['diagram', 
		'min_chlen', 'unchained_cycles', 'avloops', 'avtuples', 'tobex'
	]

	def init(diagram):
		mx = Measurement()		
		mx.diagram = diagram
		mx.min_chlen = min([len(chain.avloops) for chain in diagram.chains])
		mx.unchained_cycles = [cycle for cycle in diagram.cycles if len(cycle.chain.cycles) is 1]
		mx.avloops = [l for l in diagram.loops if l.availabled]
		mx.avtuples = [t for t in diagram.loop_tuples 
			if len([loop for loop in t if not loop.availabled and not loop.extended]) == 0
			and len([loop for loop in t if len([node.cycle for node in loop.nodes if node.cycle.isKernel]) != 0]) == 0]
		mx.tobex = diagram.measureTobex()
		return mx
		
	def measure(old_mx):
		mx = Measurement()
		mx.diagram = old_mx.diagram
		mx.min_chlen = min([len(chain.avloops) for chain in diagram.chains])
		mx.unchained_cycles = [cycle for cycle in old_mx.unchained_cycles if len(cycle.chain.cycles) is 1]
		mx.avloops = [l for l in old_mx.avloops if l.availabled]
		mx.avtuples = [t for t in old_mx.avtuples 
			if len([loop for loop in t if not loop.availabled and not loop.extended]) == 0
		]
		mx.tobex = mx.diagram.measureTobex()
		return mx
			
	def __repr__(self):
		return "⟨mx § avtuples: {} | min_chlen: {} | unchained_cycles: {} | avloops: {} | tobex: {}⟩".format(
			len(self.avtuples), self.min_chlen, len(self.unchained_cycles), len(self.avloops), self.tobex
		)			
			
	# ============================================================================================================================================================================ #

def step(diagram, jump_lvl=0, jump_path=[], jump_tuples=[], step_lvl=0, step_path=[], step_loops=[]):
	global move_index, sols
	move_index += 1
	
	if move_index % 10000 == 0:
		print("[*{}*][{}][lvl:{}~{}] {}~{}".format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t) for x,t in step_path])))
		
	if len(diagram.chains) is 1:
		# found po
		ts = " ".join(sorted([sorted([l.firstAddress() for l in t])[0] for t in jump_tuples]))
		ls = " ".join(sorted([l.firstAddress() for l in step_loops]))
		𝒮 = ts+" | "+ls
		
		if 𝒮 not in sols:
			#show(diagram); 
			print("[*{}*][{}][lvl:{}~{}] {}~{}".format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t) for x,t in step_path])))		
			
			with open(sols_file, 'a', encoding="utf8") as log:
				log.write("[sol:{:>2}][*{:>7}*][{:>11}][lvl:{}~{}]  {} ~ {}\n".format(len(sols), move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t) for x,t in step_path])))
				log.write("tuples: " + ts + "\n")
				log.write("loops: " + ls + "\n")
				log.write("\n")
											
			print("=== sol:"+str(len(sols))+" ===");
			sols += [𝒮]
		return
		
	min_chain = sorted(diagram.chains, key = lambda chain: (len(chain.avloops), chain.id))[0]
	
	for il, l in enumerate(sorted(min_chain.avloops, key = lambda l: l.firstAddress())):
		assert diagram.extendLoop(l)		
		step(diagram, jump_lvl, jump_path, jump_tuples, step_lvl+1, step_path+[(il, len(min_chain.avloops))], step_loops+[l])		
		diagram.collapseBack(l)
		
			
	# ============================================================================================================================================================================ #
	
def jump(diagram, old_mx, lvl=0, jump_path=[], jump_tuples=[]):
	global move_index
	move_index += 1
	
	if move_index % 1000 == 0:
		print("[*{}*][{}][lvl:{}] {}".format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path])))
		
	new_mx = Measurement.measure(old_mx)

	if len(diagram.chains) is 1:
		show(diagram); input("=== sol ===");
		return

	if new_mx.min_chlen is 0: # can't further connect chains
		return
		
	assert len(new_mx.avloops) >= new_mx.tobex, "can't join all chains"
		
	# if new_mx.min_chlen is 0:
	# 	diagram.point(); show(diagram); input("--- min_chlen: 0 ---")
	
	#print("[*{}*][{}][lvl:{}]  uc: {} | mx: {}".format(move_index, tstr(time() - startTime), lvl, len(uc), mx))
	
	#if lvl >= 27:
		#diagram.point(); show(diagram); input("[*{}*][{}][lvl:{}] … uc: {} | tobex: {}".format(move_index, tstr(time() - startTime), lvl, len(new_mx.unchained_cycles), new_mx.tobex))
				
	if len(new_mx.unchained_cycles) is 0 or lvl > 23: # if all cycles have been looped	
		#print("carrying on | uc: " + str(len(new_mx.unchained_cycles)) + " | lvl: " + str(lvl))
		old_sol_count = len(sols)
	
		if len(mx.avtuples) > 0: # if we still have tuples that can be extended
						
			for it, t in enumerate(mx.avtuples):
				ec = 0
				for lt, l in enumerate(t):
					if diagram.extendLoop(l):
						ec += 1
					else:
						break
		
				if ec == len(t): # if we've extended all of the tuple's loops
					jump(diagram, new_mx, lvl+1, jump_path+[(it,len(mx.avtuples))], jump_tuples+[t])
		
				for l in reversed(t[:ec]):
					diagram.collapseBack(l)
	
		if lvl >= 23:
			step(diagram, lvl, jump_path, jump_tuples, len(sol_loops), [('§', len(sol_loops))], list(sol_loops))
			
		if len(sols) != old_sol_count:
			with open(sols_file, 'a', encoding="utf8") as log:
				log.write("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n")
			
	else:				
		mc, mt = find_min_simple(diagram, new_mx.unchained_cycles, new_mx.avtuples)
		
		#print("[*{}*][{}][lvl:{}]  min | matched tuples: {} | cycle: {}".format(move_index, tstr(time() - startTime), lvl, len(mt), mc))
	
		for it, t in enumerate(mt):
			
			if (lvl == 0 and it != 2):
				continue
			
			ec = 0
			for lt, l in enumerate(t):
				if diagram.extendLoop(l):
					ec += 1
				else:
					break
	
			if ec == len(t): # if we've extended all of the tuple's loops
				jump(diagram, new_mx, lvl+1, jump_path+[(it,len(mt))], jump_tuples+[t])
	
			for l in reversed(t[:ec]):
				diagram.collapseBack(l)


if __name__ == "__main__":

	# ============================================================================================================================================================================ #
		
	diagram = Diagram(7, 1)
	# diagram.extendLoop(diagram.nodeByAddress['000001'].loop)
	
	#sol_addrs = "001005 001105 001205 001305 011003 011013 011021 011030 011034 011054 123001 123011 123021 123034 123044 123052 022005 022105 022305 112006 001042 001224 001403 001454 | 020200 012300 023100 103006 020000 003006 113030 122440 022340 021330 013410 001420 120230 100106 110210 020340 010040 111130"
	sol_addrs = "001005 001105 001205 001305 011003 011013 011021 011030 011034 011054 123001 123011 123021 123034 123044 123052 022005 022105 022305 112006 001042 001224 001403 001454 | "# 023100 103006 020000 003006 113030 122440 022340 021330 013410 001420 120230 100106 110210 020340 010040"# 111130"
	taddrs, laddrs = sol_addrs.split(" | ")
	taddrs = taddrs.split(" ")
	
	#'''
	taddrs = [ 
		
		#'002020', '002233', # 011 diag box ((1)) / ((2))
		#'013020', '013233', # 123 box ((1)) / ((3))	/ ((2)) / ((4))	
				
		#'001006', '001106', '001206', '001306', # 001 blue box-1
		
		# '001403', '001410', '001430', '001454', # 0014 blue fillers ((1))
		# '001401', '001410', '001430', '001452', # 0014 blue fillers ((2))		
		#'001410', '001430', # 0014 blue fillers ((∘))
				
		# '002020', '002110', '002200', '002233', '002242', '002251', # 011 diag box ((1))
		# '002002', '002011', '002020', '002053', '002143', '002233', # 011 diag box ((2))
		#'002020', '002233', # 011 diag box ((∘))
								
		# '013002', '013020', '013044', '013053', '013224', '013233', # 123 box ((1))
		# '013020', '013044', '013200', '013224', '013233', '013251', # 123 box ((2))
		#'013020', '013044', '013224', '013233', # 123 box ((∘))
				
		#'022006', '022106', '022306', # 022 blue box-2
		#'112005' # 112 green diag box
				
	#'123011', '123021', '123034', '123044', 
	#'011021', '011034', 
	#'101430', '001224', # common to 10 sols, along with 112 box and the 2 greens
	# '123006', '112006', '011006' # -- blue boxes
	# '001042', '001224', '001403', '001454', # 001405 alts
	#'112006', # 112 box
	# '011003', '011013', '011021', '011030', '011034', '011054' # 011 box
	# '123001', '123011', '123021', '123034', '123044', '123052' # 123 box
	#'001005', '001105', '001205', '001305', # green
	#'022005', '022105', '022305' # green
	]
	#'''
	
	sol_tuples = [diagram.nodeByAddress[addr].loop.tuple for addr in taddrs]
	if len(laddrs):
		sol_loops = [diagram.nodeByAddress[addr].loop for addr in laddrs.split(" ")]
	else:
		sol_loops = []
	print("sol | tuples: " + str(len(sol_tuples)) + " | loops: " + str(len(sol_loops)))	
	for i,t in enumerate(sol_tuples):
		for j,l in enumerate(t):
			assert diagram.extendLoop(l)
	for l in sol_loops:
		assert diagram.extendLoop(l)
	
	# ============================================================================================================================================================================ #
		
	startTime = time()
	move_index = -1
	sols = []
	sols_file = "__7__sols__z2__"
	
	# ============================================================================================================================================================================ #	

	mx = Measurement.init(diagram)
	#show(diagram)
	print("mx: " + str(mx))
	
								
	jump(diagram, mx, len(sol_tuples), [('§', len(sol_tuples))], list(sol_tuples))

	with open(sols_file, 'a', encoding="utf8") as log:
		log.write("==================================================================================================================================================================================\n\n")
				
	# mx = Measurement.measure(diagram)
	# mc, mt, ac, mm = find_min_blabla(diagram, mx.avtuples)	
	# 
	# print("[mx] " + str(mx))
		
	# mtn = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*mx.avtuples)]))
	# diagram.pointers = list(itertools.chain(*[[node for node in c.nodes if node in mtn] for c in ac]))
	# show(diagram)
	# 
	# mtn = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*mt)]))
	# diagram.pointers = list(itertools.chain(*[[node for node in c.nodes if node in mtn] for c in ac]))	
	# show(diagram)
	# 
	# mtn = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*mt)]))
	# diagram.pointers = [node for node in mc.nodes if node in mtn]	
	# show(diagram)	
	# 
	# diagram.pointers = [mc]
	# show(diagram)
	# 
	# diagram.pointers = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*mt)]))
	# show(diagram)

	# diagram.pointers = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*mt)]))
	# show(diagram)																		
	# diagram.pointers = [mc]
	# show(diagram)
	# input("[*{}*][{}][lvl:{}] … ".format(move_index, tstr(time() - startTime), lvl))

	# ============================================================================================================================================================================ #	
	
	#diagram.point()
	#show(diagram)	
