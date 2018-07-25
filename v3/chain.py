class Chain (object):
	
	__slots__ = ['id', 'marker', 'cycles', 'loops']
	
	def __init__(self, id):
		self.id = id
		self.marker = None
		self.cycles = []
		self.loops = []
		

	def __hash__(self):
		return self.id
		
		
	def __repr__(self):
		return "⟨chain:"+str(self.id)+"|"+str(len(self.cycles))+"/"+str(len(self.loops))+"§"+str(self.marker)+"⟩"
		
						
