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
			
	startTime = time()
	extend('000001')
	extend('100004')
	extend('100012')
	extend('121014')
	
	min_chlenZ, singlesZ, coercedZ = coerce()
	
	avloops = [l for l in diagram.loops if l.availabled]
	avlen = len(avloops)
	
	diagram.point()
	show(diagram)
	input("[base] avlen: " + str(avlen) + " | min chlen: " + str(min_chlenZ) + "\nsingles: " + str(singlesZ) + "\ncoerced: " + str(coercedZ))
	
#-### ~~~ lvl:0 ~~~ ###
	for i0 in range(0, avlen):
		loop0 = avloops[i0]		
		diagram.extendLoop(loop0)
		min_chlen0, singles0, coerced0 = coerce()
		avlen0 = len([l for l in avloops if l.availabled])

		results0[(
			0 if min_chlen0 == 0 else avlen0, 
			min_chlen0, 
			-(len(singles0)), 
			-(len(coerced0))
		)] += 1
			
		if min_chlen0 == 0:
			zeroes0.append((i0))
			print("[lvl:0] avlen: " + str(avlen0) + " | chlen: " + str(min_chlen0) + " | s: " + str(len(singles0)) + " | c: " + str(len(coerced0)))
		else:
#-----### ~~~ lvl:1 ~~~ ###				
			for i1 in range(i0+1, avlen):
				loop1 = avloops[i1]
				if loop1.availabled:
					diagram.extendLoop(loop1)
					min_chlen1, singles1, coerced1 = coerce()
					avlen1 = len([l for l in avloops if l.availabled])
							
					results1[(
						0 if min_chlen1 == 0 else avlen1, 
						min_chlen1, 
						-(len(singles0)+len(singles1)), 
						-(len(coerced0)+len(coerced1))
					)] += 1

					if min_chlen1 == 0:
						zeroes1.append((i0, i1))
						print("[lvl:1] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)))
					else:
#-----------### ~~~ lvl:2 ~~~ ###										
						for i2 in range(i1+1, avlen): 
							loop2 = avloops[i2]
							if loop2.availabled:
								diagram.extendLoop(loop2)
								min_chlen2, singles2, coerced2 = coerce() 
								avlen2 = len([l for l in avloops if l.availabled])

								results2[(
									0 if min_chlen2 == 0 else avlen2, 
									min_chlen2, 
									-(len(singles0)+len(singles1)+len(singles2)), 
									-(len(coerced0)+len(coerced1)+len(coerced2))
								)] += 1

								if min_chlen2 == 0:
									zeroes1.append((i0, i1, i2))
									print("[lvl:2] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)))
									
								if i2 % 290 == 0:
									print("["+tstr(time() - startTime)+"] @ " + str(i0) + " " + str(i1) + " " + str(i2) + " /" + str(avlen))							

								for l in reversed(singles2):
									diagram.collapseBack(l)		
								for l in coerced2:
									diagram.setLoopAvailabled(l)																	
								diagram.collapseBack(loop2)												
#-----------### ~~~ lvl:2 ~~~ ###																																		
					for l in reversed(singles1):
						diagram.collapseBack(l)		
					for l in coerced1:
						diagram.setLoopAvailabled(l)											
					diagram.collapseBack(loop1)																									
#-----### ~~~ lvl:1 ~~~ ###			
		for l in reversed(singles0):
			diagram.collapseBack(l)						
		for l in coerced0:
			diagram.setLoopAvailabled(l)			
		diagram.collapseBack(loop0)
		
		with open("__587_lvl2_results.txt", 'a') as log:
			total = 0
			for k,v in sorted(results2.items()):
				log.write(str(k) + " : " + str(v) + "\n")
				total += v
			log.write("=== " + str(i0) + ": " + str(total) + " | @ " + tstr(time() - startTime) + "\n")
		results2.clear()		
		with open("__587_lvl2_zeroes.txt", 'a') as log:
			for e in zeroes2:
				log.write(str(e) + " : " + "|".join([str(avloops[i]) for i in e]) + "\n")
			log.write("=== " + str(i0) + ": " + str(len(zeroes2)) + " | @ " + tstr(time() - startTime) + "\n")
		zeroes2.clear
#-### ~~~ lvl:0 ~~~ ###
				
	diagram.point()
	show(diagram)
	
	sorted0 = sorted(results0.items())	
	print("["+tstr(time() - startTime)+"] lvl:0\n| results:\n" + "\n".join(str(pair[0])+": "+str(pair[1]) for pair in sorted0)+"\n| zeroes:\n"+"\n".join([str(e) for e in zeroes0]))
	sorted1 = sorted(results1.items())	
	print("["+tstr(time() - startTime)+"] lvl:1\n| results:\n" + "\n".join(str(pair[0])+": "+str(pair[1]) for pair in sorted1)+"\n| zeroes:\n"+"\n".join([str(e) for e in zeroes1]))
	
	results2.clear()
	with open("__587_lvl2_results.txt", 'r') as log:
		lines = log.read().splitlines()
		for line in lines:
			if not line.startswith("==="):
				key = tuple(int(x) for x in line.split(" : ")[0][1:-1].split(", "))
				val = int(line.split(" : ")[1])
				results2[key] += val
	zeroes2count = 0
	with open("__587_lvl2_zeroes.txt", 'r') as log:
		lines = log.read().splitlines()
		for line in lines:
			if not line.startswith("==="):		
				zeroes2count += 1
				
	sorted2 = sorted(results2.items())	
	print("["+tstr(time() - startTime)+"] lvl:2\n| results:\n" + "\n".join(str(pair[0])+": "+str(pair[1]) for pair in sorted2)+"\n| zeroes: "+str(zeroes2count))

