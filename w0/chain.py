class Chain (object):
	
	__slots__ = ['id', 'avnodes',
		'cycles' # [~] set of all contained cycles [!] [dbg] needed just for asserts, debugging, and showing unconnectable chains
	]
	# 
	
	def __init__(self, id):
		self.id = id
		self.avnodes = []
		self.cycles = [] # set outside init
		

	def __hash__(self):
		return self.id
		
		
	def __repr__(self):
		return f"⟨chain:{self.id}|av:{len(self.avnodes)}⟩"
		
						
