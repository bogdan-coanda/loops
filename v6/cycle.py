from common import unitRoots
import math


class Cycle (object):
	
	__slots__ = ['index', 'address', 'nodes', 'px', 'py', 'isKernel', 'chain', 'marker', 'inner_roots', 'outer_roots']
	
	def __init__(self, index, address, px, py):
		self.index = index
		self.address = address
		self.nodes = [] # late init
		self.px = px
		self.py = py
		self.isKernel = False
		self.chain = None
		self.marker = None
		self.inner_roots = None
		self.outer_roots = None


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
		self.inner_roots = unitRoots(root_count, radius, -3+0.5+unit_angle_fraction_offset)
		outer_radius = 2/math.sqrt(3)*radius
		self.outer_roots = unitRoots(root_count, outer_radius, -2+unit_angle_fraction_offset)
		
		if centerX:
			self.px = centerX
		if centerY:
			self.py = centerY
		
		for i in range(len(self.nodes)):
			self.nodes[i].px = self.px + self.inner_roots[i][0]
			self.nodes[i].py = self.py + self.inner_roots[i][1]
		
