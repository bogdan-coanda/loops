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

	diagram = Diagram(6, kernelPath='222', drawSolCounts=True)
	cOc('2322 2232 2223 2222')
	# cOc('2322 2232 2223 2222 4222 2322 2232 2223 2222 4222 2322 2232 2223 2222')

	with open('6.K1.sols.txt', 'r', encoding="utf8") as log:
		for sol, line in enumerate(log):
			for addr in line.split():
				diagram.nodeByAddress[addr].loop.sols.add(sol)
				
	sloops = sorted([loop for loop in diagram.loops if loop.available], key = lambda loop: -len(loop.sols))
	for loop in sloops[:10] + sloops[-10:]:
		print(f"{loop}: {len(loop.sols)}")
	
	n0 = diagram.nodeByAddress['01305']
	diagram.extendLoop(n0.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n0.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n1 = diagram.nodeByAddress['01205']
	diagram.extendLoop(n1.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n1.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n2 = diagram.nodeByAddress['01005']
	diagram.extendLoop(n2.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n2.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)
																			
	n3 = diagram.nodeByAddress['01105']
	diagram.extendLoop(n3.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n3.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n4 = diagram.nodeByAddress['02004']
	diagram.extendLoop(n4.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n4.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n5 = diagram.nodeByAddress['02104']
	diagram.extendLoop(n5.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n5.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n6 = diagram.nodeByAddress['02204']
	diagram.extendLoop(n6.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n6.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n7 = diagram.nodeByAddress['02304']
	diagram.extendLoop(n7.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n7.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n8 = diagram.nodeByAddress['11205']
	diagram.extendLoop(n8.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n8.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n9 = diagram.nodeByAddress['10104']
	diagram.extendLoop(n9.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n9.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n10 = diagram.nodeByAddress['12105']
	diagram.extendLoop(n10.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n10.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n11 = diagram.nodeByAddress['11005']
	diagram.extendLoop(n11.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n11.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n12 = diagram.nodeByAddress['11105']
	diagram.extendLoop(n12.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n12.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n13 = diagram.nodeByAddress['12005']
	diagram.extendLoop(n13.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n13.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n14 = diagram.nodeByAddress['12344']
	diagram.extendLoop(n14.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n14.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n15 = diagram.nodeByAddress['12321']
	diagram.extendLoop(n15.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n15.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)

	n16 = diagram.nodeByAddress['12312']
	diagram.extendLoop(n16.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n16.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)
	
	n17 = diagram.nodeByAddress['12303']
	diagram.extendLoop(n17.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n17.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)
	
	n18 = diagram.nodeByAddress['10003']
	diagram.extendLoop(n18.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n18.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)
	
	n19 = diagram.nodeByAddress['10130']
	diagram.extendLoop(n19.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n19.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)
	
	n20 = diagram.nodeByAddress['10110']
	diagram.extendLoop(n20.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n20.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)
	
	n21 = diagram.nodeByAddress['10205']
	diagram.extendLoop(n21.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n21.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)
	
	n22 = diagram.nodeByAddress['10330']
	diagram.extendLoop(n22.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n22.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)
	
	n23 = diagram.nodeByAddress['10020']
	diagram.extendLoop(n23.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n23.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)
	
	n24 = diagram.nodeByAddress['02220']
	diagram.extendLoop(n24.loop)

	for loop in diagram.loops:
		loop.sols.intersection_update(n24.loop.sols)	
		if len(loop.sols) == 0 and loop.available:
			diagram.setLoopUnavailable(loop)
	#'''
	# max_sol_count = max([len(loop.sols) for loop in diagram.loops if loop.available and len(loop.sols) > 0]) if len(diagram.chains) > 1 else -1
	# diagram.pointers = [node for node in diagram.nodes if node.loop.available and len(node.loop.sols) == max_sol_count]

									
	show(diagram)
