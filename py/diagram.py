from state import State
from drawn import Drawn
from forest import Forest
from superperms import *
from node import Node
from cycle import Cycle
from loop import Loop
from link import Link
from functools import cmp_to_key
from common import *
from jk import *
from time import time
import pickle
import math


class Diagram (object):
	
	def __init__(self, N, knownID = None):
		# defaults to remember
		#self.k3cc = -2
		#self.k2cc = -1
		#self.k1cc = -1

		self.spClass = N
		self.knownID = knownID
		
		self.generateGraph()
			
		self.arrowCount = [0, 0, 0]
		self.jkcc = 0	
		self.rx_looped_count = 0

		self.mx_unreachable_cycles = set()
		self.mx_singles = set()
		self.mx_sparks = set()
														
		# self.rx_availables = set() # should only contain nodes that are looped, loop.availabled and not loop.extended
														
		self.ss = State(self)
		self.drawn = Drawn(self)
		self.forest = Forest(self)
				
		self.generateKernel()

		self.solution = ""			
		self.eecc = 0
		self.RR = 1200
		self.mxlvl = 0
		self.auto = True
		self.cursive = True
		self.chainAutoInc = 0
		self.chainStarters = [self.startNode]
		self.chainColors = { 0: "#ffdd22" }
		self.connectedChainPairs = set()
		self.skipped = 0		
		self.cached_superperm = None
		self.cached_road = None
		self.road_is_walked = False
		self.cached_extender = None		
		self.startTime = time()
		self.C5 = "2".join(["1"*(self.spClass-1)]*(self.spClass-1))	

				
	def generateGraph(self):
		self.k3cc = self.spClass - 2
		self.k2cc = self.spClass - 1
		self.k1cc = self.spClass - 1
		
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
		
		def genNode(lvl = 2, qx = DM, qy = DM):
			nonlocal gn_address, gn_perm, gn_next, gn_cc, gn_qq, gn_all
			
			if lvl == self.spClass + 1:
				gn_perm = gn_next
				if self.spClass is 8:
					q8 = gn_address[-1]
					dx = math.floor(RH*math.cos((q8 - 3.5) * 2 * math.pi / 8))
					dy = math.floor(RH*math.sin((q8 - 3.5) * 2 * math.pi / 8))
				elif self.spClass is 7:
					q7 = gn_address[-1]
					dx = math.floor(RH*math.cos((q7 - 3) * 2 * math.pi / 7))
					dy = math.floor(RH*math.sin((q7 - 3) * 2 * math.pi / 7))
				elif self.spClass is 6:
					q6 = gn_address[-1]
					dx = math.floor(RH*math.cos((q6 - 2.5) * 2 * math.pi / 6))
					dy = math.floor(RH*math.sin((q6 - 2.5) * 2 * math.pi / 6))
				
				
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
				self.cycles.append(Cycle(gn_cc, "".join([str(a) for a in gn_address[:-1]]), qx, qy))
				self.cycles[-1].available_loops_count = self.spClass
				
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
		#assert len(gn_all) == len(self.perms)
				
				
	def generateLinks(self):
		
		self.links = [[]] * (self.spClass)
		
		for node in self.nodes:
			node.links = [None]*self.spClass
			node.prevs = [None]*self.spClass
		
		for node in self.nodes:
			for type in range(1, self.spClass):
				next = self.nodeByPerm[DX(type, node.perm)]
				link = Link(type, node, next)
				node.links[type] = link
				next.prevs[type] = link
				self.links[type].append(link)
				
				
	def generateLoops(self):
		self.loops = []
		lix = -1 # current loop index
		for node in self.nodes:			
			
			# everyone holds a link to its cycle center
			node.cycle = self.cycles[node.cycleIndex]
			node.cycleBrethren = [n for n in node.cycle.nodes if n != node]
			
			# if this node has yet to be included in a loop
			if node.loopIndex == -1:
				# adapt current loop details to a new loop
				lix += 1				
				self.loops.append(Loop(lix))
				# [5] this is the first node in the new loop
				node.loopIndex = lix
				node.loop = self.loops[lix]
				self.loops[lix].nodes.add(node)
						
			next = node
			
			# for each cycle in the loop extension
			for j in range(self.spClass-2):
				# make the jump into the cycle
				next = next.links[2].next
				
				# [2] potentials will be looped in if this node becomes availabled and then extended
				node.potentials.add(next)				
				
				# [3] bases will be unavailabled when this next node becomes looped in
				next.bases.add(node)
				
				# [4] all bases are available at start
				next.potentialedBy.add(node)
						
				for i in range(self.spClass-1):
					next = next.links[1].next
					# [2] potential as well
					node.potentials.add(next)
				
				# [7] the last node in the cycle is the one to make the jump, so we store it as a brethren of the current node
				node.loopBrethren.add(next)
				
				# [5] copy details from the first node in the current loop
				next.loopIndex = node.loopIndex		
				node.loop = self.loops[node.loopIndex]
				self.loops[node.loopIndex].nodes.add(node)

		#assert len(self.nodes) == len(self.perms)
		#assert len(self.nodes) / self.spClass == len(self.cycles)
		#assert len(self.nodes) / (self.spClass-1) == len(self.loops)		
		
		
	def generateKernel(self):
		self.startPerm = self.perms[0]	
		self.startNode = self.nodeByPerm[self.startPerm]									

		node = self.startNode				
		node.looped = True
		node.cycle.looped = True

		next = None
		curr = node
		
		workedNodes = set() 		
		workedNodes.add(node)
			
		linkType = 0
			
		for i in range(self.k3cc):
			for j in range(self.k2cc):
			
				if next != None:
					next = self.appendPath(curr, linkType)
					curr = next
					workedNodes.add(curr)
					curr.cycle.looped = True

				for k in range(self.k1cc):				
					linkType = 1
					next = self.appendPath(curr, linkType)
					
					curr = next
					workedNodes.add(curr)

				next = curr.links[2].next
				linkType = 2
			
			next = curr.links[3].next
			linkType = 3
		
		#assert self.startNode == 
		self.appendPath(curr, linkType)#, "functional"
		self.rx_unlooped_cycles = set([cycle for cycle in self.cycles if cycle.looped == False])
		#print("[rx_unlooped_cycles] after generate kernel: " + str(len(self.rx_unlooped_cycles)))
		self.tryMakeUnavailable(workedNodes)
		
		
	def loadKnowns(self):
		with open('sols.'+str(self.spClass)+".pkl", 'rb') as infile:
			self.knowns = pickle.load(infile)
			print("[diagram@"+tstr(time()-self.startTime)+"] loaded " + str(len(self.knowns)) + " known solutions found in " + str(self.knowns[-1].jkcc) + " steps | runtime: " + tstr(self.knowns[-1].tdiff))
		
		
	def generateDiagramForKnownID(self, knownID):
		known = self.knowns[knownID]
		𝒟 = Diagram(self.spClass, knownID)
		𝒟.startTime = self.startTime
		for step in known.state:
			𝒟.measureNodes(𝒟.startNode)
			node = 𝒟.nodeByPerm[step.perm]
			𝒟.extendLoop(node)
		return 𝒟

		
	def superperm(self):
		if self.cached_superperm == None:			
			node = self.startNode
			superperm = node.perm
			while node.nextLink.next != self.startNode:						
				node = node.nextLink.next
				superperm += node.perm[-(node.prevLink.type):]
			self.cached_superperm = superperm
			if self.knownID is not None and self.knownID % 1 == 0:			
				print("[diagram:"+str(self.knownID)+" @ "+tstr(time()-self.startTime)+"] generated superperm")
		return superperm
		
		
	def road(self):
		if self.cached_road == None:
			node = self.startNode
			road = str(self.startNode.prevLink.type)
			while node.nextLink.next != self.startNode:						
				node = node.nextLink.next
				road += str(node.prevLink.type)
			
			# reduce format	
			road = road.replace(self.C5, "§")
			road = road.replace("3", "-")
			road = road.replace("2", "|")	
			for i in range(5, 1, -1):
				road = road.replace("1"*i, str(i))
			
			walked = road
			# 'sort' to the first alphanumeric …
			parts = road.strip('-').split('-')
			halls = []
			for _ in range(len(parts)):
				parts = parts[1:] + [parts[0]]
				halls.append("-".join(parts))
				halls.append(halls[-1][::-1])
			road = '-'+sorted(halls)[0]			
										
			self.cached_road = road
			self.road_is_walked = road == walked
			if self.knownID is not None and self.knownID % 1000 == 0:			
				print("[diagram:"+str(self.knownID)+"@"+tstr(time()-self.startTime)+"] generated road: " + road)		
		return road
		
		
	def extender(self):
		if self.cached_extender == None:
			node = self.startNode
			extender = []
		
		def tryex(node):
			if node.nextLink.type == 1:
				return node.nextLink.next
			else:
				assert node.nextLink.type == 2	
				extender.append(node.perm)
				next = pushex(node.nextLink.next)
				assert node.links[1].next == next
				return next
			
		def pushex(node):
			for i in range(self.spClass - 2):
				for j in range(self.spClass - 1):
					
					node = tryex(node)
							
				assert node.nextLink.type == 2
				node = node.nextLink.next							
			return node
																
		for i in range(self.k3cc):
			for j in range(self.k2cc):
				for k in range(self.k1cc):				
								
					node = tryex(node)		
					
				assert (j == self.k2cc - 1 and node.nextLink.type == 3) or node.nextLink.type == 2
				node = node.nextLink.next
									
		self.cached_extender = extender
		if self.knownID is not None and self.knownID % 1000 == 0:			
			print("\n[diagram:"+str(self.knownID)+"@"+tstr(time()-self.startTime)+"] generated extender: " + " ".join([str(node) for node in extender]))		
		return extender
		
		
	def loadExtenders(self):
		with open('extenders.'+str(self.spClass)+".pkl", 'rb') as infile:	
			self.extenders = list(pickle.load(infile))
		self.extenders = [[self.nodeByPerm[perm] for perm in extender] for extender in self.extenders]
		print("Loaded "+str(len(self.extenders))+" extenders")		
		
								
	def appendPath(self, curr, type):
