from diagram import *
from uicanvas import *
from itertools import chain
							
	
def handle(binary=[]):
	
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
										
	def extend(key=""):		
		nonlocal ex
		print("["+key+"][extend:"+str(ex)+"]["+str(nodes[0])+"]"+str(sorted(groupby([node.ktype for node in nodes], G = lambda g: len(g)).items())))
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
		nonlocal  nodes
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
		nonlocal nodes
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
	sew('1033037'); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose() # 2/2
	
	# lvl 7 § 26: ⟨cycle:1951@021125|2⟩ | 0211254: ['0210355'] | 0211255: ['0210354']
	#sew('0210354'); extend(); single() # 2/2 (sg:0)
	
	# lvl 8 § 16: ⟨cycle:736@003231|2⟩ | 0032316: ['0001404'] | 0032317: ['0032337']
	#sew('0032337'); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose() # 2/2
		
	# lvl 9 § [singling] count: 0 [choose] ⟨cycle:74@000144|2⟩ | 0001440:['0032352'] 0001445:['1101446']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
				
	# lvl 11 § [singling] count: 1 [choose] ⟨cycle:745@003243|2⟩ | 0032433:['0032342'] 0032437:['0032427']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	# lvl 12 § [singling] count: 0 [choose] ⟨cycle:75@000145|2⟩ | 0001454:['1101455', '1002352'] 0001455:['1101454']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	# lvl 13 § [singling] count: 0 [choose] ⟨cycle:208@000455|2⟩ | 0004550:['0034563', '0004566'] 0004554:['1004555']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
	
	# lvl 16 § [singling] count: 2 [choose] ⟨cycle:831@003445|2⟩ | 0034452:['0234555', '0034541'] 0034454:['0030353']
	#sew(avs2[0]); extend(); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()

	for choice in binary:
		if choice is 0:
			address = avs1[0] if len(avs1) is not 0 else base1
		else:
			address = avs2[0] if len(avs2) is not 0 else base2
		
		try:
			sew(address); extend("".join([str(x) for x in binary])); single(); cycle, ((base1, avs1), (base2, avs2)) = choose()
		except Exception as e:
			return (diagram, (cycle, ((base1, avs1), (base2, avs2))), str(e))
			
	print("~~~ ~~~~ ~ ~~~")	
	return (diagram, (cycle, ((base1, avs1), (base2, avs2))), None)
	
	
if __name__ == "__main__":
		
	output = []
		
	def judge(binary=[]):
		try:
			
			diagram, (cycle, ((base1, avs1), (base2, avs2))), broken = handle(binary)
			if len(diagram.rx_unreachables) is not 0 or broken:
				loopedCount, chains, avs = diagram.measure()
				outstr = "[judge] ["+str(loopedCount)+"/"+str(len(diagram.nodes))+"] " + "".join([str(x) for x in binary]) + " | " + str(broken)
				output.append(outstr)
				input(outstr)
				return
				
		except Exception as e:
			print(e)
			input()
			return
					
		if len(avs1) is 0:
			avs1 = [base1]
		
		judge(binary + [0])	
				
		if len(avs2) is 0:
			avs2 = [base2]
				
		judge(binary + [1])	
	
	judge([int(i) for i in "001"])
	
	print("~~~ ~~~~ ~~~~ ~~~")	
	print("\n".join(output))
	print("~~~ ~~~~ ~~~~ ~~~")	
	
