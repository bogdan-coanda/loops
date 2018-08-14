from diagram import *
from uicanvas import *
from common import *
import itertools


def patch(diagram):
	
	diagram.makeChain([], [diagram.cycleByAddress['0100']])
	diagram.extendLoop(diagram.nodeByAddress['01005'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['0110']])
	diagram.extendLoop(diagram.nodeByAddress['01105'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['0120']])
	diagram.extendLoop(diagram.nodeByAddress['01205'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['0130']])
	diagram.extendLoop(diagram.nodeByAddress['01305'].loop)
	
	diagram.nodeByAddress['01045'].nextLink = diagram.nodeByAddress['01045'].links[3]
	diagram.nodeByAddress['01145'].nextLink = diagram.nodeByAddress['01145'].links[3]
	diagram.nodeByAddress['01245'].nextLink = diagram.nodeByAddress['01245'].links[3]
	diagram.nodeByAddress['01345'].nextLink = diagram.nodeByAddress['01345'].links[3]
			
	diagram.nodeByAddress['00345'].nextLink = Link(4, diagram.nodeByAddress['00345'], diagram.nodeByAddress['01000'])
	diagram.nodeByAddress['01345'].nextLink = Link(4, diagram.nodeByAddress['01345'], diagram.nodeByAddress['00000'])
	
	diagram.makeChain(list(diagram.chains), [])
		
	# every cycle has its own chain at start
	#for cycle in diagram.cycles:
		#if cycle.chain is None:
			#diagram.makeChain([], [cycle])					

def jmp(x):
	diagram.jmp(x); show(diagram); input("[jmp] » "+str(x))
	
def adv(x):
	diagram.adv(x); show(diagram); input("[adv] » "+str(x))
	

if __name__ == "__main__":
	
	with open('sols.6.partial_2_4D.txt', 'r') as file:
		lines = file.read().splitlines()
		
	print(len(lines))

	diagram = Diagram(6)
					
	sols = []
	for id in range(772):
		sols.append(sorted([diagram.nodeByAddress[addr].loop.firstNode().address for addr in lines[id*5+2].split('addr: ')[1].split(' ')]))
	sols = sorted(sols)
	

	for sindex,sol in enumerate(sols):
		
			diagram = Diagram(6)
			patch(diagram)
			
			for addr in sol:
				diagram.extendLoop(diagram.nodeByAddress[addr].loop)
				
			show(diagram)	
			input("#"+str(sindex))