#		assert curr.nextLink == None # and curr.links[type].next.looped == False	
#		if self.jkcc <= 80 or "000000" in [curr.perm]: #, curr.links[type].next.perm]:
#			self.log("appending", "path type: " + str(type) + " from: " + str(curr) + " | to: " + str(curr.links[type].next))
		next = curr.links[type].next
		next.looped = True		
		self.rx_looped_count += 1
		curr.nextLink = next.prevLink = curr.links[type]
		return curr.nextLink.next


	def deletePath(self, curr):
#		assert curr.nextLink != None # and curr.nextLink.next.looped == True
#		if self.jkcc <= 80 or "000000" in [curr.perm]: #, curr.nextLink.next.perm]:
#			##self.log("deleting", "path type: " + str(curr.nextLink.type) + " from: " + str(curr) + " | to: " + str(curr.nextLink.next))
		next = curr.nextLink.next			
		next.looped = False
		self.rx_looped_count -= 1
		next.extended = False
		curr.nextLink = next.prevLink = None		
		return next
	
	
	def tryMakeUnavailable(self, nodes):
#		print("[makeAv] » » »\nnodes: " + " ".join([str(node) for node in nodes]))
		flp = set()
		
		for node in nodes:
			if node.loop.availabled:
				if not self.checkAvailability(node):
					node.loop.availabled = False
					for node in node.loop.nodes:
						node.cycle.available_loops_count -= 1						
					flp.add(node.loop)
		
		self.measureCycles()

