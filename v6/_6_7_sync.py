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

	results_filename = "__203__tobex__lvl2__results.txt"
	zeroes_filename = "__203__tobex__zeroes.txt"
	found_filename = "__203__tobex__found.txt"
	minim_filename = "__203__tobex__minim.txt"

	# [base] avlen: 636 | min chlen: 5 | tobex count: 120 ratio: 5.3
	startTime = time()
	
	# [base] avlen: 629 | min chlen: 4 | tobex count: 120 ratio: 5.241666666666666
	extend('000001')
	
	# [274m30s.84] avlen: 591 | chlen: 3 | s: 0 | c: 0 | tobex c: 117 r: 5.051282051282051
	# @ 510 519 529 /629
	# | (loop:[green:80]:110005|Ex)
	# | (loop:[green:84]:110041|Ex)
	# | (loop:[yellow:82]:110220|Ex)
	
	extend('110005')
	extend('110041')
	extend('110220')
	
	# [200m1s.347] avlen: 542 | chlen: 2 | s: 2 | c: 2 | tobex c: 115 r: 4.71304347826087
	# @ 255 427 428 /591
	# | (loop:[indigo:80]:020001|Ex)
	# | (loop:[orange:96]:101053|Ex)
	# | (loop:[orange:111]:101101|Ex)

	extend('020001')
	extend('101053')
	extend('101101')
	
	# [430m27s.886] avlen: 445 | chlen: 2 | s: 8 | c: 6 | tobex c: 109 r: 4.08256880733945
	# @ 270 450 508 /542
	# | (loop:[indigo:87]:020312|Ex)
	# | (loop:[yellow:96]:110031|Ex)
	# | (loop:[blue:103]:120306|Ex)
	
	extend('020312')
	extend('110031')
	extend('120306')
	
	# [59m39s.470] avlen: 203 | chlen: 2 | s: 36 | c: 41 | tobex c: 81 r: 2.506172839506173
	# @ 17 166 424 /445
	# | (loop:[orange:25]:002034|Ex)
	# | (loop:[red:35]:013020|Ex)
	# | (loop:[green:106]:121014|Ex)
	
	extend('002034')
	extend('013020')
	extend('121014')
	
	# extend('100004')
	# extend('100012')
	# extend('121014')
	
	# [0m1s.894] avlen: 527 | chlen: 2 | s: 5 | c: 0 @ 443 475 394 /587
	# | (loop:[green:72]:102023|Ex)
	# | (loop:[blue:79]:103406|Ex)
	# | (loop:[yellow:78]:100211|Ex)	
	
	# extend('102023')
	# extend('103406')
	# extend('100211')
	
	# [257m7s.946] avlen: 394 | chlen: 2 | s: 12 | c: 1 @ 386 398 505 /527
	# | (loop:[blue:68]:101306|Ex)
	# | (loop:[green:74]:102041|Ex)
	# | (loop:[blue:108]:121306|Ex)

	# extend('101306')
	# extend('102041')
	# extend('121306')
			
	min_chlenZ, singlesZ, coercedZ = coerce()
	
	avloopsZ = [l for l in diagram.loops if l.availabled]
	avlenZ = len(avloopsZ)
	tobex_countZ = diagram.tobex_base_count - len([l for l in avloopsZ if l.extended])
	tobex_ratioZ = (avlenZ / tobex_countZ) if tobex_countZ is not 0 else 0
			
	min_found_tobex_ratio2 = tobex_ratioZ*2
			
	diagram.point()
	show(diagram)
	input("[base] avlen: " + str(avlenZ) + " | min chlen: " + str(min_chlenZ) + " | tobex count: " + str(tobex_countZ) + " ratio: " + str(tobex_ratioZ) + "\nsingles: " + str(singlesZ) + "\ncoerced: " + str(coercedZ))
	
