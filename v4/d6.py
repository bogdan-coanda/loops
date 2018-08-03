from diagram import *
from uicanvas import *
import itertools


def ext(addr):
	for node in diagram.nodeByAddress[addr].tuple:
		assert diagram.extendLoop(node.loop)
	diagram.pointers = itertools.chain(*[node.loop.nodes for node in diagram.nodeByAddress[addr].tuple])
	
def extend(addr):
	assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)	

if __name__ == "__main__":
	
	diagram = Diagram(6)
	
	extend('00001')
	
	
	diagram.pointers = diagram.bases
	show(diagram)
	
