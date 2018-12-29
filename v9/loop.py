from extension_result import *
import itertools


class Loop (object):
	
	__slots__ = [
		'index', 'nodes', '_firstAddress',
		'availabled', 'extended', 'extension_result', 'seen', 
		'ktype', 'ktype_radialIndex',
		#'ktype_columnIndex'
		'_killingField', 
		'tuple']
	
	killingFieldRecalcCount = 0
	killingFieldAllCount = 0
	killingFieldCacheCount = 0
	killingFieldUnneededCount = 0
	
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
		# killingField cache
		self._killingField = None
						

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
		return '⟨loop:['+color_string(self.ktype)+":"+str(self.ktype_radialIndex)+"]:"+self.firstAddress()+'|'+('Av' if self.availabled else '')+('Ex' if self.extended else '')+"⟩"#self.root()+'|'+':'.join([n.address[len(self._root):] for n in self.nodes])
				
	def adjacentLoops(self):
		return [node.links[1].next.links[1].next.prevs[2].node.loop for node in self.nodes]
		
	def killingField(self):
		
		Loop.killingFieldAllCount += 1
								
		# find loops with just multiple appearances - these nodes would get killed when extending this (self) loop, as they tie to at least two of the self's new connected chains
		seen = set() # unique seen once loops
		dups = set() # unique seen more loops

		# gather around all avloops for chains tied to this loop (including multiples)				
		for n in self.nodes:
			for ncn in n.chain.avnodes:
				loop = ncn.loop
				if loop in seen:
					if loop not in dups:
						dups.add(loop)
				else:
					seen.add(loop)
		
		# remove self
		dups.remove(self)

		if self._killingField == dups:
			Loop.killingFieldUnneededCount += 1
																				
		# check cache
		# if self._killingField:
		# 	Loop.killingFieldCacheCount += 1
		# 	assert self._killingField == dups
			#return self._killingField				
		# else:			
		# 	Loop.killingFieldRecalcCount += 1
		# 	if self._killingField == dups:
		# 		Loop.killingFieldUnneededCount += 1
		self._killingField = dups
											
		if Loop.killingFieldAllCount % 100000 == 0:	
			print(f"[killingField] {self} | unneeded: {Loop.killingFieldUnneededCount} | recalc: {Loop.killingFieldRecalcCount} / cache: {Loop.killingFieldCacheCount} | all: {Loop.killingFieldAllCount}")
		
		return self._killingField 

	def chain(self):
		return self.nodes[0].chain
		
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
		
						
