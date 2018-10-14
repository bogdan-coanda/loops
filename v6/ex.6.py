from diagram import *
from uicanvas import *

def extend(addr):
	on = original.nodeByAddress[addr]
	dn = diagram.nodeByPerm[on.perm]
	assert diagram.extendLoop(dn.loop) 
	
def point(diagram):
	diagram.pointers = []
		
	if len(diagram.chains) is 1 and len(list(diagram.chains)[0].cycles) is len(diagram.cycles):
		return
		
	cycle_avlen, smallest_cycle_group = (len(diagram.cycles), [])
	sorted_empty_cycles = sorted(groupby([cycle for cycle in diagram.cycles if cycle.chain is None], K = lambda cycle: len([n for n in cycle.nodes if n.loop.availabled])).items())
	if len(sorted_empty_cycles):
		cycle_avlen, smallest_cycle_group = sorted_empty_cycles[0]
	
	chain_avlen, smallest_chain_group = (len(diagram.cycles), [])
	sorted_chain_groups = sorted(groupby(diagram.chains, K = lambda chain: len(chain.avloops)).items())
	if len(sorted_chain_groups) > 0:
		chain_avlen, smallest_chain_group	= sorted_chain_groups[0]		

	min_avlen = min(cycle_avlen, chain_avlen)
	if min_avlen == cycle_avlen:
		diagram.pointers += [cycle.avnode() if min_avlen is not 0 else cycle for cycle in smallest_cycle_group]
	if min_avlen == chain_avlen:
		diagram.pointers += itertools.chain(*[[[n for n in loop.nodes if n.cycle.chain is chain][0] for loop in chain.avloops] if min_avlen is not 0 else chain.cycles for chain in smallest_chain_group])						
	
def recolor():
	for node in original.nodes:
		diagram.nodeByPerm[node.perm].ktype = node.ktype
	for cycle in original.cycles:
		diagram.nodeByPerm[cycle.avnode().perm].cycle.index = cycle.index
	
	for ktype in range(6):
		for i in range(24):
			#if diagram.loopsByKType[ktype][i].firstNode().address == '10005':
				#print("[loop:10005] ktype: " + str(ktype) + " | i: " + str(i) + " | ktype_index: " + str(diagram.loopsByKType[ktype][i].ktype_index) + " ⇒ " + str(original.loopsByFirstPerm[diagram.loopsByKType[ktype][i].firstNode().perm].ktype_index) + " | loop: " + str(diagram.loopsByKType[ktype][i]) + " | firstNode: " + str(diagram.loopsByKType[ktype][i].firstNode()) + " | perm: " + str(diagram.loopsByKType[ktype][i].firstNode().perm))

			diagram.loopsByKType[ktype][i].ktype = original.loopsByFirstPerm[diagram.loopsByKType[ktype][i].firstPerm()].ktype
			diagram.loopsByKType[ktype][i].ktype_index = original.loopsByFirstPerm[diagram.loopsByKType[ktype][i].firstPerm()].ktype_index

			# diagram.loopsByKType[ktype][i] = original.loopsByKType[ktype][i]
			
