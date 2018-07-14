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
	K454 = diagram.nodeByAddress['000454']
	bases = [H001, K454]	
	diagram.walk(bases)
	
	diagram.pointers = list(bases)
	
	#extendPointers()
	#jmp(0); # adv: 2,3,4,5
	#jmp(1); # adv: 2,3,4,5
	#jmp(2); # adv: 2,4,5
	#jmp(3); # adv: 3,4,5
	#jmp(4); # adv: 2,3,4,5
	
	# ~~~ binders ~~~
	'''
	#extend(H001.address)
	#extend(K454.address)
	
	# @100:0:red # 0/3
	pointTo('100002'); extendPointers()
	pointTo('100011'); extendPointers()
	pointTo('100020'); extendPointers()
	pointTo('100044'); extendPointers()
	pointTo('100053'); extendPointers()
	
	# @010:green
	pointTo('010205'); extendPointers()

	# @010:4:violet # 1/2
	pointTo('010401'); extendPointers()
	pointTo('010410'); extendPointers()
	pointTo('010434'); extendPointers()
	pointTo('010443'); extendPointers()
	pointTo('010452'); extendPointers()

	# @120:2&3:indigo
	pointTo('120200'); extendPointers()
	pointTo('120224'); extendPointers()
	pointTo('120233'); extendPointers()
	pointTo('120242'); extendPointers()
	pointTo('120251'); extendPointers()
	
	# @011:2:indigo # 0/3
	pointTo('011204'); extendPointers()
	pointTo('011213'); extendPointers()
	pointTo('011222'); extendPointers()
	pointTo('011231'); extendPointers()
	pointTo('011240'); extendPointers()
		
	# @121:green
	#pointTo('121205'); extendPointers()
					
	# @121:0:violet
	#pointTo('121000'); extendPointers()		
		
	# @121:0:indigo
	#pointTo('121001'); extendPointers()
	#pointTo('121010'); extendPointers()
	#pointTo('121034'); extendPointers()
	#pointTo('121043'); extendPointers()
	#pointTo('121052'); extendPointers()

	# @103:4:red
	#pointTo('103404'); extendPointers()
	#pointTo('103413'); extendPointers()
	#pointTo('103422'); extendPointers()
	#pointTo('103431'); extendPointers()
	#pointTo('103440'); extendPointers()

	# @112:0:yellow
	#pointTo('112004'); extendPointers()
	
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	
	# pointTo('123100'); extendPointers()
	# pointTo('123124'); extendPointers()
	# pointTo('123133'); extendPointers()
	# pointTo('123142'); extendPointers()
	# pointTo('123151'); extendPointers()
	# 
	# pointTo('123000'); extendPointers()
	# pointTo('123024'); extendPointers()
	# pointTo('123033'); extendPointers()
	# pointTo('123042'); extendPointers()
	# pointTo('123051'); extendPointers()
		
	pointTo('123404'); extendPointers()
	pointTo('123413'); extendPointers()	
	pointTo('123422'); extendPointers()
	pointTo('123431'); extendPointers()
	pointTo('123440'); extendPointers()
	
	pointTo('123200'); extendPointers()
	pointTo('123224'); extendPointers()
	
	pointTo('023230'); extendPointers()
	pointTo('023254'); extendPointers()
	
	'''
	# pointTo('102205'); extendPointers()
	pointTo('111205'); extendPointers()
	# pointTo('120205'); extendPointers()
	
	pointTo('102105'); extendPointers()
	pointTo('102305'); extendPointers()
	# pointTo('111105'); extendPointers()
	# pointTo('111305'); extendPointers()
	pointTo('120105'); extendPointers()
	pointTo('120305'); extendPointers()
	
	pointTo('102403'); extendPointers()
	pointTo('102412'); extendPointers()
	pointTo('102421'); extendPointers()
	pointTo('102430'); extendPointers()
	pointTo('102454'); extendPointers()
	
	pointTo('122003'); extendPointers()
	pointTo('122012'); extendPointers()
	pointTo('122021'); extendPointers()
	pointTo('122030'); extendPointers()
	pointTo('122054'); extendPointers()
	
	pointTo('111245'); extendPointers()
	pointTo('111221'); extendPointers()
	pointTo('111212'); extendPointers()
	'''
	'''
	pointTo('123404'); extendPointers()
	pointTo('123413'); extendPointers()	
	pointTo('123422'); extendPointers()
	pointTo('123431'); extendPointers()
	pointTo('123440'); extendPointers()
	
	pointTo('123224'); extendPointers()
	pointTo('123233'); extendPointers()
	pointTo('123242'); extendPointers()

	pointTo('123204'); extendPointers()
	pointTo('123213'); extendPointers()	
	pointTo('123222'); extendPointers()
	pointTo('123231'); extendPointers()
	pointTo('123240'); extendPointers()
			
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
								
	'''
	diagram.pointers = [
		diagram.nodeByAddress['1234000'],
		diagram.nodeByAddress['1234025'],
		diagram.nodeByAddress['1234034'],
		diagram.nodeByAddress['1234043'],
		diagram.nodeByAddress['1234052'],
		diagram.nodeByAddress['1234061']
	]; extendPointers()

	diagram.pointers = [
		diagram.nodeByAddress['1234125'],
		diagram.nodeByAddress['1234134'],
		diagram.nodeByAddress['1234143'],
		diagram.nodeByAddress['1234152']
	]; extendPointers()
	'''							
																																																																							
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	unlooped_cycle_count, grouped_cycles_by_av = measure()
	#diagram.pointers = sorted([c.avnode() for c in grouped_cycles_by_av[0][1]], key = lambda n: n.address); print("\n".join([str(n) for n in diagram.pointers]))
	#diagram.pointers = diagram.pointers[0].tuple
	'''
	for loop in diagram.loops:
		lc = len([n for n in loop.nodes if n.address.startswith('123')])
		if lc < 2 or lc == 6:
			loop.availabled = False
	'''
	
	show(diagram); 
		
