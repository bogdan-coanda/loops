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
			if len([loop for loop in tuple if loop.availabled]) == diagram.spClass-2
			and len([loop for loop in tuple if len([node.cycle for node in loop.nodes if node.cycle.isKernel]) != 0]) == 0]
		return (min_chlen, avlen, chain_count, tobex_count, tobex_ratio, avtuples)
					
		

	def step(jump_lvl=0, jump_path=[[-1,0]], extuples=[], step_lvl=0, step_path=[[-1,0,False]], exloops=[]):
		global move_index, sol_count	
		log_template = "[*{}*][{}][lvl:{}/{}#{}#{}] [step] {} | avtuples: {} | chlen: {} | avlen: {} | chains: {} | s: {} | c: {} | z: {} | r: {} | tobex c: {} r: {:.3f}"
	
		# initial measurement	
		base_mx = Measurement.measure(diagram)
		step_path[-1][1] = len(base_mx.avtuples)
								
		move_index += 1
		if move_index % 1 == 0:
			with open(running_filename + ".txt", 'a') as log:
				log.write((log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "|".join([str(x)+"."+str(t)+("b" if b else "") for x,t,b in step_path]), "-- --", len(base_mx.avtuples), base_mx.min_chlen, base_mx.avlen, base_mx.chain_count, len(base_mx.singles), len(base_mx.coerced), len(base_mx.zeroes), len(base_mx.results), base_mx.tobex_count, base_mx.tobex_ratio) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n" + "\n| ".join([str(l) for l in exloops]) + "\n\n").replace("⟩", ")").replace("⟨", "("))

		# diagram.point(); show(diagram)
		print(log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t)+("ᵝ" if b else "") for x,t,b in step_path]), "-- init --", len(base_mx.avtuples), base_mx.min_chlen, base_mx.avlen, base_mx.chain_count, len(base_mx.singles), len(base_mx.coerced), len(base_mx.zeroes), len(base_mx.results), base_mx.tobex_count, base_mx.tobex_ratio))
					
																		
		if len(diagram.chains) == 1:
			with open(sols_filename + ".txt", 'a') as log:
				log.write((log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "|".join([str(x)+"."+str(t)+("b" if b else "") for x,t,b in step_path]), "-- --", len(base_mx.avtuples), base_mx.min_chlen, base_mx.avlen, base_mx.chain_count, len(base_mx.singles), len(base_mx.coerced), len(base_mx.zeroes), len(base_mx.results), base_mx.tobex_count, base_mx.tobex_ratio) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n" + "\n| ".join([str(l) for l in exloops]) + "\n\n").replace("⟩", ")").replace("⟨", "("))
			show(diagram)
			sol_count += 1
			input("sol! " + str(sol_count))
			pass # will clean() and return
						
		elif base_mx.min_chlen == 0:
			# print(log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t)+("ᵝ" if b else "") for x,t,b in step_path]), "-- failed by measure --", len(base_mx.avtuples), base_mx.min_chlen, base_mx.avlen, base_mx.chain_count, len(base_mx.singles), len(base_mx.coerced), len(base_mx.zeroes), len(base_mx.results), base_mx.tobex_count, base_mx.tobex_ratio))			
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
				# print(log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t)+("ᵝ" if b else "") for x,t,b in step_path]), "-- extending " + str(selected_loop) + " | " + str(selected_result[1]) +  " --", len(base_mx.avtuples), base_mx.min_chlen, base_mx.avlen, base_mx.chain_count, len(base_mx.singles), len(base_mx.coerced), len(base_mx.zeroes), len(results), base_mx.tobex_count, base_mx.tobex_ratio))

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
				# print(log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), ".".join([str(x)+upper(t)+("ᵝ" if b else "") for x,t,b in step_path]), "-- after seen " + str(selected_loop) + " | " + str(selected_result[1]) +  " --", len(curr_mx.avtuples), curr_mx.min_chlen, curr_mx.avlen, curr_mx.chain_count, len(curr_mx.singles), len(curr_mx.coerced), len(curr_mx.zeroes), len(results), curr_mx.tobex_count, curr_mx.tobex_ratio))

				if len(diagram.chains) == 1:
					with open(sols_filename + ".txt", 'a') as log:
						log.write((log_template.format(move_index, tstr(time() - startTime), jump_lvl, step_lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "|".join([str(x)+"."+str(t)+("b" if b else "") for x,t,b in step_path]), "-- --", len(curr_mx.avtuples), curr_mx.min_chlen, curr_mx.avlen, curr_mx.chain_count, len(curr_mx.singles), len(curr_mx.coerced), len(curr_mx.zeroes), len(results), curr_mx.tobex_count, curr_mx.tobex_ratio) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n" + "\n| ".join([str(l) for l in exloops]) + "\n\n").replace("⟩", ")").replace("⟨", "("))
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
	input("~~~")	
	

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
					# print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- [tuple:"+str(tindex)+"] passed --", len(curr_mx.avtuples), curr_mx.min_chlen, curr_mx.avlen, curr_mx.chain_count, len(curr_mx.singles), len(curr_mx.coerced), len(curr_mx.zeroes), len(curr_mx.results), curr_mx.tobex_count, curr_mx.tobex_ratio))
				else:
					# diagram.point(); show(diagram)
					# print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- [tuple:"+str(tindex)+"] failed by measure --", len(curr_mx.avtuples), curr_mx.min_chlen, curr_mx.avlen, curr_mx.chain_count, len(curr_mx.singles), len(curr_mx.coerced), len(curr_mx.zeroes), len(curr_mx.results), curr_mx.tobex_count, curr_mx.tobex_ratio))					
					pass
					
				# clean up after current measurement
				clean(curr_mx.singles, curr_mx.coerced, curr_mx.zeroes)
			else:
				# diagram.point(); show(diagram)			
				# print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- [tuple:"+str(tindex)+"] failed by "+str(len(curr_extended_loops))+"/"+str(len(curr_tuple))+" --", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
				pass
				
			# collapse current tuple				
			for loop in reversed(curr_extended_loops):
				diagram.collapseBack(loop)		

		return viable_results
		

	def jump(lvl=0, jump_path=[[-1,0]], extuples=[], seen_tuples=[]):
		global move_index
		log_template = "[*{}*][{}][lvl:{}#{}] [jump] {} | avtuples: {} | chlen: {} | avlen: {} | chains: {} | s: {} | c: {} | z: {} | r: {} | tobex c: {} r: {:.3f}"
	
		# initial measurement	
		base_mx = Measurement.measure(diagram)		
		base_mx.avtuples = [t for t in base_mx.avtuples if t not in seen_tuples]
		jump_path[-1][1] = len(base_mx.avtuples)
						
		move_index += 1
		if move_index % 1 == 0:
			with open(running_filename + ".txt", 'a') as log:
				log.write((log_template.format(move_index, tstr(time() - startTime), lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "-- --", len(base_mx.avtuples), base_mx.min_chlen, base_mx.avlen, base_mx.chain_count, len(base_mx.singles), len(base_mx.coerced), len(base_mx.zeroes), len(base_mx.results), base_mx.tobex_count, base_mx.tobex_ratio) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n\n").replace("⟩", ")").replace("⟨", "("))

		# diagram.point(); show(diagram)
		print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- init --", len(base_mx.avtuples), base_mx.min_chlen, base_mx.avlen, base_mx.chain_count, len(base_mx.singles), len(base_mx.coerced), len(base_mx.zeroes), len(base_mx.results), base_mx.tobex_count, base_mx.tobex_ratio))
			
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
		log_template = "[*{}*][{}][lvl:{}#{}] [jump] {} | avtuples: {} | chlen: {} | avlen: {} | chains: {} | s: {} | c: {} | z: {} | r: {} | tobex c: {} r: {:.3f}"
	
		# initial measurement	
		base_mx = Measurement.measure(diagram)		
		base_mx.avtuples = [t for t in base_mx.avtuples if t not in seen_tuples]
		jump_path[-1][1] = len(base_mx.avtuples)
		
		assert len(base_mx.singles) is 0
		
		move_index += 1
		if move_index % 1 == 0:
			with open(running_filename + ".txt", 'a') as log:
				log.write((log_template.format(move_index, tstr(time() - startTime), lvl, "|".join([str(x)+"."+str(t) for x,t in jump_path]), "-- --", len(base_mx.avtuples), base_mx.min_chlen, base_mx.avlen, base_mx.chain_count, len(base_mx.singles), len(base_mx.coerced), len(base_mx.zeroes), len(base_mx.results), base_mx.tobex_count, base_mx.tobex_ratio) + "\n" + "\n| ".join([" : ".join([str(l) for l in t]) for t in extuples]) + "\n\n").replace("⟩", ")").replace("⟨", "("))

		# diagram.point(); show(diagram)
		print(log_template.format(move_index, tstr(time() - startTime), lvl, ".".join([str(x)+upper(t) for x,t in jump_path]), "-- init --", len(base_mx.avtuples), base_mx.min_chlen, base_mx.avlen, base_mx.chain_count, len(base_mx.singles), len(base_mx.coerced), len(base_mx.zeroes), len(base_mx.results), base_mx.tobex_count, base_mx.tobex_ratio))
		
			
	
	startTime = time()
	move_index = -1
	sol_count = 0
	
	show(diagram)
	input("----------")
	lvl = 0
	ass_before = detail()
	jump()
	ass_after = detail()
	assert ass_before == ass_after, "broken first step"
	show(diagram)
	print("[*{}*][{}] sols found: {}".format(move_index, tstr(time() - startTime), sol_count))
	print("------------")
