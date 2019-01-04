from common import tstr
from time import time
import itertools


class KillingField (object):
	
	__slots__ = ['loop', 'field', 'seen']
	
	regenCount = 0
	vts =[0, 0, 0, 0]
	vtc = 0
	
	def __init__(self, loop):
		self.loop = loop
		self.field, self.seen = KillingField.calculateKillingFieldSet(loop)
				
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
		
	def regenerate(self, extendedLoop=None):
		
		oldField = self.field
		oldSeen = self.seen
			
		tx = time()
		self.field, self.seen = KillingField.calculateKillingFieldSet(self.loop)		
		
		if extendedLoop:					
			KillingField.regenCount += 1			
					
			KillingField.vts[0] += (time() - tx)
			
			tx = time()
			kf = KillingField.calculateKillingFieldSet2(self.loop)
			KillingField.vts[1] += (time() - tx)		
			assert self.field == set(kf) and len(self.field) == len(kf)
			
			tx = time()
			kf_all, kf_uni = KillingField.calculateKillingFieldSet3(self.loop)
			KillingField.vts[2] += (time() - tx)						
			assert self.field == kf_all

			tx = time()
			kf_field, kf_seen = KillingField.calculateKillingFieldSet4(self.loop, extendedLoop, oldSeen, oldField)
			KillingField.vts[3] += (time() - tx)						
			assert self.field == kf_field and self.seen == kf_seen, f"{self.field.difference(kf_field)} | {kf_field.difference(self.field)} ∘ {self.seen.difference(kf_seen)} | {kf_seen.difference(self.seen)}"
												
		if KillingField.vtc % 1000 == 0:
			print(f"[vtc:{KillingField.vtc}] vts: " + ' | '.join([f"{i}: {tstr(KillingField.vts[i])}" for i in range(len(KillingField.vts))]))
		KillingField.vtc += 1
		
	def assess(self):
		kf_field, kf_seen = KillingField.calculateKillingFieldSet(self.loop)
		assert self.field == kf_field #and self.seen == kf_seen
		
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
		return dups, seen

	def calculateKillingFieldSet2(self_loop):
										
		# find loops with just multiple appearances - these nodes would get killed when extending this (self) loop, as they tie to at least two of the self's new connected chains
		seen = [] # unique seen once loops
		dups = [] # unique seen more loops

		# gather around all avloops for chains tied to this loop (including multiples)				
		for n in self_loop.nodes:
			for ncn in n.chain.avnodes:
				loop = ncn.loop
				if loop in seen:
					if loop not in dups:
						dups.append(loop)
				else:
					seen.append(loop)
		
		# remove self
		dups.remove(self_loop)
		
		# return killing field							
		return dups

	def calculateKillingFieldSet3(self_loop):
										
		# find loops with just multiple appearances - these nodes would get killed when extending this (self) loop, as they tie to at least two of the self's new connected chains
		all = list(itertools.chain(*[[ncn.loop for ncn in n.chain.avnodes] for n in self_loop.nodes]))
		uni = set(all)
		
		for loop in uni:
			all.remove(loop)
		
		all = set(all)
		all.remove(self_loop)
		return (all, uni)

	def calculateKillingFieldSet4(self_loop, extendedLoop=None, oldSeen=None, oldField=None):
		
		if extendedLoop:			
						
			changedNode = [node for node in self_loop.nodes if node.chain == extendedLoop.extension_result.new_chain]
			assert len(changedNode) == 1
			changedNode = changedNode[0]
			
			oldChain = [chain for chain in extendedLoop.extension_result.affected_chains if changedNode in chain.avnodes]
			assert len(oldChain) == 1
			oldChain = oldChain[0]
			
			if extendedLoop.firstAddress() == '0000054':
				print(f"[kf4] changed node: {changedNode} | oldChain: {oldChain} | new chain nodes not in old chain: {len([node for node in extendedLoop.extension_result.new_chain.avnodes if node not in oldChain.avnodes])} | new chain nodes not in old chain but in oldSeen: {len([node for node in extendedLoop.extension_result.new_chain.avnodes if node not in oldChain.avnodes and node.loop in oldSeen])}")
						
			kf_field = set([loop for loop in oldField if loop.availabled])
			kf_seen = set([loop for loop in oldSeen if loop.availabled])
			for node in extendedLoop.extension_result.new_chain.avnodes:
				if extendedLoop.firstAddress() == '0000054':
					print(f"[kf4] checking {node} with {node.loop}")
				if node not in oldChain.avnodes:
					if extendedLoop.firstAddress() == '0000054':
						print(f"[kf4] ⇒ not in old chain")
					loop = node.loop
					if loop in kf_seen:
						if extendedLoop.firstAddress() == '0000054':
							print(f"[kf4] ⇒ in seen")
						if loop not in kf_field:
							if extendedLoop.firstAddress() == '0000054':
								print(f"[kf4] ⇒ not in field")
							kf_field.add(loop)
					else:
						if extendedLoop.firstAddress() == '0000054':
							print(f"[kf4] ⇒ not in seen")
						kf_seen.add(loop)						
			
			assert self_loop not in kf_field
			
			return kf_field, kf_seen
			
		return oldField
		
																																		
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
			kfPreviousFields.append((node.loop.killingField, node.loop.killingField.field, node.loop.killingField.seen))
			node.loop.killingField.regenerate(loop)
		
		# print(f"[kf:fixExtend] {len(loop.killingField)} | removes: {len(kfRemoves)} (uniq:{len(list(set(kfRemoves)))}) | recalcs: {len(kfRecalcs)} (uniq:{len(set(kfRecalcs))}) | redones: {len(set(kfRecalcs).intersection(kfRemoves))} | {loop}")		
		return kfPreviousFields#, kfRemovedLoops)
		
	def fixCollapseBack(kfPreviousFields): #, kfRemovedLoops):
		# revert to previous killing fields (mandatory recalcs before removes)
		for kf, field, seen in reversed(kfPreviousFields):
			kf.field = field
			kf.seen = seen
				
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
			
