class Cycle (object):
	
	def __init__(self, index, address, px, py):
		self.index = index
		self.address = address
		self.nodes = set() # late init
		self.looped = False
		self.available_loops_count = 0 # late init
		self.px = px
		self.py = py
		self.chained_by_count = 0
		
		
	def __repr__(self):
		return "⟨cycle:"+str(self.index)+"@"+self.address+"|"+("λ" if self.looped else "")+str(self.available_loops_count)+"⟩"
