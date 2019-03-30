from diagram import *
from uicanvas import *


def cOc(segment):
	for i,x in enumerate(segment):
		if x in [' ', '-']:
			pass
		elif x == 'b':
			assert diagram.connectOpenChain('l3b')
		elif x == '+':
			assert diagram.connectOpenChain(4)
		else:
			assert diagram.connectOpenChain(int(x))		
			

if __name__ == "__main__":

	diagram = Diagram(6, kernelPath='222', drawSolCounts=True)
	# cOc('2322 2232 2223 2222')
	# cOc('2322 2232 2223 2222 4222 2322 2232 2223 2222 4222 2322 2232 2223 2222')

	ktype_loops = groupby(diagram.loops, K = lambda l: l.ktype)
	ktype_pairs = defaultdict(list)
	for kt1 in range(0, 5):
		for kt2 in range(kt1+1, 6):
			seen1 = []
			seen2 = []
			for loop1 in sorted([l for l in diagram.loops if l.ktype == kt1], key = lambda l: l.ktype_radialIndex):
				if loop1 not in seen1:
					ls2 = sorted(set([[ncn.loop for ncn in n.cycle.nodes if ncn.ktype == kt2][0] for n in loop1.nodes]), key = lambda l: l.ktype_radialIndex)
					ls1 = sorted(set([[ncn.loop for ncn in n.cycle.nodes if ncn.ktype == kt1][0] for n in ls2[0].nodes]), key = lambda l: l.ktype_radialIndex)
					for l in ls1:
						assert l not in seen1
					for l in ls2:
						assert l not in seen2						
					seen1 += ls1
					seen2 += ls2
					ktype_pairs[(kt1, kt2)].append(ls1)
					ktype_pairs[(kt2, kt1)].append(ls2)
					
	# for kt1 in range(0, 5):
	# 	for kt2 in range(kt1+1, 6):
	# 		for i in range(6):
	# 			print(f"({kt1}, {kt2}) ⇒ {[color_string(l.ktype) + ':' + str(l.ktype_radialIndex) for l in ktype_pairs[(kt1, kt2)][i]]}")				
	# 			print(f"({kt2}, {kt1}) ⇒ {[color_string(l.ktype) + ':' + str(l.ktype_radialIndex) for l in ktype_pairs[(kt2, kt1)][i]]}")								
				
	sol_counts = []
	xxx = 0
	with open('6.Ω.sols.txt', 'r', encoding="utf8") as log:
		for sol, line in enumerate(log):
			if sol % 10000 == 0:
				print(f"@{sol}")
				
			for addr in line.split():
				assert addr == diagram.nodeByAddress[addr].loop.firstAddress()
				diagram.nodeByAddress[addr].loop.sols.append(sol)
				
			loops = set([diagram.nodeByAddress[addr].loop for addr in line.split()])
			counts = defaultdict(int)
			for kt1 in range(0, 5):
				for kt2 in range(kt1+1, 6):
					for i in range(6):
						counts[len(loops.intersection(ktype_pairs[(kt1, kt2)][i]))] += 1
						counts[len(loops.intersection(ktype_pairs[(kt2, kt1)][i]))] += 1
			if counts[4] >= 12: # => 20 sols
			# if counts[4] == 0 and counts[3] == 0 and counts[2] <= 31: # => 4 sols
			#if counts[4] == 0 and counts[3] == 0 and counts[1] <= 61: # => - sols
			# if counts[0] >= 110: # => 4 sols
			# if counts[0] <= 64: # => 12 sols
			# if counts[1] >= 90: # => 4 sols
			# if counts[1] <= 28: # => 8 sols
			# if counts[2] >= 46: # => 4 sols
			# if counts[2] <= 2: # => 4 sols (all with counts[4] == 12)
				print(f"#{xxx}: {line}")
				xxx += 1
				input2(f"#{sol}: {list(counts.items())}")
				
	print("sol counts:")
	print(set(sol_counts.keys()))
	#for c,g in groupby(enumerate(sol_counts), K = lambda sc: sc[1], G = lambda g: len(g)).items():
		#print(f"{c}: {g}")
	print("--- -------")
	sloops = sorted([loop for loop in diagram.loops if loop.available], key = lambda loop: -len(loop.sols))
	for loop in sloops[:10] + sloops[-10:]:
		print(f"{loop}: {len(loop.sols)}")
	
	'''	
	addrs = [
		
		'10042', # sols: 1087888 # ⟨violet:1⟩  # {YV:0}
		'00032', # sols:    8661 # ⟨violet:4⟩  # {YV:0}
		'00342', # sols:    3299 # ⟨violet:7⟩  # {YV:0}
		'02141', # sols:    1644 # ⟨violet:10⟩ # {YV:0}
				
		'11005', # sols:  398406 #   ⟨blue:16⟩ # {BY:4}
		'10105', # sols:  181244 #   ⟨blue:13⟩ # {BY:4}
		'11305', # sols:     223 #   ⟨blue:19⟩ # {BY:4}
		'12205', # sols:     141 #   ⟨blue:22⟩ # {BY:4}
				
		'00100', # sols:   83420 #    ⟨red:1⟩  # {YR:5}
		'01000', # sols:   39709 #    ⟨red:4⟩  # {YR:5}		
		'01301', # sols:     756 #    ⟨red:10⟩ # {YR:5}
		'01310', # sols:     416 #    ⟨red:7⟩  # {YR:5}

		# '01100', # sols:      30 # ⟨orange:5⟩	 # {YO:2}
		# '00002', # sols:       6 # ⟨orange:8⟩	 # {YO:2}
		# '00223', # sols:			 2 # ⟨orange:11⟩ # {YO:2}
		
		# '00205', # sols:			 6 #   ⟨blue:2⟩
		# '00305', # sols:			 4 #   ⟨blue:3⟩				
		# '01205', # sols:			 5 #   ⟨blue:6⟩
		# '02105', # sols:			 5 #   ⟨blue:9⟩		
		# '10005', # sols:   20605 #   ⟨blue:12⟩		
		# '12305', # sols:			10 #   ⟨blue:23⟩
		# 
		# '00233', # sols:      91 # ⟨yellow:5⟩
		# '00242', # sols:      74 # ⟨yellow:8⟩
		# '10210', # sols:			16 # ⟨yellow:14⟩
		# '10003', # sols: 			 1 # ⟨yellow:15⟩
		# '10233', # sols:      21 # ⟨yellow:17⟩				
		# '10012', # sols: 			 1 # ⟨yellow:18⟩
		# '10242', # sols:      44 # ⟨yellow:20⟩		
		# '10021', # sols: 			 1 # ⟨yellow:21⟩		
		# 
		
		

		# '01305', '01205', '01005', '01105', # blue_4, blue_5, blue_6, blue_7
		# '02004', '02104', '02204', '02304', # green_8, green_9, green_10, green_11
		# '11205', '11005', '11105', # blue_16, blue_17, blue_18
		# '12105', '12005', 
		# '12344', '12321', '12312', '12303', # violet_11, violet_19, violet_22, violet_23
		# '10104', '10003', '10130', 
		# '10110', '10330', '10020', # orange_12, orange_13, orange_15
		# '10205', 
		# '02220'
	]

	for addr in addrs:	
		
		node = diagram.nodeByAddress[addr]
		diagram.extendLoop(node.loop)

		for loop in diagram.loops:
			loop.sols = list(set(loop.sols).intersection(node.loop.sols))	
			if len(loop.sols) == 0 and loop.available:
				diagram.setLoopUnavailable(loop)

	max_sol_count = max([len(loop.sols) for loop in diagram.loops if loop.available and len(loop.sols) > 0]) if len(diagram.chains) > 1 else -1
	diagram.pointers = [node for node in diagram.nodes if node.loop.available and len(node.loop.sols) == max_sol_count]
	#'''
									
	show(diagram)
