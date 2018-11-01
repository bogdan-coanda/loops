from diagram import *
from uicanvas import *
from common import *
from itertools import chain
from time import time
from collections import defaultdict

if __name__ == "__main__":
	
	# diagram = Diagram(6, 3)
	diagram = Diagram(7, 4)
	
	def extend(addr):
		assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	def collapse(addr):
		diagram.collapseBack(diagram.nodeByAddress[addr].loop)
					
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
		
																								
	results0 = defaultdict(int)		
	zeroes0 = []
	results1 = defaultdict(int)		
	zeroes1 = []	
	results2 = defaultdict(int)		
	zeroes2 = []	

	results_filename = "__gg__lvl2__results.txt"
	zeroes_filename = "__gg__zeroes.txt"
	minim_filename = "__gg__minim.txt"
	maxim_filename = "__gg__maxim.txt"
	sols_filename = "__gg__sols.txt"
	
	# [base] avlen: 636 | min chlen: 5 | tobex count: 120 ratio: 5.3
	startTime = time()
	
	# [base] avlen: 629 | min chlen: 4 | tobex count: 119 ratio: 5.285714285714286
	extend('000001')
	

																																													
	min_chlenZ, singlesZ, coercedZ = coerce()
	
	headChainZ = diagram.startNode.cycle.chain
	avlenZ = len([l for l in diagram.loops if l.availabled])
	tobex_countZ = diagram.measureTobex()
	tobex_ratioZ = (avlenZ / tobex_countZ) if tobex_countZ is not 0 else 0
			
	min_found_tobex_ratio0 = 99999999999999
	max_found_tobex_ratio0 = 0
	min_found_tobex_ratio1 = 99999999999999
	max_found_tobex_ratio1 = 0
	min_found_tobex_ratio2 = 99999999999999
	max_found_tobex_ratio2 = 0
		
	diagram.point()
	show(diagram)
	input("[base] avlen: " + str(avlenZ) + " | min chlen: " + str(min_chlenZ) + " | tobex count: " + str(tobex_countZ) + " ratio: " + str(tobex_ratioZ) + "\nsingles: " + str(singlesZ) + "\ncoerced: " + str(coercedZ) + " | head chain: " + str(headChainZ) + " | head loops: " + str(len(headChainZ.avloops)))
	
#-### ~~~ lvl:0 ~~~ ###
	for i0, loop0 in enumerate(headChainZ.avloops):
		diagram.extendLoop(loop0)
		min_chlen0, singles0, coerced0 = coerce()
		headChain0 = diagram.startNode.cycle.chain
		avlen0 = len([l for l in diagram.loops if l.availabled])
		tobex_count0 = diagram.measureTobex()
		tobex_ratio0 = (avlen0 / tobex_count0) if tobex_count0 != 0 else 0

		results0[(
			avlen0, 
			min_chlen0,
			len(headChain0.avloops),
			-(len(singles0)), 
			-(len(coerced0)),
			tobex_count0,
			tobex_ratio0
		)] += 1
			
		log_line0 = ("["+tstr(time() - startTime)+"] avlen: " + str(avlen0) + " | chlen: " + str(min_chlen0) + " | s: " + str(len(singles0)) + " | c: " + str(len(coerced0)) + " | tobex c: " + str(tobex_count0) + " r: " + str(tobex_ratio0) + " | head c: " + str(headChain0) + " av: " + str(len(headChain0.avloops)) + " @ " + str(i0) + "/" + str(len(headChainZ.avloops)) + "\n| " + str(loop0) + "\n\n").replace("⟩", ")").replace("⟨", "(")
			
		if min_chlen0 != 0 and tobex_ratio0 <= min_found_tobex_ratio0:
			min_found_tobex_ratio0 = tobex_ratio0
			with open("__0__"+minim_filename, 'a') as log:
				log.write(log_line0)
												
		if min_chlen0 != 0 and tobex_ratio0 >= max_found_tobex_ratio0:
			max_found_tobex_ratio0 = tobex_ratio0
			with open("__0__"+maxim_filename, 'a') as log:
				log.write(log_line0)
							
		if len(diagram.chains) == 1:
			with open("__0__"+sols_filename, 'a') as log:
				log.write(log_line0)
			show(diagram)
			input("sol! " + log_line0)
		
		elif min_chlen0 == 0:
			zeroes0.append((i0))
			with open("__0__"+zeroes_filename, 'a') as log:
				log.write(log_line0)
