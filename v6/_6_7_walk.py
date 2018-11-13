from diagram import *
from uicanvas import *
from common import *
from itertools import chain
from time import time
from collections import defaultdict


class Measurement (object):
	
	__slots__ = ['diagram', 
		'singles', 'coerced', 'zeroes', 'results', # from reduce() { singles/coerced + decimate loop }
		'min_chlen', 'avlen', 'chain_count', 'tobex_count', 'tobex_ratio', 'avtuples' # from detail() { simple measurement }
	]
	
	def __init__(self, diagram):
		self.diagram = diagram
		
	def measure(diagram):
		mx = Measurement(diagram)
		mx.singles, mx.coerced, mx.zeroes, mx.results = reduce()			
		mx.min_chlen, mx.avlen, mx.chain_count, mx.tobex_count, mx.tobex_ratio, mx.avtuples = detail()		
		return mx

	def zero(diagram):
		mx = Measurement(diagram)
		mx.singles, mx.coerced, mx.zeroes, mx.results = ([],[],[],[])			
		mx.min_chlen, mx.avlen, mx.chain_count, mx.tobex_count, mx.tobex_ratio, mx.avtuples = (0, 0, 0, 0, 0, [])
		return mx

	def __repr__(self):
		return "⟨avtuples: {} | chlen: {} | avlen: {} | chains: {} | s: {} | c: {} | z: {} | r: {} | tobex c: {} r: {:.3f}⟩".format(
			len(self.avtuples), self.min_chlen, self.avlen, self.chain_count,
			len(self.singles), len(self.coerced), len(self.zeroes), len(self.results), 
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
		

class Result (object):
	
	__slots__ = ['obj', 'mx']
	
	def __init__(self, obj, mx):
		self.obj = obj
		self.mx = mx


if __name__ == "__main__":
		
	diagram = Diagram(7, 1)
	# diagram = Diagram(6, 3)
	# diagram = Diagram(7, 1)
	# diagram = Diagram(7, 4)

	# SP(7,4): 58
	# from ⁑⁑ avtuples:   64  | av:   636   | ch:  5  | s: 0 | c: 0 | z: 0 | tobex c: 120 r:    5.300
	#  to  ⁑⁑ avtuples: 57…60 | av: 601…605 | ch: 3…4 | s: 0 | c: 0 | z: 0 | tobex c: 115 r: 5.226…5.260
	# SP(7,1): 152
	# from ⁑⁑ avtuples:   158   | av: 790 | ch:  5  | s: 0 | c: 0 | z: 0 | tobex c: 138 r:    5.725
	#  to  ⁑⁑ avtuples: 149…152 | av: 790 | ch: 3…5 | s: 0 | c: 0 | z: 0 | tobex c: 133 r: 5.601…5.714
	# SP(6,3): 0
	# from ⁑⁑ avtuples: 3 | av: 54 | ch: 3 | s: 0 | c: 0 | z: 0 | tobex c: 15 r: 3.600
					
	def extend(addr):
		assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	def collapse(addr):
		diagram.collapseBack(diagram.nodeByAddress[addr].loop)
	def unavail(addr):
		diagram.setLoopUnavailabled(diagram.nodeByAddress[addr].loop)
					
	def coerce():
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
		
	def decimate():
		zeroes = []
		
		while True:
			found = False
			results = {}
			avloops = [l for l in diagram.loops if l.availabled]
			#print("..[decimate] curr | avloops: " + str(len(avloops)))
			for index, loop in enumerate(avloops):
				diagram.extendLoop(loop)
				singles, coerced = coerce()
				min_chlen, avlen, chain_count, tobex_count, tobex_ratio, avtuples = detail()

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
			
	def reduce():
		# mandatory
		curr_singles, curr_coerced = coerce()
		#print("[reduce] init | s: " + str(len(curr_singles)) + " | c: " + str(len(curr_coerced)))
		curr_zeroes, curr_results = decimate()
		#print("[reduce] init | z: " + str(len(curr_zeroes)) + " | r: " + str(len(curr_results)))
		
		singles = list(curr_singles)
		coerced = list(curr_coerced)
		zeroes = list(curr_zeroes)
		results = curr_results		
		
		# additional
		while True:
			if len(curr_zeroes) > 0:
				curr_singles, curr_coerced = coerce()
				singles += curr_singles
				coerced += curr_coerced			
				#print("[reduce] curr | s: " + str(len(curr_singles)) + " | c: " + str(len(curr_coerced)))
				
				if len(curr_singles) or len(curr_coerced):
					curr_zeroes, curr_results = decimate()
					zeroes += curr_zeroes
					results = curr_results
					#print("[reduce] curr | z: " + str(len(curr_zeroes)) + " | r: " + str(len(curr_results)))
				else:
					break
			else:
				break
		#print("[reduce] done | s: " + str(len(singles)) + " | c: " + str(len(coerced)) + " | z: " + str(len(zeroes)) + " | r: " + str(len(results)))
		return (singles, coerced, zeroes, results)
	
	
	def clean(singles, coerced, zeroes):
		for l in reversed(singles):
			diagram.collapseBack(l)						
		for l in coerced:
			diagram.setLoopAvailabled(l)
		for l in zeroes:
			diagram.setLoopAvailabled(l)		
	
	
	def detail():
		min_chlen = min([len(chain.avloops) for chain in diagram.chains])
		avlen = len([l for l in diagram.loops if l.availabled])
		chain_count = len(diagram.chains)
		tobex_count = diagram.measureTobex()
		tobex_ratio = (avlen / tobex_count) if tobex_count is not 0 else 0		
		avtuples = [tuple for tuple in diagram.loop_tuples 
			if len([loop for loop in tuple if not loop.availabled and not loop.extended]) == 0
			and len([loop for loop in tuple if len([node.cycle for node in loop.nodes if node.cycle.isKernel]) != 0]) == 0]
		return (min_chlen, avlen, chain_count, tobex_count, tobex_ratio, avtuples)
					
		

	def step(jump_lvl=0, jump_path=[[-1,0]], extuples=[], step_lvl=0, step_path=[[-1,0,False]], exloops=[]):
		global move_index, sol_count	
		log_template = "[*{}*][{}][lvl:{}/{}#{}#{}] [step] {} | {}"
	
		# initial measurement	
		base_mx = Measurement.measure(diagram)
		step_path[-1][1] = len(base_mx.avtuples)
								
		move_index += 1
		if move_index % 1 == 0:
			with open(running_filename + ".txt", 'a') as log:
				log.write((log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "|".join([str(x)+"."+str(t)+("b" if b else "") for x,t,b in step_path]), "-- --", str(base_mx)) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n" + "\n| ".join([str(l) for l in exloops]) + "\n\n").replace("⟩", ")").replace("⟨", "("))

		# diagram.point(); show(diagram)
		print(log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t)+("ᵝ" if b else "") for x,t,b in step_path]), "-- init --", str(base_mx)))
					
																		
		if len(diagram.chains) == 1:
			with open(sols_filename + ".txt", 'a') as log:
				log.write((log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "|".join([str(x)+"."+str(t)+("b" if b else "") for x,t,b in step_path]), "-- --", str(base_mx)) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n" + "\n| ".join([str(l) for l in exloops]) + "\n\n").replace("⟩", ")").replace("⟨", "("))
			show(diagram)
			sol_count += 1
			input("sol! " + str(sol_count))
			pass # will clean() and return
						
		elif base_mx.min_chlen == 0:
			# print(log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t)+("ᵝ" if b else "") for x,t,b in step_path]), "-- failed by measure --", str(base_mx)))			
			pass # will clean() and return
		
		else:
			seen_loops = []
			
			seen_singles = []
			seen_coerced = []
			seen_zeroes = []			
			results = base_mx.results # will be curr.results on the next while
					
			while True:
				# sort by {0 if min_chlen == 0 else tobex_ratio}, tobex_ratio, avlen, min_chlen
				sorted_results = sorted(results.items(), key = lambda pair: (0 if pair[1][1] == 0 else pair[1][-1], pair[1][-1], pair[1][0], pair[1][1]))

				#diagram.point()
				#show(diagram)
											
				av2loops = list(itertools.chain(*[list(chain.avloops) for chain in diagram.chains if len(chain.avloops) == 2]))
				#print("av2loops: "+str(len(av2loops))+"\n"+"\n".join([str(l) for l in av2loops]))
				filtered_results = None
				binary = None
				
				if len(av2loops):
					filtered_results = [p for p in sorted_results if p[0] in av2loops]
					binary = True
					#input("filtered results: "+str(len(filtered_results))+"\n"+"\n".join([str(p) for p in filtered_results]))					
				else:
					filtered_results = [p for p in sorted_results if p[0] in diagram.startNode.cycle.chain.avloops]
					binary = False
					#input("filtered results: "+str(len(filtered_results))+"\n"+"\n".join([str(p) for p in filtered_results]))					
				
				selected_result = filtered_results[0]
				selected_loop = selected_result[0]
				step_path[-1][0] += 1
				step_path[-1][1] = len(filtered_results)
				step_path[-1][2] = binary
				
				# diagram.point(); show(diagram)
				# print(log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t)+("ᵝ" if b else "") for x,t,b in step_path]), "-- extending " + str(selected_loop) + " | " + str(selected_result[1]) +  " --", str(base_mx)))

				assert diagram.extendLoop(selected_loop)
				step(jump_lvl, jump_path, extuples, step_lvl+1, step_path+[[-1, 0, False]], exloops+[selected_loop])
				diagram.collapseBack(selected_loop)
				
				diagram.setLoopUnavailabled(selected_loop)
				seen_loops.append(selected_loop)

				curr_mx = Measurement.measure(diagram)
				seen_singles += curr_mx.singles
				seen_coerced += curr_mx.coerced
				seen_zeroes += curr_mx.zeroes
				results = curr_mx.results

				# diagram.point(); show(diagram)
				# print(log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t)+("ᵝ" if b else "") for x,t,b in step_path]), "-- after seen " + str(selected_loop) + " | " + str(selected_result[1]) +  " --", str(curr_mx)))

				if len(diagram.chains) == 1:
					with open(sols_filename + ".txt", 'a') as log:
						log.write((log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "|".join([str(x)+"."+str(t)+("b" if b else "") for x,t,b in step_path]), "-- --", str(curr_mx)) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n" + "\n| ".join([str(l) for l in exloops]) + "\n\n").replace("⟩", ")").replace("⟨", "("))
					show(diagram)
					sol_count += 1
					input("sol! " + str(sol_count))
					break # will clean() and return				
																				
				elif curr_mx.min_chlen == 0:
					break # will clean() and return

			clean(seen_singles, seen_coerced, seen_zeroes)
			for l in seen_loops:
				diagram.setLoopAvailabled(l)																																																
			pass # will clean() and return		
			
		clean(base_mx.singles, base_mx.coerced, base_mx.zeroes)
		
		
	head_filename = '__walk_7.1__'
	running_filename = head_filename + "running"
	sols_filename = head_filename + "sols"
	
	# ============================================================================================================================================================================ #

	# for addr in ['01105', '01305', '01204', '12012', '12112', '12000']:
	# 	for loop in diagram.nodeByAddress[addr].loop.tuple:
	# 		assert diagram.extendLoop(loop)

	# diagram.setLoopUnavailabled(diagram.nodeByAddress['00001'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['00201'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['00143'].loop)
		
	# ============================================================================================================================================================================ #
	
	log_template = "[{}] | avtuples: {} | chlen: {} | avlen: {} | chains: {} | s: {} | c: {} | z: {} | r: {} | tobex c: {} r: {:.3f}"
	
	# [-- 0 --] | avtuples: 146 | chlen: 5 | avlen: 790 | chains: 691 | s: 0 | c: 0 | z: 0 | r: 790 | tobex c: 138 r: 5.725

	diagram.extendLoop(diagram.nodeByAddress['000001'].loop)
	
	# [-- 1 --] | avtuples: 142 | chlen: 4 | avlen: 783 | chains: 686 | s: 0 | c: 0 | z: 0 | r: 783 | tobex c: 137 r: 5.715
	
	mx = Measurement.measure(diagram)
	
	print(log_template.format("-- --", len(mx.avtuples), mx.min_chlen, mx.avlen, mx.chain_count, len(mx.singles), len(mx.coerced), len(mx.zeroes), len(mx.results), mx.tobex_count, mx.tobex_ratio))
		

	diagram.point(); show(diagram)
	print("~~~")	
	

	# ============================================================================================================================================================================ #
		
	# SP(6,1) | [lvl:0] | viable results: 28
	#	from ⁑⁑ avtuples:   28  | av:  112  | ch:  4  | s: 0 | c:  0  | z: 0 | tobex c: 25 r:   4.480
	#	 to  ⁑⁑ avtuples: 21…23 | av: 84…92 | ch: 2-4 | s: 0 | c: 0…4 | z: 0 | tobex c: 21 r: 4.0…4.381
	
	# for addr in ['01033', '01010', '02320', '02311']:
	# 	diagram.extendLoop(diagram.nodeByAddress[addr].loop)

	# SP(6,1) | [lvl:1] | viable results: 11
	#	from ⁑⁑ avtuples:   23  | av:   92  | ch:  4  | s: 0 | c:  0  | z: 0 | tobex c: 21 r:    4.381
	#	 to  ⁑⁑ avtuples: 21…23 | av: 60…76 | ch: 2-4 | s: 0 | c: 0…8 | z: 0 | tobex c: 17 r: 3.529…4.470	

	# for addr in ['02031', '11031', '10004', '01004']:
	# 	diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	
	# SP(6,1) | [lvl:2] | viable results: 1
	#	from ⁑⁑ avtuples: 19 | av: 76 | ch: 4 | s: 0 | c: 0 | z: 0 | tobex c: 17 r: 4.471
	#	 to  ⁑⁑ avtuples: 13 | av: 52 | ch: 2 | s: 0 | c: 4 | z: 0 | tobex c: 13 r: 4.000
	
	# for addr in ['02100', '02042', '01302', '01141']:
	# 	diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	
	# SP(6,1) | [lvl:3] | viable results: 0
	#	from ⁑⁑ avtuples: 13 | av: 52 | ch: 2 | s: 0 | c: 4 | z: 0 | tobex c: 13 r: 4.000
	
	# ============================================================================================================================================================================ #

	def measure_viables(avtuples, seen_tuples):
		viable_results = []	
	
		for tindex, curr_tuple in enumerate(avtuples):
		
			# extend current tuple
			curr_extended_loops = []
			for loop in curr_tuple:
				if diagram.extendLoop(loop):
					curr_extended_loops.append(loop)
				else:
					break				
				
			# check tuple completeness
			if len(curr_extended_loops) == len(curr_tuple):
				# current measurement
				curr_mx = Measurement.measure(diagram)
				curr_mx.avtuples = [t for t in curr_mx.avtuples if t not in seen_tuples]
				
				# check tuple viability
				if curr_mx.min_chlen != 0 or curr_mx.chain_count == 1:
					viable_results.append(Result(curr_tuple, curr_mx))
					# diagram.point(); show(diagram)
					# print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- [tuple:"+str(tindex)+"] passed --", str(curr_mx)))
				else:
					# diagram.point(); show(diagram)
					# print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- [tuple:"+str(tindex)+"] failed by measure --", str(curr_mx)))					
					pass
					
				# clean up after current measurement
				clean(curr_mx.singles, curr_mx.coerced, curr_mx.zeroes)
			else:
				# diagram.point(); show(diagram)			
				# print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- [tuple:"+str(tindex)+"] failed by "+str(len(curr_extended_loops))+"/"+str(len(curr_tuple))+" --", Measurement.zero(diagram)))
				pass
				
			# collapse current tuple				
			for loop in reversed(curr_extended_loops):
				diagram.collapseBack(loop)		

		return viable_results
		

	def jump(lvl=0, jump_path=[[-1,0]], extuples=[], seen_tuples=[]):
		global move_index
		log_template = "[*{}*][{}][lvl:{}#{}] [jump] {} | ⟨{}⟩"
	
		# initial measurement	
		base_mx = Measurement.measure(diagram)		
		base_mx.avtuples = [t for t in base_mx.avtuples if t not in seen_tuples]
		jump_path[-1][1] = len(base_mx.avtuples)
						
		move_index += 1
		if move_index % 1 == 0:
			with open(running_filename + ".txt", 'a') as log:
				log.write((log_template.format(move_index, tstr(time() - startTime), lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "-- --", str(base_mx)) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n\n").replace("⟩", ")").replace("⟨", "("))

		# diagram.point(); show(diagram)
		print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- init --", str(base_mx)))
			
		# attempt to extend all tuples for viability and measurements
		viable_results = measure_viables(base_mx.avtuples, seen_tuples)	
	
		# sort by len(avtuples), tobex_ratio, min_chlen
		viable_results = sorted(viable_results, key = lambda result: (len(result.mx.avtuples), result.mx.tobex_ratio, result.mx.min_chlen))
		jump_path[-1][1] = len(viable_results)
		# print("viable results: " + str(len(viable_results)))
		# print("\n".join([str([loop.firstAddress() for loop in v[0]]) + ", " + str(v[1:]) for v in viable_results]))		

		if len(viable_results) == 0: # no more tuples, go on stepping
			
			step(lvl, jump_path, extuples, 0, [[-1,0,False]], [])
			
		else: # jump viable tuple
			for viable_index, viable_entry in enumerate(reversed(viable_results)):
				jump_path[-1][0] = viable_index
				
				viable_tuple = viable_entry.obj
				viable_measurement = viable_entry.mx
			
				# extend viable tuple
				for loop in viable_tuple:
					assert diagram.extendLoop(loop)
				
				jump(lvl+1, jump_path+[[-1,0]], extuples+[viable_tuple], seen_tuples+[r[0] for r in viable_results[0:viable_index]])
					
				# collapse viable tuple				
				for loop in reversed(viable_tuple):
					diagram.collapseBack(loop)				
		
		# clean up after initial measurement
		clean(base_mx.singles, base_mx.coerced, base_mx.zeroes)
	
	
	def jump2(lvl=0, jump_path=[[-1,0]], extuples=[], seen_tuples=[]):
		global move_index
		log_template = "[*{}*][{}][lvl:{}#{}] [jump] {} | ⟨{}⟩"
	
		# initial measurement	
		base_mx = Measurement.measure(diagram)		
		base_mx.avtuples = [t for t in base_mx.avtuples if t not in seen_tuples]
		jump_path[-1][1] = len(base_mx.avtuples)
				
		move_index += 1
		if move_index % 1 == 0:
			with open(running_filename + ".txt", 'a') as log:
				log.write((log_template.format(move_index, tstr(time() - startTime), lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "-- --", str(base_mx)) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n\n").replace("⟩", ")").replace("⟨", "("))

		# diagram.point(); show(diagram)
		print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- init --", str(base_mx)))
		
		# assert len(base_mx.singles) is 0
				
		diagram.pointers = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*mx.avtuples)]))
		show(diagram); print("avtuples\n")
				
		min_chain_avlen, min_chains = sorted(groupby(groupby(diagram.pointers, K = lambda node: node.cycle.chain, G = lambda g: len(g)).items(), K = lambda pair: pair[1], V = lambda pair: pair[0]).items(), key = lambda pair: pair[0])[0]
		print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- base avtuples | min chains avlen: " + str(min_chain_avlen) + " count: " + str(len(min_chains)) + " --", str(base_mx)) + "\n" + "\n".join([str(x) for x in min_chains]))
		
		diagram.pointers = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*[chain.avloops for chain in min_chains])]))
		show(diagram); print("min chains pre viability\n")
		
		viable_results = measure_viables(base_mx.avtuples, seen_tuples)
		
		diagram.pointers = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*[r.obj for r in viable_results])]))
		show(diagram); print("viables\n")
				
		min_chain_avlen, min_chains = sorted(groupby(groupby(diagram.pointers, K = lambda node: node.cycle.chain, G = lambda g: len(g)).items(), K = lambda pair: pair[1], V = lambda pair: pair[0]).items(), key = lambda pair: pair[0])[0]
		print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- viables: " + str(len(viable_results)) + " | min chains avlen: " + str(min_chain_avlen) + " / count: " + str(len(min_chains)) + " --", str(base_mx)) + "\n" + "\n".join([str(x) for x in min_chains]))				

		diagram.pointers = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*[chain.avloops for chain in min_chains])]))
		show(diagram); print("min chains post viability\n")
				
		summed_results = []
		for chain in min_chains:
			summed_mx = Measurement.zero(diagram)
			summed_tuples = []
			for result in viable_results:
				if chain in [node.cycle.chain for node in itertools.chain(*[loop.nodes for loop in result.obj])]:
					#print("chain: " + str(chain) + " | for viable: " + str(result.obj) + " | mx: " + str(result.mx))
					summed_mx += result.mx
					summed_tuples.append(result.obj)
			summed_results.append(Result(summed_tuples, summed_mx))
			#print("[summed] adding\ntuples:\n"+str(summed_tuples)+"\nmx:\n"+str(summed_mx))

		# sort by -len(singles), len(avtuples), tobex_ratio, min_chlen						
		sorted_results = sorted(summed_results, key = lambda result: (-len(result.mx.singles), len(result.mx.avtuples), result.mx.tobex_ratio, result.mx.min_chlen))
		print("\nsorted results: ")
		for r in sorted_results:
			print(str(r.obj) + " | " + str(r.mx))

		selected_tuples = sorted_results[0].obj
		print("\nselected tuples: \n" + "\n".join([str(x) for x in selected_tuples]))
		
		diagram.pointers = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*selected_tuples)]))
		show(diagram); print("selected tuples (" + str(len(selected_tuples)) + ")\n")
		
		for ti, tuple in enumerate(selected_tuples):
			diagram.pointers = list(itertools.chain(*[loop.nodes for loop in tuple]))
			show(diagram); print("selected tuples["+str(ti)+"]\n")
			
		clean(base_mx.singles, base_mx.coerced, base_mx.zeroes)
		
	# ============================================================================================================================================================================ #	
		
	# [*0*][2m21s.89][lvl:0#-1¹⁴²] [jump] -- viables: 136 | min chains avlen: 2 / count: 4 -- | ⟨⟨avtuples: 142 | chlen: 4 | avlen: 783 | chains: 686 | s: 0 | c: 0 | z: 0 | r: 783 | tobex c: 137 r: 5.715⟩⟩
	# ⟨chain:90|1/7⟩
	# ⟨chain:54|1/7⟩
	# ⟨chain:492|1/7⟩
	# ⟨chain:288|1/7⟩
	# chain: ⟨chain:90|1/7⟩ | ⟨avtuples: 137 | chlen: 3 | avlen: 744 | chains: 661 | s: 0 | c: 0 | z: 0 | r: 744 | tobex c: 132 r: 5.636⟩
	# chain: ⟨chain:90|1/7⟩ | ⟨avtuples: 136 | chlen: 4 | avlen: 747 | chains: 661 | s: 0 | c: 0 | z: 0 | r: 747 | tobex c: 132 r: 5.659⟩
	# chain: ⟨chain:54|1/7⟩ | ⟨avtuples: 137 | chlen: 3 | avlen: 744 | chains: 661 | s: 0 | c: 0 | z: 0 | r: 744 | tobex c: 132 r: 5.636⟩
	# chain: ⟨chain:54|1/7⟩ | ⟨avtuples: 136 | chlen: 4 | avlen: 747 | chains: 661 | s: 0 | c: 0 | z: 0 | r: 747 | tobex c: 132 r: 5.659⟩
	# chain: ⟨chain:492|1/7⟩ | ⟨avtuples: 137 | chlen: 3 | avlen: 744 | chains: 661 | s: 0 | c: 0 | z: 0 | r: 744 | tobex c: 132 r: 5.636⟩
	# chain: ⟨chain:492|1/7⟩ | ⟨avtuples: 136 | chlen: 4 | avlen: 747 | chains: 661 | s: 0 | c: 0 | z: 0 | r: 747 | tobex c: 132 r: 5.659⟩
	# chain: ⟨chain:288|1/7⟩ | ⟨avtuples: 137 | chlen: 3 | avlen: 744 | chains: 661 | s: 0 | c: 0 | z: 0 | r: 744 | tobex c: 132 r: 5.636⟩
	# chain: ⟨chain:288|1/7⟩ | ⟨avtuples: 136 | chlen: 4 | avlen: 747 | chains: 661 | s: 0 | c: 0 | z: 0 | r: 747 | tobex c: 132 r: 5.659⟩
	# sorted results: 
	# [[⟨loop:[blue:15]:003006|Av⟩, ⟨loop:[blue:9]:001406|Av⟩, ⟨loop:[blue:61]:100106|Av⟩, ⟨loop:[blue:82]:110206|Av⟩, ⟨loop:[blue:48]:021306|Av⟩], [⟨loop:[indigo:30]:003001|Av⟩, ⟨loop:[violet:13]:001401|Av⟩, ⟨loop:[red:21]:010100|Av⟩, ⟨loop:[orange:67]:101200|Av⟩, ⟨loop:[yellow:44]:020004|Av⟩]] | ⟨avtuples: 273 | chlen: 7 | avlen: 1491 | chains: 1322 | s: 0 | c: 0 | z: 0 | r: 1491 | tobex c: 264 r: 11.295⟩
		
	# ⟨003006,003001⟩
	for loop in diagram.nodeByAddress['003006'].loop.tuple:
		assert diagram.extendLoop(loop)
		
	# ============================================================================================================================================================================ #
		
	# [*0*][2m20s.753][lvl:0#-1¹³⁷] [jump] -- viables: 131 | min chains avlen: 3 / count: 17 -- | ⟨⟨avtuples: 137 | chlen: 3 | avlen: 744 | chains: 661 | s: 0 | c: 0 | z: 0 | r: 744 | tobex c: 132 r: 5.636⟩⟩
	# ⟨chain:486|1/6⟩
	# ⟨chain:282|1/6⟩
	# ⟨chain:114|1/6⟩
	# ⟨chain:48|1/6⟩
	# ⟨chain:66|1/7⟩
	# ⟨chain:144|1/7⟩
	# ⟨chain:252|1/7⟩
	# ⟨chain:198|1/7⟩
	# ⟨chain:115|1/5⟩
	# ⟨chain:49|1/5⟩
	# ⟨chain:487|1/5⟩
	# ⟨chain:283|1/5⟩
	# ⟨chain:365|1/3⟩
	# ⟨chain:491|1/5⟩
	# ⟨chain:287|1/5⟩
	# ⟨chain:119|1/5⟩
	# ⟨chain:53|1/5⟩
	# 
	# sorted results: 
	# [[⟨loop:[orange:11]:002100|Av⟩, ⟨loop:[yellow:24]:010004|Av⟩, ⟨loop:[indigo:65]:002002|Av⟩, ⟨loop:[violet:42]:010302|Av⟩, ⟨loop:[red:33]:011401|Av⟩], [⟨loop:[green:33]:012032|Av⟩, ⟨loop:[green:11]:002014|Av⟩, ⟨loop:[green:24]:010041|Av⟩, ⟨loop:[green:65]:101005|Av⟩, ⟨loop:[green:42]:020023|Av⟩], [⟨loop:[blue:33]:012306|Av⟩, ⟨loop:[blue:11]:002106|Av⟩, ⟨loop:[blue:24]:010406|Av⟩, ⟨loop:[blue:65]:101006|Av⟩, ⟨loop:[blue:42]:020206|Av⟩]] | ⟨avtuples: 388 | chlen: 9 | avlen: 2122 | chains: 1908 | s: 0 | c: 0 | z: 0 | r: 2122 | tobex c: 381 r: 16.709⟩
	# [[⟨loop:[red:100]:010001|Av⟩, ⟨loop:[orange:111]:101101|Av⟩, ⟨loop:[yellow:59]:020301|Av⟩, ⟨loop:[indigo:38]:003402|Av⟩, ⟨loop:[violet:72]:001302|Av⟩], [⟨loop:[yellow:64]:100004|Av⟩, ⟨loop:[indigo:80]:020001|Av⟩, ⟨loop:[violet:46]:012101|Av⟩, ⟨loop:[red:18]:002401|Av⟩, ⟨loop:[orange:7]:001200|Av⟩], [⟨loop:[violet:98]:003403|Av⟩, ⟨loop:[red:52]:001303|Av⟩, ⟨loop:[orange:75]:100003|Av⟩, ⟨loop:[yellow:89]:110103|Av⟩, ⟨loop:[indigo:106]:021203|Av⟩]] | ⟨avtuples: 390 | chlen: 9 | avlen: 2127 | chains: 1908 | s: 0 | c: 0 | z: 0 | r: 2127 | tobex c: 381 r: 16.748⟩
	# [[⟨loop:[indigo:34]:003411|Av⟩, ⟨loop:[violet:12]:001311|Av⟩, ⟨loop:[red:20]:010010|Av⟩, ⟨loop:[orange:66]:101110|Av⟩, ⟨loop:[yellow:43]:020310|Av⟩], [⟨loop:[orange:22]:001224|Av⟩, ⟨loop:[yellow:68]:100013|Av⟩, ⟨loop:[indigo:40]:020010|Av⟩, ⟨loop:[violet:31]:012110|Av⟩, ⟨loop:[red:14]:002410|Av⟩], [⟨loop:[indigo:91]:021212|Av⟩, ⟨loop:[violet:94]:003412|Av⟩, ⟨loop:[red:92]:001312|Av⟩, ⟨loop:[orange:90]:100012|Av⟩, ⟨loop:[yellow:93]:110112|Av⟩]] | ⟨avtuples: 392 | chlen: 9 | avlen: 2134 | chains: 1908 | s: 0 | c: 0 | z: 0 | r: 2134 | tobex c: 381 r: 16.803⟩
	# [[⟨loop:[yellow:60]:100040|Av⟩, ⟨loop:[indigo:81]:020052|Av⟩, ⟨loop:[violet:47]:012152|Av⟩, ⟨loop:[red:19]:002452|Av⟩, ⟨loop:[orange:8]:001251|Av⟩], [⟨loop:[red:53]:001354|Av⟩, ⟨loop:[orange:76]:100054|Av⟩, ⟨loop:[yellow:85]:110154|Av⟩, ⟨loop:[indigo:107]:021254|Av⟩, ⟨loop:[violet:99]:003454|Av⟩], [⟨loop:[indigo:39]:003453|Av⟩, ⟨loop:[violet:73]:001353|Av⟩, ⟨loop:[red:101]:010052|Av⟩, ⟨loop:[orange:112]:101152|Av⟩, ⟨loop:[yellow:55]:020352|Av⟩]] | ⟨avtuples: 393 | chlen: 11 | avlen: 2133 | chains: 1908 | s: 0 | c: 0 | z: 0 | r: 2133 | tobex c: 381 r: 16.795⟩
	#
	# selected tuples: 
	# [⟨loop:[orange:11]:002100|Av⟩, ⟨loop:[yellow:24]:010004|Av⟩, ⟨loop:[indigo:65]:002002|Av⟩, ⟨loop:[violet:42]:010302|Av⟩, ⟨loop:[red:33]:011401|Av⟩]
	# [⟨loop:[green:33]:012032|Av⟩, ⟨loop:[green:11]:002014|Av⟩, ⟨loop:[green:24]:010041|Av⟩, ⟨loop:[green:65]:101005|Av⟩, ⟨loop:[green:42]:020023|Av⟩]
	# [⟨loop:[blue:33]:012306|Av⟩, ⟨loop:[blue:11]:002106|Av⟩, ⟨loop:[blue:24]:010406|Av⟩, ⟨loop:[blue:65]:101006|Av⟩, ⟨loop:[blue:42]:020206|Av⟩]
		
	# ⟨012306,002100,012032⟩
	for loop in diagram.nodeByAddress['012306'].loop.tuple:
		assert diagram.extendLoop(loop)
				
	# ============================================================================================================================================================================ #	
		
	# [*0*][2m5s.118][lvl:0#-1¹²⁹] [jump] -- viables: 123 | min chains avlen: 3 / count: 18 -- | ⟨⟨avtuples: 129 | chlen: 3 | avlen: 708 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 708 | tobex c: 127 r: 5.575⟩⟩
	# ⟨chain:486|1/6⟩
	# ⟨chain:282|1/6⟩
	# ⟨chain:114|1/6⟩
	# ⟨chain:48|1/6⟩
	# ⟨chain:115|1/5⟩
	# ⟨chain:49|1/5⟩
	# ⟨chain:487|1/5⟩
	# ⟨chain:283|1/5⟩
	# ⟨chain:44|1/5⟩
	# ⟨chain:386|1/5⟩
	# ⟨chain:482|1/4⟩
	# ⟨chain:278|1/5⟩
	# ⟨chain:110|1/5⟩
	# ⟨chain:365|1/3⟩
	# ⟨chain:491|1/5⟩
	# ⟨chain:287|1/5⟩
	# ⟨chain:119|1/5⟩
	# ⟨chain:53|1/5⟩
	#
	# sorted results: 
	# [[⟨loop:[red:100]:010001|Av⟩, ⟨loop:[orange:111]:101101|Av⟩, ⟨loop:[yellow:59]:020301|Av⟩, ⟨loop:[indigo:38]:003402|Av⟩, ⟨loop:[violet:72]:001302|Av⟩], [⟨loop:[yellow:64]:100004|Av⟩, ⟨loop:[indigo:80]:020001|Av⟩, ⟨loop:[violet:46]:012101|Av⟩, ⟨loop:[red:18]:002401|Av⟩, ⟨loop:[orange:7]:001200|Av⟩], [⟨loop:[violet:98]:003403|Av⟩, ⟨loop:[red:52]:001303|Av⟩, ⟨loop:[orange:75]:100003|Av⟩, ⟨loop:[yellow:89]:110103|Av⟩, ⟨loop:[indigo:106]:021203|Av⟩]] | ⟨avtuples: 364 | chlen: 8 | avlen: 2017 | chains: 1833 | s: 0 | c: 0 | z: 0 | r: 2017 | tobex c: 366 r: 16.533⟩
	# [[⟨loop:[indigo:34]:003411|Av⟩, ⟨loop:[violet:12]:001311|Av⟩, ⟨loop:[red:20]:010010|Av⟩, ⟨loop:[orange:66]:101110|Av⟩, ⟨loop:[yellow:43]:020310|Av⟩], [⟨loop:[orange:22]:001224|Av⟩, ⟨loop:[yellow:68]:100013|Av⟩, ⟨loop:[indigo:40]:020010|Av⟩, ⟨loop:[violet:31]:012110|Av⟩, ⟨loop:[red:14]:002410|Av⟩], [⟨loop:[indigo:91]:021212|Av⟩, ⟨loop:[violet:94]:003412|Av⟩, ⟨loop:[red:92]:001312|Av⟩, ⟨loop:[orange:90]:100012|Av⟩, ⟨loop:[yellow:93]:110112|Av⟩]] | ⟨avtuples: 368 | chlen: 9 | avlen: 2026 | chains: 1833 | s: 0 | c: 0 | z: 0 | r: 2026 | tobex c: 366 r: 16.607⟩
	# [[⟨loop:[yellow:60]:100040|Av⟩, ⟨loop:[indigo:81]:020052|Av⟩, ⟨loop:[violet:47]:012152|Av⟩, ⟨loop:[red:19]:002452|Av⟩, ⟨loop:[orange:8]:001251|Av⟩], [⟨loop:[red:53]:001354|Av⟩, ⟨loop:[orange:76]:100054|Av⟩, ⟨loop:[yellow:85]:110154|Av⟩, ⟨loop:[indigo:107]:021254|Av⟩, ⟨loop:[violet:99]:003454|Av⟩], [⟨loop:[indigo:39]:003453|Av⟩, ⟨loop:[violet:73]:001353|Av⟩, ⟨loop:[red:101]:010052|Av⟩, ⟨loop:[orange:112]:101152|Av⟩, ⟨loop:[yellow:55]:020352|Av⟩]] | ⟨avtuples: 369 | chlen: 11 | avlen: 2025 | chains: 1833 | s: 0 | c: 0 | z: 0 | r: 2025 | tobex c: 366 r: 16.598⟩
	# [[⟨loop:[orange:22]:001224|Av⟩, ⟨loop:[yellow:68]:100013|Av⟩, ⟨loop:[indigo:40]:020010|Av⟩, ⟨loop:[violet:31]:012110|Av⟩, ⟨loop:[red:14]:002410|Av⟩], [⟨loop:[yellow:92]:110022|Av⟩, ⟨loop:[indigo:90]:021033|Av⟩, ⟨loop:[violet:93]:003233|Av⟩, ⟨loop:[red:91]:001133|Av⟩, ⟨loop:[orange:94]:100333|Av⟩], [⟨loop:[blue:64]:100406|Av⟩, ⟨loop:[blue:80]:110006|Av⟩, ⟨loop:[blue:46]:021106|Av⟩, ⟨loop:[blue:18]:003306|Av⟩, ⟨loop:[blue:7]:001206|Av⟩]] | ⟨avtuples: 369 | chlen: 9 | avlen: 2028 | chains: 1833 | s: 0 | c: 0 | z: 0 | r: 2028 | tobex c: 366 r: 16.623⟩
	# 
	# selected tuples: 
	# [⟨loop:[red:100]:010001|Av⟩, ⟨loop:[orange:111]:101101|Av⟩, ⟨loop:[yellow:59]:020301|Av⟩, ⟨loop:[indigo:38]:003402|Av⟩, ⟨loop:[violet:72]:001302|Av⟩]
	# [⟨loop:[yellow:64]:100004|Av⟩, ⟨loop:[indigo:80]:020001|Av⟩, ⟨loop:[violet:46]:012101|Av⟩, ⟨loop:[red:18]:002401|Av⟩, ⟨loop:[orange:7]:001200|Av⟩]
	# [⟨loop:[violet:98]:003403|Av⟩, ⟨loop:[red:52]:001303|Av⟩, ⟨loop:[orange:75]:100003|Av⟩, ⟨loop:[yellow:89]:110103|Av⟩, ⟨loop:[indigo:106]:021203|Av⟩]	
		
	# ⟨010001, 100004, 003403⟩
	for loop in diagram.nodeByAddress['010001'].loop.tuple:
		assert diagram.extendLoop(loop)	
		
	# ============================================================================================================================================================================ #
		
	# [*0*][1m34s.993][lvl:0#-1¹²²] [jump] -- viables: 115 | min chains avlen: 3 / count: 38 -- | ⟨⟨avtuples: 122 | chlen: 3 | avlen: 677 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 677 | tobex c: 122 r: 5.549⟩⟩
	# ⟨chain:385|1/5⟩
	# ⟨chain:481|1/5⟩
	# ⟨chain:277|1/6⟩
	# ⟨chain:109|1/6⟩
	# ⟨chain:43|1/6⟩
	# ⟨chain:276|1/7⟩
	# ⟨chain:108|1/7⟩
	# ⟨chain:42|1/7⟩
	# ⟨chain:384|1/7⟩
	# ⟨chain:324|1/7⟩
	# ⟨chain:462|1/6⟩
	# ⟨chain:516|1/7⟩
	# ⟨chain:648|1/7⟩
	# ⟨chain:570|1/6⟩
	# ⟨chain:115|1/5⟩
	# ⟨chain:49|1/5⟩
	# ⟨chain:487|1/5⟩
	# ⟨chain:283|1/5⟩
	# ⟨chain:44|1/5⟩
	# ⟨chain:386|1/5⟩
	# ⟨chain:482|1/4⟩
	# ⟨chain:278|1/5⟩
	# ⟨chain:110|1/5⟩
	# ⟨chain:708|1/6⟩
	# ⟨chain:702|1/6⟩
	# ⟨chain:696|1/6⟩
	# ⟨chain:690|1/6⟩
	# ⟨chain:714|1/6⟩
	# ⟨chain:174|1/5⟩
	# ⟨chain:156|1/5⟩
	# ⟨chain:168|1/5⟩
	# ⟨chain:150|1/5⟩
	# ⟨chain:162|1/5⟩
	# ⟨chain:365|1/3⟩
	# ⟨chain:491|1/5⟩
	# ⟨chain:287|1/5⟩
	# ⟨chain:119|1/5⟩
	# ⟨chain:53|1/5⟩		
	#	
	# sorted results: 
	# [[⟨loop:[indigo:34]:003411|Av⟩, ⟨loop:[violet:12]:001311|Av⟩, ⟨loop:[red:20]:010010|Av⟩, ⟨loop:[orange:66]:101110|Av⟩, ⟨loop:[yellow:43]:020310|Av⟩], [⟨loop:[orange:22]:001224|Av⟩, ⟨loop:[yellow:68]:100013|Av⟩, ⟨loop:[indigo:40]:020010|Av⟩, ⟨loop:[violet:31]:012110|Av⟩, ⟨loop:[red:14]:002410|Av⟩], [⟨loop:[indigo:91]:021212|Av⟩, ⟨loop:[violet:94]:003412|Av⟩, ⟨loop:[red:92]:001312|Av⟩, ⟨loop:[orange:90]:100012|Av⟩, ⟨loop:[yellow:93]:110112|Av⟩]] | ⟨avtuples: 338 | chlen: 9 | avlen: 1921 | chains: 1758 | s: 0 | c: 0 | z: 0 | r: 1921 | tobex c: 351 r: 16.419⟩
	# [[⟨loop:[indigo:45]:021000|Av⟩, ⟨loop:[violet:17]:003200|Av⟩, ⟨loop:[red:6]:001100|Av⟩, ⟨loop:[orange:63]:100300|Av⟩, ⟨loop:[yellow:84]:110004|Av⟩], [⟨loop:[green:80]:110005|Av⟩, ⟨loop:[green:46]:021014|Av⟩, ⟨loop:[green:18]:003032|Av⟩, ⟨loop:[green:7]:001023|Av⟩, ⟨loop:[green:64]:100041|Av⟩], [⟨loop:[blue:64]:100406|Av⟩, ⟨loop:[blue:80]:110006|Av⟩, ⟨loop:[blue:46]:021106|Av⟩, ⟨loop:[blue:18]:003306|Av⟩, ⟨loop:[blue:7]:001206|Av⟩]] | ⟨avtuples: 344 | chlen: 8 | avlen: 1904 | chains: 1758 | s: 0 | c: 0 | z: 0 | r: 1904 | tobex c: 351 r: 16.274⟩
	# [[⟨loop:[orange:22]:001224|Av⟩, ⟨loop:[yellow:68]:100013|Av⟩, ⟨loop:[indigo:40]:020010|Av⟩, ⟨loop:[violet:31]:012110|Av⟩, ⟨loop:[red:14]:002410|Av⟩], [⟨loop:[yellow:92]:110022|Av⟩, ⟨loop:[indigo:90]:021033|Av⟩, ⟨loop:[violet:93]:003233|Av⟩, ⟨loop:[red:91]:001133|Av⟩, ⟨loop:[orange:94]:100333|Av⟩], [⟨loop:[blue:64]:100406|Av⟩, ⟨loop:[blue:80]:110006|Av⟩, ⟨loop:[blue:46]:021106|Av⟩, ⟨loop:[blue:18]:003306|Av⟩, ⟨loop:[blue:7]:001206|Av⟩]] | ⟨avtuples: 345 | chlen: 9 | avlen: 1929 | chains: 1758 | s: 0 | c: 0 | z: 0 | r: 1929 | tobex c: 351 r: 16.487⟩
	# [[⟨loop:[orange:79]:100324|Av⟩, ⟨loop:[yellow:88]:110013|Av⟩, ⟨loop:[indigo:105]:021024|Av⟩, ⟨loop:[violet:97]:003224|Av⟩, ⟨loop:[red:51]:001124|Av⟩], [⟨loop:[blue:64]:100406|Av⟩, ⟨loop:[blue:80]:110006|Av⟩, ⟨loop:[blue:46]:021106|Av⟩, ⟨loop:[blue:18]:003306|Av⟩, ⟨loop:[blue:7]:001206|Av⟩], [⟨loop:[red:104]:010411|Av⟩, ⟨loop:[orange:110]:101011|Av⟩, ⟨loop:[yellow:58]:020211|Av⟩, ⟨loop:[indigo:37]:003312|Av⟩, ⟨loop:[violet:71]:001212|Av⟩]] | ⟨avtuples: 346 | chlen: 8 | avlen: 1927 | chains: 1758 | s: 0 | c: 0 | z: 0 | r: 1927 | tobex c: 351 r: 16.470⟩
	# [[⟨loop:[green:118]:123032|Av⟩, ⟨loop:[green:117]:123023|Av⟩, ⟨loop:[green:116]:123014|Av⟩, ⟨loop:[green:115]:123005|Av⟩, ⟨loop:[green:119]:123041|Av⟩], [⟨loop:[violet:36]:013100|Av⟩, ⟨loop:[red:70]:013002|Av⟩, ⟨loop:[orange:103]:102402|Av⟩, ⟨loop:[yellow:114]:120202|Av⟩, ⟨loop:[indigo:57]:023200|Av⟩], [⟨loop:[blue:116]:123106|Av⟩, ⟨loop:[blue:115]:123006|Av⟩, ⟨loop:[blue:119]:123406|Av⟩, ⟨loop:[blue:118]:123306|Av⟩, ⟨loop:[blue:117]:123206|Av⟩]] | ⟨avtuples: 346 | chlen: 9 | avlen: 1931 | chains: 1758 | s: 0 | c: 0 | z: 0 | r: 1931 | tobex c: 351 r: 16.504⟩
	# [[⟨loop:[indigo:53]:021401|Av⟩, ⟨loop:[violet:76]:003101|Av⟩, ⟨loop:[red:85]:001001|Av⟩, ⟨loop:[orange:107]:100201|Av⟩, ⟨loop:[yellow:99]:110301|Av⟩], [⟨loop:[green:77]:103023|Av⟩, ⟨loop:[green:86]:111014|Av⟩, ⟨loop:[green:108]:121032|Av⟩, ⟨loop:[green:95]:113005|Av⟩, ⟨loop:[green:54]:022041|Av⟩], [⟨loop:[blue:108]:121306|Av⟩, ⟨loop:[blue:95]:113006|Av⟩, ⟨loop:[blue:54]:022406|Av⟩, ⟨loop:[blue:77]:103206|Av⟩, ⟨loop:[blue:86]:111106|Av⟩]] | ⟨avtuples: 347 | chlen: 9 | avlen: 1928 | chains: 1758 | s: 0 | c: 0 | z: 0 | r: 1928 | tobex c: 351 r: 16.479⟩
	# [[⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩], [⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩], [⟨loop:[orange:55]:002001|Av⟩, ⟨loop:[yellow:39]:010301|Av⟩, ⟨loop:[indigo:73]:002403|Av⟩, ⟨loop:[violet:101]:010203|Av⟩, ⟨loop:[red:112]:011302|Av⟩]] | ⟨avtuples: 347 | chlen: 9 | avlen: 1939 | chains: 1758 | s: 0 | c: 0 | z: 0 | r: 1939 | tobex c: 351 r: 16.573⟩
	# [[⟨loop:[yellow:60]:100040|Av⟩, ⟨loop:[indigo:81]:020052|Av⟩, ⟨loop:[violet:47]:012152|Av⟩, ⟨loop:[red:19]:002452|Av⟩, ⟨loop:[orange:8]:001251|Av⟩], [⟨loop:[red:53]:001354|Av⟩, ⟨loop:[orange:76]:100054|Av⟩, ⟨loop:[yellow:85]:110154|Av⟩, ⟨loop:[indigo:107]:021254|Av⟩, ⟨loop:[violet:99]:003454|Av⟩], [⟨loop:[indigo:39]:003453|Av⟩, ⟨loop:[violet:73]:001353|Av⟩, ⟨loop:[red:101]:010052|Av⟩, ⟨loop:[orange:112]:101152|Av⟩, ⟨loop:[yellow:55]:020352|Av⟩]] | ⟨avtuples: 348 | chlen: 11 | avlen: 1932 | chains: 1758 | s: 0 | c: 0 | z: 0 | r: 1932 | tobex c: 351 r: 16.513⟩
	# 
	# selected tuples: 
	# [⟨loop:[indigo:34]:003411|Av⟩, ⟨loop:[violet:12]:001311|Av⟩, ⟨loop:[red:20]:010010|Av⟩, ⟨loop:[orange:66]:101110|Av⟩, ⟨loop:[yellow:43]:020310|Av⟩]
	# [⟨loop:[orange:22]:001224|Av⟩, ⟨loop:[yellow:68]:100013|Av⟩, ⟨loop:[indigo:40]:020010|Av⟩, ⟨loop:[violet:31]:012110|Av⟩, ⟨loop:[red:14]:002410|Av⟩]
	# [⟨loop:[indigo:91]:021212|Av⟩, ⟨loop:[violet:94]:003412|Av⟩, ⟨loop:[red:92]:001312|Av⟩, ⟨loop:[orange:90]:100012|Av⟩, ⟨loop:[yellow:93]:110112|Av⟩]	
		
	# ⟨003411,001224,021212⟩
	for loop in diagram.nodeByAddress['003411'].loop.tuple:
		assert diagram.extendLoop(loop)	
			
	# ============================================================================================================================================================================ #	

	# [*0*][1m28s.471][lvl:0#-1¹¹²] [jump] -- viables: 105 | min chains avlen: 2 / count: 5 -- | ⟨⟨avtuples: 112 | chlen: 3 | avlen: 643 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 643 | tobex c: 117 r: 5.496⟩⟩
	# ⟨chain:174|1/5⟩
	# ⟨chain:156|1/4⟩
	# ⟨chain:168|1/5⟩
	# ⟨chain:150|1/5⟩
	# ⟨chain:162|1/5⟩				
	#
	# sorted results: 
	# [[⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩], [⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩]] | ⟨avtuples: 211 | chlen: 6 | avlen: 1221 | chains: 1122 | s: 0 | c: 0 | z: 0 | r: 1221 | tobex c: 224 r: 10.902⟩
	# [[⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩], [⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩]] | ⟨avtuples: 211 | chlen: 6 | avlen: 1221 | chains: 1122 | s: 0 | c: 0 | z: 0 | r: 1221 | tobex c: 224 r: 10.902⟩
	# [[⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩], [⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩]] | ⟨avtuples: 211 | chlen: 6 | avlen: 1221 | chains: 1122 | s: 0 | c: 0 | z: 0 | r: 1221 | tobex c: 224 r: 10.902⟩
	# [[⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩], [⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩]] | ⟨avtuples: 211 | chlen: 6 | avlen: 1221 | chains: 1122 | s: 0 | c: 0 | z: 0 | r: 1221 | tobex c: 224 r: 10.902⟩
	# [[⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩], [⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩]] | ⟨avtuples: 211 | chlen: 6 | avlen: 1221 | chains: 1122 | s: 0 | c: 0 | z: 0 | r: 1221 | tobex c: 224 r: 10.902⟩
	# 
	# selected tuples: 
	# [⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩]
	# [⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩]
	
	# ⟨011406,011032⟩
	for loop in diagram.nodeByAddress['011406'].loop.tuple:
		assert diagram.extendLoop(loop)	
			
	# ============================================================================================================================================================================ #
		
	# [*0*][1m18s.659][lvl:0#-1¹⁰⁵] [jump] -- viables: 98 | min chains avlen: 3 / count: 64 -- | ⟨⟨avtuples: 105 | chlen: 3 | avlen: 608 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 608 | tobex c: 112 r: 5.429⟩⟩
	# ⟨chain:180|1/3⟩
	# ⟨chain:186|1/6⟩
	# ⟨chain:78|1/4⟩
	# ⟨chain:84|1/6⟩
	# ⟨chain:126|1/4⟩
	# ⟨chain:132|1/5⟩
	# ⟨chain:402|1/4⟩
	# ⟨chain:408|1/6⟩
	# ⟨chain:264|1/4⟩
	# ⟨chain:240|1/4⟩
	# ⟨chain:385|1/5⟩
	# ⟨chain:481|1/5⟩
	# ⟨chain:277|1/6⟩
	# ⟨chain:109|1/6⟩
	# ⟨chain:43|1/6⟩
	# ⟨chain:276|1/7⟩
	# ⟨chain:108|1/7⟩
	# ⟨chain:42|1/7⟩
	# ⟨chain:384|1/7⟩
	# ⟨chain:324|1/7⟩
	# ⟨chain:462|1/6⟩
	# ⟨chain:516|1/7⟩
	# ⟨chain:648|1/7⟩
	# ⟨chain:570|1/6⟩
	# ⟨chain:44|1/5⟩
	# ⟨chain:386|1/5⟩
	# ⟨chain:482|1/4⟩
	# ⟨chain:278|1/5⟩
	# ⟨chain:110|1/5⟩
	# ⟨chain:247|1/5⟩
	# ⟨chain:193|1/5⟩
	# ⟨chain:61|1/5⟩
	# ⟨chain:139|1/5⟩
	# ⟨chain:415|1/4⟩
	# ⟨chain:414|1/5⟩
	# ⟨chain:246|1/4⟩
	# ⟨chain:192|1/6⟩
	# ⟨chain:60|1/6⟩
	# ⟨chain:138|1/6⟩
	# ⟨chain:208|1/3⟩
	# ⟨chain:76|1/3⟩
	# ⟨chain:124|1/3⟩
	# ⟨chain:400|1/3⟩
	# ⟨chain:262|1/3⟩
	# ⟨chain:708|1/6⟩
	# ⟨chain:702|1/6⟩
	# ⟨chain:696|1/6⟩
	# ⟨chain:690|1/6⟩
	# ⟨chain:714|1/6⟩
	# ⟨chain:267|1/5⟩
	# ⟨chain:183|1/5⟩
	# ⟨chain:81|1/5⟩
	# ⟨chain:129|1/4⟩
	# ⟨chain:405|1/5⟩
	# ⟨chain:426|1/6⟩
	# ⟨chain:624|1/6⟩
	# ⟨chain:660|1/4⟩
	# ⟨chain:348|1/6⟩
	# ⟨chain:222|1/6⟩
	# ⟨chain:365|1/3⟩
	# ⟨chain:491|1/5⟩
	# ⟨chain:287|1/5⟩
	# ⟨chain:119|1/5⟩
	# ⟨chain:53|1/5⟩		
	# 
	# sorted results: 
	# [[⟨loop:[indigo:30]:003001|Av⟩, ⟨loop:[violet:13]:001401|Av⟩, ⟨loop:[red:21]:010100|Av⟩, ⟨loop:[orange:67]:101200|Av⟩, ⟨loop:[yellow:44]:020004|Av⟩], [⟨loop:[green:31]:012014|Av⟩, ⟨loop:[green:14]:002041|Av⟩, ⟨loop:[green:22]:010023|Av⟩, ⟨loop:[green:68]:101032|Av⟩, ⟨loop:[green:40]:020005|Av⟩], [⟨loop:[blue:22]:010206|Av⟩, ⟨loop:[blue:68]:101306|Av⟩, ⟨loop:[blue:40]:020006|Av⟩, ⟨loop:[blue:31]:012106|Av⟩, ⟨loop:[blue:14]:002406|Av⟩]] | ⟨avtuples: 288 | chlen: 8 | avlen: 1701 | chains: 1603 | s: 1 | c: 0 | z: 0 | r: 1701 | tobex c: 320 r: 15.946⟩
	# [[⟨loop:[indigo:30]:003001|Av⟩, ⟨loop:[violet:13]:001401|Av⟩, ⟨loop:[red:21]:010100|Av⟩, ⟨loop:[orange:67]:101200|Av⟩, ⟨loop:[yellow:44]:020004|Av⟩], [⟨loop:[green:21]:010014|Av⟩, ⟨loop:[green:67]:101023|Av⟩, ⟨loop:[green:44]:020041|Av⟩, ⟨loop:[green:30]:012005|Av⟩, ⟨loop:[green:13]:002032|Av⟩], [⟨loop:[blue:21]:010106|Av⟩, ⟨loop:[blue:67]:101206|Av⟩, ⟨loop:[blue:44]:020406|Av⟩, ⟨loop:[blue:30]:012006|Av⟩, ⟨loop:[blue:13]:002306|Av⟩]] | ⟨avtuples: 288 | chlen: 9 | avlen: 1707 | chains: 1603 | s: 1 | c: 0 | z: 0 | r: 1707 | tobex c: 320 r: 16.003⟩
	# [[⟨loop:[indigo:45]:021000|Av⟩, ⟨loop:[violet:17]:003200|Av⟩, ⟨loop:[red:6]:001100|Av⟩, ⟨loop:[orange:63]:100300|Av⟩, ⟨loop:[yellow:84]:110004|Av⟩], [⟨loop:[green:80]:110005|Av⟩, ⟨loop:[green:46]:021014|Av⟩, ⟨loop:[green:18]:003032|Av⟩, ⟨loop:[green:7]:001023|Av⟩, ⟨loop:[green:64]:100041|Av⟩], [⟨loop:[blue:64]:100406|Av⟩, ⟨loop:[blue:80]:110006|Av⟩, ⟨loop:[blue:46]:021106|Av⟩, ⟨loop:[blue:18]:003306|Av⟩, ⟨loop:[blue:7]:001206|Av⟩]] | ⟨avtuples: 291 | chlen: 8 | avlen: 1694 | chains: 1608 | s: 0 | c: 1 | z: 0 | r: 1694 | tobex c: 321 r: 15.832⟩
	# [[⟨loop:[orange:22]:001224|Av⟩, ⟨loop:[yellow:68]:100013|Av⟩, ⟨loop:[indigo:40]:020010|Av⟩, ⟨loop:[violet:31]:012110|Av⟩, ⟨loop:[red:14]:002410|Av⟩], [⟨loop:[yellow:92]:110022|Av⟩, ⟨loop:[indigo:90]:021033|Av⟩, ⟨loop:[violet:93]:003233|Av⟩, ⟨loop:[red:91]:001133|Av⟩, ⟨loop:[orange:94]:100333|Av⟩], [⟨loop:[blue:64]:100406|Av⟩, ⟨loop:[blue:80]:110006|Av⟩, ⟨loop:[blue:46]:021106|Av⟩, ⟨loop:[blue:18]:003306|Av⟩, ⟨loop:[blue:7]:001206|Av⟩]] | ⟨avtuples: 291 | chlen: 8 | avlen: 1723 | chains: 1608 | s: 0 | c: 0 | z: 0 | r: 1723 | tobex c: 321 r: 16.103⟩
	# [[⟨loop:[orange:79]:100324|Av⟩, ⟨loop:[yellow:88]:110013|Av⟩, ⟨loop:[indigo:105]:021024|Av⟩, ⟨loop:[violet:97]:003224|Av⟩, ⟨loop:[red:51]:001124|Av⟩], [⟨loop:[blue:64]:100406|Av⟩, ⟨loop:[blue:80]:110006|Av⟩, ⟨loop:[blue:46]:021106|Av⟩, ⟨loop:[blue:18]:003306|Av⟩, ⟨loop:[blue:7]:001206|Av⟩], [⟨loop:[red:104]:010411|Av⟩, ⟨loop:[orange:110]:101011|Av⟩, ⟨loop:[yellow:58]:020211|Av⟩, ⟨loop:[indigo:37]:003312|Av⟩, ⟨loop:[violet:71]:001212|Av⟩]] | ⟨avtuples: 294 | chlen: 8 | avlen: 1717 | chains: 1608 | s: 0 | c: 0 | z: 1 | r: 1717 | tobex c: 321 r: 16.047⟩
	# [[⟨loop:[blue:71]:102106|Av⟩, ⟨loop:[blue:104]:120406|Av⟩, ⟨loop:[blue:110]:122006|Av⟩, ⟨loop:[blue:58]:023306|Av⟩, ⟨loop:[blue:37]:013206|Av⟩], [⟨loop:[green:104]:120041|Av⟩, ⟨loop:[green:110]:122005|Av⟩, ⟨loop:[green:58]:023032|Av⟩, ⟨loop:[green:37]:013023|Av⟩, ⟨loop:[green:71]:102014|Av⟩], [⟨loop:[violet:36]:013100|Av⟩, ⟨loop:[red:70]:013002|Av⟩, ⟨loop:[orange:103]:102402|Av⟩, ⟨loop:[yellow:114]:120202|Av⟩, ⟨loop:[indigo:57]:023200|Av⟩]] | ⟨avtuples: 296 | chlen: 7 | avlen: 1725 | chains: 1608 | s: 0 | c: 5 | z: 0 | r: 1725 | tobex c: 321 r: 16.121⟩
	# [[⟨loop:[green:118]:123032|Av⟩, ⟨loop:[green:117]:123023|Av⟩, ⟨loop:[green:116]:123014|Av⟩, ⟨loop:[green:115]:123005|Av⟩, ⟨loop:[green:119]:123041|Av⟩], [⟨loop:[violet:36]:013100|Av⟩, ⟨loop:[red:70]:013002|Av⟩, ⟨loop:[orange:103]:102402|Av⟩, ⟨loop:[yellow:114]:120202|Av⟩, ⟨loop:[indigo:57]:023200|Av⟩], [⟨loop:[blue:116]:123106|Av⟩, ⟨loop:[blue:115]:123006|Av⟩, ⟨loop:[blue:119]:123406|Av⟩, ⟨loop:[blue:118]:123306|Av⟩, ⟨loop:[blue:117]:123206|Av⟩]] | ⟨avtuples: 296 | chlen: 8 | avlen: 1725 | chains: 1608 | s: 0 | c: 0 | z: 0 | r: 1725 | tobex c: 321 r: 16.121⟩
	# [[⟨loop:[indigo:53]:021401|Av⟩, ⟨loop:[violet:76]:003101|Av⟩, ⟨loop:[red:85]:001001|Av⟩, ⟨loop:[orange:107]:100201|Av⟩, ⟨loop:[yellow:99]:110301|Av⟩], [⟨loop:[green:77]:103023|Av⟩, ⟨loop:[green:86]:111014|Av⟩, ⟨loop:[green:108]:121032|Av⟩, ⟨loop:[green:95]:113005|Av⟩, ⟨loop:[green:54]:022041|Av⟩], [⟨loop:[blue:108]:121306|Av⟩, ⟨loop:[blue:95]:113006|Av⟩, ⟨loop:[blue:54]:022406|Av⟩, ⟨loop:[blue:77]:103206|Av⟩, ⟨loop:[blue:86]:111106|Av⟩]] | ⟨avtuples: 297 | chlen: 8 | avlen: 1726 | chains: 1608 | s: 0 | c: 0 | z: 0 | r: 1726 | tobex c: 321 r: 16.131⟩
	# [[⟨loop:[yellow:60]:100040|Av⟩, ⟨loop:[indigo:81]:020052|Av⟩, ⟨loop:[violet:47]:012152|Av⟩, ⟨loop:[red:19]:002452|Av⟩, ⟨loop:[orange:8]:001251|Av⟩], [⟨loop:[red:53]:001354|Av⟩, ⟨loop:[orange:76]:100054|Av⟩, ⟨loop:[yellow:85]:110154|Av⟩, ⟨loop:[indigo:107]:021254|Av⟩, ⟨loop:[violet:99]:003454|Av⟩], [⟨loop:[indigo:39]:003453|Av⟩, ⟨loop:[violet:73]:001353|Av⟩, ⟨loop:[red:101]:010052|Av⟩, ⟨loop:[orange:112]:101152|Av⟩, ⟨loop:[yellow:55]:020352|Av⟩]] | ⟨avtuples: 298 | chlen: 9 | avlen: 1726 | chains: 1608 | s: 0 | c: 0 | z: 0 | r: 1726 | tobex c: 321 r: 16.131⟩
	# [[⟨loop:[indigo:44]:020420|Av⟩, ⟨loop:[violet:30]:012020|Av⟩, ⟨loop:[red:13]:002320|Av⟩, ⟨loop:[orange:21]:001134|Av⟩, ⟨loop:[yellow:67]:100334|Av⟩], [⟨loop:[red:106]:010133|Av⟩, ⟨loop:[orange:98]:101233|Av⟩, ⟨loop:[yellow:52]:020022|Av⟩, ⟨loop:[indigo:75]:003034|Av⟩, ⟨loop:[violet:89]:001434|Av⟩], [⟨loop:[blue:21]:010106|Av⟩, ⟨loop:[blue:67]:101206|Av⟩, ⟨loop:[blue:44]:020406|Av⟩, ⟨loop:[blue:30]:012006|Av⟩, ⟨loop:[blue:13]:002306|Av⟩]] | ⟨avtuples: 298 | chlen: 8 | avlen: 1730 | chains: 1608 | s: 0 | c: 1 | z: 0 | r: 1730 | tobex c: 321 r: 16.168⟩
	# [[⟨loop:[indigo:79]:003444|Av⟩, ⟨loop:[violet:88]:001344|Av⟩, ⟨loop:[red:105]:010043|Av⟩, ⟨loop:[orange:97]:101143|Av⟩, ⟨loop:[yellow:51]:020343|Av⟩], [⟨loop:[yellow:66]:100244|Av⟩, ⟨loop:[indigo:43]:020330|Av⟩, ⟨loop:[violet:34]:012430|Av⟩, ⟨loop:[red:12]:002230|Av⟩, ⟨loop:[orange:20]:001044|Av⟩], [⟨loop:[yellow:20]:010040|Av⟩, ⟨loop:[indigo:66]:002053|Av⟩, ⟨loop:[violet:43]:010353|Av⟩, ⟨loop:[red:34]:011452|Av⟩, ⟨loop:[orange:12]:002151|Av⟩]] | ⟨avtuples: 298 | chlen: 9 | avlen: 1734 | chains: 1608 | s: 0 | c: 0 | z: 0 | r: 1734 | tobex c: 321 r: 16.206⟩
	# [[⟨loop:[blue:69]:101406|Av⟩, ⟨loop:[blue:41]:020106|Av⟩, ⟨loop:[blue:32]:012206|Av⟩, ⟨loop:[blue:10]:002006|Av⟩, ⟨loop:[blue:23]:010306|Av⟩], [⟨loop:[indigo:16]:003100|Av⟩, ⟨loop:[violet:5]:001000|Av⟩, ⟨loop:[red:62]:010303|Av⟩, ⟨loop:[orange:83]:101403|Av⟩, ⟨loop:[yellow:49]:020103|Av⟩], [⟨loop:[green:32]:012023|Av⟩, ⟨loop:[green:10]:002005|Av⟩, ⟨loop:[green:23]:010032|Av⟩, ⟨loop:[green:69]:101041|Av⟩, ⟨loop:[green:41]:020014|Av⟩]] | ⟨avtuples: 299 | chlen: 8 | avlen: 1729 | chains: 1608 | s: 0 | c: 0 | z: 1 | r: 1729 | tobex c: 321 r: 16.159⟩
	# [[⟨loop:[violet:41]:010212|Av⟩, ⟨loop:[red:32]:011311|Av⟩, ⟨loop:[orange:10]:002010|Av⟩, ⟨loop:[yellow:23]:010310|Av⟩, ⟨loop:[indigo:69]:002412|Av⟩], [⟨loop:[blue:69]:101406|Av⟩, ⟨loop:[blue:41]:020106|Av⟩, ⟨loop:[blue:32]:012206|Av⟩, ⟨loop:[blue:10]:002006|Av⟩, ⟨loop:[blue:23]:010306|Av⟩], [⟨loop:[indigo:76]:003124|Av⟩, ⟨loop:[violet:85]:001024|Av⟩, ⟨loop:[red:107]:010312|Av⟩, ⟨loop:[orange:99]:101412|Av⟩, ⟨loop:[yellow:53]:020112|Av⟩]] | ⟨avtuples: 301 | chlen: 8 | avlen: 1736 | chains: 1608 | s: 0 | c: 0 | z: 0 | r: 1736 | tobex c: 321 r: 16.224⟩
	# 
	# selected tuples: 
	# [⟨loop:[indigo:30]:003001|Av⟩, ⟨loop:[violet:13]:001401|Av⟩, ⟨loop:[red:21]:010100|Av⟩, ⟨loop:[orange:67]:101200|Av⟩, ⟨loop:[yellow:44]:020004|Av⟩]
	# [⟨loop:[green:31]:012014|Av⟩, ⟨loop:[green:14]:002041|Av⟩, ⟨loop:[green:22]:010023|Av⟩, ⟨loop:[green:68]:101032|Av⟩, ⟨loop:[green:40]:020005|Av⟩]
	# [⟨loop:[blue:22]:010206|Av⟩, ⟨loop:[blue:68]:101306|Av⟩, ⟨loop:[blue:40]:020006|Av⟩, ⟨loop:[blue:31]:012106|Av⟩, ⟨loop:[blue:14]:002406|Av⟩]
	
	# ⟨012014,010206,003001⟩
	for loop in diagram.nodeByAddress['012014'].loop.tuple:
		assert diagram.extendLoop(loop)					
										
	# ============================================================================================================================================================================ #

	startTime = time()
	move_index = -1
	sol_count = 0
	
	diagram.point(); show(diagram); print('-- start --\n')
	print("----------")
	lvl = 0
	ass_before = detail()
	jump2()
	ass_after = detail()
	assert ass_before == ass_after, "broken first step"
	diagram.point(); show(diagram); print('-- final --\n')
	print("[*{}*][{}] sols found: {}".format(move_index, tstr(time() - startTime), sol_count))
	print("------------")
