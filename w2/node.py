class Node (object):
	
	__slots__ = ['index', 'perm', 'address', 'cycle', 'nextLink', 'prevLink', 'px', 'py', 'loop', 'links', 'prevs', 'cycleBrethren', 'loopBrethren', 'ktype']
	
	def __init__(self, index, perm, address):
		self.index = index
		self.perm = perm
		self.address = address
		
		self.cycle = None # set by cycle.__init__(nodes)
				
		self.nextLink = None
		self.prevLink = None
										
		self.px = None
		self.py = None

		self.loop = None
		
		self.cycleBrethren = None
		self.loopBrethren = None

		# ktype is still usable as we're constructing it without loops
		spClass = len(perm)
		self.ktype = spClass - 1
		for q in range(0, spClass - 1):
			δ = spClass - 1 - q
			for i in range(q+1, 0, -1):
				δ = ( δ - int(address[-i]) ) % ( spClass + 1 - i )
			if δ is 0:
				self.ktype = q
		
																		
	def __repr__(self):
		return f"⟨node:{self.perm}@{self.address}|{'§' if self.cycle.chain else '∘'}⟩"		
		
		
	def __lt__(self, other):
		return self.address < other.address		
