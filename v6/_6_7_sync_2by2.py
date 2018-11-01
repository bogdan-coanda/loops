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
	# results2 = defaultdict(int)		
	# zeroes2 = []	

	# results_filename = "__lvl1__tobex__lvl2__results.txt"
	zeroes_filename = "__lvl1__tobex__zeroes.txt"
	minim_filename = "__lvl1__tobex__minim.txt"
	maxim_filename = "__lvl1__tobex__maxim.txt"
	sols_filename = "__lvl1__tobex__sols.txt"
	
	# [base] avlen: 636 | min chlen: 5 | tobex count: 120 ratio: 5.3
	startTime = time()
	
	# [base] avlen: 629 | min chlen: 4 | tobex count: 119 ratio: 5.285714285714286
	extend('000001')
	
	# [1m30s.401] avlen: 620 | chlen: 4 | s: 0 | c: 0 | tobex c: 117 r: 5.299145299145299 @ 546 562 /629
	# | (loop:[blue:87]:111206|Ex)
	# | (loop:[green:97]:113023|Ex)
							
	extend('111206')
	extend('113023')
							
	# [1m24s.800] avlen: 612 | chlen: 4 | s: 0 | c: 0 | tobex c: 115 r: 5.321739130434783 @ 519 554 /620
	# | (loop:[yellow:97]:110121|Ex)
	# | (loop:[green:96]:113014|Ex)

	extend('110121')
	extend('113014')

	# [1m34s.326] avlen: 603 | chlen: 4 | s: 0 | c: 0 | tobex c: 113 r: 5.336283185840708 @ 508 524 /612
	# | (loop:[yellow:96]:110031|Ex)
	# | (loop:[blue:83]:110306|Ex)
						
	extend('110031')
	extend('110306')
	
	# [1m26s.239] avlen: 594 | chlen: 3 | s: 0 | c: 0 | tobex c: 111 r: 5.351351351351352 @ 413 473 /603
	# | (loop:[yellow:62]:100220|Ex)
	# | (loop:[blue:72]:102206|Ex)	

	extend('100220')
	extend('102206')
	
	# [1m9s.159] avlen: 586 | chlen: 3 | s: 0 | c: 0 | tobex c: 109 r: 5.376146788990826 @ 388 474 /594
	# | (loop:[green:62]:100023|Ex)
	# | (loop:[orange:89]:102444|Ex)

	extend('100023')
	extend('102444')
			
	# [1m22s.641] avlen: 577 | chlen: 3 | s: 0 | c: 0 | tobex c: 107 r: 5.392523364485982 @ 463 490 /586
	# | (loop:[orange:118]:102321|Ex)
	# | (loop:[yellow:89]:110103|Ex)
	
	extend('102321')
	extend('110103')
	
	# [1m16s.529] avlen: 569 | chlen: 3 | s: 0 | c: 0 | tobex c: 105 r: 5.419047619047619 @ 358 371 /577
	# | (loop:[indigo:115]:023044|Ex)
	# | (loop:[indigo:118]:023403|Ex)

	extend('023044')
	extend('023403')
	
	# [1m22s.979] avlen: 560 | chlen: 3 | s: 0 | c: 0 | tobex c: 103 r: 5.436893203883495 @ 438 556 /569
	# | (loop:[orange:115]:102001|Ex)
	# | (loop:[green:112]:122023|Ex)	

	extend('102001')
	extend('122023')
	
	# [1m21s.728] avlen: 551 | chlen: 3 | s: 0 | c: 0 | tobex c: 101 r: 5.455445544554456 @ 363 427 /560
	# | (loop:[blue:58]:023306|Ex)
	# | (loop:[orange:68]:101251|Ex)
	
	extend('023306')
	extend('101251')
	
	# [1m6s.567] avlen: 543 | chlen: 3 | s: 0 | c: 0 | tobex c: 99 r: 5.484848484848484 @ 294 334 /551
	# | (loop:[yellow:51]:020343|Ex)
	# | (loop:[green:51]:022014|Ex)

	extend('020343')
	extend('022014')
	
	# [1m18s.509] avlen: 535 | chlen: 3 | s: 0 | c: 0 | tobex c: 97 r: 5.515463917525773 @ 391 484 /543
	# | (loop:[orange:94]:100333|Ex)
	# | (loop:[green:94]:112041|Ex)

	extend('100333')
	extend('112041')

	# [0m59s.60] avlen: 527 | chlen: 3 | s: 0 | c: 0 | tobex c: 95 r: 5.5473684210526315 @ 244 369 /535
	# | (loop:[violet:118]:013354|Ex)
	# | (loop:[yellow:77]:100121|Ex)						

	extend('013354')
	extend('100121')

	# [0m52s.924] avlen: 519 | chlen: 3 | s: 0 | c: 0 | tobex c: 93 r: 5.580645161290323 @ 199 408 /527
	# | (loop:[violet:112]:012224|Ex)
	# | (loop:[orange:70]:102010|Ex)

	extend('012224')
	extend('102010')
	
	# [0m53s.306] avlen: 511 | chlen: 3 | s: 0 | c: 0 | tobex c: 91 r: 5.615384615384615 @ 193 288 /519
	# | (loop:[violet:107]:012143|Ex)
	# | (loop:[blue:45]:021006|Ex)

	extend('012143')
	extend('021006')
			
	# [0m33s.117] avlen: 503 | chlen: 3 | s: 0 | c: 0 | tobex c: 89 r: 5.651685393258427 @ 115 198 /511
	# | (loop:[violet:101]:010203|Ex)
	# | (loop:[blue:34]:012406|Ex)
			
	extend('010203')
	extend('012406')
				
	# [0m32s.910] avlen: 495 | chlen: 3 | s: 0 | c: 0 | tobex c: 87 r: 5.689655172413793 @ 108 138 /503
	# | (loop:[red:106]:010133|Ex)
	# | (loop:[blue:24]:010406|Ex)

	extend('010133')
	extend('010406')

	# [1m13s.832] avlen: 486 | chlen: 3 | s: 0 | c: 0 | tobex c: 85 r: 5.7176470588235295 @ 390 478 /495
	# | (loop:[orange:101]:102133|Ex)
	# | (loop:[green:107]:121023|Ex)

	extend('102133')
	extend('121023')

	# [0m44s.238] avlen: 479 | chlen: 3 | s: 0 | c: 0 | tobex c: 83 r: 5.771084337349397 @ 135 344 /486
	# | (loop:[violet:44]:010443|Ex)
	# | (loop:[yellow:70]:100253|Ex)

	extend('010443')
	extend('100253')

	# [0m58s.45] avlen: 471 | chlen: 3 | s: 0 | c: 0 | tobex c: 81 r: 5.814814814814815 @ 231 247 /479
	# | (loop:[green:44]:020041|Ex)
	# | (loop:[yellow:59]:020301|Ex)

	extend('020041')
	extend('020301')

	# [0m56s.226] avlen: 463 | chlen: 3 | s: 0 | c: 0 | tobex c: 79 r: 5.860759493670886 @ 201 298 /471
	# | (loop:[violet:37]:013151|Ex)
	# | (loop:[indigo:113]:023233|Ex)
		
	extend('013151')
	extend('023233')

	# [0m20s.107] avlen: 456 | chlen: 3 | s: 0 | c: 0 | tobex c: 77 r: 5.922077922077922 @ 53 178 /463
	# | (loop:[indigo:73]:002403|Ex)
	# | (loop:[violet:113]:012403|Ex)

	extend('002403')
	extend('012403')
	
	# [1m18s.382] avlen: 448 | chlen: 3 | s: 0 | c: 0 | tobex c: 75 r: 5.973333333333334 @ 143 228 /456
	# | (loop:[blue:27]:011206|Ex)
	# | (loop:[yellow:54]:020202|Ex)

	extend('011206')
	extend('020202')

	# [1m38s.241] avlen: 434 | chlen: 2 | s: 1 | c: 0 | tobex c: 72 r: 6.027777777777778 @ 131 197 /448
	# | (loop:[red:65]:011024|Ex)
	# | (loop:[violet:38]:013330|Ex)

	extend('011024')
	extend('013330')

	# [2m5s.205] avlen: 426 | chlen: 2 | s: 0 | c: 0 | tobex c: 70 r: 6.085714285714285 @ 133 168 /434
	# | (loop:[red:66]:011203|Ex)
	# | (loop:[violet:35]:013010|Ex)

	extend('011203')
	extend('013010')
	
	# [2m16s.484] avlen: 418 | chlen: 2 | s: 0 | c: 0 | tobex c: 68 r: 6.147058823529412 @ 130 150 /426
	# | (loop:[blue:26]:011106|Ex)
	# | (loop:[violet:106]:012053|Ex)

	extend('011106')
	extend('012053')	
	
	# [0m41s.31] avlen: 411 | chlen: 2 | s: 0 | c: 0 | tobex c: 66 r: 6.2272727272727275 @ 22 144 /418
	# | (loop:[red:86]:001052|Ex)
	# | (loop:[green:33]:012032|Ex)	

	extend('001052')
	extend('012032')	
	
	# [2m5s.518] avlen: 403 | chlen: 2 | s: 0 | c: 0 | tobex c: 64 r: 6.296875 @ 51 86 /411
	# | (loop:[indigo:35]:003043|Ex)
	# | (loop:[yellow:33]:010112|Ex)	

	extend('003043')
	extend('010112')	
	
	# [5m4s.897] avlen: 388 | chlen: 2 | s: 1 | c: 0 | tobex c: 61 r: 6.360655737704918 @ 72 99 /403
	# | (loop:[green:23]:010032|Ex)
	# | (loop:[violet:23]:010320|Ex)	

	extend('010032')
	extend('010320')	

	# [5m41s.514] avlen: 380 | chlen: 2 | s: 0 | c: 0 | tobex c: 59 r: 6.440677966101695 @ 160 369 /388
	# | (loop:[blue:40]:020006|Ex)
	# | (loop:[yellow:115]:120352|Ex)

	extend('020006')
	extend('120352')	
	
	# [3m34s.723] avlen: 371 | chlen: 2 | s: 0 | c: 0 | tobex c: 57 r: 6.508771929824562 @ 75 303 /380
	# | (loop:[red:101]:010052|Ex)
	# | (loop:[blue:76]:103106|Ex)	
	
	extend('010052')
	extend('103106')
	
	# [6m21s.565] avlen: 362 | chlen: 2 | s: 0 | c: 0 | tobex c: 55 r: 6.581818181818182 @ 203 233 /371
	# | (loop:[indigo:54]:021452|Ex)
	# | (loop:[green:63]:100032|Ex)			

	extend('021452')
	extend('100032')
	
	# [8m3s.820] avlen: 352 | chlen: 2 | s: 0 | c: 0 | tobex c: 53 r: 6.6415094339622645 @ 296 306 /362
	# | (loop:[green:82]:110023|Ex)
	# | (loop:[yellow:82]:110220|Ex)	

	extend('110023')
	extend('110220')
			
	# [7m5s.357] avlen: 342 | chlen: 3 | s: 0 | c: 0 | tobex c: 51 r: 6.705882352941177 @ 228 239 /352
	# | (loop:[yellow:61]:100130|Ex)
	# | (loop:[yellow:63]:100310|Ex)

	extend('100130')
	extend('100310')
							
	# [3m0s.747] avlen: 333 | chlen: 3 | s: 0 | c: 0 | tobex c: 49 r: 6.795918367346939 @ 84 188 /342
	# | (loop:[red:104]:010411|Ex)
	# | (loop:[indigo:93]:021353|Ex)

	extend('010411')
	extend('021353')

	# [4m29s.192] avlen: 323 | chlen: 3 | s: 0 | c: 0 | tobex c: 47 r: 6.872340425531915 @ 161 166 /333
	# | (loop:[yellow:47]:020334|Ex)
	# | (loop:[indigo:89]:020453|Ex)

	extend('020334')
	extend('020453')
	
	# [2m37s.256] avlen: 312 | chlen: 3 | s: 0 | c: 0 | tobex c: 45 r: 6.933333333333334 @ 125 131 /323
	# | (loop:[violet:56]:013133|Ex)
	# | (loop:[blue:39]:013406|Ex)

	extend('013133')
	extend('013406')
	
	# [1m17s.994] avlen: 302 | chlen: 2 | s: 0 | c: 0 | tobex c: 43 r: 7.023255813953488 @ 90 165 /312
	# | (loop:[red:28]:011320|Ex)
	# | (loop:[indigo:48]:021320|Ex)

	extend('011320')
	extend('021320')
			
	# [1m41s.684] avlen: 289 | chlen: 2 | s: 0 | c: 0 | tobex c: 41 r: 7.048780487804878 @ 196 241 /302
	# | (loop:[yellow:66]:100244|Ex)
	# | (loop:[blue:79]:103406|Ex)

	extend('100244')
	extend('103406')
	
	# [0m34s.290] avlen: 274 | chlen: 2 | s: 0 | c: 2 | tobex c: 39 r: 7.0256410256410255 @ 86 253 /289
	# | (loop:[violet:105]:012002|Ex)
	# | (loop:[blue:91]:112106|Ex)	

	extend('012002')
	extend('112106')
															
	# [0m10s.657] avlen: 263 | chlen: 2 | s: 0 | c: 0 | tobex c: 37 r: 7.108108108108108 @ 15 53 /274
	# | (loop:[red:52]:001303|Ex)
	# | (loop:[red:105]:010043|Ex)

	extend('001303')
	extend('010043')
									
	# [0m8s.828] avlen: 245 | chlen: 2 | s: 0 | c: 0 | tobex c: 35 r: 7.0 @ 54 115 /263
	# | (loop:[red:22]:010151|Ex)
	# | (loop:[indigo:85]:020043|Ex)

	extend('010151')
	# extend('020043')
																																													
	min_chlenZ, singlesZ, coercedZ = coerce()
	
	avloopsZ = [l for l in diagram.loops if l.availabled]
	avlenZ = len(avloopsZ)
	tobex_countZ = diagram.measureTobex()
	tobex_ratioZ = (avlenZ / tobex_countZ) if tobex_countZ is not 0 else 0
			
	min_found_tobex_ratio1 = tobex_ratioZ*2
	max_found_tobex_ratio1 = 0
	
	diagram.point()
	show(diagram)
	print("extended: " + str(len([l for l in diagram.loops if l.extended and not (l.firstNode().address.startswith('00') and l.firstNode().address.endswith('06'))])))
	input("[base] avlen: " + str(avlenZ) + " | min chlen: " + str(min_chlenZ) + " | tobex count: " + str(tobex_countZ) + " ratio: " + str(tobex_ratioZ) + "\nsingles: " + str(singlesZ) + "\ncoerced: " + str(coercedZ))
	
