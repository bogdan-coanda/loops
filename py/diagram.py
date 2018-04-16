from state import State
from drawn import Drawn
from forest import Forest
from superperms import *
from node import Node
from cycle import Cycle
from loop import Loop
from link import Link

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
		
		self.ss = State(self)
		self.drawn = Drawn(self)
		self.forest = Forest(self)
				
		self.generateKernel()

		self.solution = ""			
		self.jkcc = 0	
		self.eecc = 0
		self.RR = 1200
		self.mxlvl = 0
		self.auto = True
		self.cursive = True
		
		
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
			node.links = [None]
			for type in range(1, self.spClass):
				next = self.nodeByPerm[DX(type, node.perm)]
				link = Link(type, node, next)
				node.links.append(link)
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
		
		self.tryMakeAvailable(workedNodes)
		
		
	def appendPath(self, curr, type):
		assert curr.nextLink == None and curr.links[type].next.looped == False	
		next = curr.links[type].next
		next.looped = True		
		curr.nextLink = next.prevLink = curr.links[type]
		return curr.nextLink.next


	def deletePath(self, curr):
		assert curr.nextLink != None and curr.nextLink.next.looped == True
		next = curr.nextLink.next			
		next.looped = False
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
		return (len([bro for bro in curr.loopBrethren if bro.looped]) + (1 if curr.looped else 0)) <= 1


	def measureNodes(self):

		self.drawn.reset()		
												
		node = self.startNode
		while node != None:
			if node.looped:
				self.drawn.looped_count += 1	
				if node.availabled and not node.extended:
					self.drawn.availables.append(node)
			node = node.nextLink.next if node.nextLink != None else None
									
		for cycle in self.cycles:						
			av = 0
			lp = False
			lf = None
			for leaf in cycle.nodes:
				if leaf.looped: # if any node is looped, then the whole cycle is considered looped
						lp = True
				if leaf.availabled:
						av += 1
						lf = leaf # retain a leaf in case it's single
			if not lp:
				if av == 0:
					self.drawn.unreachable_cycle_count += 1
				elif av == 1:
					bros = list(filter(lambda bro: bro.looped, lf.loopBrethren))
					if len(bros) == 1:
						self.drawn.singles.add(bros[0])
		
		if self.drawn.looped_count > self.drawn.max_looped_count:
			self.drawn.max_looped_count = self.drawn.looped_count


	def extendLoop(self, node):
		# extend S2 if S1:S2:S3 to S1:[P:[S]x(ss-1)]x(ss-2):P:S3
		
		# extend only if available and not already extended	
		if not node.availabled or node.extended or node.seen:
			return False
		
		# mark as extended
		node.extended = True
		
		# add the last node to bases
		# delete S2
		assert node.links[1] == node.nextLink
		last = self.deletePath(node)
		
		workedNodes = set()		
		workedNodes.add(node)
				
		# append extended path
		curr = node
		for j in range(self.spClass - 2):
			next = self.appendPath(curr, 2)
			curr = next
			workedNodes.add(curr)
				
			for i in range(self.spClass - 1):
				next = self.appendPath(curr, 1)
				curr = next
				workedNodes.add(curr)
				
		# append the last P path
		next = self.appendPath(curr, 2)
		workedNodes.add(last)

		self.tryMakeAvailable(workedNodes)		
		return True


	def collapseLoop(self, node):
		# collapse only if extended
		if not node.extended:
			return
	
		# mark as not extended
		node.extended = False
		
		# remove available nodes for the soon to be collapsed extension  
		last = node.links[1].next
	
		workedNodes = set()
	
		# remove extended path
		curr = node
		next = None
		while curr != last:
			next = self.deletePath(curr)
			workedNodes.add(curr)
			curr = next
				
		# add the replacement S path
		assert last == self.appendPath(node, 1)
		workedNodes.add(last)
		
		# for all base nodes, if they can be availabled, do it
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
	
