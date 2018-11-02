from extension_result import *
import itertools


class Loop (object):
	
	__slots__ = ['index', 'nodes', 'availabled', 'extended', '_root', 'head', 'extension_result', 'seen', '_firstNode', 'ktype', 'ktype_columnIndex', 'ktype_radialIndex', '_killingField']
	
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
		# @generateLoops
		self.ktype = None
		self.ktype_columnIndex = None
		self.ktype_radialIndex = None
		
		
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
		return '⟨loop:['+color_string(self.ktype)+":"+str(self.ktype_radialIndex)+"]:"+self.firstAddress()+'|'+('Av' if self.availabled else '')+('Ex' if self.extended else '')+"⟩"#self.root()+'|'+':'.join([n.address[len(self._root):] for n in self.nodes])
		
	def addr(self):
		return self.nodes[0].address
		
	def firstPerm(self):
		return sorted([node.perm for node in self.nodes])[0]
		
	def firstAddress(self):
		return sorted([node.address for node in self.nodes])[0]
		
	def adjacentLoops(self):
		return [node.links[1].next.links[1].next.prevs[2].node.loop for node in self.nodes]
		
	def killingField(self):
		# gather around all avloops for chains tied to this loop (including multiples)
		all_avloops = list(itertools.chain(*[n.cycle.chain.avloops for n in self.nodes]))
		
		# one of each avloop instance
		unique_avloops = set(all_avloops)
		
		# remove an avloop instance for each unique
		for avloop in unique_avloops:
			all_avloops.remove(avloop)
	
		# what remains are multiples of some avloops 
		self._killingField = set(all_avloops)
		
		# remove self
		self._killingField.remove(self)
		
		return self._killingField 
		
	def chain(self):
		return self.nodes[0].cycle.chain
		
def color_string(ktype):
	if ktype is 0:
		return "blue"
	elif ktype is 1:
		return "green"
	elif ktype is 2:
		return "yellow"
	elif ktype is 3:
		return "orange"
	elif ktype is 4:
		return "red"
	elif ktype is 5:
		return "violet"
	elif ktype is 6:
		return "indigo"		
	else:
		return "«·??·»"
		
						