#-### ~~~ lvl:0 ~~~ ###
	for i0 in range(0, avlenZ):
		loop0 = avloopsZ[i0]		
		diagram.extendLoop(loop0)
		min_chlen0, singles0, coerced0 = coerce()
		avlen0 = len([l for l in avloopsZ if l.availabled])
		tobex_count0 = diagram.measureTobex()
		tobex_ratio0 = (avlen0 / tobex_count0) if tobex_count0 != 0 else 0

		results0[(
			avlen0, 
			min_chlen0, 
			-(len(singles0)), 
			-(len(coerced0)),
			tobex_count0,
			tobex_ratio0
		)] += 1
			
		if len(diagram.chains) == 1:
			with open(sols_filename, 'a') as log:
				log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen0) + " | chlen: " + str(min_chlen0) + " | s: " + str(len(singles0)) + " | c: " + str(len(coerced0)) + " | tobex c: " + str(tobex_count0) + " r: " + str(tobex_ratio0) + " @ " + str(i0) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n\n").replace("⟩", ")").replace("⟨", "("))
			show(diagram)
			input(("["+tstr(time() - startTime)+"] avlen: " + str(avlen0) + " | chlen: " + str(min_chlen0) + " | s: " + str(len(singles0)) + " | c: " + str(len(coerced0)) + " | tobex c: " + str(tobex_count0) + " r: " + str(tobex_ratio0) + " @ " + str(i0) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n\n").replace("⟩", ")").replace("⟨", "("))
		
		elif min_chlen0 == 0:
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
					tobex_count1 = diagram.measureTobex()
					tobex_ratio1 = (avlen1 / tobex_count1) if tobex_count1 != 0 else 0
		
					results1[(
						avlen1, 
						min_chlen1,  
						-(len(singles0)+len(singles1)), 
						-(len(coerced0)+len(coerced1)),
						tobex_count1,
						tobex_ratio1
					)] += 1
					
					if i1 % 120 == 0:
						print("["+tstr(time() - startTime)+"] @ " + str(i0) + " " + str(i1) + " /" + str(avlenZ))

					if min_chlen1 != 0 and tobex_ratio1 <= min_found_tobex_ratio1:
						min_found_tobex_ratio1 = tobex_ratio1
						with open(minim_filename, 'a') as log:
							log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)) + " | tobex c: " + str(tobex_count1) + " r: " + str(tobex_ratio1) + " @ " + str(i0) + " " + str(i1) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n\n").replace("⟩", ")").replace("⟨", "("))
							
					if min_chlen1 != 0 and tobex_ratio1 >= max_found_tobex_ratio1:
						max_found_tobex_ratio1 = tobex_ratio1
						with open(maxim_filename, 'a') as log:
							log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)) + " | tobex c: " + str(tobex_count1) + " r: " + str(tobex_ratio1) + " @ " + str(i0) + " " + str(i1) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n\n").replace("⟩", ")").replace("⟨", "("))
							
					if len(diagram.chains) == 1:
						with open(sols_filename, 'a') as log:
							log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)) + " | tobex c: " + str(tobex_count1) + " r: " + str(tobex_ratio1) + " @ " + str(i0) + " " + str(i1) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n\n").replace("⟩", ")").replace("⟨", "("))
						show(diagram)
						input(("["+tstr(time() - startTime)+"] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)) + " | tobex c: " + str(tobex_count1) + " r: " + str(tobex_ratio1) + " @ " + str(i0) + " " + str(i1) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n\n").replace("⟩", ")").replace("⟨", "("))
										
					elif min_chlen1 == 0:
						zeroes1.append((i0, i1))
						print("[lvl:1] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)) + " | tobex c: " + str(tobex_count1) + " r: " + str(tobex_ratio1))
						with open(zeroes_filename, 'a') as log:
							log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)) + " | tobex c: " + str(tobex_count1) + " r: " + str(tobex_ratio1) + " @ " + str(i0) + " " + str(i1) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n\n").replace("⟩", ")").replace("⟨", "("))
#---------### ~~~ lvl:2 ~~~ ###
					# else:
					# 	for i2 in range(i1+1, avlenZ): 
					# 		loop2 = avloopsZ[i2]
					# 		if loop2.availabled:
					# 			diagram.extendLoop(loop2)
					# 			min_chlen2, singles2, coerced2 = coerce() 
					# 			avlen2 = len([l for l in avloopsZ if l.availabled])
					# 			tobex_count2 = diagram.measureTobex()
					# 			tobex_ratio2 = (avlen2 / tobex_count2) if tobex_count2 != 0 else 0
					# 
					# 			results2[(
					# 				avlen2, 
					# 				min_chlen2, 
					# 				-(len(singles0)+len(singles1)+len(singles2)), 
					# 				-(len(coerced0)+len(coerced1)+len(coerced2)),
					# 				tobex_count2,
					# 				tobex_ratio2
					# 			)] += 1
					# 
					# 			if len(diagram.chains) == 1:
					# 				with open(sols_filename, 'a') as log:
					# 					log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen2) + " | chlen: " + str(min_chlen2) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)) + " | tobex c: " + str(tobex_count2) + " r: " + str(tobex_ratio2) + " @ " + str(i0) + " " + str(i1) + " " + str(i2) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n| " + str(loop2) + "\n\n").replace("⟩", ")").replace("⟨", "("))
					# 				show(diagram)
					# 				input(("["+tstr(time() - startTime)+"] avlen: " + str(avlen2) + " | chlen: " + str(min_chlen2) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)) + " | tobex c: " + str(tobex_count2) + " r: " + str(tobex_ratio2) + " @ " + str(i0) + " " + str(i1) + " " + str(i2) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n| " + str(loop2) + "\n\n").replace("⟩", ")").replace("⟨", "("))							
					# 
								#elif min_chlen2 == 0:
								#	zeroes2.append((i0, i1, i2))
								#	print("[lvl:2] avlen: " + str(avlen2) + " | chlen: " + str(min_chlen2) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)) + " | tobex c: " + str(tobex_count2) + " r: " + str(tobex_ratio2))
					# 
					# 			if i2 % 300 == 0:
					# 				print("["+tstr(time() - startTime)+"] @ " + str(i0) + " " + str(i1) + " " + str(i2) + " /" + str(avlenZ))							
					# 
					# 			if min_chlen2 != 0 and tobex_ratio2 <= min_found_tobex_ratio2:
					# 				min_found_tobex_ratio2 = tobex_ratio2
					# 				with open(minim_filename, 'a') as log:
					# 					log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen2) + " | chlen: " + str(min_chlen2) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)) + " | tobex c: " + str(tobex_count2) + " r: " + str(tobex_ratio2) + " @ " + str(i0) + " " + str(i1) + " " + str(i2) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n| " + str(loop2) + "\n\n").replace("⟩", ")").replace("⟨", "("))
					# 
					# 			if min_chlen2 != 0 and tobex_ratio2 >= max_found_tobex_ratio2:
					# 				max_found_tobex_ratio2 = tobex_ratio2
					# 				with open(maxim_filename, 'a') as log:
					# 					log.write(("["+tstr(time() - startTime)+"] avlen: " + str(avlen2) + " | chlen: " + str(min_chlen2) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)) + " | tobex c: " + str(tobex_count2) + " r: " + str(tobex_ratio2) + " @ " + str(i0) + " " + str(i1) + " " + str(i2) + " /" + str(avlenZ) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n| " + str(loop2) + "\n\n").replace("⟩", ")").replace("⟨", "("))
					# 
					# 			for l in reversed(singles2):
					# 				diagram.collapseBack(l)		
					# 			for l in coerced2:
					# 				diagram.setLoopAvailabled(l)
					# 			diagram.collapseBack(loop2)
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
		
		# with open(results_filename, 'a') as log:
		# 	total = 0
		# 	for k,v in sorted(results2.items(), key = lambda pair: (0 if pair[0][1] == 0 else pair[0][-1], pair[0][-1], pair[0][0], pair[0][1])):
		# 		log.write(str(k) + " : " + str(v) + "\n")
		# 		total += v
		# 	log.write("=== " + str(i0) + ": " + str(total) + " | @ " + tstr(time() - startTime) + "\n")
		# results2.clear()		
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

	# results2.clear()
	# with open(results_filename, 'r') as log:
	# 	lines = log.read().splitlines()
	# 	for line in lines:
	# 		if not line.startswith("==="):
	# 			key = tuple(int(x) if '.' not in x else float(x) for x in line.split(" : ")[0][1:-1].split(", "))
	# 			val = int(line.split(" : ")[1])
	# 			results2[key] += val
	# zeroes2count = 0
	# with open(zeroes_filename, 'r') as log:
	# 	lines = log.read().splitlines()
	# 	for line in lines:
	# 		if not line.startswith("==="):		
	# 			zeroes2count += 1
	# 
	# sorted2 = sorted(results2.items(), key = lambda pair: (0 if pair[0][1] == 0 else pair[0][-1], pair[0][-1], pair[0][0], pair[0][1]))
	# print("["+tstr(time() - startTime)+"] lvl:2\n| results:\n" + "\n".join(str(pair[0])+": "+str(pair[1]) for pair in sorted2)+"\n| zeroes: "+str(zeroes2count))

