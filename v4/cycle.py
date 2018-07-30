class Cycle (object):
	
	__slots__ = ['index', 'address', 'nodes', 'px', 'py', 'isKernel', 'chain', 'marker']
	
	def __init__(self, index, address, px, py):
		self.index = index
		self.address = address
		self.nodes = set() # late init
		self.px = px
		self.py = py
		self.isKernel = False
		self.chain = None
		self.marker = None


	def avnode(self):		
		nodes = sorted(self.nodes, key = lambda n: n.address)
		rc = [node for node in nodes if node.loop.availabled]
		return rc[0] if len(rc) > 0 else nodes[0]
		
				
	def __repr__(self):
		return "⟨cycle:"+str(self.index)+"@"+self.address+"|"+str(self.available_loops_count)+"§"+str(self.chain)+"⟩"
		
		
	def __lt__(self, other):
		return self.address < other.address	
		
