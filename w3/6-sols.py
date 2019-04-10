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
	#'''			
	sol_counts = []
	xxx = 0
	with open('6.Ω.sols.txt', 'r', encoding="utf8") as log:
		for sol, line in enumerate(log):
			if sol % 10000 == 0:
				print(f"@{sol}")
				
			for addr in line.split():
				assert addr == diagram.nodeByAddress[addr].loop.firstAddress()
				diagram.nodeByAddress[addr].loop.sols.append(sol)#'''
	'''
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
		#[0]# 257701: [(0, 107), (1, 35), (2, 16), (3, 10), (4, 12)]
		
		'01305', #   ⟨blue:7⟩  # 𐄙BG/1𐄙 𐄙BY/1𐄙 𐄙BO/5𐄙 𐄙BR/5𐄙 𐄙BV/2𐄙 # ∘5
		'00241', # ⟨orange:3⟩  # 𐄛OB/2𐄛 𐄙OG/2𐄙 𐄚OY/0𐄚 𐄚OR/2𐄚 𐄚OV/2𐄚 # ∘10
		'01141', # ⟨orange:6⟩  # 𐄙OB/4𐄙 𐄙OG/4𐄙 𐄚OY/0𐄚 𐄙OR/4𐄙 𐄚OV/2𐄚 # ∘7
		'00223', # ⟨orange:11⟩ # 𐄛OB/2𐄛 𐄙OG/0𐄙 𐄙OY/2𐄙 𐄙OR/5𐄙 𐄚OV/5𐄚 # ∘8
		'00100', #    ⟨red:1⟩  # 𐄙RB/1𐄙 𐄙RG/1𐄙 𐄚RY/5𐄚 𐄙RO/1𐄙 𐄚RV/0𐄚 # ∘7
		'01000', #    ⟨red:4⟩  # 𐄛RB/3𐄛 𐄙RG/3𐄙 𐄚RY/5𐄚 𐄚RO/3𐄚 𐄚RV/0𐄚 # ∘10
		'01032', #    ⟨red:8⟩  # 𐄛RB/3𐄛 𐄙RG/5𐄙 𐄙RY/3𐄙 𐄙RO/0𐄙 𐄚RV/3𐄚 # ∘8
		'01023', #    ⟨red:20⟩ # 𐄛RB/3𐄛 𐄙RG/4𐄙 𐄙RY/1𐄙 𐄚RO/3𐄚 𐄚RV/3𐄚 # ∘9
		'00041', # ⟨violet:1⟩  # 𐄙VB/0𐄙 𐄙VG/0𐄙 𐄙VY/0𐄙 𐄙VO/4𐄙 𐄙VR/1𐄙 # ∘5
		'00301', # ⟨violet:6⟩  # 𐄙VB/2𐄙 𐄙VG/2𐄙 𐄙VY/2𐄙 𐄙VO/1𐄙 𐄙VR/4𐄙 # ∘5
		'01004', #  ⟨green:4⟩  # 𐄙GB/1𐄙 𐄚GY/1𐄚 𐄜GO/3𐄜 𐄛GR/3𐄛 𐄚GV/0𐄚 # ∘12

		# '00031', #  ⟨green:3⟩  # 𐄙GB/0𐄙 𐄚GY/0𐄚 𐄛GO/2𐄛 𐄜GR/2𐄜 𐄚GV/2𐄚 # ∘12
		# '00232', # ⟨orange:19⟩ # 𐄛OB/2𐄛 𐄙OG/1𐄙 𐄙OY/4𐄙 𐄚OR/2𐄚 𐄚OV/5𐄚 # ∘9
		
		'00013', #  ⟨green:1⟩  # 𐄙GB/0𐄙 𐄛GY/1𐄛 𐄜GO/1𐄜 𐄛GR/1𐄛 𐄛GV/0𐄛 # ∘14
		'00123', #    ⟨red:17⟩ # 𐄚RB/1𐄚 𐄙RG/2𐄙 𐄚RY/1𐄚 𐄚RO/1𐄚 𐄛RV/3𐄛 # ∘10
						
		'02004', #  ⟨green:8⟩  # 𐄜GB/2𐄜 𐄚GY/2𐄚 𐄛GO/0𐄛 𐄛GR/3𐄛 𐄜GV/3𐄜 # ∘16
		'02013', #  ⟨green:9⟩  # 𐄜GB/2𐄜 𐄚GY/0𐄚 𐄛GO/0𐄛 𐄛GR/4𐄛 𐄜GV/4𐄜 # ∘16
		'02022', #  ⟨green:10⟩ # 𐄜GB/2𐄜 𐄚GY/1𐄚 𐄛GO/1𐄛 𐄛GR/5𐄛 𐄜GV/4𐄜 # ∘16
		'02031', #  ⟨green:11⟩ # 𐄜GB/2𐄜 𐄚GY/2𐄚 𐄛GO/2𐄛 𐄛GR/5𐄛 𐄜GV/5𐄜 # ∘16
		
		'10004', #  ⟨green:12⟩ # 𐄜GB/3𐄜 𐄜GY/3𐄜 𐄜GO/3𐄜 𐄛GR/0𐄛 𐄚GV/0𐄚 # ∘17
		'10013', #  ⟨green:13⟩ # 𐄜GB/3𐄜 𐄜GY/4𐄜 𐄚GO/4𐄚 𐄛GR/0𐄛 𐄚GV/1𐄚 # ∘15
		'10022', #  ⟨green:14⟩ # 𐄜GB/3𐄜 𐄜GY/5𐄜 𐄛GO/5𐄛 𐄚GR/1𐄚 𐄚GV/1𐄚 # ∘15
		'10031', #  ⟨green:15⟩ # 𐄜GB/3𐄜 𐄜GY/3𐄜 𐄛GO/5𐄛 𐄜GR/2𐄜 𐄚GV/2𐄚 # ∘17
		
		'11004', #  ⟨green:16⟩ # 𐄜GB/4𐄜 𐄜GY/4𐄜 𐄛GO/0𐄛 𐄛GR/0𐄛 𐄜GV/3𐄜 # ∘18
		'11013', #  ⟨green:17⟩ # 𐄜GB/4𐄜 𐄜GY/5𐄜 𐄛GO/1𐄛 𐄚GR/1𐄚 𐄜GV/3𐄜 # ∘17
		'11022', #  ⟨green:18⟩ # 𐄜GB/4𐄜 𐄜GY/3𐄜 𐄛GO/1𐄛 𐄜GR/2𐄜 𐄜GV/4𐄜 # ∘19
		'11031', #  ⟨green:19⟩ # 𐄜GB/4𐄜 𐄜GY/4𐄜 𐄛GO/2𐄛 𐄜GR/2𐄜 𐄜GV/5𐄜 # ∘19
		
		'12004', #  ⟨green:20⟩ # 𐄜GB/5𐄜 𐄜GY/5𐄜 𐄜GO/3𐄜 𐄛GR/3𐄛 𐄜GV/3𐄜 # ∘19
		'12013', #  ⟨green:21⟩ # 𐄜GB/5𐄜 𐄜GY/3𐄜 𐄜GO/3𐄜 𐄛GR/4𐄛 𐄜GV/4𐄜 # ∘19
		'12022', #  ⟨green:22⟩ # 𐄜GB/5𐄜 𐄜GY/4𐄜 𐄚GO/4𐄚 𐄛GR/4𐄛 𐄜GV/5𐄜 # ∘17
		'12031', #  ⟨green:23⟩ # 𐄜GB/5𐄜 𐄜GY/5𐄜 𐄛GO/5𐄛 𐄛GR/5𐄛 𐄜GV/5𐄜 # ∘18
	]
	
	'''
