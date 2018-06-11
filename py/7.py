from diagram import *
from uicanvas import *
from itertools import chain
							
	
if __name__ == "__main__":
	
	diagram = Diagram(7)
	diagram.generateKernel()
	
	def qp(lvl=0):
				
		if lvl >= 40:
			show(diagram)
			loopedCount, chains, avs = diagram.measure()
			input("[lvl: "+str(lvl)+"]")
		else:
			loopedCount, chains, avs = diagram.measure()
		
		# final end
		if loopedCount == len(diagram.nodes):
			if len(chains) is 1:
				show(diagram)
				input('!!!Found!!!')
				return
			else:
				return

		# dead end [~] stopped apriori
		#if len(diagram.rx_unreachables) is not 0:
			#return						
			
		# singles
		if len(diagram.rx_singles) is not 0:
			avs = [list(diagram.rx_singles)[0].availabled_node().loop]
			
		# filter and sort avs
		# ...
		
		lvl_seen = []		
		cc = 0
		for loop in avs:
			if diagram.extendLoop(loop):
			
				if len(diagram.rx_unreachables) is 0:	
					qp(lvl+1)
					
				diagram.collapseLoop(loop)
				diagram.forceUnavailable([loop])
				lvl_seen.append(loop)				
			cc += 1
		diagram.forceAvailable(lvl_seen)
	
	qp()				
	print("~~~§~~~")
