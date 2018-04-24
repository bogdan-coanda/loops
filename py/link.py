class Link (object):
	
	def __init__(self, type, node, next):
		self.type = type
		self.node = node
		self.next = next
		
	def __repr__(self):
		return "[link:"+str(self.type)+"|"+self.node.perm+"»"+self.next.perm+"]"
