COERCED_EXTEND = True
COERCED_KILL = False

class ExtensionResult (object):
	
	__slots__ = ['new_chain', 'affected_loops', 'affected_chains']#, 'affected_singles', 'reachable', 'temporary_reachable', 'extended_count', 'killed_count', 'coerced_loops', 'temporary_extended_count', 'temporary_killed_count', 'temporary_coerced_loops']
	'''
	def __init__(self):
		self.new_chain = None
		self.affected_loops = None
		self.affected_chains = None
		self.affected_singles = [] # empty in case .coerce() is not called
						
		# coerced loops are time-ordered pairs of (loop, bool ? `extended` : `killed`)
		self.coerced_loops = []
		self.extended_count = 0
		self.killed_count = 0
		self.reachable = None
		
		self.temporary_coerced_loops = []
		self.temporary_extended_count = 0
		self.temporary_killed_count = 0
		self.temporary_reachable = None
	'''
	def setExtensionDetails(self, new_chain, affected_loops, affected_chains):
		self.new_chain = new_chain
		self.affected_loops = affected_loops
		self.affected_chains = affected_chains
	'''
	def addCoercionDetails(self, singles, coerced):
		self.affected_singles += singles
		self.affected_loops += coerced
		
	def setReachability(self, reachable, temporary):
		if not temporary:
			self.reachable = reachable
		else:
			self.temporary_reachable = reachable
		
	def coerce(self, loop, type, temporary):
		if not temporary:
			self.coerced_loops.append((loop, type))
			if type == COERCED_EXTEND:
				self.extended_count += 1
			else: #if type == COERCED_KILL:
				self.killed_count += 1
		else:
			self.temporary_coerced_loops.append((loop, type))
			if type == COERCED_EXTEND:
				self.temporary_extended_count += 1
			else: #if type == COERCED_KILL:
				self.temporary_killed_count += 1			
						
	def reset(self, temporary):
		if not temporary:
			self.coerced_loops = []
			self.extended_count = 0
			self.killed_count = 0
		else:
			self.temporary_coerced_loops = []
			self.temporary_extended_count = 0
			self.temporary_killed_count = 0			
	'''
