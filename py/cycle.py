class Cycle (object):
	
	def __init__(self, index, address):
		self.index = index
		self.address = address
		self.nodes = set()
		self.looped = False
		
	def __repr__(self):
		return "[cycle:"+str(self.index)+"@"+self.address+"]"
