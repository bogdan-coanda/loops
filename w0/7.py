from diagram import *
from uicanvas import *


def purge():

	next_sample_lengths_per_loop_tuple = {}
	unavailed = []
	unsuccess = 0
	
	for it, tuple in enumerate(diagram.loop_tuples):
		if tuple[0].availabled: # [!] need only full tuples here (need ot() to have run previously)
			
			# try extend tuple
			ec = 0
			for loop in tuple:
				if not diagram.extendLoop(loop):
					break
				else:
					ec += 1
			
			# note successfulness
			if ec != len(tuple):
				next_sample_lengths_per_loop_tuple[tuple] = -1
			else:
				next_sample_lengths_per_loop_tuple[tuple] = len(diagram.point())	
							
			# collapse back
			for loop in reversed(tuple[:ec]):
				diagram.collapseBack(loop)

			# purge if unsuccessful
			if next_sample_lengths_per_loop_tuple[tuple] <= 0:
				unsuccess += 1
				for loop in tuple:
					if loop.availabled:
						diagram.setLoopUnavailabled(loop)
						unavailed.append(loop)
						if len([node for node in loop.nodes if len(node.chain.avnodes) == 0]) > 0:
							return (False, unavailed, next_sample_lengths_per_loop_tuple)
						
	print(f"[purge] ⇒ unavailabled {len(unavailed)} loops in {unsuccess} failed tuples | tuples per sample length: {sorted(groupby(next_sample_lengths_per_loop_tuple.items(), K = lambda p: p[1], G = lambda g: len(g)).items())}")
	return (True, unavailed, next_sample_lengths_per_loop_tuple)


def choose(next_sample_lengths_per_loop_tuple):
	# ot()
	# reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()

	# ~ choose next ~ #	
	next_sample_length_ratios_per_chain = {}
	for chain in diagram.chains:		
		next_sample_length_ratios_per_chain[chain] = sum([next_sample_lengths_per_loop_tuple[node.loop.tuple] for node in chain.avnodes]) / len(chain.avnodes) # [!] need no empty chains here			

	singles = [chain for chain in diagram.chains if len(chain.avnodes) == 1]
	if len(singles):
		print(f"[choose] singles: {len(singles)}")
		min_ratio = min([r for c,r in next_sample_length_ratios_per_chain.items() if c in singles])
		min_chain = sorted([c for c,r in next_sample_length_ratios_per_chain.items() if r == min_ratio and c in singles], key = lambda c: c.avnodes[0].address)[0]		
		min_nodes = min_chain.avnodes
	else:
		min_ratio = min([r for c,r in next_sample_length_ratios_per_chain.items()])
		min_chain = sorted([c for c,r in next_sample_length_ratios_per_chain.items() if r == min_ratio], key = lambda c: (len(c.avnodes), c.id))[0]
		min_nodes = sorted(min_chain.avnodes, key = lambda n: (next_sample_lengths_per_loop_tuple[n.loop.tuple], n.address))
		
	print(f"[choose] min_ratio: {min_ratio} | min_chain: {min_chain} | min_nodes:\n{NEWLINE.join([str((next_sample_lengths_per_loop_tuple[n.loop.tuple], n.address)) for n in min_nodes])}")
	return min_nodes



