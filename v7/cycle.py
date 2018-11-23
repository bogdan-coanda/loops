from common import unitRoots
import math


class Cycle (object):
	
	__slots__ = ['index', 'address', 'nodes', 'px', 'py', 'isKernel', 'chain']
	
	def __init__(self, index, address, nodes):
		self.index = index
		
		self.nodes = nodes
		for node in self.nodes:
			# everyone holds a link to its cycle center
			node.cycle = self
			node.cycleBrethren = [n for n in self.nodes if n != node]
		
		saddr = list(set([node.address[:-1] for node in self.nodes]))
		assert len(saddr) is 1 and saddr[0] == address, "invalid cycle address: " + str(saddr)
		self.address = address
		
		self.px = 0
		self.py = 0
		self.isKernel = False
		self.chain = None
		# [!unused!] self.inner_roots = None
		# [!unused!] self.outer_roots = None


	def avnode(self):		
		nodes = sorted(self.nodes, key = lambda n: n.address)
		rc = [node for node in nodes if node.loop.availabled]
		return rc[0] if len(rc) > 0 else nodes[0]
		
	def avnode_or_self(self):
		nodes = sorted(self.nodes, key = lambda n: n.address)
		rc = [node for node in nodes if node.loop.availabled]
		return rc[0] if len(rc) > 0 else self		
				
	def __repr__(self):
		return "⟨cycle:"+str(self.index)+"@"+self.address+"§"+str(self.chain)+"⟩"
		
		
	def __lt__(self, other):
		return self.address < other.address	
		
	
	def setCoords(self, radius, unit_angle_fraction_offset, centerX = None, centerY = None):
		root_count = len(self.nodes)
		# [!unused!] self.inner_roots = unitRoots(root_count, radius, -3+0.5+unit_angle_fraction_offset)
		# [!unused!] outer_radius = 2/math.sqrt(3)*radius
		# [!unused!] self.outer_roots = unitRoots(root_count, outer_radius, -2+unit_angle_fraction_offset)
		
		if centerX:
			self.px = centerX
		if centerY:
			self.py = centerY
		
		inner_roots = unitRoots(root_count, radius, -3+0.5+unit_angle_fraction_offset)
		
		for i in range(len(self.nodes)):
			self.nodes[i].px = self.px + inner_roots[i][0]
			self.nodes[i].py = self.py + inner_roots[i][1]
		