#		print("[makeUn] called with " + str(len(nodes)) + " nodes => flp: " + str(len(flp)) + " | unreachables: " + str(len(self.mx_unreachable_cycles)) + " | singles: " + str(len(self.mx_singles)) + " | sparks: " + str(len(self.mx_sparks)))		
		return flp
				
				
	def makeAvailableAgain(self, node):
		for loop in node.ext_flp:
			loop.availabled = True
			for nn in loop.nodes:
				nn.cycle.available_loops_count += 1				

		self.measureCycles()		
				
#		print("[makeAv] called for " + str(node) + " => flp: " + str(len(node.ext_flp)) + " | unreachables: " + str(len(self.mx_unreachable_cycles)) + " | singles: " + str(len(self.mx_singles)) + " | sparks: " + str(len(self.mx_sparks)))
				
				
	def measureCycles(self):
		self.mx_unreachable_cycles.clear()
		self.mx_singles.clear()
		self.mx_sparks.clear()
		
		for cycle in self.rx_unlooped_cycles: #touched_cycles:
			if cycle.available_loops_count == 0: # if no loop is available
				self.mx_unreachable_cycles.add(cycle) # ⇒ the cycle is unreachable
			elif cycle.available_loops_count == 1: # if a single loop is available
				lf = [nn for nn in cycle.nodes if nn.loop.availabled][0] # get the cycle's available node
				bros = list(filter(lambda bro: bro.looped, lf.loopBrethren)) # get the node's looped bros
				if len(bros) == 1: # if a single bro is looped
					self.mx_singles.add(bros[0]) # ⇒ the cycle is singled 
				elif len(bros) == 0: # if no bro is looped
					self.mx_sparks.add(lf) # [~] sparks should contain loops, not one of their nodes

								
	def checkAvailability(self, curr):
		if curr.looped and (
				#curr.prevLink == None or 
				curr.prevLink.type != 1 
				#or curr.nextLink == None 
				or curr.nextLink.type != 1 
				#or curr.nextLink.next.nextLink == None 
				or curr.nextLink.next.nextLink.type != 1):
			return False
						
		##self.log("checkAv", "» curr: " + str(curr) + " | loop nodes: " + " ".join([str(node) for node in curr.loop.nodes if node.looped]))
		
		chains = set()
		# for every looped current loop node
		for node in [node for node in curr.loop.nodes if node.looped]:				
			if node.chainID in chains:
				##self.log("checkAv", "failed for same chain check: " + str(node.chainID))
				return False # check if we see the same chainID twice
			else:
				##self.log("checkAv", "adding " + str(node) + " to chains")
				chains.add(node.chainID)
		
		while len(chains) > 1:
			ch = chains.pop()
			if len(chains.intersection(self.allConnectedChains(ch))) > 0:
				##self.log("checkAv", "failed for connected chains check: " + str(node))
				return False
										
		##self.log("checkAv", "passed for chains: " + " ".join([str(chainID) for chainID in chains]))
		return True
		

	def allConnectedChains(self, chain):
		# returns an array flood filled from chain
		#print("[conns] pairs: " + " ".join([str(a) + ":" + str(b) for a,b in self.connectedChainPairs]))
		seen = set([chain])
		done = []
		while len(seen) > 0:
			ch = seen.pop()
			for a,b in self.connectedChainPairs:
				#print("[conns] a: " + str(a) + " | ch: " + str(ch) + " | b: " + str(b) + " | seen: " + " ".join([str(ch) for ch in seen]) + " | done: " + " ".join([str(ch) for ch in done]))
				if a == ch and b not in seen and b not in done:
					seen.add(b)
			done.append(ch)
		#print("[conns] chain: " + str(chain) + " | conns: " + " ".join([str(ch) for ch in done]))
		return done					


	def areConnected(self, chain1, chain2):
		return chain2 in self.allConnectedChains(chain1)
		

	def measureNodes(self, last_extended_node = None):
		#print("[measuring] » » » chain starters: " + " ".join([node.perm for node in self.chainStarters]))
	
		if last_extended_node is None:
			last_extended_node = self.startNode
		last_extended_node = self.startNode # [~] ignoring input
	
		self.drawn.reset()		

		if len(self.chainStarters) == 1:
			
			startNode = self.chainStarters[0]
			self.drawn.chains.add(startNode.chainID)			
			node = last_extended_node if startNode.chainID == 0 else startNode 			
			#if node != startNode:
				#print("[measuring] rewrote start node to: " + str(node) + " with index: " + str(startNode.index))
			while True:
				if node.loop.availabled and not node.extended:
					self.drawn.availables.append(node)
				node = node.nextLink.next
				if node == startNode:
					break
					
		else:	
								
			for startNode in self.chainStarters:
				if len(self.drawn.chains.intersection(self.allConnectedChains(startNode.chainID))) > 0:
					continue
				self.drawn.chains.add(startNode.chainID)
				node = last_extended_node if startNode.chainID == 0 else startNode			
				#if node != startNode:
					#print("[measuring] rewrote start node to: " + str(node) + " with index: " + str(startNode.index))
				while True:
					if node.loop.availabled and not node.extended:
						self.drawn.availables.append(node)
						#print("[measuring] av: " + " ".join([node.perm + "§" + str(node.chainID) for node in self.drawn.availables]))
					node = node.nextLink.next
					if node == startNode:
						break
																												
	# [~] real extend loop
	# assert loop is instance of Loop
	# extendNode
	# loop.extendedFrom - for collapseLoop
	def extendLoop(self, node):
			
		if not node.looped:
			return self.addChain(node)
						
		# extend S2 if S1:S2:S3 to S1:[P:[S]x(ss-1)]x(ss-2):P:S3
			
		# extend only if available and not already extended	or seen
		# [~] loops can be unavailabled from the jk inner loop
		if not node.loop.availabled or node.extended:
			return False
					
		#print("[extending] » » » node: " + str(node) + " with index: " + str(node.index))					
					
		# mark as extended		
		node.extended = True
		node.ext_reset()
				
		# delete S2
