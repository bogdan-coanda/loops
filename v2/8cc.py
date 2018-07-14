from diagram import *
from uicanvas import *
from groupby import *


def measure():
	unlooped_cycle_count = len([c for c in diagram.cycles if c.chained_by_count is 0])
	grouped_cycles_by_av = sorted(groupby([c for c in diagram.cycles if c.chained_by_count is 0], K = lambda c: c.available_loops_count).items())
	print("unlooped cycles: " + str(unlooped_cycle_count))
	print("cycle av counts: " + str([(k, len(v)) for k,v in grouped_cycles_by_av]))			
	return (unlooped_cycle_count, grouped_cycles_by_av)
			
def extend(address):		
	global node
	node = diagram.nodeByAddress[address]
	assert diagram.extendLoop(node.loop)		
	diagram.pointers = node.tuple		
		
		
def pointTo(address):
	diagram.pointToAddressTuple(address)

def repointTo(address):
	diagram.pointToAddressTuple(diagram.nodeByReaddress[address].address)
	
					
def jmp(bid):
	diagram.jmp(bid)
	
def adv(cid):
	diagram.adv(cid)												
		
										
def extendPointers():
	for i,n in enumerate(diagram.pointers):
		assert diagram.extendLoop(n.loop)		


def unwant():
	unwanted_loops = [loop for loop in diagram.loops if loop.availabled and len([node for node in loop.nodes if node.chainID is not None and node.chainID is not 0]) > 1]
	print("unwanted loops: " + str(len(unwanted_loops)) + " | av. loops: " + str(len([loop for loop in diagram.loops if loop.availabled])) + "/" + str(len(diagram.loops)))
	
	for loop in unwanted_loops:
		diagram.setLoopUnavailabled(loop)



																																				
if __name__ == "__main__":
	
	diagram = Diagram(8)
	diagram.generateKernel()
	
	H001 = diagram.nodeByAddress['0000001']
	H201 = diagram.nodeByAddress['0000201'] 		
	H401 = diagram.nodeByAddress['0000401']
	K165 = diagram.nodeByAddress['0000165']
	K365 = diagram.nodeByAddress['0000365']
	K565 = diagram.nodeByAddress['0000565']
	
	bases = [H001, K165, H201, K365, H401, K565]
	
	diagram.walk(bases)
	
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''	
	
	pairsperboxcount = [set([":".join(sorted([n.address[:4] for n in t[:X]])) for t in diagram.tuples if len(set([n.address[:4] for n in t])) is X]) for X in range(1, 7)]
	for pairs in pairsperboxcount:
		print("len: " + str(len(pairs)))
		
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	
	pointTo('1234505'); extendPointers()
	pointTo('1234514'); extendPointers()
	pointTo('1234523'); extendPointers()
	
	pointTo('1234125'); extendPointers()
	pointTo('1234134'); extendPointers()
	
	unwant()
	
	pointTo('0134406'); extendPointers()
	pointTo('0134007'); extendPointers()
	pointTo('0134107'); extendPointers()
	pointTo('0134307'); extendPointers()
	pointTo('0134507'); extendPointers()
	
	unwant()
	#~~~#
	#pointTo('1114106'); extendPointers()
	#pointTo('1114007'); extendPointers()
	#pointTo('1114207'); extendPointers()	

	unwant()
	
	#pointTo('1134007'); extendPointers()	
	#pointTo('1134407'); extendPointers()	

	#unwant()
																																																																										
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	#unlooped_cycle_count, grouped_cycles_by_av = measure()
	#diagram.pointers = sorted([c.avnode() for c in grouped_cycles_by_av[0][1]], key = lambda n: n.address); print("\n".join([str(n) for n in diagram.pointers]))
	#diagram.pointers = diagram.pointers[0].tuple
	'''	
	for loop in diagram.loops:
		lc = len([n for n in loop.nodes if n.address.startswith('1234')])
		if lc < 2 or lc == 7:
			loop.availabled = False
	'''
	'''
	diagram.reorder('12345670') # green⇒blue
	
	
	repointTo('1021207'); extendPointers(); unwant()
	repointTo('1021407'); extendPointers(); unwant()
	
	repointTo('1023007'); extendPointers(); unwant()
	repointTo('1023207'); extendPointers(); unwant()
	
	diagram.reorder('23456701') # green⇒black

	repointTo('0113307'); extendPointers(); unwant()
	repointTo('0113507'); extendPointers(); unwant()
			
	repointTo('0222307'); extendPointers(); unwant()
	repointTo('0222507'); extendPointers(); unwant()
	
	repointTo('0204307'); extendPointers(); unwant()
	repointTo('0204507'); extendPointers(); unwant()
	
	diagram.reorder('34567012') # green⇒indigo
	
	repointTo('1124107'); extendPointers(); unwant()
	repointTo('1124307'); extendPointers(); unwant()

	repointTo('1032007'); extendPointers(); unwant()
	repointTo('1032407'); extendPointers(); unwant()

	repointTo('0124307'); extendPointers(); unwant()
	repointTo('0124507'); extendPointers(); unwant()
	
	repointTo('1204307'); extendPointers(); unwant()
	repointTo('1213307'); extendPointers(); unwant()
	repointTo('1222307'); extendPointers(); unwant()
							
	diagram.reorder('45670123') # green⇒violet

	repointTo('0232307'); extendPointers(); unwant()
	repointTo('0232507'); extendPointers(); unwant()

	repointTo('1131107'); extendPointers(); unwant()
	repointTo('1131307'); extendPointers(); unwant()
	
	repointTo('1004207'); extendPointers(); unwant()

	diagram.reorder('01234567') # green⇒green

	repointTo('0001556'); extendPointers()	
	repointTo('0130310'); extendPointers()
	repointTo('0131314'); extendPointers()	
	repointTo('0034013'); extendPointers()		



	#repointTo('1210007'); extendPointers(); unwant()
	#repointTo('1210407'); extendPointers(); unwant()
																													
	#'''
	'''
	repointTo('1202007'); extendPointers()
	repointTo('1202207'); extendPointers()

	repointTo('1201107'); extendPointers()
	repointTo('1201307'); extendPointers()
			
	unlooped_cycle_count, grouped_cycles_by_av = measure()
	
	diagram.reorder('01234567')
	'''
	
	unlooped_cycle_count, grouped_cycles_by_av = measure()
	show(diagram); 
		
