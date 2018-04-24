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
				self.cycles.append(Cycle(gn_cc))
				
			for q in range(0, lvl):
				gn_address[lvl - 2] = q
				genNode(lvl + 1)
				gn_next = DX(self.spClass - lvl + 1, gn_perm)

			if lvl == self.spClass:
				gn_cc += 1
													
		genNode()
		assert len(gn_all) == len(self.perms)
				
				
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

		assert len(self.nodes) == len(self.perms)
		assert len(self.nodes) / self.spClass == len(self.cycles)
		assert len(self.nodes) / (self.spClass-1) == len(self.loops)		
		
		
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
		
		assert self.startNode == self.appendPath(curr, linkType)
		self.tryMakeAvailable(workedNodes)
		
		
	def appendPath(self, curr, type):
#		assert curr.nextLink == None and curr.links[type].next.looped == False	
		#print("[appending] path type: " + str(type) + " from: " + str(curr.perm) + " | to: " + str(curr.links[type].next.perm))
		next = curr.links[type].next
		next.looped = True		
		curr.nextLink = next.prevLink = curr.links[type]
		if curr.perm == "041532":
			print("«»")
		return curr.nextLink.next


	def deletePath(self, curr):
#		assert curr.nextLink != None and curr.nextLink.next.looped == True
		#print("[deleting] path type: " + str(curr.nextLink.type) + " from: " + str(curr.perm) + " | to: " + str(curr.nextLink.next.perm))
		next = curr.nextLink.next			
		next.looped = False
		next.extended = False
		curr.nextLink = next.prevLink = None		
		if curr.perm == "041532":
			print("»«")
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
		if curr.perm == "423510":
			print("here")
		if curr.looped and (curr.prevLink == None 
				or curr.prevLink.type != 1 
				or curr.nextLink == None 
				or curr.nextLink.type != 1 
				or curr.nextLink.next.nextLink == None 
				or curr.nextLink.next.nextLink.type != 1):
			return False
						
		#print("[checkAv] curr: " + curr.perm + " | loop nodes: " + " ".join([node.perm for node in curr.loop.nodes if node.looped]))
		
		chains = set()
		# for every looped current loop node
		for node in [node for node in curr.loop.nodes if node.looped]:				
			if node.chainID in chains:
				#print("[checkAv] failed for same chain check: " + str(node.chainID))
				return False # check if we see the same chainID twice
			else:
				chains.add(node.chainID)
		
		if len(chains) > 2:
			print("[checkAv] failed for too many chains check")
			#assert False, "jk: " + str(self.jkcc) + " | conns: " + " ".join([str(chain) for chain in chains])
			return False

		if len(chains) == 2:
			a = chains.pop()
			b = chains.pop()
			if self.areConnected(a, b):
				#print("[checkAv] failed for connected chains check: " + str(node.chainID) + " @ node: " + node.perm + "@" + node.address)
				#assert False, "jk: " + str(self.jkcc) + " | conns: " + " ".join([str(chain) for chain in chains])
				return False
				
		#print("[checkAv] passed for chains: " + " ".join([str(chainID) for chainID in chains]))
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

		seen = set()
		for startNode in sorted(self.chainStarters, key = cmp_to_key(
			lambda x, y: (0 if x.perm == y.perm else (1 if x.perm > y.perm else -1)) 
				if x.chainID == y.chainID else y.chainID - x.chainID)): # [~] reversed chain id order
			#print("[measuring] seen: " + " ".join([str(chain) for chain in seen]) + " | conns: " + " ".join([str(chain) for chain in self.allConnectedChains(startNode.chainID)]))
			if len(seen.intersection(self.allConnectedChains(startNode.chainID))) > 0:
				#assert False, "Found connected start node, should happen at jk:10"
				continue
			seen.add(startNode.chainID)
			#print("[measuring] startNode: " + startNode.perm + "§" + str(startNode.chainID))
			node = startNode			
			while True:
				assert node is not None
				if node.looped:
					self.drawn.looped_count += 1	
					if node.availabled and not node.extended:
						self.drawn.availables.append(node)
						#print("[measuring] av: " + " ".join([node.perm + "§" + str(node.chainID) for node in self.drawn.availables]))
				node = node.nextLink.next if node.nextLink != None else None
				if node.perm == "041532":
					print("measured »« " + str(node.nextLink))
				if node == startNode:
					break
										
			for cycle in self.cycles:						
				av = 0
				lp = False
				lf = None
				for leaf in cycle.nodes:
					if leaf.looped: # if any node is looped, then the whole cycle is considered looped
							lp = True
					if leaf.availabled and not leaf.seen:
							av += 1
							lf = leaf # retain a leaf in case it's single
				if not lp: # if the cycle isn't looped in
					if av == 0: # if no node is reachable
						self.drawn.unreachable_cycle_count += 1
					elif av == 1: # if a single node is reachable
						bros = list(filter(lambda bro: bro.looped, lf.loopBrethren))
						if len(bros) == 1: # if a single bro is already looped
							self.drawn.singles.add(bros[0])
						elif len(bros) == 0: # if no bro is looped
							self.drawn.sparks.add(lf)						
															
		if self.drawn.looped_count > self.drawn.max_looped_count:
			self.drawn.max_looped_count = self.drawn.looped_count


	def extendLoop(self, node):
			
		if not node.looped:
			return self.addChain(node)
						
		# extend S2 if S1:S2:S3 to S1:[P:[S]x(ss-1)]x(ss-2):P:S3
			
		# extend only if available and not already extended	or seen
		if not node.availabled or node.extended or node.seen:
			return False
					
		print("[extending] node: " + str(node))
		
		if node.perm == "423510":
			print("here")
					
					
		# mark as extended
		node.extended = True
		
		# delete S2
