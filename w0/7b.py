from diagram import *
from uicanvas import *
from mx import *


def L2():
	for i in range(len(diagram.pointers)):
		diagram.pointers[i] = diagram.pointers[i].links[2].next if (i % 2 == 0 or diagram.spClass % 2 == 1) else diagram.pointers[i].prevs[2].node
		
def L1():			
	for i in range(len(diagram.pointers)):
		diagram.pointers[i] = diagram.pointers[i].links[1].next if (i % 2 == 0 or diagram.spClass % 2 == 1) else diagram.pointers[i].prevs[1].node
					
def JP(count=1):
	for i in range(count):
		for j in range(diagram.spClass-1):
			L1();
		L2()
																
def EX():
	for i in range(len(diagram.pointers)):
		if i % 2 == 0 or diagram.spClass % 2 == 1:
			diagram.extendLoop(diagram.pointers[i].loop)
		else:
			diagram.extendLoop(diagram.pointers[i].prevs[1].node.loop)
			
			
if __name__ == "__main__":
	
	diagram = Diagram(7, 1)
	mx = MX(diagram)

	diagram.extendLoop(diagram.nodeByAddress['000001'].loop)	
	
	show(diagram)
				
