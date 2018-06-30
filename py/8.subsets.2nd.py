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
2: ⟨cycle:191@000432|2⟩ | 0004323: ['0004234'] | 0004327: ['0004347']
8: ⟨cycle:683@003114|2⟩ | 0031147: ['0031127'] | 0031143: ['0031232']
14: ⟨cycle:1892@021002|2⟩ | 0210027: ['0210047'] | 0210023: ['0210534']
18: ⟨cycle:2550@100042|2⟩ | 1000427: ['1000447'] | 1000423: ['1000334']
23: ⟨cycle:3399@110054|2⟩ | 1100547: ['1100527'] | 1100543: ['1100032']
0: ⟨cycle:54@000115|2⟩ | 0001157: ['0001137'] | 0001153: []
3: ⟨cycle:197@000441|2⟩ | 0004417: ['0004437'] | 0004413: []
4: ⟨cycle:242@001044|2⟩ | 0010444: [] | 0010446: ['1110445']
5: ⟨cycle:345@001312|2⟩ | 0013120: ['0223121'] | 0013122: []
6: ⟨cycle:529@002234|2⟩ | 0022346: ['0023245'] | 0022344: []
7: ⟨cycle:677@003105|2⟩ | 0031053: [] | 0031057: ['0031037']
9: ⟨cycle:812@003420|2⟩ | 0034200: [] | 0034203: ['0031500']
10: ⟨cycle:839@003456|2⟩ | 0034563: ['0004566'] | 0034566: []
11: ⟨cycle:856@010022|2⟩ | 0100222: [] | 0100220: ['0104321']
12: ⟨cycle:1691@020014|2⟩ | 0200146: ['0231145'] | 0200144: []
13: ⟨cycle:1752@020142|2⟩ | 0201422: [] | 0201420: ['1201421']
15: ⟨cycle:1898@021011|2⟩ | 0210113: [] | 0210117: ['0210137']
19: ⟨cycle:2556@100051|2⟩ | 1000513: [] | 1000517: ['1000537']
20: ⟨cycle:2604@100200|2⟩ | 1002003: ['0001000'] | 1002000: []
21: ⟨cycle:2631@100236|2⟩ | 1002363: ['1000066'] | 1002366: []
22: ⟨cycle:3393@110045|2⟩ | 1100453: [] | 1100457: ['1100437']
26: ⟨cycle:4633@122016|2⟩ | 1220163: ['0210266'] | 1220166: []
27: ⟨cycle:4648@122040|2⟩ | 1220400: [] | 1220403: ['1100300']
16: ⟨cycle:2300@022444|2⟩ | 0224440: [] | 0224444: []
17: ⟨cycle:2466@023342|2⟩ | 0233422: [] | 0233426: []
24: ⟨cycle:3747@111412|2⟩ | 1114126: [] | 1114122: []
25: ⟨cycle:4379@120414|2⟩ | 1204140: [] | 1204144: []
28: ⟨cycle:4895@123132|2⟩ | 1231322: [] | 1231326: []
29: ⟨cycle:4932@123224|2⟩ | 1232240: [] | 1232244: []
30: ⟨cycle:5001@123403|2⟩ | 1234033: [] | 1234037: []
31: ⟨cycle:5008@123413|2⟩ | 1234133: [] | 1234137: []
32: ⟨cycle:5015@123423|2⟩ | 1234237: [] | 1234233: []
33: ⟨cycle:5022@123433|2⟩ | 1234333: [] | 1234337: []
34: ⟨cycle:5029@123443|2⟩ | 1234437: [] | 1234433: []
35: ⟨cycle:5036@123453|2⟩ | 1234537: [] | 1234533: []	
	'''
	
	# 1: ⟨cycle:60@000124|2⟩ | 0001243: ['0001332'] | 0001247: ['0001227']
	#sew('0001332'); extend() # 1/2 # type:2/4/6 (yellow/red/indigo)
	sew('0001227'); extend() # 2/2 # type:0 (blue)
	
	'''
	sew('1234037'); extend() # 1/2		
	sew('0001153'); extend() # 1/2
	sew('0001243'); extend() # 1/2
	sew('0001262'); extend() # 1/2
	sew('0001440'); extend() # 1/2
	sew('0010444'); extend() # 1/2
	sew('0014111'); extend() # 1/2
	sew('0014123'); extend() # 1/2
	sew('0032136'); extend() # 1/2
	sew('0032310'); extend() # 1/2
	sew('0001411'); extend() # 1/2
	sew('0032143'); extend() # 1/2
	sew('0023136'); extend() # 1/2
	sew('0023153'); extend() # 1/2
	sew('1224237'); extend() # F
	sew('1122137'); extend() # F
	sew('1122046'); extend() # F
	sew('1220452'); extend() # F
	sew('1113117'); extend() # F
	sew('1100531'); extend() # F
	sew('1223437'); extend() # F
	sew('1214427'); extend() # F
	sew('1210332'); extend() # F
	sew('1223540'); extend() # F
	sew('1223246'); extend() # F
	sew('1122344'); extend() # F
	sew('1122326'); extend() # F
	sew('1122216'); extend() # F
	'''
	'''
	sew('1234037'); extend() # 1/2
	sew('1232240'); extend() # 1/2
	sew('1220400'); extend() # 1/2
	sew('1200311'); extend() # 1/2
	sew('1200232'); extend() # 1/2
	sew('1100543'); extend() # 1/2
	sew('1224235'); extend() # 1/2
	sew('1210530'); extend() # 1/2
	sew('1224021'); extend() # 1/2
	sew('1210512'); extend() # 1/2
	sew('1224055'); extend() # 1/2
	sew('1202250'); extend() # 1/2
	sew('1201350'); extend() # 1/2
	sew('1201341'); extend() # 1/2
	sew('1122042'); extend() # 1/2
	sew('1210350'); extend() # 1/2
	sew('1224201'); extend() # 1/2
	sew('1210341'); extend() # 1/2
	sew('1210521'); extend() # 1/2
	sew('1122307'); extend() # F
	sew('1210454'); extend() # 2/2
	sew('1220452'); extend() # 1/2
	sew('1210335'); extend() # 2/2
	sew('1214442'); extend() # F
	sew('1214524'); extend() # F
	sew('1232416'); extend() # F
	sew('1223416'); extend() # F
	sew('1104226'); extend() # F # 18480/40320
	'''
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
	
	twos = sorted([cycle for cycle in diagram.cycles if cycle.available_loops_count == 2 and cycle.chained_by_count == 0], key = lambda c: c.address)
	print("[twos] len: " + str(len(twos)) + "\n" + str(twos))
	
	for i,cycle in enumerate(twos):
		avnodes = sorted([cn for cn in cycle.nodes if cn.loop.availabled], key = lambda c: c.address)
		line = ""
		for node in avnodes:
			chainedbros = [bro.address for bro in node.loopBrethren if bro.chainID is not None]
			line += " | " + node.address + ": " + str(chainedbros)			
		print(str(i) + ": " + str(cycle) + line)
	
	singles = sorted(diagram.rx_singles, key = lambda c: c.address)
	print("[singles] len: " + str(len(singles)) + "\n" + str(singles))	
	if len(singles) > 0:
		print([n for n in singles[-1].nodes if n.loop.availabled])
	
