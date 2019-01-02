class KillingField (object):
	
	__slots__ = ['loop', 'field']
	
	def __init__(self, loop):
		self.loop = loop
		self.field = KillingField.calculateKillingFieldSet(loop)
				
	def __len__(self):
		return len(self.field)
		
	def __iter__(self):
		return iter(self.field)
		
	def add(self, loop):
		self.field.add(loop)		

	def remove(self, loop):
		self.field.remove(loop)
		
	def intersection(self, other):
		return self.field.intersection(other.field)
		
	def regenerate(self):
		self.field = KillingField.calculateKillingFieldSet(self.loop)
		
	def assess(self):
		assert self.field == KillingField.calculateKillingFieldSet(self.loop)
		
	def assessAllLoops(diagram):
		for l in diagram.loops:
			if l.availabled:
				l.killingField.assess()		
				
	def calculateKillingFieldSet(self_loop):
										
		# find loops with just multiple appearances - these nodes would get killed when extending this (self) loop, as they tie to at least two of the self's new connected chains
		seen = set() # unique seen once loops
		dups = set() # unique seen more loops

		# gather around all avloops for chains tied to this loop (including multiples)				
		for n in self_loop.nodes:
			for ncn in n.chain.avnodes:
				loop = ncn.loop
				if loop in seen:
					if loop not in dups:
						dups.add(loop)
				else:
					seen.add(loop)
		
		# remove self
		dups.remove(self_loop)
		
		# return killing field							
		return dups
		
	def fixGenerateKernel(kernel_chain):
		kfPreviousFields = []		
		
		for node in kernel_chain.avnodes:
			kfPreviousFields.append((node.loop.killingField, node.loop.killingField.field))
			node.loop.killingField.regenerate()
		
		return kfPreviousFields#, kfRemovedLoops)
				
	def fixExtendLoop(loop):
		# kfRemoves = []
		# kfRecalcs = []
	
		# kfRemovedLoops = []
		kfPreviousFields = []
		
		# for each dead loop [~] should be solved by individual calls to fixSetLoopUnavailabled
		# for affected_loop in loop.extension_result.affected_loops:
			# remove it from its killing field :: loops :: killing fields
		# 	for kf_loop in affected_loop.killingField:
		# 		if kf_loop.availabled: # only update still available killing field :: loops
		# 			kf_loop.killingField.remove(affected_loop)
					#kfRemoves.append(kf_loop.killingField)
		# 			kfRemovedLoops.append((kf_loop.killingField, affected_loop))
		 
		for node in loop.extension_result.new_chain.avnodes:
			#kfRecalcs.append(node.loop.killingField)
			kfPreviousFields.append((node.loop.killingField, node.loop.killingField.field))
			node.loop.killingField.regenerate()
		
		# print(f"[kf:fixExtend] {len(loop.killingField)} | removes: {len(kfRemoves)} (uniq:{len(list(set(kfRemoves)))}) | recalcs: {len(kfRecalcs)} (uniq:{len(set(kfRecalcs))}) | redones: {len(set(kfRecalcs).intersection(kfRemoves))} | {loop}")		
		return kfPreviousFields#, kfRemovedLoops)
		
	def fixCollapseBack(kfPreviousFields): #, kfRemovedLoops):
		# revert to previous killing fields (mandatory recalcs before removes)
		for kf, field in reversed(kfPreviousFields):
			kf.field = field
				
		# for kf, l in kfRemovedLoops:
		# 	kf.add(l)		
	
	def fixSetLoopUnavailabled(loop):
		kfRemovedLoops = []
				
		for kf_loop in loop.killingField:
			if kf_loop.availabled: # only update still available killing field :: loops
				kf_loop.killingField.remove(loop)
				kfRemovedLoops.append((kf_loop.killingField, loop))		
				
		return kfRemovedLoops
		
	def fixSetLoopAvailabled(kfRemovedLoops):
		for kf, l in reversed(kfRemovedLoops):
			kf.add(l)		
			
