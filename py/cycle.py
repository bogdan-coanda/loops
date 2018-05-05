class Cycle (object):
	
	def __init__(self, index, address):
		self.index = index
		self.address = address
		self.nodes = set() # late init
		self.looped = False
		self.available_loops_count = 0 # late init
		
	def __repr__(self):
		return "[cycle:"+str(self.index)+"@"+self.address+"|"+("λ" if self.looped else "")+str(self.available_loops_count)+"]"
