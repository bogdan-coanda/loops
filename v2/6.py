from diagram import *
from uicanvas import *
from groupby import *


def measure():
	unlooped_cycle_count = len([c for c in diagram.cycles if c.chained_by_count is 0])
	grouped_cycles_by_av = sorted(groupby([c for c in diagram.cycles if c.chained_by_count is 0], K = lambda c: c.available_loops_count).items())
	print("unlooped cycles: " + str(unlooped_cycle_count))
	print("cycle av counts: " + str([(k, len(v)) for k,v in grouped_cycles_by_av]))			
	print("available loops: " + str(len([loop for loop in diagram.loops if loop.availabled])) + "/" + str(len(diagram.loops)))				
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
		
		
def select():
	unlooped_cycle_count, grouped_cycles_by_av = measure()
	diagram.pointers = sorted([c.avnode() for c in grouped_cycles_by_av[0][1]], key = lambda n: n.address); print("\n".join([str(n) for n in diagram.pointers]))
	print("selecting: " + str(diagram.pointers[0]))
	diagram.pointers = diagram.pointers[0].tuple
	
		
				
		
if __name__ == "__main__":
	
	diagram = Diagram(6)
	diagram.generateKernel()
	
	H001 = diagram.nodeByAddress['00001']
	H201 = diagram.nodeByAddress['00201'] 		
	K143 = diagram.nodeByAddress['00143']
	K343 = diagram.nodeByAddress['00343']
	
	bases = [H001, K143, H201, K343]
	
	#diagram.walk(bases)
	
	#node = diagram.nodeByAddress['00000']

	# ~~~ walk ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							
			
	#pointTo('10305'); extendPointers() # blue(α)
	#pointTo('10105'); extendPointers() # blue(β)
	# » 
	#pointTo('10204'); extendPointers() # green(1)
	# »» 
	#pointTo('10020'); extendPointers() # orange(3)/purple(5)
	# »»» 
	#pointTo('10233'); extendPointers() # yellow(2)/red(4)
	# »»»»
	#pointTo('10043'); extendPointers() # orange(3)/purple(5)
			
	# ~~~ ~~~~ ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							
	# [cycle] » blue(0) » green(1) » yellow(2) » orange(3) » red(4) » purple(5)
														
	# binders
	#extend('00001') # red(4)    | Bro:0 ~ I:blue(α)
	#extend('00143') # yellow(2) | Ι: @2 ~ orange(3):3
	#extend('00201') # yellow(2) | I: @4 ~ purple(5):3
	#extend('00343') # red(4)    | I: @4 ~ blue(β) | ΙI: @3 ~ blue(α)
				
	# islands
	# I.
	# extend('11005') # blue(α)
	# extend('11205') # blue(β)
	# extend('11104') # green(1)
	# » purple(5) » red(4) » orange(3)	
	# II.
	#extend('10105') # blue(β)
	#extend('10305') # blue(α)
	#extend('10204') # green(1)
	# » orange(3) » red(4) » purple(5)
	# III.
	#extend('01105') # blue(α)
	#extend('01305') # blue(β)
	#extend('01204') # green(1)
	# » orange(3) » yellow(2) » purple(5)
	# IV.
	#extend('02005') # blue(β)
	#extend('02205') # blue(α)
	#extend('02104') # green(1)
	# » purple(5) » yellow(2) » orange(3)
	
	#extend('11310') # I.   | » x | purple
	#extend('10020') # II.  | » x | orange	
	#extend('10011') # III. | » x | orange
	#extend('11333') # IV.  | » x | purple
	
	#extend('01220') # I.   | » y | red
	#extend('01211') # II.  | » y | red
	#extend('10233') # III. | » y | yellow
	#extend('10210') # IV.  | » y | yellow
	
	#extend('10043') # I.   | » z | orange
	#extend('11301') # II.  | » z | purple	
	#extend('11342') # III. | » z | purple
	#extend('10002') # IV.  | » z | orange
