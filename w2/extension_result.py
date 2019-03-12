COERCED_EXTEND = True
COERCED_KILL = False

class ExtensionResult (object):
	
	__slots__ = ['new_chain', 'affected_loops', 'affected_chains', 'updated_chains']
	
	def setExtensionDetails(self, new_chain, affected_loops, affected_chains, updated_chains):
		self.new_chain = new_chain
		self.affected_loops = affected_loops
		self.affected_chains = affected_chains
		self.updated_chains = updated_chains

