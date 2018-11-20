from diagram import *
from uicanvas import *
from common import *
from itertools import chain
from time import time
from collections import defaultdict





if __name__ == "__main__":

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
				
	# ============================================================================================================================================================================ #

	def measure_viables(diagram, avtuples):
		viable_results = []	
	
		for tindex, curr_tuple in enumerate(avtuples):
			if tindex % 20 == 0:
				print("[viables] index: " + str(tindex) + " / " + str(len(avtuples)))
		
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
				curr_mx.avtuples = curr_mx.avtuples
				
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
				Measurement.clean(diagram, curr_mx.singles, curr_mx.coerced, curr_mx.zeroes)
			else:
				# diagram.point(); show(diagram)			
				# print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- [tuple:"+str(tindex)+"] failed by "+str(len(curr_extended_loops))+"/"+str(len(curr_tuple))+" --", Measurement.zero(diagram)))
				pass
				
			# collapse current tuple				
			for loop in reversed(curr_extended_loops):
				diagram.collapseBack(loop)		

		return viable_results
		
	# ============================================================================================================================================================================ #	
	
	def find_min_blabla(diagram, viable_results):
		min_viable_tuple_count = diagram.spClass
		min_matched_results_set = set()
		
		unchained_cycles = [cycle for cycle in diagram.cycles if len(cycle.chain.cycles) is 1]
		print("[find_min_blabla] unchained_cycles: " + str(len(unchained_cycles)))
		for cycle in unchained_cycles:
			curr_cycle_tuples = [node.loop.tuple for node in cycle.nodes if node.loop.availabled or node.loop.extended]
			matched_results = tuple(sorted([result for result in viable_results if result.obj in curr_cycle_tuples], key = lambda result: (result.mx.min_chlen, result.mx.avlen)))
			
			if len(matched_results) < min_viable_tuple_count:
				min_viable_tuple_count = len(matched_results)
				min_matched_results_set = set([matched_results])
			elif len(matched_results) == min_viable_tuple_count:
				min_matched_results_set.add(matched_results)					
								
		summed_matched_results_results = []
		for matched_results in min_matched_results_set:
			summed_mx = Measurement.zero(diagram)			
			for result in matched_results:
				print("\t-- : " + str(result.mx))
				summed_mx += result.mx
			print("\t== : " + str(summed_mx) + "\n")
			summed_matched_results_results.append(Result(matched_results, summed_mx))
			
		sorted_blabla = sorted(summed_matched_results_results, 
			key = lambda result: (result.mx.min_chlen, result.mx.avlen, result.obj[0].mx.min_chlen, result.obj[0].mx.avlen))
			
		summed_result = sorted_blabla[0] if len(sorted_blabla) else Result([], Measurement.zero(diagram))
		print("[find_min_blabla] chosen: \n\t==" + str(summed_result.mx) + "".join(["\n\t|~ " + str(r.obj) + "\n\t-- " + str(r.mx) for r in summed_result.obj]))
								
		return summed_result
	
	# ============================================================================================================================================================================ #
	
	head_filename = '__unifive_7.1__'
	running_filename = head_filename + "running"
	sols_filename = head_filename + "sols"
	
	def jump3(diagram, lvl=0, jump_path=[[-1,0]], extuples=[], prev_viables=None):
		global move_index
		log_template = "[*{}*][{}][lvl:{}#{}] [jump] {} | viables: {} | ⟨{}⟩"
	
		# initial measurement	
		base_mx = Measurement.measure(diagram)		
		if prev_viables is None:
			prev_viables = base_mx.avtuples
				
		move_index += 1
		if move_index % 1 == 0:
			with open(running_filename + ".txt", 'a') as log:
				log.write((log_template.format(move_index, tstr(time() - startTime), lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "-- --", str(len(prev_viables)), str(base_mx)) + "\n|" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n\n").replace("⟩", ")").replace("⟨", "("))

		# diagram.point(); show(diagram)
		print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- init --", str(len(prev_viables)), str(base_mx)))
		
		# assert len(base_mx.singles) is 0
				
		#diagram.pointers = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*base_mx.avtuples)]))
		#show(diagram); print("avtuples\n")
		
		viable_results = measure_viables(diagram, prev_viables)
		print("new viables: " + str(len(viable_results))) # + "\n".join([str(r.obj) + " | " + str(r.mx) for r in viable_results]) + "\n")
		
		#diagram.pointers = list(itertools.chain(*[loop.nodes for loop in itertools.chain(*[r.obj for r in viable_results])]))
		#show(diagram); print("viables\n")
				
		summed_result = find_min_blabla(diagram, viable_results)
	
		if len([c for c in diagram.cycles if len(c.chain.cycles) is 1]) is 0: # no more tuples, go on stepping
			
			step(lvl, jump_path, extuples, 0, [[-1,0,False]], [])
			
		else:
			chosen_tuples = [r.obj for r in summed_result.obj]
	
			print("chosen tuples: (" + str(len(chosen_tuples)) + ") | mx: " + str(summed_result.mx))
	
			jump_path[-1][1] = len(chosen_tuples)
																					
			for curr_index, curr_tuple in enumerate(chosen_tuples):
				jump_path[-1][0] = curr_index
							
				# extend viable tuple
				for loop in curr_tuple:
					assert diagram.extendLoop(loop)
				
				# show(diagram); input("extended: " + str(curr_tuple))
				
				jump3(diagram, lvl+1, jump_path+[[-1,0]], extuples+[curr_tuple], [r.obj for r in viable_results])
					
				# collapse viable tuple				
				for loop in reversed(curr_tuple):
					diagram.collapseBack(loop)							
			
		clean(base_mx.singles, base_mx.coerced, base_mx.zeroes)
		
	# ============================================================================================================================================================================ #	
	# ============================================================================================================================================================================ #
	# ============================================================================================================================================================================ #
		
	diagram = Diagram(7, 1)
	
	sol_addrs = "001224 001114 001014 001214 001005 001403 002020 002110 002200 002420 002444 002045 002140 002453 013115 013133 013322 013412 013445 022005 022014 022032 013053 112006 | 020200 012300 023100 103006 020000 003006 113030 122440 022340 021330 013410 001420 120230 100106 110210 020340 010040 111130"
	taddrs, laddrs = sol_addrs.split(" | ")
	sol_tuples = [diagram.nodeByAddress[addr].loop.tuple for addr in taddrs.split(" ")]
	sol_loops = [diagram.nodeByAddress[addr].loop for addr in laddrs.split(" ")]
	print("sol | tuples: " + str(len(sol_tuples)) + " | loops: " + str(len(sol_loops)))	
	
	touched_cycles = list(itertools.chain(*[itertools.chain(*[[node.cycle for node in loop.nodes] for loop in sol_tuple]) for sol_tuple in sol_tuples])) 
	unchained_cycles = [c for c in diagram.cycles if len(c.chain.cycles) is 1]
	print("touched cycles: "+str(len(touched_cycles))+" | unchained cycles: "+str(len(unchained_cycles)))
	
	for cycle in unchained_cycles:
		touched_cycles.remove(cycle)
		
	print("remaining cycles: "+str(len(touched_cycles)))
	
	for index, sol_tuple in enumerate(sol_tuples):
		tuple_cycles = itertools.chain(*[[node.cycle for node in loop.nodes] for loop in sol_tuple])
		intersected_cycles = set(tuple_cycles).intersection(touched_cycles)
		print("@"+str(index)+" | intersected cycles: "+str(len(intersected_cycles)))
	
	input("---")
	'''
	for tuple in sol_tuples:
		for loop in tuple:
			diagram.extendLoop(loop)

	unchained_cycles = [c for c in diagram.cycles if len(c.chain.cycles) is 1]
									
	for loop in sol_loops:
		diagram.extendLoop(loop)
		
	show(diagram); input("unchained cycles by tuples: " + str(len(unchained_cycles)))
	'''
			
	diagram.extendLoop(diagram.nodeByAddress['000002'].loop)
	
	for index, addr in enumerate([
		# '110005', '001014', '100005', '003014', # green blocks		
		# '103014', '103032', '103041', # green blocks
		'112106',	# blue middle block:1.1.2
		'002453', '010042', '002020', '011221',	'011024', '010202', # middle block:0.1.1
		'013151', '120130', '013020', '023020', '013010', '013100', # middle block:1.2.3
		'100103', '002051' # '001224', '101430' # diag		
	]):
		t = diagram.nodeByAddress[addr].loop.tuple
		for loop in t:
			diagram.extendLoop(loop)
		
	
	# for index, addr in enumerate([
	# ]):
	# 	tuple = diagram.nodeByAddress[addr].loop.tuple
	# 	for loop in tuple:
	# 		diagram.extendLoop(loop)
	# 
	# 	show(diagram); input("@" + str(index) + " | " + str(tuple))
		
	show(diagram);
	
	'''
	'''
		
	# startTime = time()
	# move_index = -1
	# sol_count = 0	
	
	# jump3(diagram)
	
	# ___
	
	# ⟨001406, 001401⟩
	# for loop in d.nodeByAddress['001406'].loop.tuple:
	# 	assert d.extendLoop(loop)	
	# 
	# ⟨002100, 002105, 002106⟩
	# for loop in d.nodeByAddress['002100'].loop.tuple:
	# 	assert d.extendLoop(loop)	
	# 
	# ⟨001304, 001302, 001303⟩
	# for loop in d.nodeByAddress['001304'].loop.tuple:
	# 	assert d.extendLoop(loop)	
	# 
	# ⟨001312, 001313, 001311⟩ # 1/3
	# for loop in d.nodeByAddress['001313'].loop.tuple:
	# 	assert d.extendLoop(loop)	
	# 
	# ⟨001005, 001006⟩
	# for loop in d.nodeByAddress['001005'].loop.tuple:
	# 	assert d.extendLoop(loop)	
	# 
	# ⟨022405, 022406, 022401⟩
	# for loop in d.nodeByAddress['022405'].loop.tuple:
	# 	assert d.extendLoop(loop)										
	# 
	# ⟨002151⟩
	# for loop in d.nodeByAddress['002151'].loop.tuple:
	# 	assert d.extendLoop(loop)										
	# 
	# ⟨001136, 001131⟩⟩
	# for loop in d.nodeByAddress['001136'].loop.tuple:
	# 	assert d.extendLoop(loop)
	# 
	# ⟨001011, 001010⟩
	# for loop in d.nodeByAddress['001011'].loop.tuple:
	# 	assert d.extendLoop(loop)
		
	# ⟨001025, 001026⟩ # 1/2
	# for loop in d.nodeByAddress['001026'].loop.tuple:
	# 	assert d.extendLoop(loop)
		
	# ⟨022323, 022321⟩ 1/2
	# for loop in d.nodeByAddress['022321'].loop.tuple:
	# 	assert d.extendLoop(loop)
		
	# ⟨022016, 022010⟩ 1/2
	# for loop in d.nodeByAddress['022010'].loop.tuple:
	# 	assert d.extendLoop(loop)
		
	# ⟨001131⟩ # F
	# for loop in d.nodeByAddress['001131'].loop.tuple:
	# 	assert d.extendLoop(loop)
		
						
	mx = Measurement.measure(diagram)		
	vr = measure_viables(diagram, mx.avtuples)
				
	summed_result = find_min_blabla(diagram, vr)
	
	#show(d)
	print("[-] viables: " + str(len(vr)) + " | mx: " + str(mx))
	for i,r in enumerate(summed_result.obj):
		print("["+str(i)+"]"+str(r.obj in sol_tuples))
	unchained_cycles = [c for c in diagram.cycles if len(c.chain.cycles) is 1]
	print("unchained_cycles: "+str(len(unchained_cycles)))
