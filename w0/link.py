class Link (object):

	__slots__ = ['type', 'node', 'next']
		
	def __init__(self, type, node, next):
		self.type = type
		self.node = node
		self.next = next
		
	def __repr__(self):
		return "[link:"+str(self.type)+"|"+str(self.node)+"»"+str(self.next)+"]"
		
