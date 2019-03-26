from diagram import *
from uicanvas import *


def cOc(segment):
	for i,x in enumerate(segment):
		if x in [' ', '-']:
			pass
		elif x == 'b':
			assert diagram.connectOpenChain('l3b')
		elif x == '+':
			assert diagram.connectOpenChain(4)
		else:
			assert diagram.connectOpenChain(int(x))		
			

if __name__ == "__main__":

	diagram = Diagram(6, kernelPath='222')
	cOc('2322 2232 2223 2222')

	with open('6.sols.txt', 'r', encoding="utf8") as log:
		for sol, line in enumerate(log):
			for addr in line.split():
				diagram.nodeByAddress[addr].loop.sols.add(sol)
				
	sloops = sorted([loop for loop in diagram.loops if loop.available], key = lambda loop: -len(loop.sols))
	for loop in sloops[:10] + sloops[-10:]:
		print(f"{loop}: {len(loop.sols)}")
	
	n0 = diagram.nodeByAddress['00001']
	diagram.extendLoop(n0.loop)
	
	for loop in diagram.loops:
		loop.sols.intersection_update(n0.loop.sols)	

	n1 = diagram.nodeByAddress['00211']
	diagram.extendLoop(n1.loop)
	
	for loop in diagram.loops:
		loop.sols.intersection_update(n1.loop.sols)	

	n2 = diagram.nodeByAddress['00111']
	diagram.extendLoop(n2.loop)
	
	for loop in diagram.loops:
		loop.sols.intersection_update(n2.loop.sols)	

	n3 = diagram.nodeByAddress['00043']
	diagram.extendLoop(n3.loop)
	
	for loop in diagram.loops:
		loop.sols.intersection_update(n3.loop.sols)	
																														
	min_sol_count = min([len(loop.sols) for loop in diagram.loops if loop.available and len(loop.sols) > 0])
	diagram.pointers = [node for node in diagram.nodes if len(node.loop.sols) == min_sol_count]
	
			
	show(diagram)
