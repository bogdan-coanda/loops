from loop import color_string


class Measurement (object):
	
	__slots__ = ['diagram', 
		'min_chlen', 'unchained_cycles', 'avloops', 'avtuples', 'tobex',
		'reduced', 'singles', 'coerced', 'zeroes', # from reduce() { singles/coerced + decimate loop } # reduced: if reduce() was ran
		'avtuples_before_viability', 'avtuples_before_untouched',
		'mc', 'mn', 'mt' 
		# mc holds either a cycle or a chains
		# mn holds the nodes whose loops will be tested
		# mt holds either the tuples belonging to the nodes tested, or is undefined
	]


	def __init__(self, diagram, old_mx = None):
		# 0. tie to diagram
		self.diagram = diagram
		
		# 1. find minimum chain avloops length
		self.min_chlen = min([len(chain.avloops) for chain in diagram.chains])
		
		# 2. find cycles not chained to any other
		self.unchained_cycles = [cycle for cycle in (old_mx.unchained_cycles if old_mx else diagram.cycles) if len(cycle.chain.cycles) is 1]
		
		# 3. find available loops 
		self.avloops = [l for l in (old_mx.avloops if old_mx else diagram.loops) if l.availabled]
		
		# 4. find available tuples (incl. already extended loops, excl. kernel connected loops)
		self.avtuples = [t for t in (old_mx.avtuples if old_mx else diagram.loop_tuples)
			if len([loop for loop in t if not loop.availabled and not loop.extended]) == 0
			and len([loop for loop in t if len([node.cycle for node in loop.nodes if node.cycle.isKernel]) != 0]) == 0]
			
		# 5. find number of loops that still need to be extended to reach a `potential` solution
		self.tobex = diagram.measureTobex()
				
		# 6. not yet reduced (as reducing is costly)
		self.reduced = False
								
		
	def remeasure(self):
		return Measurement(self.diagram, self)
		
		
	def __repr__(self):
		return "⟨mx | min chlen: {} | avloops: {} | avtuples: {}{} | chains: {} | unicycles: {} | tobex: {}⟩".format(
			self.min_chlen, len(self.avloops), len(self.avtuples), 
			"" if not hasattr(self, 'avtuples_before_viability') else "/"+str(len(self.avtuples_before_viability)),
			len(self.diagram.chains), len(self.unchained_cycles), self.tobex,
		) + ("" if not hasattr(self, 'reduced') or not self.reduced else "\n | s: {} | c: {} | z: {}".format(
				len(self.singles), len(self.coerced), len(self.zeroes))
		) + ("" if not hasattr(self, 'mc') else "\n | mc: {} | mt: ({}) {}".format(
			self.mc, len(self.mn), "".join(["["+n.address+":"+color_string(n.loop.ktype)+"]" for n in self.mn]))
		)
			
			
	def single(self):
		assert not self.reduced		
		self.min_chlen, self.singles, _ = Measurement.__coerce(self.diagram, self.min_chlen, False)
		self.coerced = []
		self.zeroes = []
		self.__init__(self.diagram, self)		
		self.reduced = True
		
			
	def reduce(self):
		assert not self.reduced
		# reduce
		self.min_chlen, self.singles, self.coerced, self.zeroes = Measurement.__reduce(self.diagram, self.min_chlen)
		# remeasure self
		self.__init__(self.diagram, self)
		# retain state
		self.reduced = True		
		
	
	def clean(self):
		if self.reduced:
			# clean
			Measurement.__clean(self.diagram, self.singles, self.coerced, self.zeroes)
			# leave self in a flawed state (but still printable)
			del self.reduced
			
	
	def measure_viable_tuples(self):
		self.avtuples_before_viability = self.avtuples
		self.avtuples = Measurement.__measure_viable_tuples(self.diagram, self.avtuples)		
		return self.avtuples
	
	
	def measure_untouched_tuples(self):
		self.avtuples_before_untouched = self.avtuples
		self.avtuples = Measurement.__measure_untouched_tuples(self.diagram, self.avtuples)
		return self.avtuples
			
			
	def find_min_simple(self):
		self.mc, self.mn, self.mt = Measurement._find_min_simple(self.diagram, self.unchained_cycles, self.avtuples)
		return self.mt
		
	
	def find_min_chain(self):
		self.mc, self.mn = Measurement.__find_min_chain(self.diagram)
		return self.mn
		
			
	# === internal =============================================================================================================================================================== #	

	def __coerce(diagram, min_chlen, doCoerce=True):
		singles = []
		coerced = []
		
		while True:
			found = False
			
			for chain in diagram.chains:
				avlen = len(chain.avloops)
				
				if avlen == 0:
					return (0, singles, coerced) 

				elif avlen == 1:
					avloop = list(chain.avloops)[0]
					singles.append(avloop)
					diagram.extendLoop(avloop)
					
					min_chlen = min([len(chain.avloops) for chain in diagram.chains])
					if min_chlen is 0:
						# input(".[coerce] dead @ extend | singles: " + str(len(singles)) + ", coerced: " + str(len(coerced)))
						return (0, singles, coerced)						
					
					found = True
					break
				
				elif avlen == 2 and doCoerce:
					killingFields = [loop.killingField() for loop in chain.avloops]
					intersected = killingFields[0].intersection(killingFields[1])
					if len(intersected):
						for avloop in intersected:
							coerced.append(avloop)
							diagram.setLoopUnavailabled(avloop)
							
							affected_min_chlen = min([len(n.cycle.chain.avloops) for n in avloop.nodes])
							if affected_min_chlen < min_chlen:
								min_chlen = affected_min_chlen
								if min_chlen is 0:
									# input(".[coerce] dead @ coerce | singles: " + str(len(singles)) + ", coerced: " + str(len(coerced)))
									return (0, singles, coerced)
							
						found = True
						break
																	
			if not found:
				return (min_chlen, singles, coerced)
		
		
	def __decimate(diagram, min_chlen):
		zeroes = []		
		
		while True:
			found = False
			avloops = [l for l in diagram.loops if l.availabled]
			# print("..[decimate] curr | avloops: " + str(len(avloops)))
			for index, loop in enumerate(avloops):
				diagram.extendLoop(loop)
				next_min_chlen, next_singles, next_coerced = Measurement.__coerce(diagram, min_chlen)
				next_chain_count = len(diagram.chains) # retain `current` chain count
				
				Measurement.__clean(diagram, next_singles, next_coerced, [])
				diagram.collapseBack(loop)
												
				if next_min_chlen == 0 and next_chain_count > 1:
					# print("..[decimate] zeroing " + str(loop) + " after s: " + str(len(singles)) + " | c: " + str(len(coerced)))
					zeroes.append(loop)
					diagram.setLoopUnavailabled(loop)
					
					affected_min_chlen = min([len(n.cycle.chain.avloops) for n in loop.nodes])
					if affected_min_chlen < min_chlen:
						min_chlen = affected_min_chlen
						if min_chlen is 0:
							# input("..[decimate] dead | zeroes: " + str(len(zeroes)))
							return (0, zeroes)
					
					found = True
			
			if not found:
				#print("..[decimate] done | zeroes: " + str(len(zeroes)))
				return (min_chlen, zeroes)
			#print("..[decimate] curr | zeroes: " + str(len(zeroes)))
			
			
	def __reduce(diagram, min_chlen):
		# mandatory
		min_chlen, curr_singles, curr_coerced = Measurement.__coerce(diagram, min_chlen)
		print("[reduce] init | s: " + str(len(curr_singles)) + " | c: " + str(len(curr_coerced)))
				
		if min_chlen is 0:
			# input("[reduce] dead @ init coerce | s: " + str(len(curr_singles)) + " | c: " + str(len(curr_coerced)) + " | z: 0")
			return (0, curr_singles, curr_coerced, [])
							
		min_chlen, curr_zeroes = Measurement.__decimate(diagram, min_chlen)
		print("[reduce] init | z: " + str(len(curr_zeroes)))
		
		if min_chlen is 0:
			# input("[reduce] dead @ init decimate | s: " + str(len(curr_singles)) + " | c: " + str(len(curr_coerced)) + " | z: " + str(len(curr_zeroes)))
			return (0, curr_singles, curr_coerced, curr_zeroes)		
		
		singles = list(curr_singles)
		coerced = list(curr_coerced)
		zeroes = list(curr_zeroes)
		
		# additional
		while True:
			if len(curr_zeroes) > 0:
				min_chlen, curr_singles, curr_coerced = Measurement.__coerce(diagram, min_chlen)
				singles += curr_singles
				coerced += curr_coerced			
				print("[reduce] curr | s: " + str(len(curr_singles)) + " | c: " + str(len(curr_coerced)))
				
				if min_chlen is 0:
					# input("[reduce] dead @ curr coerce | s: " + str(len(singles)) + " | c: " + str(len(coerced)) + " | z: " + str(len(zeroes)))
					return (0, singles, coerced, zeroes)
											
				if len(curr_singles) or len(curr_coerced):
					min_chlen, curr_zeroes = Measurement.__decimate(diagram, min_chlen)
					zeroes += curr_zeroes
					print("[reduce] curr | z: " + str(len(curr_zeroes)))
					
					if min_chlen is 0:
						# input("[reduce] dead @ curr decimate | s: " + str(len(singles)) + " | c: " + str(len(coerced)) + " | z: " + str(len(zeroes)))
						return (0, singles, coerced, zeroes)
										
				else:
					break
			else:
				break
				
		print("[reduce] done | s: " + str(len(singles)) + " | c: " + str(len(coerced)) + " | z: " + str(len(zeroes)))
		return (min_chlen, singles, coerced, zeroes)		
				
				
	def __clean(diagram, singles, coerced, zeroes):
		for l in reversed(singles):
			diagram.collapseBack(l)						
		for l in coerced:
			diagram.setLoopAvailabled(l)
		for l in zeroes:
			diagram.setLoopAvailabled(l)		
	
	
	def __measure_viable_tuples(diagram, avtuples):
		viable_tuples = []
		
		for tindex, curr_tuple in enumerate(avtuples):
			
			# extend current tuple
			curr_extended_loops = []
			for loop in curr_tuple:
				if diagram.extendLoop(loop):
					curr_extended_loops.append(loop)
				else:
					break							
	
			# check tuple completeness
			if len(curr_extended_loops) == len(curr_tuple):
				min_chlen = min([len(chain.avloops) for chain in diagram.chains])
				
				# check tuple viability
				if min_chlen != 0 or len(diagram.chains) == 1:
					viable_tuples.append(curr_tuple)

			# collapse current tuple				
			for loop in reversed(curr_extended_loops):
				diagram.collapseBack(loop)		
	
		return viable_tuples


	def __measure_untouched_tuples(diagram, avtuples):
		return [t for t in avtuples # all tuples # with no connected loops
							if len( # having no loops # if we have no connected loops
								[l for l in t # which # if we have connected loops
										if len( # having nodes # if we have connected nodes
											[n for n in l.nodes # which # if we have connected nodes
													if len(n.cycle.chain.cycles) is not 1] # are in cycles tied to other cycles (extended through by another node) # if we have a connected node
										) is not 0]
							) is 0]								


	def _find_min_simple(diagram, unchained_cycles, avtuples):
		min_viable_tuple_count = diagram.spClass
		min_cycle = None
		min_matched_tuples = []
			
		#print("[find_min_blabla] unchained_cycles: " + str(len(unchained_cycles)))
		for cycle in unchained_cycles:
			curr_cycle_tuples = [node.loop.tuple for node in cycle.nodes if node.loop.availabled or node.loop.extended]
			matched_tuples = [t for t in avtuples if t in curr_cycle_tuples]
			
			if len(matched_tuples) < min_viable_tuple_count:
				min_viable_tuple_count = len(matched_tuples)
				min_cycle = cycle
				min_matched_tuples = matched_tuples
				
		# reorder by ktype	
		min_nodes = sorted([n for n in min_cycle.nodes if n.loop.tuple in min_matched_tuples], key = lambda n: n.ktype) if min_cycle is not None else []
		assert len(min_nodes) == len(min_matched_tuples)
		min_matched_tuples = [n.loop.tuple for n in min_nodes]
		
		return (min_cycle, min_nodes, min_matched_tuples)
																							

	def __find_min_chain(diagram):
		
		min_chain = diagram.startNode.cycle.chain
		min_avlen = len(min_chain.avloops)
		min_address = sorted(min_chain.cycles, key = lambda cycle: cycle.address)[0].address
				
		for curr_chain in diagram.chains:
			if len(curr_chain.avloops) <= min_avlen:
				curr_address = sorted(curr_chain.cycles, key = lambda cycle: cycle.address)[0].address
				if len(curr_chain.avloops) < min_avlen or curr_address < min_address:
					min_chain = curr_chain
					min_avlen = len(min_chain.avloops)
					min_address = curr_address
		
		min_nodes = []
		for loop in min_chain.avloops:
			ns = [node for node in loop.nodes if node.cycle.chain is min_chain]
			assert len(ns) is 1
			min_nodes.append(ns.pop())
		
		return (min_chain, sorted(min_nodes, key = lambda node: (node.ktype, node.address)))
																							
