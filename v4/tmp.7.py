from diagram import *
from uicanvas import *
import itertools


def patch(diagram):
	
	for head in ['001', '002', '003']:
								
		diagram.makeChain([], [diagram.cycleByAddress[head+'00']])
		diagram.extendLoop(diagram.nodeByAddress[head+'006'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'10']])
		diagram.extendLoop(diagram.nodeByAddress[head+'106'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'20']])
		diagram.extendLoop(diagram.nodeByAddress[head+'206'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'30']])
		diagram.extendLoop(diagram.nodeByAddress[head+'306'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'40']])
		diagram.extendLoop(diagram.nodeByAddress[head+'406'].loop)	
		
		diagram.nodeByAddress[head+'056'].nextLink = diagram.nodeByAddress[head+'056'].links[3]
		diagram.nodeByAddress[head+'156'].nextLink = diagram.nodeByAddress[head+'156'].links[3]
		diagram.nodeByAddress[head+'256'].nextLink = diagram.nodeByAddress[head+'256'].links[3]
		diagram.nodeByAddress[head+'356'].nextLink = diagram.nodeByAddress[head+'356'].links[3]
		diagram.nodeByAddress[head+'456'].nextLink = diagram.nodeByAddress[head+'456'].links[3]
		
	diagram.nodeByAddress['000456'].nextLink = Link(4, diagram.nodeByAddress['000456'], diagram.nodeByAddress['001000'])
	diagram.nodeByAddress['001456'].nextLink = Link(4, diagram.nodeByAddress['001456'], diagram.nodeByAddress['002000'])
	diagram.nodeByAddress['002456'].nextLink = Link(4, diagram.nodeByAddress['002456'], diagram.nodeByAddress['003000'])
	diagram.nodeByAddress['003456'].nextLink = Link(4, diagram.nodeByAddress['003456'], diagram.nodeByAddress['000000'])
	
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
	
	diagram = Diagram(7, withKernel=False)
	#patch(diagram)
	
	extendColumn('0000', 1)
	extendColumn('1001', 0)
	extendColumn('1002', 2)
	extendColumn('1002', 0)
	extendColumn('1003', 0)
	
	#extendColumn('100', 3)
	#extendColumn('101', 2)
	#extendAddress('01302')
		
	#extendAddress('10224')
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
