from state import State
from drawn import Drawn
from forest import Forest
from superperms import *
from node import Node
from cycle import Cycle
from loop import Loop
from link import Link
from functools import cmp_to_key
from jk import *


class Diagram (object):
	
	def __init__(self, N):
		# defaults to remember
		#self.k3cc = -2
		#self.k2cc = -1
		#self.k1cc = -1

		self.spClass = N
		
		self.generateGraph()
			
		self.arrowCount = [0, 0, 0]
		self.available_count = len(self.nodes)
		self.jkcc = 0	
		self.rx_looped_count = 0
				
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
		self.chainStarters = set([self.startNode])
		self.connectedChainPairs = set()
		self.skipped = 0		
		
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
		
		gn_address = [0] * (self.spClass-1)
		gn_perm = self.perms[0]
		gn_next = gn_perm
		gn_cc = 0
		gn_qq = 0
		gn_all = set()
		
		def genNode(lvl = 2):
			nonlocal gn_address, gn_perm, gn_next, gn_cc, gn_qq, gn_all
			
			if lvl == self.spClass + 1:
				gn_perm = gn_next
				node = Node(gn_perm, gn_qq, gn_cc, "".join([str(a) for a in gn_address]))
				self.nodes.append(node)
				self.cycles[-1].nodes.add(node)
				self.nodeByPerm[gn_perm] = node
				gn_all.add(gn_perm)
				gn_qq += 1
				gn_next = D1(gn_perm)
				return
				
			if lvl == self.spClass:
				self.cycles.append(Cycle(gn_cc, "".join([str(a) for a in gn_address[:-1]])))
				
			for q in range(0, lvl):
				gn_address[lvl - 2] = q
				genNode(lvl + 1)
				gn_next = DX(self.spClass - lvl + 1, gn_perm)

			if lvl == self.spClass:
				gn_cc += 1
													
		genNode()
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
		self.tryMakeAvailable(workedNodes)
		
		
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
	
	
	def tryMakeAvailable(self, nodes):
		for node in nodes:
			wasAvailabled = node.availabled
			node.availabled = self.checkAvailability(node)
			if node.availabled:
				if wasAvailabled == False:
					self.available_count += 1
				for bro in node.loopBrethren:
					bro.availabled = True
			else:
				if wasAvailabled == True:
					self.available_count -= 1
				for bro in node.loopBrethren:
					bro.availabled = False	

				
	def checkAvailability(self, curr):
		if curr.looped and (curr.prevLink == None 
				or curr.prevLink.type != 1 
				or curr.nextLink == None 
				or curr.nextLink.type != 1 
				or curr.nextLink.next.nextLink == None 
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
								
		'''
		if len(chains) > 2:
			if self.jkcc == 2674:
				# [~] this is just plain wrong
				print("[checkAv] failed for too many chains check | chains: " + " ".join([str(ch) for ch in chains]))
			return False

		if len(chains) == 2:
			a = chains.pop()
			b = chains.pop()
			if self.areConnected(a, b):
				if self.jkcc == 2674:
					print("[checkAv] failed for connected chains check: " + str(node.chainID) + " @ node: " + node.perm + "@" + node.address)
				return False
		'''		
		
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
		

	def measureNodes(self):

		self.drawn.reset()		

		#print("[measuring] chain starters: " + " ".join([node.perm for node in self.chainStarters]))

		self.drawn.chains = set()
		for startNode in sorted(self.chainStarters, key = cmp_to_key(
			lambda x, y: (0 if x.perm == y.perm else (1 if x.perm > y.perm else -1)) 
				if x.chainID == y.chainID else x.chainID - y.chainID)): # [!~] reversed chain id order
			#print("[measuring] conns: " + " ".join([str(chain) for chain in self.allConnectedChains(startNode.chainID)]))
			if len(self.drawn.chains.intersection(self.allConnectedChains(startNode.chainID))) > 0:
				#assert False, "Found connected start node, should happen at jk:10"
				continue
			self.drawn.chains.add(startNode.chainID)
			#print("[measuring] startNode: " + startNode.perm + "§" + str(startNode.chainID))
			node = startNode			
			while True:
				#assert node is not None
				if node.looped:
					if node.availabled and not node.extended:
						self.drawn.availables.append(node)
						#print("[measuring] av: " + " ".join([node.perm + "§" + str(node.chainID) for node in self.drawn.availables]))
				node = node.nextLink.next if node.nextLink != None else None
				if node == startNode:
					break
										
#		assert self.rx_looped_count == self.drawn.looped_count	
									
		for cycle in self.cycles:						
			av = 0
			lp = False
			lf = None
			for leaf in cycle.nodes:
				if leaf.looped: # if any node is looped, then the whole cycle is considered looped
					lp = True
					break
				if leaf.availabled and not leaf.seen:
					av += 1
					if av > 1:
						break
					lf = leaf # retain a leaf in case it's single
			if not lp: # if the cycle isn't looped in
				if av == 0: # if no node is reachable
					self.drawn.unreachable_cycles.add(cycle)
				elif av == 1: # if a single node is reachable
					bros = list(filter(lambda bro: bro.looped, lf.loopBrethren))
					if len(bros) == 1: # if a single bro is already looped
						self.drawn.singles.add(bros[0])
					elif len(bros) == 0: # if no bro is looped
						self.drawn.sparks.add(lf)						
															
##		if self.rx_looped_count > self.drawn.max_looped_count:
##			self.drawn.max_looped_count = self.rx_looped_count


	def extendLoop(self, node):
			
		if not node.looped:
			return self.addChain(node)
						
		# extend S2 if S1:S2:S3 to S1:[P:[S]x(ss-1)]x(ss-2):P:S3
			
		# extend only if available and not already extended	or seen
		if not node.availabled or node.extended or node.seen:
			return False
					
		##self.log("extending", "» node: " + str(node))					
					
		# mark as extended		
		node.extended = True
		node.ext_reset()
#		node.ext_looped_count = self.drawn.looped_count
				
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
				self.connectedChainPairs.update([(curr.chainID, next.chainID),(next.chainID, curr.chainID)])
				node.ext_connectedChains.append((curr.chainID, next.chainID))
				
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
				
		# append the last P path
		#assert last == 
		self.appendPath(curr, 2)#, "functional"
		node.ext_appendedLinks.append(curr.nextLink)
		node.ext_workedNodes.append(last)
		#self.log("extending", "worked last: " + str(last))

#		self.log("extending", "« deleted: " + str(len(node.ext_deletedLinks)))
#		self.log("extending", "« appended: " + str(len(node.ext_appendedLinks)))
#		self.log("extending", "« connected: " + str(len(node.ext_connectedChains)))
#		self.log("extending", "« worked: " + str(len(node.ext_workedNodes)))		
#		self.log("extending", "« chained: " + str(len(node.ext_chained)))
				
#		if self.jkcc >= 999999:
#			assert False, "jk: " + str(self.jkcc)		
			
		self.tryMakeAvailable(node.ext_workedNodes)		
		return True


	def collapseLoop(self, node):
		if node.chainStarter:
			self.removeChain(node)
						
		# collapse only if extended
		if not node.extended:
			return
		
#		self.log("collapsing", "» node: " + str(node))
	
		# mark as not extended
		node.extended = False		
#		node.coll_reset()
								
		for link in node.ext_appendedLinks:
			self.deletePath(link.node)
			
		for link in node.ext_deletedLinks:
			self.appendPath(link.node, link.type)
			
		for n in node.ext_chained:
			n.chainID = 0
			
		for pair in node.ext_connectedChains:
			self.connectedChainPairs.difference_update([pair, pair[::-1]])
						
		self.tryMakeAvailable(node.ext_workedNodes)						
		

	def addChain(self, node):
		
		# extend only if available and not already extended	or seen
		if not node.availabled or node.extended or node.seen:
#			assert False, "[addChain] refusing to add chain for node: " + str(node)
			return False
						
#		self.log("adding chain", "» node: " + str(node))
						
		# mark as extended
		node.looped = True
		node.extended = True
		node.chainStarter = True
		self.chainAutoInc += 1
		node.chainID = self.chainAutoInc
		self.chainStarters.add(node)
	
		# add the last node to bases
		workedNodes = set()		
		workedNodes.add(node)
		
		# append extended path
		curr = node
		for j in range(self.spClass - 1):
			next = self.appendPath(curr, 2)
			next.chainID = self.chainAutoInc
			curr = next
			workedNodes.add(curr)
				
			for i in range(self.spClass - 1):
				next = self.appendPath(curr, 1)
				next.chainID = self.chainAutoInc
				curr = next
				workedNodes.add(curr)
		
		self.tryMakeAvailable(workedNodes)				
		return True


	def removeChain(self, node):
#		self.log("removing chain", "» node: " + str(node))
		self.chainStarters.remove(node)
		node.chainID = 0
		node.chainStarter = False
		node.extended = False
		node.looped = False

		workedNodes = set()
		workedNodes.add(node)
		
		curr = node
		while True:
			curr.chainID = 0
			curr = self.deletePath(curr)
			workedNodes.add(curr)
			if curr == node:
				break		

		self.tryMakeAvailable(workedNodes)


	def log(self, mark, text, forced = False):
		if False: # forced or "lvl:" in mark: # False: #mark == "appending" or mark == "deleting" or mark == "extending" or mark == "collapsing" or mark == "adding chain" or mark == "removing chain" or self.jkcc == -19: # or (("connecting" in text or mark == "extending") and self.jkcc <= 45)  and "014253" in text) or self.jkcc in [169, 169] or:
			print("["+str(self.jkcc)+"]["+mark+"] " + text)

if __name__ == "__main__":
	'''
	diagram = Diagram(5)
	print()
	perm = diagram.perms[int(len(diagram.perms) / 2)]
	print("target: " + perm)
	print("pid: " + str(diagram.pids[perm]) + " | perm: " + diagram.perms[diagram.pids[perm]])
	node = diagram.nodeByPerm[perm]	
	print("links:\n" + "\n".join([str(y) + " » " + node.links[y].next.perm for y in range(1, diagram.spClass)]))
	print("cycle: " + str(node.cycleIndex) + "\n" + "\n".join([n.perm for n in node.cycle.nodes]))
	print("---")
	diagram.measureNodes()
	diagram.extendLoop(diagram.drawn.availables[0])
	diagram.measureNodes()
	diagram.extendLoop(diagram.drawn.availables[0])
	diagram.measureNodes()
	print("===")
	'''
	diagram = Diagram(6)
	diagram.startTime = time()
	diagram.sols = []
	
	# with open('sols.'+str(diagram.spClass)+".pkl", 'wb') as outfile:
	# 	pickle.dump(diagram.sols, outfile, 0)

	with open('sols.'+str(diagram.spClass)+".pkl", 'rb') as infile:
		diagram.knowns = pickle.load(infile)
		
	for i in range(len(diagram.knowns)):
		if type(diagram.knowns[i]) is tuple:
			diagram.knowns[i] = Sol(diagram.knowns[i][0], diagram.knowns[i][1], [Step(step[0], step[1], step[2], 0, step[3]) for step in diagram.knowns[i][2]], diagram.knowns[i][3])
			
	print("knowns: " + str(len(diagram.knowns)))
			
	jk(diagram)
	print("---")
	
