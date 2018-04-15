class Node (object):
	
	def __init__(self, perm, index, cycleIndex, address):
		self.perm = perm
		self.index = index
		self.cycleIndex = cycleIndex
		self.address = address
		
		self.looped = False
		self.extended = False
		self.nextNode = None
		self.prevNode = None
		self.nextLink = None
		self.prevLink = None
		self.suivant = False
		self.dessus = False
		self.backed = False
		self.marked = False

		# all normal nodes are available at start for extending as they're unblemished
		self.availabled = True
													
		# [2] each normal node holds links to its (N-2)*N potential nodes (nodes looped in when extended from this node)
		self.potentials = set()
	
		# [3] each normal node holds links to its (N-2) base nodes (nodes that when extended, loop in this node as well among others)
		self.bases = set();

 		# [4] each normal node is CURRENTLY potentialed by up to (N-2) base nodes
		self.potentialedBy = set()	
	
		# [5] each node has a loop index (0-based with -1 meaning unparsed) for the loop it extends into
		self.loopIndex = -1
			
		# [7] each node holds links to its N-2 brethren (nodes that extend into the same loop)
		self.loopBrethren = set()
		
		self.seen = False