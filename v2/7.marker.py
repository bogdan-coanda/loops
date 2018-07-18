from diagram import *
from uicanvas import *
from groupby import *
from random import choice, shuffle
from itertools import chain

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
	
def jtm():
	if diagram.pointers[0].cycle.marker is not None:
		return
	
	for i,bro in enumerate(diagram.pointers[0].loopBrethren):
		if bro.cycle.marker is not None:
			jmp(i)
			return
	
def adv(cid):
	diagram.adv(cid)												
		
										
def extendPointers():
	for i,n in enumerate(diagram.pointers):
		assert diagram.extendLoop(n.loop)
		for bro in n.loopBrethren:
			assert bro.cycle.marker is None or bro.cycle.marker is n.cycle.marker
			bro.cycle.marker = n.cycle.marker


def markCycle(addr, marker):
	diagram.cycleByAddress[addr].marker = marker


def extendBar(addr, last):
	off = 0
	for i in range(5):
		node = diagram.nodeByAddress[addr+str(i+off)+str((last-i-off)%6)]
		if node.cycle.marker is None and last is i and diagram.nodeByAddress[addr+str(i+off)+str((last-i-off)%6)].cycle.marker is not None:
			node = diagram.nodeByAddress[addr+(i+1)+((last-i-1)%6)]
		pointTo(node.address); extendPointers()
		if i is last:
			off = 1
		
		
def extendMid(addr, last):
	off = 0
	for i in range(3):
		node = diagram.nodeByAddress[addr+str(1+i+off)+str((last-i-off)%6)]
		if node.cycle.marker is None and last is i and diagram.nodeByAddress[addr+str(1+i+off)+str((last-i-off)%6)].cycle.marker is not None:
			node = diagram.nodeByAddress[addr+(1+i+1)+((last-i-1)%6)]
		pointTo(node.address); extendPointers()
		if i is last:
			off = 1
			
def extendFifth(addr):
	pointTo(addr+'042'); extendPointers()	
	pointTo(addr+'142'); extendPointers()	
	pointTo(addr+'242'); extendPointers()	
	pointTo(addr+'342'); extendPointers()	
	pointTo(addr+'442'); extendPointers()	

	pointTo(addr+'033'); extendPointers()
	pointTo(addr+'133'); extendPointers()
	pointTo(addr+'233'); extendPointers()
	pointTo(addr+'333'); extendPointers()
	pointTo(addr+'433'); extendPointers()
													
	pointTo(addr+'024'); extendPointers()
	pointTo(addr+'124'); extendPointers()
	pointTo(addr+'224'); extendPointers()
	pointTo(addr+'324'); extendPointers()
	pointTo(addr+'424'); extendPointers()
	
	
def unwant():
	unwanted_loops = [loop for loop in diagram.loops if loop.availabled and (len([node for node in loop.nodes if node.chainID is not None and node.chainID is not 0]) > 1 or len([node for node in loop.nodes if node.chainID is 0]) > 0)]
	print("unwanted loops: " + str(len(unwanted_loops)) + " | av. loops: " + str(len([loop for loop in diagram.loops if loop.availabled])) + "/" + str(len(diagram.loops)))
	
	for loop in unwanted_loops:
		diagram.setLoopUnavailabled(loop)
			
																																																								
																								
