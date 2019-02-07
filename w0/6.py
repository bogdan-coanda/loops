from diagram import *
from uicanvas import *


def extend(addr):
	assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	
def et(addr):
	for node in diagram.nodeByAddress[addr].tuple:
		assert diagram.extendLoop(node.loop)

def L2():
	for i in range(len(diagram.pointers)):
		diagram.pointers[i] = diagram.pointers[i].links[2].next if i % 2 == 0 else diagram.pointers[i].prevs[2].node
		
def L1():			
	for i in range(len(diagram.pointers)):
		diagram.pointers[i] = diagram.pointers[i].links[1].next if i % 2 == 0 else diagram.pointers[i].prevs[1].node
					
def jump():
	L1();	L1(); L1(); L1(); L1(); L2()
																
def ex():
	for i in range(len(diagram.pointers)):
		if i % 2 == 0:
			diagram.extendLoop(diagram.pointers[i].loop)
		else:
			diagram.extendLoop(diagram.pointers[i].prevs[1].node.loop)
	
		
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
