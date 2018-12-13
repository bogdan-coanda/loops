class Chain (object):
	
	__slots__ = ['id', 'cycles', 'avloops']
	
	def __init__(self, id):
		self.id = id
		self.cycles = []
		self.avloops = set()
		

	def __hash__(self):
		return self.id
		
		
	def __repr__(self):
		return f"⟨chain:{self.id}|av:{len(self.avloops)}|cy:{len(self.cycles)}⟩"
		
						
