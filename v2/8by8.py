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
	
	extend(H001.address)
	
	pointTo(H001.address); jmp(3); adv(2); extendPointers()
	pointTo(H001.address); jmp(4);
	
	pointTo('1000206'); extendPointers()
	pointTo('1000307'); extendPointers()
	
	pointTo('1000440'); extendPointers()
	pointTo('1000465'); extendPointers()
	pointTo('1000404'); extendPointers()
	pointTo('1000413'); extendPointers()
	pointTo('1000422'); extendPointers()
	pointTo('1000431'); extendPointers()

	pointTo('1000530'); extendPointers()
	pointTo('1000555'); extendPointers()
	pointTo('1000564'); extendPointers()
	pointTo('1000503'); extendPointers()
	pointTo('1000512'); extendPointers()
	pointTo('1000521'); extendPointers()

	pointTo('1000020'); extendPointers()
	pointTo('1000045'); extendPointers()
	pointTo('1000054'); extendPointers()
	pointTo('1000063'); extendPointers()
	pointTo('1000002'); extendPointers()
	pointTo('1000011'); extendPointers()

	# 1/2
	pointTo('1000210'); extendPointers()
	pointTo('1000235'); extendPointers()
	pointTo('1000244'); extendPointers()
	pointTo('1000253'); extendPointers()
	
	# red
	pointTo('0010305'); extendPointers()
	pointTo('0010314'); extendPointers()
	pointTo('0010323'); extendPointers()
	pointTo('0010332'); extendPointers()
	pointTo('0010341'); extendPointers()
	pointTo('0010350'); extendPointers()
	
	pointTo('0010503'); extendPointers()
	pointTo('0010512'); extendPointers()
	pointTo('0010521'); extendPointers()
	pointTo('0010530'); extendPointers()
	pointTo('0010555'); extendPointers()
	pointTo('0010564'); extendPointers()
	
	pointTo('0131004'); extendPointers()
	pointTo('0131013'); extendPointers()
	pointTo('0131022'); extendPointers()

	pointTo('1104206'); extendPointers() # 0/2	
	pointTo('1104416'); extendPointers() # 1/2
	pointTo('1104452'); extendPointers() # 0/2
	pointTo('1101002'); extendPointers() # 0/2
	pointTo('1110002'); extendPointers() # 0/2
	pointTo('1114315'); extendPointers() # 0/2
	pointTo('0231336'); extendPointers() # 0/2
	pointTo('0104126'); extendPointers() # 0/1
	pointTo('1110013'); extendPointers() # 1/2
	pointTo('1204336'); extendPointers() # 1/2
	pointTo('0224005'); extendPointers() # 1/2
	pointTo('0224125'); extendPointers() # 0/1
	pointTo('1231032'); extendPointers() # 1/2
	pointTo('1231212'); extendPointers() # 0/1
	pointTo('1114102'); extendPointers() # 0/1
	pointTo('1231050'); extendPointers() # 1/2
	#pointTo('1231103'); extendPointers() # 0/1
	#pointTo('1232046'); extendPointers() # 0/1
	
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	unlooped_cycle_count, grouped_cycles_by_av = measure()
	diagram.pointers = sorted([c.avnode() for c in grouped_cycles_by_av[0][1]], key = lambda n: n.address); print("\n".join([str(n) for n in diagram.pointers]))
	#diagram.pointers = diagram.pointers[0].tuple
	show(diagram); 
		
