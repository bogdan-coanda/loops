from diagram import *
from uicanvas import *
from itertools import chain
							
	
if __name__ == "__main__":
	
	diagram = Diagram(6)	
	#diagram.generateKernel()																				
	#diagram.forceUnavailable(set(chain(*[[node.loop for node in cycle.nodes if node.loop.availabled] for cycle in diagram.cycles if cycle.isKernel])))
		
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

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	
	bases = [diagram.nodeByAddress['11104']]
	nodes = list(bases)
	diagram.pointers = nodes

	nodes[0].cycle.chainMarker = 1

	chk()
	extend(); chk();					
	
	jmp(1); adv(4); extend(); chk();
	jmp(2); adv(3); extend(); chk();
	jmp(3); adv(2); extend(); chk();

	# purple links #
	adv(1); jmp(0); adv(2); nodes[0].cycle.chainMarker = 4; extend(); chk();
	adv(1); jmp(1); adv(1); nodes[0].cycle.chainMarker = 3; extend(); chk();
	#adv(1);         adv(3);                                 extend(); chk();
	#adv(1); jmp(3); adv(4);                                 extend(); chk();
	#'''

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
									
	bases = [diagram.nodeByAddress['10204']]
	nodes = list(bases)
	diagram.pointers = nodes

	nodes[0].cycle.chainMarker = 2

	chk()
	extend(); chk();								
			
	jmp(1); adv(4); extend(); chk();			
	jmp(2); adv(3); extend(); chk();
	jmp(3); adv(2); extend(); chk();
				
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	
	bases = [diagram.nodeByAddress['01204']]
	nodes = list(bases)
	diagram.pointers = nodes

	nodes[0].cycle.chainMarker = 3

	chk()
	extend(); chk();					
	
	jmp(1); adv(4); extend(); chk();
	jmp(2); adv(3); extend(); chk();
	jmp(3); adv(2); extend(); chk();

	adv(1); jmp(0); adv(2); nodes[0].cycle.chainMarker = 2; extend(); chk();
	adv(1); jmp(1); adv(1); nodes[0].cycle.chainMarker = 1; extend(); chk();
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
		
	bases = [diagram.nodeByAddress['02104']]
	nodes = list(bases)
	diagram.pointers = nodes

	nodes[0].cycle.chainMarker = 4

	chk()
	extend(); chk();					
	
	jmp(1); adv(4); extend(); chk();
	jmp(2); adv(3); extend(); chk();
	jmp(3); adv(2); extend(); chk();
	
	show(diagram)
	diagram.measure()
	
