class Node (object):
	
	__slots__ = ['perm', 'index', 'cycleIndex', 'address', 'nextLink', 'prevLink', 'loopBrethren', 'chainID', 'px', 'py', 'loop', 'links', 'prevs', 'cycle', 'cycleBrethren']
	
	def __init__(self, perm, index, cycleIndex, address, px, py):
		self.perm = perm
		self.index = index
		self.cycleIndex = cycleIndex
		self.address = address
		
		self.nextLink = None
		self.prevLink = None

		# all normal nodes are available at start for extending as they're unblemished
		#self.availabled = True # is now a loop-level property
																	
		# [7] each node holds links to its N-2 brethren (nodes that extend into the same loop)
		self.loopBrethren = set()
		
		#self.seen = False
				
		self.chainID = None # also accounts for self.looped == self.chainID is not None
		
		self.px = px
		self.py = py
						
		self.loop = None

		
						
	def __repr__(self):
		return "⟨node:"+self.perm+"@"+self.address+"§"+str(self.chainID)+"|"+("λ" if self.chainID is not None else "")+("ε" if self.loop.extended else "")+("A" if self.loop.availabled else "")+"⟩"
		
		
