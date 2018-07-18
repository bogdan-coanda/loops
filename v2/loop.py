class Loop (object):
	
	__slots__ = ['index', 'nodes', 'availabled', 'extended', 'seen', '_root', '_type', '_pseudo', '_psnode', 'head', 'utype']
	
	def __init__(self, index):
		self.index = index
		self.nodes = None # ordered list
		self.availabled = True
		self.extended = False
		self.seen = False # for faded coloring, marker
		self._root = None # cache for root()
		self._type = None # cache for type()
		self._pseudo = None # cache for pseudo()
		self.head = None # first node from sorted nodes list
		self.utype = None
		self._psnode = None

		
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
		
	
	def type(self):
		if self._type is None:
			self._type = len(self.pseudo()) - len(self.root())
		return self._type
		

	def hasKernelNodes(self):
		return len([n for n in self.nodes if set(n.address[:-3]) == set(['0'])]) > 0
		
		
	def pseudo(self):
		if self._pseudo is None:
			self._pseudo = min([n.address for n in self.nodes])
		return self._pseudo


	def psnode(self):
		if self._psnode is None:
			self._psnode = sorted(self.nodes, key = lambda n: n.address)[0]
		return self._psnode		
		
	
	def chnode(self):
		chnodes = [node for node in self.nodes if node.chainID is not None]
		return chnodes[0] if len(chnodes) is not 0 else list(self.nodes)[0]
		
	def __repr__(self):
		return '⟨loop:'+self.root()+'|'+':'.join([n.address[len(self._root):] for n in self.nodes])+'⟩'
		

	def __lt__(self, other):
		return self.head.address < other.head.address
		
