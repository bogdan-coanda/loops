class Chain (object):
	
	__slots__ = ['id', 'avnodes'] #, 'cycles', 'avloops']
	
	def __init__(self, id):
		self.id = id
		self.avnodes = []
		#self.cycles = []
		#self.avloops = set()
		

	def __hash__(self):
		return self.id
		
		
	def __repr__(self):
		return f"⟨chain:{self.id}|av:{len(self.avnodes)}⟩"
		
						
