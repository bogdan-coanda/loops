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
					self.appendPath(linkType, curr, next)
					curr = next
					workedNodes.add(curr)

				for k in range(self.k1cc):				
					next = curr.links[1].next
					linkType = 1
					self.appendPath(linkType, curr, next)
					curr = next
					workedNodes.add(curr)

				next = curr.links[2].next
				linkType = 2
			
			next = curr.links[3].next
			linkType = 3
		
		for node in workedNodes:			
			column = int(node.cycleIndex / (self.spClass - 1)) # 0-3
			row = node.cycleIndex % (self.spClass - 1) # 0-4
			if column + row == self.spClass - 2: # (0,4);(1,3);(2,2);(3,1) == 4
				node.seedType = 0 # 0
			else:
				node.seedType = column + 1 # 1-4

		self.tryMakeAvailable(workedNodes)
		
		
	def appendPath(self, type, curr, next):
		next.looped = True

		curr.nextNode = next
		next.prevNode = curr	
	
		curr.nextLink = next.prevLink = curr.links[type]


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
		if curr.looped and (curr.prevLink == None or curr.prevLink.type != 1 or curr.nextNode == None or curr.nextLink.type != 1 or curr.nextNode.nextNode == None or curr.nextNode.nextLink.type != 1):
			return False
		'''			
		curr.prevLink == null
		|| curr.prevLink.ctype != 1 
		|| curr.nextNode == null 
		|| curr.nextLink.ctype != 1 
		|| curr.nextNode.nextNode == null 
		|| curr.nextNode.nextLink.ctype != 1))			
			'''
		return (len([bro for bro in curr.loopBrethren if bro.looped]) + (1 if curr.looped else 0)) <= 1





				
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
