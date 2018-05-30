class Loop (object):
	
	def __init__(self, index):
		self.index = index
		self.nodes = set()
		self.availabled = True
		self.extended = False
		self.seen = False # for faded coloring, marker
		self.color = None
		self._root = None # cache for root()

		
	def root(self):
		if self._root is not None:
			return self._root
			
		self._root = ""
		nodes = list(self.nodes)
		for k in range(len(nodes[0].address)):
			for ni in range(1, len(nodes)):
				if nodes[ni].address[k] is not nodes[0].address[k]:
					return self._root
			self._root += nodes[0].address[k]
		return self._root # should never be needed
		

	def hasKernelNodes(self):
		return len([n for n in self.nodes if set(n.address[:-3]) == set(['0'])]) > 0
		
		
	def pseudo(self):
		return min([n.address for n in self.nodes])
		
	def __repr__(self):
		return '⟨loop:'+self.root()+'|'+':'.join(sorted([n.address[len(self._root):] for n in self.nodes]))+'⟩'
		
