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
			print("[decimate] avloops: " + str(len(avloops)))
			for loop in avloops:
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
				return (zeroes, results)
			print("[decimate] zeroes so far: " + str(len(zeroes)))
				
				
																								
	results0 = defaultdict(int)		
	zeroes0 = []
	results1 = defaultdict(int)		
	zeroes1 = []	
	results2 = defaultdict(int)		
	zeroes2 = []	

	head_filename = '__ff28__'
	results_filename = head_filename + "results"
	zeroes_filename = head_filename + "zeroes"
	minim_filename = head_filename + "minim"
	maxim_filename = head_filename + "maxim"
	sols_filename = head_filename + "sols"
	
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

	# __2____ff6__maxim
	# [55m13s.599] avlen: 503 | chlen: 2 | s: 0 | c: 0 | tobex c: 99 r: 5.08080808080808 | head c: (chain:1612294|215/269) av: 269
	# @ 51/254 134/211 40/86
	# | (loop:[indigo:73]:002403|Ex)
	# | (loop:[yellow:68]:100013|Ex)
	# | (loop:[blue:72]:102206|Ex)

	extend('002403')
	extend('100013')
	extend('102206')
	
	# __2____ff7__maxim
	# [272m53s.465] avlen: 479 | chlen: 2 | s: 0 | c: 0 | tobex c: 96 r: 4.989583333333333 | head c: (chain:5266113|230/274) av: 274
	# @ 155/269 11/120 10/117
	# | (loop:[green:45]:021005|Ex)
	# | (loop:[blue:48]:021306|Ex)
	# | (loop:[blue:49]:021406|Ex)
	
	extend('021005')
	extend('021306')
	extend('021406')
	
	# __2____ff8__maxim
	# [347m58s.339] avlen: 457 | chlen: 2 | s: 0 | c: 0 | tobex c: 93 r: 4.913978494623656 | head c: (chain:5974271|245/282) av: 282
	# @ 148/274 4/131 121/132
	# | (loop:[yellow:57]:020121|Ex)
	# | (loop:[yellow:41]:020130|Ex)
	# | (loop:[yellow:118]:120211|Ex)
	
	extend('020121')
	extend('020130')
	extend('120211')
	
	# __ff9__zeroes__0__
	# [0m6s.42] avlen: 406 | chlen: 0 | s: 3 | c: 9 | tobex c: 89 r: 4.561797752808989 | head c: (chain:206|260/242) av: 242
	# @ 139/282
	# | (loop:[violet:39]:013420|Ex)
	
	unavail('013420')
		
	# __ff10__maxim__0__
	# [0m7s.32] avlen: 448 | chlen: 2 | s: 0 | c: 0 | tobex c: 92 r: 4.869565217391305 | head c: (chain:369|250/283) av: 283
	# @ 246/281
	# | (loop:[yellow:84]:110004|Ex)
	
	extend('110004')
	
	# __ff11__zeroes__0__
	#[0m6s.82] avlen: 412 | chlen: 0 | s: 3 | c: 2 | tobex c: 88 r: 4.681818181818182 | head c: (chain:369|265/259) av: 259
	# @ 233/283
	# | (loop:[orange:118]:102321|Ex)	
	
	unavail('102321')
	
	# __ff12__maxim__0__
	# [0m5s.464] avlen: 439 | chlen: 2 | s: 0 | c: 0 | tobex c: 91 r: 4.824175824175824 | head c: (chain:248|255/278) av: 278
	# @ 147/282
	# | (loop:[yellow:53]:020112|Ex)
	
	extend('020112')
	
	# __ff13__zeroes__0__
	# [0m10s.598] avlen: 235 | chlen: 0 | s: 20 | c: 44 | tobex c: 70 r: 3.357142857142857 | head c: (chain:351|355/150) av: 150
	# @ 187/278
	# | (loop:[indigo:99]:023421|Ex)
			
	unavail('023421')
	
	# __ff14__maxim__0__
	# [0m6s.834] avlen: 430 | chlen: 2 | s: 0 | c: 0 | tobex c: 90 r: 4.777777777777778 | head c: (chain:413|260/272) av: 272
	# @ 240/277
	# | (loop:[yellow:88]:110013|Ex)
	
	extend('110013')
	
	# __ff15__zeroes__0__
	# [0m7s.50] avlen: 277 | chlen: 0 | s: 16 | c: 28 | tobex c: 73 r: 3.7945205479452055 | head c: (chain:236|320/170) av: 170
	# @ 128/272
	# | (loop:[blue:37]:013206|Ex)
	# 
	# [0m7s.170] avlen: 310 | chlen: 0 | s: 10 | c: 17 | tobex c: 79 r: 3.9240506329113924 | head c: (chain:256|320/198) av: 198
	# @ 133/272
	# | (loop:[red:78]:013403|Ex)	
	
	unavail('013206')
	unavail('013403')

	# __ff16__zeroes__0__		
	# [0m6s.32] avlen: 135 | chlen: 0 | s: 37 | c: 45 | tobex c: 52 r: 2.5961538461538463 | head c: (chain:210|430/90) av: 90 @ 100/270
	# | (loop:[green:33]:012032|Ex)
	# 
	# [0m6s.336] avlen: 67 | chlen: 0 | s: 50 | c: 41 | tobex c: 39 r: 1.7179487179487178 | head c: (chain:286|500/46) av: 46 @ 118/270
	# | (loop:[green:37]:013023|Ex)

	unavail('012032')
	unavail('013023')

	# __ff17__zeroes__0__
	# [0m4s.952] avlen: 117 | chlen: 0 | s: 40 | c: 47 | tobex c: 49 r: 2.3877551020408165 | head c: (chain:105|460/76) av: 76 @ 19/268
	# | (loop:[orange:37]:001143|Ex)
	# 
	# [0m6s.789] avlen: 221 | chlen: 0 | s: 22 | c: 20 | tobex c: 67 r: 3.298507462686567 | head c: (chain:480|370/153) av: 153 @ 230/268
	# | (loop:[blue:77]:103206|Ex)			

	unavail('001143')
	unavail('103206')

	# __ff18__zeroes__0__		
	# [0m4s.3] avlen: 155 | chlen: 0 | s: 34 | c: 70 | tobex c: 55 r: 2.8181818181818183 | head c: (chain:110|395/111) av: 111 @ 24/266
	# | (loop:[orange:55]:002001|Ex)
	
	unavail('002001')
	
	# __ff19__maxim__0__	
	# [0m4s.387] avlen: 415 | chlen: 2 | s: 0 | c: 0 | tobex c: 89 r: 4.662921348314606 | head c: (chain:441|265/265) av: 265 @ 220/265
	# | (loop:[orange:88]:102354|Ex)	
	
	extend('102354')

	# __ff20__zeroes__0__				
	# [0m4s.438] avlen: 242 | chlen: 0 | s: 17 | c: 32 | tobex c: 71 r: 3.408450704225352 | head c: (chain:283|355/157) av: 157 @ 128/265
	# | (loop:[violet:59]:013453|Ex)
	# 
	# [0m5s.79] avlen: 306 | chlen: 0 | s: 9 | c: 18 | tobex c: 79 r: 3.8734177215189876 | head c: (chain:416|320/200) av: 200 @ 188/265
	# | (loop:[orange:107]:100201|Ex)
	# 
	# [0m5s.483] avlen: 160 | chlen: 0 | s: 27 | c: 40 | tobex c: 61 r: 2.622950819672131 | head c: (chain:498|400/108) av: 108 @ 222/265
	# | (loop:[orange:104]:102453|Ex)
	# 
	# [0m5s.652] avlen: 380 | chlen: 0 | s: 2 | c: 4 | tobex c: 86 r: 4.4186046511627906 | head c: (chain:529|280/242) av: 242 @ 237/265
	# | (loop:[green:89]:111041|Ex)

	unavail('013453')
	unavail('100201')
	unavail('102453')
	unavail('111041')
	
	# __ff21__zeroes__0__					
	# [0m5s.957] avlen: 236 | chlen: 0 | s: 19 | c: 26 | tobex c: 69 r: 3.420289855072464 | head c: (chain:468|360/154) av: 154 @ 219/261
	# | (loop:[orange:89]:102444|Ex)	

	unavail('102444')

	# __ff22__maxim__0__														
	# [0m4s.928] avlen: 399 | chlen: 2 | s: 1 | c: 0 | tobex c: 87 r: 4.586206896551724 | head c: (chain:483|270/255) av: 255 @ 233/260
	# | (loop:[blue:87]:111206|Ex)

	extend('111206')

	# __ff23__zeroes__0__							
	# [0m6s.891] avlen: 325 | chlen: 0 | s: 8 | c: 15 | tobex c: 78 r: 4.166666666666667 | head c: (chain:78|295/212) av: 212 @ 18/255
	# | (loop:[red:93]:001402|Ex)
	# 
	# [0m7s.739] avlen: 200 | chlen: 0 | s: 24 | c: 33 | tobex c: 62 r: 3.225806451612903 | head c: (chain:241|365/133) av: 133 @ 105/255
	# | (loop:[blue:34]:012406|Ex)
	# 
	# [0m7s.877] avlen: 265 | chlen: 0 | s: 15 | c: 21 | tobex c: 71 r: 3.732394366197183 | head c: (chain:264|335/178) av: 178 @ 107/255
	# | (loop:[violet:34]:012430|Ex)
	# 
	# [0m8s.160] avlen: 85 | chlen: 0 | s: 43 | c: 42 | tobex c: 43 r: 1.9767441860465116 | head c: (chain:327|460/64) av: 64 @ 120/255
	# | (loop:[violet:37]:013151|Ex)
	# 
	# [0m8s.355] avlen: 156 | chlen: 0 | s: 30 | c: 38 | tobex c: 56 r: 2.7857142857142856 | head c: (chain:366|395/114) av: 114 @ 125/255
	# | (loop:[blue:38]:013306|Ex)
	# 
	# [0m8s.798] avlen: 168 | chlen: 0 | s: 27 | c: 43 | tobex c: 59 r: 2.847457627118644 | head c: (chain:477|395/122) av: 122 @ 167/255
	# | (loop:[indigo:111]:023053|Ex)
	# 
	# [0m9s.414] avlen: 172 | chlen: 0 | s: 30 | c: 61 | tobex c: 56 r: 3.0714285714285716 | head c: (chain:597|375/113) av: 113 @ 215/255
	# | (loop:[green:76]:103014|Ex)
	# 
	# [0m9s.650] avlen: 190 | chlen: 0 | s: 26 | c: 40 | tobex c: 60 r: 3.1666666666666665 | head c: (chain:641|370/118) av: 118 @ 222/255
	# | (loop:[green:84]:110041|Ex)

	unavail('001402')
	unavail('012406')		
	unavail('012430')
	unavail('013151')		
	unavail('013306')
	unavail('023053')		
	unavail('103014')
	unavail('110041')		
					
	# __ff24__zeroes__0__												
	# [0m6s.439] avlen: 123 | chlen: 0 | s: 36 | c: 38 | tobex c: 50 r: 2.46 | head c: (chain:150|435/84) av: 84 @ 38/247
	# | (loop:[indigo:30]:003001|Ex)
	# 
	# [0m6s.559] avlen: 336 | chlen: 0 | s: 4 | c: 12 | tobex c: 82 r: 4.097560975609756 | head c: (chain:171|295/212) av: 212 @ 46/247
	# | (loop:[violet:92]:003143|Ex)
	# 
	# [0m7s.563] avlen: 285 | chlen: 0 | s: 11 | c: 17 | tobex c: 75 r: 3.8 | head c: (chain:354|325/191) av: 191 @ 135/247
	# | (loop:[yellow:43]:020310|Ex)
	# 
	# [0m8s.156] avlen: 125 | chlen: 0 | s: 36 | c: 35 | tobex c: 50 r: 2.5 | head c: (chain:469|430/77) av: 77 @ 168/247
	# | (loop:[indigo:118]:023403|Ex)					

	unavail('003001')
	unavail('003143')		
	unavail('020310')
	unavail('023403')		

	# __ff25__zeroes__0__												
	# [0m2s.822] avlen: 273 | chlen: 0 | s: 12 | c: 24 | tobex c: 74 r: 3.689189189189189 | head c: (chain:151|325/170) av: 170 @ 48/243
	# | (loop:[indigo:38]:003402|Ex)

	unavail('003402')

	# __ff26__maxim__0__												
	# [0m4s.126] avlen: 383 | chlen: 2 | s: 0 | c: 0 | tobex c: 86 r: 4.453488372093023 | head c: (chain:287|275/244) av: 244 @ 116/242
	# | (loop:[red:118]:013242|Ex)

	extend('013242')

	# __ff26__maxim__0__												
	# [0m37s.668] avlen: 362 | chlen: 2 | s: 1 | c: 2 | tobex c: 84 r: 4.309523809523809 | head c: (chain:3093|280/230) av: 230
	# @ 211/235
	# | (loop:[green:93]:112032|Ex)

	extend('112032')

	min_chlenZ, singlesZ, coercedZ = coerce()
	
	zeroes, results = decimate()
	input("zeroes: " + str(len(zeroes)) + "\n" + "\n".join([str(l) for l in zeroes]))
	
	sorted_results = sorted(results.items(), key = lambda pair: (0 if pair[1][1] == 0 else pair[1][-1], pair[1][-1], pair[1][0], pair[1][1]))
	input("results: " + str(len(sorted_results)) + "\n" + "\n".join([str(p) for p in sorted_results]))
	
	filtered_results = [p for p in sorted_results if p[0] in diagram.startNode.cycle.chain.avloops]
	input("filtered: " + str(len(filtered_results)) + "\n" + "\n".join([str(p) for p in filtered_results]))
	
	# __ff27__zeroes__0__														
	# [0m12s.485] avlen: 109 | chlen: 0 | s: 36 | c: 40 | tobex c: 49 r: 2.2244897959183674 | head c: (chain:251|450/80) av: 80 @ 86/244
	# | (loop:[red:32]:011311|Ex)
	# 
	# [0m13s.239] avlen: 236 | chlen: 0 | s: 17 | c: 29 | tobex c: 68 r: 3.4705882352941178 | head c: (chain:397|345/163) av: 163 @ 141/244
	# | (loop:[indigo:52]:021311|Ex)
	# 
	# [0m13s.512] avlen: 133 | chlen: 0 | s: 33 | c: 35 | tobex c: 52 r: 2.5576923076923075 | head c: (chain:456|430/86) av: 86 @ 152/244
	# | (loop:[indigo:95]:023011|Ex)
	# 
	# [0m13s.689] avlen: 129 | chlen: 0 | s: 35 | c: 35 | tobex c: 50 r: 2.58 | head c: (chain:500|435/89) av: 89 @ 159/244
	# | (loop:[indigo:112]:023143|Ex)
	# 
	# [0m14s.395] avlen: 227 | chlen: 0 | s: 19 | c: 21 | tobex c: 66 r: 3.4393939393939394 | head c: (chain:632|355/167) av: 167 @ 214/244
	# | (loop:[yellow:95]:110352|Ex)
	# 
	# [0m14s.838] avlen: 82 | chlen: 0 | s: 46 | c: 63 | tobex c: 39 r: 2.1025641025641026 | head c: (chain:714|450/60) av: 60 @ 236/244
	# | (loop:[blue:110]:122006|Ex)
	
	# unavail('011311')
	# unavail('021311')
	# unavail('023011')
	# unavail('023143')
	# unavail('110352')
	# unavail('122006')

	# __ff28__zeroes__0__														
	# [0m3s.439] avlen: 128 | chlen: 0 | s: 34 | c: 21 | tobex c: 51 r: 2.5098039215686274 | head c: (chain:384|440/89) av: 89 @ 141/238
	# | (loop:[indigo:93]:021353|Ex)

	# unavail('021353')

	# __ff29__zeroes__0__														
	# [0m4s.2] avlen: 216 | chlen: 0 | s: 20 | c: 23 | tobex c: 65 r: 3.3230769230769233 | head c: (chain:351|350/142) av: 142 @ 133/237
	# | (loop:[indigo:89]:020453|Ex)
	# 
	# [0m4s.960] avlen: 263 | chlen: 0 | s: 13 | c: 12 | tobex c: 72 r: 3.6527777777777777 | head c: (chain:532|335/166) av: 166 @ 213/237
	# | (loop:[blue:91]:112106|Ex)

	# unavail('020453')
	# unavail('112106')
		
	# min_chlenZ, singlesZ, coercedZ = coerce()
	
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
			with open(minim_filename+"__0__.txt", 'a') as log:
				log.write(log_line0)
												
		if min_chlen0 != 0 and tobex_ratio0 >= max_found_tobex_ratio0:
			max_found_tobex_ratio0 = tobex_ratio0
			with open(maxim_filename+"__0__.txt", 'a') as log:
				log.write(log_line0)
							
		if len(diagram.chains) == 1:
			with open(sols_filename+"__0__.txt", 'a') as log:
				log.write(log_line0)
			show(diagram)
			input("sol! " + log_line0)
		
		elif min_chlen0 == 0:
			zeroes0.append((i0))
			with open(zeroes_filename+"__0__.txt", 'a') as log:
				log.write(log_line0)
