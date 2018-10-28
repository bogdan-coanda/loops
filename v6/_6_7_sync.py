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

	results_filename = "__394_lvl2_results.txt"
	zeroes_filename = "__394_lvl2_zeroes.txt"
	found_filename = "__394__found.txt"

	startTime = time()
	extend('000001')
	extend('100004')
	extend('100012')
	extend('121014')
	
	# [0m1s.894] avlen: 527 | chlen: 2 | s: 5 | c: 0 @ 443 475 394 /587
	# | (loop:[green:72]:102023|Ex)
	# | (loop:[blue:79]:103406|Ex)
	# | (loop:[yellow:78]:100211|Ex)	
	
	extend('102023')
	extend('103406')
	extend('100211')
	
	# [257m7s.946] avlen: 394 | chlen: 2 | s: 12 | c: 1 @ 386 398 505 /527
	# | (loop:[blue:68]:101306|Ex)
	# | (loop:[green:74]:102041|Ex)
	# | (loop:[blue:108]:121306|Ex)

	extend('101306')
	extend('102041')
	extend('121306')
			
	min_chlenZ, singlesZ, coercedZ = coerce()
	
	avloopsZ = [l for l in diagram.loops if l.availabled]
	avlenZ = len(avloopsZ)
	
	diagram.point()
	show(diagram)
	input("[base] avlen: " + str(avlenZ) + " | min chlen: " + str(min_chlenZ) + "\nsingles: " + str(singlesZ) + "\ncoerced: " + str(coercedZ))
	
#-### ~~~ lvl:0 ~~~ ###
	for i0 in range(0, avlenZ):
		loop0 = avloopsZ[i0]		
		diagram.extendLoop(loop0)
		min_chlen0, singles0, coerced0 = coerce()
		avlen0 = len([l for l in avloopsZ if l.availabled])

		results0[(
			0 if min_chlen0 == 0 else avlen0, 
			min_chlen0 if min_chlen0 != 0 else avlen0, 
			-(len(singles0)), 
			-(len(coerced0))
		)] += 1
			
		if min_chlen0 == 0:
			zeroes0.append((i0))
			print("[lvl:0] avlen: " + str(avlen0) + " | chlen: " + str(min_chlen0) + " | s: " + str(len(singles0)) + " | c: " + str(len(coerced0)))
			with open(found_filename, 'a') as log:
				log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen0) + " | chlen: " + str(min_chlen0) + " | s: " + str(len(singles0)) + " | c: " + str(len(coerced0)) + " @ " + str(i0) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n\n").replace("⟩", ")").replace("⟨", "("))
#---### ~~~ lvl:1 ~~~ ###				
		else:
			for i1 in range(i0+1, avlenZ):
				loop1 = avloopsZ[i1]
				if loop1.availabled:
					diagram.extendLoop(loop1)
					min_chlen1, singles1, coerced1 = coerce()
					avlen1 = len([l for l in avloopsZ if l.availabled])

					results1[(
						0 if min_chlen1 == 0 else avlen1, 
						min_chlen1 if min_chlen1 != 0 else avlen1,  
						-(len(singles0)+len(singles1)), 
						-(len(coerced0)+len(coerced1))
					)] += 1

					if min_chlen1 == 0:
						zeroes1.append((i0, i1))
						print("[lvl:1] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)))
						with open(found_filename, 'a') as log:
							log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)) + " @ " + str(i0) + " " + str(i1) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n\n").replace("⟩", ")").replace("⟨", "("))
#---------### ~~~ lvl:2 ~~~ ###
					else:
						for i2 in range(i1+1, avlenZ): 
							loop2 = avloopsZ[i2]
							if loop2.availabled:
								diagram.extendLoop(loop2)
								min_chlen2, singles2, coerced2 = coerce() 
								avlen2 = len([l for l in avloopsZ if l.availabled])

								results2[(
									0 if min_chlen2 == 0 else avlen2, 
									min_chlen2 if min_chlen2 != 0 else avlen2, 
									-(len(singles0)+len(singles1)+len(singles2)), 
									-(len(coerced0)+len(coerced1)+len(coerced2))
								)] += 1

								if min_chlen2 == 0:
									zeroes2.append((i0, i1, i2))
									print("[lvl:2] avlen: " + str(avlen2) + " | chlen: " + str(min_chlen2) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)))

								if i2 % 190 == 0:
									print("["+tstr(time() - startTime)+"] @ " + str(i0) + " " + str(i1) + " " + str(i2) + " /" + str(avlenZ))							

								# if avlen2 <= 401 or min_chlen2 == 0:
								# 	with open(found_filename, 'a') as log:
								# 		log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen2) + " | chlen: " + str(min_chlen2) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)) + " @ " + str(i0) + " " + str(i1) + " " + str(i2) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n| " + str(loop2) + "\n\n").replace("⟩", ")").replace("⟨", "("))

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
					# if i1 % 190 == 0:
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
			for k,v in sorted(results2.items()):
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
	
	sorted0 = sorted(results0.items())	
	print("["+tstr(time() - startTime)+"] lvl:0\n| results:\n" + "\n".join(str(pair[0])+": "+str(pair[1]) for pair in sorted0)+"\n| zeroes:\n"+"\n".join([str(e) for e in zeroes0]))
	sorted1 = sorted(results1.items())	
	print("["+tstr(time() - startTime)+"] lvl:1\n| results:\n" + "\n".join(str(pair[0])+": "+str(pair[1]) for pair in sorted1)+"\n| zeroes:\n"+"\n".join([str(e) for e in zeroes1]))

	# results2.clear()
	# with open(results_filename, 'r') as log:
	# 	lines = log.read().splitlines()
	# 	for line in lines:
	# 		if not line.startswith("==="):
	# 			key = tuple(int(x) for x in line.split(" : ")[0][1:-1].split(", "))
	# 			val = int(line.split(" : ")[1])
	# 			results2[key] += val
	# zeroes2count = 0
	# with open(zeroes_filename, 'r') as log:
	# 	lines = log.read().splitlines()
	# 	for line in lines:
	# 		if not line.startswith("==="):		
	# 			zeroes2count += 1
	# 
	# sorted2 = sorted(results2.items())	
	# print("["+tstr(time() - startTime)+"] lvl:2\n| results:\n" + "\n".join(str(pair[0])+": "+str(pair[1]) for pair in sorted2)+"\n| zeroes: "+str(zeroes2count))

