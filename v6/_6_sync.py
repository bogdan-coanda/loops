from diagram import *
from uicanvas import *
from common import *
from itertools import chain
from time import time

if __name__ == "__main__":
	
	diagram = Diagram(6, 3)
	
	def extend(addr):
		assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	def collapse(addr):
		diagram.collapseBack(diagram.nodeByAddress[addr].loop)
	def single():
		singles = []
		diagram.point()
		while diagram.pointer_avlen == 1 and len(diagram.pointers):
			singles.append(diagram.pointers[0].loop)
			diagram.extendLoop(diagram.pointers[0].loop)
			diagram.point()
		return singles			
		
	results = []		
	
	startTime = time()
	
	avloops_0 = [l for l in diagram.loops if l.availabled]
	print("avloops_0: " + str(len(avloops_0)))
	
	for il_0, loop_0 in enumerate(avloops_0):
		diagram.extendLoop(loop_0)
		singles_0 = single()		
		
		if diagram.pointer_avlen == 0:
			results.append(((0, 1, 0, 0), (loop_0)))
		
		else:
			avloops_1 = [l for l in diagram.loops if l.availabled]
			#print("avloops_1: " + str(len(avloops_1)))
			
			for il_1, loop_1 in enumerate(avloops_1):
				diagram.extendLoop(loop_1)
				singles_1 = single()

				if diagram.pointer_avlen == 0:
					results.append(((0, 2, 0, 0), (loop_0, loop_1)))
				else:
					avloops_2 = [l for l in diagram.loops if l.availabled]
					#print("avloops_1: " + str(len(avloops_1)))
					
					for il_2, loop_2 in enumerate(avloops_2):
						diagram.extendLoop(loop_2)
						singles_2 = single()

						if diagram.pointer_avlen == 0:
							results.append(((0, 3, 0, 0), (loop_0, loop_1, loop_2)))				
						else:
							result = ((diagram.pointer_avlen, 3, -(len(singles_0)+len(singles_1)+len(singles_2)), len([l for l in diagram.loops if l.availabled])), (loop_0, loop_1, loop_2))
							if il_1 % 100 == 0 and il_2 == 0:
								print("["+tstr(time() - startTime)+"] @ " + str(il_0) + "/" + str(len(avloops_0)) + " " + str(il_1) + "/" + str(len(avloops_1)) + " " + str(il_2) + "/" + str(len(avloops_2)))
							results.append(result)
						
						for l in reversed(singles_2):
							diagram.collapseBack(l)					
						diagram.collapseBack(loop_2)
				
				for l in reversed(singles_1):
					diagram.collapseBack(l)					
				diagram.collapseBack(loop_1)
								
		for l in reversed(singles_0):
			diagram.collapseBack(l)					
		diagram.collapseBack(loop_0)
		
	print("["+tstr(time() - startTime)+"][trial] ---")
	grouped = sorted(groupby(results, 
		K = lambda result: result[0],
		V = lambda result: result[1]#,
		#G = lambda g: len(g)
	).items())
	diagram.pointers = list(set(chain(*[[l.firstNode() for l in ls] for ls in grouped[0][1]])))
	show(diagram)
	print("["+tstr(time() - startTime)+"](avlen | loops | -singles | availabled): loop_count\n" + "\n".join(str(g[0])+": "+str(len(g[1])) for g in grouped) + "\naddrs: \n"+" ".join([str([l.firstAddress() for l in ls]) for ls in grouped[0][1]]))				