if __name__ == "__main__":
	
	original = Diagram(6, 3) 
	
	diagram = Diagram(6, 3)#, original.nodeByAddress['00005'].links[1].next.perm)
	# diagram = Diagram(6, 1, original.nodeByAddress['02231'].links[1].next.perm)
		
	# diagram = Diagram(6, 3, original.nodeByAddress['00005'].links[1].next.perm)
	# diagram = Diagram(6, 0, original.nodeByAddress['00014'].links[1].next.perm)
	# diagram = Diagram(6, 0, original.nodeByAddress['00024'].loopBrethren[3].links[1].next.perm)
	# diagram = Diagram(6, 0, original.nodeByAddress['00034'].loopBrethren[2].links[1].next.perm)
	# diagram = Diagram(6, 0, original.nodeByAddress['00044'].loopBrethren[1].links[1].next.perm)
	# diagram = Diagram(6, 3, original.nodeByAddress['00004'].loopBrethren[0].links[1].next.perm)
	
	#diagram = Diagram(6, 0, original.nodeByAddress['01105'].links[1].next.perm)
		
	# diagram = Diagram(6, 0, original.nodeByAddress['00004'].links[1].next.perm)
	# diagram = Diagram(6, 0, original.nodeByAddress['00014'].links[1].next.perm)
	# diagram = Diagram(6, 0, original.nodeByAddress['00024'].links[1].next.perm)
	# diagram = Diagram(6, 0, original.nodeByAddress['00034'].links[1].next.perm)
	# diagram = Diagram(6, 0, original.nodeByAddress['00044'].links[1].next.perm)
	
	#diagram = Diagram(6, 0, original.nodeByAddress['11030'].perm)
	# diagram = Diagram(6, 0, original.nodeByAddress['11005'].links[1].next.perm)
	# diagram = Diagram(6, 0, original.nodeByAddress['11015'].links[1].next.perm)
	# diagram = Diagram(6, 0, original.nodeByAddress['11025'].links[1].next.perm)
	# diagram = Diagram(6, 0, original.nodeByAddress['11035'].links[1].next.perm)
	# diagram = Diagram(6, 0, original.nodeByAddress['11045'].links[1].next.perm)
	#diagram = Diagram(6, 0, original.nodeByAddress['10032'].perm)
	#diagram = Diagram(6, 0, original.nodeByAddress['10031'].perm)
	#diagram = Diagram(6, 3, original.nodeByAddress['12342'].perm)
	#diagram = Diagram(6, 0, original.nodeByAddress['00002'].perm)
	#diagram = Diagram(6, 0, original.nodeByAddress['00005'].perm)

	recolor()
		
	for main_loop in diagram.loopsByKType[0]:
		main_ktype = main_loop.ktype
		main_ktype_index = main_loop.ktype_index
		adjacent_ktypes = [main_ktype]
		adjacent_pairs = []
		for main_node in main_loop.nodes:
			assert main_node.links[1].next.links[1].next.prevs[2].node.loop.ktype != main_ktype
			# assert main_node.links[1].next.links[1].next.prevs[2].node.loop.ktype_index == main_ktype_index
			assert main_node.links[1].next.links[1].next.prevs[2].node.loop.ktype not in adjacent_ktypes
			adjacent_ktypes.append(main_node.links[1].next.links[1].next.prevs[2].node.loop.ktype)
			adjacent_pairs.append((main_node.links[1].next.links[1].next.prevs[2].node.loop.ktype, main_node.links[1].next.links[1].next.prevs[2].node.loop.ktype_index))
		print("main ktype: " + str(main_ktype) + " | index: " + str(main_ktype_index) + " | adj: " + str(adjacent_pairs))	
	
	# extend('00005') #   blue # ⟨0:0-1-2-3-4⟩ 
	# extend('00014')
	# extend('00024')
	# extend('00034')
	# extend('00044')
	#extend('00004')
	# extend('12345')
	# extend('11225')
	#extend('00040')
	#extend('00030')

		
	#extend('00004') #  green #  ⟨0:0=4⟩   | ⟨1:8⟩ - ⟨2:12⟩ - ⟨3:16⟩
		
	#extend('00005') #   blue # ⟨0:0-1-2-3-4⟩ 
	
	# extend('00130') # violet #  ⟨1:8=9⟩   | ⟨0:4⟩  - ⟨12:64⟩ -  ⟨4:24⟩   
	# extend('10220') #    red # ⟨14:72=73⟩ | ⟨2:12⟩ -  ⟨1:8⟩  - ⟨17:88⟩
	# extend('02310') # orange # ⟨11:56=57⟩ | ⟨2:12⟩ -  ⟨3:16⟩ - ⟨19:96⟩
	# extend('00300') # yellow #  ⟨3:15=16⟩ | ⟨0:0⟩  -  ⟨9:45⟩ -  ⟨6:30⟩

	### « #5 | sol » @ v4/sols.6.py ###			
	''' ktypes:
	0 ⇒   blue
	1 ⇒  green
	2 ⇒ yellow
	3 ⇒ orange
	4 ⇒    red
	5 ⇒ violet
	'''
	
	# every cycle has its own chain at start
	# for cycle in diagram.cycles:
	# 	if cycle.chain is None:
	# 		diagram.makeChain([], [cycle])			
	
	extend('00001') #    red:12 # adj: [orange:8,  yellow:19,  green:13,   blue:12, violet:0 ] | ⟨  0: 80: 65: 61: 60⟩ | §80 §65
	extend('11005') #   blue:16 # adj: [violet:16, orange:16,    red:16, yellow:16,  green:16] | ⟨ 80: 81: 82: 83: 84⟩ | §80  	
	extend('10105') #   blue:13 # adj: [violet:13, orange:13, yellow:13,    red:13,  green:13] | ⟨ 65: 66: 67: 68: 69⟩ | §65
	extend('02302') # violet:22 # adj: [   red:10,  green:23,   blue:22, yellow:19, orange:2]  | ⟨ 55:115:111:110: 95⟩ | $110 $95	
	extend('12022') #  green:22 # adj: [orange:4,     red:21,   blue:22, violet:23, yellow:17] | ⟨102:106:110:114:118⟩ | $110
	extend('11305') #   blue:19 # adj: [yellow:19, violet:19, orange:19,    red:19,  green:19] | ⟨ 95: 96: 97: 98: 99⟩ | $95	
	extend('01033') # orange:12 # adj: [violet:4,    blue:12, yellow:21,  green:23,    red:8 ] | ⟨ 23: 63: 62:107:103⟩ | £63 £103 | #other-mid#
	extend('10030') # yellow:12 # adj: [ green:15,    red:19, violet:10, orange:21,   blue:12] | ⟨ 63: 79: 94:109: 64⟩ | £63 £.79 £.94 £.109 
	extend('10242') # yellow:20 # adj: [   red:2,  violet:17,   blue:20,  green:23, orange:15] | ⟨ 74: 89:104:103:119⟩ | £103 £,104 £,89 £,74
	extend('10205') #   blue:14	# adj: [orange:14, yellow:14,    red:14, violet:14,  green:14] | ⟨ 70: 71: 72: 73: 74⟩ | £,74  
	extend('10305') #   blue:15 # adj: [yellow:15,    red:15, violet:15, orange:15,  green:15] | ⟨ 75: 76: 77: 78: 79⟩ | £.79 
	# extend('11105') #   blue:17 # adj: [orange:17,    red:17, yellow:17, violet:17,  green:17] | ⟨ 85: 86: 87: 88: 89⟩ | £,89 
	extend('11205') #   blue:18 # adj: [   red:18, yellow:18, violet:18, orange:18,  green:18] | ⟨ 90: 91: 92: 93: 94⟩ | £.94 
	extend('12004') #  green:20 # adj: [  blue:20, orange:21,    red:6,  violet:19, yellow:23] | ⟨100:104:108:112:116⟩ | £,104 
	extend('12013') #  green:21 # adj: [orange:20,   blue:21,    red:22, violet:11, yellow:14] | ⟨101:105:109:113:117⟩ | £.109
	# 
	# setRadialCoords(diagram)	
	
	# diagram.pointers = []
	# 
	# np = diagram.nodeByAddress['01033']
	# nq = diagram.nodeByAddress['01034']
	# 
	# diagram.pointers += [np, nq]
	# 
	# def jmp(x, times = 1):				
	# 	global np, nq
	# 	for _ in range(times):
	# 		np = np.links[x].next
	# 		nq = nq.prevs[x].node
	# 
	# 		diagram.pointers += [np, nq]
	# 
	# jmp(2)
	# jmp(1)
	# jmp(2)
	# jmp(1, 3)
	# 
	# jmp(2)
	# jmp(1, 5)
	# jmp(2)
	# jmp(1, 5)
	# jmp(2)
	# jmp(1, 5)
	# jmp(2)
	# jmp(1, 5)
	# jmp(2)
	# 
	# jmp(1)
	# jmp(2)
	# jmp(1, 2)
	# 
	# jmp(2)
	# jmp(1, 5)
	# jmp(2)
	# jmp(1, 5)
	# jmp(2)
	# jmp(1, 5)
	# jmp(2)
	# jmp(1, 5)
	# jmp(2)	
			
	# extend('01222') # 0/2
	# extend('01022') # 0/2
	# extend('01230') # 0/2
	# extend('01103') # 0/2
	# extend('01122') # 1/2
	# extend('01323') # 0/1
	# extend('02204') # 0/1
	# extend('02231') # 0/1
	# 
	# extend('01230') # 0/1
			
	point(diagram)
	show(diagram)
	
	# main_loop = diagram.nodeByAddress['01033'].loop
	# diagram.collapseBack(main_loop)
	# 
	# for adj_loop in main_loop.adjacentLoops():
	# 	diagram.extendLoop(adj_loop)
	# 	show(diagram)
	# 	diagram.collapseBack(adj_loop)
	
