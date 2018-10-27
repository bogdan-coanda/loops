from diagram import *
from uicanvas import *
from common import *
from itertools import chain
from time import time
from collections import defaultdict


def extend(addr):
	assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	
def collapse(addr):
	diagram.collapseBack(diagram.nodeByAddress[addr].loop)
		
def coerce():
	singles = []
	coerced = []
		
	while True:
		found = False
		min_chain_avlen = len(diagram.loops)
									
		for chain in diagram.chains:
			avlen = len(chain.avloops)
			if avlen < min_chain_avlen:
				min_chain_avlen = avlen
			
			if avlen == 0:
				return (0, singles, coerced) 

			elif avlen == 1:
				avloop = list(chain.avloops)[0]
				singles.append(avloop)
				diagram.extendLoop(avloop)
				found = True
				break
			
			elif avlen == 2:
				killingFields = [loop.killingField() for loop in chain.avloops]
				intersected = killingFields[0].intersection(killingFields[1])
				if len(intersected):
					for avloop in intersected:
						coerced.append(avloop)
						diagram.setLoopUnavailabled(avloop)
					found = True																									
					break
	
		if not found:
			return (min_chain_avlen, singles, coerced)
						
#------------------------#
'''
extend('000001')
[$587] i: 394/396/601 | (587, 2, -1, 0)
0:⟨loop:[yellow:64]:100004|Ex⟩
1:⟨loop:[orange:90]:100012|Ex⟩
2:⟨loop:[green:106]:121014|Ex⟩
'''
if __name__ == "__main__":
	
	diagram = Diagram(7, 4)
	
	loop_0 = diagram.nodeByAddress['000001'].loop
	assert diagram.extendLoop(loop_0)	
	min_chain_avlen_0, singles_0, coerced_0 = coerce()
	avlen_0 = len([l for l in diagram.loops if l.availabled])
	print("[lvl:0] extended " + str(loop_0) + " | avlen: " + str(avlen_0) + " | min chlen: " + str(min_chain_avlen_0) + " | singles: " + str(singles_0) + " | coerced: " + str(coerced_0))

	loop_1 = diagram.nodeByAddress['100004'].loop
	assert diagram.extendLoop(loop_1)	
	min_chain_avlen_1, singles_1, coerced_1 = coerce()
	avlen_1 = len([l for l in diagram.loops if l.availabled])
	print("[lvl:1] extended " + str(loop_1) + " | avlen: " + str(avlen_1) + " | min chlen: " + str(min_chain_avlen_1) + " | singles: " + str(singles_1) + " | coerced: " + str(coerced_1))

	loop_2 = diagram.nodeByAddress['100012'].loop
	assert diagram.extendLoop(loop_2)	
	min_chain_avlen_2, singles_2, coerced_2 = coerce()
	avlen_2 = len([l for l in diagram.loops if l.availabled])
	print("[lvl:2] extended " + str(loop_2) + " | avlen: " + str(avlen_2) + " | min chlen: " + str(min_chain_avlen_2) + " | singles: " + str(singles_2) + " | coerced: " + str(coerced_2))

	loop_3 = diagram.nodeByAddress['121014'].loop
	assert diagram.extendLoop(loop_3)	
	min_chain_avlen_3, singles_3, coerced_3 = coerce()
	avlen_3 = len([l for l in diagram.loops if l.availabled])
	print("[lvl:3] extended " + str(loop_3) + " | avlen: " + str(avlen_3) + " | min chlen: " + str(min_chain_avlen_3) + " | singles: " + str(singles_3) + " | coerced: " + str(coerced_3))
							
	diagram.point()
	show(diagram)