'01305', #   ⟨blue:7⟩  # 𐄙BG/1𐄙 𐄙BY/1𐄙 𐄙BO/5𐄙 𐄙BR/5𐄙 𐄙BV/2𐄙 # ∘5
'00241', # ⟨orange:3⟩  # 𐄚OB/2𐄚 𐄙OG/2𐄙 𐄚OY/0𐄚 𐄙OR/2𐄙 𐄚OV/2𐄚 # ∘8  # -2
'01141', # ⟨orange:6⟩  # 𐄙OB/4𐄙 𐄙OG/4𐄙 𐄚OY/0𐄚 𐄙OR/4𐄙 𐄚OV/2𐄚 # ∘7
'00223', # ⟨orange:11⟩ # 𐄚OB/2𐄚 𐄙OG/0𐄙 𐄙OY/2𐄙 𐄙OR/5𐄙 𐄙OV/5𐄙 # ∘6  # -2
'00100', #    ⟨red:1⟩  # 𐄚RB/1𐄚 𐄙RG/1𐄙 𐄚RY/5𐄚 𐄚RO/1𐄚 𐄚RV/0𐄚 # ∘9  # +2
'01000', #    ⟨red:4⟩  # 𐄛RB/3𐄛 𐄙RG/3𐄙 𐄚RY/5𐄚 𐄚RO/3𐄚 𐄚RV/0𐄚 # ∘10
'01032', #    ⟨red:8⟩  # 𐄛RB/3𐄛 𐄙RG/5𐄙 𐄙RY/3𐄙 𐄙RO/0𐄙 𐄛RV/3𐄛 # ∘9  # +2
'01023', #    ⟨red:20⟩ # 𐄛RB/3𐄛 𐄙RG/4𐄙 𐄚RY/1𐄚 𐄚RO/3𐄚 𐄛RV/3𐄛 # ∘11 # +2
'00041', # ⟨violet:1⟩  # 𐄙VB/0𐄙 𐄙VG/0𐄙 𐄙VY/0𐄙 𐄙VO/4𐄙 𐄙VR/1𐄙 # ∘5
'00301', # ⟨violet:6⟩  # 𐄙VB/2𐄙 𐄙VG/2𐄙 𐄙VY/2𐄙 𐄙VO/1𐄙 𐄙VR/4𐄙 # ∘5
'01004', #  ⟨green:4⟩  # 𐄙GB/1𐄙 𐄛GY/1𐄛 𐄜GO/3𐄜 𐄛GR/3𐄛 𐄛GV/0𐄛 # ∘14 # +2

