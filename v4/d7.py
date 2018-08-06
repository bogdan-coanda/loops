from diagram import *
from uicanvas import *
import itertools


def extend(addr):
	assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)	

if __name__ == "__main__":
	
	diagram = Diagram(7)#, withKernel=False)

	#'''		
	show(diagram)	
	sp = diagram.superperm('000000', '000000')#, '00035')
	print(len(sp), sp)	
	'''
	diagram.makeChain([], [diagram.cycleByAddress['00000']])
		
	diagram.extendLoop(diagram.nodeByAddress['000005'].loop)
	
	diagram.extendLoop(diagram.nodeByAddress['000146'].loop)
	diagram.extendLoop(diagram.nodeByAddress['000236'].loop)
	diagram.extendLoop(diagram.nodeByAddress['000326'].loop)
	diagram.extendLoop(diagram.nodeByAddress['000416'].loop)
	
	diagram.makeChain([], [diagram.cycleByAddress['00001']])
	diagram.makeChain([], [diagram.cycleByAddress['00002']])
	diagram.makeChain([], [diagram.cycleByAddress['00003']])
	diagram.makeChain([], [diagram.cycleByAddress['00004']])
	
	diagram.nodeByAddress['000006'].nextLink = diagram.nodeByAddress['000006'].links[2]
	diagram.nodeByAddress['000016'].nextLink = diagram.nodeByAddress['000016'].links[2]
	diagram.nodeByAddress['000026'].nextLink = diagram.nodeByAddress['000026'].links[2]
	diagram.nodeByAddress['000036'].nextLink = diagram.nodeByAddress['000036'].links[2]
	'''		
	#diagram.pointers = diagram.bases
	'''
	show(diagram)	
	sp = diagram.superperm('000000', '000046')
	print(len(sp), sp)
	#'''
