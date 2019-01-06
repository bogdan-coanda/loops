class Tuple (object):
	
	__slots__ = ['id', 'loops', 'firstLoop', 'availabled']
	
	def __init__(self, id, loops):
		self.id = id
		self.loops = loops
		self.firstLoop = sorted(loops, key = lambda l: l.firstAddress())[0]
		self.availabled = (
			len([loop for loop in loops if not loop.availabled and not loop.extended]) == 0
			and 
			len([loop for loop in loops if len([node.cycle for node in loop.nodes if node.cycle.isKernel]) != 0]) == 0)

	def __hash__(self):
		return self.id
								
	def __getitem__(self, key):
		return self.loops[key]
		
	def __len__(self):
		return len(self.loops)
		
	def __lt__(self, other):
		return self.id < other.id
		
	def __repr__(self):
		return f"⟨tuple:{self.id}|{self.firstLoop}|{'Av' if self.availabled else ''}⟩"		
		
	def isUntouched(self):
		return len( # having no loops # if we have no connected loops
								[l for l in self.loops # which # if we have connected loops
										if len( # having nodes # if we have connected nodes
											[n for n in l.nodes # which # if we have connected nodes
													if not n.cycle.isUnchained] # are in cycles tied to other cycles (extended through by another node) # if we have a connected node
										) != 0]
							) == 0