#---### ~~~ lvl:1 ~~~ ###				
		# else:
		# 	for i1, loop1 in enumerate(headLoops0):
		# 		if loop1.availabled: # [~] redundant currently
		# 			diagram.extendLoop(loop1)
		# 			min_chlen1, singles1, coerced1 = coerce()
		# 			headChain1 = diagram.startNode.cycle.chain
		# 			headLoops1 = sorted(set(headChain1.avloops).difference(headLoopsZ[:i0+1]).difference(headLoops0[:i1+1]), key = lambda l: l.firstAddress())
		# 			avlen1 = len([l for l in diagram.loops if l.availabled])
		# 			tobex_count1 = diagram.measureTobex()
		# 			tobex_ratio1 = (avlen1 / tobex_count1) if tobex_count1 != 0 else 0
		# 
		# 			results1[(
		# 				avlen1, 
		# 				min_chlen1,  
		# 				len(headChain1.avloops),
		# 				-(len(singles0)+len(singles1)), 
		# 				-(len(coerced0)+len(coerced1)),
		# 				tobex_count1,
		# 				tobex_ratio1
		# 			)] += 1
		# 
					# if i1 % 120 == 0:
					# 	print("["+tstr(time() - startTime)+"] @ " + str(i0) + " " + str(i1) + " /" + str(avlenZ))
		# 
		# 			log_line1 = ("["+tstr(time() - startTime)+"] avlen: " + str(avlen1) + " | chlen: " + str(min_chlen1) + " | s: " + str(len(singles0)+len(singles1)) + " | c: " + str(len(coerced0)+len(coerced1)) + " | tobex c: " + str(tobex_count1) + " r: " + str(tobex_ratio1) + " | head c: " + str(headChain1) + " av: " + str(len(headChain1.avloops)) + " @ " + str(i0) + "/" + str(len(headLoopsZ)) + " " + str(i1) + "/" + str(len(headLoops0)) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n\n").replace("⟩", ")").replace("⟨", "(")
		# 
		# 			if min_chlen1 != 0 and tobex_ratio1 <= min_found_tobex_ratio1:
		# 				min_found_tobex_ratio1 = tobex_ratio1
		# 				with open(minim_filename+"__1__.txt", 'a') as log:
		# 					log.write(log_line1)
		# 
		# 			if min_chlen1 != 0 and tobex_ratio1 >= max_found_tobex_ratio1:
		# 				max_found_tobex_ratio1 = tobex_ratio1
		# 				with open(maxim_filename+"__1__.txt", 'a') as log:
		# 					log.write(log_line1)
		# 
		# 			if len(diagram.chains) == 1:
		# 				with open(sols_filename+"__1__.txt", 'a') as log:
		# 					log.write(log_line1)
		# 				show(diagram)
		# 				input(log_line1)
		# 
		# 			elif min_chlen1 == 0:
		# 				zeroes1.append((i0, i1))
		# 				with open(zeroes_filename+"__1__.txt", 'a') as log:
		# 					log.write(log_line1)
