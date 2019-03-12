class Chain (object):
	
	__slots__ = ['id', 'avnodes',
		'cycles', # [~] set of all contained cycles [!] [dbg] needed just for asserts, debugging, and showing unconnectable chains
		'isOpen', 'tailNode',
		'color' # assigned on draw
	] 

	chainAutoInc = 0
			
	def __init__(self):
		self.id = Chain.chainAutoInc
		Chain.chainAutoInc += 1
		
		self.avnodes = []
		self.cycles = [] # set outside init
		
		self.isOpen = False
		self.tailNode = None
		
		self.color = None
		

	def __hash__(self):
		return self.id
		
		
	def __repr__(self):
		return f"⟨chain:{self.id}|av:{len(self.avnodes)}⟩"
		
						
