class Chain (object):
	
	__slots__ = ['id', 'avnodes']
	
	def __init__(self, id):
		self.id = id
		self.avnodes = []
		

	def __hash__(self):
		return self.id
		
		
	def __repr__(self):
		return f"⟨chain:{self.id}|av:{len(self.avnodes)}⟩"
		
						
