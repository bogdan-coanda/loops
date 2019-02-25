from diagram import *
from uicanvas import *
from common import *
from mx import *
from time import time


if __name__ == "__main__":

	diagram = Diagram(8, 0)
	mx = MX(diagram)
		
	import enav
	enav.diagram = diagram
	from enav import *	

	nx = []

	# ---------------------------- #
		
	nx += el('0000007', diagram.bases[0].links[1].next.links[1].next.links[1].next.links[1].next.links[1].next.links[1].next.links[1].next.ktype)
	nx += el('0000107', diagram.bases[1].prevs[1].node.prevs[1].node.prevs[1].node.prevs[1].node.prevs[1].node.prevs[1].node.prevs[1].node.ktype)
	nx += el('0000207', diagram.bases[2].links[1].next.links[1].next.links[1].next.links[1].next.links[1].next.links[1].next.links[1].next.ktype)
	nx += el('0000307', diagram.bases[3].prevs[1].node.prevs[1].node.prevs[1].node.prevs[1].node.prevs[1].node.prevs[1].node.prevs[1].node.ktype)
	nx += el('0000407', diagram.bases[4].links[1].next.links[1].next.links[1].next.links[1].next.links[1].next.links[1].next.links[1].next.ktype)
	nx += el('0000507', diagram.bases[5].prevs[1].node.prevs[1].node.prevs[1].node.prevs[1].node.prevs[1].node.prevs[1].node.prevs[1].node.ktype)
		
	nx = elt('1000007', 3)
	nx = elt('0100007', 2)
	# nx = elt('0011007', 5)
		
	# nx += el('1000007', 6)
	# nx += el('0001507', 2)	
	# nx += el('0210207', 4)
	
	# diagram.point()
	diagram.pointers = list(itertools.chain(*[n.loop.nodes for n in nx]))
	show(diagram)