#---### ~~~ lvl:1 ~~~ ###				
		else:
			for i1, loop1 in enumerate(headChain0.avloops):
				if loop1.availabled: # [~] redundant currently
					diagram.extendLoop(loop1)
					min_chlen1, singles1, coerced1 = coerce()
					headChain1 = diagram.startNode.cycle.chain
					avlen1 = len([l for l in diagram.loops if l.availabled])
					tobex_count1 = diagram.measureTobex()
					tobex_ratio1 = (avlen1 / tobex_count1) if tobex_count1 != 0 else 0
		
					results1[(
						avlen1, 
						min_chlen1,  
						len(headChain1.avloops),
						-(len(singles0)+len(singles1)), 
						-(len(coerced0)+len(coerced1)),
						tobex_count1,
						tobex_ratio1
					)] += 1
					
					# if i1 % 120 == 0:
					# 	print("["+tstr(time() - startTime)+"] @ " + str(i0) + " " + str(i1) + " /" + str(avlenZ))

					log_line1 = ("["+tstr(time() - startTime)+"] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)) + " | tobex c: " + str(tobex_count1) + " r: " + str(tobex_ratio1) + " | head c: " + str(headChain1) + " av: " + str(len(headChain1.avloops)) + " @ " + str(i0) + "/" + str(len(headChainZ.avloops)) + " " + str(i1) + "/" + str(len(headChain0.avloops)) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n\n").replace("⟩", ")").replace("⟨", "(")
							
					if min_chlen1 != 0 and tobex_ratio1 <= min_found_tobex_ratio1:
						min_found_tobex_ratio1 = tobex_ratio1
						with open("__1__"+minim_filename, 'a') as log:
							log.write(log_line1)
							
					if min_chlen1 != 0 and tobex_ratio1 >= max_found_tobex_ratio1:
						max_found_tobex_ratio1 = tobex_ratio1
						with open("__1__"+maxim_filename, 'a') as log:
							log.write(log_line1)
							
					if len(diagram.chains) == 1:
						with open("__1__"+sols_filename, 'a') as log:
							log.write(log_line1)
						show(diagram)
						input(log_line1)
										
					elif min_chlen1 == 0:
						zeroes1.append((i0, i1))
						with open("__1__"+zeroes_filename, 'a') as log:
							log.write(log_line1)
