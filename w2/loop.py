from extension_result import *
import itertools


class Loop (object):
	
	__slots__ = [
		'index', 'nodes', '_firstAddress',
		'available', 'extended', 'extension_result',
		'ktype', 'ktype_radialIndex',
		'tuple',
		'sols'
	]
	
			
	def __init__(self, index):
		self.index = index
		self.nodes = None # comes as a pre-ordered list, we just shuffle it to start at the smallest address
		self.available = True
		self.extended = False
		self.extension_result = ExtensionResult()

		# @generateLoops
		self.ktype = None
		self.ktype_radialIndex = None
		
		# @walk
		self.tuple = None 
		self.sols = []
								

	def setNodes(self, nodes):
		firstNode = sorted(nodes, key = lambda n: n.address)[0]
		firstIndex = nodes.index(firstNode)
		self.nodes = nodes[firstIndex:] + nodes[:firstIndex]
		self._firstAddress = self.nodes[0].address

		
	def firstNode(self):
		return self.nodes[0]
		
	def firstAddress(self):
		return self._firstAddress

				
	def __repr__(self):
		return f"⟨loop:[{color_string(self.ktype)}:{self.ktype_radialIndex}]:{self.firstAddress()}|{'Av' if self.available else ''}{'Ex' if self.extended else ''}⟩"

	def __lt__(self, other):
		return self._firstAddress < other._firstAddress		
						
						
	def adjacentLoops(self):
		return [node.links[1].next.links[1].next.prevs[2].node.loop for node in self.nodes]
		
	def chain(self):
		return self.nodes[0].cycle.chain
		
	def label(self):
		return f"⟨{color_string(self.ktype)}:{str(self.ktype_radialIndex)}⟩"
		
		
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
	elif ktype is 7:
		return "black"				
	else:
		return "«·??·»"