#-### ~~~ lvl:0 ~~~ ###
	for i0 in range(0, avlenZ):
		loop0 = avloopsZ[i0]		
		diagram.extendLoop(loop0)
		min_chlen0, singles0, coerced0 = coerce()
		avlen0 = len([l for l in avloopsZ if l.availabled])
		tobex_count0 = diagram.tobex_base_count - len([l for l in avloopsZ if l.extended])
		tobex_ratio0 = (avlen0 / tobex_count0) if tobex_count0 != 0 else 0

		results0[(
			avlen0, 
			min_chlen0, 
			-(len(singles0)), 
			-(len(coerced0)),
			tobex_count0,
			tobex_ratio0
		)] += 1
			
		if min_chlen0 == 0:
			zeroes0.append((i0))
			print("[lvl:0] avlen: " + str(avlen0) + " | chlen: " + str(min_chlen0) + " | s: " + str(len(singles0)) + " | c: " + str(len(coerced0)) + " | tobex c: " + str(tobex_count0) + " r: " + str(tobex_ratio0))
			with open(zeroes_filename, 'a') as log:
				log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen0) + " | chlen: " + str(min_chlen0) + " | s: " + str(len(singles0)) + " | c: " + str(len(coerced0)) + " | tobex c: " + str(tobex_count0) + " r: " + str(tobex_ratio0) + " @ " + str(i0) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n\n").replace("⟩", ")").replace("⟨", "("))
#---### ~~~ lvl:1 ~~~ ###				
		else:
			for i1 in range(i0+1, avlenZ):
				loop1 = avloopsZ[i1]
				if loop1.availabled:
					diagram.extendLoop(loop1)
					min_chlen1, singles1, coerced1 = coerce()
					avlen1 = len([l for l in avloopsZ if l.availabled])
					tobex_count1 = diagram.tobex_base_count - len([l for l in avloopsZ if l.extended])
					tobex_ratio1 = (avlen1 / tobex_count1) if tobex_count1 != 0 else 0
		
					results1[(
						avlen1, 
						min_chlen1,  
						-(len(singles0)+len(singles1)), 
						-(len(coerced0)+len(coerced1)),
						tobex_count1,
						tobex_ratio1
					)] += 1

					if min_chlen1 == 0:
						zeroes1.append((i0, i1))
						print("[lvl:1] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)) + " | tobex c: " + str(tobex_count1) + " r: " + str(tobex_ratio1))
						with open(zeroes_filename, 'a') as log:
							log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)) + " | tobex c: " + str(tobex_count1) + " r: " + str(tobex_ratio1) + " @ " + str(i0) + " " + str(i1) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n\n").replace("⟩", ")").replace("⟨", "("))
#---------### ~~~ lvl:2 ~~~ ###
					else:
						for i2 in range(i1+1, avlenZ): 
							loop2 = avloopsZ[i2]
							if loop2.availabled:
								diagram.extendLoop(loop2)
								min_chlen2, singles2, coerced2 = coerce() 
								avlen2 = len([l for l in avloopsZ if l.availabled])
								tobex_count2 = diagram.tobex_base_count - len([l for l in avloopsZ if l.extended])
								tobex_ratio2 = (avlen2 / tobex_count2) if tobex_count2 != 0 else 0
					
								results2[(
									avlen2, 
									min_chlen2, 
									-(len(singles0)+len(singles1)+len(singles2)), 
									-(len(coerced0)+len(coerced1)+len(coerced2)),
									tobex_count2,
									tobex_ratio2
								)] += 1

								#if min_chlen2 == 0:
								#	zeroes2.append((i0, i1, i2))
								#	print("[lvl:2] avlen: " + str(avlen2) + " | chlen: " + str(min_chlen2) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)) + " | tobex c: " + str(tobex_count2) + " r: " + str(tobex_ratio2))

								if i2 % 100 == 0:
									print("["+tstr(time() - startTime)+"] @ " + str(i0) + " " + str(i1) + " " + str(i2) + " /" + str(avlenZ))							

								if min_chlen2 != 0 and tobex_ratio2 <= min_found_tobex_ratio2:
									min_found_tobex_ratio2 = tobex_ratio2
									with open(minim_filename, 'a') as log:
										log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen2) + " | chlen: " + str(min_chlen2) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)) + " | tobex c: " + str(tobex_count2) + " r: " + str(tobex_ratio2) + " @ " + str(i0) + " " + str(i1) + " " + str(i2) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n| " + str(loop2) + "\n\n").replace("⟩", ")").replace("⟨", "("))
																		
								# if avlen2 <= 157: # or min_chlen2 == 0:
								# 	with open(found_filename, 'a') as log:
								# 		log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen2) + " | chlen: " + str(min_chlen2) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)) + " | tobex c: " + str(tobex_count2) + " r: " + str(tobex_ratio2) + " @ " + str(i0) + " " + str(i1) + " " + str(i2) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n| " + str(loop2) + "\n\n").replace("⟩", ")").replace("⟨", "("))

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
					# if i1 % 300 == 0:
					# 	print("["+tstr(time() - startTime)+"] @ " + str(i0) + " " + str(i1) + " /" + str(avlenZ))												
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
		with open(zeroes_filename, 'a') as log:
			for e in zeroes2:
				log.write((str(e) + " : " + "|".join([str(avloopsZ[i]) for i in e]) + "\n").replace("⟩", ")").replace("⟨", "("))
			log.write("=== " + str(i0) + ": " + str(len(zeroes2)) + " | @ " + tstr(time() - startTime) + "\n")
		zeroes2.clear()
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
	zeroes2count = 0
	with open(zeroes_filename, 'r') as log:
		lines = log.read().splitlines()
		for line in lines:
			if not line.startswith("==="):		
				zeroes2count += 1

	sorted2 = sorted(results2.items(), key = lambda pair: (0 if pair[0][1] == 0 else pair[0][-1], pair[0][-1], pair[0][0], pair[0][1]))
	print("["+tstr(time() - startTime)+"] lvl:2\n| results:\n" + "\n".join(str(pair[0])+": "+str(pair[1]) for pair in sorted2)+"\n| zeroes: "+str(zeroes2count))

