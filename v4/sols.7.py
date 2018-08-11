from diagram import *
from uicanvas import *
from common import *
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
	
	
def jmp(x):
	diagram.jmp(x); show(diagram); input("[jmp] » "+str(x))
	
def adv(x):
	diagram.adv(x); show(diagram); input("[adv] » "+str(x))

def exp(addr=None):
	if addr:
		diagram.pointers = diagram.nodeByAddress[addr].tuple		
	for node in diagram.pointers:
		assert diagram.extendLoop(node.loop)	
		
		
if __name__ == "__main__":
	
	diagram = Diagram(7, isDualWalkType=True, baseAddresses=['000001', '003402'])
	patch(diagram)

	#diagram.pointers = [n for n in diagram.nodes if n.tuple[0] is n.tuple[1]]; show(diagram); input("singled tuples after patch")
			
	# every cycle has its own chain at start
	#for cycle in diagram.cycles:
		#if cycle.chain is None:
			#diagram.makeChain([], [cycle])		
			
			
			
	diagram.pointers = list(diagram.bases)
	
	diagram.extendLoop(diagram.nodeByAddress['000001'].loop)
	
	diagram.extendLoop(diagram.nodeByAddress['110006'].loop)
	diagram.extendLoop(diagram.nodeByAddress['110106'].loop)
	diagram.extendLoop(diagram.nodeByAddress['110206'].loop)
	diagram.extendLoop(diagram.nodeByAddress['110306'].loop)			
	diagram.extendLoop(diagram.nodeByAddress['110406'].loop)			

	diagram.extendLoop(diagram.nodeByAddress['101006'].loop)
	diagram.extendLoop(diagram.nodeByAddress['101106'].loop)
	diagram.extendLoop(diagram.nodeByAddress['101206'].loop)
	diagram.extendLoop(diagram.nodeByAddress['101306'].loop)			
	diagram.extendLoop(diagram.nodeByAddress['101406'].loop)			

	diagram.extendLoop(diagram.nodeByAddress['100106'].loop)
	diagram.extendLoop(diagram.nodeByAddress['100206'].loop)
	diagram.extendLoop(diagram.nodeByAddress['100306'].loop)			
	diagram.extendLoop(diagram.nodeByAddress['100406'].loop)
	
	diagram.extendLoop(diagram.nodeByAddress['100020'].loop)
	#diagram.extendLoop(diagram.nodeByAddress['100030'].loop)
	diagram.extendLoop(diagram.nodeByAddress['100040'].loop)			

	diagram.extendLoop(diagram.nodeByAddress['120005'].loop)
	diagram.extendLoop(diagram.nodeByAddress['120105'].loop)
	diagram.extendLoop(diagram.nodeByAddress['120205'].loop)
	diagram.extendLoop(diagram.nodeByAddress['120405'].loop)
	
	diagram.extendLoop(diagram.nodeByAddress['120215'].loop)			
	diagram.extendLoop(diagram.nodeByAddress['120351'].loop)			
	
	# diagram.extendLoop(diagram.nodeByAddress['123006'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['123106'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['123206'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['123306'].loop)			
	# diagram.extendLoop(diagram.nodeByAddress['123406'].loop)			

	diagram.extendLoop(diagram.nodeByAddress['102005'].loop)
	diagram.extendLoop(diagram.nodeByAddress['102105'].loop)
	diagram.extendLoop(diagram.nodeByAddress['102205'].loop)
	diagram.extendLoop(diagram.nodeByAddress['102305'].loop)	
	diagram.extendLoop(diagram.nodeByAddress['102405'].loop)

	# diagram.extendLoop(diagram.nodeByAddress['103005'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['103105'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['103205'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['103305'].loop)	
	# diagram.extendLoop(diagram.nodeByAddress['103405'].loop)

	diagram.extendLoop(diagram.nodeByAddress['113005'].loop)
	diagram.extendLoop(diagram.nodeByAddress['113105'].loop)
	diagram.extendLoop(diagram.nodeByAddress['113205'].loop)
	diagram.extendLoop(diagram.nodeByAddress['113305'].loop)	
	diagram.extendLoop(diagram.nodeByAddress['113405'].loop)
																					
	show(diagram)
