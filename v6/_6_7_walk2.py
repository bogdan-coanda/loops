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
				log.write((log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "|".join([str(x)+"."+str(t)+("b" if b else "") for x,t,b in step_path]), "-- --", str(base_mx)) + "\n|" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n|" + "\n| ".join([str(l) for l in exloops]) + "\n\n").replace("⟩", ")").replace("⟨", "("))

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
		
		
	head_filename = '__walk2_7.1__'
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
				
		move_index += 1
		if move_index % 1 == 0:
			with open(running_filename + ".txt", 'a') as log:
				log.write((log_template.format(move_index, tstr(time() - startTime), lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "-- --", str(base_mx)) + "\n|" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n\n").replace("⟩", ")").replace("⟨", "("))

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
	
		if len(min_cycles) is 0 and len(unchained_cycles) is 0: # no more tuples, go on stepping
			
			step(lvl, jump_path, extuples, 0, [[-1,0,False]], [])
			
		else:
			chosen_cycle = min_cycles[0]
			chosen_tuples = list(min_cycle_tuples[0])
	
			print("chosen cycle: " + str(chosen_cycle) + "\ntuples: (" + str(len(chosen_tuples)) + ")\n" + "\n".join(["  " + str(t) for t in chosen_tuples]) + "\n")
	
			jump_path[-1][1] = len(chosen_tuples)
																					
			for curr_index, curr_tuple in enumerate(chosen_tuples):
				jump_path[-1][0] = curr_index
							
				# extend viable tuple
				for loop in curr_tuple:
					assert diagram.extendLoop(loop)
				
				jump2(lvl+1, jump_path+[[-1,0]], extuples+[curr_tuple], seen_tuples+chosen_tuples[0:curr_index])
					
				# collapse viable tuple				
				for loop in reversed(curr_tuple):
					diagram.collapseBack(loop)							
			
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
	# for loop in diagram.nodeByAddress['001401'].loop.tuple:
	# 	assert diagram.extendLoop(loop)	
	
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
