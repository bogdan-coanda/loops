class Cycle (object):
	
	__slots__ = ['index', 'address', 'nodes', 'available_loops_count', 'px', 'py', 'chained_by_count', 'isKernel', 'marker', 'readdress']
	
	def __init__(self, index, address, px, py):
		self.index = index
		self.address = address
		self.nodes = set() # late init
		self.available_loops_count = 0
		self.px = px
		self.py = py
		self.chained_by_count = 0
		self.isKernel = False
		self.marker = None
		self.readdress = None
		
		
	def __repr__(self):
		return "⟨cycle:"+str(self.index)+"@"+self.address+"|"+str(self.available_loops_count)+"⟩"
					
					
	def avnode(self):		
		nodes = sorted(self.nodes, key = lambda n: n.address)
		rc = [node for node in nodes if node.loop.availabled]
		return rc[0] if len(rc) > 0 else nodes[0]
		
					
	def chk(self):
		assert len([n for n in self.nodes if n.loop.availabled and not n.loop.seen]) is self.available_loops_count and len([n for n in self.nodes if n.loop.availabled and not n.loop.seen]) is self.chained_by_count
				
