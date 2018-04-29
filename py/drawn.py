class Drawn (object):
	
	def __init__(self, diagram):
		self.diagram = diagram
		self.max_looped_count = 0
		self.looped_count = 0	
		self.availables = []
		self.singles = set()
		self.sparks = set()
		self.unreachable_cycles = set()
		self.chains = set()

	def reset(self):
		self.looped_count = 0	
		self.availables = []
		self.singles.clear()
		self.sparks.clear()
		self.unreachable_cycles.clear()
		self.chains.clear()
		
	def clone(self):
		d = Drawn(self.diagram)
		d.looped_count = self.looped_count
		d.availables = self.availables
		d.singles.update(self.singles)
		d.sparks.update(self.sparks)
		d.unreachable_cycles.update(self.unreachable_cycles)
		d.chains.update(self.chains)
		return d
		
	def __eq__(self, other):
		return self.looped_count == other.looped_count and set(self.availables) == set(other.availables) and self.singles == other.singles and self.sparks == other.sparks and self.unreachable_cycles == other.unreachable_cycles and self.chains == other.chains
		
