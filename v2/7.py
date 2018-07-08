from diagram import *
from uicanvas import *
from groupby import *


if __name__ == "__main__":
	
	diagram = Diagram(7)
	diagram.generateKernel()
	
	#show(diagram)
	
	def measure():
		unlooped_cycle_count = len([c for c in diagram.cycles if c.chained_by_count is 0])
		grouped_cycles_by_av = sorted(groupby([c for c in diagram.cycles if c.chained_by_count is 0], K = lambda c: c.available_loops_count).items())
		print("unlooped cycles: " + str(unlooped_cycle_count))
		print("cycle av counts: " + str([(k, len(v)) for k,v in grouped_cycles_by_av]))			
		return (unlooped_cycle_count, grouped_cycles_by_av)

	node = None
			
	def extend(address):		
		global node
		node = diagram.nodeByAddress[address]
		assert diagram.extendLoop(node.loop)		
		
	# ~~~ ~~~~ ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							

	unlooped_cycle_count, grouped_cycles_by_av = measure()
	
	# spark
	extend('000001')		
	
	# island @ 100
	extend('100106')
	extend('100306')
	extend('100205')
	
	# s.diag @ 100 - yellow
	extend('100211')
	extend('100220')
	extend('100244')
	
	# p.diag @ 100 - red
	extend('100002')
	extend('100011')
	extend('100020')
	extend('100044')
	extend('100053')		

	# island @ 101
	extend('101006')
	extend('101206')
	extend('101105')
	
	# island @ 103
	extend('103206')
	extend('103406')
	extend('103305')
	
	# p.diag @ 102 - red
	extend('102000')
	extend('102024')	
	extend('102033')
	extend('102042')
	extend('102051')
	
	# s.diag @ 120 - yellow
	extend('120013')
	extend('120022')
	extend('120031')
	
	# island @ 121
	extend('121206')
	extend('121406')
	extend('121305')	

	# island @ 122
	extend('122106')
	extend('122306')
	extend('122205')	
	
	# island @ 123
	# extend('123006')
	# extend('123206')
	# extend('123105')	
	
	
	unlooped_cycle_count, grouped_cycles_by_av = measure()			
	
	# ~~~ walk ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''								
	''''
	def jmp(bid):
		for i in range(len(nodes)):
			if i % 2 == 0:
				nodes[i] = nodes[i].loopBrethren[bid]
			else:
				nodes[i] = nodes[i].loopBrethren[-1-bid]
		#diagram.pointers = nodes				
		
	def adv(cid):
		for i in range(len(nodes)):
			if i % 2 == 0:
				for _ in range(cid):
					nodes[i] = nodes[i].links[1].next
			else:
				for _ in range(cid):
					nodes[i] = nodes[i].prevs[1].node
		#diagram.pointers = nodes					
		
	nodes = [diagram.nodeByAddress['000001'], diagram.nodeByAddress['000154']]
	
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
				
	# ~~~ ~~~~ ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							
	'''
	measure()
				
	sparkNode = diagram.nodeByAddress['000001']
	diagram.extendLoop(sparkNode.loop)
		
	input()
				
	measure()
		
	bros = list(sparkNode.loopBrethren)		
	
	while len(bros) > 0:
		base = sorted(bros, key = lambda n: (n.cycle.available_loops_count, n.address))[0]
		node = sorted([ncn for ncn in base.cycle.nodes if ncn.loop.availabled], key = lambda n: n.ktype)[0]
		diagram.extendLoop(node.tuple[0].loop)
		diagram.extendLoop(node.tuple[1].loop)	
		diagram.pointers = node.tuple
		bros.remove(base)	
		measure()
	
	
	rxcc = 0
	def rx(lvl=0, road=[]):
		global rxcc
		
		unlooped_cycle_count, grouped_cycles_by_av = measure()

		if unlooped_cycle_count < 12:
			show(diagram)
		if lvl >= 100 or rxcc % 100 is 0 or unlooped_cycle_count < 12:
			print("[rx:"+str(lvl)+":"+str(rxcc)+"] road: " + " ".join([str(k)+"/"+str(v) for k,v in road]))
		rxcc += 1
		
		if unlooped_cycle_count is 0:
			if len(set([n.chainID for n in diagram.nodes])) is 1:
				input("Found!!!")
			return
			
		#cycle = grouped_cycles_by_av[0][1][0]		
		cycles = grouped_cycles_by_av[0][1] 
		#print([(c, -len([n for n in c.nodes if n.loop.availabled and len([nln for nln in n.loopBrethren if nln.chainID is not None])])) for c in cycles])
		#print([(n,[nln.chainID for nln in n.loopBrethren]) for n in cycles[0].nodes if n.loop.availabled])
		cycle = sorted(cycles, key = lambda c: (-len([n for n in c.nodes if n.loop.availabled and len([nln for nln in n.loopBrethren if nln.chainID is not None]) is not 0]), c.address))[0]		
		nodes = sorted([ncn for ncn in cycle.nodes if ncn.loop.availabled and not ncn.loop.seen], key = lambda n: (-len([nln for nln in n.loopBrethren if nln.chainID is not None]), n.address))
		
				
		𝒞 = 0
		for node in nodes:
			
			diagram.extendLoop(node.tuple[0].loop)
			diagram.extendLoop(node.tuple[1].loop)
			diagram.pointers = node.tuple
			
			rx(lvl+1, road+[(𝒞, len(nodes))])
			
			diagram.collapseLoop(node.tuple[1].loop)
			diagram.collapseLoop(node.tuple[0].loop)
			𝒞 += 1
			
	
	rx()
		
	# ~~~ ~RX~ ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							

	diagram.pointers = [node]
																											
			
	show(diagram)
	
