class Chain (object):
	
	__slots__ = ['id', 'marker', 'cycles', 'avloops']
	
	def __init__(self, id):
		self.id = id
		self.marker = None
		self.cycles = []
		self.avloops = set()
		

	def __hash__(self):
		return self.id
		
		
	def __repr__(self):
		return "⟨chain:"+str(self.id)+"|"+str(len(self.cycles))+"/"+str(len(self.avloops))+"§"+str(self.marker)+"⟩"
		
						
