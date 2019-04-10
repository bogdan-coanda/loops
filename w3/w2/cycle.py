class Cycle (object):
	
	__slots__ = ['index', 'address', 'nodes', 'px', 'py', 'chain']
			
	def __init__(self, index, address, nodes):
		self.index = index
		
		self.nodes = sorted(nodes, key = lambda n: n.address) # just in case we receive them in disorder or in a set
		for node in self.nodes:
			# everyone holds a link to its cycle center
			node.cycle = self
			node.cycleBrethren = [n for n in self.nodes if n != node]
		
		saddr = list(set([node.address[:-1] for node in self.nodes]))
		assert len(saddr) is 1 and saddr[0] == address, "invalid cycle address: " + str(saddr)
		self.address = address
		
		self.px = 0
		self.py = 0
		self.chain = None		
		
		
	def top_node(self):		
		return self.nodes[0]
		
		
	def bot_node(self):
		return self.nodes[-1]
				
				
	def __repr__(self):
		return f"⟨cycle:{self.index}@{self.address}|{'§' if self.chain else '∘'}⟩"
		
		
	def __lt__(self, other):
		return self.address < other.address			
