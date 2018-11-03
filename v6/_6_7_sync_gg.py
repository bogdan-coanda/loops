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

	results_filename = "__ff6__lvl2__results.txt"
	zeroes_filename = "__ff6__zeroes.txt"
	minim_filename = "__ff6__minim.txt"
	maxim_filename = "__ff6__maxim.txt"
	sols_filename = "__ff6__sols.txt"
	
	# [base] avlen: 636 | min chlen: 5 | tobex count: 120 ratio: 5.3
	startTime = time()
	
	# [base] avlen: 629 | min chlen: 4 | tobex count: 119 ratio: 5.285714285714286
	extend('000001')

	# __2____ff1__maxim
	# [6m22s.68] avlen: 611 | chlen: 3 | s: 0 | c: 0 | tobex c: 116 r: 5.267241379310345 | head c: (chain:412431|140/146) av: 146
	# @ 95/110 11/28 5/31
	# | (loop:[red:21]:010100|Ex)
	# | (loop:[indigo:106]:021203|Ex)
	# | (loop:[blue:47]:021206|Ex)
	
	extend('010100')
	extend('021203')
	extend('021206')

	# __2____ff2__maxim
	# [13m29s.226] avlen: 593 | chlen: 3 | s: 0 | c: 0 | tobex c: 113 r: 5.247787610619469 | head c: (chain:726492|155/183) av: 183
	# @ 89/146 27/72 22/61
	# | (loop:[indigo:39]:003453|Ex)
	# | (loop:[violet:118]:013354|Ex)
	# | (loop:[green:57]:023023|Ex)

	extend('003453')
	extend('013354')
	extend('023023')

	# __2____ff3__maxim
	# 16m22s.953] avlen: 569 | chlen: 3 | s: 1 | c: 0 | tobex c: 109 r: 5.220183486238532 | head c: (chain:667263|170/211) av: 211
	# @ 39/183 40/159 15/130
	# | (loop:[orange:39]:001412|Ex)
	# | (loop:[indigo:78]:003354|Ex)
	# | (loop:[blue:22]:010206|Ex)

	extend('001412')
	extend('003354')
	extend('010206')

	# __2____ff4__maxim
	# [50m20s.125] avlen: 549 | chlen: 3 | s: 0 | c: 0 | tobex c: 106 r: 5.179245283018868 | head c: (chain:1957259|185/241) av: 241
	# @ 181/211 12/43 26/44
	# | (loop:[yellow:70]:100253|Ex)
	# | (loop:[orange:112]:101152|Ex)
	# | (loop:[green:97]:113023|Ex)

	extend('100253')
	extend('101152')
	extend('113023')
	
	# __2____ff5__maxim
	# [71m10s.701] avlen: 524 | chlen: 3 | s: 1 | c: 0 | tobex c: 102 r: 5.137254901960785 | head c: (chain:2152652|200/254) av: 254
	# @ 97/241 88/152 6/67
	# | (loop:[red:103]:010321|Ex)
	# | (loop:[yellow:62]:100220|Ex)
	# | (loop:[yellow:66]:100244|Ex)
	
	extend('010321')
	extend('100220')
	extend('100244')

	min_chlenZ, singlesZ, coercedZ = coerce()
	
	headChainZ = diagram.startNode.cycle.chain
	headLoopsZ = sorted(headChainZ.avloops, key = lambda l: l.firstAddress())
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
	input("[base] avlen: " + str(avlenZ) + " | min chlen: " + str(min_chlenZ) + " | tobex count: " + str(tobex_countZ) + " ratio: " + str(tobex_ratioZ) + "\nsingles: " + str(singlesZ) + "\ncoerced: " + str(coercedZ) + " | head chain: " + str(headChainZ) + " | head loops: " + str(len(headLoopsZ)))
	
#-### ~~~ lvl:0 ~~~ ###
	for i0, loop0 in enumerate(headLoopsZ):
		diagram.extendLoop(loop0)
		min_chlen0, singles0, coerced0 = coerce()
		headChain0 = diagram.startNode.cycle.chain
		headLoops0 = sorted(set(headChain0.avloops).difference(headLoopsZ[:i0+1]), key = lambda l: l.firstAddress())
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
			
		log_line0 = ("["+tstr(time() - startTime)+"] avlen: " + str(avlen0) + " | chlen: " + str(min_chlen0) + " | s: " + str(len(singles0)) + " | c: " + str(len(coerced0)) + " | tobex c: " + str(tobex_count0) + " r: " + str(tobex_ratio0) + " | head c: " + str(headChain0) + " av: " + str(len(headChain0.avloops)) + " @ " + str(i0) + "/" + str(len(headLoopsZ)) + "\n| " + str(loop0) + "\n\n").replace("⟩", ")").replace("⟨", "(")
			
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
			for i1, loop1 in enumerate(headLoops0):
				if loop1.availabled: # [~] redundant currently
					diagram.extendLoop(loop1)
					min_chlen1, singles1, coerced1 = coerce()
					headChain1 = diagram.startNode.cycle.chain
					headLoops1 = sorted(set(headChain1.avloops).difference(headLoopsZ[:i0+1]).difference(headLoops0[:i1+1]), key = lambda l: l.firstAddress())
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

					log_line1 = ("["+tstr(time() - startTime)+"] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)) + " | tobex c: " + str(tobex_count1) + " r: " + str(tobex_ratio1) + " | head c: " + str(headChain1) + " av: " + str(len(headChain1.avloops)) + " @ " + str(i0) + "/" + str(len(headLoopsZ)) + " " + str(i1) + "/" + str(len(headLoops0)) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n\n").replace("⟩", ")").replace("⟨", "(")
							
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
						for i2, loop2 in enumerate(headLoops1): 
							if loop2.availabled:
								diagram.extendLoop(loop2)
								min_chlen2, singles2, coerced2 = coerce() 
								headChain2 = diagram.startNode.cycle.chain
								#headLoops2 = sorted(set(headChain2.avloops).difference(headLoopsZ[:i0+1]).difference(headLoops0[:i1+1]).difference(headLoops0[:i2+1]), key = lambda l: l.firstAddress())
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

								if i2 % 20 == 0:
									print("["+tstr(time() - startTime)+"] @ " + str(i0) + " /" + str(len(headLoopsZ)) + " " + str(i1) + " /" + str(len(headLoops0)) + " " + str(i2) + " /" + str(len(headLoops1)))							
									
								log_line2 = ("["+tstr(time() - startTime)+"] avlen: " + str(avlen2) + " | chlen: " + str(min_chlen2) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)) + " | tobex c: " + str(tobex_count2) + " r: " + str(tobex_ratio2) + " | head c: " + str(headChain2) + " av: " + str(len(headChain2.avloops)) + " @ " + str(i0) + "/" + str(len(headLoopsZ)) + " " + str(i1) + "/" + str(len(headLoops0)) + " " + str(i2) + "/" + str(len(headLoops1)) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n| " + str(loop2) + "\n\n").replace("⟩", ")").replace("⟨", "(")

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

