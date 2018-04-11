class Drawn (object):
	
	def __init__(self, diagram):
		self.diagram = diagram
		self.looped_count = 0
		self.availables = []
		self.unreachable_cycle_count = 0
		self.singles = set()

