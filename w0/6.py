from diagram import *
from uicanvas import *


def L2():
	for i in range(len(diagram.pointers)):
		diagram.pointers[i] = diagram.pointers[i].links[2].next if i % 2 == 0 else diagram.pointers[i].prevs[2].node
		
def L1():			
	for i in range(len(diagram.pointers)):
		diagram.pointers[i] = diagram.pointers[i].links[1].next if i % 2 == 0 else diagram.pointers[i].prevs[1].node
					
def JP():
	L1();	L1(); L1(); L1(); L1(); L2()
																
def EX():
	for i in range(len(diagram.pointers)):
		if i % 2 == 0:
			diagram.extendLoop(diagram.pointers[i].loop)
		else:
			diagram.extendLoop(diagram.pointers[i].prevs[1].node.loop)
				
def jump(lvl=0, path=[]):
	global sols
	
	# show(diagram)
	# input2(f"[lvl:{lvl}] {'.'.join([(str(x)+upper(t)) for x,t in path])}")
			
	if lvl == 6:
		if len(diagram.chains) == 1:
			show(diagram)
			input2(f"[lvl:{lvl}][sols:{sols}] {'.'.join([(str(x)+upper(t)) for x,t in path])}")
			sols += 1
		return
	
	diagram.point()		
	for it, tuple in enumerate([n.tuple for n in diagram.pointer_sample]):
		ec = 0
		for node in tuple:
			if not diagram.extendLoop(node.loop):
				break
			else:
				ec += 1
		
		if ec == len(tuple):				
			jump(lvl+1, path+[(it, len(tuple))])
		
		for node in reversed(tuple[:ec]):
			diagram.collapseBack(node.loop)	
			
	# show(diagram)
	# input2(f"[lvl:{lvl}] exit")
		
		
if __name__ == "__main__":
		
	diagram = Diagram(6, 1)
	
	import enav
	enav.diagram = diagram
	from enav import *
		
	# extend('00043')
	# 
	# sols = 0
	# jump()
	# 
	# diagram.collapseBack(diagram.nodeByAddress['00043'].loop)
		
	# ==================================== #
		
	# diagram.pointers = [
	# 	diagram.nodeByAddress['00001'],
	# 	diagram.nodeByAddress['00143'].links[1].next,
	# 	diagram.nodeByAddress['00201'],
	# 	diagram.nodeByAddress['00343'].links[1].next
	# ]
	# 
	# L2(); JP(); JP(); JP(); L1(); EX()

	# ==================================== #
				
	# ∘ bases
	#extend('00001')
	#et('00001')
		
	# ∘ orange/purple
	#et('12000')		
	#et('12023')		
		
	# ∘ blue/green
	#et('01105')
	#et('01204')
	#et('01305')
	
	# ∘ yellow/red
	#et('12012')
	
	# ==================================== #

	# ∘ bases
	#extend('00042')

	# ∘ blue/green		
	# et('01104')
	# et('01205')
	# et('01304')

	# ∘ yellow/red		
	# et('12010')
	
	# ∘ orange/purple
	# et('12000')
	# et('12034')

	# ==================================== #

	# ∘ bases
	# extend('00001') # {a}
	# extend('00002') # {b}
	# extend('00042') # {y}
	extend('00043') # {z}

	# ∘ blue
	eb('01', 1) # {az}
	# eg('01', 1) # {by}
		
	# ∘ long column 
	# elt('10005', 3) # {a}	
	# elt('10004', 3) # {y}	
	# elt('10204', 2) # {b}	
	elt('10205', 2) # {z}
		
	# ∘ short column
	# est('10205', 2) # {a}	
	# est('10204', 2) # {y}
	# est('10004', 3) # {b}	
	# est('10005', 3) # {z}
			
	# ∘ green
	# et('10204') # {a}
	# et('10205') # {y}
	# et('10005') # {b}
	# et('10004') # {z}

	# ==================================== #

	# ∘ bases
	# et('00001') # {.a}
	# et('00002') # {b.}
	# et('00042') # {.y}
	# et('00043') # {z.}		

	diagram.point()	
	# diagram.draw_boxes = [('00', 0), ('01', 0), ('00', 1), ('00', 3), ('11', 5), ('12', 4), ('12', 5)]
	#diagram.pointers = [diagram.nodeByAddress['10133'].tuple[1]]
	show(diagram)
