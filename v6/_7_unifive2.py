from diagram import *
from uicanvas import *
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
		matched_tuples = tuple(sorted([t for t in avtuples if t in curr_cycle_tuples], key = lambda t: t[0].firstAddress()))
		
		if len(matched_tuples) < min_viable_tuple_count:
			min_viable_tuple_count = len(matched_tuples)
			min_cycle = cycle
			min_matched_tuples = matched_tuples
				
	return (min_cycle, min_matched_tuples)
			
class Measurement (object):
	
	__slots__ = ['diagram', 
		'unchained_cycles', 'avloops', 'avtuples', 'tobex'
	]

	def init(diagram):
		mx = Measurement()		
		mx.diagram = diagram
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
		mx.unchained_cycles = [cycle for cycle in old_mx.unchained_cycles if len(cycle.chain.cycles) is 1]
		mx.avloops = [l for l in old_mx.avloops if l.availabled]
		mx.avtuples = [t for t in old_mx.avtuples 
			if len([loop for loop in t if not loop.availabled and not loop.extended]) == 0
		]
		mx.tobex = mx.diagram.measureTobex()
		return mx
			
	# ============================================================================================================================================================================ #

def jump(diagram, old_mx, lvl=0, jump_path=[], jumped_tuples=[]):
	global move_index
	move_index += 1
	
	if move_index % 100 == 0:
		print("[*{}*][{}][lvl:{}] {}".format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path])))
		
	new_mx = Measurement.measure(old_mx)
	
	#print("[*{}*][{}][lvl:{}]  uc: {} | mx: {}".format(move_index, tstr(time() - startTime), lvl, len(uc), mx))
	
	if lvl >= 27 and len(new_mx.avloops) >= 2:
		diagram.point(); show(diagram); input("[*{}*][{}][lvl:{}] … uc: {} | tobex: {}".format(move_index, tstr(time() - startTime), lvl, len(new_mx.unchained_cycles), new_mx.tobex))
		
	if len(new_mx.unchained_cycles) is 0: # if all cycles have been looped	
		if lvl >= 27 and len(new_mx.avloops) >= 2:
			diagram.point(); show(diagram); input("[*{}*][{}][lvl:{}] § uc: 0 | tobex: {}".format(move_index, tstr(time() - startTime), lvl, new_mx.tobex))
			
	else:				
		mc, mt = find_min_simple(diagram, new_mx.unchained_cycles, new_mx.avtuples)
		
		#print("[*{}*][{}][lvl:{}]  min | matched tuples: {} | cycle: {}".format(move_index, tstr(time() - startTime), lvl, len(mt), mc))
	
		for it, t in enumerate(mt):
			ec = 0
			for lt, l in enumerate(t):
				if diagram.extendLoop(l):
					ec += 1
				else:
					break
	
	
			if ec == len(t): # if we've extended all of the tuple's loops
				jump(diagram, new_mx, lvl+1, jump_path+[(it,len(mt))], jumped_tuples+[t])
	
			for l in reversed(t[:ec]):
				diagram.collapseBack(l)


if __name__ == "__main__":

	# ============================================================================================================================================================================ #
		
	diagram = Diagram(7, 1)
	diagram.extendLoop(diagram.nodeByAddress['000001'].loop)
	
	# ============================================================================================================================================================================ #
		
	startTime = time()
	move_index = -1
	sol_count = 0	
				
	# ============================================================================================================================================================================ #	

	mx = Measurement.init(diagram)
	jump(diagram, mx)

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
