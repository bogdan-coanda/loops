from state import State
from drawn import Drawn
from forest import Forest
from superperms import *
from node import Node
from center import Center

class Diagram (object):
	
	def __init__(self, N):
		# defaults to remember
		#self.k3cc = -2
		#self.k2cc = -1
		#self.k1cc = -1

		self.spClass = N
		
		self.startPerm = self.generateGraph()
	
		self.startNode = None
		self.solution = ""
		self.mode = "LOOP"
		self.currentColor = "yellow"
		self.currentColorHue = 60
		self.arrowCount = [0, 0, 0]
		self.available_count = 0
			
		self.jkcc = 0	
		self.eecc = 0
		self.RR = 1200
		self.mxlvl = 0
		self.auto = True
		self.cursive = True
		self.ss = State(self)

		self.drawn = Drawn(self)

		self.forest = Forest(self)

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
		self.centers = []
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
				self.nodeByPerm[gn_perm] = node
				gn_all.add(gn_perm)
				self.nodes.append(node)
				gn_qq += 1
				gn_next = D1(gn_perm)
				return
				
			if lvl == self.spClass:
				self.centers.append(Center(gn_cc))
				
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
	
	print("---")
