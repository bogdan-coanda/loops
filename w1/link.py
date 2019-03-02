class Link (object):

	__slots__ = ['type', 'node', 'next', 'available']
		
	def __init__(self, type, node, next):
		self.type = type
		self.node = node
		self.next = next
		self.available = True
		
	def __repr__(self):
		return "[link:"+str(self.type)+"|"+str(self.node)+"»"+str(self.next)+"]"
		
