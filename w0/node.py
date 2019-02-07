class Node (object):
	
	__slots__ = ['index', 'perm', 'address', 'cycle', 'chain', 'nextLink', 'prevLink', 'loopBrethren', 'px', 'py', 'loop', 'links', 'prevs', 'cycleBrethren', 'ktype', 'tuple']
	
	def __init__(self, index, perm, address):
		self.index = index
		self.perm = perm
		self.address = address
		
		self.cycle = None # set by cycle.__init__(nodes)
		self.chain = None
		
		self.nextLink = None
		self.prevLink = None
																	
		# each node holds links to its N-2 brethren (nodes that extend into the same loop)
		self.loopBrethren = set()
								
		self.px = None
		self.py = None
						
		self.loop = None

		self.tuple = None
						
		spClass = len(perm)
		self.ktype = spClass - 1		
		for q in range(0, spClass - 1):
			δ = spClass - 1 - q
			for i in range(q+1, 0, -1):
				δ = ( δ - int(address[-i]) ) % ( spClass + 1 - i )
			if δ is 0:
				self.ktype = q
		
																		
	def __repr__(self):
		# [~][!] node.chain is only valid if the associated loop is available, as only 'available' nodes are moved to new groups when extending
		return f"⟨node:{self.perm}@{self.address}§{str(self.chain) if self.loop.availabled else '∘'}|{'Av' if self.loop.availabled else ''}{'Ex' if self.loop.extended else ''}⟩"		
		
		
	def __lt__(self, other):
		return self.address < other.address		
