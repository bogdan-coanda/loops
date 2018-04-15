from time import time
from functools import cmp_to_key


class State (object):
	
	def __init__(self, diagram):
		self.diagram = diagram
		self.state = "new"
		self.initTime = 0
		self.lvl = 0 
		self.seen = set()
		self.lvls_node = [None]
		self.lvls_seen = [set()]
		self.lvls_availables = [[]]
		self.lvls_avIndex = [0]
		self.lvls_hasSingles = [False]
		
	def init(self):
		self.state = "running"
		self.initTime = time()
		self.diagram.measureNodes()
		
		def cmp(x, y):
			p = 1 if a in self.diagram.drawn.singles else 0;
			q = 1 if b in self.diagram.drawn.singles else 0;
			return q - p if p != q else b.index - a.index
					
		self.diagram.drawn.availables.sort(key = cmp_to_key(cmp))				
		self.lvls_node = [myDiagram.drawn.availables[0]]
		self.lvls_node[0].marked = True
		self.lvls_availables = [self.diagram.drawn.availables]
		self.lvls_hasSingles = [len(self.diagram.drawn.singles) > 0]

	def next_available(self):
		self.lvls_node[self.lvl].marked = False
		self.lvls_avIndex[self.lvl] = self.lvls_avIndex[self.lvl] + 1
		if self.lvls_hasSingles[self.lvl] == False and self.lvls_avIndex[self.lvl] < len(self.lvls_availables[self.lvl]):
			self.lvls_node[self.lvl] = self.lvls_availables[self.lvl][self.lvls_avIndex[self.lvl]]
			self.lvls_node[self.lvl].marked = True
		else:
			self.lvls_node[self.lvl] = None
			