if __name__ == "__main__":
	
	diagram = Diagram(7, 1)
	
	import enav
	enav.diagram = diagram
	from enav import *
	
	extend('000001');
	
	ot()			
	reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()
	min_nodes = choose(next_sample_lengths_per_loop_tuple)
	
	# [ot] ⇒ unavailabled 28 loops in 7 incomplete tuples | remaining tuples: 151
	# [purge] ⇒ unavailabled 30 loops in 6 failed tuples | tuples per sample length: [(-1, 6), (1, 8), (2, 127), (3, 10)]
	# [choose] min_ratio: 1.6666666666666667 | min_chain: ⟨chain:74|av:6⟩ | min_nodes:
	# (1, '002223')
	# (1, '002224')
	# (2, '002221')
	# (2, '002222')
	# (2, '002225')
	# (2, '002226')
	et('002223') # 0/6
	
	singles = sorted([chain for chain in diagram.chains if len(chain.avnodes) == 1], key = lambda chain: chain.avnodes[0].address)
	if len(singles):
		min_nodes = singles[0].avnodes
		print(f"singles: {min_nodes}")
		
	# singles: [⟨node:6412305@001406§⟨chain:54|av:1⟩|Av⟩]
	et('001406') # 0/1

	singles = sorted([chain for chain in diagram.chains if len(chain.avnodes) == 1], key = lambda chain: chain.avnodes[0].address)
	if len(singles):
		min_nodes = singles[0].avnodes
		print(f"singles: {min_nodes}")
	else:
		ot()			
		reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()
		min_nodes = choose(next_sample_lengths_per_loop_tuple)								
		
	# [ot] ⇒ unavailabled 24 loops in 6 incomplete tuples | remaining tuples: 128
	# [purge] ⇒ unavailabled 0 loops in 0 failed tuples | tuples per sample length: [(1, 4), (2, 42), (3, 82)]
	# [choose] min_ratio: 2.0 | min_chain: ⟨chain:61|av:6⟩ | min_nodes:
	# (1, '002013')
	# (1, '002016')
	# (2, '002011')
	# (2, '002014')
	# (3, '002010')
	# (3, '002012')		
	et('002016') # 1/6

	singles = sorted([chain for chain in diagram.chains if len(chain.avnodes) == 1], key = lambda chain: chain.avnodes[0].address)
	if len(singles):
		min_nodes = singles[0].avnodes
		print(f"singles: {min_nodes}")
	else:
		ot()			
		reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()
		min_nodes = choose(next_sample_lengths_per_loop_tuple)								
	
	# singles: [⟨node:2301546@002410§⟨chain:85|av:1⟩|Av⟩]
	et('002410') # 0/1

	singles = sorted([chain for chain in diagram.chains if len(chain.avnodes) == 1], key = lambda chain: chain.avnodes[0].address)
	if len(singles):
		min_nodes = singles[0].avnodes
		print(f"singles: {min_nodes}")
	else:
		ot()			
		reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()
		min_nodes = choose(next_sample_lengths_per_loop_tuple)

	# [ot] ⇒ unavailabled 4 loops in 1 incomplete tuples | remaining tuples: 119
	# [purge] ⇒ unavailabled 15 loops in 3 failed tuples | tuples per sample length: [(-1, 2), (0, 1), (1, 11), (2, 103), (3, 2)]
	# [choose] min_ratio: 1.5 | min_chain: ⟨chain:78|av:4⟩ | min_nodes:
	# (1, '002304')
	# (1, '002305')
	# (2, '002302')
	# (2, '002306')
	et('002304') # 0/4

	singles = sorted([chain for chain in diagram.chains if len(chain.avnodes) == 1], key = lambda chain: chain.avnodes[0].address)
	if len(singles):
		min_nodes = singles[0].avnodes
		print(f"singles: {min_nodes}")
	else:
		ot()			
		reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()
		min_nodes = choose(next_sample_lengths_per_loop_tuple)
		
	# singles: [⟨node:2356041@001303§⟨chain:48|av:1⟩|Av⟩]		
	et('001303') # 0/1
	
	singles = sorted([chain for chain in diagram.chains if len(chain.avnodes) == 1], key = lambda chain: chain.avnodes[0].address)
	if len(singles):
		min_nodes = singles[0].avnodes
		print(f"singles: {min_nodes}")
	else:
		ot()			
		reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()
		min_nodes = choose(next_sample_lengths_per_loop_tuple)	

	# [ot] ⇒ unavailabled 8 loops in 2 incomplete tuples | remaining tuples: 105
	# [purge] ⇒ unavailabled 55 loops in 11 failed tuples | tuples per sample length: [(-1, 5), (0, 6), (1, 89), (2, 5)]
	# [choose] singles: 9
	# [choose] min_ratio: 2.0 | min_chain: ⟨chain:66|av:1⟩ | min_nodes:
	# (2, '002106')	
	et('002106') # 0/1

	singles = sorted([chain for chain in diagram.chains if len(chain.avnodes) == 1], key = lambda chain: chain.avnodes[0].address)
	if len(singles):
		min_nodes = singles[0].avnodes
		print(f"singles: {min_nodes}")
	else:
		ot()			
		reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()
		min_nodes = choose(next_sample_lengths_per_loop_tuple)	
		
	# [ot] ⇒ unavailabled 12 loops in 3 incomplete tuples | remaining tuples: 90
	# [purge] ⇒ unavailabled 25 loops in 5 failed tuples | tuples per sample length: [(-1, 2), (0, 3), (1, 20), (2, 65)]
	# [choose] min_ratio: 1.25 | min_chain: ⟨chain:81|av:4⟩ | min_nodes:
	# (1, '002330')
	# (1, '002331')
	# (1, '002333')
	# (2, '002335')
	et('002335') # 3/4

	singles = sorted([chain for chain in diagram.chains if len(chain.avnodes) == 1], key = lambda chain: chain.avnodes[0].address)
	if len(singles):
		min_nodes = singles[0].avnodes
		print(f"singles: {min_nodes}")
	else:
		ot()			
		reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()
		min_nodes = choose(next_sample_lengths_per_loop_tuple)	
		
	# singles: [⟨node:4026531@101253§⟨chain:407|av:1⟩|Av⟩]
	# et('101253') # 0/1
	# 
	# singles = sorted([chain for chain in diagram.chains if len(chain.avnodes) == 1], key = lambda chain: chain.avnodes[0].address)
	# if len(singles):
	# 	min_nodes = singles[0].avnodes
	# 	print(f"singles: {min_nodes}")
	# else:
	# 	ot()			
	# 	reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()
	# 	min_nodes = choose(next_sample_lengths_per_loop_tuple)	

	# [ot] ⇒ unavailabled 8 loops in 2 incomplete tuples | remaining tuples: 77
	# [purge] ⇒ unavailabled 60 loops in 12 failed tuples | tuples per sample length: [(-1, 3), (0, 9), (1, 64), (2, 1)]
	# [choose] singles: 24
	# [choose] min_ratio: 1.0 | min_chain: ⟨chain:53|av:1⟩ | min_nodes:
	# (1, '001353')
	# et('001353') # 0/1
	# 
	# singles = sorted([chain for chain in diagram.chains if len(chain.avnodes) == 1], key = lambda chain: chain.avnodes[0].address)
	# if len(singles):
	# 	min_nodes = singles[0].avnodes
	# 	print(f"singles: {min_nodes}")
	# else:
	# 	ot()			
	# 	reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()
	# 	min_nodes = choose(next_sample_lengths_per_loop_tuple)
		
	# singles: [⟨node:6304125@001206§⟨chain:42|av:1⟩|Av⟩]		
	# et('001206') # 0/1
	# 
	# singles = sorted([chain for chain in diagram.chains if len(chain.avnodes) == 1], key = lambda chain: chain.avnodes[0].address)
	# if len(singles):
	# 	min_nodes = singles[0].avnodes
	# 	print(f"singles: {min_nodes}")
	# else:
	# 	ot()			
	# 	reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()
	# 	min_nodes = choose(next_sample_lengths_per_loop_tuple)
		
	# singles: [⟨node:3051462@002321§⟨chain:80|av:1⟩|Av⟩]
	# et('002321') # 0/1
	# 
	# singles = sorted([chain for chain in diagram.chains if len(chain.avnodes) == 1], key = lambda chain: chain.avnodes[0].address)
	# if len(singles):
	# 	min_nodes = singles[0].avnodes
	# 	print(f"singles: {min_nodes}")
	# else:
	# 	ot()			
	# 	reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()
	# 	min_nodes = choose(next_sample_lengths_per_loop_tuple)
								
	# singles: [⟨node:6031452@011016§⟨chain:151|av:1⟩|Av⟩]										
	# et('011016') # 0/1
	# 
	# singles = sorted([chain for chain in diagram.chains if len(chain.avnodes) == 1], key = lambda chain: chain.avnodes[0].address)
	# if len(singles):
	# 	min_nodes = singles[0].avnodes
	# 	print(f"singles: {min_nodes}")
	# else:
	# 	ot()			
	# 	reachable, purged_loops, next_sample_lengths_per_loop_tuple = purge()
	# 	min_nodes = choose(next_sample_lengths_per_loop_tuple)
		
		
		
		
		
		
		
	diagram.point()
	show(diagram)