'00013', #  ⟨green:1⟩  # 𐄙GB/0𐄙 𐄛GY/1𐄛 𐄜GO/1𐄜 𐄛GR/1𐄛 𐄛GV/0𐄛 # ∘14 # +2
'00123', #    ⟨red:17⟩ # 𐄚RB/1𐄚 𐄙RG/2𐄙 𐄚RY/1𐄚 𐄚RO/1𐄚 𐄛RV/3𐄛 # ∘10 # +1

'02004', #  ⟨green:8⟩  # 𐄜GB/2𐄜 𐄚GY/2𐄚 𐄛GO/0𐄛 𐄛GR/3𐄛 𐄜GV/3𐄜 # ∘16
'02013', #  ⟨green:9⟩  # 𐄜GB/2𐄜 𐄙GY/0𐄙 𐄛GO/0𐄛 𐄛GR/4𐄛 𐄜GV/4𐄜 # ∘15 # -1
'02022', #  ⟨green:10⟩ # 𐄜GB/2𐄜 𐄛GY/1𐄛 𐄜GO/1𐄜 𐄛GR/5𐄛 𐄜GV/4𐄜 # ∘18 # +2
'02031', #  ⟨green:11⟩ # 𐄜GB/2𐄜 𐄚GY/2𐄚 𐄚GO/2𐄚 𐄛GR/5𐄛 𐄜GV/5𐄜 # ∘15 # -1

