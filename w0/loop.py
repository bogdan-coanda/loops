from extension_result import *
from killing_field import *
import itertools


class Loop (object):
	
	__slots__ = [
		'index', 'nodes', '_firstAddress',
		'availabled', 'extended', 'extension_result', 'seen', 
		'ktype', 'ktype_radialIndex',
		#'ktype_columnIndex'
		'killingField', 
		'tuple',
		'columnByKType']
	
			
	def __init__(self, index):
		self.index = index
		self.nodes = None # comes as a pre-ordered list, we just shuffle it to start at the smallest address
		self.availabled = True
		self.extended = False
		self.extension_result = ExtensionResult()
		self.seen = False # should only be used by search methods and not by internal checks
		# @generateLoops
		self.ktype = None
		self.ktype_radialIndex = None
		# @walk		
		self.tuple = None
		# @generateColumns for loops with ktype == 0 # contains columns for ktype > 1
		self.columnByKType = {}
		# killingField
		self.killingField = None
						

	def setNodes(self, nodes):
		firstNode = sorted(nodes, key = lambda n: n.address)[0]
		firstIndex = nodes.index(firstNode)
		self.nodes = nodes[firstIndex:] + nodes[:firstIndex]
		self._firstAddress = self.nodes[0].address

	def hasKernelNodes(self):
		return len([n for n in nodes if set(n.address[:-3]) == set(['0'])]) > 0
		
	def firstNode(self):
		return self.nodes[0]
		
	def firstAddress(self):
		return self._firstAddress
		
	def __repr__(self):
		return '⟨loop:['+color_string(self.ktype)+":"+str(self.ktype_radialIndex)+"]:"+self.firstAddress()+'|'+('Av' if self.availabled else '')+('Ex' if self.extended else '')+(f"|kF:{len(self.killingField)}" if self.killingField and self.availabled else '') + "⟩"#self.root()+'|'+':'.join([n.address[len(self._root):] for n in self.nodes])
				
	def adjacentLoops(self):
		return [node.links[1].next.links[1].next.prevs[2].node.loop for node in self.nodes]
		
	def chain(self):
		return self.nodes[0].chain
		
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
		
						
