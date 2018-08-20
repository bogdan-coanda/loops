from diagram import *
from uicanvas import *
import itertools


def patch(diagram):
	
	for head in ['01', '02']:
								
		diagram.makeChain([], [diagram.cycleByAddress[head+'00']])
		diagram.extendLoop(diagram.nodeByAddress[head+'005'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'10']])
		diagram.extendLoop(diagram.nodeByAddress[head+'105'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'20']])
		diagram.extendLoop(diagram.nodeByAddress[head+'205'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'30']])
		diagram.extendLoop(diagram.nodeByAddress[head+'305'].loop)
		
		diagram.nodeByAddress[head+'045'].nextLink = diagram.nodeByAddress[head+'045'].links[3]
		diagram.nodeByAddress[head+'145'].nextLink = diagram.nodeByAddress[head+'145'].links[3]
		diagram.nodeByAddress[head+'245'].nextLink = diagram.nodeByAddress[head+'245'].links[3]
		diagram.nodeByAddress[head+'345'].nextLink = diagram.nodeByAddress[head+'345'].links[3]
		
	diagram.nodeByAddress['00345'].nextLink = Link(4, diagram.nodeByAddress['00345'], diagram.nodeByAddress['01000'])
	diagram.nodeByAddress['01345'].nextLink = Link(4, diagram.nodeByAddress['01345'], diagram.nodeByAddress['02000'])
	diagram.nodeByAddress['02345'].nextLink = Link(4, diagram.nodeByAddress['02345'], diagram.nodeByAddress['00000'])
	
	diagram.makeChain(list(diagram.chains), [])		
	

def extendAddress(addr):
	assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
		
def extendColumn(column_addr, key):
	i = 0
	j = key
	while i < diagram.spClass-1:
		extendAddress(column_addr+str(i)+str(j))
		if j > 0:
			i += 1
			j -= 1
		else:
			i += 2
			j = diagram.spClass - 3


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
									
def tonoavail(addr):
	loop = diagram.nodeByAddress[addr].loop
	loop.seen = True
	diagram.setLoopUnavailabled(loop)
	
	
			
if __name__ == "__main__":
	
	diagram = Diagram(6)#, withKernel=False)
	patch(diagram)

	# every cycle has its own chain at start
	# for cycle in diagram.cycles:
	# 	if cycle.chain is None:
	# 		diagram.makeChain([], [cycle])		
			
	# extendAddress('10005')
	extendAddress('10105')
	extendAddress('10205')
	extendAddress('10305')

	extendAddress('11005')
	extendAddress('11105')
	extendAddress('11205')
	extendAddress('11305')
	
	# extendAddress('12005')
	# extendAddress('12105')
	# extendAddress('12205')
	# extendAddress('12305')
	
	# ~~~ #
	
	tonoavail('10005')
	tonoavail('12005')
	tonoavail('12105')
	tonoavail('12205')
	tonoavail('12305')	
	
	extendAddress('10014')
	
	extendAddress('12104')
	extendAddress('12113')
	extendAddress('12222')
	
	extendAddress('11301')
	extendAddress('10044')
	extendAddress('12341')
	extendAddress('10020')
	
	
	point(diagram)			
	show(diagram)