#		assert node.links[1] == node.nextLink
		last = self.deletePath(node)
		
		# add the last node to bases
		workedNodes = set()		
		workedNodes.add(node)
				
		# append extended path
		curr = node
		for j in range(self.spClass - 2):
			next = curr.links[2].next
			#print("[extending] next@d2: " + next.perm + " | looped: " + str(next.looped) + " | in chain: " + str(next.chainID))
			
			assert not next.looped or next.chainID != curr.chainID, "Trying to extend into the same chain - [~] should? check if the chains are connected instead of same"
			if next.looped:
				assert next.prevLink.type == 1 and next.nextLink.type == 1 and next.prevLink.node.prevLink.type == 1, "Invalid extension entrypoint into different chain"
				prev = next.prevLink.node
				assert next == self.deletePath(next.prevLink.node), "functional"
				assert next == self.appendPath(curr, 2), "functional"				
				# connect these chains together
				print("[extending] connecting chains " + curr.perm + "§" + str(curr.chainID) + " » " + next.perm + "§" + str(next.chainID))
				self.connectedChainPairs.update([(curr.chainID, next.chainID),(next.chainID, curr.chainID)])
				# [old] jump straight to the end of this cycle, as it's looped by the other chain
				# curr = prev
				# walk all the way along the path to 'work' all the nodes in the other cycle, up to the end of this cycle
				while curr != prev:
					workedNodes.add(curr)
					curr = curr.nextLink.next
				
				#assert False, "jk: " + str(self.jkcc)
				
			else: # normal, empty chain				
				next = self.appendPath(curr, 2)
				next.chainID = node.chainID
				curr = next
				workedNodes.add(curr)
					
				for i in range(self.spClass - 1):
					#print("[extending] next@d1: " + curr.links[1].next.perm + " | looped: " + str(curr.links[1].next.looped) + " | in chain: " + str(curr.links[1].next.chainID))
					next = self.appendPath(curr, 1)
					next.chainID = node.chainID
					curr = next
					workedNodes.add(curr)
				
		# append the last P path
		assert last == self.appendPath(curr, 2)
		workedNodes.add(last)

		if self.jkcc >= 9999:
			assert False, "jk: " + str(self.jkcc)		
			
		self.tryMakeAvailable(workedNodes)		
		return True


	def collapseLoop(self, node):
		if node.chainStarter:
			self.removeChain(node)
						
		# collapse only if extended
		if not node.extended:
			return
	
		# mark as not extended
		node.extended = False
		
		last = node.links[1].next
	
		# remove available nodes for the soon to be collapsed extension  
		workedNodes = set()
	
		# remove extended path
		curr = node
		next = None
		while curr != last:
			workedNodes.add(curr)
			next = self.deletePath(curr)
			#print("[collapsing] next: " + next.perm)						
			
			if node.chainID != next.chainID:
				print("[collapsing] unchained: " + str(node.chainID) + " | " + str(next.chainID))
				self.connectedChainPairs.difference_update([(node.chainID, next.chainID), (next.chainID, node.chainID)])
				prev = next.prevs[1].node # !!!§§§
				#print("[collapsing] prev: " + prev.perm)
				curr = next
				while curr != prev:
					workedNodes.add(curr)
					#print("[collapsing] curr: " + curr.perm)
					curr = curr.nextLink.next				
				next = self.deletePath(prev)
				print("[collapsing] deleted link from " + prev.perm + " to " + next.perm)
				self.appendPath(prev, 1)
				print("[collapsing] appended link from " + prev.perm + " to " + prev.nextLink.next.perm)
				
			#assert node.chainID == next.chainID, "BD between " + curr.perm + " and " + next.perm
			# need to undo what extendLoop into another chain did, including plugging back in the S1 link in the other chain, and including disconnecting the two chains
			workedNodes.add(curr)
			if next != last: # the last node is the extended one from its own chain
				next.chainID = 0
			curr = next
			#print("[collapsing] curr: " + curr.perm)			
				
		# add the replacement S path
		assert last == self.appendPath(node, 1)
		workedNodes.add(last)
		
		# for all base nodes, if they can be availabled, do it
		self.tryMakeAvailable(workedNodes)


	def addChain(self, node):
		
		# extend only if available and not already extended	or seen
		if not node.availabled or node.extended or node.seen:
			return False
						
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
		self.chainStarters.remove(node)
		node.chainID = 0
		node.chainStarter = False
		node.extended = False
		node.looped = False

		workedNodes = set()
		workedNodes.add(node)
		
		curr = node
		next = node.nextLink.next
		while next != node:
			next.chainID = 0
			self.deletePath(curr)
			curr = next
			workedNodes.add(curr)
			next = next.nextLink.next

		self.tryMakeAvailable(workedNodes)


if __name__ == "__main__":
	
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
	
	diagram = Diagram(6)
	diagram.startTime = time()
	diagram.sols = []
	
	# with open('sols.'+str(diagram.spClass)+".pkl", 'wb') as outfile:
	# 	pickle.dump(diagram.sols, outfile, 0)

	with open('sols.'+str(diagram.spClass)+".pkl", 'rb') as infile:
		diagram.knowns = pickle.load(infile)
		
	for i in range(len(diagram.knowns)):
		if type(diagram.knowns[i]) is tuple:
			diagram.knowns[i] = Sol(diagram.knowns[i][0], diagram.knowns[i][1], [Step(step[0], step[1], step[2], 0, step[3]) for step in diagram.knowns[i][2]], diagram.knowns[i][3], diagram.knowns[i][4])

	print("knowns: " + str(len(diagram.knowns)))
			
	jk(diagram)
	print("---")
	
