class Chain (object):
	
	__slots__ = ['id', 'diagram', 'headCycle', 'tailCycle', 'color', 'cycleCount', 
		'rvstack_overwrittenChain', 'rvstack_tailCycle'
	]
	
	chainAutoInc = 0
	
	def __init__(self, diagram, addr, color):
		self.id = Chain.chainAutoInc
		Chain.chainAutoInc += 1
		
		self.diagram = diagram
		self.color = color
		
		self.headCycle = self.tailCycle = diagram.cycleByAddress[addr]
		assert self.headCycle.chain == None
		
		self.headCycle.chain = self
		self.cycleCount = 1
		diagram.chains.append(self)
		
		self.rvstack_overwrittenChain = []
		self.rvstack_tailCycle = []
		
				
	def connect(self, linkType):		
		# connect to tail
		next_link = self.tailCycle.bot_node().links[linkType]
		assert next_link.available == True
		next_cycle = next_link.next.cycle
		
		# print(f"[chain:connect] {self} | next link: {next_link} | next cycle: {next_cycle}")
		
		assert next_cycle.chain != self
		
		self.tailCycle.bot_node().nextLink = next_link
		self.tailCycle.bot_node().nextLink.next.prevLink = next_link
		
		# we'll overwrite a chain, so we delete it from the diagram's chain list
		self.rvstack_overwrittenChain.append(next_cycle.chain)
		self.diagram.chains.remove(next_cycle.chain)
		
		# set cycle chain and follow nextLinks
		next_cycle.chain = self
		self.cycleCount += 1

		while next_cycle.bot_node().nextLink:
			next_cycle = next_cycle.bot_node().nextLink.next.cycle
			next_cycle.chain = self
			self.cycleCount += 1
			
		# set new tail
		self.rvstack_tailCycle.append(self.tailCycle)
		self.tailCycle = next_cycle
				
	def revert(self):
		self.tailCycle = self.rvstack_tailCycle.pop()
		next_link = self.tailCycle.bot_node().nextLink
		next_cycle = next_link.next.cycle
				
		self.tailCycle.bot_node().nextLink.next.prevLink = None
		self.tailCycle.bot_node().nextLink = None

		overwrittenChain = self.rvstack_overwrittenChain.pop()						
		self.diagram.chains.append(overwrittenChain)
		
		next_cycle.chain = overwrittenChain				
		self.cycleCount -= 1
		
		while next_cycle.bot_node().nextLink:
			next_cycle = next_cycle.bot_node().nextLink.next.cycle
			next_cycle.chain = overwrittenChain
			self.cycleCount -= 1
				
	def __repr__(self):
		return f"⟨chain:{self.id}@{self.headCycle.address}⇒{self.tailCycle.address}|§{self.cycleCount}⟩"

