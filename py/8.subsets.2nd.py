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

	diagram.forceUnavailable(set(chain(*[[node.loop for node in cycle.nodes if node.loop.availabled] for cycle in diagram.cycles if cycle.isKernel])))	

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
										
	ex = 0
										
	def extend():		
		global ex
		print("[extend:"+str(ex)+"] "+str(sorted(groupby([node.ktype for node in nodes], G = lambda g: len(g)).items())))
		for i,node in enumerate(nodes):
			#print("[ext] "+str(i)+": "+str(node))
			assert diagram.extendLoop(node.loop), "failed to extend " + str(node) + " @ " + str(i)
			for nln in node.loopBrethren:
				#print("[ext] nln: "+str(node))
				assert nln.cycle.chainMarker is None or node.cycle.chainMarker is None or nln.cycle.chainMarker is node.cycle.chainMarker
				nln.cycle.chainMarker = node.cycle.chainMarker
		diagram.forceUnavailable(set([loop for loop in diagram.loops if loop.availabled and len(set([node.cycle.chainMarker for node in loop.nodes if node.cycle.chainMarker is not None])) > 1]))
		ex += 1
		chk()				
		recolor()
		
		
	def chk():	
		#for cycle in diagram.cycles:
			#cycle.chk()		
		#print("[chk]")
		global nodes
		_p = diagram.pointers
		nodes = list(bases)
		chkcc = 0
		uncc = 0
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
					if avcc is not 0 and avcc is not len(nodes):
						uncc += 1
						#for cycle in diagram.cycles:
							#cycle.chk()
						diagram.forceUnavailable([node.loop for node in nodes if node.loop.availabled])
						#for cycle in diagram.cycles:
							#cycle.chk()						
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
					if avcc is not 0 and avcc is not len(nodes):
						uncc += 1
						#for cycle in diagram.cycles:
							#cycle.chk()
						diagram.forceUnavailable([node.loop for node in nodes if node.loop.availabled])
						#for cycle in diagram.cycles:
							#cycle.chk()
					if avcc is not 0:
						chkcc += 1				
					nxt()				
		diagram.pointers = _p
		#diagram.pointers = nodes
		#print("[chk] cc: " + str(chkcc))
		if uncc > 0:
			print("[chk] unavailabled " + str(uncc) + " nodes")
		#for cycle in diagram.cycles:
			#cycle.chk()


	def recolor():
		rc = 0
		for base in bases:
			for node in base.loopBrethren:
				if node.chainID is not None:
					CM = node.cycle.chainMarker
					curr = node.nextLink.next
					while curr != node:
						assert curr.cycle.chainMarker is None or curr.cycle.chainMarker is CM
						if curr.cycle.chainMarker is None:
							rc += 1
							curr.cycle.chainMarker = CM
						curr = curr.nextLink.next
			#if rc > 0:
				#print("[recolor] recolored " + str(rc) + " nodes")
			diagram.forceUnavailable(set([loop for loop in diagram.loops if loop.availabled and len(set([node.cycle.chainMarker for node in loop.nodes if node.cycle.chainMarker is not None])) > 1]))
			if rc > 0:
				chk()
				recolor()

	# ~~~ walk ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							
	print("~~~ walk ~ ~~~")
	
	wq = [list(nodes)]
	while len(wq) > 0:
		
		t = wq.pop()
		for node in t:
			node.tuple = t
			
		nodes = list(t)
		adv(1)
		if nodes[0].tuple is None:
			wq.append(list(nodes))

		nodes = list(t)
		jmp(0)
		if nodes[0].tuple is None:
			wq.append(list(nodes))

	assert len([n for n in diagram.nodes if n.tuple is None]) is 0

	def sew(address):
		global nodes
		tuple = list(diagram.nodeByAddress[address].tuple)
		nodes = tuple
		diagram.pointers = tuple
								
	# ~~~ ~~~~ ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # '''

	def sxj0a5():
		jmp(0); adv(5);

	def sxj1a4():
		jmp(1); adv(4);
		
	def sxj2a3():
		jmp(2); adv(3);
		
	def sxj3a2():
		jmp(3); adv(2);

	def sxj0a5j0a6():
		sxj0a5(); jmp(0);	adv(6);
				
	def sxj4a3():	
		jmp(4); adv(3);			

	def sxj5a2():
		jmp(5); adv(2);
	
	def sxj0a5j0a6j3a4():
		sxj0a5j0a6(); jmp(3); adv(4);

	def sxj2a3j0a6():
		sxj2a3();	jmp(0); adv(6); 

	def sxj2a3j0a6j5a2():
		sxj2a3j0a6(); jmp(5); adv(2);
				
	def sxj5a2j3a6():
		sxj5a2(); jmp(3); adv(6);				

	def sxj0a5j0a6j3a4j2a2():
		sxj0a5j0a6j3a4(); jmp(2); adv(2);

	def sxj0a5j0a6j3a4j3a6():
		sxj0a5j0a6j3a4(); jmp(3); adv(6);

	def sxj4a3j4a6():
		sxj4a3(); jmp(4); adv(6);										

	def sxj4a3j3a6():	
		sxj4a3(); jmp(3); adv(6);
	
	def sxj2a3j0a6j5a2j5a6():
		sxj2a3j0a6j5a2(); jmp(5); adv(6);
	
	def sxj2a3j0a6j5a2j5a6j0a6():
		sxj2a3j0a6j5a2j5a6(); jmp(0); adv(6)
		
	def sxj2a3j0a6j5a2j5a6j0a6j0a6():
		sxj2a3j0a6j5a2j5a6j0a6(); jmp(0); adv(6);
				
	def sxj2a3j0a6j5a2j5a6j0a6j3a4():
		sxj2a3j0a6j5a2j5a6j0a6(); jmp(3); adv(4);
				
	def sxj5a2j3a6j0a6():
		sxj5a2j3a6(); jmp(0); adv(6)

	def sxj5a2j3a6j0a6j3a4():
		sxj5a2j3a6j0a6(); jmp(3); adv(4);
		
	def sxj0a5j0a6j3a4j2a2j5a2():
		sxj0a5j0a6j3a4j2a2(); jmp(5); adv(2);

	def sxj0a5j0a6j3a4j2a2j5a2j0a6():
		sxj0a5j0a6j3a4j2a2j5a2(); jmp(0); adv(6);
								
	def sxj2a3j0a6j5a2j5a6j0a6j0a6j0a6():
		sxj2a3j0a6j5a2j5a6j0a6j0a6(); jmp(0); adv(6);
								
	chk()

	# ~~~ step α ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # '''
	print("~~~ step α ~~~")
	
	sxj0a5(); extend() 																			# type:0 (blue)
	sxj0a5j0a6(); extend() 																	# type:1 (green)		
	sxj0a5j0a6j3a4(); extend() 															# type:3/5/7 (orange/purple/black)		
	sxj0a5j0a6j3a4j2a2(); extend() 													# type:2/4/6 (yellow/red/indigo)		
	sxj0a5j0a6j3a4j2a2j5a2(); extend() 											# type:3/5/7 (orange/purple/black)		
	sxj0a5j0a6j3a4j2a2j5a2j0a6(); extend() 									# type:1 (green)
	sxj0a5j0a6j3a4j2a2j5a2j0a6(); jmp(0); adv(2); extend() 	# type:0 (blue)
	sxj0a5j0a6j3a4j2a2j5a2j0a6(); jmp(3); adv(6); extend() 	# type:0 (blue)
	
	sxj0a5j0a6j3a4j3a6(); extend() 									# type:2/4/6 (yellow/red/indigo)					
	sxj0a5j0a6j3a4j3a6(); jmp(0); adv(6); extend() 	# type:3/5/7 (orange/purple/black)			
	
	sxj1a4(); extend() 																			# type:0 (blue)	
	sxj2a3(); extend() 																			# type:0 (blue)	
	sxj2a3j0a6(); extend() 																	# type:1 (green)
	sxj2a3j0a6j5a2(); extend() 															# type:3/5/7 (orange/purple/black)		
	sxj2a3j0a6j5a2j5a6(); extend() 													# type:2/4/6 (yellow/red/indigo)	
	sxj2a3j0a6j5a2j5a6j0a6(); extend() 											# type:3/5/7 (orange/purple/black)		
	sxj2a3j0a6j5a2j5a6j0a6j0a6(); extend() 									# type:2/4/6 (yellow/red/indigo)	
	sxj2a3j0a6j5a2j5a6j0a6j0a6j0a6(); extend() 							# type:3/5/7 (orange/purple/black)	
	sxj2a3j0a6j5a2j5a6j0a6j3a4(); extend() 									# type:1 (green)	
	sxj2a3j0a6j5a2j5a6j0a6j3a4(); jmp(2); adv(2); extend() 	# type:0 (blue)
	sxj2a3j0a6j5a2j5a6j0a6j3a4(); jmp(5); adv(6); extend() 	# type:0 (blue)	
	
	sxj3a2(); extend() 											# type:0 (blue)
	sxj4a3(); extend() 											# type:3/5/7 (orange/purple/black)	
	sxj4a3j3a6(); extend() 									# type:2/4/6 (yellow/red/indigo)			
	sxj4a3j4a6(); extend() 									# type:1 (green)
	sxj4a3j4a6(); jmp(0); adv(2); extend() 	# type:0 (blue)
	sxj4a3j4a6(); jmp(3); adv(6); extend() 	# type:0 (blue)	
	
	sxj5a2(); extend() 															# type:3/5/7 (orange/purple/black)	
	sxj5a2j3a6(); extend() 													# type:2/4/6 (yellow/red/indigo)	
	sxj5a2j3a6j0a6(); extend() 											# type:3/5/7 (orange/purple/black)	
	sxj5a2j3a6j0a6j3a4(); extend() 									# type:1 (green)
	sxj5a2j3a6j0a6j3a4(); jmp(0); adv(2); extend() 	# type:0 (blue)
	sxj5a2j3a6j0a6j3a4(); jmp(3); adv(6); extend() 	# type:0 (blue)	
		
	# ~~~ step Ω ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							
	print("~~~ step Ω ~~~")
	
	
	
	'''
	def sx7():
		jmp(4); adv(1);
		
	sx7(); jmp(2); adv(6); extend()
	sx7(); jmp(3); adv(5); extend()
	
	def sx2():
		sxj0a5j0a6(); jmp(0); adv(1);
			
	sx2(); jmp(0); adv(2); extend()			
	sx2(); jmp(3); adv(6); extend()
	sx2(); jmp(4); adv(5); extend()
	
	def sx3():
		sx2(); jmp(4); adv(5);

	def sx3j0():
		sx3(); jmp(0); adv(2); jmp(0); adv(1); 

	def sx3j1():
		sx3(); jmp(1); adv(1); jmp(0); adv(1);
			
	sx3j0(); extend()
	sx3j0(); jmp(0); adv(6); extend()
	sx3j0(); jmp(4); adv(2); extend()
	
	sx3j1(); extend()
	sx3j1(); jmp(0); adv(6); extend()
	sx3j1(); jmp(4); adv(2); extend()
			
	def sx4():
		sx3(); jmp(4); adv(7); jmp(4); adv(1);
	
	#sx4(); jmp(1); adv(4); extend();
			
	def sx5():
		sx4(); jmp(0); adv(5); 
		
	def sx5j1():
		sx5(); jmp(1); adv(1); jmp(3); adv(1); 

	def sx5j3():
		sx5(); jmp(3); adv(6); jmp(4); adv(1);

	sx5j1(); extend()
	sx5j1(); jmp(0); adv(6); extend()
	sx5j1(); jmp(4); adv(2); extend()	
	
	def sx6mid():
		sx3(); jmp(4); adv(7); jmp(0); adv(5)		
													
	sx4(); jmp(1); adv(6); extend()
	sx4(); jmp(2); adv(5); extend()	
	sx4(); jmp(4); adv(3); extend()	
	sx4(); jmp(5); adv(2); extend()
			
	sx6mid(); adv(4); extend()	
	sx6mid(); jmp(1); adv(2); extend()
						
	def sx8():
		sx7(); adv(2); jmp(2); adv(1); jmp(3); adv(5);
		
	sx8(); jmp(1); adv(2); extend()	
	sx8(); jmp(3); adv(5); extend()
		
	def sx10():
		sx8(); jmp(1); adv(1); jmp(2);
		
	sx10(); adv(1); extend()
		
	def sx11():				
		sx8(); adv(2); 
		
	def sx11j1():	
		sx11(); jmp(1); adv(4); jmp(0); adv(1); 
		
	def sx11j2():	
		sx11(); jmp(2);	adv(3); jmp(0); adv(1); 
				
	def sx11j3():	
		sx11(); jmp(3); adv(2); jmp(0); adv(1); 

	def sx11j4():	
		sx11(); jmp(4); adv(1); jmp(0); adv(1); 
			
	sx11j3(); extend()
	sx11j3(); jmp(0); adv(6); extend()
	sx11j3(); jmp(4); adv(2); extend()		
	
	sx11j4(); extend()
	sx11j4(); jmp(0); adv(6); extend()
	sx11j4(); jmp(4); adv(2); extend()
		
	def sx12():
		sx10(); adv(1); 		
	
	def sx12j0():	
		sx12(); jmp(0); adv(2); jmp(2); adv(1); 

	def sx12j1():
		sx12(); jmp(1); adv(1); jmp(2); adv(1); 
						
	sx12j1(); extend()
	sx12j1(); jmp(0); adv(6); extend()
	sx12j1(); jmp(4); adv(2); extend()
																										
	# ~~~ ~~~~ ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							
	print("~~~ ~~~~ ~ ~~~")	

	show(diagram)
	diagram.measure()
	singles = sorted(diagram.rx_singles, key = lambda c: c.address)
	print(singles)
	if len(singles) > 0:
		print([n for n in singles[-1].nodes if n.loop.availabled])
	
