class Loop (object):
	
	def __init__(self, index):
		self.index = index
		self.nodes = set()
		self.availabled = True
#		self.seen = False
		self.color = None
