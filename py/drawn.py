class Drawn (object):
	
	def __init__(self, diagram):
		self.diagram = diagram
		self.max_looped_count = 0
		self.singles = set()

	def reset(self):
		self.looped_count = 0	
		self.availables = []
		self.singles.clear()
		self.unreachable_cycle_count = 0
		
