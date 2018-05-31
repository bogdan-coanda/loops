class Node (object):
	
	def __init__(self, perm, index, cycleIndex, address, px, py):
		self.perm = perm
		self.index = index
		self.cycleIndex = cycleIndex
		self.address = address
		
		self.looped = False
		self.extended = False
		self.nextLink = None
		self.prevLink = None
		self.suivant = False
		self.dessus = False
		self.backed = False
		self.marked = False

		# all normal nodes are available at start for extending as they're unblemished
		#self.availabled = True # is now a loop-level property
														
		# [5] each node has a loop index (0-based with -1 meaning unparsed) for the loop it extends into
		self.loopIndex = -1
			
		# [7] each node holds links to its N-2 brethren (nodes that extend into the same loop)
		self.loopBrethren = set()
		
		#self.seen = False
		
		self.chainStarter = False
		
		self.chainID = None # also accounts for self.looped == self.chainID is not None
		
		self.px = px
		self.py = py
		
		self.color = None
		
		self.real = None # the node that was actually extended when extend was called on this node		


	def ext_reset(self):		
		self.ext_deletedLinks = []
		self.ext_appendedLinks = []
		self.ext_workedNodes = []
		self.ext_connectedChains = []
		self.ext_chained = []
#		self.ext_avs = []
#		self.ext_uns = []
		self.ext_flp = []
		self.ext_loopedCycles = []		
		
						
	def __repr__(self):
		return "⟨node:"+self.perm+"@"+self.address+"§"+str(self.chainID)+"|"+("λ" if self.looped else "")+("ε" if self.extended else "")+("ψ" if self.chainStarter else "")+("A" if self.loop.availabled else "")+"⟩"
		
		