#---------### ~~~ lvl:2 ~~~ ###
					# else:
					# 	for i2, loop2 in enumerate(headLoops1): 
					# 		if loop2.availabled:
					# 			diagram.extendLoop(loop2)
					# 			min_chlen2, singles2, coerced2 = coerce() 
					# 			headChain2 = diagram.startNode.cycle.chain
								#headLoops2 = sorted(set(headChain2.avloops).difference(headLoopsZ[:i0+1]).difference(headLoops0[:i1+1]).difference(headLoops0[:i2+1]), key = lambda l: l.firstAddress())
					# 			avlen2 = len([l for l in diagram.loops if l.availabled])
					# 			tobex_count2 = diagram.measureTobex()
					# 			tobex_ratio2 = (avlen2 / tobex_count2) if tobex_count2 != 0 else 0
					# 
					# 			results2[(
					# 				avlen2, 
					# 				min_chlen2, 
					# 				len(headChain2.avloops),
					# 				-(len(singles0)+len(singles1)+len(singles2)), 
					# 				-(len(coerced0)+len(coerced1)+len(coerced2)),
					# 				tobex_count2,
					# 				tobex_ratio2
					# 			)] += 1
					# 
					# 			if i2 % 20 == 0:
					# 				print("["+tstr(time() - startTime)+"] @ " + str(i0) + " /" + str(len(headLoopsZ)) + " " + str(i1) + " /" + str(len(headLoops0)) + " " + str(i2) + " /" + str(len(headLoops1)))							
					# 
					# 			log_line2 = ("["+tstr(time() - startTime)+"] avlen: " + str(avlen2) + " | chlen: " + str(min_chlen2) + " | s: " + str(len(singles0)+len(singles1)+len(singles2)) + " | c: " + str(len(coerced0)+len(coerced1)+len(coerced2)) + " | tobex c: " + str(tobex_count2) + " r: " + str(tobex_ratio2) + " | head c: " + str(headChain2) + " av: " + str(len(headChain2.avloops)) + " @ " + str(i0) + "/" + str(len(headLoopsZ)) + " " + str(i1) + "/" + str(len(headLoops0)) + " " + str(i2) + "/" + str(len(headLoops1)) + "\n| " + str(loop0) + "\n| " + str(loop1) + "\n| " + str(loop2) + "\n\n").replace("⟩", ")").replace("⟨", "(")
					# 
					# 			if min_chlen2 != 0 and tobex_ratio2 <= min_found_tobex_ratio2:
					# 				min_found_tobex_ratio2 = tobex_ratio2
					# 				with open(minim_filename+"__2__.txt", 'a') as log:
					# 					log.write(log_line2)
					# 
					# 			if min_chlen2 != 0 and tobex_ratio2 >= max_found_tobex_ratio2:
					# 				max_found_tobex_ratio2 = tobex_ratio2
					# 				with open(maxim_filename+"__2__.txt", 'a') as log:
					# 					log.write(log_line2)
					# 
					# 			if len(diagram.chains) == 1:
					# 				with open(sols_filename+"__2__.txt", 'a') as log:
					# 					log.write(log_line2)
					# 				show(diagram)
					# 				input(log_line2)							
					# 
					# 			elif min_chlen2 == 0:
					# 				zeroes2.append((i0, i1, i2))
					# 
					# 			for l in reversed(singles2):
					# 				diagram.collapseBack(l)		
					# 			for l in coerced2:
					# 				diagram.setLoopAvailabled(l)
					# 			diagram.collapseBack(loop2)
