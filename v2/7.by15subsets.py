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
	# [cycle] » blue(0) » green(1) » yellow(2) » orange(3) » red(4) » violet(5) » indigo(6)
	
	unlooped_cycle_count, grouped_cycles_by_av = measure()
	
	# spark
	#extend('000001') # violet(5) | I: @3 ~ blue(α)
	extend('000354') # violet(5) | I: @5 ~ blue(β)
	
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
	#extend('100002')
	#extend('100011')
	extend('100020') # I. | » x | red
	#extend('100044')
	#extend('100053')		
	
	
			
	unlooped_cycle_count, grouped_cycles_by_av = measure()
	
	# ~~~ walk ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							
	print("~~~ walk ~ ~~~")
	
	nodes = [diagram.nodeByAddress['000001'], diagram.nodeByAddress['000354'])]
	
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
	
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							
		
	diagram.pointers = diagram.nodeByAddress['000001'].tuple
	show(diagram)
	
