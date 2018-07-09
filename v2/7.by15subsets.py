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
	
	diagram.pointers = [node]
	show(diagram)
	