if __name__ == "__main__":
	
	diagram = Diagram(7)
	diagram.generateKernel()
	
	diagram.pointers = list(diagram.nodeByAddress['123042'].loop.nodes)
	
	bases = [diagram.nodeByAddress[addr] for addr in ['123042', '123142', '123242', '123342', '123442']]
	
	diagram.monowalk(bases)
	
	pairsperboxcount = [set([":".join(sorted([n.address[:3] for n in t[:X]])) for t in diagram.tuples if len(set([n.address[:3] for n in t])) is X]) for X in range(1, 6)]
	for pairs in pairsperboxcount:
		print("len: " + str(len(pairs)))
					
	for pairsindex, pairs in enumerate(pairsperboxcount):
		for pair in pairs:
			boxes = pair.split(':')
			for box in boxes:
				print(str(pairsindex) + " | " + box)
				boxcycles = sorted([cycle for cycle in diagram.cycles if cycle.address.startswith(box)], key = lambda c: c.address)
				mincycle = boxcycles[0]
				maxcycle = boxcycles[-1]
				diagram.draw_boxes.append((pairsindex, mincycle.px, mincycle.py, maxcycle.px - mincycle.px, maxcycle.py - mincycle.py))
	
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
		
	markCycle('12304', 3)
	markCycle('12314', 4)
	markCycle('12324', 5)
	markCycle('12334', 1)
	markCycle('12344', 2)

	# 123:mid
	pointTo('123042'); extendPointers()					
	pointTo('123033'); extendPointers()					
	pointTo('123024'); extendPointers()
	unwant()
	#pointTo('123001'); jmp(3); extendPointers()	# 123:top
	#pointTo('123054'); jmp(1); extendPointers() # 123:bot
	
	#pointTo('123001'); jmp(0); adv(4); extendPointers()
	#pointTo('123054'); jmp(4); adv(3); extendPointers()

	# 112:mid
	#pointTo('112001'); jmp(4); extendPointers() # 112:top
	pointTo('112024'); jmp(1); extendPointers()							
	pointTo('112033'); jmp(4); extendPointers()					
	pointTo('112042'); jmp(4); extendPointers()					
	#pointTo('112054'); #jmp(1); #extendPointers() # 112:bot
			
	# 011:mid
	#pointTo('011054'); jmp(3); extendPointers()	# 011:bot		
	pointTo('011042'); jmp(2); extendPointers()					
	pointTo('011033'); extendPointers()					
	pointTo('011024'); extendPointers()						
	#pointTo('011002'); jmp(1); extendPointers()	# 011:top # 0/2
	#pointTo('011003'); extendPointers()	# 011:top # 1/2
	
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
		
	#pointTo('123003'); jtm(); extendPointers(); diagram.pointers = list(chain(*[node.loop.nodes for node in diagram.pointers]))
	#pointTo('112003'); jtm(); extendPointers(); diagram.pointers = list(chain(*[node.loop.nodes for node in diagram.pointers]))
	#pointTo('011003'); jtm(); extendPointers(); diagram.pointers = list(chain(*[node.loop.nodes for node in diagram.pointers]))
	
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''

	unwant()

	#pointTo('101336'); jtm(); extendPointers(); #unwant() # 1/2
	#pointTo('101426'); jtm(); extendPointers(); #unwant() # 1/2
	#pointTo('102326'); jtm(); extendPointers(); #unwant() # 1/2		
	#pointTo('122336'); jtm(); extendPointers(); #unwant() # 1/2
	#pointTo('111226'); jtm(); extendPointers(); #unwant() # 1/2
	#pointTo('111336'); jtm(); extendPointers(); #unwant() # 1/2
	
	#pointTo('100326'); jtm(); extendPointers(); #unwant() # 1/2
	#pointTo('100216'); jtm(); extendPointers(); #unwant() # 1/2
	#pointTo('100436'); jtm(); extendPointers(); #unwant() # 0/1
	#pointTo('100026'); jtm(); extendPointers(); #unwant() # 1/2
	#pointTo('101126'); jtm(); extendPointers(); #unwant() # 1/2
	#pointTo('011004'); jtm(); extendPointers(); #unwant() # 2/3
	#pointTo('101201'); jtm(); extendPointers(); #unwant() # 1/2
	#pointTo('112003'); jtm(); extendPointers(); #unwant() # 1/2
	#pointTo('111403'); jtm(); extendPointers(); #unwant() # 0/1
	#pointTo('011055'); jtm(); extendPointers(); #unwant() # 1/2
	#pointTo('101005'); jtm(); extendPointers(); #unwant() # 1/2
	#pointTo('123054'); jtm(); extendPointers(); #unwant() # 0/1
	#pointTo('122004'); jtm(); extendPointers(); #unwant() # 1/2

	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	
	pointTo('101312'); jtm(); extendPointers(); unwant() # 0/2
	pointTo('101326'); jtm(); extendPointers(); unwant() # 0/1
	#pointTo('011003'); jtm(); extendPointers(); unwant() # 2/3
	#pointTo('101121'); jtm(); extendPointers(); unwant() # 0/1
	#pointTo('101336'); jtm(); extendPointers(); unwant() # 0/1
	#pointTo('101003'); jtm(); extendPointers(); #unwant() # 0/1
	
	#pointTo('113236'); jtm(); extendPointers(); #unwant() # 1/2
	#pointTo('100326'); jtm(); extendPointers(); #unwant() # 0/1
	#pointTo('100216'); jtm(); extendPointers(); #unwant() # 0/1
	#pointTo('100436'); jtm(); extendPointers(); #unwant() # 0/1
	#pointTo('101326'); jtm(); extendPointers(); #unwant() # 0/1
	#pointTo('100105'); jtm(); extendPointers(); #unwant() # 1/2
	
	#pointTo('101205'); jtm(); extendPointers(); #unwant() # 0/1
	#pointTo('101125'); jtm(); extendPointers(); #unwant() # 0/1
	#pointTo('122240'); jtm(); extendPointers(); #unwant() # 0/1
	#pointTo('112055'); jtm(); extendPointers(); #unwant() # 1/2
	
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count = measure()	
	diagram.pointers = [cycle.avnode() for cycle in grouped_cycles_by_av[0][1]]	
			
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''														
	'''
	pointTo('000001'); diagram.pointers = list(chain(*[node.loop.nodes for node in diagram.pointers]))
	
	for node in diagram.pointers:
		if node.loop.availabled:
			diagram.setLoopUnavailabled(node.loop)
	adv(1)
	for node in diagram.pointers:
		if node.loop.availabled:		
			diagram.setLoopUnavailabled(node.loop)	
	adv(5)
	for node in diagram.pointers:
		if node.loop.availabled:			
			diagram.setLoopUnavailabled(node.loop)	
	adv(1)
	
	pointTo('021211'); jtm(); extendPointers() # 0/1
	pointTo('010034'); jtm(); extendPointers() # 1/2
	pointTo('113126'); jtm(); extendPointers() # 1/2
	pointTo('122326'); jtm(); extendPointers() # 1/2
	pointTo('101316'); jtm(); extendPointers() # 1/2
	pointTo('021446'); jtm(); extendPointers() # 1/2
	pointTo('101446'); jtm(); extendPointers() # 1/2
	pointTo('110036'); jtm(); extendPointers() # 1/2
	#pointTo('021143'); jtm(); extendPointers() # 1/2
	#pointTo('010001'); jtm(); extendPointers() # 0/1
	#pointTo('122240'); jtm(); extendPointers() # 0/1
	#pointTo('010154'); jtm(); extendPointers() # 0/1
	
	#unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count = measure()	
	#diagram.pointers = [cycle.avnode() for cycle in grouped_cycles_by_av[0][1]]
	'''
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	'''	
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count = measure()	
	diagram.pointers = grouped_cycles_by_av[0][1][0].avnode().tuple; 
	jtm(); extendPointers() # 0/1
	
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count = measure()	
	diagram.pointers = grouped_cycles_by_av[0][1][0].avnode().tuple;
	'''
	'''
	pointTo('000001'); jmp(3); adv(3); jmp(2); extendPointers()
	pointTo('021220'); jmp(2); extendPointers()
	pointTo('021244'); jmp(3); extendPointers()
	pointTo('021253'); extendPointers()
	pointTo('021202'); jmp(2); extendPointers()
	#diagram.pointers = list(chain(*[node.loop.nodes for node in diagram.pointers]))

	pointTo('000001'); diagram.pointers = list(chain(*[node.loop.nodes for node in diagram.pointers]))
	'''
	
							
	#pointTo('013210');
	#extendMid('0132', 1)
	#pointTo('011001'); jmp(1); extendPointers()
	#pointTo('011054'); #jmp(1);
	'''
	diagram.extendLoop(H001.loop)

	markCycle('10000', 1)
	markCycle('10001', 2)
	markCycle('10010', 3)
	markCycle('10100', 4)
	markCycle('11000', 5)
			
	
	pointTo('100106'); extendPointers()
	pointTo('100114'); extendPointers()
	pointTo('100346'); extendPointers()
		
	pointTo('101006'); extendPointers()	
	pointTo('110006'); extendPointers()

	#extendBar('1000', 3) # orange
	extendBar('1000', 2) # red
	extendBar('1004', 3) # red

	extendMid('1002', 1) # yellow
	#extendMid('1002', 0) # orange
	
	pointTo('010023'); extendPointers()
	pointTo('010116'); extendPointers()
	pointTo('010346'); extendPointers()
		
	#extendBar('1210', 0) # indigo

	pointTo('101014'); extendPointers()	
	pointTo('101246'); extendPointers()	
			
	#pointTo('103012'); extendPointers()
	#pointTo('103003'); extendPointers()
	#pointTo('103124'); extendPointers()
	#pointTo('103021'); extendPointers()
	#pointTo('103133'); extendPointers()			
		
	#pointTo('100210'); extendPointers()
	#pointTo('100234'); extendPointers()
	#pointTo('100243'); extendPointers()
													
	# pointTo('100211'); extendPointers()
	# pointTo('100220'); extendPointers()
	# pointTo('100244'); extendPointers()
	# pointTo('101246'); extendPointers()
	# 
	# pointTo('101302'); extendPointers()
	# pointTo('101311'); extendPointers()
	# pointTo('101335'); extendPointers()
	# pointTo('101344'); extendPointers()
	# pointTo('101353'); extendPointers()
	# 
	# pointTo('101401'); extendPointers()
	# pointTo('101425'); extendPointers()
	# pointTo('101434'); extendPointers()
	# pointTo('101443'); extendPointers()
	# pointTo('101452'); extendPointers()
	
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count = measure()	
	show(diagram); 
	
	# [(cycle, len([node for node in cycle.nodes if node.loop.availabled]), len([node for node in cycle.nodes if node.loop.availabled and len([n for n in node.loop.nodes if n.chainID is not None]) > 0])) for cycle in [cycle for cycle in diagram.cycles if cycle.chained_by_count is 0 and len([node for node in cycle.nodes if node.loop.availabled and len([n for n in node.loop.nodes if n.chainID is not None]) > 0]) is 1]]
		