#---------### ~~~ lvl:2 ~~~ ###
					else:
						for i2, loop2 in enumerate(headChain1.avloops): 
							if loop2.availabled:
								diagram.extendLoop(loop2)
								min_chlen2, singles2, coerced2 = coerce() 
								headChain2 = diagram.startNode.cycle.chain
								avlen2 = len([l for l in diagram.loops if l.availabled])
								tobex_count2 = diagram.measureTobex()
								tobex_ratio2 = (avlen2 / tobex_count2) if tobex_count2 != 0 else 0

								results2[(
									avlen2, 
									min_chlen2, 
									len(headChain2.avloops),
									-(len(singles0)+len(singles1)+len(singles2)), 
									-(len(coerced0)+len(coerced1)+len(coerced2)),
									tobex_count2,
									tobex_ratio2
								)] += 1

								if i2 % 10 == 0:
									print("["+tstr(time() - startTime)+"] @ " + str(i0) + " /" + str(len(headChainZ.avloops)) + " " + str(i1) + " /" + str(len(headChain0.avloops)) + " " + str(i2) + " /" + str(len(headChain1.avloops)))							
									
								log_line2 = ("["+tstr(time() - startTime)+"] avlen: " + str(avlen2) + " | chlen: " + str(min_chlen2) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)) + " | tobex c: " + str(tobex_count2) + " r: " + str(tobex_ratio2) + " | head c: " + str(headChain2) + " av: " + str(len(headChain2.avloops)) + " @ " + str(i0) + "/" + str(len(headChainZ.avloops)) + " " + str(i1) + "/" + str(len(headChain0.avloops)) + " " + str(i2) + "/" + str(len(headChain1.avloops)) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n| " + str(loop2) + "\n\n").replace("⟩", ")").replace("⟨", "(")

								if min_chlen2 != 0 and tobex_ratio2 <= min_found_tobex_ratio2:
									min_found_tobex_ratio2 = tobex_ratio2
									with open("__2__"+minim_filename, 'a') as log:
										log.write(log_line2)

								if min_chlen2 != 0 and tobex_ratio2 >= max_found_tobex_ratio2:
									max_found_tobex_ratio2 = tobex_ratio2
									with open("__2__"+maxim_filename, 'a') as log:
										log.write(log_line2)

								if len(diagram.chains) == 1:
									with open("__2__"+sols_filename, 'a') as log:
										log.write(log_line2)
									show(diagram)
									input(log_line2)							

								elif min_chlen2 == 0:
									zeroes2.append((i0, i1, i2))

								for l in reversed(singles2):
									diagram.collapseBack(l)		
								for l in coerced2:
									diagram.setLoopAvailabled(l)
								diagram.collapseBack(loop2)
#---------### ~~~ lvl:2 ~~~ ###
					for l in reversed(singles1):
						diagram.collapseBack(l)		
					for l in coerced1:
						diagram.setLoopAvailabled(l)
					diagram.collapseBack(loop1)
					# break # [~]
#---### ~~~ lvl:1 ~~~ ###			
		for l in reversed(singles0):
			diagram.collapseBack(l)						
		for l in coerced0:
			diagram.setLoopAvailabled(l)			
		diagram.collapseBack(loop0)
		
		with open(results_filename, 'a') as log:
			total = 0
			for k,v in sorted(results2.items(), key = lambda pair: (0 if pair[0][1] == 0 else pair[0][-1], pair[0][-1], pair[0][0], pair[0][1])):
				log.write(str(k) + " : " + str(v) + "\n")
				total += v
			log.write("=== " + str(i0) + ": " + str(total) + " | @ " + tstr(time() - startTime) + "\n")
		results2.clear()		
		# with open(zeroes_filename, 'a') as log:
		# 	for e in zeroes2:
		# 		log.write((str(e) + " : " + "|".join([str(avloopsZ[i]) for i in e]) + "\n").replace("⟩", ")").replace("⟨", "("))
		# 	log.write("=== " + str(i0) + ": " + str(len(zeroes2)) + " | @ " + tstr(time() - startTime) + "\n")
		# zeroes2.clear()
		# break # [~]		
#-### ~~~ lvl:0 ~~~ ###
				
	diagram.point()
	show(diagram)
	
	sorted0 = sorted(results0.items(), key = lambda pair: (0 if pair[0][1] == 0 else pair[0][-1], pair[0][-1], pair[0][0], pair[0][1]))
	print("["+tstr(time() - startTime)+"] lvl:0\n| results:\n" + "\n".join(str(pair[0])+": "+str(pair[1]) for pair in sorted0)+"\n| zeroes:\n"+"\n".join([str(e) for e in zeroes0]))
	sorted1 = sorted(results1.items(), key = lambda pair: (0 if pair[0][1] == 0 else pair[0][-1], pair[0][-1], pair[0][0], pair[0][1]))	
	print("["+tstr(time() - startTime)+"] lvl:1\n| results:\n" + "\n".join(str(pair[0])+": "+str(pair[1]) for pair in sorted1)+"\n| zeroes:\n"+"\n".join([str(e) for e in zeroes1]))

	results2.clear()
	with open(results_filename, 'r') as log:
		lines = log.read().splitlines()
		for line in lines:
			if not line.startswith("==="):
				key = tuple(int(x) if '.' not in x else float(x) for x in line.split(" : ")[0][1:-1].split(", "))
				val = int(line.split(" : ")[1])
				results2[key] += val
	zeroes2count = len(zeroes2)
	# with open(zeroes_filename, 'r') as log:
	# 	lines = log.read().splitlines()
	# 	for line in lines:
	# 		if not line.startswith("==="):		
	# 			zeroes2count += 1

	sorted2 = sorted(results2.items(), key = lambda pair: (0 if pair[0][1] == 0 else pair[0][-1], pair[0][-1], pair[0][0], pair[0][1]))
	print("["+tstr(time() - startTime)+"] lvl:2\n| results:\n" + "\n".join(str(pair[0])+": "+str(pair[1]) for pair in sorted2)+"\n| zeroes: "+str(zeroes2count))

