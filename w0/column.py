import itertools

class Column (object):
	
	__slots__ = ['id', 'tuples', 'firstNode', 'columnLoops', 'unavailabled']
	
	
	def __init__(self, id, tuples):
		self.id = id
		self.tuples = tuples
		self.firstNode = min(itertools.chain(*[itertools.chain(*[[n for n in l.nodes] for l in t]) for t in tuples]), key = lambda n: n.address)		
		self.columnLoops = sorted(set([n.loop for n in itertools.chain(*[itertools.chain(*[itertools.chain(*[n.cycle.nodes for n in l.nodes]) for l in t]) for t in tuples]) if n.ktype == 0]), key = lambda l: l.firstAddress())
		self.unavailabled = False # to be forced manually
		
		
	def isAvailabled(self):
		return self.unavailabled == False and len([t for t in self.tuples if len([l for l in t if not l.availabled]) > 0]) == 0
		
	def __repr__(self):
		return f"⟨column:{self.id}@{self.firstNode.address}|t:{len(self.tuples)}|cL:{len(self.columnLoops)}|bb:{len(set([l.firstAddress()[:-3] for l in self.columnLoops]))}⟩"
