from superperms import *
from common import *
from cycle import Cycle
from node import Node
from link import Link
from loop import Loop
from chain import Chain
from uicanvas import show
import itertools
import math
from time import time


class Diagram (object):
	
	
	def __init__(self, N, kernelSize=1):
		
		self.spClass = N
		self.kernelSize = kernelSize
		self.chainAutoInc = -1
				
		self.generateGraph()
																																					
		self.startPerm = self.perms[0]	
		self.startNode = self.nodeByPerm[self.startPerm]									

		# subsets		
		self.pointers = []
		
		# every cycle has its own chain at start
		for cycle in self.cycles:

			# create new chain
			self.chainAutoInc += 1
			new_chain = Chain(self.chainAutoInc)
																			
			# move cycle
			cycle.chain = new_chain
			new_chain.cycles.append(cycle)								
			new_chain.avloops = set([node.loop for node in cycle.nodes])
																																					
			# a new chain is born
			self.chains.add(new_chain)
								
				
		if self.kernelSize > 0:
			self.generateKernel()
			
		self.cleanexCount = 0
									
		
	def generateGraph(self):
				
		self.perms = ["".join([str(p) for p in perm]) for perm in Permutator(list(range(self.spClass))).results]
		self.pids = {}
		for i in range(len(self.perms)):
			self.pids[self.perms[i]] = i		
		
		self.generateNodes()
		self.generateLinks()
		self.generateLoops()		
		
		
	def generateNodes(self):
		
		self.nodes = []
		self.cycles = []
		self.nodeByPerm = {}
		self.nodeByAddress = {}
		self.cycleByAddress = {}
		self.chains = set()
		
		gn_address = [0] * (self.spClass-1)
		gn_perm = self.perms[0]
		gn_next = gn_perm
		gn_cc = 0
		gn_qq = 0
		gn_all = set()
		
		DM = 32
		RH = 8

		if self.spClass is 8:
			xydelta = [
				(0, DM*(self.spClass-2)*(self.spClass-1)), 
				(DM*((self.spClass-3)*(self.spClass-2)-1), 0), 
				(DM*(self.spClass-1), 0), 
				(0, DM*(self.spClass)), 
				(DM, 0), 
				(0, DM), 
				(0, 0)]				
		elif self.spClass is 7:
			xydelta = [
				(DM*((self.spClass-3)*(self.spClass-2)-1), 0), 
				(DM*(self.spClass-1), 0), 
				(0, DM*self.spClass), 
				(DM, 0), 
				(0, DM), 
				(0, 0)]
		elif self.spClass is 6:
			xydelta = [
				(0, DM*self.spClass), 
				(DM*(self.spClass-1), 0), 
				(DM, 0), 
				(0, DM), 
				(0, 0)]
		elif self.spClass is 5:
			xydelta = [
				(DM*(self.spClass-1), 0), 
				(DM, 0), 
				(0, DM), 
				(0, 0)]				
		elif self.spClass is 4:
			xydelta = [
				(DM, 0), 
				(0, DM), 
				(0, 0)]				
						
		def genNode(lvl = 2, qx = DM, qy = DM):
			nonlocal gn_address, gn_perm, gn_next, gn_cc, gn_qq, gn_all
			
			if lvl == self.spClass + 1:
				gn_perm = gn_next
				qLast = gn_address[-1]
				dx = math.floor(RH*math.cos((2*qLast - (self.spClass-1)) * math.pi / self.spClass))
				dy = math.floor(RH*math.sin((2*qLast - (self.spClass-1)) * math.pi / self.spClass))				
				
				node = Node(gn_perm, gn_qq, gn_cc, "".join([str(a) for a in gn_address]), qx+dx, qy+dy)
				self.nodes.append(node)
				self.cycles[-1].nodes.add(node)
				self.nodeByPerm[gn_perm] = node
				self.nodeByAddress[node.address] = node
				gn_all.add(gn_perm)
				gn_qq += 1
				gn_next = D1(gn_perm)
				return
				
			if lvl == self.spClass:
				cycle = Cycle(gn_cc, "".join([str(a) for a in gn_address[:-1]]), qx, qy)				
				#cycle.available_loops_count = self.spClass
				self.cycles.append(cycle)
				self.cycleByAddress[cycle.address] = cycle
				 
				
			for q in range(0, lvl):
				gn_address[lvl - 2] = q
				genNode(lvl + 1, qx + q * xydelta[lvl-2][0], qy + q * xydelta[lvl-2][1])
				gn_next = DX(self.spClass - lvl + 1, gn_perm)

			if lvl == self.spClass:
				gn_cc += 1
																	
		genNode()
		max([node.px for node in self.nodes])
		self.W = max([cycle.px for cycle in self.cycles]) + DM
		self.H = max([cycle.py for cycle in self.cycles]) + DM		
		#print("generated nodes | WxH: " + str(self.W) + "x" + str(self.H))
		#assert len(gn_all) == len(self.perms)		
		
		
	def generateLinks(self):
		
		self.links = [[]] * (self.spClass)
		
		for node in self.nodes:
			node.links = [None]*self.spClass
			node.prevs = [None]*self.spClass
		
		nc = 0
		for node in self.nodes:
			#if nc % 10000 is 0:
				#print("[links] " + str(nc) + "/" + str(len(self.nodes)))
			for type in range(1, self.spClass):
				next = self.nodeByPerm[DX(type, node.perm)]
				link = Link(type, node, next)
				node.links[type] = link
				next.prevs[type] = link
				self.links[type].append(link)
			nc += 1
			
		#print("generated links")
		
				
	def generateLoops(self):
		
		self.loops = []
		lix = -1 # current loop index
		
		for node in self.nodes:			
			
			# everyone holds a link to its cycle center
			node.cycle = self.cycles[node.cycleIndex]
			node.cycleBrethren = [n for n in node.cycle.nodes if n != node]
			
			# if this node has yet to be included in a loop
			if node.loop is None:
				# adapt current loop details to a new loop
				lix += 1				
				# create a new loop
				self.loops.append(Loop(lix))
										
				# collect loop nodes
				loopNodes = [node]
				next = node			
				# for each cycle in the loop extension
				for j in range(self.spClass-2):
					# make the jump into the cycle
					next = next.links[2].next
					# jump the 1-paths												
					for i in range(self.spClass-1):
						next = next.links[1].next
					# the last node is a loop extender
					loopNodes.append(next)
				
				# update loop & nodes details
				self.loops[lix].head = sorted(loopNodes, key = lambda n: (n.address[-1], n.address[-2]))[0]
				self.loops[lix].nodes = loopNodes[loopNodes.index(self.loops[lix].head):] + loopNodes[:loopNodes.index(self.loops[lix].head)]
				for ln in loopNodes:
					ln.loop = self.loops[lix]
					lnindex = loopNodes.index(ln)
					ln.loopBrethren = loopNodes[lnindex+1:] + loopNodes[:lnindex]

		#print("generated loops")								
				
	
	def generateKernel(self):
				
		affected_chains = []
		bases = []
		
		node = self.startNode.prevs[1].node
		
		for kern_index in range(self.kernelSize):			
			for column_index in range(self.spClass - 2):
			
				#print("[kernel] k: " + str(kern_index) + " | c: " + str(column_index) + " | node: " + str(node))	
				node.loop.extended = True
			
				for n in node.loop.nodes:				
					affected_chains.append(n.cycle.chain)
					n.cycle.isKernel = True

				# connect last bro
				node.loopBrethren[-1].nextLink = node.loopBrethren[-1].nextLink.next.prevLink = (
					node.loopBrethren[-1].links[3] if column_index != self.spClass - 3 else (node.loopBrethren[-1].links[4] if kern_index != self.kernelSize - 1 else Link(4, node.loopBrethren[-1], self.startNode))
				)

				node = node.loopBrethren[-1].nextLink.next.prevs[1].node																		
																							
		self.chainAutoInc = -1
		new_chain, affected_loops, touched_chains = self.makeChain(affected_chains)
				

	### ~~~ extensions ~~~ ###	
				
		
	def extendLoop(self, loop):		
		#print("[extend] loop: " + str(loop))
			
		##assert set(list(itertools.chain(*[chain.avloops for chain in diagram.chains]))) == set([loop for loop in diagram.loops if loop.availabled and len([node for node in loop.nodes if node.cycle.chain])])
		#assert set(list(itertools.chain(*[chain.loops for chain in diagram.chains]))) == set([loop for loop in diagram.loops if loop.availabled and len([node for node in loop if node.cycle.chain)])
			
		# assert/return false if not we can't or already did extend		
		if loop.availabled is False or loop.extended is True:
			return False
			
		loop.extended = True
						
		affected_chains = []
		
		for node in loop.nodes:
			affected_chains.append(node.cycle.chain)
		
		new_chain, affected_loops, touched_chains = self.makeChain(affected_chains)				
		
		#for node in loop.nodes:
			#assert not node.links[1].next.loop.availabled and not node.prevs[1].node.loop.availabled, "broken extension neighbours!!!"
			
		#for lp in self.loops:
			#if lp.availabled:
				#assert self.checkAvailability(lp), "broken checked loops"
				
		#assert len([node for node in loop.nodes if node.links[1].next.loop.availabled or node.prevs[1].node.loop.availabled]) is 0, "broken extension neighbours!!!"		
		loop.extension_result = (new_chain, affected_loops, affected_chains, touched_chains)

		##assert set(list(itertools.chain(*[chain.avloops for chain in diagram.chains]))) == set([loop for loop in diagram.loops if loop.availabled and len([n for n in loop.nodes if n.cycle.chain])])
		
		return True
		
		
	def cleanExtension(self, extended_loop):
			
		self.cleanexCount += 1
			
		ice = 0	
		while True:			
			for chain in self.chains:
				if len(chain.avloops) is 0:
					return 
			
			avcount = 0
			potentcount = 0
			deadcount = 0
			for loop in self.loops:
				if loop.availabled:			
					avcount += 1
					
					Δ = loop.extension_result[3].intersection(extended_loop.extension_result[3]) if loop.extension_result else []
					hasPotential = loop.extension_result is None or len(Δ) 
					old_extension_result = loop.extension_result or [[]]*4
					if hasPotential:
						potentcount += 1
					
					if (self.cleanexCount == 97 and avcount >= 17 and potentcount >= 11) or (self.cleanexCount == 96 and (ice == 4 or ice == 0) and self.nodeByAddress['122300'] in loop.nodes):

						self.pointers = extended_loop.nodes
						show(self)
						input("[cleanex:"+str(ice)+"@"+str(self.cleanexCount)+"] - before | extended_loop: " + str(extended_loop))
												
						self.pointers = itertools.chain(*[chain.cycles for chain in extended_loop.extension_result[3]])
						show(self)
						input("[cleanex:"+str(ice)+"@"+str(self.cleanexCount)+"] - before | extended_loop touched chains: " + str(extended_loop))

						self.pointers = itertools.chain(*[chain.cycles for chain in loop.extension_result[3]])
						show(self)
						input("[cleanex:"+str(ice)+"@"+str(self.cleanexCount)+"] - before | previous extension result for: " + str(loop))
											
						self.pointers = loop.nodes
						show(self)
						input("[cleanex:"+str(ice)+"@"+str(self.cleanexCount)+"] - before | will extend loop: " + str(loop))											

					# 	self.pointers = self.nodeByAddress['121410'].loop.nodes
					# 	show(self)
					# 	input("@97 - before | will kill loop at: " + str(self.nodeByAddress['121410']))
					# 
					# if self.nodeByAddress['122300'] in loop.nodes:
					# 	print('cleanex: '+str(self.cleanexCount)+" | ice: "+str(ice)+" for "+str(loop))																									
					# 	if self.cleanexCount == 96 and ice == 4:
					# 		show(self)
					# 		input("@96 - before extending loop at: " + str(self.nodeByAddress['121410']))							
																																																																																							
					assert self.extendLoop(loop)
					
					if (self.cleanexCount == 97 and avcount >= 17 and potentcount >= 11) or (self.cleanexCount == 96 and ice == 4 and self.nodeByAddress['122300'] in loop.nodes):	
						show(self)
						input("[cleanex:"+str(ice)+"@"+str(self.cleanexCount)+"] - after extending: " + str(loop))
						
					valid = True
					for touched_chain in loop.extension_result[3]:
						if len(touched_chain.avloops) is 0:
							valid = False
							assert hasPotential, "no potential !?"
							break
					self.collapseBack(loop)
					if not valid:
						if self.nodeByAddress['121410'] in loop.nodes:
							show(self)
							input("[cleanex:"+str(ice)+"@"+str(self.cleanexCount)+"] will set unavailable: " + str(loop) + " | cc: " + str([node.cycle for node in loop.nodes]))
						self.setLoopUnavailabled(loop)
						deadcount += 1
						extended_loop.extension_result[1].append(loop)
						extended_loop.extension_result[3].update([node.cycle.chain for node in loop.nodes])
			
			print("[cleanex:"+str(ice)+"@"+str(self.cleanexCount)+"] tried " + str(avcount) + " available loops | with " + str(potentcount) + " potentials ("+str(potentcount*100/avcount)+"%) ⇒ " + str(deadcount) + " cleaned")
			if deadcount is 0:
				return
			ice += 1
								
																						
	def collapseBack(self, loop):	
		#print("[collapse] loop: " + str(loop))				
		self.breakChain(*(loop.extension_result))
		#loop.extension_result = None
		loop.extended = False
																
	
	def checkAvailability(self, loop):
		for i in range(1, len(loop.nodes)):
			ichain = loop.nodes[i].cycle.chain
			for j in range(0, i):
				jchain = loop.nodes[j].cycle.chain
				# if the loop would link back to the same chain, or to a different colored (marked) chain
				if ichain is jchain:
					return False
		return True
						
										
	def setLoopAvailabled(self, loop):
		#assert loop.availabled is False
		loop.availabled = True
		for node in loop.nodes:
			cycle = node.cycle
			cycle.chain.avloops.add(loop)
		
		
	def setLoopUnavailabled(self, loop):
		#assert loop.availabled is True
		loop.availabled = False
		for node in loop.nodes:
			if loop in node.cycle.chain.avloops: # [~] why would the loop not be here ? got removed twice ? got debugged twice over already and proven correct ?
				node.cycle.chain.avloops.remove(loop)
																		
																											
	def makeChain(self, affected_chains):

		# create new chain
		self.chainAutoInc += 1
		new_chain = Chain(self.chainAutoInc)
		affected_loops = []
		touched_chains = set(affected_chains)
		
		# for each old chain
		for index, old_chain in enumerate(affected_chains):
							
			# move cycles to new chain
			for cycle in old_chain.cycles:
				cycle.chain = new_chain
				new_chain.cycles.append(cycle)
										
			# kill chain
			#print("[makeChain] removing: " + str(old_chain))
			self.chains.remove(old_chain)			
			
		# move/remember loops												
		# for each old chain
		for old_chain in affected_chains:												
			for loop in old_chain.avloops:
				if loop.availabled:
					if not self.checkAvailability(loop):
						# remember erased loop
						self.setLoopUnavailabled(loop)
						touched_chains.update([node.cycle.chain for node in loop.nodes])
						affected_loops.append(loop)
					else:
						# move still available loop to new chain
						new_chain.avloops.add(loop)
																																					
		# a new chain is born
		#print("[makeChain] adding: " + str(new_chain))
		self.chains.add(new_chain)
		touched_chains.remove(new_chain)
		return (new_chain, affected_loops, touched_chains)
		
		
	def breakChain(self, new_chain, affected_loops, affected_chains, touched_chains): # touched_chains is unused here
		#print("[breakChain] removing: " + str(new_chain))
		self.chains.remove(new_chain)
		for chain in affected_chains:
			#print("[breakChain] adding: " + str(chain))
			self.chains.add(chain)
			for cycle in chain.cycles:
				cycle.chain = chain
		for loop in affected_loops:
			self.setLoopAvailabled(loop)
					
					
	### ~~~ pointers ~~~ ###																																																				
				
			
	def pointToAddressTuple(self, address):
		self.pointers = list(self.nodeByAddress[address].tuple)


	def superperm(self, start_addr, end_addr):
		curr = self.nodeByAddress[start_addr]
		SP = curr.perm
		#print("SP: " + str(SP))		
		while True:
			nextLink = curr.nextLink if curr.nextLink else (curr.links[2] if curr.loop.extended else curr.links[1])	
			curr = nextLink.next
			if curr.address == start_addr:
				break
			SP += curr.perm[-nextLink.type:]
			if curr.address == end_addr:
				curr.nextLink = Link(0, curr, self.nodeByAddress[start_addr])
				break
		#print("SP: " + str(SP))
		return SP
		#for node in self.nodes:
			#assert node.perm in SP



if __name__ == "__main__":
		
	diagram = Diagram(7, 4)								
	
	diagram.extendLoop(diagram.nodeByAddress['000001'].loop)
	#diagram.extendLoop(diagram.nodeByAddress['123001'].loop)
	# diagram.collapseBack(diagram.nodeByAddress['123001'].loop)
	# diagram.collapseBack(diagram.nodeByAddress['000001'].loop)
	
	show(diagram)

	diagram.pointers = []
	affected_nodes = list(itertools.chain(*[loop.nodes for loop in diagram.nodeByAddress['000001'].loop.extension_result[1]]))
	for cycle in diagram.cycles:
		if cycle.chain in diagram.nodeByAddress['000001'].loop.extension_result[3]:
			diagram.pointers += [node for node in cycle.nodes if node in affected_nodes]
	show(diagram)

	diagram.pointers = []	
	for cycle in diagram.cycles:
		if cycle.chain in diagram.nodeByAddress['000001'].loop.extension_result[3]:
			diagram.pointers.append(cycle)
	show(diagram)	
