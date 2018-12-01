from diagram import *
from uicanvas import *
from common import *
from itertools import chain
from time import time
from collections import defaultdict


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

if __name__ == "__main__":

	# ============================================================================================================================================================================ #
		
	diagram = Diagram(8, 1)

	taddrs = []
	
	# taddrs += [ '1234000' ] # top
	# taddrs += [ '1234010', '1234020', '1234030', '1234040' ] # green
	taddrs += [ '1234014', '1234025', '1234032', '1234034' ] # blue
	taddrs += [ '1234050' ] # bot
	
	# taddrs += [ '1233107' ] # top green
	# taddrs += [ '1233106' ] # top blue
	# taddrs += [ '1233006', '1233206', '1233306', '1233406' ] # green
	taddrs += [ '1233007', '1233207', '1233307', '1233407' ] # blue
	# taddrs += [ '1233507' ] # bot green		
	taddrs += [ '1233506' ] # bot blue
	
	# taddrs += [ '1204107' ] # top green
	#	taddrs += [ '1204106' ] # top blue
	# taddrs += [ '1224507' ] # bot green
	taddrs += [ '1224506' ] # bot blue
	
	# kernel derived
	
	taddrs += [ # [blue bars]
		'1000107', '1100007', '1010007', '1001007', '1000507', '1010407'
	]

	taddrs += [ # [blue bars]∘[kern:01:03]
		'1000206', '1000407', '1010106', '1010507'
	]
	
	# taddrs += [ # [blue bars]∘[kern:01:03] | outer violet
	# 	'1000002', '1000011', '1000020', '1000045', '1000054', '1000063'
	# ]	

	# taddrs += [ # [blue bars]∘[kern:01:03] | outer red
	# 	'1000003', '1000012', '1000021', '1000030', '1000055', '1000064'
	# ]	

	taddrs += [ # [blue bars]∘[kern:01:03] | outer orange
		'1000004', '1000013', '1000022', '1000031', '1000040', '1000065'
	]	

	# taddrs += [ # [blue bars]∘[kern:01:03] | inner red
	# 	'1000210', '1000235', '1000244', '1000253'
	# ]								

	# taddrs += [ # [blue bars]∘[kern:01:03] | inner orange
	# 	'1000211', '1000220', '1000245', '1000254'
	# ]								
										
	taddrs += [ # [blue bars]∘[kern:01:03] | inner yellow
		'1000212', '1000221', '1000230', '1000255'
	]


	# taddrs += [ # [green diags]
	# 	'1000106', '1100006', '1010006', '1001006', '1000506', '1010406'
	# ]
	# 
	# taddrs += [ # [green diags]∘[kern:62:64]
	# 	'1000207', '1000406', '1010107', '1010506'
	# ]

	taddrs += [	# [blue bars]∘[kern:01:03] | outer red ∘ inner yellow | singles
		'0034325', '0034334', 
	]
	
	taddrs += [ # 1010 filler purple
		#'1010304', '1010313'#, '1010322'
	]
	
	taddrs += [ # path
		# '1002067', # 1/2 # … 1002063
		# '1010320', # 0/3 # … 1010321 1010321
		# '0032202', # 0/3 # mt: (3) 0032202 0032204 0032205
		# '0033541', # 0/3 # mt: (3) 0033541 0033542 0033547
		# '0033367', # 1/2 # mt: (2) 0033364 0033367
		# '0034316', # 0/3 # mt: (3) 0034312 0034316 0034317
		# '0032261', # 0/3 # mt: (3) 0032261 0032263 0032266
	]
	
	taddrs += [ # columns
		#'0002522'
	]
	
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #	

	laddrs = []
	
	# [blue bars]∘[kern:01]
	laddrs += [ '0000001' ]
	# laddrs += [ '0000365' ]	
	# laddrs += [ '0000201' ]
	# laddrs += [ '0000565' ]	
	# laddrs += [ '0000401' ]
	# laddrs += [ '0000165' ]

	# [blue bars]∘[kern:03]
	# laddrs += [ '0000403' ]
	# laddrs += [ '0000563' ]	
	# laddrs += [ '0000003' ]
	# laddrs += [ '0000163' ]	
	# laddrs += [ '0000203' ]
	# laddrs += [ '0000363' ]
				
	# [green diags]∘[kern:62]
	# laddrs += [ '0000062' ]
	# laddrs += [ '0000304' ]		
	# laddrs += [ '0000262' ]
	# laddrs += [ '0000504' ]		
	# laddrs += [ '0000462' ]			
	# laddrs += [ '0000104' ]	

	# [green diags]∘[kern:64]
	# laddrs += [ '0000464' ]
	# laddrs += [ '0000502' ]		
	# laddrs += [ '0000064' ]
	# laddrs += [ '0000102' ]		
	# laddrs += [ '0000264' ]			
	# laddrs += [ '0000302' ]	
	
	# laddrs += [ # [blue bars]∘[kern:01:03] | outer red ∘ inner yellow | singles
	# 	'1002063', # 0/2
	# 	'1220107', # F
	# 	'1002300', # 0/2
	# 	'1002365', # 0/2
	# 	'1220400', # 0/2		
	# 	'1220450', # 0/2				
	# 	'1220512', # 0/2				
	# 	'1220561', # 0/2		
	# 	'1220004', # F
	# 	'1211511', # 0/2	
	# 	'1211524', # 0/2			
	# ]
							
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
							
	sol_tuples = [diagram.nodeByAddress[addr].loop.tuple for addr in taddrs]
	sol_loops = [diagram.nodeByAddress[addr].loop for addr in laddrs]
	
	for i,t in enumerate(sol_tuples):
		for j,l in enumerate(t):
			assert diagram.extendLoop(l)
	for j,l in enumerate(sol_loops):
		assert diagram.extendLoop(l)
								
	# ============================================================================================================================================================================ #	

	def jump(diagram, old_mx, lvl=0, jump_path=[], jump_tuples=[]):
		global move_index
		move_index += 1
		
		if move_index % 1 == 0:
			#show(diagram)			
			print("[*{}*][{}][lvl:{}] {}".format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path])))
			
		new_mx = Measurement.measure(old_mx)
	
		if len(diagram.chains) is 1:
			show(diagram); print("[*{}*][{}][lvl:{}] {}".format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]))); input("=== sol ===");
			return
	
		if new_mx.min_chlen is 0: # can't further connect chains
			# show(diagram)			
			print("[*{}*][{}][lvl:{}] failed min chlen: 0".format(move_index, tstr(time() - startTime), lvl))		
			return
			
		assert len(new_mx.avloops) >= new_mx.tobex, "can't join all chains"
			
		# if new_mx.min_chlen is 0:
		# 	diagram.point(); show(diagram); input("--- min_chlen: 0 ---")
		
		#print("[*{}*][{}][lvl:{}]  uc: {} | mx: {}".format(move_index, tstr(time() - startTime), lvl, len(uc), mx))
		
		if lvl >= 95:
			diagram.point(); show(diagram); input("[*{}*][{}][lvl:{}] … uc: {} | tobex: {}".format(move_index, tstr(time() - startTime), lvl, len(new_mx.unchained_cycles), new_mx.tobex))
					
		if len(new_mx.unchained_cycles) is 0: # if all cycles have been looped	
			show(diagram)
			print("[*{}*][{}][lvl:{}] {}".format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path])))
			input("~~~ found smth ~~~")
		else:							
			mc, mt = find_min_simple(diagram, new_mx.unchained_cycles, new_mx.avtuples)
			mn = sorted([n for n in mc.nodes if n.loop.tuple in mt], key = lambda n: n.ktype)
			mt = [n.loop.tuple for n in mn]
						
			# diagram.pointers = list(itertools.chain(*[itertools.chain(*[l.nodes for l in t]) for t in mt]))
			# show(diagram)
			
			print("[*{}*][{}][lvl:{}] uc: {} | mt: ({}) {}".format(move_index, tstr(time() - startTime), lvl, len(new_mx.unchained_cycles), len(mt), " ".join(["⟨" + n.address + "|" + color_string(n.ktype) + ":" + str(n.loop.ktype_radialIndex) + "⟩" for n in mn])))
		
			for it, t in enumerate(mt):
					
				#if (lvl == 0 and it != 2):
					#continue
								
				ec = 0
				for lt, l in enumerate(t):
					if diagram.extendLoop(l):
						ec += 1
					else:
						print("[*{}*][{}][lvl:{}] failed extending it: {}".format(move_index, tstr(time() - startTime), lvl, it))
						break
		
				if ec == len(t): # if we've extended all of the tuple's loops
					jump(diagram, new_mx, lvl+1, jump_path+[(it,len(mt))], jump_tuples+[t])
		
				for l in reversed(t[:ec]):
					diagram.collapseBack(l)
		
	# ============================================================================================================================================================================ #	
					
	startTime = time()
	move_index = -1
	sols = []
	sols_file = "__6__sols__xxx__"
	
	# mc, mt = find_min_simple(diagram, mx.unchained_cycles, mx.avtuples)
	# mn = sorted([n for n in mc.nodes if n.loop.tuple in mt], key = lambda n: n.address)
	# print("mc: " + mc.address + " | mt: (" + str(len(mt)) + ") " + " ".join([n.address for n in mn]))
	# diagram.pointers = list(itertools.chain(*[itertools.chain(*[l.nodes for l in t]) for t in mt]))
	# show(diagram)
	
	# ============================================================================================================================================================================ #	
	
	# diagram.point()
	# show(diagram)	
	
	mx = Measurement.init(diagram)
	
	jump(diagram, mx, len(sol_tuples), [('§', len(sol_tuples))], list(sol_tuples))	
