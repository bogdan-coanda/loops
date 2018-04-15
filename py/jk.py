from diagram import *
from time import time
from math import floor


def tstr(s):
	return "" + str(int(floor(s / 60))) + "m" + str(int(floor(s)) % 60) + "s." + str(int(s * 1000) % 1000)


def jk(diagram, lvl = 0, state = []):
					
	diagram.jkcc += 1	

	diagram.measureNodes()
	
	if diagram.drawn.looped_count == len(diagram.perms):
		print("!!!Found!!! @time: " + tstr(time() - diagram.startTime) + " | lvl: " + str(lvl) + " | " + " ".join([str(pair[0]) + "/" + str(pair[1]) + (("(" + str(pair[2]) + ")") if pair[2] > 0 else "") + ":" + pair[3] for pair in state]))
		return
		
	if diagram.drawn.unreachable_cycle_count > 0:
		return
		
	singlesCount = len(diagram.drawn.singles)
	availables = [diagram.drawn.singles.pop()] if singlesCount > 0 else diagram.drawn.availables
	lvl_seen = []
	
	cc = 0
	for node in availables:
		if not node.seen:
			
			if diagram.extendLoop(node):
				jk(diagram, lvl + 1, state + [(cc, len(availables), singlesCount, node.perm)])
				diagram.collapseLoop(node)

			node.seen = True
			lvl_seen.append(node)				
		cc += 1
		
	for node in lvl_seen:
		node.seen = False
	return			




if __name__ == "__main__":
	
	diagram = Diagram(6)
	diagram.startTime = time()
	jk(diagram)
	print("---")
