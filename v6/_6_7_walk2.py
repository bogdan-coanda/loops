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
	
	diagram.extendLoop(diagram.nodeByAddress['000001'].loop)
	
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
				
		#diagram.pointers = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*base_mx.avtuples)]))
		#show(diagram); print("avtuples\n")
		
		viable_results = measure_viables(base_mx.avtuples, seen_tuples)
		viable_tuples = [r.obj for r in viable_results]		
		print("viables: " + str(len(viable_results))) # + "\n".join([str(r.obj) + " | " + str(r.mx) for r in viable_results]) + "\n")
		
		#diagram.pointers = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*[r.obj for r in viable_results])]))
		#show(diagram); print("viables\n")
				
		min_viable_tuple_count = diagram.spClass
		min_cycles = []
		min_cycle_tuples = []
		min_cycle_results_pairs = []
		
		unchained_cycles = [cycle for cycle in diagram.cycles if len(cycle.chain.cycles) is 1]
		print("unchained_cycles: " + str(len(unchained_cycles)))
		for cycle in unchained_cycles:
			curr_cycle_tuples = [node.loop.tuple for node in cycle.nodes if node.loop.availabled or node.loop.extended]
			matched_tuples = set(curr_cycle_tuples).intersection(viable_tuples)
			matched_results = tuple([result for result in viable_results if result.obj in curr_cycle_tuples])
			assert set([r.obj for r in matched_results]) == set(matched_tuples)
			 
			if len(matched_tuples) < min_viable_tuple_count:
				min_viable_tuple_count = len(matched_tuples)
				min_cycles = [cycle]
				min_cycle_tuples = [matched_tuples]
				min_cycle_results_pairs = [(cycle, matched_results)]
			elif len(matched_tuples) == min_viable_tuple_count:
				min_cycles.append(cycle)
				min_cycle_tuples.append(matched_tuples)
				min_cycle_results_pairs.append((cycle, matched_results))
					
								
		grouped_cycles_per_matched_results = groupby(min_cycle_results_pairs, K = lambda pair: pair[1], V = lambda pair: pair[0])
		print("min_viable_tuple_count: " + str(min_viable_tuple_count) + " | min_cycles: " + str(len(min_cycles)) + " | grouped_cycles_per_matched_results: " + str(len(grouped_cycles_per_matched_results)) + "\n")
		for matched_results, cycles in grouped_cycles_per_matched_results.items():
			for cycle in cycles:
				print(str(cycle))
			for result in matched_results:
				print("\t" + str(result.obj))
			summed_mx = Measurement.zero(diagram)
			for result in matched_results:
				print("\t-- : " + str(result.mx))
				summed_mx += result.mx
			print("\t== : " + str(summed_mx) + "\n")		
	
		min_nodes = list(itertools.chain(*[
			[node for node in cycle.nodes if node.loop.tuple in min_cycle_tuples[index]]
			for index, cycle in enumerate(min_cycles)
		]))
		print("min nodes: " + str(len(min_nodes)) + "\n" + "\n".join([str(x) for x in min_nodes]) + "\n")				
		
		diagram.pointers = min_nodes
		show(diagram); print("^^min_nodes^^")
			
		clean(base_mx.singles, base_mx.coerced, base_mx.zeroes)
		
	# ===  0 ===================================================================================================================================================================== #	
	
	# [*0*][0m2s.227][lvl:0#-1¹⁴²] [jump] -- init -- | ⟨⟨avtuples: 142 | chlen: 4 | avlen: 783 | chains: 686 | s: 0 | c: 0 | z: 0 | r: 783 | tobex c: 137 r: 5.715⟩⟩
	# viables: 136
	# unchained_cycles: 685
	# min_viable_tuple_count: 2 | min_cycles: 4 | grouped_cycles_per_matched_results: 1
	
	# ⟨cycle:54@00140§⟨chain:54|1/7⟩⟩
	# ⟨cycle:90@00300§⟨chain:90|1/7⟩⟩
	# ⟨cycle:288@02130§⟨chain:288|1/7⟩⟩
	# ⟨cycle:492@11020§⟨chain:492|1/7⟩⟩
	# 	(⟨loop:[blue:15]:003006|Av⟩, ⟨loop:[blue:9]:001406|Av⟩, ⟨loop:[blue:61]:100106|Av⟩, ⟨loop:[blue:82]:110206|Av⟩, ⟨loop:[blue:48]:021306|Av⟩)
	# 	(⟨loop:[indigo:30]:003001|Av⟩, ⟨loop:[violet:13]:001401|Av⟩, ⟨loop:[red:21]:010100|Av⟩, ⟨loop:[orange:67]:101200|Av⟩, ⟨loop:[yellow:44]:020004|Av⟩)
	# 	-- : ⟨avtuples: 138 | chlen: 3 | avlen: 744 | chains: 661 | s: 0 | c: 0 | z: 0 | r: 744 | tobex c: 132 r: 5.636⟩
	# 	-- : ⟨avtuples: 137 | chlen: 4 | avlen: 747 | chains: 661 | s: 0 | c: 0 | z: 0 | r: 747 | tobex c: 132 r: 5.659⟩
	# 	== : ⟨avtuples: 275 | chlen: 7 | avlen: 1491 | chains: 1322 | s: 0 | c: 0 | z: 0 | r: 1491 | tobex c: 264 r: 11.295⟩
	
	# min nodes: 8
	# ⟨node:1230564@001401§⟨chain:54|1/7⟩|A⟩
	# ⟨node:6412305@001406§⟨chain:54|1/7⟩|A⟩
	# …
			
	# ⟨001401, 001406⟩
	for loop in diagram.nodeByAddress['001401'].loop.tuple:
		assert diagram.extendLoop(loop)
	
	# ===  1 ===================================================================================================================================================================== #
	
	# [*0*][0m2s.215][lvl:0#-1¹³⁷] [jump] -- init -- | ⟨⟨avtuples: 137 | chlen: 4 | avlen: 747 | chains: 661 | s: 0 | c: 0 | z: 0 | r: 747 | tobex c: 132 r: 5.659⟩⟩
	# viables: 129
	# unchained_cycles: 656
	# min_viable_tuple_count: 3 | min_cycles: 23 | grouped_cycles_per_matched_results: 5
	
	# ⟨cycle:49@00131§⟨chain:49|1/6⟩⟩
	# ⟨cycle:115@00341§⟨chain:115|1/6⟩⟩
	# ⟨cycle:283@02121§⟨chain:283|1/6⟩⟩
	# ⟨cycle:487@11011§⟨chain:487|1/6⟩⟩
	# 	(⟨loop:[indigo:34]:003411|Av⟩, ⟨loop:[violet:12]:001311|Av⟩, ⟨loop:[red:20]:010010|Av⟩, ⟨loop:[orange:66]:101110|Av⟩, ⟨loop:[yellow:43]:020310|Av⟩)
	# 	(⟨loop:[orange:22]:001224|Av⟩, ⟨loop:[yellow:68]:100013|Av⟩, ⟨loop:[indigo:40]:020010|Av⟩, ⟨loop:[violet:31]:012110|Av⟩, ⟨loop:[red:14]:002410|Av⟩)
	# 	(⟨loop:[indigo:91]:021212|Av⟩, ⟨loop:[violet:94]:003412|Av⟩, ⟨loop:[red:92]:001312|Av⟩, ⟨loop:[orange:90]:100012|Av⟩, ⟨loop:[yellow:93]:110112|Av⟩)
	# 	-- : ⟨avtuples: 128 | chlen: 4 | avlen: 713 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 713 | tobex c: 127 r: 5.614⟩
	# 	-- : ⟨avtuples: 132 | chlen: 4 | avlen: 710 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 710 | tobex c: 127 r: 5.591⟩
	# 	-- : ⟨avtuples: 129 | chlen: 4 | avlen: 710 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 710 | tobex c: 127 r: 5.591⟩
	# 	== : ⟨avtuples: 389 | chlen: 12 | avlen: 2133 | chains: 1908 | s: 0 | c: 0 | z: 0 | r: 2133 | tobex c: 381 r: 16.795⟩
	#
	# ⟨cycle:59@00145§⟨chain:59|1/7⟩⟩
	# ⟨cycle:95@00305§⟨chain:95|1/7⟩⟩
	# ⟨cycle:293@02135§⟨chain:293|1/7⟩⟩
	# ⟨cycle:371@10015§⟨chain:371|1/6⟩⟩
	# ⟨cycle:497@11025§⟨chain:497|1/7⟩⟩
	# 	(⟨loop:[blue:15]:003006|Av⟩, ⟨loop:[blue:9]:001406|Av⟩, ⟨loop:[blue:61]:100106|Av⟩, ⟨loop:[blue:82]:110206|Av⟩, ⟨loop:[blue:48]:021306|Av⟩)
	# 	(⟨loop:[red:11]:002051|Av⟩, ⟨loop:[orange:24]:001454|Av⟩, ⟨loop:[yellow:65]:100154|Av⟩, ⟨loop:[indigo:42]:020151|Av⟩, ⟨loop:[violet:33]:012251|Av⟩)
	# 	(⟨loop:[yellow:40]:020040|Av⟩, ⟨loop:[indigo:31]:003052|Av⟩, ⟨loop:[violet:14]:001452|Av⟩, ⟨loop:[red:22]:010151|Av⟩, ⟨loop:[orange:68]:101251|Av⟩)
	# 	-- : ⟨avtuples: 133 | chlen: 3 | avlen: 709 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 709 | tobex c: 127 r: 5.583⟩
	# 	-- : ⟨avtuples: 132 | chlen: 4 | avlen: 712 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 712 | tobex c: 127 r: 5.606⟩
	# 	-- : ⟨avtuples: 132 | chlen: 4 | avlen: 712 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 712 | tobex c: 127 r: 5.606⟩
	# 	== : ⟨avtuples: 397 | chlen: 11 | avlen: 2133 | chains: 1908 | s: 0 | c: 0 | z: 0 | r: 2133 | tobex c: 381 r: 16.795⟩
	#
	# ⟨cycle:66@00210§⟨chain:66|1/7⟩⟩
	# ⟨cycle:144@01040§⟨chain:144|1/7⟩⟩
	# ⟨cycle:198@01230§⟨chain:198|1/7⟩⟩
	# ⟨cycle:252@02020§⟨chain:252|1/7⟩⟩
	# 	(⟨loop:[orange:11]:002100|Av⟩, ⟨loop:[yellow:24]:010004|Av⟩, ⟨loop:[indigo:65]:002002|Av⟩, ⟨loop:[violet:42]:010302|Av⟩, ⟨loop:[red:33]:011401|Av⟩)
	# 	(⟨loop:[green:33]:012032|Av⟩, ⟨loop:[green:11]:002014|Av⟩, ⟨loop:[green:24]:010041|Av⟩, ⟨loop:[green:65]:101005|Av⟩, ⟨loop:[green:42]:020023|Av⟩)
	# 	(⟨loop:[blue:33]:012306|Av⟩, ⟨loop:[blue:11]:002106|Av⟩, ⟨loop:[blue:24]:010406|Av⟩, ⟨loop:[blue:65]:101006|Av⟩, ⟨loop:[blue:42]:020206|Av⟩)
	# 	-- : ⟨avtuples: 131 | chlen: 3 | avlen: 715 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 715 | tobex c: 127 r: 5.630⟩
	# 	-- : ⟨avtuples: 132 | chlen: 4 | avlen: 710 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 710 | tobex c: 127 r: 5.591⟩
	# 	-- : ⟨avtuples: 132 | chlen: 4 | avlen: 710 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 710 | tobex c: 127 r: 5.591⟩
	# 	== : ⟨avtuples: 395 | chlen: 11 | avlen: 2135 | chains: 1908 | s: 0 | c: 0 | z: 0 | r: 2135 | tobex c: 381 r: 16.811⟩
	#
	# ⟨cycle:150@01100§⟨chain:150|1/6⟩⟩
	# ⟨cycle:156@01110§⟨chain:156|1/6⟩⟩
	# ⟨cycle:162@01120§⟨chain:162|1/6⟩⟩
	# ⟨cycle:168@01130§⟨chain:168|1/6⟩⟩
	# ⟨cycle:174@01140§⟨chain:174|1/6⟩⟩
	# 	(⟨loop:[orange:11]:002100|Av⟩, ⟨loop:[yellow:24]:010004|Av⟩, ⟨loop:[indigo:65]:002002|Av⟩, ⟨loop:[violet:42]:010302|Av⟩, ⟨loop:[red:33]:011401|Av⟩)
	# 	(⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩)
	# 	(⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩)
	# 	-- : ⟨avtuples: 131 | chlen: 3 | avlen: 715 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 715 | tobex c: 127 r: 5.630⟩
	# 	-- : ⟨avtuples: 131 | chlen: 4 | avlen: 712 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 712 | tobex c: 127 r: 5.606⟩
	# 	-- : ⟨avtuples: 131 | chlen: 4 | avlen: 712 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 712 | tobex c: 127 r: 5.606⟩
	# 	== : ⟨avtuples: 393 | chlen: 11 | avlen: 2139 | chains: 1908 | s: 0 | c: 0 | z: 0 | r: 2139 | tobex c: 381 r: 16.843⟩
	#
	# ⟨cycle:222@01320§⟨chain:222|1/6⟩⟩
	# ⟨cycle:348@02330§⟨chain:348|1/6⟩⟩
	# ⟨cycle:426@10210§⟨chain:426|1/6⟩⟩
	# ⟨cycle:624@12040§⟨chain:624|1/6⟩⟩
	# ⟨cycle:660@12200§⟨chain:660|1/5⟩⟩
	# 	(⟨loop:[blue:71]:102106|Av⟩, ⟨loop:[blue:104]:120406|Av⟩, ⟨loop:[blue:110]:122006|Av⟩, ⟨loop:[blue:58]:023306|Av⟩, ⟨loop:[blue:37]:013206|Av⟩)
	# 	(⟨loop:[green:104]:120041|Av⟩, ⟨loop:[green:110]:122005|Av⟩, ⟨loop:[green:58]:023032|Av⟩, ⟨loop:[green:37]:013023|Av⟩, ⟨loop:[green:71]:102014|Av⟩)
	# 	(⟨loop:[yellow:104]:120004|Av⟩, ⟨loop:[indigo:110]:023002|Av⟩, ⟨loop:[violet:58]:013402|Av⟩, ⟨loop:[red:37]:013200|Av⟩, ⟨loop:[orange:71]:102100|Av⟩)
	# 	-- : ⟨avtuples: 131 | chlen: 4 | avlen: 712 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 712 | tobex c: 127 r: 5.606⟩
	# 	-- : ⟨avtuples: 132 | chlen: 4 | avlen: 717 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 717 | tobex c: 127 r: 5.646⟩
	# 	-- : ⟨avtuples: 133 | chlen: 4 | avlen: 714 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 714 | tobex c: 127 r: 5.622⟩
	# 	== : ⟨avtuples: 396 | chlen: 12 | avlen: 2143 | chains: 1908 | s: 0 | c: 0 | z: 0 | r: 2143 | tobex c: 381 r: 16.874⟩

	# min nodes: 69
	# ⟨node:1235064@001311§⟨chain:49|1/6⟩|A⟩
	# ⟨node:2350641@001312§⟨chain:49|1/6⟩|A⟩
	# ⟨node:3506412@001313§⟨chain:49|1/6⟩|A⟩		
	# …
				
	# ⟨001311, 001312, 001313⟩
	for loop in diagram.nodeByAddress['001311'].loop.tuple:
		assert diagram.extendLoop(loop)		
	
	# ===  2 ===================================================================================================================================================================== #
	
	# [*0*][0m2s.38][lvl:0#-1¹²⁸] [jump] -- init -- | ⟨⟨avtuples: 128 | chlen: 4 | avlen: 713 | chains: 636 | s: 0 | c: 0 | z: 0 | r: 713 | tobex c: 127 r: 5.614⟩⟩
	# viables: 121
	# unchained_cycles: 627
	# min_viable_tuple_count: 3 | min_cycles: 24 | grouped_cycles_per_matched_results: 5
		
	# ⟨cycle:59@00145§⟨chain:59|1/7⟩⟩
	# ⟨cycle:95@00305§⟨chain:95|1/7⟩⟩
	# ⟨cycle:293@02135§⟨chain:293|1/7⟩⟩
	# ⟨cycle:371@10015§⟨chain:371|1/6⟩⟩
	# ⟨cycle:497@11025§⟨chain:497|1/7⟩⟩
	# 	(⟨loop:[blue:15]:003006|Av⟩, ⟨loop:[blue:9]:001406|Av⟩, ⟨loop:[blue:61]:100106|Av⟩, ⟨loop:[blue:82]:110206|Av⟩, ⟨loop:[blue:48]:021306|Av⟩)
	# 	(⟨loop:[red:11]:002051|Av⟩, ⟨loop:[orange:24]:001454|Av⟩, ⟨loop:[yellow:65]:100154|Av⟩, ⟨loop:[indigo:42]:020151|Av⟩, ⟨loop:[violet:33]:012251|Av⟩)
	# 	(⟨loop:[yellow:40]:020040|Av⟩, ⟨loop:[indigo:31]:003052|Av⟩, ⟨loop:[violet:14]:001452|Av⟩, ⟨loop:[red:22]:010151|Av⟩, ⟨loop:[orange:68]:101251|Av⟩)
	# 	-- : ⟨avtuples: 124 | chlen: 3 | avlen: 675 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 675 | tobex c: 122 r: 5.533⟩
	# 	-- : ⟨avtuples: 123 | chlen: 4 | avlen: 678 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 678 | tobex c: 122 r: 5.557⟩
	# 	-- : ⟨avtuples: 124 | chlen: 4 | avlen: 679 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 679 | tobex c: 122 r: 5.566⟩
	# 	== : ⟨avtuples: 371 | chlen: 11 | avlen: 2032 | chains: 1833 | s: 0 | c: 0 | z: 0 | r: 2032 | tobex c: 366 r: 16.656⟩
	#
	# ⟨cycle:66@00210§⟨chain:66|1/7⟩⟩
	# ⟨cycle:144@01040§⟨chain:144|1/7⟩⟩
	# ⟨cycle:198@01230§⟨chain:198|1/7⟩⟩
	# ⟨cycle:252@02020§⟨chain:252|1/7⟩⟩
	# 	(⟨loop:[orange:11]:002100|Av⟩, ⟨loop:[yellow:24]:010004|Av⟩, ⟨loop:[indigo:65]:002002|Av⟩, ⟨loop:[violet:42]:010302|Av⟩, ⟨loop:[red:33]:011401|Av⟩)
	# 	(⟨loop:[green:33]:012032|Av⟩, ⟨loop:[green:11]:002014|Av⟩, ⟨loop:[green:24]:010041|Av⟩, ⟨loop:[green:65]:101005|Av⟩, ⟨loop:[green:42]:020023|Av⟩)
	# 	(⟨loop:[blue:33]:012306|Av⟩, ⟨loop:[blue:11]:002106|Av⟩, ⟨loop:[blue:24]:010406|Av⟩, ⟨loop:[blue:65]:101006|Av⟩, ⟨loop:[blue:42]:020206|Av⟩)
	# 	-- : ⟨avtuples: 123 | chlen: 3 | avlen: 682 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 682 | tobex c: 122 r: 5.590⟩
	# 	-- : ⟨avtuples: 123 | chlen: 4 | avlen: 676 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 676 | tobex c: 122 r: 5.541⟩
	# 	-- : ⟨avtuples: 123 | chlen: 3 | avlen: 676 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 676 | tobex c: 122 r: 5.541⟩
	# 	== : ⟨avtuples: 369 | chlen: 10 | avlen: 2034 | chains: 1833 | s: 0 | c: 0 | z: 0 | r: 2034 | tobex c: 366 r: 16.672⟩
	#
	# ⟨cycle:83@00235§⟨chain:83|1/6⟩⟩
	# ⟨cycle:131@01015§⟨chain:131|1/5⟩⟩
	# ⟨cycle:185@01205§⟨chain:185|1/6⟩⟩
	# ⟨cycle:269@02045§⟨chain:269|1/6⟩⟩
	# ⟨cycle:407@10125§⟨chain:407|1/6⟩⟩
	# 	(⟨loop:[orange:44]:002453|Av⟩, ⟨loop:[yellow:30]:010253|Av⟩, ⟨loop:[indigo:13]:002251|Av⟩, ⟨loop:[violet:21]:010051|Av⟩, ⟨loop:[red:67]:011254|Av⟩)
	# 	(⟨loop:[indigo:89]:020453|Av⟩, ⟨loop:[violet:106]:012053|Av⟩, ⟨loop:[red:98]:002353|Av⟩, ⟨loop:[orange:52]:001152|Av⟩, ⟨loop:[yellow:75]:100352|Av⟩)
	# 	(⟨loop:[yellow:40]:020040|Av⟩, ⟨loop:[indigo:31]:003052|Av⟩, ⟨loop:[violet:14]:001452|Av⟩, ⟨loop:[red:22]:010151|Av⟩, ⟨loop:[orange:68]:101251|Av⟩)
	# 	-- : ⟨avtuples: 123 | chlen: 3 | avlen: 683 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 683 | tobex c: 122 r: 5.598⟩
	# 	-- : ⟨avtuples: 123 | chlen: 4 | avlen: 678 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 678 | tobex c: 122 r: 5.557⟩
	# 	-- : ⟨avtuples: 124 | chlen: 4 | avlen: 679 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 679 | tobex c: 122 r: 5.566⟩
	# 	== : ⟨avtuples: 370 | chlen: 11 | avlen: 2040 | chains: 1833 | s: 0 | c: 0 | z: 0 | r: 2040 | tobex c: 366 r: 16.721⟩
	#
	# ⟨cycle:150@01100§⟨chain:150|1/5⟩⟩
	# ⟨cycle:156@01110§⟨chain:156|1/6⟩⟩
	# ⟨cycle:162@01120§⟨chain:162|1/6⟩⟩
	# ⟨cycle:168@01130§⟨chain:168|1/6⟩⟩
	# ⟨cycle:174@01140§⟨chain:174|1/6⟩⟩
	# 	(⟨loop:[orange:11]:002100|Av⟩, ⟨loop:[yellow:24]:010004|Av⟩, ⟨loop:[indigo:65]:002002|Av⟩, ⟨loop:[violet:42]:010302|Av⟩, ⟨loop:[red:33]:011401|Av⟩)
	# 	(⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩)
	# 	(⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩)
	# 	-- : ⟨avtuples: 123 | chlen: 3 | avlen: 682 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 682 | tobex c: 122 r: 5.590⟩
	# 	-- : ⟨avtuples: 122 | chlen: 3 | avlen: 678 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 678 | tobex c: 122 r: 5.557⟩
	# 	-- : ⟨avtuples: 122 | chlen: 3 | avlen: 678 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 678 | tobex c: 122 r: 5.557⟩
	# 	== : ⟨avtuples: 367 | chlen: 9 | avlen: 2038 | chains: 1833 | s: 0 | c: 0 | z: 0 | r: 2038 | tobex c: 366 r: 16.705⟩
	#
	# ⟨cycle:222@01320§⟨chain:222|1/6⟩⟩
	# ⟨cycle:348@02330§⟨chain:348|1/6⟩⟩
	# ⟨cycle:426@10210§⟨chain:426|1/6⟩⟩
	# ⟨cycle:624@12040§⟨chain:624|1/6⟩⟩
	# ⟨cycle:660@12200§⟨chain:660|1/4⟩⟩
	# 	(⟨loop:[blue:71]:102106|Av⟩, ⟨loop:[blue:104]:120406|Av⟩, ⟨loop:[blue:110]:122006|Av⟩, ⟨loop:[blue:58]:023306|Av⟩, ⟨loop:[blue:37]:013206|Av⟩)
	# 	(⟨loop:[green:104]:120041|Av⟩, ⟨loop:[green:110]:122005|Av⟩, ⟨loop:[green:58]:023032|Av⟩, ⟨loop:[green:37]:013023|Av⟩, ⟨loop:[green:71]:102014|Av⟩)
	# 	(⟨loop:[yellow:104]:120004|Av⟩, ⟨loop:[indigo:110]:023002|Av⟩, ⟨loop:[violet:58]:013402|Av⟩, ⟨loop:[red:37]:013200|Av⟩, ⟨loop:[orange:71]:102100|Av⟩)
	# 	-- : ⟨avtuples: 122 | chlen: 4 | avlen: 678 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 678 | tobex c: 122 r: 5.557⟩
	# 	-- : ⟨avtuples: 123 | chlen: 4 | avlen: 683 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 683 | tobex c: 122 r: 5.598⟩
	# 	-- : ⟨avtuples: 124 | chlen: 4 | avlen: 680 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 680 | tobex c: 122 r: 5.574⟩
	# 	== : ⟨avtuples: 369 | chlen: 12 | avlen: 2041 | chains: 1833 | s: 0 | c: 0 | z: 0 | r: 2041 | tobex c: 366 r: 16.730⟩

	# min nodes: 72
	# ⟨node:1230654@001452§⟨chain:59|1/7⟩|A⟩
	# ⟨node:3065412@001454§⟨chain:59|1/7⟩|A⟩
	# ⟨node:6541230@001456§⟨chain:59|1/7⟩|A⟩
	# …
				
	# ⟨001452, 001454, 001456⟩
	for loop in diagram.nodeByAddress['001452'].loop.tuple:
		assert diagram.extendLoop(loop)		
		
	# ===  3 ===================================================================================================================================================================== #	
	
	# [*0*][0m2s.30][lvl:0#-1¹²⁴] [jump] -- init -- | ⟨⟨avtuples: 124 | chlen: 4 | avlen: 679 | chains: 611 | s: 0 | c: 0 | z: 0 | r: 679 | tobex c: 122 r: 5.566⟩⟩
	# viables: 115
	# unchained_cycles: 597
	# min_viable_tuple_count: 3 | min_cycles: 19 | grouped_cycles_per_matched_results: 4
		
	# ⟨cycle:66@00210§⟨chain:66|1/7⟩⟩
	# ⟨cycle:144@01040§⟨chain:144|1/7⟩⟩
	# ⟨cycle:198@01230§⟨chain:198|1/7⟩⟩
	# ⟨cycle:252@02020§⟨chain:252|1/7⟩⟩
	# 	(⟨loop:[orange:11]:002100|Av⟩, ⟨loop:[yellow:24]:010004|Av⟩, ⟨loop:[indigo:65]:002002|Av⟩, ⟨loop:[violet:42]:010302|Av⟩, ⟨loop:[red:33]:011401|Av⟩)
	# 	(⟨loop:[green:33]:012032|Av⟩, ⟨loop:[green:11]:002014|Av⟩, ⟨loop:[green:24]:010041|Av⟩, ⟨loop:[green:65]:101005|Av⟩, ⟨loop:[green:42]:020023|Av⟩)
	# 	(⟨loop:[blue:33]:012306|Av⟩, ⟨loop:[blue:11]:002106|Av⟩, ⟨loop:[blue:24]:010406|Av⟩, ⟨loop:[blue:65]:101006|Av⟩, ⟨loop:[blue:42]:020206|Av⟩)
	# 	-- : ⟨avtuples: 119 | chlen: 3 | avlen: 648 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 648 | tobex c: 117 r: 5.538⟩
	# 	-- : ⟨avtuples: 119 | chlen: 4 | avlen: 642 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 642 | tobex c: 117 r: 5.487⟩
	# 	-- : ⟨avtuples: 119 | chlen: 3 | avlen: 642 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 642 | tobex c: 117 r: 5.487⟩
	# 	== : ⟨avtuples: 357 | chlen: 10 | avlen: 1932 | chains: 1758 | s: 0 | c: 0 | z: 0 | r: 1932 | tobex c: 351 r: 16.513⟩
	# 
	# ⟨cycle:150@01100§⟨chain:150|1/5⟩⟩
	# ⟨cycle:156@01110§⟨chain:156|1/6⟩⟩
	# ⟨cycle:162@01120§⟨chain:162|1/6⟩⟩
	# ⟨cycle:168@01130§⟨chain:168|1/6⟩⟩
	# ⟨cycle:174@01140§⟨chain:174|1/6⟩⟩
	# 	(⟨loop:[orange:11]:002100|Av⟩, ⟨loop:[yellow:24]:010004|Av⟩, ⟨loop:[indigo:65]:002002|Av⟩, ⟨loop:[violet:42]:010302|Av⟩, ⟨loop:[red:33]:011401|Av⟩)
	# 	(⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩)
	# 	(⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩)
	# 	-- : ⟨avtuples: 119 | chlen: 3 | avlen: 648 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 648 | tobex c: 117 r: 5.538⟩
	# 	-- : ⟨avtuples: 118 | chlen: 3 | avlen: 644 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 644 | tobex c: 117 r: 5.504⟩
	# 	-- : ⟨avtuples: 118 | chlen: 3 | avlen: 644 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 644 | tobex c: 117 r: 5.504⟩
	# 	== : ⟨avtuples: 355 | chlen: 9 | avlen: 1936 | chains: 1758 | s: 0 | c: 0 | z: 0 | r: 1936 | tobex c: 351 r: 16.547⟩
	# 
	# ⟨cycle:155@01105§⟨chain:155|1/6⟩⟩
	# ⟨cycle:161@01115§⟨chain:161|1/6⟩⟩
	# ⟨cycle:167@01125§⟨chain:167|1/6⟩⟩
	# ⟨cycle:173@01135§⟨chain:173|1/6⟩⟩
	# ⟨cycle:179@01145§⟨chain:179|1/6⟩⟩
	# 	(⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩)
	# 	(⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩)
	# 	(⟨loop:[yellow:20]:010040|Av⟩, ⟨loop:[indigo:66]:002053|Av⟩, ⟨loop:[violet:43]:010353|Av⟩, ⟨loop:[red:34]:011452|Av⟩, ⟨loop:[orange:12]:002151|Av⟩)
	# 	-- : ⟨avtuples: 118 | chlen: 3 | avlen: 644 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 644 | tobex c: 117 r: 5.504⟩
	# 	-- : ⟨avtuples: 118 | chlen: 3 | avlen: 644 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 644 | tobex c: 117 r: 5.504⟩
	# 	-- : ⟨avtuples: 120 | chlen: 3 | avlen: 654 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 654 | tobex c: 117 r: 5.590⟩
	# 	== : ⟨avtuples: 356 | chlen: 9 | avlen: 1942 | chains: 1758 | s: 0 | c: 0 | z: 0 | r: 1942 | tobex c: 351 r: 16.598⟩
	# 
	# ⟨cycle:222@01320§⟨chain:222|1/6⟩⟩
	# ⟨cycle:348@02330§⟨chain:348|1/6⟩⟩
	# ⟨cycle:426@10210§⟨chain:426|1/6⟩⟩
	# ⟨cycle:624@12040§⟨chain:624|1/6⟩⟩
	# ⟨cycle:660@12200§⟨chain:660|1/4⟩⟩
	# 	(⟨loop:[blue:71]:102106|Av⟩, ⟨loop:[blue:104]:120406|Av⟩, ⟨loop:[blue:110]:122006|Av⟩, ⟨loop:[blue:58]:023306|Av⟩, ⟨loop:[blue:37]:013206|Av⟩)
	# 	(⟨loop:[green:104]:120041|Av⟩, ⟨loop:[green:110]:122005|Av⟩, ⟨loop:[green:58]:023032|Av⟩, ⟨loop:[green:37]:013023|Av⟩, ⟨loop:[green:71]:102014|Av⟩)
	# 	(⟨loop:[yellow:104]:120004|Av⟩, ⟨loop:[indigo:110]:023002|Av⟩, ⟨loop:[violet:58]:013402|Av⟩, ⟨loop:[red:37]:013200|Av⟩, ⟨loop:[orange:71]:102100|Av⟩)
	# 	-- : ⟨avtuples: 119 | chlen: 4 | avlen: 649 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 649 | tobex c: 117 r: 5.547⟩
	# 	-- : ⟨avtuples: 119 | chlen: 4 | avlen: 649 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 649 | tobex c: 117 r: 5.547⟩
	# 	-- : ⟨avtuples: 120 | chlen: 4 | avlen: 646 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 646 | tobex c: 117 r: 5.521⟩
	# 	== : ⟨avtuples: 358 | chlen: 12 | avlen: 1944 | chains: 1758 | s: 0 | c: 0 | z: 0 | r: 1944 | tobex c: 351 r: 16.615⟩
	
	# min nodes: 57
	# ⟨node:3014256@002100§⟨chain:66|1/7⟩|A⟩
	# ⟨node:5630142@002105§⟨chain:66|1/7⟩|A⟩
	# ⟨node:6301425@002106§⟨chain:66|1/7⟩|A⟩	
	# …
				
	# ⟨002100, 002105, 002106⟩
	for loop in diagram.nodeByAddress['002100'].loop.tuple:
		assert diagram.extendLoop(loop)		
		
	# ===  4 ===================================================================================================================================================================== #
	
	# [*0*][0m1s.927][lvl:0#-1¹¹⁹] [jump] -- init -- | ⟨⟨avtuples: 119 | chlen: 3 | avlen: 648 | chains: 586 | s: 0 | c: 0 | z: 0 | r: 648 | tobex c: 117 r: 5.538⟩⟩
	# viables: 110
	# unchained_cycles: 568
	# min_viable_tuple_count: 3 | min_cycles: 30 | grouped_cycles_per_matched_results: 6
	
	# ⟨cycle:30@00100§⟨chain:30|1/3⟩⟩
	# ⟨cycle:96@00310§⟨chain:96|1/3⟩⟩
	# ⟨cycle:294@02140§⟨chain:294|1/3⟩⟩
	# ⟨cycle:372@10020§⟨chain:372|1/3⟩⟩
	# ⟨cycle:498@11030§⟨chain:498|1/3⟩⟩
	# 	(⟨loop:[green:16]:003014|Av⟩, ⟨loop:[green:5]:001005|Av⟩, ⟨loop:[green:62]:100023|Av⟩, ⟨loop:[green:83]:110032|Av⟩, ⟨loop:[green:49]:021041|Av⟩)
	# 	(⟨loop:[blue:49]:021406|Av⟩, ⟨loop:[blue:16]:003106|Av⟩, ⟨loop:[blue:5]:001006|Av⟩, ⟨loop:[blue:62]:100206|Av⟩, ⟨loop:[blue:83]:110306|Av⟩)
	# 	(⟨loop:[indigo:53]:021401|Av⟩, ⟨loop:[violet:76]:003101|Av⟩, ⟨loop:[red:85]:001001|Av⟩, ⟨loop:[orange:107]:100201|Av⟩, ⟨loop:[yellow:99]:110301|Av⟩)
	# 	-- : ⟨avtuples: 115 | chlen: 3 | avlen: 623 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 623 | tobex c: 112 r: 5.562⟩
	# 	-- : ⟨avtuples: 116 | chlen: 3 | avlen: 628 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 628 | tobex c: 112 r: 5.607⟩
	# 	-- : ⟨avtuples: 116 | chlen: 2 | avlen: 628 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 628 | tobex c: 112 r: 5.607⟩
	# 	== : ⟨avtuples: 347 | chlen: 8 | avlen: 1879 | chains: 1683 | s: 0 | c: 0 | z: 0 | r: 1879 | tobex c: 336 r: 16.777⟩
	# 
	# ⟨cycle:36@00110§⟨chain:36|1/4⟩⟩
	# ⟨cycle:102@00320§⟨chain:102|1/5⟩⟩
	# ⟨cycle:270@02100§⟨chain:270|1/3⟩⟩
	# ⟨cycle:378@10030§⟨chain:378|1/4⟩⟩
	# ⟨cycle:504@11040§⟨chain:504|1/5⟩⟩
	# 	(⟨loop:[indigo:45]:021000|Av⟩, ⟨loop:[violet:17]:003200|Av⟩, ⟨loop:[red:6]:001100|Av⟩, ⟨loop:[orange:63]:100300|Av⟩, ⟨loop:[yellow:84]:110004|Av⟩)
	# 	(⟨loop:[green:45]:021005|Av⟩, ⟨loop:[green:17]:003023|Av⟩, ⟨loop:[green:6]:001014|Av⟩, ⟨loop:[green:63]:100032|Av⟩, ⟨loop:[green:84]:110041|Av⟩)
	# 	(⟨loop:[blue:84]:110406|Av⟩, ⟨loop:[blue:45]:021006|Av⟩, ⟨loop:[blue:17]:003206|Av⟩, ⟨loop:[blue:6]:001106|Av⟩, ⟨loop:[blue:63]:100306|Av⟩)
	# 	-- : ⟨avtuples: 114 | chlen: 2 | avlen: 611 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 611 | tobex c: 112 r: 5.455⟩
	# 	-- : ⟨avtuples: 116 | chlen: 3 | avlen: 619 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 619 | tobex c: 112 r: 5.527⟩
	# 	-- : ⟨avtuples: 115 | chlen: 3 | avlen: 613 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 613 | tobex c: 112 r: 5.473⟩
	# 	== : ⟨avtuples: 345 | chlen: 8 | avlen: 1843 | chains: 1683 | s: 0 | c: 0 | z: 0 | r: 1843 | tobex c: 336 r: 16.455⟩
	# 
	# ⟨cycle:77@00225§⟨chain:77|1/4⟩⟩
	# ⟨cycle:125@01005§⟨chain:125|1/4⟩⟩
	# ⟨cycle:209@01245§⟨chain:209|1/4⟩⟩
	# ⟨cycle:263@02035§⟨chain:263|1/4⟩⟩
	# ⟨cycle:401@10115§⟨chain:401|1/4⟩⟩
	# 	(⟨loop:[yellow:20]:010040|Av⟩, ⟨loop:[indigo:66]:002053|Av⟩, ⟨loop:[violet:43]:010353|Av⟩, ⟨loop:[red:34]:011452|Av⟩, ⟨loop:[orange:12]:002151|Av⟩)
	# 	(⟨loop:[indigo:39]:003453|Av⟩, ⟨loop:[violet:73]:001353|Av⟩, ⟨loop:[red:101]:010052|Av⟩, ⟨loop:[orange:112]:101152|Av⟩, ⟨loop:[yellow:55]:020352|Av⟩)
	# 	(⟨loop:[violet:114]:012454|Av⟩, ⟨loop:[red:57]:002254|Av⟩, ⟨loop:[orange:36]:001053|Av⟩, ⟨loop:[yellow:70]:100253|Av⟩, ⟨loop:[indigo:103]:020354|Av⟩)
	# 	-- : ⟨avtuples: 115 | chlen: 3 | avlen: 623 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 623 | tobex c: 112 r: 5.562⟩
	# 	-- : ⟨avtuples: 114 | chlen: 3 | avlen: 618 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 618 | tobex c: 112 r: 5.518⟩
	# 	-- : ⟨avtuples: 115 | chlen: 3 | avlen: 623 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 623 | tobex c: 112 r: 5.562⟩
	# 	== : ⟨avtuples: 344 | chlen: 9 | avlen: 1864 | chains: 1683 | s: 0 | c: 0 | z: 0 | r: 1864 | tobex c: 336 r: 16.643⟩
	# 
	# ⟨cycle:82@00234§⟨chain:82|1/4⟩⟩
	# ⟨cycle:130@01014§⟨chain:130|1/4⟩⟩
	# ⟨cycle:184@01204§⟨chain:184|1/4⟩⟩
	# ⟨cycle:268@02044§⟨chain:268|1/4⟩⟩
	# ⟨cycle:406@10124§⟨chain:406|1/4⟩⟩
	# 	(⟨loop:[violet:44]:010443|Av⟩, ⟨loop:[red:30]:011042|Av⟩, ⟨loop:[orange:13]:002330|Av⟩, ⟨loop:[yellow:21]:010130|Av⟩, ⟨loop:[indigo:67]:002143|Av⟩)
	# 	(⟨loop:[red:102]:010142|Av⟩, ⟨loop:[orange:113]:101242|Av⟩, ⟨loop:[yellow:56]:020031|Av⟩, ⟨loop:[indigo:35]:003043|Av⟩, ⟨loop:[violet:74]:001443|Av⟩)
	# 	(⟨loop:[orange:37]:001143|Av⟩, ⟨loop:[yellow:71]:100343|Av⟩, ⟨loop:[indigo:104]:020444|Av⟩, ⟨loop:[violet:110]:012044|Av⟩, ⟨loop:[red:58]:002344|Av⟩)
	# 	-- : ⟨avtuples: 114 | chlen: 3 | avlen: 618 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 618 | tobex c: 112 r: 5.518⟩
	# 	-- : ⟨avtuples: 115 | chlen: 3 | avlen: 623 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 623 | tobex c: 112 r: 5.562⟩
	# 	-- : ⟨avtuples: 114 | chlen: 2 | avlen: 618 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 618 | tobex c: 112 r: 5.518⟩
	# 	== : ⟨avtuples: 343 | chlen: 8 | avlen: 1859 | chains: 1683 | s: 0 | c: 0 | z: 0 | r: 1859 | tobex c: 336 r: 16.598⟩
	# 
	# ⟨cycle:155@01105§⟨chain:155|1/6⟩⟩
	# ⟨cycle:161@01115§⟨chain:161|1/6⟩⟩
	# ⟨cycle:167@01125§⟨chain:167|1/6⟩⟩
	# ⟨cycle:173@01135§⟨chain:173|1/6⟩⟩
	# ⟨cycle:179@01145§⟨chain:179|1/6⟩⟩
	# 	(⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩)
	# 	(⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩)
	# 	(⟨loop:[yellow:20]:010040|Av⟩, ⟨loop:[indigo:66]:002053|Av⟩, ⟨loop:[violet:43]:010353|Av⟩, ⟨loop:[red:34]:011452|Av⟩, ⟨loop:[orange:12]:002151|Av⟩)
	# 	-- : ⟨avtuples: 113 | chlen: 3 | avlen: 613 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 613 | tobex c: 112 r: 5.473⟩
	# 	-- : ⟨avtuples: 113 | chlen: 3 | avlen: 617 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 617 | tobex c: 112 r: 5.509⟩
	# 	-- : ⟨avtuples: 115 | chlen: 3 | avlen: 623 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 623 | tobex c: 112 r: 5.562⟩
	# 	== : ⟨avtuples: 341 | chlen: 9 | avlen: 1853 | chains: 1683 | s: 0 | c: 0 | z: 0 | r: 1853 | tobex c: 336 r: 16.545⟩
	# 
	# ⟨cycle:222@01320§⟨chain:222|1/5⟩⟩
	# ⟨cycle:348@02330§⟨chain:348|1/5⟩⟩
	# ⟨cycle:426@10210§⟨chain:426|1/5⟩⟩
	# ⟨cycle:624@12040§⟨chain:624|1/5⟩⟩
	# ⟨cycle:660@12200§⟨chain:660|1/3⟩⟩
	# 	(⟨loop:[blue:71]:102106|Av⟩, ⟨loop:[blue:104]:120406|Av⟩, ⟨loop:[blue:110]:122006|Av⟩, ⟨loop:[blue:58]:023306|Av⟩, ⟨loop:[blue:37]:013206|Av⟩)
	# 	(⟨loop:[green:104]:120041|Av⟩, ⟨loop:[green:110]:122005|Av⟩, ⟨loop:[green:58]:023032|Av⟩, ⟨loop:[green:37]:013023|Av⟩, ⟨loop:[green:71]:102014|Av⟩)
	# 	(⟨loop:[yellow:104]:120004|Av⟩, ⟨loop:[indigo:110]:023002|Av⟩, ⟨loop:[violet:58]:013402|Av⟩, ⟨loop:[red:37]:013200|Av⟩, ⟨loop:[orange:71]:102100|Av⟩)
	# 	-- : ⟨avtuples: 114 | chlen: 3 | avlen: 618 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 618 | tobex c: 112 r: 5.518⟩
	# 	-- : ⟨avtuples: 114 | chlen: 3 | avlen: 618 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 618 | tobex c: 112 r: 5.518⟩
	# 	-- : ⟨avtuples: 115 | chlen: 3 | avlen: 615 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 615 | tobex c: 112 r: 5.491⟩
	# 	== : ⟨avtuples: 343 | chlen: 9 | avlen: 1851 | chains: 1683 | s: 0 | c: 0 | z: 0 | r: 1851 | tobex c: 336 r: 16.527⟩
	
	# min nodes: 90
	# ⟨node:2304561@001001§⟨chain:30|1/3⟩|A⟩
	# ⟨node:5612304@001005§⟨chain:30|1/3⟩|A⟩
	# ⟨node:6123045@001006§⟨chain:30|1/3⟩|A⟩	
	# …
				
	# ⟨001001, 001005, 001006⟩
	for loop in diagram.nodeByAddress['001001'].loop.tuple:
		assert diagram.extendLoop(loop)		
		
	# ===  5 ===================================================================================================================================================================== #
	
	# [*0*][0m1s.938][lvl:0#-1¹¹⁶] [jump] -- init -- | ⟨⟨avtuples: 116 | chlen: 2 | avlen: 628 | chains: 561 | s: 0 | c: 0 | z: 0 | r: 628 | tobex c: 112 r: 5.607⟩⟩
	# viables: 105
	# unchained_cycles: 538
	# min_viable_tuple_count: 2 | min_cycles: 5 | grouped_cycles_per_matched_results: 1
	
	# ⟨cycle:36@00110§⟨chain:36|1/3⟩⟩
	# ⟨cycle:102@00320§⟨chain:102|1/4⟩⟩
	# ⟨cycle:270@02100§⟨chain:270|1/2⟩⟩
	# ⟨cycle:378@10030§⟨chain:378|1/3⟩⟩
	# ⟨cycle:504@11040§⟨chain:504|1/4⟩⟩
	# 	(⟨loop:[green:45]:021005|Av⟩, ⟨loop:[green:17]:003023|Av⟩, ⟨loop:[green:6]:001014|Av⟩, ⟨loop:[green:63]:100032|Av⟩, ⟨loop:[green:84]:110041|Av⟩)
	# 	(⟨loop:[blue:84]:110406|Av⟩, ⟨loop:[blue:45]:021006|Av⟩, ⟨loop:[blue:17]:003206|Av⟩, ⟨loop:[blue:6]:001106|Av⟩, ⟨loop:[blue:63]:100306|Av⟩)
	# 	-- : ⟨avtuples: 113 | chlen: 3 | avlen: 599 | chains: 536 | s: 0 | c: 0 | z: 0 | r: 599 | tobex c: 107 r: 5.598⟩
	# 	-- : ⟨avtuples: 113 | chlen: 3 | avlen: 598 | chains: 536 | s: 0 | c: 0 | z: 0 | r: 598 | tobex c: 107 r: 5.589⟩
	# 	== : ⟨avtuples: 226 | chlen: 6 | avlen: 1197 | chains: 1072 | s: 0 | c: 0 | z: 0 | r: 1197 | tobex c: 214 r: 11.187⟩
	
	# min nodes: 10
	# ⟨node:5623041@001105§⟨chain:36|1/3⟩|A⟩
	# ⟨node:6230415@001106§⟨chain:36|1/3⟩|A⟩
	# …	
	
	# ⟨001105, 001106⟩
	for loop in diagram.nodeByAddress['001105'].loop.tuple:
		assert diagram.extendLoop(loop)			
	
	# ===  6 ===================================================================================================================================================================== #
	
	# [*0*][0m1s.883][lvl:0#-1¹¹³] [jump] -- init -- | ⟨⟨avtuples: 113 | chlen: 3 | avlen: 599 | chains: 536 | s: 0 | c: 0 | z: 0 | r: 599 | tobex c: 107 r: 5.598⟩⟩
	# viables: 101
	# unchained_cycles: 508
	# min_viable_tuple_count: 3 | min_cycles: 38 | grouped_cycles_per_matched_results: 8

	# ⟨cycle:37@00111§⟨chain:37|1/4⟩⟩
	# ⟨cycle:103@00321§⟨chain:103|1/4⟩⟩
	# ⟨cycle:271@02101§⟨chain:271|1/4⟩⟩
	# ⟨cycle:379@10031§⟨chain:379|1/4⟩⟩
	# ⟨cycle:505@11041§⟨chain:505|1/4⟩⟩
	# 	(⟨loop:[violet:45]:012011|Av⟩, ⟨loop:[red:17]:002311|Av⟩, ⟨loop:[orange:6]:001110|Av⟩, ⟨loop:[yellow:63]:100310|Av⟩, ⟨loop:[indigo:84]:020411|Av⟩)
	# 	(⟨loop:[indigo:76]:003124|Av⟩, ⟨loop:[violet:85]:001024|Av⟩, ⟨loop:[red:107]:010312|Av⟩, ⟨loop:[orange:99]:101412|Av⟩, ⟨loop:[yellow:53]:020112|Av⟩)
	# 	(⟨loop:[green:80]:110005|Av⟩, ⟨loop:[green:46]:021014|Av⟩, ⟨loop:[green:18]:003032|Av⟩, ⟨loop:[green:7]:001023|Av⟩, ⟨loop:[green:64]:100041|Av⟩)
	# 	-- : ⟨avtuples: 109 | chlen: 3 | avlen: 572 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 572 | tobex c: 102 r: 5.608⟩
	# 	-- : ⟨avtuples: 108 | chlen: 3 | avlen: 564 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 564 | tobex c: 102 r: 5.529⟩
	# 	-- : ⟨avtuples: 110 | chlen: 3 | avlen: 566 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 566 | tobex c: 102 r: 5.549⟩
	# 	== : ⟨avtuples: 327 | chlen: 9 | avlen: 1702 | chains: 1533 | s: 0 | c: 0 | z: 0 | r: 1702 | tobex c: 306 r: 16.686⟩
	# 
	# ⟨cycle:39@00113§⟨chain:39|1/6⟩⟩
	# ⟨cycle:105@00323§⟨chain:105|1/6⟩⟩
	# ⟨cycle:273@02103§⟨chain:273|1/6⟩⟩
	# ⟨cycle:381@10033§⟨chain:381|1/5⟩⟩
	# ⟨cycle:507@11043§⟨chain:507|1/6⟩⟩
	# 	(⟨loop:[orange:69]:101430|Av⟩, ⟨loop:[yellow:41]:020130|Av⟩, ⟨loop:[indigo:32]:003142|Av⟩, ⟨loop:[violet:10]:001042|Av⟩, ⟨loop:[red:23]:010330|Av⟩)
	# 	(⟨loop:[yellow:92]:110022|Av⟩, ⟨loop:[indigo:90]:021033|Av⟩, ⟨loop:[violet:93]:003233|Av⟩, ⟨loop:[red:91]:001133|Av⟩, ⟨loop:[orange:94]:100333|Av⟩)
	# 	(⟨loop:[indigo:44]:020420|Av⟩, ⟨loop:[violet:30]:012020|Av⟩, ⟨loop:[red:13]:002320|Av⟩, ⟨loop:[orange:21]:001134|Av⟩, ⟨loop:[yellow:67]:100334|Av⟩)
	# 	-- : ⟨avtuples: 109 | chlen: 3 | avlen: 565 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 565 | tobex c: 102 r: 5.539⟩
	# 	-- : ⟨avtuples: 108 | chlen: 3 | avlen: 565 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 565 | tobex c: 102 r: 5.539⟩
	# 	-- : ⟨avtuples: 110 | chlen: 3 | avlen: 574 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 574 | tobex c: 102 r: 5.627⟩
	# 	== : ⟨avtuples: 327 | chlen: 9 | avlen: 1704 | chains: 1533 | s: 0 | c: 0 | z: 0 | r: 1704 | tobex c: 306 r: 16.706⟩
	# 
	# ⟨cycle:42@00120§⟨chain:42|1/5⟩⟩
	# ⟨cycle:108@00330§⟨chain:108|1/5⟩⟩
	# ⟨cycle:276@02110§⟨chain:276|1/6⟩⟩
	# ⟨cycle:384@10040§⟨chain:384|1/6⟩⟩
	# 	(⟨loop:[yellow:64]:100004|Av⟩, ⟨loop:[indigo:80]:020001|Av⟩, ⟨loop:[violet:46]:012101|Av⟩, ⟨loop:[red:18]:002401|Av⟩, ⟨loop:[orange:7]:001200|Av⟩)
	# 	(⟨loop:[green:80]:110005|Av⟩, ⟨loop:[green:46]:021014|Av⟩, ⟨loop:[green:18]:003032|Av⟩, ⟨loop:[green:7]:001023|Av⟩, ⟨loop:[green:64]:100041|Av⟩)
	# 	(⟨loop:[blue:64]:100406|Av⟩, ⟨loop:[blue:80]:110006|Av⟩, ⟨loop:[blue:46]:021106|Av⟩, ⟨loop:[blue:18]:003306|Av⟩, ⟨loop:[blue:7]:001206|Av⟩)
	# 	-- : ⟨avtuples: 103 | chlen: 2 | avlen: 546 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 546 | tobex c: 102 r: 5.353⟩
	# 	-- : ⟨avtuples: 110 | chlen: 3 | avlen: 566 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 566 | tobex c: 102 r: 5.549⟩
	# 	-- : ⟨avtuples: 108 | chlen: 2 | avlen: 566 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 566 | tobex c: 102 r: 5.549⟩
	# 	== : ⟨avtuples: 321 | chlen: 7 | avlen: 1678 | chains: 1533 | s: 0 | c: 0 | z: 0 | r: 1678 | tobex c: 306 r: 16.451⟩
	# 
	# ⟨cycle:48@00130§⟨chain:48|1/6⟩⟩
	# ⟨cycle:114@00340§⟨chain:114|1/6⟩⟩
	# ⟨cycle:282@02120§⟨chain:282|1/6⟩⟩
	# ⟨cycle:486@11010§⟨chain:486|1/6⟩⟩
	# 	(⟨loop:[red:100]:010001|Av⟩, ⟨loop:[orange:111]:101101|Av⟩, ⟨loop:[yellow:59]:020301|Av⟩, ⟨loop:[indigo:38]:003402|Av⟩, ⟨loop:[violet:72]:001302|Av⟩)
	# 	(⟨loop:[yellow:64]:100004|Av⟩, ⟨loop:[indigo:80]:020001|Av⟩, ⟨loop:[violet:46]:012101|Av⟩, ⟨loop:[red:18]:002401|Av⟩, ⟨loop:[orange:7]:001200|Av⟩)
	# 	(⟨loop:[green:60]:100005|Av⟩, ⟨loop:[green:81]:110014|Av⟩, ⟨loop:[green:47]:021023|Av⟩, ⟨loop:[green:19]:003041|Av⟩, ⟨loop:[green:8]:001032|Av⟩)
	# 	-- : ⟨avtuples: 104 | chlen: 3 | avlen: 561 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 561 | tobex c: 102 r: 5.500⟩
	# 	-- : ⟨avtuples: 103 | chlen: 2 | avlen: 546 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 546 | tobex c: 102 r: 5.353⟩
	# 	-- : ⟨avtuples: 109 | chlen: 3 | avlen: 567 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 567 | tobex c: 102 r: 5.559⟩
	# 	== : ⟨avtuples: 316 | chlen: 8 | avlen: 1674 | chains: 1533 | s: 0 | c: 0 | z: 0 | r: 1674 | tobex c: 306 r: 16.412⟩
	# 
	# ⟨cycle:77@00225§⟨chain:77|1/4⟩⟩
	# ⟨cycle:125@01005§⟨chain:125|1/4⟩⟩
	# ⟨cycle:209@01245§⟨chain:209|1/4⟩⟩
	# ⟨cycle:263@02035§⟨chain:263|1/4⟩⟩
	# ⟨cycle:401@10115§⟨chain:401|1/4⟩⟩
	# 	(⟨loop:[yellow:20]:010040|Av⟩, ⟨loop:[indigo:66]:002053|Av⟩, ⟨loop:[violet:43]:010353|Av⟩, ⟨loop:[red:34]:011452|Av⟩, ⟨loop:[orange:12]:002151|Av⟩)
	# 	(⟨loop:[indigo:39]:003453|Av⟩, ⟨loop:[violet:73]:001353|Av⟩, ⟨loop:[red:101]:010052|Av⟩, ⟨loop:[orange:112]:101152|Av⟩, ⟨loop:[yellow:55]:020352|Av⟩)
	# 	(⟨loop:[violet:114]:012454|Av⟩, ⟨loop:[red:57]:002254|Av⟩, ⟨loop:[orange:36]:001053|Av⟩, ⟨loop:[yellow:70]:100253|Av⟩, ⟨loop:[indigo:103]:020354|Av⟩)
	# 	-- : ⟨avtuples: 109 | chlen: 3 | avlen: 574 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 574 | tobex c: 102 r: 5.627⟩
	# 	-- : ⟨avtuples: 108 | chlen: 3 | avlen: 569 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 569 | tobex c: 102 r: 5.578⟩
	# 	-- : ⟨avtuples: 109 | chlen: 3 | avlen: 574 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 574 | tobex c: 102 r: 5.627⟩
	# 	== : ⟨avtuples: 326 | chlen: 9 | avlen: 1717 | chains: 1533 | s: 0 | c: 0 | z: 0 | r: 1717 | tobex c: 306 r: 16.833⟩
	# 
	# ⟨cycle:82@00234§⟨chain:82|1/4⟩⟩
	# ⟨cycle:130@01014§⟨chain:130|1/4⟩⟩
	# ⟨cycle:184@01204§⟨chain:184|1/4⟩⟩
	# ⟨cycle:268@02044§⟨chain:268|1/4⟩⟩
	# ⟨cycle:406@10124§⟨chain:406|1/4⟩⟩
	# 	(⟨loop:[violet:44]:010443|Av⟩, ⟨loop:[red:30]:011042|Av⟩, ⟨loop:[orange:13]:002330|Av⟩, ⟨loop:[yellow:21]:010130|Av⟩, ⟨loop:[indigo:67]:002143|Av⟩)
	# 	(⟨loop:[red:102]:010142|Av⟩, ⟨loop:[orange:113]:101242|Av⟩, ⟨loop:[yellow:56]:020031|Av⟩, ⟨loop:[indigo:35]:003043|Av⟩, ⟨loop:[violet:74]:001443|Av⟩)
	# 	(⟨loop:[orange:37]:001143|Av⟩, ⟨loop:[yellow:71]:100343|Av⟩, ⟨loop:[indigo:104]:020444|Av⟩, ⟨loop:[violet:110]:012044|Av⟩, ⟨loop:[red:58]:002344|Av⟩)
	# 	-- : ⟨avtuples: 108 | chlen: 3 | avlen: 569 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 569 | tobex c: 102 r: 5.578⟩
	# 	-- : ⟨avtuples: 109 | chlen: 3 | avlen: 574 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 574 | tobex c: 102 r: 5.627⟩
	# 	-- : ⟨avtuples: 108 | chlen: 2 | avlen: 569 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 569 | tobex c: 102 r: 5.578⟩
	# 	== : ⟨avtuples: 325 | chlen: 8 | avlen: 1712 | chains: 1533 | s: 0 | c: 0 | z: 0 | r: 1712 | tobex c: 306 r: 16.784⟩
	# 
	# ⟨cycle:155@01105§⟨chain:155|1/6⟩⟩
	# ⟨cycle:161@01115§⟨chain:161|1/6⟩⟩
	# ⟨cycle:167@01125§⟨chain:167|1/6⟩⟩
	# ⟨cycle:173@01135§⟨chain:173|1/6⟩⟩
	# ⟨cycle:179@01145§⟨chain:179|1/6⟩⟩
	# 	(⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩)
	# 	(⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩)
	# 	(⟨loop:[yellow:20]:010040|Av⟩, ⟨loop:[indigo:66]:002053|Av⟩, ⟨loop:[violet:43]:010353|Av⟩, ⟨loop:[red:34]:011452|Av⟩, ⟨loop:[orange:12]:002151|Av⟩)
	# 	-- : ⟨avtuples: 107 | chlen: 2 | avlen: 564 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 564 | tobex c: 102 r: 5.529⟩
	# 	-- : ⟨avtuples: 107 | chlen: 2 | avlen: 568 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 568 | tobex c: 102 r: 5.569⟩
	# 	-- : ⟨avtuples: 109 | chlen: 3 | avlen: 574 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 574 | tobex c: 102 r: 5.627⟩
	# 	== : ⟨avtuples: 323 | chlen: 7 | avlen: 1706 | chains: 1533 | s: 0 | c: 0 | z: 0 | r: 1706 | tobex c: 306 r: 16.725⟩
	# 
	# ⟨cycle:222@01320§⟨chain:222|1/5⟩⟩
	# ⟨cycle:348@02330§⟨chain:348|1/5⟩⟩
	# ⟨cycle:426@10210§⟨chain:426|1/5⟩⟩
	# ⟨cycle:624@12040§⟨chain:624|1/5⟩⟩
	# ⟨cycle:660@12200§⟨chain:660|1/3⟩⟩
	# 	(⟨loop:[blue:71]:102106|Av⟩, ⟨loop:[blue:104]:120406|Av⟩, ⟨loop:[blue:110]:122006|Av⟩, ⟨loop:[blue:58]:023306|Av⟩, ⟨loop:[blue:37]:013206|Av⟩)
	# 	(⟨loop:[green:104]:120041|Av⟩, ⟨loop:[green:110]:122005|Av⟩, ⟨loop:[green:58]:023032|Av⟩, ⟨loop:[green:37]:013023|Av⟩, ⟨loop:[green:71]:102014|Av⟩)
	# 	(⟨loop:[yellow:104]:120004|Av⟩, ⟨loop:[indigo:110]:023002|Av⟩, ⟨loop:[violet:58]:013402|Av⟩, ⟨loop:[red:37]:013200|Av⟩, ⟨loop:[orange:71]:102100|Av⟩)
	# 	-- : ⟨avtuples: 108 | chlen: 3 | avlen: 569 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 569 | tobex c: 102 r: 5.578⟩
	# 	-- : ⟨avtuples: 108 | chlen: 4 | avlen: 569 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 569 | tobex c: 102 r: 5.578⟩
	# 	-- : ⟨avtuples: 109 | chlen: 4 | avlen: 566 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 566 | tobex c: 102 r: 5.549⟩
	# 	== : ⟨avtuples: 325 | chlen: 11 | avlen: 1704 | chains: 1533 | s: 0 | c: 0 | z: 0 | r: 1704 | tobex c: 306 r: 16.706⟩

	# min nodes: 114
	# ⟨node:3041526@001110§⟨chain:37|1/4⟩|A⟩
	# ⟨node:1526304@001113§⟨chain:37|1/4⟩|A⟩
	# ⟨node:5263041@001114§⟨chain:37|1/4⟩|A⟩
	# …	
		
	# ⟨001110, 001113, 001114⟩
	for loop in diagram.nodeByAddress['001110'].loop.tuple:
		assert diagram.extendLoop(loop)		
			
	# ===  7 ===================================================================================================================================================================== #
	
	# [*0*][0m1s.854][lvl:0#-1¹⁰⁹] [jump] -- init -- | ⟨⟨avtuples: 109 | chlen: 3 | avlen: 572 | chains: 511 | s: 0 | c: 0 | z: 0 | r: 572 | tobex c: 102 r: 5.608⟩⟩
	# viables: 95
	# unchained_cycles: 483
	# min_viable_tuple_count: 3 | min_cycles: 38 | grouped_cycles_per_matched_results: 8
	
	# ⟨cycle:39@00113§⟨chain:39|1/5⟩⟩
	# ⟨cycle:105@00323§⟨chain:105|1/6⟩⟩
	# ⟨cycle:273@02103§⟨chain:273|1/6⟩⟩
	# ⟨cycle:381@10033§⟨chain:381|1/5⟩⟩
	# ⟨cycle:507@11043§⟨chain:507|1/6⟩⟩
	# 	(⟨loop:[orange:69]:101430|Av⟩, ⟨loop:[yellow:41]:020130|Av⟩, ⟨loop:[indigo:32]:003142|Av⟩, ⟨loop:[violet:10]:001042|Av⟩, ⟨loop:[red:23]:010330|Av⟩)
	# 	(⟨loop:[yellow:92]:110022|Av⟩, ⟨loop:[indigo:90]:021033|Av⟩, ⟨loop:[violet:93]:003233|Av⟩, ⟨loop:[red:91]:001133|Av⟩, ⟨loop:[orange:94]:100333|Av⟩)
	# 	(⟨loop:[indigo:44]:020420|Av⟩, ⟨loop:[violet:30]:012020|Av⟩, ⟨loop:[red:13]:002320|Av⟩, ⟨loop:[orange:21]:001134|Av⟩, ⟨loop:[yellow:67]:100334|Av⟩)
	# 	-- : ⟨avtuples: 105 | chlen: 3 | avlen: 538 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 538 | tobex c: 97 r: 5.546⟩
	# 	-- : ⟨avtuples: 104 | chlen: 2 | avlen: 538 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 538 | tobex c: 97 r: 5.546⟩
	# 	-- : ⟨avtuples: 106 | chlen: 3 | avlen: 548 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 548 | tobex c: 97 r: 5.649⟩
	# 	== : ⟨avtuples: 315 | chlen: 8 | avlen: 1624 | chains: 1458 | s: 0 | c: 0 | z: 0 | r: 1624 | tobex c: 291 r: 16.742⟩
	# 
	# ⟨cycle:42@00120§⟨chain:42|1/5⟩⟩
	# ⟨cycle:108@00330§⟨chain:108|1/5⟩⟩
	# ⟨cycle:276@02110§⟨chain:276|1/6⟩⟩
	# ⟨cycle:384@10040§⟨chain:384|1/6⟩⟩
	# 	(⟨loop:[yellow:64]:100004|Av⟩, ⟨loop:[indigo:80]:020001|Av⟩, ⟨loop:[violet:46]:012101|Av⟩, ⟨loop:[red:18]:002401|Av⟩, ⟨loop:[orange:7]:001200|Av⟩)
	# 	(⟨loop:[green:80]:110005|Av⟩, ⟨loop:[green:46]:021014|Av⟩, ⟨loop:[green:18]:003032|Av⟩, ⟨loop:[green:7]:001023|Av⟩, ⟨loop:[green:64]:100041|Av⟩)
	# 	(⟨loop:[blue:64]:100406|Av⟩, ⟨loop:[blue:80]:110006|Av⟩, ⟨loop:[blue:46]:021106|Av⟩, ⟨loop:[blue:18]:003306|Av⟩, ⟨loop:[blue:7]:001206|Av⟩)
	# 	-- : ⟨avtuples: 94 | chlen: 2 | avlen: 499 | chains: 486 | s: 0 | c: 0 | z: 1 | r: 499 | tobex c: 97 r: 5.144⟩
	# 	-- : ⟨avtuples: 101 | chlen: 2 | avlen: 520 | chains: 486 | s: 0 | c: 1 | z: 4 | r: 520 | tobex c: 97 r: 5.361⟩
	# 	-- : ⟨avtuples: 104 | chlen: 3 | avlen: 540 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 540 | tobex c: 97 r: 5.567⟩
	# 	== : ⟨avtuples: 299 | chlen: 7 | avlen: 1559 | chains: 1458 | s: 0 | c: 1 | z: 5 | r: 1559 | tobex c: 291 r: 16.072⟩
	# 
	# ⟨cycle:48@00130§⟨chain:48|1/6⟩⟩
	# ⟨cycle:114@00340§⟨chain:114|1/6⟩⟩
	# ⟨cycle:282@02120§⟨chain:282|1/6⟩⟩
	# ⟨cycle:486@11010§⟨chain:486|1/6⟩⟩
	# 	(⟨loop:[red:100]:010001|Av⟩, ⟨loop:[orange:111]:101101|Av⟩, ⟨loop:[yellow:59]:020301|Av⟩, ⟨loop:[indigo:38]:003402|Av⟩, ⟨loop:[violet:72]:001302|Av⟩)
	# 	(⟨loop:[yellow:64]:100004|Av⟩, ⟨loop:[indigo:80]:020001|Av⟩, ⟨loop:[violet:46]:012101|Av⟩, ⟨loop:[red:18]:002401|Av⟩, ⟨loop:[orange:7]:001200|Av⟩)
	# 	(⟨loop:[green:60]:100005|Av⟩, ⟨loop:[green:81]:110014|Av⟩, ⟨loop:[green:47]:021023|Av⟩, ⟨loop:[green:19]:003041|Av⟩, ⟨loop:[green:8]:001032|Av⟩)
	# 	-- : ⟨avtuples: 100 | chlen: 3 | avlen: 534 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 534 | tobex c: 97 r: 5.505⟩
	# 	-- : ⟨avtuples: 94 | chlen: 2 | avlen: 499 | chains: 486 | s: 0 | c: 0 | z: 1 | r: 499 | tobex c: 97 r: 5.144⟩
	# 	-- : ⟨avtuples: 103 | chlen: 3 | avlen: 533 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 533 | tobex c: 97 r: 5.495⟩
	# 	== : ⟨avtuples: 297 | chlen: 8 | avlen: 1566 | chains: 1458 | s: 0 | c: 0 | z: 1 | r: 1566 | tobex c: 291 r: 16.144⟩
	# 
	# ⟨cycle:68@00212§⟨chain:68|1/3⟩⟩
	# ⟨cycle:146@01042§⟨chain:146|1/3⟩⟩
	# ⟨cycle:200@01232§⟨chain:200|1/3⟩⟩
	# ⟨cycle:254@02022§⟨chain:254|1/3⟩⟩
	# ⟨cycle:392@10102§⟨chain:392|1/3⟩⟩
	# 	(⟨loop:[red:29]:011410|Av⟩, ⟨loop:[orange:26]:002124|Av⟩, ⟨loop:[yellow:28]:010013|Av⟩, ⟨loop:[indigo:25]:002011|Av⟩, ⟨loop:[violet:27]:010311|Av⟩)
	# 	(⟨loop:[yellow:42]:020220|Av⟩, ⟨loop:[indigo:33]:003321|Av⟩, ⟨loop:[violet:11]:001221|Av⟩, ⟨loop:[red:24]:010420|Av⟩, ⟨loop:[orange:65]:101020|Av⟩)
	# 	(⟨loop:[orange:54]:001421|Av⟩, ⟨loop:[yellow:77]:100121|Av⟩, ⟨loop:[indigo:86]:020133|Av⟩, ⟨loop:[violet:108]:012233|Av⟩, ⟨loop:[red:95]:002033|Av⟩)
	# 	-- : ⟨avtuples: 104 | chlen: 3 | avlen: 545 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 545 | tobex c: 97 r: 5.619⟩
	# 	-- : ⟨avtuples: 106 | chlen: 3 | avlen: 548 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 548 | tobex c: 97 r: 5.649⟩
	# 	-- : ⟨avtuples: 105 | chlen: 3 | avlen: 542 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 542 | tobex c: 97 r: 5.588⟩
	# 	== : ⟨avtuples: 315 | chlen: 9 | avlen: 1635 | chains: 1458 | s: 0 | c: 0 | z: 0 | r: 1635 | tobex c: 291 r: 16.856⟩
	# 
	# ⟨cycle:77@00225§⟨chain:77|1/4⟩⟩
	# ⟨cycle:125@01005§⟨chain:125|1/4⟩⟩
	# ⟨cycle:209@01245§⟨chain:209|1/4⟩⟩
	# ⟨cycle:263@02035§⟨chain:263|1/4⟩⟩
	# ⟨cycle:401@10115§⟨chain:401|1/4⟩⟩
	# 	(⟨loop:[yellow:20]:010040|Av⟩, ⟨loop:[indigo:66]:002053|Av⟩, ⟨loop:[violet:43]:010353|Av⟩, ⟨loop:[red:34]:011452|Av⟩, ⟨loop:[orange:12]:002151|Av⟩)
	# 	(⟨loop:[indigo:39]:003453|Av⟩, ⟨loop:[violet:73]:001353|Av⟩, ⟨loop:[red:101]:010052|Av⟩, ⟨loop:[orange:112]:101152|Av⟩, ⟨loop:[yellow:55]:020352|Av⟩)
	# 	(⟨loop:[violet:114]:012454|Av⟩, ⟨loop:[red:57]:002254|Av⟩, ⟨loop:[orange:36]:001053|Av⟩, ⟨loop:[yellow:70]:100253|Av⟩, ⟨loop:[indigo:103]:020354|Av⟩)
	# 	-- : ⟨avtuples: 105 | chlen: 3 | avlen: 547 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 547 | tobex c: 97 r: 5.639⟩
	# 	-- : ⟨avtuples: 104 | chlen: 3 | avlen: 542 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 542 | tobex c: 97 r: 5.588⟩
	# 	-- : ⟨avtuples: 105 | chlen: 3 | avlen: 547 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 547 | tobex c: 97 r: 5.639⟩
	# 	== : ⟨avtuples: 314 | chlen: 9 | avlen: 1636 | chains: 1458 | s: 0 | c: 0 | z: 0 | r: 1636 | tobex c: 291 r: 16.866⟩
	# 
	# ⟨cycle:82@00234§⟨chain:82|1/4⟩⟩
	# ⟨cycle:130@01014§⟨chain:130|1/4⟩⟩
	# ⟨cycle:184@01204§⟨chain:184|1/4⟩⟩
	# ⟨cycle:268@02044§⟨chain:268|1/4⟩⟩
	# ⟨cycle:406@10124§⟨chain:406|1/4⟩⟩
	# 	(⟨loop:[violet:44]:010443|Av⟩, ⟨loop:[red:30]:011042|Av⟩, ⟨loop:[orange:13]:002330|Av⟩, ⟨loop:[yellow:21]:010130|Av⟩, ⟨loop:[indigo:67]:002143|Av⟩)
	# 	(⟨loop:[red:102]:010142|Av⟩, ⟨loop:[orange:113]:101242|Av⟩, ⟨loop:[yellow:56]:020031|Av⟩, ⟨loop:[indigo:35]:003043|Av⟩, ⟨loop:[violet:74]:001443|Av⟩)
	# 	(⟨loop:[orange:37]:001143|Av⟩, ⟨loop:[yellow:71]:100343|Av⟩, ⟨loop:[indigo:104]:020444|Av⟩, ⟨loop:[violet:110]:012044|Av⟩, ⟨loop:[red:58]:002344|Av⟩)
	# 	-- : ⟨avtuples: 104 | chlen: 3 | avlen: 542 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 542 | tobex c: 97 r: 5.588⟩
	# 	-- : ⟨avtuples: 105 | chlen: 3 | avlen: 547 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 547 | tobex c: 97 r: 5.639⟩
	# 	-- : ⟨avtuples: 104 | chlen: 2 | avlen: 542 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 542 | tobex c: 97 r: 5.588⟩
	# 	== : ⟨avtuples: 313 | chlen: 8 | avlen: 1631 | chains: 1458 | s: 0 | c: 0 | z: 0 | r: 1631 | tobex c: 291 r: 16.814⟩
	# 
	# ⟨cycle:155@01105§⟨chain:155|1/6⟩⟩
	# ⟨cycle:161@01115§⟨chain:161|1/6⟩⟩
	# ⟨cycle:167@01125§⟨chain:167|1/6⟩⟩
	# ⟨cycle:173@01135§⟨chain:173|1/6⟩⟩
	# ⟨cycle:179@01145§⟨chain:179|1/6⟩⟩
	# 	(⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩)
	# 	(⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩)
	# 	(⟨loop:[yellow:20]:010040|Av⟩, ⟨loop:[indigo:66]:002053|Av⟩, ⟨loop:[violet:43]:010353|Av⟩, ⟨loop:[red:34]:011452|Av⟩, ⟨loop:[orange:12]:002151|Av⟩)
	# 	-- : ⟨avtuples: 104 | chlen: 2 | avlen: 542 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 542 | tobex c: 97 r: 5.588⟩
	# 	-- : ⟨avtuples: 104 | chlen: 2 | avlen: 546 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 546 | tobex c: 97 r: 5.629⟩
	# 	-- : ⟨avtuples: 105 | chlen: 3 | avlen: 547 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 547 | tobex c: 97 r: 5.639⟩
	# 	== : ⟨avtuples: 313 | chlen: 7 | avlen: 1635 | chains: 1458 | s: 0 | c: 0 | z: 0 | r: 1635 | tobex c: 291 r: 16.856⟩
	# 
	# ⟨cycle:222@01320§⟨chain:222|1/5⟩⟩
	# ⟨cycle:348@02330§⟨chain:348|1/5⟩⟩
	# ⟨cycle:426@10210§⟨chain:426|1/5⟩⟩
	# ⟨cycle:624@12040§⟨chain:624|1/5⟩⟩
	# ⟨cycle:660@12200§⟨chain:660|1/3⟩⟩
	# 	(⟨loop:[blue:71]:102106|Av⟩, ⟨loop:[blue:104]:120406|Av⟩, ⟨loop:[blue:110]:122006|Av⟩, ⟨loop:[blue:58]:023306|Av⟩, ⟨loop:[blue:37]:013206|Av⟩)
	# 	(⟨loop:[green:104]:120041|Av⟩, ⟨loop:[green:110]:122005|Av⟩, ⟨loop:[green:58]:023032|Av⟩, ⟨loop:[green:37]:013023|Av⟩, ⟨loop:[green:71]:102014|Av⟩)
	# 	(⟨loop:[yellow:104]:120004|Av⟩, ⟨loop:[indigo:110]:023002|Av⟩, ⟨loop:[violet:58]:013402|Av⟩, ⟨loop:[red:37]:013200|Av⟩, ⟨loop:[orange:71]:102100|Av⟩)
	# 	-- : ⟨avtuples: 104 | chlen: 3 | avlen: 538 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 538 | tobex c: 97 r: 5.546⟩
	# 	-- : ⟨avtuples: 104 | chlen: 3 | avlen: 542 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 542 | tobex c: 97 r: 5.588⟩
	# 	-- : ⟨avtuples: 102 | chlen: 3 | avlen: 520 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 520 | tobex c: 97 r: 5.361⟩
	# 	== : ⟨avtuples: 310 | chlen: 9 | avlen: 1600 | chains: 1458 | s: 0 | c: 0 | z: 0 | r: 1600 | tobex c: 291 r: 16.495⟩
	
	# min nodes: 114
	# ⟨node:1523064@001131§⟨chain:39|1/5⟩|A⟩
	# ⟨node:2306415@001133§⟨chain:39|1/5⟩|A⟩
	# ⟨node:3064152@001134§⟨chain:39|1/5⟩|A⟩	
	# … 
		
	# ⟨001131, 001133, 001134⟩
	for loop in diagram.nodeByAddress['001131'].loop.tuple:
		assert diagram.extendLoop(loop)		
			
	# ===  8 ===================================================================================================================================================================== #
	
	# [*0*][0m1s.797][lvl:0#-1¹⁰⁵] [jump] -- init -- | ⟨⟨avtuples: 105 | chlen: 3 | avlen: 538 | chains: 486 | s: 0 | c: 0 | z: 0 | r: 538 | tobex c: 97 r: 5.546⟩⟩
	# viables: 90
	# unchained_cycles: 453
	# min_viable_tuple_count: 3 | min_cycles: 33 | grouped_cycles_per_matched_results: 7
	
	# ⟨cycle:42@00120§⟨chain:42|1/5⟩⟩
	# ⟨cycle:108@00330§⟨chain:108|1/5⟩⟩
	# ⟨cycle:276@02110§⟨chain:276|1/6⟩⟩
	# ⟨cycle:384@10040§⟨chain:384|1/6⟩⟩
	# 	(⟨loop:[yellow:64]:100004|Av⟩, ⟨loop:[indigo:80]:020001|Av⟩, ⟨loop:[violet:46]:012101|Av⟩, ⟨loop:[red:18]:002401|Av⟩, ⟨loop:[orange:7]:001200|Av⟩)
	# 	(⟨loop:[green:80]:110005|Av⟩, ⟨loop:[green:46]:021014|Av⟩, ⟨loop:[green:18]:003032|Av⟩, ⟨loop:[green:7]:001023|Av⟩, ⟨loop:[green:64]:100041|Av⟩)
	# 	(⟨loop:[blue:64]:100406|Av⟩, ⟨loop:[blue:80]:110006|Av⟩, ⟨loop:[blue:46]:021106|Av⟩, ⟨loop:[blue:18]:003306|Av⟩, ⟨loop:[blue:7]:001206|Av⟩)
	# 	-- : ⟨avtuples: 90 | chlen: 2 | avlen: 464 | chains: 461 | s: 0 | c: 0 | z: 2 | r: 464 | tobex c: 92 r: 5.043⟩
	# 	-- : ⟨avtuples: 97 | chlen: 2 | avlen: 486 | chains: 461 | s: 0 | c: 1 | z: 4 | r: 486 | tobex c: 92 r: 5.283⟩
	# 	-- : ⟨avtuples: 100 | chlen: 3 | avlen: 507 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 507 | tobex c: 92 r: 5.511⟩
	# 	== : ⟨avtuples: 287 | chlen: 7 | avlen: 1457 | chains: 1383 | s: 0 | c: 1 | z: 6 | r: 1457 | tobex c: 276 r: 15.837⟩
	# 
	# ⟨cycle:48@00130§⟨chain:48|1/6⟩⟩
	# ⟨cycle:114@00340§⟨chain:114|1/6⟩⟩
	# ⟨cycle:282@02120§⟨chain:282|1/6⟩⟩
	# ⟨cycle:486@11010§⟨chain:486|1/6⟩⟩
	# 	(⟨loop:[red:100]:010001|Av⟩, ⟨loop:[orange:111]:101101|Av⟩, ⟨loop:[yellow:59]:020301|Av⟩, ⟨loop:[indigo:38]:003402|Av⟩, ⟨loop:[violet:72]:001302|Av⟩)
	# 	(⟨loop:[yellow:64]:100004|Av⟩, ⟨loop:[indigo:80]:020001|Av⟩, ⟨loop:[violet:46]:012101|Av⟩, ⟨loop:[red:18]:002401|Av⟩, ⟨loop:[orange:7]:001200|Av⟩)
	# 	(⟨loop:[green:60]:100005|Av⟩, ⟨loop:[green:81]:110014|Av⟩, ⟨loop:[green:47]:021023|Av⟩, ⟨loop:[green:19]:003041|Av⟩, ⟨loop:[green:8]:001032|Av⟩)
	# 	-- : ⟨avtuples: 96 | chlen: 3 | avlen: 500 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 500 | tobex c: 92 r: 5.435⟩
	# 	-- : ⟨avtuples: 90 | chlen: 2 | avlen: 464 | chains: 461 | s: 0 | c: 0 | z: 2 | r: 464 | tobex c: 92 r: 5.043⟩
	# 	-- : ⟨avtuples: 99 | chlen: 3 | avlen: 499 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 499 | tobex c: 92 r: 5.424⟩
	# 	== : ⟨avtuples: 285 | chlen: 8 | avlen: 1463 | chains: 1383 | s: 0 | c: 0 | z: 2 | r: 1463 | tobex c: 276 r: 15.902⟩
	# 
	# ⟨cycle:68@00212§⟨chain:68|1/3⟩⟩
	# ⟨cycle:146@01042§⟨chain:146|1/3⟩⟩
	# ⟨cycle:200@01232§⟨chain:200|1/3⟩⟩
	# ⟨cycle:254@02022§⟨chain:254|1/3⟩⟩
	# ⟨cycle:392@10102§⟨chain:392|1/3⟩⟩
	# 	(⟨loop:[red:29]:011410|Av⟩, ⟨loop:[orange:26]:002124|Av⟩, ⟨loop:[yellow:28]:010013|Av⟩, ⟨loop:[indigo:25]:002011|Av⟩, ⟨loop:[violet:27]:010311|Av⟩)
	# 	(⟨loop:[yellow:42]:020220|Av⟩, ⟨loop:[indigo:33]:003321|Av⟩, ⟨loop:[violet:11]:001221|Av⟩, ⟨loop:[red:24]:010420|Av⟩, ⟨loop:[orange:65]:101020|Av⟩)
	# 	(⟨loop:[orange:54]:001421|Av⟩, ⟨loop:[yellow:77]:100121|Av⟩, ⟨loop:[indigo:86]:020133|Av⟩, ⟨loop:[violet:108]:012233|Av⟩, ⟨loop:[red:95]:002033|Av⟩)
	# 	-- : ⟨avtuples: 100 | chlen: 3 | avlen: 511 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 511 | tobex c: 92 r: 5.554⟩
	# 	-- : ⟨avtuples: 102 | chlen: 3 | avlen: 514 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 514 | tobex c: 92 r: 5.587⟩
	# 	-- : ⟨avtuples: 101 | chlen: 3 | avlen: 513 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 513 | tobex c: 92 r: 5.576⟩
	# 	== : ⟨avtuples: 303 | chlen: 9 | avlen: 1538 | chains: 1383 | s: 0 | c: 0 | z: 0 | r: 1538 | tobex c: 276 r: 16.717⟩
	# 
	# ⟨cycle:77@00225§⟨chain:77|1/4⟩⟩
	# ⟨cycle:125@01005§⟨chain:125|1/4⟩⟩
	# ⟨cycle:209@01245§⟨chain:209|1/4⟩⟩
	# ⟨cycle:263@02035§⟨chain:263|1/4⟩⟩
	# ⟨cycle:401@10115§⟨chain:401|1/4⟩⟩
	# 	(⟨loop:[yellow:20]:010040|Av⟩, ⟨loop:[indigo:66]:002053|Av⟩, ⟨loop:[violet:43]:010353|Av⟩, ⟨loop:[red:34]:011452|Av⟩, ⟨loop:[orange:12]:002151|Av⟩)
	# 	(⟨loop:[indigo:39]:003453|Av⟩, ⟨loop:[violet:73]:001353|Av⟩, ⟨loop:[red:101]:010052|Av⟩, ⟨loop:[orange:112]:101152|Av⟩, ⟨loop:[yellow:55]:020352|Av⟩)
	# 	(⟨loop:[violet:114]:012454|Av⟩, ⟨loop:[red:57]:002254|Av⟩, ⟨loop:[orange:36]:001053|Av⟩, ⟨loop:[yellow:70]:100253|Av⟩, ⟨loop:[indigo:103]:020354|Av⟩)
	# 	-- : ⟨avtuples: 101 | chlen: 3 | avlen: 513 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 513 | tobex c: 92 r: 5.576⟩
	# 	-- : ⟨avtuples: 100 | chlen: 3 | avlen: 508 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 508 | tobex c: 92 r: 5.522⟩
	# 	-- : ⟨avtuples: 100 | chlen: 2 | avlen: 499 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 499 | tobex c: 92 r: 5.424⟩
	# 	== : ⟨avtuples: 301 | chlen: 8 | avlen: 1520 | chains: 1383 | s: 0 | c: 0 | z: 0 | r: 1520 | tobex c: 276 r: 16.522⟩
	# 
	# ⟨cycle:82@00234§⟨chain:82|1/4⟩⟩
	# ⟨cycle:130@01014§⟨chain:130|1/4⟩⟩
	# ⟨cycle:184@01204§⟨chain:184|1/4⟩⟩
	# ⟨cycle:268@02044§⟨chain:268|1/4⟩⟩
	# ⟨cycle:406@10124§⟨chain:406|1/4⟩⟩
	# 	(⟨loop:[violet:44]:010443|Av⟩, ⟨loop:[red:30]:011042|Av⟩, ⟨loop:[orange:13]:002330|Av⟩, ⟨loop:[yellow:21]:010130|Av⟩, ⟨loop:[indigo:67]:002143|Av⟩)
	# 	(⟨loop:[red:102]:010142|Av⟩, ⟨loop:[orange:113]:101242|Av⟩, ⟨loop:[yellow:56]:020031|Av⟩, ⟨loop:[indigo:35]:003043|Av⟩, ⟨loop:[violet:74]:001443|Av⟩)
	# 	(⟨loop:[orange:37]:001143|Av⟩, ⟨loop:[yellow:71]:100343|Av⟩, ⟨loop:[indigo:104]:020444|Av⟩, ⟨loop:[violet:110]:012044|Av⟩, ⟨loop:[red:58]:002344|Av⟩)
	# 	-- : ⟨avtuples: 101 | chlen: 3 | avlen: 513 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 513 | tobex c: 92 r: 5.576⟩
	# 	-- : ⟨avtuples: 101 | chlen: 3 | avlen: 513 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 513 | tobex c: 92 r: 5.576⟩
	# 	-- : ⟨avtuples: 100 | chlen: 2 | avlen: 508 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 508 | tobex c: 92 r: 5.522⟩
	# 	== : ⟨avtuples: 302 | chlen: 8 | avlen: 1534 | chains: 1383 | s: 0 | c: 0 | z: 0 | r: 1534 | tobex c: 276 r: 16.674⟩
	# 
	# ⟨cycle:155@01105§⟨chain:155|1/6⟩⟩
	# ⟨cycle:161@01115§⟨chain:161|1/6⟩⟩
	# ⟨cycle:167@01125§⟨chain:167|1/6⟩⟩
	# ⟨cycle:173@01135§⟨chain:173|1/6⟩⟩
	# ⟨cycle:179@01145§⟨chain:179|1/6⟩⟩
	# 	(⟨loop:[blue:29]:011406|Av⟩, ⟨loop:[blue:26]:011106|Av⟩, ⟨loop:[blue:28]:011306|Av⟩, ⟨loop:[blue:25]:011006|Av⟩, ⟨loop:[blue:27]:011206|Av⟩)
	# 	(⟨loop:[green:28]:011032|Av⟩, ⟨loop:[green:25]:011005|Av⟩, ⟨loop:[green:27]:011023|Av⟩, ⟨loop:[green:29]:011041|Av⟩, ⟨loop:[green:26]:011014|Av⟩)
	# 	(⟨loop:[yellow:20]:010040|Av⟩, ⟨loop:[indigo:66]:002053|Av⟩, ⟨loop:[violet:43]:010353|Av⟩, ⟨loop:[red:34]:011452|Av⟩, ⟨loop:[orange:12]:002151|Av⟩)
	# 	-- : ⟨avtuples: 100 | chlen: 2 | avlen: 508 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 508 | tobex c: 92 r: 5.522⟩
	# 	-- : ⟨avtuples: 100 | chlen: 2 | avlen: 512 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 512 | tobex c: 92 r: 5.565⟩
	# 	-- : ⟨avtuples: 101 | chlen: 3 | avlen: 513 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 513 | tobex c: 92 r: 5.576⟩
	# 	== : ⟨avtuples: 301 | chlen: 7 | avlen: 1533 | chains: 1383 | s: 0 | c: 0 | z: 0 | r: 1533 | tobex c: 276 r: 16.663⟩
	# 
	# ⟨cycle:222@01320§⟨chain:222|1/5⟩⟩
	# ⟨cycle:348@02330§⟨chain:348|1/5⟩⟩
	# ⟨cycle:426@10210§⟨chain:426|1/5⟩⟩
	# ⟨cycle:624@12040§⟨chain:624|1/5⟩⟩
	# ⟨cycle:660@12200§⟨chain:660|1/3⟩⟩
	# 	(⟨loop:[blue:71]:102106|Av⟩, ⟨loop:[blue:104]:120406|Av⟩, ⟨loop:[blue:110]:122006|Av⟩, ⟨loop:[blue:58]:023306|Av⟩, ⟨loop:[blue:37]:013206|Av⟩)
	# 	(⟨loop:[green:104]:120041|Av⟩, ⟨loop:[green:110]:122005|Av⟩, ⟨loop:[green:58]:023032|Av⟩, ⟨loop:[green:37]:013023|Av⟩, ⟨loop:[green:71]:102014|Av⟩)
	# 	(⟨loop:[yellow:104]:120004|Av⟩, ⟨loop:[indigo:110]:023002|Av⟩, ⟨loop:[violet:58]:013402|Av⟩, ⟨loop:[red:37]:013200|Av⟩, ⟨loop:[orange:71]:102100|Av⟩)
	# 	-- : ⟨avtuples: 100 | chlen: 3 | avlen: 504 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 504 | tobex c: 92 r: 5.478⟩
	# 	-- : ⟨avtuples: 100 | chlen: 3 | avlen: 508 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 508 | tobex c: 92 r: 5.522⟩
	# 	-- : ⟨avtuples: 98 | chlen: 3 | avlen: 486 | chains: 461 | s: 0 | c: 0 | z: 0 | r: 486 | tobex c: 92 r: 5.283⟩
	# 	== : ⟨avtuples: 298 | chlen: 9 | avlen: 1498 | chains: 1383 | s: 0 | c: 0 | z: 0 | r: 1498 | tobex c: 276 r: 16.283⟩
	
	# min nodes: 99
	# ⟨node:3041256@001200§⟨chain:42|1/5⟩|A⟩
	# ⟨node:5630412@001205§⟨chain:42|1/5⟩|A⟩
	# ⟨node:6304125@001206§⟨chain:42|1/5⟩|A⟩	
	# …

	# ⟨001200, 001205, 001206⟩
	for loop in diagram.nodeByAddress['001205'].loop.tuple:
		assert diagram.extendLoop(loop)		
		
	# ===  9 ===================================================================================================================================================================== #

	# [*0*][0m2s.652][lvl:0#-1⁹⁷] [jump] -- init -- | ⟨⟨avtuples: 97 | chlen: 2 | avlen: 486 | chains: 461 | s: 0 | c: 1 | z: 4 | r: 486 | tobex c: 92 r: 5.283⟩⟩
	# viables: 80
	# unchained_cycles: 429
	# min_viable_tuple_count: 2 | min_cycles: 9 | grouped_cycles_per_matched_results: 2
	
	# ⟨cycle:43@00121§⟨chain:43|1/3⟩⟩
	# ⟨cycle:109@00331§⟨chain:109|1/2⟩⟩
	# ⟨cycle:277@02111§⟨chain:277|1/3⟩⟩
	# ⟨cycle:385@10041§⟨chain:385|1/2⟩⟩
	# ⟨cycle:481@11001§⟨chain:481|1/3⟩⟩
	# 	(⟨loop:[green:60]:100005|Av⟩, ⟨loop:[green:81]:110014|Av⟩, ⟨loop:[green:47]:021023|Av⟩, ⟨loop:[green:19]:003041|Av⟩, ⟨loop:[green:8]:001032|Av⟩)
	# 	(⟨loop:[red:104]:010411|Av⟩, ⟨loop:[orange:110]:101011|Av⟩, ⟨loop:[yellow:58]:020211|Av⟩, ⟨loop:[indigo:37]:003312|Av⟩, ⟨loop:[violet:71]:001212|Av⟩)
	# 	-- : ⟨avtuples: 92 | chlen: 3 | avlen: 441 | chains: 436 | s: 0 | c: 0 | z: 0 | r: 441 | tobex c: 87 r: 5.069⟩
	# 	-- : ⟨avtuples: 75 | chlen: 2 | avlen: 390 | chains: 411 | s: 5 | c: 3 | z: 14 | r: 390 | tobex c: 82 r: 4.756⟩
	# 	== : ⟨avtuples: 167 | chlen: 5 | avlen: 831 | chains: 847 | s: 5 | c: 3 | z: 14 | r: 831 | tobex c: 169 r: 9.825⟩
	# 
	# ⟨cycle:48@00130§⟨chain:48|1/3⟩⟩
	# ⟨cycle:114@00340§⟨chain:114|1/4⟩⟩
	# ⟨cycle:282@02120§⟨chain:282|1/4⟩⟩
	# ⟨cycle:486@11010§⟨chain:486|1/4⟩⟩
	# 	(⟨loop:[red:100]:010001|Av⟩, ⟨loop:[orange:111]:101101|Av⟩, ⟨loop:[yellow:59]:020301|Av⟩, ⟨loop:[indigo:38]:003402|Av⟩, ⟨loop:[violet:72]:001302|Av⟩)
	# 	(⟨loop:[green:60]:100005|Av⟩, ⟨loop:[green:81]:110014|Av⟩, ⟨loop:[green:47]:021023|Av⟩, ⟨loop:[green:19]:003041|Av⟩, ⟨loop:[green:8]:001032|Av⟩)
	# 	-- : ⟨avtuples: 82 | chlen: 2 | avlen: 418 | chains: 431 | s: 1 | c: 18 | z: 1 | r: 418 | tobex c: 86 r: 4.860⟩
	# 	-- : ⟨avtuples: 92 | chlen: 3 | avlen: 441 | chains: 436 | s: 0 | c: 0 | z: 0 | r: 441 | tobex c: 87 r: 5.069⟩
	# 	== : ⟨avtuples: 174 | chlen: 5 | avlen: 859 | chains: 867 | s: 1 | c: 18 | z: 1 | r: 859 | tobex c: 173 r: 9.929⟩
	
	# min nodes: 18
	# ⟨node:1253604@001212§⟨chain:43|1/3⟩|A⟩
	# ⟨node:5360412@001214§⟨chain:43|1/3⟩|A⟩
	# …
			
	# ⟨001212, 001214⟩
	for loop in diagram.nodeByAddress['001214'].loop.tuple:
		assert diagram.extendLoop(loop)		
		
	# === 10 ===================================================================================================================================================================== #

	# [*0*][0m5s.538][lvl:0#-1⁷⁵] [jump] -- init -- | ⟨⟨avtuples: 75 | chlen: 2 | avlen: 390 | chains: 411 | s: 5 | c: 3 | z: 14 | r: 390 | tobex c: 82 r: 4.756⟩⟩
	# viables: 24
	# unchained_cycles: 383
	# min_viable_tuple_count: 0 | min_cycles: 27 | grouped_cycles_per_matched_results: 1
	# 
	# ⟨cycle:114@00340§⟨chain:114|1/3⟩⟩
	# ⟨cycle:212@01302§⟨chain:212|1/5⟩⟩
	# ⟨cycle:217@01311§⟨chain:217|1/4⟩⟩
	# ⟨cycle:222@01320§⟨chain:222|1/2⟩⟩
	# ⟨cycle:227@01325§⟨chain:227|1/5⟩⟩
	# ⟨cycle:228@01330§⟨chain:228|1/3⟩⟩
	# ⟨cycle:229@01331§⟨chain:229|1/5⟩⟩
	# ⟨cycle:232@01334§⟨chain:232|1/5⟩⟩
	# ⟨cycle:234@01340§⟨chain:234|1/4⟩⟩
	# ⟨cycle:282@02120§⟨chain:282|1/3⟩⟩
	# ⟨cycle:306@02210§⟨chain:306|1/3⟩⟩
	# ⟨cycle:330@02300§⟨chain:330|1/4⟩⟩
	# ⟨cycle:354@02340§⟨chain:354|1/4⟩⟩
	# ⟨cycle:355@02341§⟨chain:355|1/5⟩⟩
	# ⟨cycle:474@10340§⟨chain:474|1/3⟩⟩
	# ⟨cycle:486@11010§⟨chain:486|1/3⟩⟩
	# ⟨cycle:582@11320§⟨chain:582|1/3⟩⟩
	# ⟨cycle:600@12000§⟨chain:600|1/4⟩⟩
	# ⟨cycle:601@12001§⟨chain:601|1/3⟩⟩
	# ⟨cycle:604@12004§⟨chain:604|1/5⟩⟩
	# ⟨cycle:614@12022§⟨chain:614|1/5⟩⟩
	# ⟨cycle:619@12031§⟨chain:619|1/4⟩⟩
	# ⟨cycle:624@12040§⟨chain:624|1/2⟩⟩
	# ⟨cycle:629@12045§⟨chain:629|1/5⟩⟩
	# ⟨cycle:666@12210§⟨chain:666|1/4⟩⟩
	# ⟨cycle:667@12211§⟨chain:667|1/5⟩⟩
	# ⟨cycle:672@12220§⟨chain:672|1/4⟩⟩
	# 	== : ⟨avtuples: 0 | chlen: 0 | avlen: 0 | chains: 0 | s: 0 | c: 0 | z: 0 | r: 0 | tobex c: 0 r: 0.000⟩
	# 
	# min nodes: 0
				
	# === 11 ===================================================================================================================================================================== #
	
	# [*0*][0m4s.169][lvl:0#-1⁸²] [jump] -- init -- | ⟨⟨avtuples: 82 | chlen: 2 | avlen: 402 | chains: 411 | s: 0 | c: 0 | z: 1 | r: 402 | tobex c: 82 r: 4.902⟩⟩
	# viables: 25
	# unchained_cycles: 385
	# min_viable_tuple_count: 0 | min_cycles: 15 | grouped_cycles_per_matched_results: 1
	# 
	# ⟨cycle:55@00141§⟨chain:55|1/5⟩⟩
	# ⟨cycle:91@00301§⟨chain:91|1/5⟩⟩
	# ⟨cycle:211@01301§⟨chain:211|1/4⟩⟩
	# ⟨cycle:289@02131§⟨chain:289|1/5⟩⟩
	# ⟨cycle:327@02243§⟨chain:327|1/4⟩⟩
	# ⟨cycle:337@02311§⟨chain:337|1/4⟩⟩
	# ⟨cycle:367@10011§⟨chain:367|1/5⟩⟩
	# ⟨cycle:445@10241§⟨chain:445|1/4⟩⟩
	# ⟨cycle:465@10323§⟨chain:465|1/4⟩⟩
	# ⟨cycle:493@11021§⟨chain:493|1/5⟩⟩
	# ⟨cycle:519@11113§⟨chain:519|1/4⟩⟩
	# ⟨cycle:573@11303§⟨chain:573|1/4⟩⟩
	# ⟨cycle:613@12021§⟨chain:613|1/4⟩⟩
	# ⟨cycle:651@12133§⟨chain:651|1/4⟩⟩
	# ⟨cycle:679@12231§⟨chain:679|1/4⟩⟩
	# 	== : ⟨avtuples: 0 | chlen: 0 | avlen: 0 | chains: 0 | s: 0 | c: 0 | z: 0 | r: 0 | tobex c: 0 r: 0.000⟩
	# 
	# min nodes: 0
			
	# === 12 ===================================================================================================================================================================== #

	# [*0*][0m8s.388][lvl:0#-1⁷²] [jump] -- init -- | ⟨⟨avtuples: 72 | chlen: 2 | avlen: 369 | chains: 376 | s: 2 | c: 5 | z: 7 | r: 369 | tobex c: 75 r: 4.920⟩⟩
	# viables: 13
	# unchained_cycles: 336
	# min_viable_tuple_count: 0 | min_cycles: 99 | grouped_cycles_per_matched_results: 1
	# 
	# ⟨cycle:55@00141§⟨chain:55|1/5⟩⟩
	# ⟨cycle:77@00225§⟨chain:77|1/4⟩⟩
	# ⟨cycle:91@00301§⟨chain:91|1/5⟩⟩
	# ⟨cycle:125@01005§⟨chain:125|1/4⟩⟩
	# ⟨cycle:209@01245§⟨chain:209|1/4⟩⟩
	# ⟨cycle:217@01311§⟨chain:217|1/5⟩⟩
	# ⟨cycle:219@01313§⟨chain:219|1/6⟩⟩
	# ⟨cycle:222@01320§⟨chain:222|1/2⟩⟩
	# ⟨cycle:224@01322§⟨chain:224|1/5⟩⟩
	# ⟨cycle:229@01331§⟨chain:229|1/6⟩⟩
	# ⟨cycle:233@01335§⟨chain:233|1/5⟩⟩
	# ⟨cycle:234@01340§⟨chain:234|1/5⟩⟩
	# ⟨cycle:238@01344§⟨chain:238|1/5⟩⟩
	# ⟨cycle:239@01345§⟨chain:239|1/5⟩⟩
	# ⟨cycle:263@02035§⟨chain:263|1/4⟩⟩
	# ⟨cycle:289@02131§⟨chain:289|1/5⟩⟩
	# ⟨cycle:301@02201§⟨chain:301|1/4⟩⟩
	# ⟨cycle:306@02210§⟨chain:306|1/3⟩⟩
	# ⟨cycle:321@02233§⟨chain:321|1/4⟩⟩
	# ⟨cycle:325@02241§⟨chain:325|1/6⟩⟩
	# ⟨cycle:326@02242§⟨chain:326|1/6⟩⟩
	# ⟨cycle:328@02244§⟨chain:328|1/6⟩⟩
	# ⟨cycle:330@02300§⟨chain:330|1/5⟩⟩
	# ⟨cycle:334@02304§⟨chain:334|1/5⟩⟩
	# ⟨cycle:335@02305§⟨chain:335|1/5⟩⟩
	# ⟨cycle:343@02321§⟨chain:343|1/5⟩⟩
	# ⟨cycle:345@02323§⟨chain:345|1/6⟩⟩
	# ⟨cycle:348@02330§⟨chain:348|1/2⟩⟩
	# ⟨cycle:350@02332§⟨chain:350|1/5⟩⟩
	# ⟨cycle:355@02341§⟨chain:355|1/6⟩⟩
	# ⟨cycle:359@02345§⟨chain:359|1/5⟩⟩
	# ⟨cycle:367@10011§⟨chain:367|1/5⟩⟩
	# ⟨cycle:401@10115§⟨chain:401|1/4⟩⟩
	# ⟨cycle:421@10201§⟨chain:421|1/4⟩⟩
	# ⟨cycle:423@10203§⟨chain:423|1/6⟩⟩
	# ⟨cycle:426@10210§⟨chain:426|1/2⟩⟩
	# ⟨cycle:428@10212§⟨chain:428|1/5⟩⟩
	# ⟨cycle:433@10221§⟨chain:433|1/4⟩⟩
	# ⟨cycle:437@10225§⟨chain:437|1/4⟩⟩
	# ⟨cycle:438@10230§⟨chain:438|1/3⟩⟩
	# ⟨cycle:442@10234§⟨chain:442|1/5⟩⟩
	# ⟨cycle:443@10235§⟨chain:443|1/5⟩⟩
	# ⟨cycle:459@10313§⟨chain:459|1/4⟩⟩
	# ⟨cycle:463@10321§⟨chain:463|1/6⟩⟩
	# ⟨cycle:464@10322§⟨chain:464|1/5⟩⟩
	# ⟨cycle:466@10324§⟨chain:466|1/5⟩⟩
	# ⟨cycle:469@10331§⟨chain:469|1/4⟩⟩
	# ⟨cycle:474@10340§⟨chain:474|1/4⟩⟩
	# ⟨cycle:493@11021§⟨chain:493|1/5⟩⟩
	# ⟨cycle:513@11103§⟨chain:513|1/4⟩⟩
	# ⟨cycle:517@11111§⟨chain:517|1/6⟩⟩
	# ⟨cycle:518@11112§⟨chain:518|1/6⟩⟩
	# ⟨cycle:520@11114§⟨chain:520|1/6⟩⟩
	# ⟨cycle:523@11121§⟨chain:523|1/4⟩⟩
	# ⟨cycle:528@11130§⟨chain:528|1/3⟩⟩
	# ⟨cycle:541@11201§⟨chain:541|1/4⟩⟩
	# ⟨cycle:542@11202§⟨chain:542|1/5⟩⟩
	# ⟨cycle:543@11203§⟨chain:543|1/5⟩⟩
	# ⟨cycle:544@11204§⟨chain:544|1/4⟩⟩
	# ⟨cycle:547@11211§⟨chain:547|1/4⟩⟩
	# ⟨cycle:548@11212§⟨chain:548|1/5⟩⟩
	# ⟨cycle:549@11213§⟨chain:549|1/5⟩⟩
	# ⟨cycle:550@11214§⟨chain:550|1/4⟩⟩
	# ⟨cycle:553@11221§⟨chain:553|1/4⟩⟩
	# ⟨cycle:554@11222§⟨chain:554|1/5⟩⟩
	# ⟨cycle:555@11223§⟨chain:555|1/5⟩⟩
	# ⟨cycle:556@11224§⟨chain:556|1/4⟩⟩
	# ⟨cycle:559@11231§⟨chain:559|1/4⟩⟩
	# ⟨cycle:560@11232§⟨chain:560|1/4⟩⟩
	# ⟨cycle:561@11233§⟨chain:561|1/5⟩⟩
	# ⟨cycle:562@11234§⟨chain:562|1/4⟩⟩
	# ⟨cycle:565@11241§⟨chain:565|1/4⟩⟩
	# ⟨cycle:566@11242§⟨chain:566|1/5⟩⟩
	# ⟨cycle:567@11243§⟨chain:567|1/5⟩⟩
	# ⟨cycle:568@11244§⟨chain:568|1/4⟩⟩
	# ⟨cycle:571@11301§⟨chain:571|1/5⟩⟩
	# ⟨cycle:572@11302§⟨chain:572|1/5⟩⟩
	# ⟨cycle:574@11304§⟨chain:574|1/5⟩⟩
	# ⟨cycle:577@11311§⟨chain:577|1/3⟩⟩
	# ⟨cycle:582@11320§⟨chain:582|1/2⟩⟩
	# ⟨cycle:597@11343§⟨chain:597|1/4⟩⟩
	# ⟨cycle:601@12001§⟨chain:601|1/4⟩⟩
	# ⟨cycle:605@12005§⟨chain:605|1/4⟩⟩
	# ⟨cycle:606@12010§⟨chain:606|1/2⟩⟩
	# ⟨cycle:610@12014§⟨chain:610|1/5⟩⟩
	# ⟨cycle:611@12015§⟨chain:611|1/5⟩⟩
	# ⟨cycle:619@12031§⟨chain:619|1/5⟩⟩
	# ⟨cycle:621@12033§⟨chain:621|1/6⟩⟩
	# ⟨cycle:624@12040§⟨chain:624|1/2⟩⟩
	# ⟨cycle:626@12042§⟨chain:626|1/5⟩⟩
	# ⟨cycle:649@12131§⟨chain:649|1/6⟩⟩
	# ⟨cycle:652@12134§⟨chain:652|1/6⟩⟩
	# ⟨cycle:667@12211§⟨chain:667|1/5⟩⟩
	# ⟨cycle:671@12215§⟨chain:671|1/5⟩⟩
	# ⟨cycle:672@12220§⟨chain:672|1/3⟩⟩
	# ⟨cycle:676@12224§⟨chain:676|1/5⟩⟩
	# ⟨cycle:677@12225§⟨chain:677|1/4⟩⟩
	# ⟨cycle:685@12241§⟨chain:685|1/5⟩⟩
	# ⟨cycle:687@12243§⟨chain:687|1/6⟩⟩
	# 	== : ⟨avtuples: 0 | chlen: 0 | avlen: 0 | chains: 0 | s: 0 | c: 0 | z: 0 | r: 0 | tobex c: 0 r: 0.000⟩
	# 
	# min nodes: 0		

	# === 13 ===================================================================================================================================================================== #
	
	# [*0*][0m3s.322][lvl:0#-1⁷¹] [jump] -- init -- | ⟨⟨avtuples: 71 | chlen: 2 | avlen: 343 | chains: 361 | s: 0 | c: 6 | z: 1 | r: 343 | tobex c: 72 r: 4.764⟩⟩
	# viables: 17
	# unchained_cycles: 330
	# min_viable_tuple_count: 0 | min_cycles: 15 | grouped_cycles_per_matched_results: 1
	# 
	# ⟨cycle:310@02214§⟨chain:310|1/6⟩⟩
	# ⟨cycle:320@02232§⟨chain:320|1/6⟩⟩
	# ⟨cycle:325@02241§⟨chain:325|1/6⟩⟩
	# ⟨cycle:458@10312§⟨chain:458|1/6⟩⟩
	# ⟨cycle:463@10321§⟨chain:463|1/7⟩⟩
	# ⟨cycle:478@10344§⟨chain:478|1/6⟩⟩
	# ⟨cycle:512@11102§⟨chain:512|1/5⟩⟩
	# ⟨cycle:517@11111§⟨chain:517|1/6⟩⟩
	# ⟨cycle:532@11134§⟨chain:532|1/6⟩⟩
	# ⟨cycle:571@11301§⟨chain:571|1/6⟩⟩
	# ⟨cycle:586@11324§⟨chain:586|1/6⟩⟩
	# ⟨cycle:596@11342§⟨chain:596|1/6⟩⟩
	# ⟨cycle:634@12104§⟨chain:634|1/6⟩⟩
	# ⟨cycle:644@12122§⟨chain:644|1/6⟩⟩
	# ⟨cycle:649@12131§⟨chain:649|1/6⟩⟩
	# 	== : ⟨avtuples: 0 | chlen: 0 | avlen: 0 | chains: 0 | s: 0 | c: 0 | z: 0 | r: 0 | tobex c: 0 r: 0.000⟩
	# 
	# min nodes: 0
		
	# === 14 ===================================================================================================================================================================== #
	
	# [*0*][0m1s.718][lvl:0#-1⁷¹] [jump] -- init -- | ⟨⟨avtuples: 71 | chlen: 2 | avlen: 334 | chains: 336 | s: 0 | c: 0 | z: 0 | r: 334 | tobex c: 67 r: 4.985⟩⟩
	# viables: 31
	# unchained_cycles: 295
	# min_viable_tuple_count: 1 | min_cycles: 20 | grouped_cycles_per_matched_results: 3
	
	# ⟨cycle:77@00225§⟨chain:77|1/3⟩⟩
	# ⟨cycle:125@01005§⟨chain:125|1/3⟩⟩
	# ⟨cycle:209@01245§⟨chain:209|1/3⟩⟩
	# ⟨cycle:221@01315§⟨chain:221|1/4⟩⟩
	# ⟨cycle:263@02035§⟨chain:263|1/3⟩⟩
	# ⟨cycle:347@02325§⟨chain:347|1/4⟩⟩
	# ⟨cycle:401@10115§⟨chain:401|1/3⟩⟩
	# ⟨cycle:425@10205§⟨chain:425|1/4⟩⟩
	# ⟨cycle:623@12035§⟨chain:623|1/4⟩⟩
	# ⟨cycle:689@12245§⟨chain:689|1/4⟩⟩
	# 	(⟨loop:[yellow:20]:010040|Av⟩, ⟨loop:[indigo:66]:002053|Av⟩, ⟨loop:[violet:43]:010353|Av⟩, ⟨loop:[red:34]:011452|Av⟩, ⟨loop:[orange:12]:002151|Av⟩)
	# 	-- : ⟨avtuples: 67 | chlen: 2 | avlen: 309 | chains: 311 | s: 0 | c: 0 | z: 0 | r: 309 | tobex c: 62 r: 4.984⟩
	# 	== : ⟨avtuples: 67 | chlen: 2 | avlen: 309 | chains: 311 | s: 0 | c: 0 | z: 0 | r: 309 | tobex c: 62 r: 4.984⟩
	# 
	# ⟨cycle:217@01311§⟨chain:217|1/4⟩⟩
	# ⟨cycle:343@02321§⟨chain:343|1/5⟩⟩
	# ⟨cycle:421@10201§⟨chain:421|1/4⟩⟩
	# ⟨cycle:619@12031§⟨chain:619|1/5⟩⟩
	# ⟨cycle:685@12241§⟨chain:685|1/5⟩⟩
	# 	(⟨loop:[green:104]:120041|Av⟩, ⟨loop:[green:110]:122005|Av⟩, ⟨loop:[green:58]:023032|Av⟩, ⟨loop:[green:37]:013023|Av⟩, ⟨loop:[green:71]:102014|Av⟩)
	# 	-- : ⟨avtuples: 65 | chlen: 2 | avlen: 303 | chains: 311 | s: 0 | c: 0 | z: 1 | r: 303 | tobex c: 62 r: 4.887⟩
	# 	== : ⟨avtuples: 65 | chlen: 2 | avlen: 303 | chains: 311 | s: 0 | c: 0 | z: 1 | r: 303 | tobex c: 62 r: 4.887⟩
	# 
	# ⟨cycle:229@01331§⟨chain:229|1/6⟩⟩
	# ⟨cycle:355@02341§⟨chain:355|1/6⟩⟩
	# ⟨cycle:433@10221§⟨chain:433|1/3⟩⟩
	# ⟨cycle:601@12001§⟨chain:601|1/4⟩⟩
	# ⟨cycle:667@12211§⟨chain:667|1/5⟩⟩
	# 	(⟨loop:[green:55]:023005|Av⟩, ⟨loop:[green:39]:013041|Av⟩, ⟨loop:[green:73]:102032|Av⟩, ⟨loop:[green:101]:120014|Av⟩, ⟨loop:[green:112]:122023|Av⟩)
	# 	-- : ⟨avtuples: 67 | chlen: 2 | avlen: 307 | chains: 311 | s: 0 | c: 0 | z: 0 | r: 307 | tobex c: 62 r: 4.952⟩
	# 	== : ⟨avtuples: 67 | chlen: 2 | avlen: 307 | chains: 311 | s: 0 | c: 0 | z: 0 | r: 307 | tobex c: 62 r: 4.952⟩
	
	# min nodes: 20
	# ⟨node:3650142@002255§⟨chain:77|1/3⟩|A⟩
	# …	
	
	# ⟨002255⟩
	# for loop in diagram.nodeByAddress['002255'].loop.tuple:
	# 	assert diagram.extendLoop(loop)
			
	# === 15 ===================================================================================================================================================================== #
	
	# [*0*][0m1s.801][lvl:0#-1⁶⁷] [jump] -- init -- | ⟨⟨avtuples: 67 | chlen: 2 | avlen: 309 | chains: 311 | s: 0 | c: 0 | z: 0 | r: 309 | tobex c: 62 r: 4.984⟩⟩
	# viables: 25
	# unchained_cycles: 265
	# min_viable_tuple_count: 1 | min_cycles: 30 | grouped_cycles_per_matched_results: 4
	
	# ⟨cycle:70@00214§⟨chain:70|1/5⟩⟩
	# ⟨cycle:148@01044§⟨chain:148|1/5⟩⟩
	# ⟨cycle:202@01234§⟨chain:202|1/5⟩⟩
	# ⟨cycle:256@02024§⟨chain:256|1/5⟩⟩
	# ⟨cycle:394@10104§⟨chain:394|1/5⟩⟩
	# 	(⟨loop:[violet:44]:010443|Av⟩, ⟨loop:[red:30]:011042|Av⟩, ⟨loop:[orange:13]:002330|Av⟩, ⟨loop:[yellow:21]:010130|Av⟩, ⟨loop:[indigo:67]:002143|Av⟩)
	# 	-- : ⟨avtuples: 63 | chlen: 2 | avlen: 284 | chains: 286 | s: 0 | c: 0 | z: 0 | r: 284 | tobex c: 57 r: 4.982⟩
	# 	== : ⟨avtuples: 63 | chlen: 2 | avlen: 284 | chains: 286 | s: 0 | c: 0 | z: 0 | r: 284 | tobex c: 57 r: 4.982⟩
	# 
	# ⟨cycle:217@01311§⟨chain:217|1/4⟩⟩
	# ⟨cycle:222@01320§⟨chain:222|1/3⟩⟩
	# ⟨cycle:232@01334§⟨chain:232|1/5⟩⟩
	# ⟨cycle:343@02321§⟨chain:343|1/5⟩⟩
	# ⟨cycle:348@02330§⟨chain:348|1/3⟩⟩
	# ⟨cycle:358@02344§⟨chain:358|1/5⟩⟩
	# ⟨cycle:421@10201§⟨chain:421|1/4⟩⟩
	# ⟨cycle:426@10210§⟨chain:426|1/3⟩⟩
	# ⟨cycle:436@10224§⟨chain:436|1/5⟩⟩
	# ⟨cycle:604@12004§⟨chain:604|1/4⟩⟩
	# ⟨cycle:619@12031§⟨chain:619|1/5⟩⟩
	# ⟨cycle:624@12040§⟨chain:624|1/3⟩⟩
	# ⟨cycle:660@12200§⟨chain:660|1/2⟩⟩
	# ⟨cycle:670@12214§⟨chain:670|1/5⟩⟩
	# ⟨cycle:685@12241§⟨chain:685|1/5⟩⟩
	# 	(⟨loop:[green:104]:120041|Av⟩, ⟨loop:[green:110]:122005|Av⟩, ⟨loop:[green:58]:023032|Av⟩, ⟨loop:[green:37]:013023|Av⟩, ⟨loop:[green:71]:102014|Av⟩)
	# 	-- : ⟨avtuples: 61 | chlen: 2 | avlen: 278 | chains: 286 | s: 0 | c: 0 | z: 1 | r: 278 | tobex c: 57 r: 4.877⟩
	# 	== : ⟨avtuples: 61 | chlen: 2 | avlen: 278 | chains: 286 | s: 0 | c: 0 | z: 1 | r: 278 | tobex c: 57 r: 4.877⟩
	# 
	# ⟨cycle:229@01331§⟨chain:229|1/6⟩⟩
	# ⟨cycle:355@02341§⟨chain:355|1/6⟩⟩
	# ⟨cycle:433@10221§⟨chain:433|1/3⟩⟩
	# ⟨cycle:601@12001§⟨chain:601|1/4⟩⟩
	# ⟨cycle:667@12211§⟨chain:667|1/5⟩⟩
	# 	(⟨loop:[green:55]:023005|Av⟩, ⟨loop:[green:39]:013041|Av⟩, ⟨loop:[green:73]:102032|Av⟩, ⟨loop:[green:101]:120014|Av⟩, ⟨loop:[green:112]:122023|Av⟩)
	# 	-- : ⟨avtuples: 63 | chlen: 2 | avlen: 282 | chains: 286 | s: 0 | c: 0 | z: 0 | r: 282 | tobex c: 57 r: 4.947⟩
	# 	== : ⟨avtuples: 63 | chlen: 2 | avlen: 282 | chains: 286 | s: 0 | c: 0 | z: 0 | r: 282 | tobex c: 57 r: 4.947⟩
	# 
	# ⟨cycle:231@01333§⟨chain:231|1/5⟩⟩
	# ⟨cycle:357@02343§⟨chain:357|1/5⟩⟩
	# ⟨cycle:435@10223§⟨chain:435|1/5⟩⟩
	# ⟨cycle:603@12003§⟨chain:603|1/4⟩⟩
	# ⟨cycle:669@12213§⟨chain:669|1/5⟩⟩
	# 	(⟨loop:[red:31]:011221|Av⟩, ⟨loop:[orange:14]:002420|Av⟩, ⟨loop:[yellow:22]:010220|Av⟩, ⟨loop:[indigo:68]:002233|Av⟩, ⟨loop:[violet:40]:010033|Av⟩)
	# 	-- : ⟨avtuples: 61 | chlen: 2 | avlen: 281 | chains: 286 | s: 0 | c: 0 | z: 3 | r: 281 | tobex c: 57 r: 4.930⟩
	# 	== : ⟨avtuples: 61 | chlen: 2 | avlen: 281 | chains: 286 | s: 0 | c: 0 | z: 3 | r: 281 | tobex c: 57 r: 4.930⟩
	
	# min nodes: 30
	# ⟨node:0146253@002143§⟨chain:70|1/5⟩|A⟩
	# …	
	
	# ⟨002143⟩
	# for loop in diagram.nodeByAddress['002143'].loop.tuple:
	# 	assert diagram.extendLoop(loop)	

	# === 16 ===================================================================================================================================================================== #
	
	# [*0*][0m1s.942][lvl:0#-1⁶³] [jump] -- init -- | ⟨⟨avtuples: 63 | chlen: 2 | avlen: 284 | chains: 286 | s: 0 | c: 0 | z: 0 | r: 284 | tobex c: 57 r: 4.982⟩⟩
	# viables: 14
	# unchained_cycles: 235
	# min_viable_tuple_count: 0 | min_cycles: 5 | grouped_cycles_per_matched_results: 1
	
	# ⟨cycle:320@02232§⟨chain:320|1/6⟩⟩
	# ⟨cycle:458@10312§⟨chain:458|1/6⟩⟩
	# ⟨cycle:512@11102§⟨chain:512|1/5⟩⟩
	# ⟨cycle:596@11342§⟨chain:596|1/6⟩⟩
	# ⟨cycle:644@12122§⟨chain:644|1/6⟩⟩
	# 	== : ⟨avtuples: 0 | chlen: 0 | avlen: 0 | chains: 0 | s: 0 | c: 0 | z: 0 | r: 0 | tobex c: 0 r: 0.000⟩
	
	# min nodes: 0
	
	# ============================================================================================================================================================================ #
	# ============================================================================================================================================================================ #
	# ============================================================================================================================================================================ #
						
	startTime = time()
	move_index = -1
	sol_count = 0
	
	diagram.point(); show(diagram); print('^^start^^\n')
	print("----------")
	lvl = 0
	ass_before = detail()
	jump2()
	ass_after = detail()
	assert ass_before == ass_after, "broken first step"
	#diagram.point(); show(diagram); print('-- final --\n')
	print("[*{}*][{}] sols found: {}".format(move_index, tstr(time() - startTime), sol_count))
	print("------------")
