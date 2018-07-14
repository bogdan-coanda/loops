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
	nodes = None
			
	def extend(address):		
		global node
		node = diagram.nodeByAddress[address]
		assert diagram.extendLoop(node.loop)		
		diagram.pointers = node.tuple
		
	# ~~~ walk ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							
	print("~~~ walk ~ ~~~")

	diagram.walk([diagram.nodeByAddress['000001'], diagram.nodeByAddress['000154']])	
	
	def extendList(nodes):
		for n in nodes:
			extend(n.address)
		diagram.pointers = nodes
	
	def pointTo(address):
		global nodes
		diagram.pointers = diagram.nodeByAddress[address].tuple
		nodes = list(diagram.pointers)
		
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
					
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''									
	# [cycle] » blue(0) » green(1) » yellow(2) » orange(3) » red(4) » violet(5) » indigo(6)
	
	unlooped_cycle_count, grouped_cycles_by_av = measure()

	#extend('000001') # violet(5) | I: @3 ~ blue(α)	
	extend('000154') # yellow(2)
	
	pointTo('000001'); jmp(2); adv(2); extendList(nodes) # blue
	
	pointTo('000001'); jmp(3); adv(3); extendList(nodes) # red/orange
	
	extendList(diagram.nodeByAddress['100002'].tuple)
	extendList(diagram.nodeByAddress['100020'].tuple)
	extendList(diagram.nodeByAddress['100044'].tuple)
	extendList(diagram.nodeByAddress['100053'].tuple)
	
	extendList(diagram.nodeByAddress['100205'].tuple)
	extendList(diagram.nodeByAddress['100306'].tuple)
	extendList(diagram.nodeByAddress['100403'].tuple)
	extendList(diagram.nodeByAddress['100412'].tuple)
	extendList(diagram.nodeByAddress['100421'].tuple)
	extendList(diagram.nodeByAddress['100430'].tuple)
	extendList(diagram.nodeByAddress['100454'].tuple)
	
	# 0/2 - orange
	extendList(diagram.nodeByAddress['100210'].tuple)
	extendList(diagram.nodeByAddress['100234'].tuple)
	extendList(diagram.nodeByAddress['100243'].tuple)
	
	# 0/2 - violet
	extendList(diagram.nodeByAddress['010353'].tuple)
	extendList(diagram.nodeByAddress['010344'].tuple)
	extendList(diagram.nodeByAddress['010320'].tuple)
	extendList(diagram.nodeByAddress['010311'].tuple)
	extendList(diagram.nodeByAddress['010302'].tuple)
	
	extendList(diagram.nodeByAddress['103305'].tuple)
	extendList(diagram.nodeByAddress['103206'].tuple)
	extendList(diagram.nodeByAddress['103406'].tuple)
	extendList(diagram.nodeByAddress['103153'].tuple)
	extendList(diagram.nodeByAddress['103144'].tuple)
	extendList(diagram.nodeByAddress['103120'].tuple)
	
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	'''
	# spark
	extend('000001') # violet(5) | I: @3 ~ blue(α)
	#extend('000354') # violet(5) | I: @5 ~ blue(β)
	
	# island @ 100 | I.
	extend('100106')
	extend('100306')
	extend('100205')

	# island @ 110 | II.
	extend('110006') # blue(β)
	extend('110206') # blue(α)
	extend('110105') # green(1)
			
	# s.diag @ 100 - yellow
	#extend('100211')
	#extend('100220')
	#extend('100244')
	
	# p.diag @ 100 - red
	#extendList(diagram.nodeByAddress['100002'].tuple)
	#extend('100011')
	#extend('100020') # I. | » x | red
	#extend('100044')
	#extend('100053')		
				
	unlooped_cycle_count, grouped_cycles_by_av = measure()
			
	diagram.pointers = diagram.nodeByAddress['000001'].tuple
	nodes = diagram.pointers
	
	#jmp(0); adv(4)
	#jmp(2); adv(2); jmp(0); adv(5); jmp(4); adv(4); extendList(nodes)
	#jmp(1); adv(2); extendList(nodes);
	#jmp(4); adv(2); extendList(nodes);
	
	#extendList(diagram.nodeByAddress['100002'].tuple)
	#extendList(diagram.nodeByAddress['100011'].tuple)
	#extendList(diagram.nodeByAddress['100044'].tuple)
	
	#extend('010221')
	
	#extendList(diagram.nodeByAddress['010205'].tuple)
	#extendList(diagram.nodeByAddress['010106'].tuple)
	#extendList(diagram.nodeByAddress['010306'].tuple)

	#extendList(diagram.nodeByAddress['100210'].tuple)
	#extendList(diagram.nodeByAddress['100234'].tuple)
	#extendList(diagram.nodeByAddress['100243'].tuple)

	extend(diagram.nodeByAddress['100211'].tuple[0].address)
	extend(diagram.nodeByAddress['100244'].tuple[0].address)		
	extend(diagram.nodeByAddress['100220'].tuple[1].address)	

	#extend(diagram.nodeByAddress['100220'].tuple[0].address)	
	#extend(diagram.nodeByAddress['100211'].tuple[1].address)
	#extend(diagram.nodeByAddress['100244'].tuple[1].address)		

	#extendList(diagram.nodeByAddress['100211'].tuple)
	#extendList(diagram.nodeByAddress['100220'].tuple)
	#extendList(diagram.nodeByAddress['100244'].tuple)
	
	extendList(diagram.nodeByAddress['122215'].tuple)
	extendList(diagram.nodeByAddress['122224'].tuple)
	extendList(diagram.nodeByAddress['122233'].tuple)
	
	extendList(diagram.nodeByAddress['122122'].tuple)
	extendList(diagram.nodeByAddress['122131'].tuple)
	extendList(diagram.nodeByAddress['122140'].tuple)
	
	extendList(diagram.nodeByAddress['013044'].tuple)
	extendList(diagram.nodeByAddress['013053'].tuple)
	
	extendList(diagram.nodeByAddress['012243'].tuple)
	extendList(diagram.nodeByAddress['012252'].tuple)	
	
	extend('101105')
	extend('101006')
	extend('101206')
	
	extend('011105')
	extend('011006')
	extend('011206')
	
	extendList(diagram.nodeByAddress['110105'].tuple)
	extendList(diagram.nodeByAddress['110006'].tuple)
	extendList(diagram.nodeByAddress['110206'].tuple)	
	
	extendList(diagram.nodeByAddress['113205'].tuple)
	extendList(diagram.nodeByAddress['113106'].tuple)
	extendList(diagram.nodeByAddress['113306'].tuple)
	
	#diagram.pointers = diagram.nodeByAddress['103120'].tuple
	extendList(diagram.nodeByAddress['103120'].tuple)
	extendList(diagram.nodeByAddress['103111'].tuple)
	extendList(diagram.nodeByAddress['103102'].tuple)
	extendList(diagram.nodeByAddress['103144'].tuple)
	extendList(diagram.nodeByAddress['103153'].tuple)
	
	extendList(diagram.nodeByAddress['013305'].tuple)
	extendList(diagram.nodeByAddress['013206'].tuple)
	extendList(diagram.nodeByAddress['013406'].tuple)
	
	unlooped_cycle_count, grouped_cycles_by_av = measure()	
	extendList(grouped_cycles_by_av[0][1][0].avnode().tuple)
	
	unlooped_cycle_count, grouped_cycles_by_av = measure()
	extendList(grouped_cycles_by_av[0][1][0].avnode().tuple)

	unlooped_cycle_count, grouped_cycles_by_av = measure()
	extend(grouped_cycles_by_av[0][1][0].avnode().address)
	
	unlooped_cycle_count, grouped_cycles_by_av = measure()
	extendList(grouped_cycles_by_av[0][1][0].avnode().tuple)
	
	extendList(diagram.nodeByAddress['100053'].tuple)
	extendList(diagram.nodeByAddress['100002'].tuple)
	
	extend('100210')
	extend('100243')
	
	extend('112305')
	extend('112206')
	extend('112406')
			
	extendList(diagram.nodeByAddress['112012'].tuple)
	extendList(diagram.nodeByAddress['112003'].tuple)
	extendList(diagram.nodeByAddress['112021'].tuple)
	extendList(diagram.nodeByAddress['112030'].tuple)
	extendList(diagram.nodeByAddress['112054'].tuple)
	
	extendList(diagram.nodeByAddress['100412'].tuple)
	extendList(diagram.nodeByAddress['100403'].tuple)
	extendList(diagram.nodeByAddress['100421'].tuple)
	extendList(diagram.nodeByAddress['100430'].tuple)
	extendList(diagram.nodeByAddress['100454'].tuple)
	
	#extendList(diagram.nodeByAddress['010306'].tuple)
	#extendList(diagram.nodeByAddress['010106'].tuple)
	#extendList(diagram.nodeByAddress['010223'].tuple)
	#diagram.pointers = diagram.nodeByAddress['010223'].tuple
	#extend('010223')
							
	extendList(diagram.nodeByAddress['011110'].tuple)
	
	unlooped_cycle_count, grouped_cycles_by_av = measure()
	extendList(grouped_cycles_by_av[0][1][0].avnode().tuple)
	
	extendList(diagram.nodeByAddress['010235'].tuple)
	extendList(diagram.nodeByAddress['010211'].tuple)
	
	unlooped_cycle_count, grouped_cycles_by_av = measure()
	extendList(grouped_cycles_by_av[0][1][0].avnode().tuple)

	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	show(diagram); measure()
