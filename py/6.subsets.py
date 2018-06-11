from diagram import *
from uicanvas import *
from itertools import chain
							
	
if __name__ == "__main__":
	
	diagram = Diagram(6)
	diagram.loadExtenders()
	
	maxcommon_pair = (0, 0)
	maxcommon_count = 0
	seen = set()
	for i in range(len(diagram.extenders)):
		for j in range(i+1, len(diagram.extenders)):
			common = len(set(diagram.extenders[i]).intersection(diagram.extenders[j]))
			if common >= maxcommon_count:
				maxcommon_count = common
				maxcommon_pair = (i, j)				
				if (maxcommon_count >= 24):
					print("@ " + str(i) + " » " + str(maxcommon_count) + " | " + str(maxcommon_pair))
					if i in seen or j in seen:
						print("» » » third")
					seen.add(i)
					seen.add(j)
						
	print(str(maxcommon_count) + " | " + str(maxcommon_pair))
	
