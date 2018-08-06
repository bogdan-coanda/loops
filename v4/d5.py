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
	#'''
	diagram = Diagram(5)
	
	#extend('0001')
	#extend('1203')
	#extend('1212')
	#extend('1220')
	
	'''
	diagram = Diagram(5, withKernel=False)
	
	#cychain('000')
	#extend('0004')
	
	#extend('0001')
	#extend('1020')
	#extend('1110')
	#extend('1131')
	#extend('1200')
	#extend('0104')
	
	cychain('020'); annex('0204')
	cychain('021'); annex('0214')
	cychain('022')
	
	extend('1110')
	extend('0004')
	extend('0001')	
	#extend('1200')
	#extend('0104')
	#extend('1020')
	#extend('1131')
	
	
	
	sp = diagram.superperm('0200', '0224')
	#'''	
	sp = diagram.superperm('0000', '0000')
	print(len(sp), sp)
	
	show(diagram)
