class Cycle (object):
	
	__slots__ = ['index', 'address', 'nodes', 'available_loops_count', 'px', 'py', 'chained_by_count']
	
	def __init__(self, index, address, px, py):
		self.index = index
		self.address = address
		self.nodes = set() # late init
		self.available_loops_count = 0 # late init
		self.px = px
		self.py = py
		self.chained_by_count = 0
		
		
	def __repr__(self):
		return "⟨cycle:"+str(self.index)+"@"+self.address+"|"+str(self.available_loops_count)+"⟩"