# ============================================================================================================================================================================== #	
# ============================================================================================================================================================================== #	

if __name__ == "__main__":	
	
	from diagram import Diagram
	from uicanvas import show
	
	d = Diagram(6,1)
	d.point(); show(d); print("§")
		
	mx0 = Measurement(d)	
	mx0.reduce()
	mx0.measure_viable_tuples()
	mt0 = mx0.find_min_simple()
	d.pointers = mx0.mn; show(d); print(mx0)

	# 0⁴
	for l in mt0[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 0⁴")

	mx1 = mx0.remeasure()	
	mx1.reduce()
	mx1.measure_viable_tuples()
	mt1 = mx1.find_min_simple()
	d.pointers = mx1.mn; show(d); print(mx1)

	# 0⁴0³
	for l in mt1[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 0⁴0³")

	mx2 = mx1.remeasure()	
	mx2.reduce()
	mx2.measure_viable_tuples()
	mt2 = mx2.find_min_simple()
	d.pointers = mx2.mn; show(d); print(mx2)

	# 0⁴0³0¹
	for l in mt2[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 0⁴0³0¹")		

	mx3 = mx2.remeasure()	
	mx3.reduce()
	mx3.measure_viable_tuples()
	mt3 = mx3.find_min_simple()
	d.pointers = mx3.mn; show(d); print(mx3)

	# 0⁴0³0¹0¹
	for l in mt3[0]:
		assert d.extendLoop(l)

	d.point(); show(d); print("§ 0⁴0³0¹0¹")

	mx4 = mx3.remeasure()	
	mx4.reduce()
	mx4.measure_viable_tuples()
	mt4 = mx4.find_min_simple()
	d.pointers = mx4.mn; show(d); print(mx4)
	''' ⇒ dead end '''
	 
	mx4.clean()
	for l in reversed(mt3[0]):
		d.collapseBack(l)	
	
	d.pointers = mx3.mn; show(d); print(mx3)
	''' ⇒ dead end '''

	mx3.clean()
	for l in reversed(mt2[0]):
		d.collapseBack(l)	
														
	d.pointers = mx2.mn; show(d); print(mx2)
	''' ⇒ dead end '''

	mx2.clean()
	for l in reversed(mt1[0]):
		d.collapseBack(l)	
														
	d.pointers = mx1.mn; show(d); print(mx1)
	
	# 0⁴1³
	for l in mt1[1]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 0⁴1³")		
	
	mx2 = mx1.remeasure()	
	mx2.reduce()
	mx2.measure_viable_tuples()
	mt2 = mx2.find_min_simple()
	d.pointers = mx2.mn; show(d); print(mx2)	
	''' ⇒ 4 sols [kern:02] '''
	
	mx2.clean()
	for l in reversed(mt1[1]):
		d.collapseBack(l)
	
	d.pointers = mx1.mn; show(d); print(mx1)
	
	# 0⁴2³
	for l in mt1[2]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 0⁴2³")		
	
	mx2 = mx1.remeasure()	
	mx2.reduce()
	mx2.measure_viable_tuples()
	mt2 = mx2.find_min_simple()
	d.pointers = mx2.mn; show(d); print(mx2)	
	
	# 0⁴2³0²
	for l in mt2[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 0⁴2³0²")
	
	mx3 = mx2.remeasure()	
	mx3.reduce()
	mx3.measure_viable_tuples()
	mt3 = mx3.find_min_simple()
	d.pointers = mx3.mn; show(d); print(mx3)
		
	# 0⁴2³0²0²
	for l in mt3[0]:
		assert d.extendLoop(l)

	d.point(); show(d); print("§ 0⁴2³0²0²")		
	
	mx4 = mx3.remeasure()	
	mx4.reduce()
	mx4.measure_viable_tuples()
	mt4 = mx4.find_min_simple()
	d.pointers = mx4.mn; show(d); print(mx4)	
	''' ⇒ dead end '''
	 
	mx4.clean()
	for l in reversed(mt3[0]):
		d.collapseBack(l)	
	
	d.pointers = mx3.mn; show(d); print(mx3)
					
	# 0⁴2³0²1²
	for l in mt3[1]:
		assert d.extendLoop(l)

	d.point(); show(d); print("§ 0⁴2³0²1²")		
	
	mx4 = mx3.remeasure()	
	mx4.reduce()
	mx4.measure_viable_tuples()
	mt4 = mx4.find_min_simple()
	d.pointers = mx4.mn; show(d); print(mx4)		
	''' ⇒ dead end '''
	 
	mx4.clean()
	for l in reversed(mt3[1]):
		d.collapseBack(l)	
	
	d.pointers = mx3.mn; show(d); print(mx3)
	''' ⇒ dead end '''

	mx3.clean()
	for l in reversed(mt2[0]):
		d.collapseBack(l)	
														
	d.pointers = mx2.mn; show(d); print(mx2)
		
	# 0⁴2³1²
	for l in mt2[1]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 0⁴2³1²")

	mx3 = mx2.remeasure()	
	mx3.reduce()
	mx3.measure_viable_tuples()
	mt3 = mx3.find_min_simple()
	d.pointers = mx3.mn; show(d); print(mx3)
	''' ⇒ dead end '''

	mx3.clean()
	for l in reversed(mt2[1]):
		d.collapseBack(l)	
														
	d.pointers = mx2.mn; show(d); print(mx2)
	''' ⇒ dead end '''

	mx2.clean()
	for l in reversed(mt1[2]):
		d.collapseBack(l)	
														
	d.pointers = mx1.mn; show(d); print(mx1)				
	''' ⇒ dead end '''

	mx1.clean()
	for l in reversed(mt0[0]):
		d.collapseBack(l)	
		
	d.pointers = mx0.mn; show(d); print(mx0)

	# 1⁴
	for l in mt0[1]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 1⁴")	
																																																					
	mx1 = mx0.remeasure()	
	mx1.reduce()
	mx1.measure_viable_tuples()
	mt1 = mx1.find_min_simple()
	d.pointers = mx1.mn; show(d); print(mx1)	
	
	# 1⁴0³
	for l in mt1[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 1⁴0³")	
	
	mx2 = mx1.remeasure()	
	mx2.reduce()
	mx2.measure_viable_tuples()
	mt2 = mx2.find_min_simple()
	d.pointers = mx2.mn; show(d); print(mx2)		
	
	# 1⁴0³0¹
	for l in mt2[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 1⁴0³0¹")	
	
	mx3 = mx2.remeasure()	
	mx3.reduce()
	mx3.measure_viable_tuples()
	mt3 = mx3.find_min_simple()
	d.pointers = mx3.mn; show(d); print(mx3)
		
	# 1⁴0³0¹0¹
	for l in mt3[0]:
		assert d.extendLoop(l)

	d.point(); show(d); print("§ 1⁴0³0¹0¹")				
	
	mx4 = mx3.remeasure()	
	mx4.reduce()
	mx4.measure_viable_tuples()
	mt4 = mx4.find_min_simple()
	d.pointers = mx4.mn; show(d); print(mx4)				
	''' ⇒ dead end '''
	 
	mx4.clean()
	for l in reversed(mt3[0]):
		d.collapseBack(l)	
	
	d.pointers = mx3.mn; show(d); print(mx3)
	''' ⇒ dead end '''

	mx3.clean()
	for l in reversed(mt2[0]):
		d.collapseBack(l)	
														
	d.pointers = mx2.mn; show(d); print(mx2)	
	''' ⇒ dead end '''

	mx2.clean()
	for l in reversed(mt1[0]):
		d.collapseBack(l)	
														
	d.pointers = mx1.mn; show(d); print(mx1)					
	
	# 1⁴1³
	for l in mt1[1]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 1⁴1³")		
	
	mx2 = mx1.remeasure()	
	mx2.reduce()
	mx2.measure_viable_tuples()
	mt2 = mx2.find_min_simple()
	d.pointers = mx2.mn; show(d); print(mx2)		
	
	# 1⁴1³0²
	for l in mt2[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 1⁴1³0²")		
		
	mx3 = mx2.remeasure()	
	mx3.reduce()
	mx3.measure_viable_tuples()
	mt3 = mx3.find_min_simple()
	d.pointers = mx3.mn; show(d); print(mx3)	
	
	# 1⁴1³0²0¹
	for l in mt3[0]:
		assert d.extendLoop(l)

	d.point(); show(d); print("§ 1⁴1³0²0¹")					
	
	mx4 = mx3.remeasure()	
	mx4.reduce()
	mx4.measure_viable_tuples()
	mt4 = mx4.find_min_simple()
	d.pointers = mx4.mn; show(d); print(mx4)				
	''' ⇒ 4 sols [kern:43] '''			
		
	mx4.clean()
	for l in reversed(mt3[0]):
		d.collapseBack(l)	
	
	d.pointers = mx3.mn; show(d); print(mx3)
	''' ⇒ dead end '''

	mx3.clean()
	for l in reversed(mt2[0]):
		d.collapseBack(l)	
														
	d.pointers = mx2.mn; show(d); print(mx2)		
	
	# 1⁴1³1²
	for l in mt2[1]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 1⁴1³1²")			
	
	mx3 = mx2.remeasure()	
	mx3.reduce()
	mx3.measure_viable_tuples()
	mt3 = mx3.find_min_simple()
	d.pointers = mx3.mn; show(d); print(mx3)			
	''' ⇒ dead end '''

	mx3.clean()
	for l in reversed(mt2[1]):
		d.collapseBack(l)	
														
	d.pointers = mx2.mn; show(d); print(mx2)		
	''' ⇒ dead end '''

	mx2.clean()
	for l in reversed(mt1[1]):
		d.collapseBack(l)	
														
	d.pointers = mx1.mn; show(d); print(mx1)
		
	# 1⁴2³
	for l in mt1[2]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 1⁴2³")				
	
	mx2 = mx1.remeasure()	
	mx2.reduce()
	mx2.measure_viable_tuples()
	mt2 = mx2.find_min_simple()
	d.pointers = mx2.mn; show(d); print(mx2)			
	
	# 1⁴2³0¹
	for l in mt2[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 1⁴2³0¹")				
	
	mx3 = mx2.remeasure()	
	mx3.reduce()
	mx3.measure_viable_tuples()
	mt3 = mx3.find_min_simple()
	d.pointers = mx3.mn; show(d); print(mx3)				
	''' ⇒ dead end '''

	mx3.clean()
	for l in reversed(mt2[0]):
		d.collapseBack(l)	
														
	d.pointers = mx2.mn; show(d); print(mx2)			
	''' ⇒ dead end '''

	mx2.clean()
	for l in reversed(mt1[2]):
		d.collapseBack(l)	
														
	d.pointers = mx1.mn; show(d); print(mx1)	
	''' ⇒ dead end '''

	mx1.clean()
	for l in reversed(mt0[1]):
		d.collapseBack(l)	
		
	d.pointers = mx0.mn; show(d); print(mx0)

	# 2⁴
	for l in mt0[2]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 2⁴")		
	
	mx1 = mx0.remeasure()	
	mx1.reduce()
	mx1.measure_viable_tuples()
	mt1 = mx1.find_min_simple()
	d.pointers = mx1.mn; show(d); print(mx1)		
	
	# 2⁴0²
	for l in mt1[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 2⁴0²")					
	
	mx2 = mx1.remeasure()	
	mx2.reduce()
	mx2.measure_viable_tuples()
	mt2 = mx2.find_min_simple()
	d.pointers = mx2.mn; show(d); print(mx2)				
	
	# 2⁴0²0¹
	for l in mt2[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 2⁴0²0¹")					
	
	mx3 = mx2.remeasure()	
	mx3.reduce()
	mx3.measure_viable_tuples()
	mt3 = mx3.find_min_simple()
	d.pointers = mx3.mn; show(d); print(mx3)				
	
	# 2⁴0²0¹0¹
	for l in mt3[0]:
		assert d.extendLoop(l)

	d.point(); show(d); print("§ 2⁴0²0¹0¹")						
	
	mx4 = mx3.remeasure()	
	mx4.reduce()
	mx4.measure_viable_tuples()
	mt4 = mx4.find_min_simple()
	d.pointers = mx4.mn; show(d); print(mx4)					
	
	# 2⁴0²0¹0¹0²
	for l in mt4[0]:
		assert d.extendLoop(l)

	d.point(); show(d); print("§ 2⁴0²0¹0¹0²")							

	mx5 = mx4.remeasure()	
	mx5.reduce()
	mx5.measure_viable_tuples()
	mt5 = mx5.find_min_simple()
	d.pointers = mx5.mn; show(d); print(mx5)								
	''' ⇒ dead end '''

	mx5.clean()
	for l in reversed(mt4[0]):
		d.collapseBack(l)	
		
	d.pointers = mx4.mn; show(d); print(mx4)

	# 2⁴0²0¹0¹1²
	for l in mt4[1]:
		assert d.extendLoop(l)

	d.point(); show(d); print("§ 2⁴0²0¹0¹1²")							
	mx5 = mx4.remeasure()	
	mx5.reduce()
	mx5.measure_viable_tuples()
	mt5 = mx5.find_min_simple()
	d.pointers = mx5.mn; show(d); print(mx5)															
	''' ⇒ 4 sols [kern:42] '''

	mx5.clean()
	for l in reversed(mt4[1]):
		d.collapseBack(l)	

	d.pointers = mx4.mn; show(d); print(mx4)			
	''' ⇒ dead end '''
	 
	mx4.clean()
	for l in reversed(mt3[0]):
		d.collapseBack(l)	
	
	d.pointers = mx3.mn; show(d); print(mx3)
	''' ⇒ dead end '''

	mx3.clean()
	for l in reversed(mt2[0]):
		d.collapseBack(l)	
														
	d.pointers = mx2.mn; show(d); print(mx2)	
	''' ⇒ dead end '''

	mx2.clean()
	for l in reversed(mt1[0]):
		d.collapseBack(l)	
														
	d.pointers = mx1.mn; show(d); print(mx1)						
	
	# 2⁴1²
	for l in mt1[1]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 2⁴1²")						
	
	mx2 = mx1.remeasure()	
	mx2.reduce()
	mx2.measure_viable_tuples()
	mt2 = mx2.find_min_simple()
	d.pointers = mx2.mn; show(d); print(mx2)					
	
	# 2⁴1²0¹
	for l in mt2[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 2⁴1²0¹")						
	
	mx3 = mx2.remeasure()	
	mx3.reduce()
	mx3.measure_viable_tuples()
	mt3 = mx3.find_min_simple()
	d.pointers = mx3.mn; show(d); print(mx3)					
	
	# 2⁴1²0¹0¹
	for l in mt3[0]:
		assert d.extendLoop(l)

	d.point(); show(d); print("§ 2⁴1²0¹0¹")						
		
	mx4 = mx3.remeasure()	
	mx4.reduce()
	mx4.measure_viable_tuples()
	mt4 = mx4.find_min_simple()
	d.pointers = mx4.mn; show(d); print(mx4)						
	
	# 2⁴1²0¹0¹0²
	for l in mt4[0]:
		assert d.extendLoop(l)

	d.point(); show(d); print("§ 2⁴1²0¹0¹0²")							

	mx5 = mx4.remeasure()	
	mx5.reduce()
	mx5.measure_viable_tuples()
	mt5 = mx5.find_min_simple()
	d.pointers = mx5.mn; show(d); print(mx5)									
	''' ⇒ dead end '''

	mx5.clean()
	for l in reversed(mt4[0]):
		d.collapseBack(l)	
		
	d.pointers = mx4.mn; show(d); print(mx4)

	# 2⁴1²0¹0¹1²
	for l in mt4[1]:
		assert d.extendLoop(l)

	d.point(); show(d); print("§ 2⁴1²0¹0¹1²")							
	mx5 = mx4.remeasure()	
	mx5.reduce()
	mx5.measure_viable_tuples()
	mt5 = mx5.find_min_simple()
	d.pointers = mx5.mn; show(d); print(mx5)																
	''' ⇒ 4 sols [kern:02] '''	

	mx5.clean()
	for l in reversed(mt4[1]):
		d.collapseBack(l)	

	d.pointers = mx4.mn; show(d); print(mx4)			
	''' ⇒ dead end '''
	 
	mx4.clean()
	for l in reversed(mt3[0]):
		d.collapseBack(l)	
	
	d.pointers = mx3.mn; show(d); print(mx3)
	''' ⇒ dead end '''

	mx3.clean()
	for l in reversed(mt2[0]):
		d.collapseBack(l)	
														
	d.pointers = mx2.mn; show(d); print(mx2)	
	''' ⇒ dead end '''

	mx2.clean()
	for l in reversed(mt1[1]):
		d.collapseBack(l)	
														
	d.pointers = mx1.mn; show(d); print(mx1)								
	''' ⇒ dead end '''

	mx1.clean()
	for l in reversed(mt0[2]):
		d.collapseBack(l)	
		
	d.pointers = mx0.mn; show(d); print(mx0)

	# 3⁴
	for l in mt0[3]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 3⁴")	
																																																					
	mx1 = mx0.remeasure()	
	mx1.reduce()
	mx1.measure_viable_tuples()
	mt1 = mx1.find_min_simple()
	d.pointers = mx1.mn; show(d); print(mx1)		
	
	# 3⁴0²
	for l in mt1[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 3⁴0²")					
	
	mx2 = mx1.remeasure()	
	mx2.reduce()
	mx2.measure_viable_tuples()
	mt2 = mx2.find_min_simple()
	d.pointers = mx2.mn; show(d); print(mx2)					
	
	# 3⁴0²0¹
	for l in mt2[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 3⁴0²0¹")		

	mx3 = mx2.remeasure()	
	mx3.reduce()
	mx3.measure_viable_tuples()
	mt3 = mx3.find_min_simple()
	d.pointers = mx3.mn; show(d); print(mx3)	
	''' ⇒ dead end '''

	mx3.clean()
	for l in reversed(mt2[0]):
		d.collapseBack(l)	
														
	d.pointers = mx2.mn; show(d); print(mx2)	
	''' ⇒ dead end '''

	mx2.clean()
	for l in reversed(mt1[0]):
		d.collapseBack(l)	
														
	d.pointers = mx1.mn; show(d); print(mx1)									
	
	# 3⁴1²
	for l in mt1[1]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 3⁴1²")							
	
	mx2 = mx1.remeasure()	
	mx2.reduce()
	mx2.measure_viable_tuples()
	mt2 = mx2.find_min_simple()
	d.pointers = mx2.mn; show(d); print(mx2)						
	
	# 3⁴1²0²
	for l in mt2[0]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 3⁴1²0²")		
		
	mx3 = mx2.remeasure()	
	mx3.reduce()
	mx3.measure_viable_tuples()
	mt3 = mx3.find_min_simple()
	d.pointers = mx3.mn; show(d); print(mx3)		
	
	# 3⁴1²0²0¹
	for l in mt3[0]:
		assert d.extendLoop(l)

	d.point(); show(d); print("§ 3⁴1²0²0¹")						
		
	mx4 = mx3.remeasure()	
	mx4.reduce()
	mx4.measure_viable_tuples()
	mt4 = mx4.find_min_simple()
	d.pointers = mx4.mn; show(d); print(mx4)								
	''' ⇒ dead end '''
	 
	mx4.clean()
	for l in reversed(mt3[0]):
		d.collapseBack(l)	
	
	d.pointers = mx3.mn; show(d); print(mx3)	
	''' ⇒ dead end '''

	mx3.clean()
	for l in reversed(mt2[0]):
		d.collapseBack(l)	
														
	d.pointers = mx2.mn; show(d); print(mx2)	
	
	# 3⁴1²1²
	for l in mt2[1]:
		assert d.extendLoop(l)
		
	d.point(); show(d); print("§ 3⁴1²1²")

	mx3 = mx2.remeasure()	
	mx3.reduce()
	mx3.measure_viable_tuples()
	mt3 = mx3.find_min_simple()
	d.pointers = mx3.mn; show(d); print(mx3)	
	
	# 3⁴1²1²0¹
	for l in mt3[0]:
		assert d.extendLoop(l)

	d.point(); show(d); print("§ 3⁴1²1²0¹")						
		
	mx4 = mx3.remeasure()	
	mx4.reduce()
	mx4.measure_viable_tuples()
	mt4 = mx4.find_min_simple()
	d.pointers = mx4.mn; show(d); print(mx4)									
	''' ⇒ dead end '''
	 
	mx4.clean()
	for l in reversed(mt3[0]):
		d.collapseBack(l)	
	
	d.pointers = mx3.mn; show(d); print(mx3)	
	''' ⇒ dead end '''

	mx3.clean()
	for l in reversed(mt2[1]):
		d.collapseBack(l)	
														
	d.pointers = mx2.mn; show(d); print(mx2)		
	''' ⇒ dead end '''

	mx2.clean()
	for l in reversed(mt1[1]):
		d.collapseBack(l)	
														
	d.pointers = mx1.mn; show(d); print(mx1)	
	''' ⇒ dead end '''

	mx1.clean()
	for l in reversed(mt0[3]):
		d.collapseBack(l)	
		
	d.pointers = mx0.mn; show(d); print(mx0)	
	''' ⇒ dead end '''
	
	mx0.clean()		
	d.point(); show(d);		
