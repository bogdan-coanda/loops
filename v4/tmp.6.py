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

def extendGreen(column_addr):
	for i in range(diagram.spClass-2):
		extendAddress(column_addr+str(i)+str(4-i))
									
			
if __name__ == "__main__":
	
	diagram = Diagram(6)#, withKernel=False)
	patch(diagram)
	
	extendColumn('100', 3)
	extendColumn('101', 2)
	extendAddress('01302')
		
	extendAddress('10224')
	#extendAddress('10233')
	#extendAddress('11103')
	#extendAddress('12004')
	#extendAddress('12013')
	# extendGreen('121')
	# 
	# extendAddress('10105')
	# extendAddress('10205')
	# extendAddress('11105')
	# extendAddress('11305')
	
	#extendGreen('121')
	
	#extendAddress('00001')
	#extendAddress('01343')
	
	# 
	# extendColumn('100', 2)
	# extendColumn('101', 1)
	# extendColumn('122', 0)
	# extendColumn('121', 1)
	# extendColumn('010', 0)
	
	diagram.pointers = [cycle.avnode() for cycle in diagram.cycles if cycle.chain is None and len([n for n in cycle.nodes if n.loop.availabled]) < 2]
	show(diagram)
