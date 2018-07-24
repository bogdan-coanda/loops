class Chain (object):
	
	__slots__ = ['id', 'marker', 'cycles', 'loops']
	
	def __init__(self, id):
		self.id = id
		self.marker = None
		self.cycles = []
		self.loops = []
