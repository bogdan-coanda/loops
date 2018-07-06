from diagram import *
from uicanvas import *
from groupby import *


if __name__ == "__main__":
	
	diagram = Diagram(8)
	diagram.generateKernel()

	sparkNode = diagram.nodeByAddress['0000001']
	diagram.extendLoop(sparkNode.loop)
	
	
	print("unlooped cycles: " + str(len([c for c in diagram.cycles if c.chained_by_count is 0])))
	print("cycle av counts: " + str(sorted(groupby([c for c in diagram.cycles if c.chained_by_count is 0], K = lambda c: c.available_loops_count, G = lambda g: len(g)).items())))	
			
	show(diagram)
