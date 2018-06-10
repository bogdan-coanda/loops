import ui
from diagram import *
from colorsys import hls_to_rgb
from random import random
from uicanvas import *
from itertools import chain


if __name__ == "__main__":
	
	diagram = Diagram(7)
	
	diagram.generateKernel()
	
	# first wave: fill with disconnected cycled
	# A. uniform blues
	
	'''
	for loop in diagram.loops:
		if loop.head.ktype is 0:
			diagram.extendLoop(loop)
	
	diagram.collapseLoop(diagram.nodeByAddress['123006'].loop)
	diagram.extendLoop(diagram.nodeByAddress['123050'].loop)
	diagram.extendLoop(diagram.nodeByAddress['123010'].loop)
	diagram.extendLoop(diagram.nodeByAddress['123045'].loop)

	diagram.collapseLoop(diagram.nodeByAddress['103016'].loop)	
	diagram.extendLoop(diagram.nodeByAddress['103012'].loop)
	'''
	
	## for n in diagram.nodeByAddress['123005'].loop.nodes:
		## diagram.extendLoop(n.links[1].next.loop)
	
	
	diagram.extendLoop(diagram.nodeByAddress['123040'].loop)
	diagram.extendLoop(diagram.nodeByAddress['123030'].loop)
	diagram.extendLoop(diagram.nodeByAddress['123020'].loop)
	diagram.extendLoop(diagram.nodeByAddress['123010'].loop)
	diagram.extendLoop(diagram.nodeByAddress['123000'].loop)
	# '''
	
	diagram.extendLoop(diagram.nodeByAddress['123001'].loop)
	
	show(diagram)
	diagram.measure()
