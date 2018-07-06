class Node (object):
	
	__slots__ = ['perm', 'index', 'cycleIndex', 'address', 'nextLink', 'prevLink', 'loopBrethren', 'chainID', 'px', 'py', 'loop', 'links', 'prevs', 'cycle', 'cycleBrethren', 'ktype', 'showLinksOfTypes', 'tuple']
	
	def __init__(self, perm, index, cycleIndex, address, px, py):
		self.perm = perm
		self.index = index
		self.cycleIndex = cycleIndex
		self.address = address
		
		self.nextLink = None
		self.prevLink = None
																	
		# each node holds links to its N-2 brethren (nodes that extend into the same loop)
		self.loopBrethren = set()
						
		self.chainID = None # also accounts for self.looped == self.chainID is not None
		
		self.px = px
		self.py = py
						
		self.loop = None
		
		spClass = len(perm)
		self.ktype = spClass - 1		
		for q in range(0, spClass - 1):
			δ = spClass - 1 - q
			for i in range(q+1, 0, -1):
				δ = ( δ - int(address[-i]) ) % ( spClass + 1 - i )
			if δ is 0:
				self.ktype = q

		self.showLinksOfTypes = []
		self.tuple = None
		
																		
	def __repr__(self):
		return "⟨node:"+self.perm+"@"+self.address+"§"+str(self.chainID)+"|"+("λ" if self.chainID is not None else "")+("ε" if self.loop.extended else "")+("A" if self.loop.availabled else "")+"⟩"
		
		
	def __lt__(self, other):
		return self.address < other.address		
