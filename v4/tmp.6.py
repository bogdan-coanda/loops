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

									
			
if __name__ == "__main__":
	
	diagram = Diagram(6)#, withKernel=False)
	patch(diagram)

	extendAddress('10044')
	extendAddress('10134')
	extendAddress('10224')
	extendAddress('10314')

	#±# extendAddress('12044')
	extendAddress('12134')
	extendAddress('12224')
	extendAddress('12314')		
	extendAddress('10241')
	
	# extendAddress('10140')
	# extendAddress('11213')
	# extendAddress('12113')
	
	# extendAddress('11025')
	# extendAddress('12035')		
	
	# extendAddress('11312')
	
	extendAddress('11130')
	
	diagram.pointers = diagram.nodeByAddress['12044'].loop.nodes; show(diagram); input('missing yellow');
	
	
	# extendAddress('10231')
	# extendAddress('11213')						
	# extendAddress('12113')
	# 
	# 
	# extendAddress('11144')
	# extendAddress('11223')	
	# 
	# extendAddress('10241')
	# 
	# extendAddress('11005')
	# extendAddress('12035')
		
	diagram.pointers = []
	
	nodes = [cycle.avnode() if len([n for n in cycle.nodes if n.loop.availabled]) is 1 else cycle for cycle in diagram.cycles if cycle.chain is None and len([n for n in cycle.nodes if n.loop.availabled]) < 2]
	if len(nodes):
		diagram.pointers += list(nodes)
	
	chain = sorted(diagram.chains, key = lambda chain: len(chain.avloops))[0]
	print(chain, len(chain.avloops))
	if len(chain.avloops) is 1:
		diagram.pointers += [[n for n in loop.nodes if n.cycle.chain is chain][0] for loop in chain.avloops]
	elif len(chain.avloops) is 0:
		diagram.pointers += [cycle.avnode() if len([n for n in cycle.nodes if n.loop.availabled]) is 1 else cycle for cycle in chain.cycles]
	
	if len(diagram.pointers) is 0:
		diagram.pointers = sorted([cycle for cycle in diagram.cycles if cycle.chain is None], key = lambda cycle: (len([n for n in cycle.nodes if n.loop.availabled]), cycle.address))[0:1]

	# cy0 = [node.cycle for node in diagram.nodeByAddress['10231'].loop.nodes]
	# cy1 = [node.cycle for node in diagram.nodeByAddress['11213'].loop.nodes]
	# cy2 = [node.cycle for node in diagram.nodeByAddress['12113'].loop.nodes]
	# pairs = [(loop, set([node.cycle for node in loop.nodes])) for loop in diagram.loops]
	# loops = [loop for loop,set in pairs if len(set.intersection(cy0)) and len(set.intersection(cy1)) and len(set.intersection(cy2))]
	# for il,loop in enumerate(loops):
	# 	diagram.pointers = loop.nodes; show(diagram); input("#"+str(il))
			
	show(diagram)
