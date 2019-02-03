from diagram import *
from uicanvas import *


if __name__ == "__main__":
	
	diagram = Diagram(6, 1)
	
	diagram.extendLoop(diagram.nodeByAddress['00001'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['00143'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['00201'].loop)	
	# diagram.extendLoop(diagram.nodeByAddress['00343'].loop)
		
	# diagram.extendLoop(diagram.nodeByAddress['01104'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['01205'].loop)	
	# diagram.extendLoop(diagram.nodeByAddress['01304'].loop)
	
	# diagram.extendLoop(diagram.nodeByAddress['02205'].loop)		
	
	# diagram.extendLoop(diagram.nodeByAddress['10105'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['10204'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['10305'].loop)			

	diagram.extendLoop(diagram.nodeByAddress['11005'].loop)
	diagram.extendLoop(diagram.nodeByAddress['11104'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['11205'].loop)			
		
	# diagram.extendLoop(diagram.nodeByAddress['10043'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['10034'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['10011'].loop)		
	# diagram.extendLoop(diagram.nodeByAddress['10002'].loop)
	# 
	# diagram.extendLoop(diagram.nodeByAddress['11111'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['11120'].loop)
	# 
	# diagram.extendLoop(diagram.nodeByAddress['11301'].loop)
	diagram.extendLoop(diagram.nodeByAddress['11310'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['11333'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['11342'].loop)
	# 
	# diagram.extendLoop(diagram.nodeByAddress['01211'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['01220'].loop)
	# 
	# diagram.extendLoop(diagram.nodeByAddress['01105'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['01204'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['01305'].loop)
	# 
	# diagram.extendLoop(diagram.nodeByAddress['02005'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['02104'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['02205'].loop)			
					
	show(diagram)
