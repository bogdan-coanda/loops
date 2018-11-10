from diagram import *
from uicanvas import *
from common import *
from itertools import chain
from time import time
from collections import defaultdict

if __name__ == "__main__":
		
	diagram = Diagram(6, 1)
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
			min_chlen = len(diagram.loops)
			
			for chain in diagram.chains:
				avlen = len(chain.avloops)
				if avlen < min_chlen:
					min_chlen = avlen
				
				if avlen == 0:
					return (0, singles, coerced) 

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
				return (min_chlen, singles, coerced)
		
	def decimate():
		zeroes = []
		
		while True:
			found = False
			results = {}
			avloops = [l for l in diagram.loops if l.availabled]
			#print("..[decimate] curr | avloops: " + str(len(avloops)))
			for index, loop in enumerate(avloops):
				# if index == 348 and loop.firstAddress() == '113106':
				# 	assert False
				diagram.extendLoop(loop)
				min_chlen, singles, coerced = coerce()
				avlen = len([l for l in diagram.loops if l.availabled])
				tobex_count = diagram.measureTobex()
				tobex_ratio = (avlen / tobex_count) if tobex_count != 0 else 0

				results[loop] = (
					avlen, 
					min_chlen,
					len(diagram.startNode.cycle.chain.avloops),
					-(len(singles)), 
					-(len(coerced)),
					tobex_count,
					tobex_ratio
				)
										
				for l in reversed(singles):
					diagram.collapseBack(l)						
				for l in coerced:
					diagram.setLoopAvailabled(l)			
				diagram.collapseBack(loop)				
								
				if min_chlen == 0:
					zeroes.append(loop)
					diagram.setLoopUnavailabled(loop)
					found = True
			
			if not found:
				#print("..[decimate] done | zeroes: " + str(len(zeroes)))
				return (zeroes, results)
			#print("..[decimate] curr | zeroes: " + str(len(zeroes)))
			
	def reduce():
		# mandatory
		curr_min_chlen, curr_singles, curr_coerced = coerce()
		#print("[reduce] init | ch: " + str(curr_min_chlen) + " | s: " + str(len(curr_singles)) + " | c: " + str(len(curr_coerced)))
		curr_zeroes, curr_results = decimate()
		#print("[reduce] init | z: " + str(len(curr_zeroes)))
		
		min_chlen = curr_min_chlen
		singles = list(curr_singles)
		coerced = list(curr_coerced)
		zeroes = list(curr_zeroes)
		results = curr_results		
		
		# additional
		while True:
			if len(curr_zeroes) > 0:
				curr_min_chlen, curr_singles, curr_coerced = coerce()
				min_chlen = curr_min_chlen
				singles += curr_singles
				coerced += curr_coerced			
				#print("[reduce] curr | ch: " + str(curr_min_chlen) + " | s: " + str(len(curr_singles)) + " | c: " + str(len(curr_coerced)))
				
				if len(curr_singles) or len(curr_coerced):
					curr_zeroes, curr_results = decimate()
					zeroes += curr_zeroes
					results = curr_results
					#print("[reduce] curr | z: " + str(len(curr_zeroes)))
				else:
					break
			else:
				break
		#print("[reduce] done | ch: " + str(min_chlen) + " | s: " + str(len(singles)) + " | c: " + str(len(coerced)) + " | z: " + str(len(zeroes)))
		return (min_chlen, singles, coerced, zeroes, results)
	
	
	def clean(singles, coerced, zeroes):
		for l in reversed(singles):
			diagram.collapseBack(l)						
		for l in coerced:
			diagram.setLoopAvailabled(l)
		for l in zeroes:
			diagram.setLoopAvailabled(l)		
	
	
	def detail():
		avlen = len([l for l in diagram.loops if l.availabled])
		tobex_count = diagram.measureTobex()
		tobex_ratio = (avlen / tobex_count) if tobex_count is not 0 else 0		
		return (avlen, tobex_count, tobex_ratio)
					
		
	def measure():
		min_chlen, singles, coerced, zeroes, results = reduce()			
		avlen, tobex_count, tobex_ratio = detail()
		avtuples = [tuple for tuple in diagram.loop_tuples if len([loop for loop in tuple if loop.availabled]) == diagram.spClass-2]
		
		return (min_chlen, singles, coerced, zeroes, results, avlen, tobex_count, tobex_ratio, avtuples)

	def step(jump_lvl=0, jump_path=[[-1,0]], extuples=[], step_lvl=0, step_path=[[-1,0,False]], exloops=[]):
		global move_index						
		log_template = "[*{}*][{}][lvl:{}/{}#{}#{}] [step] {} | avtuples: {} | chlen: {} | avlen: {} | s: {} | c: {} | z: {} | tobex c: {} r: {:.3f}"
	
		# initial measurement	
		base_min_chlen, base_singles, base_coerced, base_zeroes, results, base_avlen, base_tobex_count, base_tobex_ratio, base_avtuples = measure()
		step_path[-1][1] = len(base_avtuples)
								
		move_index += 1
		if move_index % 1 == 0:
			with open(running_filename + ".txt", 'a') as log:
				log.write((log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "|".join([str(x)+"."+str(t)+("b" if b else "") for x,t,b in step_path]), "-- --", len(base_avtuples), base_min_chlen, base_avlen, len(base_singles), len(base_coerced), len(base_zeroes), base_tobex_count, base_tobex_ratio) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n" + "\n| ".join([str(l) for l in exloops]) + "\n\n").replace("⟩", ")").replace("⟨", "("))

		diagram.point(); show(diagram)
		input(log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t)+("ᵝ" if b else "") for x,t,b in step_path]), "-- init --", len(base_avtuples), base_min_chlen, base_avlen, len(base_singles), len(base_coerced), len(base_zeroes), base_tobex_count, base_tobex_ratio))
					
																		
		if len(diagram.chains) == 1:
			with open(sols_filename + ".txt", 'a') as log:
				log.write((log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "|".join([str(x)+"."+str(t)+("b" if b else "") for x,t,b in step_path]), "-- --", len(base_avtuples), base_min_chlen, base_avlen, len(base_singles), len(base_coerced), len(base_zeroes), base_tobex_count, base_tobex_ratio) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n" + "\n| ".join([str(l) for l in exloops]) + "\n\n").replace("⟩", ")").replace("⟨", "("))
			show(diagram)
			input("sol! " + log_line)
			pass # will clean() and return
						
		elif base_min_chlen == 0:
			input(log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t)+("ᵝ" if b else "") for x,t,b in step_path]), "-- failed by measure --", len(base_avtuples), base_min_chlen, base_avlen, len(base_singles), len(base_coerced), len(base_zeroes), base_tobex_count, base_tobex_ratio))			
			pass # will clean() and return
		
		else:
			seen_loops = []
			
			seen_singles = []
			seen_coerced = []
			seen_zeroes = []
			
			while True:
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
				
				selected_loop = filtered_results[0][0]
				step_path[-1][0] += 1
				step_path[-1][1] = len(filtered_results)
				step_path[-1][2] = binary
				
				diagram.point(); show(diagram)
				input(log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t)+("ᵝ" if b else "") for x,t,b in step_path]), "-- extending " + str(selected_loop) + " | " + str(filtered_results[-1][1]) +  " --", len(base_avtuples), base_min_chlen, base_avlen, len(base_singles), len(base_coerced), len(base_zeroes), base_tobex_count, base_tobex_ratio))

				assert diagram.extendLoop(selected_loop)
				step(jump_lvl, jump_path, extuples, step_lvl+1, step_path+[[-1, 0, False]], exloops+[selected_loop])
				diagram.collapseBack(selected_loop)
				
				diagram.setLoopUnavailabled(selected_loop)
				seen_loops.append(selected_loop)

												
				curr_min_chlen, curr_singles, curr_coerced, curr_zeroes, results, curr_avlen, curr_tobex_count, curr_tobex_ratio, curr_avtuples = measure()
				seen_singles += curr_singles
				seen_coerced += curr_coerced
				seen_zeroes += curr_zeroes

				diagram.point(); show(diagram)
				input(log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t)+("ᵝ" if b else "") for x,t,b in step_path]), "-- after seen " + str(selected_loop) + " | " + str(filtered_results[-1][1]) +  " --", len(curr_avtuples), curr_min_chlen, curr_avlen, len(curr_singles), len(curr_coerced), len(curr_zeroes), curr_tobex_count, curr_tobex_ratio))

				if len(diagram.chains) == 1:
					with open(sols_filename + ".txt", 'a') as log:
						log.write((log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "|".join([str(x)+"."+str(t)+("b" if b else "") for x,t,b in step_path]), "-- --", len(curr_avtuples), curr_min_chlen, curr_avlen, len(curr_singles), len(curr_coerced), len(curr_zeroes), curr_tobex_count, curr_tobex_ratio) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n" + "\n| ".join([str(l) for l in exloops]) + "\n\n").replace("⟩", ")").replace("⟨", "("))
					show(diagram)
					input("sol! " + log_line)
					pass # will clean() and return				
																				
				elif curr_min_chlen == 0:
					break # will clean() and return

			clean(seen_singles, seen_coerced, seen_zeroes)
			for l in seen_loops:
				diagram.setLoopAvailabled(l)																																																
			pass # will clean() and return		
			
		clean(base_singles, base_coerced, base_zeroes)
		
		
	head_filename = '__walk_6.1__'
	running_filename = head_filename + "running"
	
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

	def jump(lvl=0, jump_path=[[-1,0]], extuples=[], seen_tuples=[]):
		global move_index
		log_template = "[*{}*][{}][lvl:{}#{}] [jump] {} | avtuples: {} | chlen: {} | avlen: {} | s: {} | c: {} | z: {} | tobex c: {} r: {:.3f}"
	
		# initial measurement	
		base_min_chlen, base_singles, base_coerced, base_zeroes, base_results, base_avlen, base_tobex_count, base_tobex_ratio, base_avtuples = measure()
		base_avtuples = [t for t in base_avtuples if t not in seen_tuples]
		jump_path[-1][1] = len(base_avtuples)
						
		move_index += 1
		if move_index % 1 == 0:
			with open(running_filename + ".txt", 'a') as log:
				log.write((log_template.format(move_index, tstr(time() - startTime), lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "-- --", len(base_avtuples), base_min_chlen, base_avlen, len(base_singles), len(base_coerced), len(base_zeroes), base_tobex_count, base_tobex_ratio) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n\n").replace("⟩", ")").replace("⟨", "("))

		diagram.point(); show(diagram)
		input(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- init --", len(base_avtuples), base_min_chlen, base_avlen, len(base_singles), len(base_coerced), len(base_zeroes), base_tobex_count, base_tobex_ratio))
			
		# attempt to extend all tuples for viability and measurements
		viable_results = []	
	
		for tindex, curr_tuple in enumerate(base_avtuples):
		
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
				curr_min_chlen, curr_singles, curr_coerced, curr_zeroes, curr_results, curr_avlen, curr_tobex_count, curr_tobex_ratio, curr_avtuples = measure()			
				curr_avtuples = [t for t in curr_avtuples if t not in seen_tuples]
				
				# check tuple viability
				if curr_min_chlen != 0:
					viable_results.append((curr_tuple, curr_min_chlen, curr_avlen, len(curr_singles), len(curr_coerced), len(curr_zeroes), curr_tobex_count, curr_tobex_ratio, len(curr_avtuples)))
					# diagram.point()
					# show(diagram)
					print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- [tuple:"+str(tindex)+"] passed --", len(curr_avtuples), curr_min_chlen, curr_avlen, len(curr_singles), len(curr_coerced), len(curr_zeroes), curr_tobex_count, curr_tobex_ratio))								
				else:
					# diagram.point()
					# show(diagram)
					print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- [tuple:"+str(tindex)+"] failed by measure --", len(curr_avtuples), curr_min_chlen, curr_avlen, len(curr_singles), len(curr_coerced), len(curr_zeroes), curr_tobex_count, curr_tobex_ratio))					
					
				# clean up after current measurement
				clean(curr_singles, curr_coerced, curr_zeroes)
			else:
				# diagram.point()
				# show(diagram)			
				print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- [tuple:"+str(tindex)+"] failed by "+str(len(curr_extended_loops))+"/"+str(len(curr_tuple))+" --", 0, 0, 0, 0, 0, 0, 0, 0))
						
			# collapse current tuple				
			for loop in reversed(curr_extended_loops):
				diagram.collapseBack(loop)
												
		# sort by len(avtuples), tobex_ratio, min_chlen
		viable_results = sorted(viable_results, key = lambda pair: (pair[-1], pair[-2], pair[1]))
		jump_path[-1][1] = len(viable_results)
		input("viable results: " + str(len(viable_results)))
		input("\n".join([str([loop.firstAddress() for loop in v[0]]) + ", " + str(v[1:]) for v in viable_results]))		

		if len(viable_results) == 0: # no more tuples, go on stepping
			
			step(lvl, jump_path, extuples)
			
		else: # jump viable tuple
			for viable_index, viable_entry in enumerate(reversed(viable_results)):
				jump_path[-1][0] = viable_index
				
				viable_tuple = viable_entry[0]
				viable_measurement = viable_entry[1:]
			
				# extend viable tuple
				for loop in viable_tuple:
					assert diagram.extendLoop(loop)
				
				jump(lvl+1, jump_path+[[-1,0]], extuples+[viable_tuple], seen_tuples+[r[0] for r in viable_results[0:viable_index]])
					
				# collapse viable tuple				
				for loop in reversed(viable_tuple):
					diagram.collapseBack(loop)				
		
		# clean up after initial measurement
		clean(base_singles, base_coerced, base_zeroes)
	
	
	startTime = time()
	move_index = -1
	
	show(diagram)
	input("----------")
	lvl = 0
	ass_before = detail()
	jump()
	ass_after = detail()
	assert ass_before == ass_after, "broken first step"
	show(diagram)	
	print("------------")