#---------### ~~~ lvl:2 ~~~ ###
					# for l in reversed(singles1):
					# 	diagram.collapseBack(l)		
					# for l in coerced1:
					# 	diagram.setLoopAvailabled(l)
					# diagram.collapseBack(loop1)
					# break # [~]
#---### ~~~ lvl:1 ~~~ ###			
		for l in reversed(singles0):
			diagram.collapseBack(l)						
		for l in coerced0:
			diagram.setLoopAvailabled(l)			
		diagram.collapseBack(loop0)
		
		# with open(results_filename+"__2__.txt", 'a') as log:
		# 	total = 0
		# 	for k,v in sorted(results2.items(), key = lambda pair: (0 if pair[0][1] == 0 else pair[0][-1], pair[0][-1], pair[0][0], pair[0][1])):
		# 		log.write(str(k) + " : " + str(v) + "\n")
		# 		total += v
		# 	log.write("=== " + str(i0) + ": " + str(total) + " | @ " + tstr(time() - startTime) + "\n")
		# results2.clear()		
		# with open(zeroes_filename+"__2__.txt", 'a') as log:
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
	# sorted1 = sorted(results1.items(), key = lambda pair: (0 if pair[0][1] == 0 else pair[0][-1], pair[0][-1], pair[0][0], pair[0][1]))	
	# print("["+tstr(time() - startTime)+"] lvl:1\n| results:\n" + "\n".join(str(pair[0])+": "+str(pair[1]) for pair in sorted1)+"\n| zeroes:\n"+"\n".join([str(e) for e in zeroes1]))
	# 
	# results2.clear()
	# with open(results_filename+"__2__.txt", 'r') as log:
	# 	lines = log.read().splitlines()
	# 	for line in lines:
	# 		if not line.startswith("==="):
	# 			key = tuple(int(x) if '.' not in x else float(x) for x in line.split(" : ")[0][1:-1].split(", "))
	# 			val = int(line.split(" : ")[1])
	# 			results2[key] += val
	# zeroes2count = len(zeroes2)
	# with open(zeroes_filename+"__2__.txt", 'r') as log:
	# 	lines = log.read().splitlines()
	# 	for line in lines:
	# 		if not line.startswith("==="):		
	# 			zeroes2count += 1
	# 
	# sorted2 = sorted(results2.items(), key = lambda pair: (0 if pair[0][1] == 0 else pair[0][-1], pair[0][-1], pair[0][0], pair[0][1]))
	# print("["+tstr(time() - startTime)+"] lvl:2\n| results:\n" + "\n".join(str(pair[0])+": "+str(pair[1]) for pair in sorted2)+"\n| zeroes: "+str(zeroes2count))

