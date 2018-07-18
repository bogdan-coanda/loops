from diagram import *
from uicanvas import *
from groupby import *
from random import choice, shuffle


def measure():
	unlooped_cycle_count = len([c for c in diagram.cycles if c.chained_by_count is 0])
	grouped_cycles_by_av = sorted(groupby([c for c in diagram.cycles if c.chained_by_count is 0], K = lambda c: c.available_loops_count).items())
	available_loops_count = len([loop for loop in diagram.loops if loop.availabled])
	chains_count = len(set([node.chainID for node in diagram.nodes if node.chainID is not None]))
	print("unlooped cycles: " + str(unlooped_cycle_count))
	print("cycle av counts: " + str([(k, len(v)) for k,v in grouped_cycles_by_av]))			
	print("available loops: " + str(available_loops_count) + "/" + str(len(diagram.loops)))				
	return (unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count)
	
			
def extend(address):		
	global node
	node = diagram.nodeByAddress[address]
	assert diagram.extendLoop(node.loop)		
	diagram.pointers = node.tuple		
		
		
def pointTo(address):
	diagram.pointToAddressTuple(address)
		
def jmp(bid):
	diagram.jmp(bid)
	
def adv(cid):
	diagram.adv(cid)												
		
										
def extendPointers():
	for i,n in enumerate(diagram.pointers):
		assert diagram.extendLoop(n.loop)		

												
if __name__ == "__main__":
	
	diagram = Diagram(7)
	diagram.generateKernel()

	# for node in diagram.nodes:
	# 	node.tuple = [node]
		
	H001 = diagram.nodeByAddress['000001']
	#K454 = diagram.nodeByAddress['000454']
	bases = [H001]#, K454]	
	diagram.walk(bases)
	
	diagram.pointers = list(bases)
	
	diagram.extendLoop(H001.loop)
	
	pointTo('100003'); extendPointers()
	pointTo('100012'); extendPointers()
	pointTo('100021'); extendPointers()
	pointTo('100030'); extendPointers()
	pointTo('100054'); extendPointers()
	
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	'''
	lvl = 0
	chosen = []
	while True:		
		avloops = [loop for loop in diagram.loops if loop.availabled and len([node for node in loop.nodes if node.chainID is not None]) is not 0]
		if len(avloops) is 0:
			unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count = measure()
			print("[random:"+str(lvl)+"] breaking @ " + str(available_loops_count * 100.0 / len(diagram.loops)))
			break
		
		#loop = choice(avloops)
		shuffle(avloops)
		for loop in avloops:	
			print("[random:"+str(lvl)+"] chosen: " + str(loop))
			if not diagram.extendLoop(loop):
				#diagram.pointers = [loop.chnode()]
				#show(diagram)
				print("[random] broken…")
				loop = None
			else:
				break
			
		if loop is None:			
			loop = avloops[0]
			print("[random:"+str(lvl)+"] bypassing short: " + str(loop))
			if not diagram.extendLoop(loop, False):
				print("[random:"+str(lvl)+"] bypassing failed!")
				break
				
		chosen.append(loop)
		lvl += 1
	
																																																										
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count = measure()	
	show(diagram); 
		
