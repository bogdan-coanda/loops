from common import tstr, input2
from time import time
import itertools


class KillingField (object):
	
	__slots__ = ['loop', 'field', 'seen']
		
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
		self.field, self.seen = KillingField.calculateKillingFieldSet(self.loop)		
		
						
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
		
																																		
	def fixGenerateKernel(kernel_chain):
		kfPreviousFields = []		
		
		for node in kernel_chain.avnodes:
			kfPreviousFields.append((node.loop.killingField, node.loop.killingField.field))
			node.loop.killingField.regenerate()
		
		return kfPreviousFields
				
																												
	def fixExtendLoop(diagram, extendedLoop):
				
		kfAddedLoops = [] 
		
		# ∘ for each old chain
		for oldChain in extendedLoop.extension_result.affected_chains:
			# ∘ for each changed node in the old chain ~ basically we go through every node in the new chain, but by knowing in which old chain the node was before
			for changedNode in oldChain.avnodes:

				'''
				# ∘ for each node in the new chain
				for node in extendedLoop.extension_result.new_chain.avnodes:
					# ∘ that is not in the selected old chain
					if node not in oldChain.avnodes:
						# ∘ update the killing field for the selected changed node
						loop = node.loop
				'''		
				
				# ∘ go through every node in the new chain
				for o2Chain in extendedLoop.extension_result.affected_chains:
					# ∘ that is not in the old chain
					if o2Chain != oldChain:
						#print(f"[kf:extend] ∘∘ o2 chain: {oc2}/{len(extendedLoop.extension_result.affected_chains)}")									
						for ch2Node in o2Chain.avnodes:
							#print(f"[kf:extend] ∘∘∘ ch2 node: {cn2}/{len(o2Chain.avnodes)}")				
							# ∘ these new node :: loops are the 'additions' to this old chain to become the new chain
							loop = ch2Node.loop
										
							kf_field = changedNode.loop.killingField.field
							kf_seen = changedNode.loop.killingField.seen						
							
							if loop in kf_seen:
								if loop not in kf_field:
									kf_field.add(loop)
									kfAddedLoops.append((kf_field, loop))
							else:
								kf_seen.add(loop)
								kfAddedLoops.append((kf_seen, loop))
					
				# assert changedNode.loop not in kf_field
				
		return kfAddedLoops
				
		
	def fixCollapseBack(kfAddedLoops):
		for kfset, l in kfAddedLoops:
			kfset.remove(l)
			
	
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
			
