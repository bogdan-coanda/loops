class Loop (object):
	
	def __init__(self, index):
		self.index = index
		self.nodes = set()
		self.availabled = True
		self.seen = False # for faded coloring, marker
		self.color = None
		
#	def __eq__(self, other):
#		return self.nodes == other.nodes
