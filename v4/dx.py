from diagram import *
from uicanvas import *
import itertools


def ext(addr):
	for node in diagram.nodeByAddress[addr].tuple:
		assert diagram.extendLoop(node.loop)
	diagram.pointers = itertools.chain(*[node.loop.nodes for node in diagram.nodeByAddress[addr].tuple])
		

if __name__ == "__main__":
	
	diagram = Diagram(7)
	
	
	
	ext('100002')
	ext('100011')
	ext('100020')
	ext('100044')
	ext('100053')
	
	ext('100205')
	
	diagram.extendLoop(diagram.nodeByAddress['000001'].loop)
	diagram.pointers = diagram.nodeByAddress['000001'].loop.nodes
	
	ext('100106')
	'''
	ext('100211')
	ext('100220')
	ext('100244')
	diagram.pointers = itertools.chain(*[itertools.chain(*[node.loop.nodes for node in diagram.nodeByAddress[addr].tuple]) for addr in ['100211', '100220', '100244']]) #'''
	
	ext('100210')
	ext('100234')
	ext('100243')
	diagram.pointers = itertools.chain(*[itertools.chain(*[node.loop.nodes for node in diagram.nodeByAddress[addr].tuple]) for addr in ['100210', '100234', '100243']]) #'''
	'''
	ext('123012')
	ext('123021')
	ext('123030')
	
	diagram.extendLoop(diagram.nodeByAddress['110010'].loop)
	diagram.pointers = diagram.nodeByAddress['110010'].loop.nodes
	'''
	
	#diagram.extendLoop(diagram.nodeByAddress['001126'].loop)
	#diagram.extendLoop(diagram.nodeByAddress['021006'].loop)
	
	#diagram.extendLoop(diagram.nodeByAddress['022001'].loop)
	
	ext('103400')
	diagram.extendLoop(diagram.nodeByAddress['103424'].loop)
	diagram.extendLoop(diagram.nodeByAddress['103433'].loop)
	diagram.extendLoop(diagram.nodeByAddress['103442'].loop)
	diagram.extendLoop(diagram.nodeByAddress['103451'].loop)
	
	#diagram.extendLoop(diagram.nodeByAddress['013022'].loop)
	
	grouped_cycles_by_av = sorted(groupby([c for c in diagram.cycles if c.chain is None], K = lambda c: (len([node for node in c.nodes if node.loop.availabled]), -len([node for node in c.nodes if node.loop.availabled and len([n for n in node.loop.nodes if n.cycle.chain is not None]) > 0]))).items())
	avcycle = grouped_cycles_by_av[0][1][0] if len(grouped_cycles_by_av) else None
	avnodes = sorted([node for node in avcycle.nodes if node.loop.availabled], key = lambda node: (-len([n for n in node.loop.nodes if n.cycle.chain is not None]), node.address)) if avcycle else None
	
	diagram.pointers = avnodes
	
	show(diagram)
