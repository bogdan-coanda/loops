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
			if node.cycle.chainMarker is None:
				cms = [nln for nln in node.loopBrethren if nln.cycle.chainMarker is not None]
				if len(cms) > 0:
					print("[cms]")
					node = cms[0]
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
								
	def single():
		wc = 0; 
		while len(diagram.rx_singles) > 0 and len(diagram.rx_unreachables) is 0:
			wc += 1; sew(sorted(diagram.rx_singles, key = lambda c: c.address)[-1].availabled_node().address); extend() # F
		print('[singling] count: ' + str(wc))								
		return wc
								
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
	
	def dualKey(chain):
		cycle, ((base1, avs1), (base2, avs2)) = chain
		return (-(len(avs1)+len(avs2)), abs(len(avs1)-len(avs2)), len(avs2)-len(avs1))
			
	def monoKey(chain):
		cycle, ((base1, avs1), (base2, avs2)) = chain
		return -len(avs1)
			
	def choose():
		twos = sorted([cycle for cycle in diagram.cycles if cycle.available_loops_count == 2 and cycle.chained_by_count == 0], key = lambda c: c.address)		
		avnodes = [(cycle, sorted([cn for cn in cycle.nodes if cn.loop.availabled], key = lambda c: c.address)) for cycle in twos]
		chained = [(avnodes[0], [(node.address,[bro.address for bro in node.loopBrethren if bro.chainID is not None]) for node in avnodes[1]]) for avnodes in avnodes]
		bothSided = [(cycle, ((base1, avs1), (base2, avs2))) for cycle, ((base1, avs1), (base2, avs2)) in chained if len(avs1) is not 0 and len(avs2) is not 0]				
		
		if len(bothSided) is not 0:	
			sortedBoths = sorted(bothSided, key = dualKey)
			chosen = sortedBoths[0]												
		else:
			sortedSingles = sorted(chained, key = monoKey)
			chosen = sortedSingles[0]													
				
		cycle, ((base1, avs1), (base2, avs2)) = chosen			
		print("[choose] " + str(cycle) + " | " + str(base1) + ":" + str(avs1) + " " + str(base2) + ":" + str(avs2))
		return chosen	
		
	# lvl 1 § 1: ⟨cycle:60@000124|2⟩ | 0001243: ['0001332'] | 0001247: ['0001227']
	sew('0001332'); extend() # 1/2 

	# lvl 2 § 4: ⟨cycle:189@000430|2⟩ | 0004300: ['0214301'] | 0004304: []
	sew('0214301'); extend() # 1/2
	
	# lvl 3
	sew('1100453'); extend() # F
	
	# lvl 4 § 9: ⟨cycle:724@003213|2⟩ | 0032136: ['0001135'] | 0032137: ['0032157']
	sew('0001135'); extend() # 1/2
	
	# lvl 5 § 16: ⟨cycle:1957@021134|2⟩ | 0211345: ['0210444'] | 0211347: ['0211337']
	sew('0210444'); extend() # 1/2
	
	# lvl 6 § 23: ⟨cycle:3279@103303|2⟩ | 1033031: ['1032132', '1032043'] | 1033037: []
	sew('1032132'); extend() # 1/2
	
	# lvl 7 § 26: ⟨cycle:1951@021125|2⟩ | 0211254: ['0210355'] | 0211255: ['0210354']
	sew('0210354'); extend(); single() # 2/2 (sg:0)
	
	# lvl 8 § 16: ⟨cycle:736@003231|2⟩ | 0032316: ['0001404'] | 0032317: ['0032337']
	sew('0032337'); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose() # 2/2
		
	# lvl 9 § [singling] count: 0 [choose] ⟨cycle:74@000144|2⟩ | 0001440:['0032352'] 0001445:['1101446']
	sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
				
	# lvl 11 § [singling] count: 1 [choose] ⟨cycle:745@003243|2⟩ | 0032433:['0032342'] 0032437:['0032427']
	sew(avs1[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	# lvl 12 § [singling] count: 0 [choose] ⟨cycle:75@000145|2⟩ | 0001454:['1101455', '1002352'] 0001455:['1101454']
	sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	# lvl 13 § [singling] count: 0 [choose] ⟨cycle:208@000455|2⟩ | 0004550:['0034563', '0004566'] 0004554:['1004555']
	sew(avs1[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	# lvl 16 § [singling] count: 2 [choose] ⟨cycle:831@003445|2⟩ | 0034452:['0234555', '0034541'] 0034454:['0030353']
	sew(avs2[0]); extend(); single(); #cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	def judge(chosen):
		cycle, ((base1, avs1), (base2, avs2)) = chosen
		
		if len(diagram.rx_unreachables) is not 0:
			return
		
		if len(avs1) is 0:
			avs1 = [base1]
		if len(avs2) is 0:
			avs2 = [base2]
			
		
	
	judge(choose())
	
	# lvl 20 § [singling] count: 3 [choose] ⟨cycle:88@000204|2⟩ | 0002040:['0001141', '0001052'] 0002043:['0002132']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	# lvl 21 § [singling] count: 0 [choose] ⟨cycle:2449@023316|2⟩ | 0233162:['0023163', '0202161'] 0233166:['0233150']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
			
	# lvl 19 § [singling] count: 2 [choose] ⟨cycle:1936@021104|2⟩ | 0211040:['0210141', '1210053'] 0211041:['0210140']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	# lvl 22 § [singling] count: 2 [choose] ⟨cycle:1640@013402|2⟩ | 0134025:['0103026', '0121012'] 0134027:['0134037', '0134047']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	# lvl 23 § [singling] count: 0 [choose] ⟨cycle:748@003246|2⟩ | 0032461:['0031562', '1031563'] 0032466:['0001465']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
		
	# lvl 30 § [singling] count: 6 [choose] ⟨cycle:1349@012205|2⟩ | 0122051:['0122142', '0122324', '0122560'] 0122057:['0122067']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
					
	# lvl 25 § [singling] count: 1 [choose] ⟨cycle:752@003253|2⟩ | 0032532:['0032443', '0031544'] 0032537:['0032517', '0032527']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	# lvl 27 § [singling] count: 1 [choose] ⟨cycle:1383@012254|2⟩ | 0122540:['0031553', '1031554'] 0122543:['0120246', '0120230']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	# lvl 34 § [singling] count: 1 [choose] ⟨cycle:1358@012220|2⟩ | 0122203:['0124005', '0120401'] 0122206:['0122260', '0122351']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	# lvl 32 § [singling] count: 0 [choose] ⟨cycle:773@003323|2⟩ | 0033232:['0033143', '0024231'] 0033237:['0033257']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()  
	
	# lvl 34 § [singling] count: 1 [choose] ⟨cycle:1358@012220|2⟩ | 0122203:['0124005', '0120401'] 0122206:['0122260', '0122351']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()

	# lvl 32 § [singling] count: 0 [choose] ⟨cycle:1519@013110|2⟩ | 0131101:['0032103', '0031204'] 0131105:['0131016', '0131000']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	# lvl 26
	#sew('1224327'); extend() # F
	
	# lvl 27
	#sew('1224440'); extend() # F - dead
	
	
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

	#show(diagram)
	diagram.measure()
		
	singles = sorted(diagram.rx_singles, key = lambda c: c.address)
	print("[singles] len: " + str(len(singles)) + "\n" + str(singles))	
	if len(singles) > 0:
		print([n for n in singles[-1].nodes if n.loop.availabled])
	
