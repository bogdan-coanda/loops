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
	#print("unlooped cycles: " + str(unlooped_cycle_count))
	#print("cycle av counts: " + str([(k, len(v)) for k,v in grouped_cycles_by_av]))			
	#print("available loops: " + str(available_loops_count) + "/" + str(len(diagram.loops)))				
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
		
	skipped = 0
		
	def backbytuple(lvl = 0, road = []):
		global  skipped
		if len(road) > lvl:
			tuple = diagram.nodeByAddress[road[lvl]].tuple
			for tuplenode in tuple:
				diagram.extendLoop(tuplenode.loop)
			for n in tuple:
				if len([bro for bro in n.loopBrethren if bro.cycle.marker is not None]) is 0:
					for bro in n.loopBrethren:
						bro.cycle.marker = n.cycle.marker				
			backbytuple(lvl+1, road)				
			for i in range(len(tuple))[::-1]:
				assert diagram.collapseLoop(tuple[i].loop)		
	
		road = road[:lvl]			
			
		print("[lvl:"+str(lvl)+"] road: " + " ".join([str(pair[0])+"/"+str(pair[1]) if len(pair) is 3 else "["+str(index)+"]" for index,pair in enumerate(road)]))
		print("[lvl:"+str(lvl)+"] addr: " + " ".join([pair[2].address if len(pair) is 3 else pair for pair in road]))
		
		unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count = measure()		
	
		if available_loops_count is 0:
			if unlooped_cycle_count is 0 and chains_count is 1:
				show(diagram)
				print("[lvl:"+str(lvl)+"] FOUND | road: " + " ".join([str(pair[0])+"/"+str(pair[1]) if len(pair) is 2 else pair for pair in road]))
				print("[lvl:"+str(lvl)+"] FOUND:\n" + "\n".join([str(pair[2]) for pair in road]))
				input("~~~~~~~~~~~~~~~~~~")
				return
			else:
				#show(diagram)
				#input("No avloops")
				return
	
		if lvl is 27 or unlooped_cycle_count is 0:
			if len([loop for loop in diagram.loops if loop.availabled and loop.hasKernelNodes()]) > 0:
				diagram.pointers = [loop.psnode() for loop in diagram.loops if loop.availabled]			
				show(diagram)
				input("Intermediate")
				#backbyloop(lvl, road)			
				return
			else:
				print("[skipping:"+str(skipped)+"]")
				if skipped % 10 is 0:
					input("...")
				skipped += 1
				return 
							
		cycle = sorted(grouped_cycles_by_av[0][1], key = lambda c: c.address)[0]
		#print("[lvl:"+str(lvl)+"] selecting: " + str(cycle))
		
		lvl_seen = []
		
		avnodes = sorted([n for n in cycle.nodes if n.loop.availabled], key = lambda n: n.address)
		for nodeindex, node in enumerate(avnodes):
			
			tuple = list(node.tuple)		

			#diagram.pointers = tuple		
			#show(diagram)
			#print("[lvl:"+str(lvl)+"] road: " + " ".join([str(pair[0])+"/"+str(pair[1]) for pair in road]))
			#input("[lvl:"+str(lvl)+"] extending: " + str(node) + " " + str(nodeindex) + "/" + str(len(avnodes)))
			
			excc = 0
			for tupleindex, tuplenode in enumerate(tuple):
				if diagram.extendLoop(tuplenode.loop):
					excc += 1
				else:
					break
										
			if excc is len(tuple):
				for n in tuple:
					if len([bro for bro in n.loopBrethren if bro.cycle.marker is not None]) is 0:
						for bro in n.loopBrethren:
							bro.cycle.marker = n.cycle.marker
				backbytuple(lvl+1, road+[(nodeindex, len(avnodes), node)])

			for i in range(excc-1, -1, -1):
				assert diagram.collapseLoop(tuple[i].loop)

			# diagram.pointers = list(tuplenode.tuple)		
			# show(diagram)
			# input("[lvl:"+str(lvl)+"] collapsing: " + str(node) + " " + str(nodeindex) + "/" + str(len(avnodes)))
			
			if excc is len(tuple):
				for tuplenode in tuple:
					lvl_seen.append(tuplenode.loop)
					diagram.setLoopUnavailabled(tuplenode.loop)
									
		for loop in lvl_seen:
			diagram.setLoopAvailabled(loop)
			
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
		
	markCycle('12300', 3)
	markCycle('12310', 4)
	markCycle('12320', 5)
	markCycle('12330', 1)
	markCycle('12340', 2)
			
	#unwant()
	
	backbytuple(0, [
		'123005',
		'123011',
		'122214',
		'122314',
		'122321',
		'122402',
		'121204',
		'112005',
		'113313',	
	
		'120410',
		'001005',
		'001113',		
		'001020',
		'010414',
		'010000',
		'011006',
		'003030',
		'002005',
		
		'113020',
		'122023',
		'120131',
		'100040',
		'100454',
		'122144',
		'122054'
	])
	
	'''
	pointTo('123005'); jtm(); extendPointers();
	pointTo('123011'); jtm(); extendPointers();
	pointTo('122214'); jtm(); extendPointers();
	pointTo('122314'); jtm(); extendPointers();
	pointTo('122321'); jtm(); extendPointers();	
	pointTo('122402'); jtm(); extendPointers();	
	pointTo('121204'); jtm(); extendPointers();
	pointTo('112005'); jtm(); extendPointers();
	pointTo('113313'); jtm(); extendPointers();

	pointTo('120410'); jtm(); extendPointers();
	pointTo('001005'); jtm(); extendPointers();
	pointTo('001113'); jtm(); extendPointers();
	pointTo('001020'); jtm(); extendPointers();
	pointTo('010414'); jtm(); extendPointers();
	pointTo('010000'); jtm(); extendPointers();
	pointTo('011006'); jtm(); extendPointers();
	pointTo('003030'); jtm(); extendPointers();
	pointTo('002005'); jtm(); extendPointers();
	
	pointTo('113020'); jtm(); extendPointers();
	pointTo('122023'); jtm(); extendPointers();
	pointTo('120131'); jtm(); extendPointers();
	pointTo('100040'); jtm(); extendPointers();
	pointTo('100454'); jtm(); extendPointers();
	pointTo('122144'); jtm(); extendPointers();
	pointTo('122054'); jtm(); extendPointers();
	
	#loop = diagram.nodeByAddress['000101'].loop
	#diagram.extendLoop(loop, False)
	#diagram.pointers = loop.nodes
	
	#pointTo('122001'); jtm(); extendPointers();
	#pointTo('100332'); jtm(); extendPointers();
	
	# ~~~ ~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count = measure()	
	#diagram.pointers += [cycle.avnode() for cycle in grouped_cycles_by_av[0][1]]
	diagram.pointers = [loop.psnode() for loop in diagram.loops if loop.availabled]
	show(diagram); 
	
	# [(cycle, len([node for node in cycle.nodes if node.loop.availabled]), len([node for node in cycle.nodes if node.loop.availabled and len([n for n in node.loop.nodes if n.chainID is not None]) > 0])) for cycle in [cycle for cycle in diagram.cycles if cycle.chained_by_count is 0 and len([node for node in cycle.nodes if node.loop.availabled and len([n for n in node.loop.nodes if n.chainID is not None]) > 0]) is 1]]
		
