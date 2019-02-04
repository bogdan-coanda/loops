from diagram import *
from uicanvas import *


if __name__ == "__main__":
	
	diagram = Diagram(6, 1)
	
	diagram.pointers = [
		diagram.nodeByAddress['00001'],
		diagram.nodeByAddress['00143'].links[1].next,
		diagram.nodeByAddress['00201'],
		diagram.nodeByAddress['00343'].links[1].next
	]
	
	print(diagram.pointers)
	
	#print([node.links[1].next for node in diagram.pointers])
	'''
	#diagram.jmp(0); #show(diagram)
	# diagram.adv(3); #show(diagram)
	
	def L2():
		for i in range(len(diagram.pointers)):
			diagram.pointers[i] = diagram.pointers[i].links[2].next if i % 2 == 0 else diagram.pointers[i].prevs[2].node
			
	def L1():			
		for i in range(len(diagram.pointers)):
			diagram.pointers[i] = diagram.pointers[i].links[1].next if i % 2 == 0 else diagram.pointers[i].prevs[1].node
						
													
	#for i in range(len(diagram.pointers)):
		#diagram.pointers[i] = diagram.pointers[i].links[1].next.links[1].next.links[1].next if i % 2 == 0 else diagram.pointers[i].prevs[1].node.prevs[1].node.prevs[1].node
		#diagram.pointers[i] = diagram.pointers[i].links[2].next if i % 2 == 0 else diagram.pointers[i].links[1].next.prevs[2].node
	
	# diagram.jmp(0); 
	
	def extend():
		for i in range(len(diagram.pointers)):
			if i % 2 == 0:
				diagram.extendLoop(diagram.pointers[i].loop)
			else:
				diagram.extendLoop(diagram.pointers[i].prevs[1].node.loop)
	
	def jump():
		L1();	L1(); L1(); L1(); L1(); L2()
	
	#show(diagram)		
		
	#extend()	
	
	#save(diagram);		
	L2()
	#save(diagram)
	L1()
	#save(diagram)
	L1()
	
	#save(diagram)		
	extend()			
	#save(diagram)												
	L2(); L1();	L1(); L1()
	
	#save(diagram)		
	extend()
	#save(diagram)	
	L2(); jump(); jump(); L1(); L1(); L1()
	
	#save(diagram)
	extend()
	#save(diagram)	
	L1(); L1(); L2(); L1()

	#save(diagram)	
	extend()
	#save(diagram)
	L2(); jump(); jump(); jump(); L1(); L1(); L1(); 
	
	#save(diagram)
	extend()
	#save(diagram)	
	L2(); L1(); L1(); L1()                                                                                                                                                                                                                        
	
	#save(diagram)
	extend()
	#save(diagram)
							
	'''	
	
	#diagram.extendLoop(diagram.nodeByAddress['00001'].loop)	
	# diagram.extendLoop(diagram.nodeByAddress['00143'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['00201'].loop)	
	#diagram.extendLoop(diagram.nodeByAddress['00343'].loop)
								
	assert diagram.extendLoop(diagram.nodeByAddress['10105'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['10204'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['10305'].loop)			

	assert diagram.extendLoop(diagram.nodeByAddress['11005'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['11104'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['11205'].loop)			

	assert diagram.extendLoop(diagram.nodeByAddress['10043'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['10034'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['10011'].loop)		
	assert diagram.extendLoop(diagram.nodeByAddress['10002'].loop)

	assert diagram.extendLoop(diagram.nodeByAddress['11111'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['11120'].loop)

	assert diagram.extendLoop(diagram.nodeByAddress['11301'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['11310'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['11333'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['11342'].loop)

	assert diagram.extendLoop(diagram.nodeByAddress['01211'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['01220'].loop)

	assert diagram.extendLoop(diagram.nodeByAddress['01105'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['01204'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['01305'].loop)

	assert diagram.extendLoop(diagram.nodeByAddress['02005'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['02104'].loop)
	assert diagram.extendLoop(diagram.nodeByAddress['02205'].loop)			
					
	show(diagram)
	#'''