'10004', #  ⟨green:12⟩ # 𐄜GB/3𐄜 𐄜GY/3𐄜 𐄜GO/3𐄜 𐄛GR/0𐄛 𐄛GV/0𐄛 # ∘18 # +1
'10013', #  ⟨green:13⟩ # 𐄜GB/3𐄜 𐄜GY/4𐄜 𐄚GO/4𐄚 𐄛GR/0𐄛 𐄚GV/1𐄚 # ∘15
'10022', #  ⟨green:14⟩ # 𐄜GB/3𐄜 𐄜GY/5𐄜 𐄛GO/5𐄛 𐄛GR/1𐄛 𐄚GV/1𐄚 # ∘16 # +1
'10031', #  ⟨green:15⟩ # 𐄜GB/3𐄜 𐄜GY/3𐄜 𐄛GO/5𐄛 𐄛GR/2𐄛 𐄙GV/2𐄙 # ∘15 # -2

'11004', #  ⟨green:16⟩ # 𐄜GB/4𐄜 𐄜GY/4𐄜 𐄛GO/0𐄛 𐄛GR/0𐄛 𐄜GV/3𐄜 # ∘18
'11013', #  ⟨green:17⟩ # 𐄜GB/4𐄜 𐄜GY/5𐄜 𐄜GO/1𐄜 𐄛GR/1𐄛 𐄜GV/3𐄜 # ∘19 # +2
'11022', #  ⟨green:18⟩ # 𐄜GB/4𐄜 𐄜GY/3𐄜 𐄜GO/1𐄜 𐄛GR/2𐄛 𐄜GV/4𐄜 # ∘19 #  0
'11031', #  ⟨green:19⟩ # 𐄜GB/4𐄜 𐄜GY/4𐄜 𐄚GO/2𐄚 𐄛GR/2𐄛 𐄜GV/5𐄜 # ∘17 # -2

