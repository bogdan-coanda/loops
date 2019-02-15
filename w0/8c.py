from diagram import *
from uicanvas import *
from common import *
from mx import *



if __name__ == "__main__":

	diagram = Diagram(8, 1)
	
	import enav
	enav.diagram = diagram
	from enav import *	
		
	# ---------------------------- #
	
	print(f"avcolumns: {len([col for col in diagram.columns if col.isAvailabled()])}")
	
	# diagram.pointers = [col.firstNode for col in diagram.columns]
	# show(diagram)
	
	# elt('0000007', 2) # 18
	# elt('0000007', 3)
	# elt('0000007', 4)
	# elt('0000007', 5)
	# elt('0000007', 6)
	# elt('0000007', 7)
		
	# ---------------------------- #	
	show(diagram)
