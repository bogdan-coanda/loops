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
	
	diagram.point()
	show(diagram)
