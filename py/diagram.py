from state import State
from drawn import Drawn
from forest import Forest
from superperms import *
from node import Node
from cycle import Cycle

class Diagram (object):
	
	def __init__(self, N):
		# defaults to remember
		#self.k3cc = -2
		#self.k2cc = -1
		#self.k1cc = -1

		self.spClass = N
		
		self.generateGraph()
		
		self.startPerm = self.perms[0]	
		self.startNode = self.nodeByPerm[self.startPerm]

		self.solution = ""
		self.mode = "LOOP"

		self.arrowCount = [0, 0, 0]
		self.available_count = len(self.nodes)
			
		self.jkcc = 0	
		self.eecc = 0
		self.RR = 1200
		self.mxlvl = 0
		self.auto = True
		self.cursive = True
		
		self.ss = State(self)
		self.drawn = Drawn(self)
		self.forest = Forest(self)
				
		for node in self.nodes:
			node.looped = False
			node.extended = False
			node.nextNode = None
			node.prevNode = None
			node.nextLink = None
			node.prevLink = None
			node.suivant = False
			node.dessus = False
			node.backed = False
			node.marked = False

			# all normal nodes are available at start for extending as they're unblemished
			node.availabled = True
										
			# everyone holds a link to its cycle center
			node.cycle = self.cycles[node.cc]
				
			# [2] each normal node holds links to its (N-2)*N potential nodes (nodes looped in when extended from this node)
			node.potentials = set()
		
			# [3] each normal node holds links to its (N-2) base nodes (nodes that when extended, loop in this node as well among others)
			node.bases = set();

	 		# [4] each normal node is CURRENTLY potentialed by up to (N-2) base nodes
			node.potentialedBy = set()	
		
			# [5] each node has a loop index (1-based as 0 means unparsed) for the loop it extends into
			node.loopIndex = 0
				
			# [7] each node holds links to its N-2 brethren (nodes that extend into the same loop)
			node.loopBrethren = set()
				
			node.isSeed = False


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
				self.cycles[-1].nodes.append(node)
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
			node.link = [0]
			for y in range(1, self.spClass):
				next = self.nodeByPerm[DX(y, node.perm)]
				node.link.append(next)
				self.links[y].append((node,next))
				
if __name__ == "__main__":
	
	diagram = Diagram(5)
	
	perm = diagram.perms[int(len(diagram.perms) / 2)]
	print("target: " + perm)
	print("pid: " + str(diagram.pids[perm]) + " | perm: " + diagram.perms[diagram.pids[perm]])
	node = diagram.nodeByPerm[perm]	
	print("links:\n" + "\n".join([str(y) + " » " + node.link[y].perm for y in range(1, diagram.spClass)]))
	print("cycled:\n" + "\n".join([n.perm for n in node.cycle.nodes]))
	print("---")
