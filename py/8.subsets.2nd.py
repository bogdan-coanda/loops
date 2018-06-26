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
										
										
	def extend():		
		for i,node in enumerate(nodes):
			#print("[ext] "+str(i)+": "+str(node))
			assert diagram.extendLoop(node.loop), "failed to extend " + str(node) + " @ " + str(i)
			for nln in node.loopBrethren:
				#print("[ext] nln: "+str(node))
				assert nln.cycle.chainMarker is None or node.cycle.chainMarker is None or nln.cycle.chainMarker is node.cycle.chainMarker
				nln.cycle.chainMarker = node.cycle.chainMarker
		diagram.forceUnavailable(set([loop for loop in diagram.loops if loop.availabled and len(set([node.cycle.chainMarker for node in loop.nodes if node.cycle.chainMarker is not None])) > 1]))
		chk()				
		recolor()
		
		
	def chk():	
		for cycle in diagram.cycles:
			cycle.chk()		
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
						for cycle in diagram.cycles:
							cycle.chk()
						diagram.forceUnavailable([node.loop for node in nodes if node.loop.availabled])
						for cycle in diagram.cycles:
							cycle.chk()						
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
						for cycle in diagram.cycles:
							cycle.chk()
						diagram.forceUnavailable([node.loop for node in nodes if node.loop.availabled])
						for cycle in diagram.cycles:
							cycle.chk()
					if avcc is not 0:
						chkcc += 1				
					nxt()				
		diagram.pointers = _p
		#diagram.pointers = nodes
		#print("[chk] cc: " + str(chkcc))
		if uncc > 0:
			print("[chk] unavailabled " + str(uncc) + " nodes")
		for cycle in diagram.cycles:
			cycle.chk()


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
			if rc > 0:
				print("[recolor] recolored " + str(rc) + " nodes")
			diagram.forceUnavailable(set([loop for loop in diagram.loops if loop.availabled and len(set([node.cycle.chainMarker for node in loop.nodes if node.cycle.chainMarker is not None])) > 1]))
			if rc > 0:
				chk()
				recolor()
			
	# ~~~ ~~~~ ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # '''

	chk()

	# ~~~ step 0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # '''
	print("~~~ step 0 ~~~")
	
	jmp(0); adv(5); extend()
	jmp(1); adv(4); extend()
	jmp(2); adv(3); extend()
	jmp(3); adv(2); extend()

	# ~~~ step 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	print("~~~ step 1 ~~~")
	
	def sx1():
		jmp(0); adv(5); jmp(0);	adv(6);
		
	sx1(); extend()
	
	# ~~~ step 2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	print("~~~ step 2 ~~~")
	
	def sx2():
		sx1(); jmp(0); adv(1);
			
	sx2(); jmp(0); adv(2); extend()
	sx2(); jmp(1); adv(1); extend()
	sx2(); jmp(3); adv(6); extend()
	sx2(); jmp(4); adv(5); extend()

	# ~~~ step 3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # '''
	print("~~~ step 3 ~~~")
	
	def sx3():
		sx2(); jmp(4); adv(5);

	def sx3j0():
		sx3(); jmp(0); adv(2); jmp(0); adv(1); 
						
	sx3j0(); extend()
	sx3j0(); jmp(0); adv(6); extend()
	sx3j0(); jmp(4); adv(2); extend()

	def sx3j1():
		sx3(); jmp(1); adv(1); jmp(0); adv(1);
	
	sx3j1(); extend()
	sx3j1(); jmp(0); adv(6); extend()
	sx3j1(); jmp(4); adv(2); extend()
	
	sx3(); jmp(5); adv(4); jmp(0); adv(1); jmp(0); extend()

	# ~~~ step 4 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	print("~~~ step 4 ~~~")
	
	def sx4():
		sx3(); jmp(4); adv(7); jmp(4); adv(1);
		
	sx4(); jmp(0); adv(5); extend();
	sx4(); jmp(1); adv(4); extend();

	# ~~~ step 5 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	print("~~~ step 5 ~~~")
	
	def sx5():
		sx4(); jmp(0); adv(5); 
		
	def sx5j1():
		sx5(); jmp(1); adv(1); jmp(3); adv(1); 
		
	sx5j1(); extend()
	sx5j1(); jmp(0); adv(6); extend()
	sx5j1(); jmp(4); adv(2); extend()	
	
	def sx5j3():
		sx5(); jmp(3); adv(6); jmp(4); adv(1);
	
	sx5j3(); extend()
	sx5j3(); jmp(0); adv(6); extend()
	sx5j3(); jmp(4); adv(2); extend()	

	# ~~~ step 6 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	print("~~~ step 6 ~~~")
	
	sx4(); adv(1); extend()
	sx4(); jmp(1); adv(6); extend()
	sx4(); jmp(2); adv(5); extend()	
	sx4(); jmp(3); adv(4); extend()
	sx4(); jmp(4); adv(3); extend()	
	sx4(); jmp(5); adv(2); extend()
	
	def sx6mid():
		sx3(); jmp(4); adv(7); jmp(0); adv(5)
		
	sx6mid(); adv(4); extend()
	sx6mid(); jmp(0); adv(3); extend()
	sx6mid(); jmp(1); adv(2); extend()
					
	# ~~~ step 7 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''		
	print("~~~ step 7 ~~~")
	
	def sx7():
		jmp(4); adv(1);
		
	sx7(); adv(2); extend()
	sx7(); jmp(0); adv(1); extend()
	sx7(); jmp(2); adv(6); extend()
	sx7(); jmp(3); adv(5); extend()
	sx7(); jmp(4); adv(4); extend()
	sx7(); jmp(5); adv(3); extend()
	
	# ~~~ step 8 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''		
	print("~~~ step 8 ~~~")
	
	def sx8():
		sx7(); adv(2); jmp(2); adv(1); jmp(3); adv(5);
		
	sx8(); adv(4); extend()
	sx8(); jmp(0); adv(3); extend()
	sx8(); jmp(1); adv(2); extend()

	# ~~~ step 9 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''		
	print("~~~ step 9 ~~~")			
	
	sx8(); adv(2); extend()
	sx8(); jmp(3); adv(5); extend()
	sx8(); jmp(4); adv(4); extend()
	sx8(); jmp(5); adv(3); extend()
	
	# ~~~ step 10 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''		
	print("~~~ step 10 ~~~")				
	
	def sx10():
		sx8(); jmp(1); adv(1); jmp(2);
	
	sx10(); adv(1); extend()
	sx10(); adv(4); jmp(5); adv(6); extend()

	# ~~~ step 11 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''		
	print("~~~ step 11 ~~~")				
			
	def sx11():				
		sx8(); adv(2); 
		
	sx11(); jmp(1); adv(4); jmp(0); adv(1); extend()
	sx11(); jmp(2);	adv(3); jmp(0); adv(1); extend()
	sx11(); jmp(3); adv(2); jmp(0); adv(1); extend()
	sx11(); jmp(4); adv(1); jmp(0); adv(1); extend()

	# ~~~ step 12 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''		
	print("~~~ step 12 ~~~")				

	def sx12():
		sx10(); adv(1); 		
		
	sx12(); jmp(0); adv(2); jmp(2); adv(1); extend()
	sx12(); jmp(1); adv(1); jmp(2); adv(1); extend()
							
	# ~~~ ~~~~ ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							
	
	show(diagram)
	diagram.measure()
	