#		assert node.links[1] == node.nextLink
		node.ext_deletedLinks.append(node.nextLink)
		last = self.deletePath(node)
		
		# add the last node to bases
		node.ext_workedNodes.append(node)
						
		# append extended path
		curr = node
		for j in range(self.spClass - 2):
			next = curr.links[2].next
			###self.log("extending", "next@d2: " + str(next) + " | looped: " + str(next.looped) + " | in chain: " + str(next.chainID))
			
			#assert not next.looped or next.chainID != curr.chainID, "Trying to extend into the same chain - [~] should? check if the chains are connected instead of same"
			if next.looped:
				#assert next.prevLink.type == 1 and next.nextLink.type == 1 and next.prevLink.node.prevLink.type == 1, "Invalid extension entrypoint into different chain"
				prev = next.prevLink.node
				node.ext_deletedLinks.append(next.prevLink)
				#assert next == 
				self.deletePath(next.prevLink.node)#, "functional"
				#assert next == 
				self.appendPath(curr, 2)#, "functional"				
				node.ext_appendedLinks.append(curr.nextLink)
				# connect these chains together
				#self.log("extending", "connecting chains " + str(curr) + " » " + str(next))
				self.connectedChainPairs.update([(curr.chainID, next.chainID), (next.chainID, curr.chainID)])
				node.ext_connectedChains.append((curr.chainID, next.chainID))
				node.ext_connectedChains.append((next.chainID, curr.chainID))
				
				# [old] jump straight to the end of this cycle, as it's looped by the other chain
				# curr = prev
				# walk all the way along the path to 'work' all the nodes in the other cycle, up to the end of this cycle
				while curr != prev:
					node.ext_workedNodes.append(curr)
					#self.log("extending", "worked: " + str(curr))
					curr = curr.nextLink.next
				
				#assert False, "jk: " + str(self.jkcc)
				
			else: # normal, empty chain				
				next = self.appendPath(curr, 2)
				node.ext_appendedLinks.append(curr.nextLink)
				next.cycle.looped = True
				self.rx_unlooped_cycles.remove(next.cycle)
				node.ext_loopedCycles.append(next.cycle)
				#print("[rx_unlooped_cycles] during extend loop: removed " + str(next.cycle))				
				#self.log("extending", "normal jump " + str(curr) + " » " + str(next))
				next.chainID = node.chainID
				node.ext_chained.append(next)
				curr = next
				node.ext_workedNodes.append(curr)
				#self.log("extending", "worked: " + str(curr))
					
				for i in range(self.spClass - 1):
					#self.log("extending", "next@d1: " + str(curr.links[1].next) + " | looped: " + str(curr.links[1].next.looped) + " | in chain: " + str(curr.links[1].next.chainID))
					next = self.appendPath(curr, 1)
					node.ext_appendedLinks.append(curr.nextLink)
					next.chainID = node.chainID
					node.ext_chained.append(next)
					curr = next
					node.ext_workedNodes.append(curr)
					#self.log("extending", "worked: " + str(curr))
				
		#print("[rx_unlooped_cycles] after extend loop: " + str(len(self.rx_unlooped_cycles)))
				
		# append the last P path
		#assert last == 
		self.appendPath(curr, 2)#, "functional"
		node.ext_appendedLinks.append(curr.nextLink)
		node.ext_workedNodes.append(last)
		#self.log("extending", "worked last: " + str(last))
		
		#print("[extending] « deleted: " + str(len(node.ext_deletedLinks)))
		#print("[extending] « appended: " + str(len(node.ext_appendedLinks)))
		#print("[extending] « connected: " + str(len(node.ext_connectedChains)))
		#print("[extending] « worked: " + str(len(node.ext_workedNodes)))		
		#print("[extending] « chained: " + str(len(node.ext_chained)))
				