#	
	diagram.pointers = list(H001.loop.nodes)
	
	# ~~~ ~~~~ ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							
	'''
	unlooped_cycle_count, grouped_cycles_by_av = measure()

	#diagram.pointers = bases
													
	#diagram.reorder('123450') # purple(5)
	#diagram.reorder('345012') # orange(3)
				
	#diagram.reorder('234501') # red(4)
	#diagram.reorder('450123') # yellow(2)

	#diagram.reorder('345012') # orange(3)
	#diagram.reorder('123450') # purple(5)
			
	#diagram.reorder('501234') # green(1)			
	
	#diagram.reorder('012345') # blue(α/β)
	
	exnodes = [
		('10105', 'I:blue(β)'),
		('10305', 'I:blue(α)'),
		('10204', 'I:green(1)'),
		('11005', 'II:blue(α)'),
		('11205', 'II:blue(β)'),
		('11104', 'II:green(1)'),
		('01105', 'III:blue(α)'),
		('01305', 'III:blue(β)'),
		('01204', 'III:green(1)'),	
		('02005', 'IV:blue(β)'),
		('02205', 'IV:blue(α)'),
		('02104', 'IV:green(1)'),
		('10020', 'I»x:orange(3)'),
		('11310', 'II»x:purple(5)'),
		('10011', 'III»x:orange(3)'),
		('11333', 'IV»x:purple(5)'),
		('01211', 'I»y:red(4)'),
		('01220', 'II»y:red(4)'),
		('10233', 'III»y:yellow(2)'),
		('10210', 'IV»y:yellow(2)'),
		('11301', 'I»z:purple(5)'),
		('10043', 'II»z:orange(3)'),
		('11342', 'III»z:purple(5)'),
		('10002', 'IV»z:orange(3)')
	]
	
	bnodes = [
		(H001, 'H001'),
		(K143, 'K143'),
		(H201, 'H201'),
		(K343, 'K343')
	]
	
	for i,pair1 in enumerate(exnodes):
		for j,pair2 in enumerate(exnodes):
			if j > i:
				if len(set([n.cycle for n in diagram.nodeByAddress[pair1[0]].loop.nodes]).intersection(set([n.cycle for n in diagram.nodeByAddress[pair2[0]].loop.nodes]))) > 0:
					print(pair1[1] + " ~ " + pair2[1])
					
	for ii,pairb in enumerate(bnodes):
		for ib,bro in (enumerate(pairb[0].loopBrethren) if ii % 2 is 0 else enumerate(reversed(pairb[0].loopBrethren))):
			for pairex in exnodes:
				if len(set([n.cycle for n in diagram.nodeByAddress[pairex[0]].loop.nodes]).intersection([bro.cycle])) > 0:
					print(pairb[1] + ":" + str(ib) + " ~ " + pairex[1])
				 
	#diagram.pointers = list(bases)
	#jmp(0); adv(3); extendPointers()
	
	#extend(H001.address);
	#jmp(0); adv(3); extendPointers() # Η001:0 ⇒ I:blue(α)
	#pointTo('11005'); extendPointers() # I:blue(α)

	# ~~~ grouped by trees ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''							
					
	# I.
	#extend('11005') # I:α (blue)     | H001[0]
	#extend('11205') # I:β (blue)     | K343[1]
	#extend('11104') # I:1 (green)		
	#extend('11310') # I:2 (purple)   | H201[2]
	#extend('01220') # I:3 (red)
	#extend('10043') # I:4 (orange)   | K143[3]

	# II.
	#extend('10305') # II:α (blue)    | K343[0]
	#extend('10105') # II:β (blue)    | H001[1]
	#extend('10204') # II:1 (green)
	#extend('10020') # II:2 (orange)  | K143[2]
	#extend('01211') # II:3 (red)
	#extend('11301') # II:4 (purple)  | H201[3]

	# III.
	#extend('01105') # III:α (blue)   | H201[0]
	#extend('01305') # III:β (blue)   | H143[1]
	#extend('01204') # III:1 (green)
	#extend('10011') # III:2 (orange) | H001[2]
	#extend('10233') # III:3 (yellow)
	#extend('11342') # III:4 (purple) | H343[3]
					
	# IV.
	#extend('02205') # IV:α (blue)    | H143[0]	
	#extend('02005') # IV:β (blue)    | H201[1]
	#extend('02104') # IV:1 (green)
	#extend('11333') # IV:2 (purple)  | H343[2]
	#extend('10210') # IV:3 (yellow)
	#extend('10002') # IV:4 (orange)  | H001[3]
																				
	# binders																																																
	#extend('00001') # red    | [0] » I:α (blue)   | [1] » II:β (blue)  | [2] » III:2 (orange) | [3] » IV:4 (orange)
	#extend('00143') # yellow | [0] » IV:α (blue)  | [1] » III:β (blue) | [2] » II:2 (orange)  | [3] » I:4 (orange)
	#extend('00201') # yellow | [0] » III:α (blue) | [1] » IV:β (blue)  | [2] » I:2 (purple)   | [3] » II:4 (purple)
	#extend('00343') # red    | [0] » II:α (blue)  | [1] » I:β (blue)   | [2] » IV:2 (purple)  | [3] » III:4 (purple)
					
	# ~~~ grouped by H001[x] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''																		

	# extend('00001') # red    | [0] » I:α (blue)   | [1] » II:β (blue)  | [2] » III:2 (orange) | [3] » IV:4 (orange)
	
	# lvl 1
	# extend('11005') # I:α (blue)     | H001[0]	
	# extend('10105') # II:β (blue)    | H001[1]
	# extend('10011') # III:2 (orange) | H001[2]
	# extend('10002') # IV:4 (orange)  | H001[3]
			
	# assert len(set([node.chainID for node in diagram.nodes if node.chainID is not None])) is 1
	
	# lvl 2
	# extend('11104') # I:1 (green)		
	# extend('10204') # II:1 (green)
	# extend('01204') # III:1 (green)			
	# extend('10233') # III:3 (yellow)			
	# extend('10210') # IV:3 (yellow)																																																															
	
	# assert len(set([node.chainID for node in diagram.nodes if node.chainID is not None])) is 1
	
	# lvl 3
	# extend('11205') # I:β (blue)     | K343[1]
	# extend('11310') # I:2 (purple)   | H201[2]
	# extend('10305') # II:α (blue)    | K343[0]
	# extend('10020') # II:2 (orange)  | K143[2]	
	# extend('01105') # III:α (blue)   | H201[0]
	# extend('01305') # III:β (blue)   | H143[1]
	# extend('11342') # III:4 (purple) | H343[3]
	# extend('11333') # IV:2 (purple)  | H343[2]
	
	# assert len(set([node.chainID for node in diagram.nodes if node.chainID is not None])) is 1	
	
	# lvl 4
	# extend('01220') # I:3 (red)
	# extend('01211') # II:3 (red)	
	# extend('02104') # IV:1 (green)
	
	# assert len(set([node.chainID for node in diagram.nodes if node.chainID is not None])) is 1	
	
	# lvl 5		
	# extend('10043') # I:4 (orange)   | K143[3]
	# extend('11301') # II:4 (purple)  | H201[3]
	# extend('02205') # IV:α (blue)    | H143[0]	
	# extend('02005') # IV:β (blue)    | H201[1]
	
	# assert len(set([node.chainID for node in diagram.nodes if node.chainID is not None])) is 1	
		
	# ~~~ grouped by K143[x] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''																		
	
	# extend('00143') # yellow | [0] » IV:α (blue)  | [1] » III:β (blue) | [2] » II:2 (orange)  | [3] » I:4 (orange)
	'''
	# lvl 1
	extend('02205') # IV:α (blue)    | H143[0]
	extend('01305') # III:β (blue)   | H143[1]
	extend('10020') # II:2 (orange)  | K143[2]
	extend('10043') # I:4 (orange)   | K143[3]

	assert len(set([node.chainID for node in diagram.nodes if node.chainID is not None])) is 1
	
	# lvl 2
	extend('02104') # IV:1 (green)
	extend('01204') # III:1 (green)					
	extend('10204') # II:1 (green)
	extend('01211') # II:3 (red)	
	extend('01220') # I:3 (red)
		
	assert len(set([node.chainID for node in diagram.nodes if node.chainID is not None])) is 1
	
	# lvl 3
	extend('02005') # IV:β (blue)    | H201[1]
	extend('11333') # IV:2 (purple)  | H343[2]
	extend('01105') # III:α (blue)   | H201[0]
	extend('10011') # III:2 (orange) | H001[2]
	extend('10305') # II:α (blue)    | K343[0]
	extend('10105') # II:β (blue)    | H001[1]		
	extend('11301') # II:4 (purple)  | H201[3]		
	extend('11310') # I:2 (purple)   | H201[2]
			
	assert len(set([node.chainID for node in diagram.nodes if node.chainID is not None])) is 1	
	
	# lvl 4										
	extend('10210') # IV:3 (yellow)
	extend('10233') # III:3 (yellow)			
	extend('11104') # I:1 (green)		
				
	assert len(set([node.chainID for node in diagram.nodes if node.chainID is not None])) is 1	
	
	# lvl 5		
	extend('10002') # IV:4 (orange)  | H001[3]
	extend('11342') # III:4 (purple) | H343[3]
	extend('11005') # I:α (blue)     | H001[0]	
	extend('11205') # I:β (blue)     | K343[1]
				
	assert len(set([node.chainID for node in diagram.nodes if node.chainID is not None])) is 1	
				
	# ~~~ ~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''																		
	'''
	diagram.pointers = list(bases)
	adv(4); jmp(0); adv(2);
	bases = list(diagram.pointers)
	
	select(); extendPointers() # 0/4
	select(); adv(5); extendPointers() # 2/3
	select(); adv(1); #extendPointers() # 1/3
	select(); adv(0); extendPointers() # 0/3
	select(); adv(5); extendPointers() # 1/2
	select(); adv(0); extendPointers() # 0/2
	
	# sols:
	# bind:00001 | 0/4 0/3 3/4 1/2 1/3 0/2
	
	
	#extend(diagram.pointers[0].address)
	
	#diagram.pointers = list(bases); jmp(0); adv(3); extendPointers() # 1/3
	#diagram.pointers = list(bases); jmp(1); adv(2); extendPointers() # 0/2
	#diagram.pointers = list(bases); jmp(2); adv(3); #extendPointers() # 0/2
	#diagram.pointers = list(bases); jmp(3); adv(2); #extendPointers()
	
	#pointTo('11111'); extendPointers()
	#pointTo('11031'); extendPointers()
	#pointTo('12032'); extendPointers()
	#pointTo('01124'); #extendPointers()
	
	

	# ~~~ ~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''																				

	unlooped_cycle_count, grouped_cycles_by_av = measure()	
	show(diagram)
