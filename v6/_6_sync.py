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
	
	avloops = [l for l in diagram.loops if l.availabled]
	avlen = len(avloops)
	print("avlen: " + str(avlen))
	
	for i0 in range(avlen):
		loop0 = avloops[i0]		
		diagram.extendLoop(loop0)
				
		for i1 in range(i0+1, avlen):
			loop1 = avloops[i1]
			if loop1.availabled:
				diagram.extendLoop(loop1)
				
				for i2 in range(i1+1, avlen): 
					loop2 = avloops[i2]
					if loop2.availabled:
						diagram.extendLoop(loop2)
						
						singles = single()
						if diagram.pointer_avlen == 0:
							results.append(((0, 0, -len(singles)), [l.firstAddress() for l in [loop0, loop1, loop2]]))										
						else:
							results.append(((len([l for l in avloops if l.availabled]), diagram.pointer_avlen, -len(singles)), [l.firstAddress() for l in [loop0, loop1, loop2]]))
	
						if i2 < i1+5:
							print("["+tstr(time() - startTime)+"] @ " + str(i0) + " " + str(i1) + " " + str(i2) + " /" + str(avlen))	
	
						for l in reversed(singles):
							diagram.collapseBack(l)		
										
						diagram.collapseBack(loop2)
				diagram.collapseBack(loop1)
		diagram.collapseBack(loop0)
			
	print("["+tstr(time() - startTime)+"][trial] ---")
	grouped = sorted(groupby(results, 
		K = lambda result: result[0],
		V = lambda result: result[1]#,
		#G = lambda g: len(g)
	).items())
	diagram.pointers = [diagram.nodeByAddress[addr] for addr in set(chain(*grouped[0][1]))]
	show(diagram)
	print("["+tstr(time() - startTime)+"](availabled | pointer_avlen | -singles): loop_count\n" + "\n".join(str(g[0])+": "+str(len(g[1])) for g in grouped) + "\naddrs: \n"+" ".join([str(ls) for ls in grouped[0][1]]))				