#		if self.jkcc >= 999999:999999:
#			assert False, "jk: " + str(self.jkcc)		
			
		node.ext_flp = self.tryMakeUnavailable(node.ext_workedNodes)
		#print("[extending] « avs: " + str(len(node.ext_flp)))
		return True


	def collapseLoop(self, node):
		if node.chainStarter:
			self.removeChain(node)
						
		# collapse only if extended
		if not node.extended:
			#print("[collapsing] » refusing unextended node: " + str(node))
			return
		
		#print("[collapsing] » node: " + str(node))
	
		# mark as not extended
		node.extended = False		
								
		for link in node.ext_appendedLinks:
			self.deletePath(link.node)
			
		for link in node.ext_deletedLinks:
			self.appendPath(link.node, link.type)
		
		for cycle in node.ext_loopedCycles:
			cycle.looped = False
			self.rx_unlooped_cycles.add(cycle)
			#print("[rx_unlooped_cycles] during collapse loop: " + str(cycle))
					
		#print("[rx_unlooped_cycles] after collapse loop: " + str(len(self.rx_unlooped_cycles)))			
					
		for n in node.ext_chained:
			n.chainID = 0
			
		for pair in node.ext_connectedChains:
			self.connectedChainPairs.difference_update([pair, pair[::-1]])
						
		self.makeAvailableAgain(node)
										

	def addChain(self, node):
		
		# extend only if available and not already extended	or seen
		if not node.loop.availabled or node.extended:
#			assert False, "[addChain] refusing to add chain for node: " + str(node)
			return False
						
#		self.log("adding chain", "» node: " + str(node))
						
		# mark as extended
		node.looped = True
		node.extended = True
		node.chainStarter = True
		self.chainAutoInc += 1
		node.chainID = self.chainAutoInc
		self.chainStarters.append(node)
		
		node.ext_reset()
	
		# add the last node to bases
		node.ext_workedNodes.append(node)
		
		# append extended path
		curr = node
		for j in range(self.spClass - 1):
			next = self.appendPath(curr, 2)
			node.ext_appendedLinks.append(curr.nextLink)
			next.cycle.looped = True
			self.rx_unlooped_cycles.remove(next.cycle)
			node.ext_loopedCycles.append(next.cycle)
			#print("[rx_unlooped_cycles] during add chain: " + str(next.cycle))
			next.chainID = self.chainAutoInc
			node.ext_chained.append(next)
			curr = next
			node.ext_workedNodes.append(curr)				
			
			for i in range(self.spClass - 1):
				next = self.appendPath(curr, 1)
				node.ext_appendedLinks.append(curr.nextLink)
				next.chainID = self.chainAutoInc
				node.ext_chained.append(next)
				curr = next
				node.ext_workedNodes.append(curr)						
				
		#print("[rx_unlooped_cycles] after add chain: " + str(len(self.rx_unlooped_cycles)))				
				
		node.ext_flp = self.tryMakeUnavailable(node.ext_workedNodes)
		return True


	def removeChain(self, node):
#		self.log("removing chain", "» node: " + str(node))
		self.chainStarters.pop() # [~] equals pop ?
		node.chainID = 0
		node.chainStarter = False
		node.extended = False
		node.looped = False
		
		for link in node.ext_appendedLinks:
			self.deletePath(link.node)
			
		for link in node.ext_deletedLinks:
			self.appendPath(link.node, link.type)
			
		for cycle in node.ext_loopedCycles:
			cycle.looped = False
			self.rx_unlooped_cycles.add(cycle)
			#print("[rx_unlooped_cycles] during remove chain: " + str(cycle))
			
		#print("[rx_unlooped_cycles] after remove chain: " + str(len(self.rx_unlooped_cycles)))
						
		for n in node.ext_chained:
			n.chainID = 0
	
		self.makeAvailableAgain(node)
				

	def log(self, mark, text, forced = False):
		if False: # forced or "lvl:" in mark: # False: #mark == "appending" or mark == "deleting" or mark == "extending" or mark == "collapsing" or mark == "adding chain" or mark == "removing chain" or self.jkcc == -19: # or (("connecting" in text or mark == "extending") and self.jkcc <= 45)  and "014253" in text) or self.jkcc in [169, 169] or:
			print("["+str(self.jkcc)+"]["+mark+"] " + text)

if __name__ == "__main__":
	from common import Step, Sol
	run()	
