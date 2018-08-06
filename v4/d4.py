from diagram import *
from uicanvas import *
import itertools


def cychain(addr):
	diagram.makeChain([], [diagram.cycleByAddress[addr]])

def extend(addr):
	assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)	

def annex(addr):
	diagram.nodeByAddress[addr].nextLink = diagram.nodeByAddress[addr].links[2]


if __name__ == "__main__":
	'''
	diagram = Diagram(4)
	
	#extend('0001')
	#extend('1203')
	#extend('1212')
	#extend('1220')
	'''	
	diagram = Diagram(4, withKernel=False)
	
	cychain('00')
	
	extend('003')		
	extend('001')
		
	cychain('12')
	annex('021')
	
	
	
	
	sp = diagram.superperm('022', '122')
	#'''	
	#sp = diagram.superperm('000', '000')
	print(len(sp), sp)
	
	show(diagram)
	