'12004', #  ⟨green:20⟩ # 𐄜GB/5𐄜 𐄜GY/5𐄜 𐄜GO/3𐄜 𐄛GR/3𐄛 𐄜GV/3𐄜 # ∘19
'12013', #  ⟨green:21⟩ # 𐄜GB/5𐄜 𐄜GY/3𐄜 𐄜GO/3𐄜 𐄛GR/4𐄛 𐄜GV/4𐄜 # ∘19
'12022', #  ⟨green:22⟩ # 𐄜GB/5𐄜 𐄜GY/4𐄜 𐄚GO/4𐄚 𐄛GR/4𐄛 𐄜GV/5𐄜 # ∘17
'12031', #  ⟨green:23⟩ # 𐄜GB/5𐄜 𐄜GY/5𐄜 𐄛GO/5𐄛 𐄛GR/5𐄛 𐄜GV/5𐄜 # ∘18
	'''	
	
	# 𐄜GB/2𐄜 𐄜GB/3𐄜 𐄜GB/4𐄜 𐄜GB/5𐄜
	# 𐄜GY/3𐄜 𐄜GY/4𐄜 𐄜GY/5𐄜
	# 𐄜GO/3𐄜	
	# 𐄜GR/2𐄜
	# 𐄜GV/3𐄜 𐄜GV/4𐄜 𐄜GV/5𐄜
	
	# 𐄛OB/2𐄛
	# 𐄛RB/3𐄛
	# 𐄛GO/0𐄛 𐄛GO/1𐄛 𐄛GO/2𐄛 𐄛GO/0𐄛
	# 𐄛GR/0𐄛 𐄛GR/3𐄛 𐄛GR/4𐄛 𐄛GR/5𐄛
	
	# 𐄚GY/0𐄚 𐄚GY/1𐄚 𐄚GY/2𐄚
	# 𐄚GO/4𐄚
	# 𐄚GR/1𐄚
	# 𐄚GV/0𐄚 𐄚GV/1𐄚 𐄚GV/2𐄚
	# 𐄚OY/0𐄚
	# 𐄚RY/5𐄚
	# 𐄚OR/2𐄚
	# 𐄚RO/3𐄚
	# 𐄚OV/2𐄚 𐄚OV/5𐄚
	# 𐄚RV/0𐄚 𐄚RV/3𐄚

	# 𐄙GB/0𐄙 𐄙GB/1𐄙
	# 𐄙BG/1𐄙
	# 𐄙BY/1𐄙
	# 𐄙OB/4𐄙
	# 𐄙BO/5𐄙	
	# 𐄙RB/1𐄙
	# 𐄙BR/5𐄙
	# 𐄙VB/0𐄙 𐄙VB/2𐄙
	# 𐄙BV/2𐄙
	# 𐄙OG/0𐄙 𐄙OG/1𐄙 𐄙OG/2𐄙 𐄙OG/4𐄙
	# 𐄙RG/1𐄙 𐄙RG/3𐄙 𐄙RG/4𐄙 𐄙RG/5𐄙
	# 𐄙VG/0𐄙 𐄙VG/2𐄙
	# 𐄙OY/2𐄙 𐄙OY/4𐄙
	# 𐄙RY/1𐄙 𐄙RY/3𐄙
	# 𐄙VY/0𐄙 𐄙VY/2𐄙
	# 𐄙RO/0𐄙 𐄙RO/1𐄙
	# 𐄙OR/4𐄙	𐄙OR/5𐄙
	# 𐄙VO/1𐄙 𐄙VO/4𐄙
	# 𐄙VR/1𐄙 𐄙VR/4𐄙

	qw_table = { 4: '𐄜', 3: '𐄛', 2: '𐄚', 1: '𐄙' }
	loops = [diagram.nodeByAddress[addr].loop for addr in addrs]
	
	for addr in addrs:	
		
		node = diagram.nodeByAddress[addr]
		assert node.loop.firstAddress() == addr
		assert diagram.extendLoop(node.loop)

		for loop in diagram.loops:
			loop.sols = list(set(loop.sols).intersection(node.loop.sols))	
			if len(loop.sols) == 0 and loop.available:
				diagram.setLoopUnavailable(loop)
							
		pairs = []
		for kt1 in range(0, 5):
			for kt2 in range(kt1+1, 6):
				for i in range(6):
					if node.loop in ktype_pairs[(kt1, kt2)][i]:
						pairs.append((kt1, kt2, i, qw_table[len(set(ktype_pairs[(kt1, kt2)][i]).intersection(loops))], len(set(ktype_pairs[(kt1, kt2)][i]).intersection(loops))))
					if node.loop in ktype_pairs[(kt2, kt1)][i]:
						pairs.append((kt2, kt1, i, qw_table[len(set(ktype_pairs[(kt2, kt1)][i]).intersection(loops))], len(set(ktype_pairs[(kt2, kt1)][i]).intersection(loops))))
		print(f"'{addr}', # {'⟨'+color_string(node.loop.ktype):>7}:{str(node.loop.ktype_radialIndex)+'⟩':<3} # {' '.join([p[3]+color_string(p[0])[0].upper()+color_string(p[1])[0].upper()+'/'+str(p[2])+p[3] for p in pairs])} # ∘{sum([p[4] for p in pairs])}")
	
	for q,w in [(4,'𐄜'), (3, '𐄛'), (2, '𐄚'), (1, '𐄙')]:
		for kt1 in range(0, 5):
			for kt2 in range(kt1+1, 6):
				for i in range(6):		
					if len(set(ktype_pairs[(kt1, kt2)][i]).intersection(loops)) == q:
						print(f"{w}{color_string(kt1)[0].upper()}{color_string(kt2)[0].upper()}/{i}{w}")
					if len(set(ktype_pairs[(kt2, kt1)][i]).intersection(loops)) == q:
						print(f"{w}{color_string(kt2)[0].upper()}{color_string(kt1)[0].upper()}/{i}{w}")	
				
	max_sol_count = max([len(loop.sols) for loop in diagram.loops if loop.available and len(loop.sols) > 0]) if len(diagram.chains) > 1 else -1
	diagram.pointers = [node for node in diagram.nodes if node.loop.available and len(node.loop.sols) == max_sol_count]
	#'''
	
	show(diagram)
