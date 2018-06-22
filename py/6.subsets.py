from diagram import *
from uicanvas import *
from itertools import chain
							
	
if __name__ == "__main__":
	
	diagram = Diagram(6)
	diagram.loadExtenders()
	
	'''
	maxcommon_pair = (0, 0)
	maxcommon_count = 0
	seen = set()
	thirds = []
	for i in range(len(diagram.extenders)):
		for j in range(i+1, len(diagram.extenders)):
			common = len(set(diagram.extenders[i]).intersection(diagram.extenders[j]))
			if common >= maxcommon_count:
				maxcommon_count = common
				maxcommon_pair = (i, j)				
				if (maxcommon_count >= 24):
					print("@ " + str(i) + " » " + str(maxcommon_count) + " | " + str(maxcommon_pair))
					if i in seen or j in seen:
						print("» » » third:"+str(len(thirds)))
						thirds.append((i, j))
					seen.add(i)
					seen.add(j)
						
	print(str(maxcommon_count) + " | " + str(maxcommon_pair))
	'''
	thirds = [(830, 30753), (830, 42055), (1526, 1527), (2571, 3931), (2572, 3932), (2577, 3679), (2578, 3680), (2579, 3681), (2580, 3682), (2918, 2919), (2922, 2923), (2924, 2925), (2933, 2934), (2935, 2936), (2938, 2939), (3762, 3763), (3765, 3766), (3767, 3776), (3768, 3774), (4375, 4378), (5978, 5979), (5983, 5984), (5985, 5986), (5997, 32543), (5997, 41393), (6076, 6079), (6077, 6078), (6081, 6083), (6399, 8581), (6400, 8100), (6401, 8101), (6402, 8090), (6403, 8091), (6404, 8574), (7587, 7588), (7797, 8825), (8166, 8203), (8167, 8204), (8175, 8176), (8177, 8178), (9244, 12335), (9275, 33789), (9954, 34383), (11021, 11093), (11022, 11094), (11034, 11035), (11037, 11038), (11341, 35116), (11562, 16670), (11582, 34997), (12342, 12344), (12357, 35613), (14248, 14249), (14256, 14257), (14261, 14291), (14262, 14287), (15104, 36344), (15104, 39263), (15630, 15631), (15786, 34300), (17713, 37472), (17713, 38254), (18779, 18782), (19022, 19023), (19780, 37472), (19780, 38254), (20772, 21398), (20773, 21399), (21001, 21002), (21006, 21007), (22381, 22382), (22384, 22387), (22385, 22386), (22397, 36344), (22397, 39263), (22453, 22457), (22454, 22460), (22455, 22458), (22591, 23848), (22592, 23581), (22593, 23582), (22594, 23572), (22595, 23573), (22596, 23842), (23302, 23303), (23388, 23978), (23625, 23654), (23626, 23655), (23633, 23634), (23635, 23636), (24252, 39829), (24739, 40252), (25500, 25563), (25501, 25564), (25512, 25513), (25515, 25516), (25740, 40599), (25888, 28813), (25907, 40513), (26457, 40981), (26554, 40909), (27644, 32543), (27644, 41393), (28044, 28045), (28163, 40182), (28918, 33919), (29479, 30753), (29479, 42055), (30119, 30122), (30237, 30238), (30753, 42055), (31474, 31909), (31475, 31910), (31608, 31609), (31611, 31612), (32527, 32528), (32530, 32533), (32531, 32532), (32543, 41393), (32581, 32584), (32582, 32586), (32583, 32585), (32679, 33625), (32680, 33437), (32681, 33438), (32682, 33428), (32683, 33429), (32684, 33619), (33471, 33490), (33472, 33491), (33474, 33478), (33475, 33477), (34851, 34899), (34852, 34900), (34858, 34863), (34859, 34861), (35525, 35528), (36344, 39263), (37117, 39910), (37472, 38254), (38671, 38881), (38672, 38882), (38728, 38734), (38729, 38733), (39255, 39256), (39280, 39281), (39343, 39709), (39344, 39702)]
	
	uniq = sorted(set(chain(*thirds)))

	'''	
	seen = set()
	groups = []
	
	# for each unseen id
	for tid in uniq:		
		if tid not in seen:
			
			group = set()
			queue = set([tid])
			seen.add(tid)
			
			while len(queue) is not 0:
				curr = queue.pop()
				group.add(curr)		
				seen.add(curr)
						
				for pair in thirds:
					next = None
					if pair[0] == curr and pair[1] not in seen:
						next = pair[1]
					elif pair[1] == curr and pair[0] not in seen:
						next = pair[0]						
	
					if next is not None:
						queue.add(next)
						seen.add(next)
			
			#print("group: " + str(sorted(group)))
			groups.append(sorted(group))
	for group in groups:
		print(str(group) + ",")					
		
	'''
		
	groups_4 = [
		[830, 29479, 30753, 42055],   # 24 fully common extender loops; no free cycles; missing 4-symmetric 00001		
		[5997, 27644, 32543, 41393],  # 24 fully common extender loops; no free cycles; missing 4-symmetric 00002		
		[15104, 22397, 36344, 39263], # 24 fully common extender loops; no free cycles; missing 4-symmetric 01002		
		[17713, 19780, 37472, 38254]  # 24 fully common extender loops; no free cycles; missing 4-symmetric 01001
	]	
	
	groups_2_0 = [
		[9275, 33789],  # missing cycles: 0; missing 2-symmetric 00011
		[9954, 34383],  # missing cycles: 0; missing 2-symmetric 00011
		[24252, 39829], # missing cycles: 0; missing 2-symmetric 00111
		[24739, 40252], # missing cycles: 0; missing 2-symmetric 00111
				
		[11341, 35116], # missing cycles: 0; missing 2-symmetric 00033				
		[11582, 34997], # missing cycles: 0; missing 2-symmetric 00033
		[12357, 35613], # missing cycles: 0; missing 2-symmetric 00033		
				
		[25740, 40599], # missing cycles: 0; missing 2-symmetric 00133		
		[25907, 40513], # missing cycles: 0; missing 2-symmetric 00133
		[26457, 40981], # missing cycles: 0; missing 2-symmetric 00133
		[26554, 40909]  # missing cycles: 0; missing 2-symmetric 00133		
	]
	
	groups_2_1 = [		
		# 6+6 x5
		[2571, 3931], # missing cycles: 1 | {⟨cycle:22@0102|4⟩}
		[2572, 3932], # missing cycles: 1 | {⟨cycle:22@0102|4⟩}
		[2577, 3679], # missing cycles: 1 | {⟨cycle:22@0102|4⟩}
		[2578, 3680], # missing cycles: 1 | {⟨cycle:22@0102|4⟩}
		[2579, 3681], # missing cycles: 1 | {⟨cycle:22@0102|4⟩}
		[2580, 3682], # missing cycles: 1 | {⟨cycle:22@0102|4⟩}
		[6399, 8581], # missing cycles: 1 | {⟨cycle:22@0102|4⟩}
		[6400, 8100], # missing cycles: 1 | {⟨cycle:22@0102|4⟩}
		[6401, 8101], # missing cycles: 1 | {⟨cycle:22@0102|4⟩}
		[6402, 8090], # missing cycles: 1 | {⟨cycle:22@0102|4⟩}
		[6403, 8091], # missing cycles: 1 | {⟨cycle:22@0102|4⟩}
		[6404, 8574], # missing cycles: 1 | {⟨cycle:22@0102|4⟩}		

		[3767, 3776], # missing cycles: 1 | {⟨cycle:47@0212|4⟩}
		[3768, 3774], # missing cycles: 1 | {⟨cycle:47@0212|4⟩}		
		[14261, 14291], # missing cycles: 1 | {⟨cycle:47@0212|4⟩}
		[14262, 14287], # missing cycles: 1 | {⟨cycle:47@0212|4⟩}
		[33471, 33490], # missing cycles: 1 | {⟨cycle:47@0212|4⟩}
		[33472, 33491], # missing cycles: 1 | {⟨cycle:47@0212|4⟩}	
		[34851, 34899], # missing cycles: 1 | {⟨cycle:47@0212|4⟩}
		[34852, 34900], # missing cycles: 1 | {⟨cycle:47@0212|4⟩}				
		[38671, 38881], # missing cycles: 1 | {⟨cycle:47@0212|4⟩}
		[38672, 38882], # missing cycles: 1 | {⟨cycle:47@0212|4⟩}		
		[39343, 39709], # missing cycles: 1 | {⟨cycle:47@0212|4⟩}
		[39344, 39702], # missing cycles: 1 | {⟨cycle:47@0212|4⟩}		
		
		[3762, 3763], # missing cycles: 1 | {⟨cycle:57@0232|4⟩}
		[3765, 3766], # missing cycles: 1 | {⟨cycle:57@0232|4⟩}
		[14248, 14249], # missing cycles: 1 | {⟨cycle:57@0232|4⟩}
		[14256, 14257], # missing cycles: 1 | {⟨cycle:57@0232|4⟩}
		[33474, 33478], # missing cycles: 1 | {⟨cycle:57@0232|4⟩}
		[33475, 33477], # missing cycles: 1 | {⟨cycle:57@0232|4⟩}		
		[34858, 34863], # missing cycles: 1 | {⟨cycle:57@0232|4⟩}
		[34859, 34861], # missing cycles: 1 | {⟨cycle:57@0232|4⟩}		
		[38728, 38734], # missing cycles: 1 | {⟨cycle:57@0232|4⟩}
		[38729, 38733], # missing cycles: 1 | {⟨cycle:57@0232|4⟩}
		[39255, 39256], # missing cycles: 1 | {⟨cycle:57@0232|4⟩}
		[39280, 39281], # missing cycles: 1 | {⟨cycle:57@0232|4⟩}				

		[8166, 8203], # missing cycles: 1 | {⟨cycle:72@1022|4⟩}
		[8167, 8204], # missing cycles: 1 | {⟨cycle:72@1022|4⟩}
		[11021, 11093], # missing cycles: 1 | {⟨cycle:72@1022|4⟩}
		[11022, 11094], # missing cycles: 1 | {⟨cycle:72@1022|4⟩}		
		[20772, 21398], # missing cycles: 1 | {⟨cycle:72@1022|4⟩}
		[20773, 21399], # missing cycles: 1 | {⟨cycle:72@1022|4⟩}
		[22591, 23848], # missing cycles: 1 | {⟨cycle:72@1022|4⟩}
		[22592, 23581], # missing cycles: 1 | {⟨cycle:72@1022|4⟩}
		[22593, 23582], # missing cycles: 1 | {⟨cycle:72@1022|4⟩}
		[22594, 23572], # missing cycles: 1 | {⟨cycle:72@1022|4⟩}
		[22595, 23573], # missing cycles: 1 | {⟨cycle:72@1022|4⟩}
		[22596, 23842], # missing cycles: 1 | {⟨cycle:72@1022|4⟩}				
														
		[23625, 23654], # missing cycles: 1 | {⟨cycle:97@1132|4⟩}
		[23626, 23655], # missing cycles: 1 | {⟨cycle:97@1132|4⟩}
		[25500, 25563], # missing cycles: 1 | {⟨cycle:97@1132|4⟩}
		[25501, 25564], # missing cycles: 1 | {⟨cycle:97@1132|4⟩}		
		[31474, 31909], # missing cycles: 1 | {⟨cycle:97@1132|4⟩}
		[31475, 31910], # missing cycles: 1 | {⟨cycle:97@1132|4⟩}
		[32679, 33625], # missing cycles: 1 | {⟨cycle:97@1132|4⟩}
		[32680, 33437], # missing cycles: 1 | {⟨cycle:97@1132|4⟩}
		[32681, 33438], # missing cycles: 1 | {⟨cycle:97@1132|4⟩}
		[32682, 33428], # missing cycles: 1 | {⟨cycle:97@1132|4⟩}
		[32683, 33429], # missing cycles: 1 | {⟨cycle:97@1132|4⟩}
		[32684, 33619], # missing cycles: 1 | {⟨cycle:97@1132|4⟩}				
																
		# 6+1 x3								
		[2918, 2919], # missing cycles: 1 | {⟨cycle:24@0104|5⟩}
		[2922, 2923], # missing cycles: 1 | {⟨cycle:24@0104|5⟩}
		[2924, 2925], # missing cycles: 1 | {⟨cycle:24@0104|5⟩}
		[2933, 2934], # missing cycles: 1 | {⟨cycle:24@0104|5⟩}
		[2935, 2936], # missing cycles: 1 | {⟨cycle:24@0104|5⟩}
		[2938, 2939], # missing cycles: 1 | {⟨cycle:24@0104|5⟩}
		[7587, 7588], # missing cycles: 1 | {⟨cycle:24@0104|5⟩}	

		[1526, 1527], # missing cycles: 1 | {⟨cycle:34@0124|5⟩}	
		[5978, 5979], # missing cycles: 1 | {⟨cycle:34@0124|5⟩}
		[5983, 5984], # missing cycles: 1 | {⟨cycle:34@0124|5⟩}
		[5985, 5986], # missing cycles: 1 | {⟨cycle:34@0124|5⟩}
		[6076, 6079], # missing cycles: 1 | {⟨cycle:34@0124|5⟩}
		[6077, 6078], # missing cycles: 1 | {⟨cycle:34@0124|5⟩}
		[6081, 6083], # missing cycles: 1 | {⟨cycle:34@0124|5⟩}

		[8175, 8176], # missing cycles: 1 | {⟨cycle:74@1024|5⟩}
		[8177, 8178], # missing cycles: 1 | {⟨cycle:74@1024|5⟩}
		[11034, 11035], # missing cycles: 1 | {⟨cycle:74@1024|5⟩}
		[11037, 11038], # missing cycles: 1 | {⟨cycle:74@1024|5⟩}	
		[21001, 21002], # missing cycles: 1 | {⟨cycle:74@1024|5⟩}
		[21006, 21007], # missing cycles: 1 | {⟨cycle:74@1024|5⟩}			
		[23302, 23303], # missing cycles: 1 | {⟨cycle:74@1024|5⟩}		
														
		# 6 x3
		[22381, 22382], # missing cycles: 1 | {⟨cycle:62@1002|4⟩}
		[22384, 22387], # missing cycles: 1 | {⟨cycle:62@1002|4⟩}
		[22385, 22386], # missing cycles: 1 | {⟨cycle:62@1002|4⟩}
		[22453, 22457], # missing cycles: 1 | {⟨cycle:62@1002|4⟩}
		[22454, 22460], # missing cycles: 1 | {⟨cycle:62@1002|4⟩}
		[22455, 22458], # missing cycles: 1 | {⟨cycle:62@1002|4⟩}		

		[32527, 32528], # missing cycles: 1 | {⟨cycle:87@1112|4⟩}
		[32530, 32533], # missing cycles: 1 | {⟨cycle:87@1112|4⟩}
		[32531, 32532], # missing cycles: 1 | {⟨cycle:87@1112|4⟩}
		[32581, 32584], # missing cycles: 1 | {⟨cycle:87@1112|4⟩}
		[32582, 32586], # missing cycles: 1 | {⟨cycle:87@1112|4⟩}
		[32583, 32585], # missing cycles: 1 | {⟨cycle:87@1112|4⟩}						
				
		[23633, 23634], # missing cycles: 1 | {⟨cycle:99@1134|5⟩}
		[23635, 23636], # missing cycles: 1 | {⟨cycle:99@1134|5⟩}
		[25512, 25513], # missing cycles: 1 | {⟨cycle:99@1134|5⟩}
		[25515, 25516], # missing cycles: 1 | {⟨cycle:99@1134|5⟩}
		[31608, 31609], # missing cycles: 1 | {⟨cycle:99@1134|5⟩}
		[31611, 31612], # missing cycles: 1 | {⟨cycle:99@1134|5⟩}
		
		# 1 x13				
		[30119, 30122], # missing cycles: 1 | {⟨cycle:27@0112|6⟩}		
		[15630, 15631], # missing cycles: 1 | {⟨cycle:30@0120|5⟩}					
		[23388, 23978], # missing cycles: 1 | {⟨cycle:37@0132|6⟩}		
		[7797, 8825], # missing cycles: 1 | {⟨cycle:42@0202|6⟩}					
		[18779, 18782], # missing cycles: 1 | {⟨cycle:52@0222|6⟩}		
		[30237, 30238], # missing cycles: 1 | {⟨cycle:59@0234|5⟩}			
		[28044, 28045], # missing cycles: 1 | {⟨cycle:60@1000|5⟩}					
		[12342, 12344], # missing cycles: 1 | {⟨cycle:64@1004|5⟩}		
		[11562, 16670], # missing cycles: 1 | {⟨cycle:67@1012|6⟩}				
		[4375, 4378], # missing cycles: 1 | {⟨cycle:77@1032|6⟩}		
		[9244, 12335], # missing cycles: 1 | {⟨cycle:82@1102|6⟩}		
		[19022, 19023], # missing cycles: 1 | {⟨cycle:89@1114|5⟩}
		[25888, 28813], # missing cycles: 1 | {⟨cycle:92@1122|6⟩}	
			
		
	] # len: 112
	
	groups_2_2 = [
		[15786, 34300], # missing cycles: 2		
		[28163, 40182], # missing cycles: 2
		[28918, 33919], # missing cycles: 2		
		[35525, 35528], # missing cycles: 2
		[37117, 39910]  # missing cycles: 2
	]
	
	'''
	for g in groups_4:
		d = Diagram(6)	
		d.generateKernel()
		d.loadExtenders()
		common = set(d.extenders[g[0]]).intersection(d.extenders[g[1]]).intersection(d.extenders[g[2]]).intersection(d.extenders[g[3]])
		for loop in common:
			d.extendLoop(loop)
		show(d)
	#'''
	'''
	diagram.generateKernel()
	for i in range(len(groups2)):
		print("["+str(groups2[i][0])+", "+str(groups2[i][1])+"], # missing cycles: "+str(100-len([
			cycle for cycle in set(chain(*[[
				node.cycle for node in loop.nodes] for loop in set(diagram.extenders[groups2[i][0]]).intersection(diagram.extenders[groups2[i][1]])])) if not cycle.isKernel])))
	#'''
	'''
	diagram.generateKernel()
	for i in range(len(groups_2_1)):
		print("["+str(groups_2_1[i][0])+", "+str(groups_2_1[i][1])+"], # missing cycles: 1 | "+str(set([cycle for cycle in diagram.cycles if not cycle.isKernel]).difference([cycle for cycle in set(chain(*[[node.cycle for node in loop.nodes] for loop in set(diagram.extenders[groups_2_1[i][0]]).intersection(diagram.extenders[groups_2_1[i][1]])])) if not cycle.isKernel])))
	'''
	'''
	for g in groups_2_1:
		d = Diagram(6)
		d.loadExtenders()
		d.generateKernel()	
		for loop in set(d.extenders[g[0]]).intersection(d.extenders[g[1]]):
			d.extendLoop(loop)
		show(d)
		input()
	'''
	'''
	diagram.generateKernel()
	
	def annex():
		avs = [loop for loop in diagram.loops if loop.availabled and len([node for node in loop.nodes if node.chainID is not None]) is not 0]
		ccs = []
		maxcc = 0
		maxav = None
		
		for loop in avs:
			diagram.extendLoop(loop)
			newcc = len([loop for loop in diagram.loops if loop.availabled and len([node for node in loop.nodes if node.chainID is not None]) is not 0])
			ccs.append((newcc, loop))
			if newcc > maxcc:
				maxcc = newcc
				maxav = loop
			diagram.collapseLoop(loop)
			
		print(sorted(groupby(ccs, K = lambda k: k[0], G = lambda g: len(g)).items()))
		return maxcc, maxav, ccs
	
	
	def qp(lvl=0):

		if lvl >=	20:	
			show(diagram)
			loopedCount, chains, avs = diagram.measure()
			input("[lvl: "+str(lvl)+"]")
		else:
			loopedCount, chains, avs = diagram.measure()		
			
		# final end
		if loopedCount == len(diagram.nodes):
			if len(chains) is 1:
				show(diagram)
				input('!!!Found!!!')
				return
			else:
				return
				
		# singles
		if len(diagram.rx_singles) is not 0:
			avs = [list(diagram.rx_singles)[0].availabled_node().loop]
		else:
			maxcc, maxav, ccs = annex()
			avs = [pair[1] for pair in ccs if pair[0] == maxcc]
			
		# filter and sort avs
		# ...
		
		lvl_seen = []		
		cc = 0
		for loop in avs:
			if diagram.extendLoop(loop):
				print("[lvl:"+str(lvl)+"] @ " + str(cc) + "/" + str(len(avs)))				
				
				if len(diagram.rx_unreachables) is 0:	
					qp(lvl+1)
					
				diagram.collapseLoop(loop)
				diagram.forceUnavailable([loop])
				lvl_seen.append(loop)				
			cc += 1
		diagram.forceAvailable(lvl_seen)
	
	qp()								
	'''
	'''
	diagram.generateKernel()
	diagram.extendLoop(diagram.nodeByAddress['00001'].loop)
	diagram.extendLoop(diagram.nodeByAddress['00201'].loop)
	diagram.extendLoop(diagram.nodeByAddress['00143'].loop)
	diagram.extendLoop(diagram.nodeByAddress['00343'].loop)			
	show(diagram)
	diagram.measure()
	#'''
	'''
	diagram.generateKernel()
	diagram.loadExtenders()
	common = set(diagram.extenders[groups_4[0][0]]).intersection(diagram.extenders[groups_4[0][1]]).intersection(diagram.extenders[groups_4[0][2]]).intersection(diagram.extenders[groups_4[0][3]])
	for loop in common:
		diagram.extendLoop(loop)
	show(diagram)
	#'''
	'''
	>>> diagram.nodeByAddress['00001'].loopBrethren  »  22|1 : 24|2 : 23|3 : 20|4
	[⟨node:134502@11002§22|λA⟩, ⟨node:145023@10103§24|λA⟩, ⟨node:150234@10014§23|λA⟩, ⟨node:102345@10000§20|λA⟩]
		
	>>> diagram.nodeByAddress['00143'].loopBrethren
	[⟨node:354120@01044§22|λA⟩, ⟨node:341205@01030§24|λA⟩, ⟨node:312054@01341§23|λA⟩, ⟨node:320541@02242§20|λA⟩]

	>>> diagram.nodeByAddress['00201'].loopBrethren  »  23|3 : 20|4 : 22|1 : 24|2
	[⟨node:314520@01102§23|λA⟩, ⟨node:345201@02003§20|λA⟩, ⟨node:352014@02314§22|λA⟩, ⟨node:320145@02300§24|λA⟩]
		
	>>> diagram.nodeByAddress['00343'].loopBrethren
	[⟨node:154302@11344§23|λA⟩, ⟨node:143025@11330§20|λA⟩, ⟨node:130254@11241§22|λA⟩, ⟨node:102543@10342§24|λA⟩]
	'''
	'''
	marks = [loop for loop in diagram.loops if loop.availabled]
	for loop in common:
		diagram.collapseLoop(loop)
		
	for loop in marks:
		diagram.extendLoop(loop)
	#'''

	diagram.nodeByAddress['00001'].loopBrethren[0].cycle.chainMarker = 1
	diagram.nodeByAddress['00143'].loopBrethren[0].cycle.chainMarker = 1
	diagram.nodeByAddress['00001'].loopBrethren[1].cycle.chainMarker = 2
	diagram.nodeByAddress['00143'].loopBrethren[1].cycle.chainMarker = 2
	diagram.nodeByAddress['00001'].loopBrethren[2].cycle.chainMarker = 3
	diagram.nodeByAddress['00143'].loopBrethren[2].cycle.chainMarker = 3
	diagram.nodeByAddress['00001'].loopBrethren[3].cycle.chainMarker = 4
	diagram.nodeByAddress['00143'].loopBrethren[3].cycle.chainMarker = 4		
					
	diagram.nodeByAddress['00201'].loopBrethren[0].cycle.chainMarker = 3
	diagram.nodeByAddress['00343'].loopBrethren[0].cycle.chainMarker = 3
	diagram.nodeByAddress['00201'].loopBrethren[1].cycle.chainMarker = 4
	diagram.nodeByAddress['00343'].loopBrethren[1].cycle.chainMarker = 4
	diagram.nodeByAddress['00201'].loopBrethren[2].cycle.chainMarker = 1
	diagram.nodeByAddress['00343'].loopBrethren[2].cycle.chainMarker = 1
	diagram.nodeByAddress['00201'].loopBrethren[3].cycle.chainMarker = 2
	diagram.nodeByAddress['00343'].loopBrethren[3].cycle.chainMarker = 2
									
	show(diagram)		

	diagram.generateKernel()
	diagram.forceUnavailable(set(chain(*[[node.loop for node in cycle.nodes if node.loop.availabled] for cycle in diagram.cycles if cycle.isKernel])))	
	diagram.forceUnavailable(set([loop for loop in diagram.loops if loop.availabled and len(set([node.cycle.chainMarker for node in loop.nodes if node.cycle.chainMarker is not None])) > 1]))

	'''
	def mark(loop, marker):
		assert diagram.extendLoop(loop)
		for node in loop.nodes:
			node.cycle.chainMarker = marker
			
	def forward(node, count):
		for _ in range(count):
			node = node.links[1].next
		return node

	def backward(node, count):
		for _ in range(count):
			node = node.prevs[1].node
		return node
	
	
	# green #					
	bro = diagram.nodeByAddress['00001'].loopBrethren[0]
	nxt = forward(bro, 3)
	mark(nxt.loop, bro.cycle.chainMarker)
	mark(backward(nxt.loopBrethren[0], 2).loop, bro.cycle.chainMarker)
	
	# orange #
	bro = diagram.nodeByAddress['00201'].loopBrethren[0]
	nxt = forward(bro, 3)
	mark(nxt.loop, bro.cycle.chainMarker)
	mark(backward(nxt.loopBrethren[0], 2).loop, bro.cycle.chainMarker)

	# yellow #
	bro = diagram.nodeByAddress['00343'].loopBrethren[-1]
	nxt = backward(bro, 3)
	mark(nxt.loop, bro.cycle.chainMarker)
	mark(forward(nxt.loopBrethren[-1], 2).loop, bro.cycle.chainMarker)	
		
	# red #
	bro = diagram.nodeByAddress['00143'].loopBrethren[-1]
	nxt = backward(bro, 3)
	mark(nxt.loop, bro.cycle.chainMarker)
	mark(forward(nxt.loopBrethren[-1], 2).loop, bro.cycle.chainMarker)					
	
					
													
	# yellow #
	bro = diagram.nodeByAddress['00001'].loopBrethren[1]
	nxt = forward(bro, 2)
	mark(nxt.loop, bro.cycle.chainMarker)
	
	# red #
	bro = diagram.nodeByAddress['00201'].loopBrethren[1]
	nxt = forward(bro, 2)
	mark(nxt.loop, bro.cycle.chainMarker)

	# green #
	bro = diagram.nodeByAddress['00343'].loopBrethren[-2]
	nxt = backward(bro, 2)
	mark(nxt.loop, bro.cycle.chainMarker)	
			
	# orange #
	bro = diagram.nodeByAddress['00143'].loopBrethren[-2]
	nxt = backward(bro, 2)
	mark(nxt.loop, bro.cycle.chainMarker)			
	
	
	
	# orange #
	bro = diagram.nodeByAddress['00001'].loopBrethren[2]
	nxt = forward(bro, 3)
	mark(nxt.loop, bro.cycle.chainMarker)	
	
	# green #
	bro = diagram.nodeByAddress['00201'].loopBrethren[2]
	nxt = forward(bro, 3)
	mark(nxt.loop, bro.cycle.chainMarker)
		
	# red #
	bro = diagram.nodeByAddress['00343'].loopBrethren[-3]
	nxt = backward(bro, 3)
	mark(nxt.loop, bro.cycle.chainMarker)
	
	# yellow #
	bro = diagram.nodeByAddress['00143'].loopBrethren[-3]
	nxt = backward(bro, 3)
	mark(nxt.loop, bro.cycle.chainMarker)
		
		
		
	# red #
	bro = diagram.nodeByAddress['00001'].loopBrethren[3]
	nxt = forward(bro, 2)
	mark(nxt.loop, bro.cycle.chainMarker)		
	mark(backward(nxt.loopBrethren[1], 2).loop, bro.cycle.chainMarker)
	
	# yellow #
	bro = diagram.nodeByAddress['00201'].loopBrethren[3]
	nxt = forward(bro, 2)
	mark(nxt.loop, bro.cycle.chainMarker)
	mark(backward(nxt.loopBrethren[1], 2).loop, bro.cycle.chainMarker)
	
	# orange #
	bro = diagram.nodeByAddress['00343'].loopBrethren[-4]
	nxt = backward(bro, 2)
	mark(nxt.loop, bro.cycle.chainMarker)				
	mark(forward(nxt.loopBrethren[-2], 2).loop, bro.cycle.chainMarker)
	
	# green #
	bro = diagram.nodeByAddress['00143'].loopBrethren[0]
	nxt = backward(bro, 2)
	mark(nxt.loop, bro.cycle.chainMarker)
	mark(forward(nxt.loopBrethren[-2], 2).loop, bro.cycle.chainMarker)
	'''
	
	H001 = diagram.nodeByAddress['00001']
	H201 = diagram.nodeByAddress['00201'] 		
	K143 = diagram.nodeByAddress['00143']
	K343 = diagram.nodeByAddress['00343']
	
	bases = [H001, K143, H201, K343]
	nodes = list(bases)
	
	def jmp(bid):
		for i in range(len(nodes)):
			if i % 2 == 0:
				nodes[i] = nodes[i].loopBrethren[bid]
			else:
				nodes[i] = nodes[i].loopBrethren[-1-bid]
		#print("[jmp]", nodes[0])
				
	def adv(cid):
		for i in range(len(nodes)):
			if i % 2 == 0:
				for _ in range(cid):
					nodes[i] = nodes[i].links[1].next
			else:
				for _ in range(cid):
					nodes[i] = nodes[i].prevs[1].node
		#print("[adv]", nodes[0])
					
	def nxt():
		for i in range(len(nodes)):
			if i % 2 == 0:
				nodes[i] = nodes[i].nextLink.next
			else:
				nodes[i] = nodes[i].prevLink.node
		#print("[nxt]", nodes[0])
										
	def extend():
		#print("[ext]", nodes[0])
		for node in nodes:
			assert diagram.extendLoop(node.loop)
			for nln in node.loop.nodes:
				nln.cycle.chainMarker = node.cycle.chainMarker
		
	def chk():	
		#print("[chk]")
		global nodes
		nodes = list(bases)
		chkcc = 0
		for _ in range(diagram.spClass-1):		
			jmp(0)
			if nodes[0].cycle.isKernel:
				continue
			elif nodes[0].chainID is None:
				for _ in range(diagram.spClass):
					adv(1)
					avcc = 0
					for node in nodes:
						if node.loop.availabled:
							avcc += 1
					assert avcc is 0 or avcc is len(nodes)												
					if avcc is not 0:
						chkcc += 1
			else:
				first = nodes[0]
				nxt()
				while nodes[0] != first:
					avcc = 0
					for node in nodes:
						if node.loop.availabled:
							avcc += 1
					assert avcc is 0 or avcc is len(nodes)
					if avcc is not 0:
						chkcc += 1				
					nxt()				
		print("[chk] cc: " + str(chkcc))
						
	chk()
	jmp(0); adv(3); extend()
	chk()
	jmp(0); adv(3); 
	jmp(0); adv(4); extend()									
	chk()
	jmp(1); adv(2); extend()									
	chk()
	
	jmp(2); adv(3); extend()									
	chk()
	jmp(3); adv(2); extend()									
	chk()
			
	nodes = [
		diagram.nodeByAddress['12012'],
		diagram.nodeByAddress['12332'],
		diagram.nodeByAddress['12123'],
		diagram.nodeByAddress['12221'],
	]
		
	extend()
	
	show(diagram)
	diagram.measure()
	#'''
		
