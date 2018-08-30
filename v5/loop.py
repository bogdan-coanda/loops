from extension_result import *

class Loop (object):
	
	__slots__ = ['index', 'nodes', 'availabled', 'extended', '_root', 'head', 'extension_result', 'seen', '_firstNode']
	
	def __init__(self, index):
		self.index = index
		self.nodes = None # ordered list
		self.availabled = True
		self.extended = False
		self._root = None # cache for root()
		self.head = None # first node from sorted nodes list
		self.extension_result = ExtensionResult()
		self.seen = False # should only be used by search methods and not by internal checks
		self._firstNode = None
		
		
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
		
	def firstNode(self):
		if self._firstNode is not None:
			return self._firstNode
			
		self._firstNode = sorted(self.nodes, key = lambda n: n.address)[0]
		return self._firstNode
		
	def __repr__(self):
		return '⟨loop:'+self.root()+'|'+':'.join([n.address[len(self._root):] for n in self.nodes])+'|'+('Av' if self.availabled else '')+('Ex' if self.extended else '')+'⟩'
		
	def addr(self):
		return self.nodes[0].address
