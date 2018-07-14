from diagram import *
from uicanvas import *
from groupby import *


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
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count = measure()
	diagram.pointers = sorted([c.avnode() for c in grouped_cycles_by_av[0][1]], key = lambda n: n.address); print("\n".join([str(n) for n in diagram.pointers]))
	print("selecting: " + str(diagram.pointers[0]))
	diagram.pointers = diagram.pointers[0].tuple
	
		
				
		
if __name__ == "__main__":
	
	diagram = Diagram(6)
	
	H001 = diagram.nodeByAddress['00001']
	H201 = diagram.nodeByAddress['00201'] 		
	K143 = diagram.nodeByAddress['00143']
	K343 = diagram.nodeByAddress['00343']
	
	bases = [H001, K143, H201, K343]
	
	diagram.walk(bases)

	diagram.pointers = list(bases)
	#show(diagram)
	#input()
	diagram.generateKernel()
											
	# ~~~ ~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''																		

	adv(4); jmp(0); adv(2);
	bases = list(diagram.pointers)
	
	def backbyloop(lvl, road):
		#print("[lvl:"+str(lvl)+"] road: " + " ".join([str(pair[0])+"/"+str(pair[1]) for pair in road]))

		unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count = measure()		
						
		if available_loops_count is 0:
			if unlooped_cycle_count is 0 and chains_count is 1:
				show(diagram)
				print("\t# [lvl:"+str(lvl)+"] FOUND | road: " + " ".join([str(pair[0])+"/"+str(pair[1]) for pair in road]))
				print("\n"+"\n".join(["\t# pointTo('"+pair[2].address+"'); extendPointers()" if isinstance(pair[2], Node) else "\n\t# ⟨"+pair[2].psnode().address+"⟩" for pair in road]))
				input("~~~~~~~~~~~~~~~~~~")
				return
			else:
				return
		
		lvl_seen = []
		
		avloops = [loop for loop in diagram.loops if loop.availabled and not loop.seen]
		for loopindex, loop in enumerate(avloops):
			
			#if (chains_count < 9):
				#diagram.pointers = [loop.psnode()]
				#show(diagram)
				#input("[lvl:"+str(lvl)+"] extending: " + str(loop) + " " + str(loopindex) + "/" + str(len(avloops)))
			
			if diagram.extendLoop(loop):
				backbyloop(lvl+1, road+[(loopindex, len(avloops), loop)])
				
				diagram.collapseLoop(loop)
		
				#diagram.pointers = [loop.psnode()]		
				#show(diagram)
				#input("[lvl:"+str(lvl)+"] collapsing: " + str(loop) + " " + str(loopindex) + "/" + str(len(avloops)))
			
				lvl_seen.append(loop)
				diagram.setLoopUnavailabled(loop)
			
		for loop in lvl_seen:
			diagram.setLoopAvailabled(loop)
			
			
	def backbytuple(lvl = 0, road = []):
		#print("[lvl:"+str(lvl)+"] road: " + " ".join([str(pair[0])+"/"+str(pair[1]) for pair in road]))
		
		unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count = measure()		
	
		if available_loops_count is 0:
			if unlooped_cycle_count is 0 and chains_count is 1:
				show(diagram)
				print("[lvl:"+str(lvl)+"] FOUND | road: " + " ".join([str(pair[0])+"/"+str(pair[1]) for pair in road]))
				print("[lvl:"+str(lvl)+"] FOUND:\n" + "\n".join([str(pair[2]) for pair in road]))
				input("~~~~~~~~~~~~~~~~~~")
				return
			else:
				return
	
		if lvl is 6 or unlooped_cycle_count is 0:
			#show(diagram)
			#input("Intermediate")
			backbyloop(lvl, road)			
			return
							
		cycle = sorted(grouped_cycles_by_av[0][1], key = lambda c: c.address)[0]
		#print("[lvl:"+str(lvl)+"] selecting: " + str(cycle))
		
		lvl_seen = []
		
		avnodes = sorted([n for n in cycle.nodes if n.loop.availabled], key = lambda n: n.address)
		for nodeindex, node in enumerate(avnodes):
			
			tuple = list(node.tuple)		

			# diagram.pointers = tuple		
			# show(diagram)
			# input("[lvl:"+str(lvl)+"] extending: " + str(node) + " " + str(nodeindex) + "/" + str(len(avnodes)))
			
			excc = 0
			for tupleindex, tuplenode in enumerate(tuple):
				if diagram.extendLoop(tuplenode.loop):
					excc += 1
				else:
					break
										
			if excc is len(tuple):
				backbytuple(lvl+1, road+[(nodeindex, len(avnodes), node)])

			for i in range(excc-1, -1, -1):
				assert diagram.collapseLoop(tuple[i].loop)

			# diagram.pointers = list(tuplenode.tuple)		
			# show(diagram)
			# input("[lvl:"+str(lvl)+"] collapsing: " + str(node) + " " + str(nodeindex) + "/" + str(len(avnodes)))
			
			# if excc is len(tuple):
			# 	for tuplenode in tuple:
			# 		lvl_seen.append(tuplenode.loop)
			# 		diagram.setLoopUnavailabled(tuplenode.loop)
									
		for loop in lvl_seen:
			diagram.setLoopAvailabled(loop)
						
	# [~] backbytuple()
									
	# ~~~ Sol.⟨A⟩ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''																				

	# [lvl:7] FOUND | road: 0/4 0/3 3/4 0/3 1/2 0/1 0/4

	#pointTo('01105'); extendPointers() # α (blue)
	#pointTo('01345'); extendPointers() # β (blue)
	#pointTo('01022'); extendPointers() # 1 (green)
	#pointTo('01010'); extendPointers() # 2 (orange/violet)
	#pointTo('01220'); extendPointers() # 3 (red~yellow)
	#pointTo('01001'); extendPointers() # 4 violet/orange

	# ⟨00001⟩

	pointTo('00001'); jmp(0); adv(3); #extendPointers() # α (blue)
	jmp(0); adv(4); #extendPointers() # 1 (green)
	jmp(3); adv(2); #extendPointers() # 2 (orange/violet)
	jmp(3); adv(4); #extendPointers() # 3 (red~yellow)
	jmp(0); adv(4); #extendPointers() # 4 violet/orange
	pointTo('00001'); jmp(1); adv(2); #extendPointers() # β (blue)
	jmp(0); adv(4); #extendPointers() # 1 (green)
	jmp(3); adv(4); #extendPointers() # 2 (orange/violet)
	jmp(0); adv(2); #extendPointers() # 3 (red~yellow)
	jmp(3); adv(2); #extendPointers() # 4 violet/orange
	pointTo('00001'); jmp(3); adv(2); extendPointers() # 4 violet/orange
	jmp(1); adv(4); extendPointers() # 3 (red~yellow)
	jmp(0); adv(4); extendPointers() # 2 (orange/violet)
	jmp(3); adv(2); extendPointers() # 1 (green)
	jmp(0); adv(2); extendPointers() # β (blue)
	adv(4); jmp(3); # backtrack to green extension point
	jmp(3); adv(4); extendPointers() # α (blue)
	
	# ~~~ Sol.⟨B⟩ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''	
		
	# [lvl:7] FOUND | road: 1/4 1/4 3/4 0/3 0/3 1/2 0/4
	
	# pointTo('01340'); extendPointers() # green
	# pointTo('10340'); extendPointers() # green
	# pointTo('11345'); extendPointers() # blue	
	# pointTo('01023'); extendPointers() # red/yellow
	# pointTo('11121'); extendPointers() # violet~orange
	# pointTo('11143'); extendPointers() # yellow/red

	# ⟨00002⟩
				
	# ~~~ Sol.⟨C⟩ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''	
	
	# [lvl:7] FOUND | road: 1/4 3/4 1/4 0/3 1/2 0/2 0/4

	# pointTo('11331'); extendPointers() # green
	# pointTo('10122'); extendPointers() # green
	# pointTo('11125'); extendPointers() # blue	
	# pointTo('01132'); extendPointers() # orange/violet	
	# pointTo('01023'); extendPointers() # yellow~red
	# pointTo('11342'); extendPointers() # violet/orange

	# ⟨00042⟩
		
	# ~~~ Sol.⟨D⟩ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''	

	# [lvl:7] FOUND | road: 2/4 1/5 3/4 3/4 0/3 0/2 0/4

	# pointTo('01115'); extendPointers() # blue
	# pointTo('01335'); extendPointers() # blue
	# pointTo('01131'); extendPointers() # green	
	# pointTo('11111'); extendPointers() # yellow/red	
	# pointTo('01024'); extendPointers() # orange~violet
	# pointTo('10242'); extendPointers() # red/yellow

	# ⟨00043⟩
		
	# ~~~ ~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #	'''	
						
	'''
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

	#diagram.reorder('123450')

	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, chains_count = measure()	
	show(diagram)
