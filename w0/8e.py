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
		
	nx += elt('0000007', 6)
	
	
	# diagram.point()
	diagram.pointers = list(itertools.chain(*[n.loop.nodes for n in nx]))	
	show(diagram)

