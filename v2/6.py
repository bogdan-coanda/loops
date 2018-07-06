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
		
	measure()		
		
	sparkNode = diagram.nodeByAddress['00001']
	diagram.extendLoop(sparkNode.loop)
	
	measure()
	
	bros = list(sparkNode.loopBrethren)		
	base = sorted(bros, key = lambda n: (n.cycle.available_loops_count, n.address))[0]
	node = sorted([ncn for ncn in base.cycle.nodes if ncn.loop.availabled and not ncn.loop.seen], key = lambda n: n.ktype)[0]
	diagram.extendLoop(node.loop)	
	
	measure()
	
	bros.remove(base)
	base = sorted(bros, key = lambda n: (n.cycle.available_loops_count, n.address))[0]
	node = sorted([ncn for ncn in base.cycle.nodes if ncn.loop.availabled and not ncn.loop.seen], key = lambda n: n.ktype)[0]
	diagram.extendLoop(node.loop)

	measure()

	bros.remove(base)
	base = sorted(bros, key = lambda n: (n.cycle.available_loops_count, n.address))[0]
	node = sorted([ncn for ncn in base.cycle.nodes if ncn.loop.availabled and not ncn.loop.seen], key = lambda n: n.ktype)[0]
	diagram.extendLoop(node.loop)

	measure()

	bros.remove(base)
	base = sorted(bros, key = lambda n: (n.cycle.available_loops_count, n.address))[0]
	node = sorted([ncn for ncn in base.cycle.nodes if ncn.loop.availabled and not ncn.loop.seen], key = lambda n: n.ktype)[0]
	diagram.extendLoop(node.loop)
			
	unlooped_cycle_count, grouped_cycles_by_av = measure()
	
	def extend(index):
		global node, cycle, unlooped_cycle_count, grouped_cycles_by_av
		cycle = grouped_cycles_by_av[0][1][0]
		node = sorted([ncn for ncn in cycle.nodes if ncn.loop.availabled and not ncn.loop.seen], key = lambda n: n.ktype)[index]
		diagram.extendLoop(node.loop)		
		return measure()

	def extendList(list):
		global unlooped_cycle_count, grouped_cycles_by_av
		for x in list:			
			unlooped_cycle_count, grouped_cycles_by_av = extend(int(x))

	rxcc = 0
	def rx(lvl=0, road=[]):
		global rxcc
		
		unlooped_cycle_count, grouped_cycles_by_av = measure()
		if unlooped_cycle_count < 10:
			show(diagram)
		print("[rx:"+str(lvl)+":"+str(rxcc)+"] road: " + " ".join([str(k)+"/"+str(v) for k,v in road]))
		rxcc += 1
		
		if unlooped_cycle_count is 0:
			if len(set([n.chainID for n in diagram.nodes])) is 1:
				input("Found!!!")
			return
			
					
		cycle = grouped_cycles_by_av[0][1][0]		
		nodes = sorted([ncn for ncn in cycle.nodes if ncn.loop.availabled and not ncn.loop.seen], key = lambda n: n.ktype)
	
		𝒞 = 0
		for node in nodes:
			
			diagram.extendLoop(node.loop)
			diagram.pointers = [node]
			
			rx(lvl+1, road+[(𝒞, len(nodes))])
			
			diagram.collapseLoop(node.loop)
			𝒞 += 1
			
	
	rx()
	
	#extendList("000000000000001000")
	
	# ~~~~~~~~~~~~~~~~~~~ #'''

	diagram.pointers = [node]
																											
			
	show(diagram)
