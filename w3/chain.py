class Chain (object):
	
	__slots__ = ['id', 'loops',
		'cycles', # [~] set of all contained cycles [!] [dbg] needed just for asserts, debugging, and showing unconnectable chains
		
		# open chain
		'isOpen', 'headNode', 'tailNode',
		
		# assigned on draw
		'color', 
		
		# affected chains are the underlying chains that are tied together by this new chain
		# they're the chains that need to be added to the diagram on this chain's demise
		'affected_chains',
						
		# affected loops are avloops set to unavailabled because we're connecting the affected chains together
		# they're the loops that need to be re-availabled on this chain's demise
		'affected_loops'
	] 

	chainAutoInc = 0
			
	def __init__(self):
		self.id = Chain.chainAutoInc
		Chain.chainAutoInc += 1
		
		self.loops = []
		self.cycles = [] # set outside init
		
		self.isOpen = False
		self.headNode = None
		self.tailNode = None
		
		self.color = None
		

	def __hash__(self):
		return self.id
		
		
	def __repr__(self):
		return f"⟨chain:{self.id}|av:{len(self.avloops())}/{len(self.loops)}⟩"


	def avloops(self):
		return [l for l in self.loops if l.available]	
	
						
