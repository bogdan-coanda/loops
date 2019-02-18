from diagram import *
from uicanvas import *


if __name__ == "__main__":
		
	diagram = Diagram(6, 1)
	
	import enav
	enav.diagram = diagram
	from enav import *
	
	# ------------------------------ #
	
	extend('00001')
	
	el('10005', 3)
	es('12305', 2)
	el('12205', 5)
	es('12105', 4)
	
	#et('10105')
	#et('11005')
	#extend('01205')
	
	# ------------------------------ #
	
	diagram.point()
	show(diagram)
