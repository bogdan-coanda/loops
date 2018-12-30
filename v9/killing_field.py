class KillingField (object):
	
	__slots__ = ['loop', 'field']
	
	def __init__(self, loop):
		self.loop = loop
		self.field = KillingField.calculateKillingFieldSet(loop)
				
	def __len__(self):
		return len(self.field)
		
	def __iter__(self):
		return iter(self.field)
		
	def add(self, loop):
		self.field.add(loop)		

	def remove(self, loop):
		self.field.remove(loop)
		
	def regenerate(self):
		self.field = KillingField.calculateKillingFieldSet(self.loop)
		
	def assess(self):
		self.field == KillingField.calculateKillingFieldSet(self.loop)
		
	def calculateKillingFieldSet(self_loop):
										
		# find loops with just multiple appearances - these nodes would get killed when extending this (self) loop, as they tie to at least two of the self's new connected chains
		seen = set() # unique seen once loops
		dups = set() # unique seen more loops

		# gather around all avloops for chains tied to this loop (including multiples)				
		for n in self_loop.nodes:
			for ncn in n.chain.avnodes:
				loop = ncn.loop
				if loop in seen:
					if loop not in dups:
						dups.add(loop)
				else:
					seen.add(loop)
		
		# remove self
		dups.remove(self_loop)
		
		# return killing field							
		return dups
