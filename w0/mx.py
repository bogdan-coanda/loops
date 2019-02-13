from collections import defaultdict
from common import groupby

class MX (object):
	
	__slots__ = ['diagram']

	# 0. tie to diagram		
	def __init__(self, diagram):
		self.diagram = diagram
		
	# 1. find minimum chain avloops length		
	def min_chain_avloops_length(self):
		return min([len(chain.avnodes) for chain in self.diagram.chains])		

	# 2. find cycles not chained to any other				
	def filter_unicycle_chains(self, prev_unicycle_chains=None): # [!] chains can't be re-filtered as extended ones are still 'alive' 
		return [chain for chain in self.diagram.chains if len(chain.cycles) is 1]
		
	# 3. find available tuples (incl. already extended loops, excl. kernel connected loops)		
	def filter_avtuples(self, prev_avtuples=None):
		if prev_avtuples == None:
			return [t for t in self.diagram.loop_tuples
				if len([loop for loop in t if not loop.availabled and not loop.extended]) == 0
				and len([loop for loop in t if len([node.cycle for node in loop.nodes if node.cycle.isKernel]) != 0]) == 0]	
		else:
			return [t for t in prev_avtuples
				if len([loop for loop in t if not loop.availabled and not loop.extended]) == 0]
							
	# 4. further filter tuples by actually trying to extend each of them
	def purge(self, avtuples, unicycle_chains):

		surviving_tuples = []
		next_sample_lengths = {} # per each surviving tuple
		next_single_choices = {} # per some of the surviving tuples, if any
		
		for it, tuple in enumerate(avtuples):		
			# print(f"[purge] testing: {[l.label() for l in sorted(tuple, key = lambda loop: (loop.ktype_radialIndex, loop.ktype))]}")
			#if it % 10 == 0: print(f"[purge] @ {it}/{len(avtuples)}")
			
			# try extend tuple
			ec = 0
			for loop in tuple:
				if not self.diagram.extendLoop(loop):
					break
				else:
					ec += 1
			
			# keep only if successful
			if ec == len(tuple):
				# keep only if still connectable by loops
				if self.min_chain_avloops_length() > 0:					
					ucc = self.filter_unicycle_chains(unicycle_chains)
					avt = self.filter_avtuples(avtuples)
					mr, mc, mn, mt = self.find_min_matched_tuples(ucc, avt)
					# keep only if still coverable by tuples
					if len(mn) > 0:
						# print(f"[purge] keeping")
						surviving_tuples.append(tuple)
						next_sample_lengths[tuple] = len(mn)
						if len(mn) == 1:
							next_single_choices[tuple] = mn
					
			# collapse back
			for loop in reversed(tuple[:ec]):
				self.diagram.collapseBack(loop)
						
		return (surviving_tuples, next_sample_lengths, next_single_choices)
	
	# ⇒ returns a minimum length set of tuples connected via a single-cycle chain, meant to be iterated through in a backtracker jump
	def find_min_matched_tuples(self, unicycle_chains, avtuples, next_sample_lengths=defaultdict(lambda:1)):
		#print(f"[fmmt] avtuples: {len(avtuples)}" + "\n" + "\n".join(["|".join([l.label() for l in sorted(tuple, key = lambda loop: (loop.ktype_radialIndex, loop.ktype))]) for tuple in avtuples]))
		min_viable_tuple_count = self.diagram.spClass
		min_next_sample_ratio = 2**42
		min_cycle = None
		min_matched_tuples = []
			
		# print(f"[fmmt] {unicycle_chains[0]}")
			
		for chain in unicycle_chains:
			cycle = chain.cycles[0]

			# cover each cycle with available tuples
			curr_cycle_tuples = [node.loop.tuple for node in cycle.nodes if node.loop.availabled or node.loop.extended]
			matched_tuples = [t for t in avtuples if t in curr_cycle_tuples]
			next_sample_ratio = 0 if len(matched_tuples) == 0 else sum([next_sample_lengths[t] for t in matched_tuples]) + len(matched_tuples)

			# remember smallest sample ratio with smallest sample count
			if next_sample_ratio < min_next_sample_ratio or (next_sample_ratio == min_next_sample_ratio and len(matched_tuples) < min_viable_tuple_count):
				min_next_sample_ratio = next_sample_ratio
				min_viable_tuple_count = len(matched_tuples)
				min_cycle = cycle
				min_matched_tuples = matched_tuples
				
		# reorder by sample count and ktype
		min_nodes = sorted([n for n in min_cycle.nodes if n.loop.tuple in min_matched_tuples], key = lambda n: (next_sample_lengths[n.loop.tuple], n.ktype)) if min_cycle is not None else []
		
		assert len(min_nodes) == len(min_matched_tuples) # [~][!] fails for very late initial purges
		
		min_matched_tuples = [n.loop.tuple for n in min_nodes]
		
		return (min_next_sample_ratio, min_cycle, min_nodes, min_matched_tuples)
		
		
	def print_cycle_ratio(self, cycle_address, avtuples, next_sample_lengths):
		cycle = self.diagram.cycleByAddress[cycle_address]
		curr_cycle_tuples = [node.loop.tuple for node in cycle.nodes if node.loop.availabled or node.loop.extended]
		matched_tuples = [t for t in avtuples if t in curr_cycle_tuples]
		next_sample_ratio = 0 if len(matched_tuples) == 0 else sum([next_sample_lengths[t] for t in matched_tuples]) / len(matched_tuples)		
		min_nodes = sorted([n for n in cycle.nodes if n.loop.tuple in matched_tuples], key = lambda n: (next_sample_lengths[n.loop.tuple], n.ktype))
		assert len(min_nodes) == len(matched_tuples)
		min_matched_tuples = [n.loop.tuple for n in min_nodes]
		print(f"[mx] ratio for {cycle} ⇒ mr: {next_sample_ratio:.4f} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
