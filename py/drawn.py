class Drawn (object):
	
	def __init__(self, diagram):
		self.diagram = diagram
##		self.max_looped_count = 0
#		self.looped_count = 0	
		self.availables = []
		self.chains = set()

	def reset(self):
#		self.looped_count = 0	
		self.availables = []
		self.chains.clear()
		
	def clone(self):
		d = Drawn(self.diagram)
#		d.looped_count = self.looped_count
		d.availables = self.availables
		d.chains.update(self.chains)
		return d
		
	def __eq__(self, other):
		return set(self.availables) == set(other.availables) and self.chains == other.chains # self.looped_count == other.looped_count and 
		
