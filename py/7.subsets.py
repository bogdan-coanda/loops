from diagram import *
from uicanvas import *
from itertools import chain
							
	
if __name__ == "__main__":
	
	diagram = Diagram(8)
	
	
	diagram.generateKernel()
	# diagram.extendLoop(diagram.nodeByAddress['0000001'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['0000165'].loop)		
	# diagram.extendLoop(diagram.nodeByAddress['0000201'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['0000365'].loop)	
	# diagram.extendLoop(diagram.nodeByAddress['0000401'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['0000565'].loop)

	diagram.nodeByAddress['0000001'].loopBrethren[0].cycle.chainMarker = 1
	diagram.nodeByAddress['0000165'].loopBrethren[0].cycle.chainMarker = 1
	diagram.nodeByAddress['0000001'].loopBrethren[1].cycle.chainMarker = 2
	diagram.nodeByAddress['0000165'].loopBrethren[1].cycle.chainMarker = 2
	diagram.nodeByAddress['0000001'].loopBrethren[2].cycle.chainMarker = 3
	diagram.nodeByAddress['0000165'].loopBrethren[2].cycle.chainMarker = 3
	diagram.nodeByAddress['0000001'].loopBrethren[3].cycle.chainMarker = 4
	diagram.nodeByAddress['0000165'].loopBrethren[3].cycle.chainMarker = 4				
	diagram.nodeByAddress['0000001'].loopBrethren[4].cycle.chainMarker = 5
	diagram.nodeByAddress['0000165'].loopBrethren[4].cycle.chainMarker = 5				
	diagram.nodeByAddress['0000001'].loopBrethren[5].cycle.chainMarker = 6
	diagram.nodeByAddress['0000165'].loopBrethren[5].cycle.chainMarker = 6						

	diagram.nodeByAddress['0000201'].loopBrethren[0].cycle.chainMarker = 5
	diagram.nodeByAddress['0000365'].loopBrethren[0].cycle.chainMarker = 5
	diagram.nodeByAddress['0000201'].loopBrethren[1].cycle.chainMarker = 6
	diagram.nodeByAddress['0000365'].loopBrethren[1].cycle.chainMarker = 6
	diagram.nodeByAddress['0000201'].loopBrethren[2].cycle.chainMarker = 1
	diagram.nodeByAddress['0000365'].loopBrethren[2].cycle.chainMarker = 1
	diagram.nodeByAddress['0000201'].loopBrethren[3].cycle.chainMarker = 2
	diagram.nodeByAddress['0000365'].loopBrethren[3].cycle.chainMarker = 2
	diagram.nodeByAddress['0000201'].loopBrethren[4].cycle.chainMarker = 3
	diagram.nodeByAddress['0000365'].loopBrethren[4].cycle.chainMarker = 3
	diagram.nodeByAddress['0000201'].loopBrethren[5].cycle.chainMarker = 4
	diagram.nodeByAddress['0000365'].loopBrethren[5].cycle.chainMarker = 4

	diagram.nodeByAddress['0000401'].loopBrethren[0].cycle.chainMarker = 3
	diagram.nodeByAddress['0000565'].loopBrethren[0].cycle.chainMarker = 3
	diagram.nodeByAddress['0000401'].loopBrethren[1].cycle.chainMarker = 4
	diagram.nodeByAddress['0000565'].loopBrethren[1].cycle.chainMarker = 4
	diagram.nodeByAddress['0000401'].loopBrethren[2].cycle.chainMarker = 5
	diagram.nodeByAddress['0000565'].loopBrethren[2].cycle.chainMarker = 5
	diagram.nodeByAddress['0000401'].loopBrethren[3].cycle.chainMarker = 6
	diagram.nodeByAddress['0000565'].loopBrethren[3].cycle.chainMarker = 6
	diagram.nodeByAddress['0000401'].loopBrethren[4].cycle.chainMarker = 1
	diagram.nodeByAddress['0000565'].loopBrethren[4].cycle.chainMarker = 1
	diagram.nodeByAddress['0000401'].loopBrethren[5].cycle.chainMarker = 2
	diagram.nodeByAddress['0000565'].loopBrethren[5].cycle.chainMarker = 2
																					
	'''																				
	show(diagram)
	diagram.measure()
	input()
	#'''																			
																						
	diagram.forceUnavailable(set(chain(*[[node.loop for node in cycle.nodes if node.loop.availabled] for cycle in diagram.cycles if cycle.isKernel])))
	diagram.forceUnavailable(set([loop for loop in diagram.loops if loop.availabled and len(set([node.cycle.chainMarker for node in loop.nodes if node.cycle.chainMarker is not None])) > 1]))
	
	def mark(loop, marker):
		diagram.extendLoop(loop)
		for node in loop.nodes:
			node.cycle.chainMarkeras = marker

	def forward(node, count):
		for _ in range(count):
			node = node.links[1].next
		return node

	def backward(node, count):
		for _ in range(count):
			node = node.prevs[1].node
		return node

	H001 = diagram.nodeByAddress['0000001']
	H201 = diagram.nodeByAddress['0000201'] 		
	H401 = diagram.nodeByAddress['0000401']
	K165 = diagram.nodeByAddress['0000165']
	K365 = diagram.nodeByAddress['0000365']
	K565 = diagram.nodeByAddress['0000565']
	
	bases = [H001, K165, H201, K365, H401, K565]
	nodes = list(bases)
		
	def jmp(bid):
		for i in range(len(nodes)):
			if i % 2 == 0:
				nodes[i] = nodes[i].loopBrethren[bid]
			else:
				nodes[i] = nodes[i].loopBrethren[-1-bid]
		diagram.pointers = nodes				
		#print("[jmp]", nodes[0])
				
	def adv(cid):
		for i in range(len(nodes)):
			if i % 2 == 0:
				for _ in range(cid):
					nodes[i] = nodes[i].links[1].next
			else:
				for _ in range(cid):
					nodes[i] = nodes[i].prevs[1].node
		diagram.pointers = nodes					
		#print("[adv] cid: "+str(cid))
					
	def nxt():
		for i in range(len(nodes)):
			if i % 2 == 0:
				nodes[i] = nodes[i].nextLink.next
			else:
				nodes[i] = nodes[i].prevLink.node
		#diagram.pointers = nodes				
		#print("[nxt]", nodes[0])
										
	def extend():		
		for i,node in enumerate(nodes):
			#print("[ext] "+str(i)+": "+str(node))
			assert diagram.extendLoop(node.loop), "failed to extend " + str(node) + " @ " + str(i)
			for nln in node.loopBrethren:
				#print("[ext] nln: "+str(node))
				assert nln.cycle.chainMarker is None or node.cycle.chainMarker is None or nln.cycle.chainMarker is node.cycle.chainMarker
				nln.cycle.chainMarker = node.cycle.chainMarker
		diagram.forceUnavailable(set([loop for loop in diagram.loops if loop.availabled and len(set([node.cycle.chainMarker for node in loop.nodes if node.cycle.chainMarker is not None])) > 1]))				
		
	def chk():	
		#print("[chk]")
		global nodes
		_p = diagram.pointers
		nodes = list(bases)
		chkcc = 0
		for _ in range(diagram.spClass-1):		
			jmp(0)
			if nodes[0].cycle.isKernel:
				continue
			elif nodes[0].chainID is None:
				for _ in range(diagram.spClass):
					adv(1)
					avcc = 0
					for node in nodes:
						if node.loop.availabled:
							avcc += 1
					assert avcc is 0 or avcc is len(nodes)												
					if avcc is not 0:
						chkcc += 1
			else:
				first = nodes[0]
				nxt()
				while nodes[0] != first:
					avcc = 0
					for node in nodes:
						if node.loop.availabled:
							avcc += 1
					assert avcc is 0 or avcc is len(nodes)
					if avcc is not 0:
						chkcc += 1				
					nxt()				
		diagram.pointers = _p
		#diagram.pointers = nodes
		#print("[chk] cc: " + str(chkcc))

	chk()
							
	# step 0 #
	
	jmp(0); adv(5); extend()
	chk()	
	jmp(0); adv(5); 
	jmp(0); adv(6); extend()									
	chk()
	jmp(0); adv(5); 
	jmp(0); adv(6); 
	jmp(5); adv(3); extend()
	chk()
	
	# step 1 #
	
	jmp(1); adv(4); extend()
	chk()
	jmp(2); adv(3); extend()
	chk()
	jmp(3); adv(2); extend()
	chk()		
	jmp(4); adv(6); extend()
	chk()
	jmp(5); adv(5); extend()
	chk()	

	# step 2 #
	
	jmp(0); adv(5); 
	jmp(0); adv(6);
	jmp(3); adv(5);
	jmp(5); adv(5);
	for i,m in enumerate([2, 5, 6, 3, 4, 1]):
		nodes[i].cycle.chainMarker = m			
	extend()
	chk()
	
	jmp(0); adv(5); 
	jmp(0); adv(6);
	jmp(3); adv(5);
	jmp(4); adv(6);
	for i,m in enumerate([3, 4, 1, 2, 5, 6]):
		nodes[i].cycle.chainMarker = m			
	extend()
	chk()
	
	jmp(0); adv(5); 
	jmp(0); adv(6);
	jmp(3); adv(5);
	jmp(3); adv(7);
	for i,m in enumerate([4, 3, 2, 1, 6, 5]):
		nodes[i].cycle.chainMarker = m			
	extend()
	chk()
							
	# step 3 #
	
	jmp(0); adv(5); 
	jmp(0); adv(6);
	jmp(3); adv(5);
	jmp(5); adv(5);
	jmp(0); adv(2);
	jmp(0); 			
	for i,m in enumerate([1, 6, 5, 4, 3, 2]):
		nodes[i].cycle.chainMarker = m			
	adv(2); extend()
	chk()
	
	# step 4 #	
	
	jmp(0); adv(5); 
	jmp(0); adv(6);
	jmp(3); adv(5);
	jmp(5); adv(5);
	jmp(0); adv(2);
	jmp(0); adv(2); 
	jmp(4); adv(1);
	jmp(4);	
	for i,m in enumerate([2, 5, 6, 3, 4, 1]):
		nodes[i].cycle.chainMarker = m				
	adv(2); extend()
	chk()	
	
	jmp(0); adv(5); 
	jmp(0); adv(6);
	jmp(3); adv(5);
	jmp(5); adv(5);
	jmp(0); adv(2);
	jmp(0); adv(2); 
	jmp(4); adv(1);
	jmp(3);	
	for i,m in enumerate([3, 4, 1, 2, 5, 6]):
		nodes[i].cycle.chainMarker = m			
	adv(3); extend()		
	chk()
	
	jmp(0); adv(5); 
	jmp(0); adv(6);
	jmp(3); adv(5);
	jmp(5); adv(5);
	jmp(0); adv(2);
	jmp(0); adv(2); 
	jmp(4); adv(1);
	jmp(2);	
	for i,m in enumerate([3, 4, 1, 2, 5, 6]):
		nodes[i].cycle.chainMarker = m																																									
	adv(4); extend()																																				
	chk()
	
	# step 5 #
	'''
	jmp(0); adv(5); 
	jmp(0); adv(6);
	jmp(3); adv(5);
	jmp(5); adv(5);
	jmp(3); adv(6);
	jmp(1); adv(6);
	#extend()
	chk()
	#'''
	
	jmp(1); adv(4); 
	jmp(0); adv(6);
	extend()
	chk()		

	jmp(1); adv(4); 
	jmp(0); adv(6);
	jmp(3); adv(5);
	extend()
	chk()
					
	jmp(1); adv(4); 
	jmp(0); adv(6);
	jmp(5); adv(3);
	extend()
	chk()

	# step 6 #
	
	jmp(1); adv(4); 
	jmp(0); adv(6);
	jmp(0); adv(1);
	jmp(0); adv(3);
	for i,m in enumerate([1, 6, 5, 4, 3, 2]):
		nodes[i].cycle.chainMarker = m																																									
	extend()
	chk()
	
	jmp(1); adv(4); 
	jmp(0); adv(6);
	jmp(0); adv(1);
	jmp(1); adv(2);
	for i,m in enumerate([6, 1, 4, 5, 2, 3]):
		nodes[i].cycle.chainMarker = m																																									
	extend()
	chk()
	
	# step 7 #
	
	jmp(4); adv(6); 
	jmp(5)
	chk()
	
	show(diagram)
	diagram.measure()
	
