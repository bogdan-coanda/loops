from diagram import *
from uicanvas import *


def extend(addr):
	assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	
def et(addr):
	for node in diagram.nodeByAddress[addr].tuple:
		assert diagram.extendLoop(node.loop)


if __name__ == "__main__":
		
	diagram = Diagram(6, 1)
	
	et('00001')
	
	# ∘ orange
	# extend('12000')
	# extend('12023')
	# extend('12032')
	# extend('12041')
			
	# ∘ purple
	# extend('12200')
	# extend('12223')
	# extend('12232')
	# extend('12241')

	et('12000')		
	et('12023')		
	
	# ------- #
	
	# ∘ blue/green
	#et('01105')
	#et('01204')
	#et('01305')
	
	# ∘ yellow/red
	#et('12012')
	
	show(diagram)
