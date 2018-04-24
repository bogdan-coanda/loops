class Drawn (object):
	
	def __init__(self, diagram):
		self.diagram = diagram
		self.max_looped_count = 0
		self.singles = set()
		self.sparks = set()

	def reset(self):
		self.looped_count = 0	
		self.availables = []
		self.singles.clear()
		self.sparks.clear()
		self.unreachable_cycle_count = 0
		
	def clone(self):
		d = Drawn(self.diagram)
		d.looped_count = self.looped_count
		d.availables = self.availables
		d.singles.update(self.singles)
		d.sparks.update(self.sparks)
		d.unreachable_cycle_count = self.unreachable_cycle_count
		return d
		
	def __eq__(self, other):
		return self.looped_count == other.looped_count and set(self.availables) == set(other.availables) and self.singles == other.singles and self.sparks == other.sparks and self.unreachable_cycle_count == other.unreachable_cycle_count
		
