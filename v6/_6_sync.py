from diagram import *
from uicanvas import *
from common import *
from itertools import chain


if __name__ == "__main__":
	
	diagram = Diagram(7, 4)
	
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
	
	avloops_0 = [l for l in diagram.loops if l.availabled]
	print("avloops_0: " + str(len(avloops_0)))
	
	for il_0, loop_0 in enumerate(avloops_0):
		diagram.extendLoop(loop_0)
		singles_0 = single()		
		
		if diagram.pointer_avlen == 0:
			results.append(((0, -len(singles_0), len([l for l in diagram.loops if l.availabled]), -len(diagram.pointers)), (loop_0, None)))
		
		else:
			avloops_1 = [l for l in diagram.loops if l.availabled]
			#print("avloops_1: " + str(len(avloops_1)))
			
			for il_1, loop_1 in enumerate(avloops_1):
				diagram.extendLoop(loop_1)
				singles_1 = single()
		
				result = ((diagram.pointer_avlen, (-len(singles_0), -len(singles_1)), len([l for l in diagram.loops if l.availabled]), -len(diagram.pointers)), (loop_0, loop_1))
				#print("[trial] " + str(result))
				if il_1 % 100 == 0:
					print("@ " + str(il_0) + "/" + str(len(avloops_0)) + " " + str(il_1) + "/" + str(len(avloops_1)))
				results.append(result)

				for l in reversed(singles_1):
					diagram.collapseBack(l)					
				diagram.collapseBack(loop_1)
								
		for l in reversed(singles_0):
			diagram.collapseBack(l)					
		diagram.collapseBack(loop_0)
		
	print("[trial] ---")
	grouped = sorted(groupby(results, 
		K = lambda result: result[0],
		V = lambda result: result[1]#,
		#G = lambda g: len(g)
	).items())
	diagram.pointers = chain(*[[l.firstNode() for l in ls] for ls in grouped[0][1]])
	show(diagram)
	input("(avlen | -singles | availabled | -pointers): loop_count\n" + "\n".join(str(g[0])+": "+str(len(g[1])) for g in grouped) + "\nloops: \n"+"\n".join(list(itertools.chain(*[[str(l) for l in ls] for ls in grouped[0][1]]))) + "\naddrs: \n"+" ".join(list(itertools.chain(*[[l.firstAddress() for l in ls] for ls in grouped[0][1]]))))				
