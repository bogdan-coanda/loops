from diagram import *
from uicanvas import *
from groupby import *


if __name__ == "__main__":
	
	diagram = Diagram(6)
	diagram.generateKernel()

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
	
	# binders
	#extend('00001')
	#extend('00143')
	#extend('00201')
	#extend('00343')
				
	# islands
	# I.
	extend('10105')
	extend('10305')
	extend('10204')
	#'''	
	'''# II.
	extend('11005')
	extend('11205')
	extend('11104')
	#'''
	'''# III.
	extend('01105')
	extend('01305')
	extend('01204')	
	#'''
	'''# IV.
	extend('02005')
	extend('02205')
	extend('02104')
	#'''	
	
	extend('10020') # I.   | » x
	#extend('11310') # II.  | » x
	#extend('10011') # III. | » x
	#extend('11333') # IV.  | » x
	
	extend('01211') # I.   | » y
	#extend('01220') # II.	| » y
	#extend('10233') # III. | » y
	#extend('10210') # IV.  | » y
	
	extend('11301') # I.   | » z
	#extend('10043') # II.	| » z	
	#extend('11342') # III. | » z
	#extend('10002') # IV.  | » z	

					
	'''
	# spark
	extend('00001')		
				
	# island @ 10
	extend('10105')
	extend('10305')
	extend('10204')
				
	# s.diag @ 10 - yellow
	extend('10210')
	extend('10233')
	
	# p.diag @ 10 - orange
	extend('10002')
	extend('10011')
	extend('10020')
	extend('10043')
	'''						
	'''
	bros = list(sparkNode.loopBrethren)		
	
	while len(bros) > 0:
		base = sorted(bros, key = lambda n: (n.cycle.available_loops_count, n.address))[0]
		node = sorted([ncn for ncn in base.cycle.nodes if ncn.loop.availabled and not ncn.loop.seen], key = lambda n: n.ktype)[0]
		diagram.extendLoop(node.loop)	
		bros.remove(base)	
		measure()
		
	
	rxcc = 0
	def rx(lvl=0, road=[]):
		global rxcc
		
		unlooped_cycle_count, grouped_cycles_by_av = measure()
		#if unlooped_cycle_count < 10:
		show(diagram)
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
			
			diagram.extendLoop(node.loop)
			diagram.pointers = [node]
			
			rx(lvl+1, road+[(𝒞, len(nodes))])
			
			diagram.collapseLoop(node.loop)
			𝒞 += 1
			
	
	rx()
		
	# ~~~~~~~~~~~~~~~~~~~ #'''

	diagram.pointers = [node]
																											
			
	show(diagram)
