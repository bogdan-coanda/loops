from diagram import *
from uicanvas import *


if __name__ == "__main__":
		
	diagram = Diagram(6, 0)
	
	import enav
	enav.diagram = diagram
	from enav import *
	
	# ------------------------------ #

	el('00005', diagram.bases[0].ktype)
	el('00105', diagram.bases[1].ktype)
	el('00205', diagram.bases[2].ktype)
	el('00305', diagram.bases[3].ktype)
			
	el('00105', 4)
			
	# extend('00001')
	# 
	# el('10005', 3)
	# es('12305', 2)
	# el('12205', 5)
	# es('12105', 4)
	
	#et('10105')
	#et('11005')
	#extend('01205')
	
	# ------------------------------ #
	
	diagram.point()
	show(diagram)
