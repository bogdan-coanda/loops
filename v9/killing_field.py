from common import tstr, input2
from time import time
import itertools


class KillingField (object):
	
	__slots__ = ['loop', 'field', 'seen']
	
	regenCount = 0
	vts =[0, 0, 0, 0]
	vtc = 0
	dts = [0, 0]
	dtc = 0
	e1 = 0
	e2 = 0
	as1 = 0
	af1 = 0
	as2 = 0
	af2 = 0
	
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
		
		# oldField = self.field
		# oldSeen = self.seen
			
		# tx = time()
		self.field, self.seen = KillingField.calculateKillingFieldSet(self.loop)		
		
		# if extendedLoop:					
		# KillingField.regenCount += 1			
				
		# KillingField.vts[0] += (time() - tx)
			
			# tx = time()
			# kf = KillingField.calculateKillingFieldSet2(self.loop)
			# KillingField.vts[1] += (time() - tx)		
			# assert self.field == set(kf) and len(self.field) == len(kf)
			# 
			# tx = time()
			# kf_all, kf_uni = KillingField.calculateKillingFieldSet3(self.loop)
			# KillingField.vts[2] += (time() - tx)						
			# assert self.field == kf_all
			# 
			# tx = time()
			# kf_field, kf_seen = KillingField.calculateKillingFieldSet4(self.loop, extendedLoop, oldSeen, oldField)
			# KillingField.vts[3] += (time() - tx)						
			# assert self.field == kf_field and self.seen == kf_seen, f"{self.field.difference(kf_field)} | {kf_field.difference(self.field)} ∘ {self.seen.difference(kf_seen)} | {kf_seen.difference(self.seen)}"
												
		# if KillingField.vtc % 1000 == 0:
		# 	print(f"[vtc:{KillingField.vtc}] vts: " + ' | '.join([f"{i}: {tstr(KillingField.vts[i])}" for i in range(len(KillingField.vts))]))
		# KillingField.vtc += 1
		
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
						
			# «self_loop» is one of extendedLoop.extension_result.new_chain.avnodes::loop
						
			changedNode = [node for node in self_loop.nodes if node.chain == extendedLoop.extension_result.new_chain]
			assert len(changedNode) == 1
			changedNode = changedNode[0]
			
			# «changedNode» is the corresponding loop::node of extendedLoop.extension_result.new_chain.avnodes
			
			oldChain = [chain for chain in extendedLoop.extension_result.affected_chains if changedNode in chain.avnodes]
			assert len(oldChain) == 1
			oldChain = oldChain[0]
			
			# «oldChain» is the corresponding prior chain of the changedNode/self_loop
			
			
			#if extendedLoop.firstAddress() == '0000054':
				#print(f"[kf4] changed node: {changedNode} | oldChain: {oldChain} | new chain nodes not in old chain: {len([node for node in extendedLoop.extension_result.new_chain.avnodes if node not in oldChain.avnodes])} | new chain nodes not in old chain but in oldSeen: {len([node for node in extendedLoop.extension_result.new_chain.avnodes if node not in oldChain.avnodes and node.loop in oldSeen])}")
						
			kf_field = set([loop for loop in oldField if loop.availabled])
			kf_seen = set([loop for loop in oldSeen if loop.availabled])
			for node in extendedLoop.extension_result.new_chain.avnodes:
				#if extendedLoop.firstAddress() == '0000054':
					#print(f"[kf4] checking {node} with {node.loop}")
				if node not in oldChain.avnodes:
					#if extendedLoop.firstAddress() == '0000054':
						#print(f"[kf4] ⇒ not in old chain")
					loop = node.loop
					if loop in kf_seen:
						#if extendedLoop.firstAddress() == '0000054':
							#print(f"[kf4] ⇒ in seen")
						if loop not in kf_field:
							#if extendedLoop.firstAddress() == '0000054':
								#print(f"[kf4] ⇒ not in field")
							kf_field.add(loop)
					else:
						#if extendedLoop.firstAddress() == '0000054':
							#print(f"[kf4] ⇒ not in seen")
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
				
	def fixExtendLoop(diagram, extendedLoop):

		# first version
		kfPreviousFields = []
		# twigs = {}		
				
		def fxel1():		
			for changedNode in extendedLoop.extension_result.new_chain.avnodes:
				kfPreviousFields.append((changedNode.loop.killingField, changedNode.loop.killingField.field, changedNode.loop.killingField.seen))			
																																												
				# find loops with just multiple appearances - these nodes would get killed when extending this (self) loop, as they tie to at least two of the self's new connected chains
				seen = set() # unique seen once loops
				dups = set() # unique seen more loops
		
				# gather around all avloops for chains tied to this loop (including multiples)				
				for n in changedNode.loop.nodes:
					for ncn in n.chain.avnodes:
						
						KillingField.e1 += 1
						loop = ncn.loop
						
						if loop in seen:
							if loop not in dups:								
								KillingField.af1 += 1
								dups.add(loop)								
						else:
							KillingField.as1 += 1
							seen.add(loop)
				
				# remove self
				dups.remove(changedNode.loop)
				KillingField.af1 += 1
				
				# return killing field							
				changedNode.loop.killingField.field = dups
				changedNode.loop.killingField.seen = seen
				# twigs[changedNode] = ((changedNode.loop.killingField.field, changedNode.loop.killingField.seen))		


		tx = time()
		fxel1()				
		d1 = time() - tx

		# revert				
		KillingField.assessAllLoops(diagram)
		
		for kf, field, seen in reversed(kfPreviousFields):
			kf.field = field
			kf.seen = seen										
									
		# second version		
		kfAddedLoops = [] 
		
		def fxel2():
			
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
								KillingField.e2 += 1
								loop = ch2Node.loop
											
								kf_field = changedNode.loop.killingField.field
								kf_seen = changedNode.loop.killingField.seen						
								
								if loop in kf_seen:
									#print(f"[kf:extend] ∘∘∘ ⇒ in seen({len(kf_seen)})")
									if loop not in kf_field:
									# assert loop not in kf_field									
										# print(f"[kf:extend] ∘∘∘ ⇒⇒ not in [field({len(kf_field)})] // adding")
										kf_field.add(loop)
										KillingField.af2 += 1
										kfAddedLoops.append((kf_field, loop))
									# else:
									# 	print(f"[kf:extend] ∘∘∘ ⇒⇒ in [field({len(kf_field)})] // not adding !!!")									
								else:
									#print(f"[kf:extend] ∘∘∘ ⇒ not in [seen({len(kf_seen)})] // adding")
									KillingField.as2 += 1
									kf_seen.add(loop)
									kfAddedLoops.append((kf_seen, loop))
						
					# assert changedNode.loop not in kf_field
					# assert twigs[changedNode][0] == changedNode.loop.killingField.field		
							
		
		tx = time()		
		fxel2()															
		d2 = time() - tx
		
		
		KillingField.assessAllLoops(diagram)
				
		KillingField.dts[0] += d1
		KillingField.dts[1] += d2
		KillingField.dtc += 1

		if KillingField.dtc % 10 == 0:		
			print(f"[kf:fixExtend][dtc:{KillingField.dtc}] d1: {tstr(KillingField.dts[0])} | d2: {tstr(KillingField.dts[1])} | e: {KillingField.e1} / {KillingField.e2} | as: {KillingField.as1} / {KillingField.as2} | af: {KillingField.af1} / {KillingField.af2}")
			KillingField.e1 = 0
			KillingField.e2 = 0
			KillingField.af1 = 0
			KillingField.as1 = 0
			KillingField.af2 = 0
			KillingField.as2 = 0			

		return kfAddedLoops
		
		
	def fixCollapseBack(kfAddedLoops): #, kfRemovedLoops):
		# revert to previous killing fields (mandatory recalcs before removes)
		# for kf, field, seen in reversed(kfPreviousFields):
		# 	kf.field = field
		# 	kf.seen = seen
		# 
		# for kf, l in kfRemovedLoops:
		# 	kf.add(l)		
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
			
