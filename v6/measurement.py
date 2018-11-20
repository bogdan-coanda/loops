class Measurement (object):
	
	__slots__ = ['diagram', 
		'reduced', 'singles', 'coerced', 'zeroes', 'results', # from reduce() { singles/coerced + decimate loop } # reduced: if reduce() was ran
		'min_chlen', 'avlen', 'chain_count', 'tobex_count', 'tobex_ratio', 'avtuples' # from detail() { simple measurement }
	]
	
	def __init__(self, diagram):
		self.diagram = diagram
		self.reduced = False
		
	def measure(diagram, reduce=False):
		mx = Measurement(diagram)
		if reduce:
			mx.singles, mx.coerced, mx.zeroes, mx.results = Measurement.reduce(diagram)
			mx.reduced = True
		mx.min_chlen, mx.avlen, mx.chain_count, mx.tobex_count, mx.tobex_ratio, mx.avtuples = Measurement.detail(diagram)		
		return mx

	def zero(diagram):
		mx = Measurement(diagram)
		mx.singles, mx.coerced, mx.zeroes, mx.results = ([],[],[],[])			
		mx.min_chlen, mx.avlen, mx.chain_count, mx.tobex_count, mx.tobex_ratio, mx.avtuples = (0, 0, 0, 0, 0, [])
		return mx

	def __repr__(self):
		if self.reduced:
			return "⟨avtuples: {} | chlen: {} | avlen: {} | chains: {} | s: {} | c: {} | z: {} | r: {} | tobex c: {} r: {:.3f}⟩".format(
				len(self.avtuples), self.min_chlen, self.avlen, self.chain_count,
				len(self.singles), len(self.coerced), len(self.zeroes), len(self.results), 
				self.tobex_count, self.tobex_ratio
			)
		else:
			return "⟨avtuples: {} | chlen: {} | avlen: {} | chains: {} | tobex c: {} r: {:.3f}⟩".format(
				len(self.avtuples), self.min_chlen, self.avlen, self.chain_count,
				self.tobex_count, self.tobex_ratio
			)			

	def __iadd__(self, other):
		self.singles += other.singles
		self.coerced += other.coerced
		self.zeroes += other.zeroes
		self.results += other.results
		self.tobex_count += other.tobex_count
		self.tobex_ratio += other.tobex_ratio
		self.avtuples += other.avtuples
		self.min_chlen += other.min_chlen
		self.avlen += other.avlen
		self.chain_count += other.chain_count
		return self
		
	# === globals ================================================================================================================================================================ #	

	def coerce(diagram):
		singles = []
		coerced = []
		
		while True:
			found = False
			
			for chain in diagram.chains:
				avlen = len(chain.avloops)
				
				if avlen == 0:
					return (singles, coerced) 

				elif avlen == 1:
					avloop = list(chain.avloops)[0]
					singles.append(avloop)
					diagram.extendLoop(avloop)
					found = True
					break
				
				elif avlen == 2:
					killingFields = [loop.killingField() for loop in chain.avloops]
					intersected = killingFields[0].intersection(killingFields[1])
					if len(intersected):
						for avloop in intersected:
							coerced.append(avloop)
							diagram.setLoopUnavailabled(avloop)
						found = True
						break
																	
			if not found:
				return (singles, coerced)		
		
	def decimate(diagram):
		zeroes = []
		
		while True:
			found = False
			results = {}
			avloops = [l for l in diagram.loops if l.availabled]
			#print("..[decimate] curr | avloops: " + str(len(avloops)))
			for index, loop in enumerate(avloops):
				diagram.extendLoop(loop)
				singles, coerced = Measurement.coerce(diagram)
				min_chlen, avlen, chain_count, tobex_count, tobex_ratio, avtuples = Measurement.detail(diagram)

				results[loop] = (
					avlen, 
					min_chlen,
					len(diagram.startNode.cycle.chain.avloops),
					-(len(singles)), 
					-(len(coerced)),
					chain_count,
					tobex_count,
					tobex_ratio
				)
				
				#print("..[decimate] " + str(loop) + " | " + str(results[loop]))
				
				for l in reversed(singles):
					diagram.collapseBack(l)						
				for l in coerced:
					diagram.setLoopAvailabled(l)			
				diagram.collapseBack(loop)				
								
				if min_chlen == 0 and chain_count > 1:
					#print("..[decimate] zeroing " + str(loop))
					zeroes.append(loop)
					diagram.setLoopUnavailabled(loop)
					found = True
			
			if not found:
				#print("..[decimate] done | zeroes: " + str(len(zeroes)))
				return (zeroes, results)
			#print("..[decimate] curr | zeroes: " + str(len(zeroes)))
			
	def reduce(diagram):
		# mandatory
		curr_singles, curr_coerced = Measurement.coerce(diagram)
		#print("[reduce] init | s: " + str(len(curr_singles)) + " | c: " + str(len(curr_coerced)))
		curr_zeroes, curr_results = Measurement.decimate(diagram)
		#print("[reduce] init | z: " + str(len(curr_zeroes)) + " | r: " + str(len(curr_results)))
		
		singles = list(curr_singles)
		coerced = list(curr_coerced)
		zeroes = list(curr_zeroes)
		results = curr_results		
		
		# additional
		while True:
			if len(curr_zeroes) > 0:
				curr_singles, curr_coerced = Measurement.coerce(diagram)
				singles += curr_singles
				coerced += curr_coerced			
				#print("[reduce] curr | s: " + str(len(curr_singles)) + " | c: " + str(len(curr_coerced)))
				
				if len(curr_singles) or len(curr_coerced):
					curr_zeroes, curr_results = Measurement.decimate(diagram)
					zeroes += curr_zeroes
					results = curr_results
					#print("[reduce] curr | z: " + str(len(curr_zeroes)) + " | r: " + str(len(curr_results)))
				else:
					break
			else:
				break
		#print("[reduce] done | s: " + str(len(singles)) + " | c: " + str(len(coerced)) + " | z: " + str(len(zeroes)) + " | r: " + str(len(results)))
		return (singles, coerced, zeroes, results)		
		
	def clean(diagram, singles, coerced, zeroes):
		for l in reversed(singles):
			diagram.collapseBack(l)						
		for l in coerced:
			diagram.setLoopAvailabled(l)
		for l in zeroes:
			diagram.setLoopAvailabled(l)		
	
	
	def detail(diagram):
		min_chlen = min([len(chain.avloops) for chain in diagram.chains])
		avlen = len([l for l in diagram.loops if l.availabled])
		chain_count = len(diagram.chains)
		tobex_count = diagram.measureTobex()
		tobex_ratio = (avlen / tobex_count) if tobex_count is not 0 else 0		
		avtuples = [t for t in diagram.loop_tuples 
			if len([loop for loop in t if not loop.availabled and not loop.extended]) == 0
			and len([loop for loop in t if len([node.cycle for node in loop.nodes if node.cycle.isKernel]) != 0]) == 0]
		return (min_chlen, avlen, chain_count, tobex_count, tobex_ratio, avtuples)		
		
	# ============================================================================================================================================================================ #	

class Result (object):
	
	__slots__ = ['obj', 'mx']
	
	def __init__(self, obj, mx):
		self.obj = obj
		self.mx = mx
