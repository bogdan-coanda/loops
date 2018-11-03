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

	results_filename = "__gg5__lvl2__results.txt"
	zeroes_filename = "__gg5__zeroes.txt"
	minim_filename = "__gg5__minim.txt"
	maxim_filename = "__gg5__maxim.txt"
	sols_filename = "__gg5__sols.txt"
	
	# [base] avlen: 636 | min chlen: 5 | tobex count: 120 ratio: 5.3
	startTime = time()
	
	# [base] avlen: 629 | min chlen: 4 | tobex count: 119 ratio: 5.285714285714286
	extend('000001')
	
	# __2____gg__minim
	# [38m32s.983] avlen: 591 | chlen: 3 | s: 0 | c: 0 | tobex c: 116 r: 5.094827586206897 | head c: (chain:1404168|140/111) av: 111
	# @ 86/110 67/115 117/118
	# | (loop:[green:80]:110005|Ex)
	# | (loop:[yellow:82]:110220|Ex)
	# | (loop:[green:84]:110041|Ex)

	extend('110005')
	extend('110220')
	extend('110041')

	# __2____gg2__minim
	# [9m16s.830] avlen: 542 | chlen: 2 | s: 2 | c: 2 | tobex c: 111 r: 4.882882882882883 | head c: (chain:579798|165/127) av: 127
	# @ 36/111 3/116 1/130
	# | (loop:[indigo:80]:020001|Ex)
	# | (loop:[orange:111]:101101|Ex)
	# | (loop:[orange:96]:101053|Ex)

	extend('020001')
	extend('101101')
	extend('101053')

	# __2____gg3__minim
	# [62m48s.733] avlen: 445 | chlen: 2 | s: 8 | c: 6 | tobex c: 100 r: 4.45 | head c: (chain:2537694|215/136) av: 136
	# @ 102/127 72/135 54/132
	# | (loop:[indigo:87]:020312|Ex)
	# | (loop:[yellow:96]:110031|Ex)
	# | (loop:[blue:103]:120306|Ex)

	extend('020312')
	extend('110031')
	extend('120306')

	# __2____gg4__minim
	# [5m6s.259] avlen: 202 | chlen: 2 | s: 38 | c: 11 | tobex c: 59 r: 3.4237288135593222 | head c: (chain:155678|345/103) av: 103
	# @ 3/136 130/132 7/133
	# | (loop:[green:93]:112032|Ex)
	# | (loop:[indigo:37]:003312|Ex)
	# | (loop:[blue:91]:112106|Ex)

	extend('112032')
	extend('003312')
	extend('112106')
	
	min_chlenZ, singlesZ, coercedZ = coerce()
	
	headChainZ = diagram.startNode.cycle.chain
	headLoopsZ = list(headChainZ.avloops)
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
		headLoops0 = [l for l in headLoopsZ[i0+1:] if l in headChain0.avloops] + [l for l in list(headChain0.avloops) if l not in headLoopsZ]
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
					headLoops1 = [l for l in headLoops0[i0+1:] if l in headChain1.avloops] + [l for l in list(headChain1.avloops) if l not in headLoops0]
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
								headLoops2 = [l for l in headLoops1[i2+1:] if l in headChain2.avloops] + [l for l in list(headChain2.avloops) if l not in headLoops1]
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

