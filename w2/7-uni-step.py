from diagram import *
from uicanvas import *
from mx import *
from time import time
from collections import defaultdict
from functools import reduce

'''
[  34][lvl:29] off: -3 §[ 0»809085][ 31m21s.686][lvl:56][ch:291|av:242] 0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0².0².0².0².0².0².0².0².0².0².0².0².0².0².0².0³.0².0³.0².1².0³.2³.0².1².1².1².1².0².1².1².1².1².0².1².0².0¹.1².0².0².1².1².1².1².0².0².0²
[  34][lvl:29] off: -3 §[ 0»809085][ 31m21s.686][lvl:56][purge] ⇒ killed: 8 | ⇒ min chlen: 1
[show] chains: 131 (111/20) | connected cycles: 609 | links: ℓ₁x3585 ℓ₂x651 ℓ₃x26 ℓ₄x0 | total: 4832 | final: 5905.0
[  34][lvl:29] off: -3 §[ 0»809188][ 31m22s.266][lvl:88] new min step chains: 131  |  » ∘ «

[  34][lvl:29] off: -3 §[ 0»3455478][ 147m16s.41][lvl:70][ch:221|av:148] 0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0².0².0².0².0².0².0².0².0².0².0².0².0².0².0².0³.0².0³.1².0².0³.1².0².1².0².1².1².1².1².0².0².0¹.1².0².0².0².1².0¹.0².0¹.0².0².1².1².1².1².1².1².1².1².0².1².0².0².1².0¹.0¹.0².1².1²
[  34][lvl:29] off: -3 §[ 0»3455478][ 147m16s.41][lvl:70][purge] ⇒ killed: 17 | ⇒ min chlen: 1
[show] chains: 126 (110/16) | connected cycles: 610 | links: ℓ₁x3586 ℓ₂x657 ℓ₃x26 ℓ₄x0 | total: 4873 | final: 5905.0
[  34][lvl:29] off: -3 §[ 0»3455497][147m16s.661][lvl:89] new min step chains: 126  |  » ∘ «

[show] chains: 121 (107/14) | connected cycles: 613 | links: ℓ₁x3601 ℓ₂x663 ℓ₃x26 ℓ₄x0 | total: 4914 | final: 5905.0
[  34][lvl:29] off: -3 §[ 0»3455498][258m28s.996][lvl:90] new min step chains: 121  |  » ∘ «

[show] chains: 116 (102/14) | connected cycles: 618 | links: ℓ₁x3630 ℓ₂x669 ℓ₃x26 ℓ₄x0 | total: 4955 | final: 5905.0
[  34][lvl:29] off: -3 §[ 0»3455499][259m15s.805][lvl:91] new min step chains: 116  |  » ∘ «

[show] chains: 111 (97/14) | connected cycles: 623 | links: ℓ₁x3659 ℓ₂x675 ℓ₃x26 ℓ₄x0 | total: 4996 | final: 5905.0
[  34][lvl:29] off: -3 §[ 0»3455500][259m52s.567][lvl:92] new min step chains: 111  |  » ∘ «
'''


step_cc = -1
step_id = -1
min_step_chains_reached = 126
sols_cc = 0


def step(pre_key, step_lvl=0, step_path=[]):
	global step_cc, step_id, min_step_chains_reached, sols_cc
	if step_lvl == 0:
		step_cc += 1
	step_id += 1
	
	def key():
		return f"{pre_key}[{step_cc:>2}»{step_id:>4}][{tstr(time() - startTime):>11}][lvl:{step_lvl}]"
			
	if step_id % 1000 == 0:
		print(f"{key()}[ch:{len(diagram.chains)}|av:{len([l for l in diagram.loops if l.available])}] {'.'.join([(str(x)+upper(t)) for x,t,_ in step_path])}")
	
	if len(diagram.chains) == 1:
		
		with open('6.Ω.sols.txt', 'a', encoding="utf8") as log:
			log.write(' '.join([addr for _,_,addr in step_path]) + "\n")
		with open('6.Ω.path.txt', 'a', encoding="utf8") as log:
			log.write('.'.join([(str(x)+upper(t)) for x,t,_ in step_path]) + "\n")
		
		show(diagram)								
		input2(f"{key()} #{sols_cc} sol found.")
		sols_cc += 1
		return
				
	if len(diagram.chains) < min_step_chains_reached:
		min_step_chains_reached = len(diagram.chains)
		diagram.point()		
		show(diagram)
		input2(f"{key()} new min step chains: {min_step_chains_reached}")
				
	# unloops/chloops
	seen = []

	# --- --- --- #
	'''
	#looped = 0
	
	#curr_len = len([l for l in diagram.loops if l.available])
	#min_avcount = min([ch.avcount for ch in diagram.chains])
	
	#if min_avcount > 1:
		#km = diagram.buildKillingMap()
		
		# sk = sorted(km.items(), key = lambda p: (-p[1], p[0]))
		# for i in list(range(0, 1)) + list(range(len(sk)-1, len(sk))):
		# 	print(f"#{i}: {sk[i][1]} ⇒ {curr_len-sk[i][1]} | {color_string(sk[i][0].ktype)+':'+str(sk[i][0].ktype_radialIndex)}")
		# print(f"[km] tested {len(sk)} loops.")
		
		# minmax_per_chain = []
		# for ch in diagram.chains:
		# 	if ch.avcount == 2:
		# 		chloops = ch.avloops()
		# 		if km[chloops[0]] > km[chloops[1]]:
		# 			minmax_per_chain.append((curr_len-km[chloops[0]], curr_len-km[chloops[1]], (chloops[0], chloops[1]), ch))
		# 		else:	
		# 			minmax_per_chain.append((curr_len-km[chloops[1]], curr_len-km[chloops[0]], (chloops[1], chloops[0]), ch))
		# 
		# smm = sorted(minmax_per_chain, key = lambda p: p[:3])
		# for i in range(len(smm)) if len(smm) < 2 else list(range(0, 1)) + list(range(len(smm)-1, len(smm))):
		# 	print(f"#{i} | min: {smm[i][0]} | max: {smm[i][1]} | {smm[i][3]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in smm[i][2]]}")
		# print(f"[km] tested {len(smm)} 2-avloop chains.")		
		
		# median_per_chain = []
		# for ch in diagram.chains:
		# 	median_per_chain.append((sum([curr_len-km[l] for l in ch.avloops()]) / ch.avcount, ch.avcount, ch))
		# smed = sorted(median_per_chain, key = lambda p: p[:-1])
		
		min_median = None
		min_chsmed = None
		for ch in diagram.chains:
			median = sum([curr_len-km[l] for l in ch.avloops()]) / ch.avcount
			if min_median == None or median < min_median or (median == min_median and (ch.avcount < min_chsmed.avcount or (ch.avcount == min_chsmed.avcount and ch.id < min_chsmed.id))):
				min_median = median
				min_chsmed = ch
		
		
		# for i in range(len(smed)) if len(smed) < 2 else list(range(0, 1)) + list(range(len(smed)-1, len(smed))):
		# 	print(f"#{i} | median: {smed[i][0]:.2f} | avcount: {smed[i][1]} | {smed[i][2]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex)+'`#`'+str(curr_len-km[l]) for l in smed[i][2].avloops()]}")
		# print(f"[km] tested {len(smed)} chains.")		
	'''			
	'''															
		looped += 1

		avlen_per_loop = []				
		avlen_per_pair = []
		avlen_per_trio = []
		dead_children_per_loop = defaultdict(int)
						
		killedSomething = False
					
		for il, loop1 in enumerate(diagram.loops):
			if loop1.available:
				print(f"[{looped}][{tstr(time() - startTime):>11}] il: {il}")
				assert diagram.extendLoop(loop1)
				
				avlen = len([l for l in diagram.loops if l.available])				
				min_chlen = min([ch.avcount for ch in diagram.chains])

				diagram.collapseBack(loop1)
													
				if min_chlen == 0:
					diagram.setLoopUnavailable(loop1)
					seen.append(loop1)
					if min([n.cycle.chain.avcount for n in loop1.nodes]) == 0:
						break
					else:
						killedSomething = True
						
				else:
					avlen_per_loop.append([avlen, min_chlen, [loop1]])
	
					assert diagram.extendLoop(loop1)
					for jl, loop2 in enumerate(diagram.loops):
						if jl > il and loop2.available:
							assert diagram.extendLoop(loop2)
							
							avlen = len([l for l in diagram.loops if l.available])
							min_chlen = min([ch.avcount for ch in diagram.chains])
							
							if min_chlen == 0:
								dead_children_per_loop[loop1] += 1
							else:
								avlen_per_pair.append([avlen, min_chlen, [loop1, loop2]])


								for kl, loop3 in enumerate(diagram.loops):
									if kl > jl and loop3.available:
										assert diagram.extendLoop(loop3)
										
										avlen = len([l for l in diagram.loops if l.available])
										min_chlen = min([ch.avcount for ch in diagram.chains])
										
										if min_chlen != 0:
											avlen_per_trio.append([avlen, min_chlen, [loop1, loop2, loop3]])
											
										diagram.collapseBack(loop3)
															
																								
							diagram.collapseBack(loop2)
					diagram.collapseBack(loop1)			
				
		if not killedSomething:
			break

									
	if looped > 0:
		print(f"{key()}[ch:{len(diagram.chains)}|av:{len([l for l in diagram.loops if l.available])}] {'.'.join([(str(x)+upper(t)) for x,t,_ in step_path])}")		
		print(f"{key()}[purge] ⇒ killed: {len(seen)} | ⇒ min chlen: {min([ch.avcount for ch in diagram.chains])}")
				
		print('--- loops ---')		
		savl = sorted(avlen_per_loop)				
		for i in range(0, 14):
			print(f"#{i}: {savl[i][0]} | {savl[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in savl[i][2]]}")
		for i in range(len(savl)-14, len(savl)):
			print(f"#{i}: {savl[i][0]} | {savl[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in savl[i][2]]}")
		print(f"[loops] tested {len(savl)} loops.")			

		print('--- pairs ---')		
		savp = sorted(avlen_per_pair)		
		for i in range(0, 14):
			print(f"#{i}: {savp[i][0]} | {savp[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in savp[i][2]]}")
		for i in range(len(savp)-14, len(savp)):
			print(f"#{i}: {savp[i][0]} | {savp[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in savp[i][2]]}")
		print(f"[pairs] tested {len(savp)} pairs.")			

		print('--- trios ---')		
		savt = sorted(avlen_per_trio)		
		for i in range(0, 14):
			print(f"#{i}: {savt[i][0]} | {savt[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in savt[i][2]]}")
		for i in range(len(savt)-14, len(savt)):
			print(f"#{i}: {savt[i][0]} | {savt[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in savt[i][2]]}")
		print(f"[pairs] tested {len(savt)} trios.")			
												
		print('∘∘∘ deaths ∘∘∘')
		savd = sorted(dead_children_per_loop.items(), key = lambda dc: (-dc[1], dc[0]))
		for i in range(0, 14):
			print(f"#{i}: {savd[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in [savd[i][0]]]}")
		for i in range(len(savd)-14, len(savd)):
			print(f"#{i}: {savd[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in [savd[i][0]]]}")					
		print(f"[deaths] found {len(savd)} killer loops.")
		print('∘∘∘ ∘∘∘∘∘∘ ∘∘∘')
								
		prime_killer_loop = savd[0][0]
		print('--- prime killer loop ---')
		for i in range(0, len(savl)):
			if prime_killer_loop in savl[i][2]:			
				print(f"#{i}: {savl[i][0]} | {savl[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in savl[i][2]]}")
				break
		print('--- prime killer pairs ---')		
		savp_pkl_cc = 0
		for i in range(0, len(savp)):
			if prime_killer_loop in savp[i][2]:						
				print(f"#{i}: {savp[i][0]} | {savp[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in savp[i][2]]}")
				savp_pkl_cc += 1
				if savp_pkl_cc >= 7:
					break
		print('--- prime killer trios ---')		
		savt_pkl_cc = 0
		for i in range(0, len(savt)):
			if prime_killer_loop in savt[i][2]:						
				print(f"#{i}: {savt[i][0]} | {savt[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in savt[i][2]]}")
				savt_pkl_cc += 1
				if savt_pkl_cc >= 7:
					break					
		print('--- prime killer cycles/chains ---')
		for n in prime_killer_loop.nodes:
			print(f"{n.cycle} | {n.cycle.chain}")

		prime_pair = savp[0][2]
		print('--- prime pair loops ---')
		for i in range(0, len(savl)):
			if prime_pair[0] in savl[i][2] or prime_pair[1] in savl[i][2]:			
				print(f"#{i}: {savl[i][0]} | {savl[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in savl[i][2]]}")
		print('--- prime pair pairs ---')		
		savp_pkl_cc = 0
		for i in range(0, len(savp)):
			if prime_pair[0] in savp[i][2] or prime_pair[1] in savp[i][2]:			
				print(f"#{i}: {savp[i][0]} | {savp[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in savp[i][2]]}")
				savp_pkl_cc += 1
				if savp_pkl_cc >= 7:
					break				
		print('--- prime pair trios ---')		
		savt_pkl_cc = 0
		for i in range(0, len(savt)):
			if prime_pair[0] in savt[i][2] or prime_pair[1] in savt[i][2]:			
				print(f"#{i}: {savt[i][0]} | {savt[i][1]} | {[color_string(l.ktype)+':'+str(l.ktype_radialIndex) for l in savt[i][2]]}")
				savt_pkl_cc += 1
				if savt_pkl_cc >= 7:
					break									
		print('--- prime pair cycles/chains ---')
		for n in prime_pair[0].nodes:
			print(f"#[0] | {n.cycle} | {n.cycle.chain}")
		for n in prime_pair[1].nodes:
			print(f"#[1] | {n.cycle} | {n.cycle.chain}")
								
		input2('--- ----- ---- ------/------ ---')		

	'''
		
	#[±] for each 2-avloop chain get the two avlen_per_loop values into a (min, max) pair per chain ⇒ sort by (min,max,…)
	#[±] construct a global killingField map … by cummulating pairs of loops intersecting in pairs of cycles ? ⇒ need thorough asserts by avlen_per_loop table
		
	
								
	# ∘∘∘ ∘∘∘ ∘∘∘ #

	min_chain = None
	for ch in diagram.chains:
		if min_chain == None or ch.avcount < min_chain.avcount or (ch.avcount == min_chain.avcount and ch.id < min_chain.id):
			min_chain = ch
	
	if min_chain.avcount > 1: # or step_lvl % 4 == 0: 
	
		purged = -1
		singled = False
		
		while True:
				
			km = diagram.buildKillingMap()
			
			# ---  common  --- #
	
			hasCommonKills = False
			for ic, ch in enumerate(diagram.chains):
				commonKills = None # reduce(set.intersection, [km[loop] for loop in ch.avloops()])
				for loop in ch.avloops():
					if commonKills == None:
						commonKills = set(km[loop])
					else:
						commonKills.intersection_update(km[loop])
						if len(commonKills) == 0:
							break
				if commonKills is not None and len(commonKills) > 0:
					for loop in commonKills:
						if loop.available:
							diagram.setLoopUnavailable(loop)
							seen.append(loop)					
							hasCommonKills = True
					# print(f"{key()}[common:{ic}] found {len(commonKills)} common kills in {ch}\ncommon kills:\n" + '\n'.join([str(l) for l in commonKills]) + "\nby chain loops:\n" + '\n'.join([str(l) for l in ch.avloops()]))

			if hasCommonKills:		
				
				min_chlen = min([ch.avcount for ch in diagram.chains])
				if min_chlen == 0:
					# print(f"cleansed … and dying")
					for l in reversed(seen):
						diagram.resetLoopAvailable(l)					
					return
				elif min_chlen == 1:
					# print(f"{key()} cleansed to single")
					break					
								
			# ---  purge  --- #
			
			purged = 0	
			singles_per_loop = defaultdict(set)
			
			for loop in diagram.loops:
				if loop.available:
	
					diagram.extendLoop(loop)
					min_chlen = min([ch.avcount for ch in diagram.chains])
					chain_count = len(diagram.chains)
					future_singles = set([ch.avloops()[0] for ch in diagram.chains if ch.avcount == 1])
					if len(future_singles) > 0:
						singles_per_loop[loop] = future_singles
					diagram.collapseBack(loop)
	
					if min_chlen == 0 and chain_count > 1:
						diagram.setLoopUnavailable(loop)
						seen.append(loop)
						purged += 1
	
			if purged > 0:
				# print(f"{key()} purged {len(seen)} loops")
				min_chlen = min([ch.avcount for ch in diagram.chains])
				if min_chlen == 0:
					# print(f"purged … and dying")
					for l in reversed(seen):
						diagram.resetLoopAvailable(l)					
					return
				elif min_chlen == 1:				
					# print(f"{key()} purged to single")
					break
			else:
				min_chlen = min([ch.avcount for ch in diagram.chains])
				break				
		
		# --- ----- --- #		

		if min_chlen == 1:
			min_chain = None
			for ch in diagram.chains:
				if ch.avcount == 1 and (min_chain == None or ch.id < min_chain.id):
					min_chain = ch
										
		else:
			
			# if len(singles_per_loop) > 0:
			# 	print(f"{key()}[singles] found {len(singles_per_loop)} loops with {sum([len(x) for x in singles_per_loop.values()])} future singles")
			
			if len(seen) > 0:
				km = diagram.buildKillingMap()
			'''
			maq_killed = None
			maq_has_singles = None	
			maq_sum_singles = None
			
			maz_killed = None
			maz_has_singles = None	
			maz_sum_singles = None

			maα_killed = None
			maα_has_singles = None	
			maα_sum_singles = None
			'''										
			max_killed = None
			max_has_singles = None	
			max_sum_singles = None
			min_loops = None
			
			# print(f"{key()} singling & averaging")
			
			for ic, ch in enumerate(diagram.chains):
				# print(f"#{ic}: {ch}")
				
				common_singles = None # reduce(set.intersection, [singles_per_loop[loop] for loop in ch.avloops()])
				for il,loop in enumerate(ch.avloops()):
					# print(f"#{ic} / {il} | singles: {len(singles_per_loop[loop])} | kills: {len(km[loop])}")
					if common_singles == None:
						common_singles = set(singles_per_loop[loop])
					else:
						common_singles.intersection_update(singles_per_loop[loop])
						if len(common_singles) == 0:
							break				
				if len(common_singles) > 0:
					# print(f"{key()}[singles] found {ch} with {len(common_singles)} common singles")
					min_loops = [list(common_singles)[0]]
					singled = True
					break
									
				chavloops = ch.avloops()
				
				avg_killed = sum([len(km[l]) for l in chavloops]) / ch.avcount
										
				# if max_killed == None or (len(ch.cycles) <= len(min_chain.cycles) and (avg_killed > max_killed or (avg_killed == max_killed and (ch.avcount < min_chain.avcount or (ch.avcount == min_chain.avcount and ch.id < min_chain.id))))):
				# if max_killed == None or ch.avcount < min_chain.avcount or (ch.avcount == min_chain.avcount and (len(ch.cycles) <= len(min_chain.cycles) and (avg_killed > max_killed or (avg_killed == max_killed and (ch.avcount < min_chain.avcount or (ch.avcount == min_chain.avcount and ch.id < min_chain.id)))))):
				# if max_killed == None or (avg_killed > max_killed or (avg_killed == max_killed and (ch.avcount < min_chain.avcount or (ch.avcount == min_chain.avcount and ch.id < min_chain.id)))):
					
				avg_has_singles = sum([len(singles_per_loop[l]) > 0 for l in chavloops]) / ch.avcount
					
				avg_sum_singles = sum([len(singles_per_loop[l]) for l in chavloops]) / ch.avcount
					
				# print(f"#{ic} ⇒ common singles: {len(common_singles)} | avg kills: {avg_killed:.2} | has singles: {avg_has_singles:.2} | sum singles: {avg_sum_singles}")
				'''				
				# [~] prioritize for having singles for each loop in the chain!!!
				if maq_killed == None or (avg_has_singles >= maq_has_singles and len(ch.cycles) <= len(miq_chain.cycles) and (avg_killed > maq_killed or (avg_killed == maq_killed and (ch.avcount < miq_chain.avcount or (ch.avcount == miq_chain.avcount and ch.id < miq_chain.id))))):
					
					maq_killed = avg_killed
					maq_has_singles = avg_has_singles
					maq_sum_singles = avg_sum_singles
					miq_chain = ch
					
				# if max_has_singles == None or avg_has_singles > max_has_singles or (avg_has_singles == max_has_singles and (ch.avcount < min_chain.avcount or (ch.avcount == min_chain.avcount and ch.id < min_chain.id))):
																
				# [~] …and prioritize for max sum singles
				if maz_killed == None or avg_sum_singles > maz_sum_singles or (avg_sum_singles == maz_sum_singles and avg_has_singles >= maz_has_singles and len(ch.cycles) <= len(miz_chain.cycles) and (avg_killed > maz_killed or (avg_killed == maz_killed and (ch.avcount < miz_chain.avcount or (ch.avcount == miz_chain.avcount and ch.id < miz_chain.id))))):
					
					maz_killed = avg_killed
					maz_has_singles = avg_has_singles
					maz_sum_singles = avg_sum_singles
					miz_chain = ch					
				'''											
				if max_killed == None or (
					len(ch.cycles) <= len(min_chain.cycles) and avg_has_singles > max_has_singles or (
					avg_has_singles == max_has_singles and (ch.avcount < min_chain.avcount or (
					ch.avcount == min_chain.avcount and (avg_sum_singles > max_sum_singles or (
					avg_sum_singles == max_sum_singles and (avg_killed > max_killed or (
					avg_killed == max_killed and ch.id < min_chain.id)))))))):					
											
					# maα_killed = avg_killed
					# maα_has_singles = avg_has_singles
					# maα_sum_singles = avg_sum_singles
					# miα_chain = ch
					
					# # if max_killed == None or ch.avcount < min_chain.avcount or (
					# ch.avcount == min_chain.avcount and (avg_has_singles > max_has_singles or (
					# avg_has_singles == max_has_singles and (avg_sum_singles > max_sum_singles or (
					# avg_sum_singles == max_sum_singles and (avg_killed > max_killed or (
					# avg_killed == max_killed and ch.id < min_chain.id))))))):
											
					# print(f"new max_hax_singles: {avg_has_singles} >=  prev max_has_singles: {max_has_singles} | (ch:{ch})")
					max_killed = avg_killed
					max_has_singles = avg_has_singles
					max_sum_singles = avg_sum_singles
					min_chain = ch
				
			'''
			for ch in [min_chain]:
				print(f"#: {ch} | singled? {singled} | min_chlen: {min_chlen}")				
				for il,loop in enumerate(ch.avloops()):
					print(f"# / {il} | singles: {len(singles_per_loop[loop])} | kills: {len(km[loop])}")				
			input2(f'---  chosen  --- | min chain: {min_chain} | singles has: {max_has_singles} / sum: {max_sum_singles} | killed: {max_killed}')					
			#print(f'---  previouα finds --- | min chain: {miα_chain} | has singles: {maα_has_singles} | sum singles: {maα_sum_singles} | killed: {maα_killed}')													
			#print(f'---  previouz finds --- | min chain: {miz_chain} | has singles: {maz_has_singles} | sum singles: {maz_sum_singles} | killed: {maz_killed}')					
			#input2(f'---  very old finds --- | min chain: {miq_chain} | has singles: {maq_has_singles} | sum singles: {maq_sum_singles} | killed: {maq_killed}')
			#'''
		if not singled:
			if min_chlen == 1:
				min_loops = min_chain.avloops()
			else:
				min_loops = sorted(min_chain.avloops(), key = lambda loop: (-len(singles_per_loop[loop]), -len(km[loop]), loop.firstAddress()))
	else:
		min_loops = min_chain.avloops()
		
	# print(f"⇒ chosen min loops: {len(min_loops)} | min chain: {min_chain}")
			
	for i,loop in enumerate(min_loops):
		# print(f"{key()}[{i}/{min_chain.avcount}] extending {loop}")
		assert diagram.extendLoop(loop)	
		step(pre_key, step_lvl+1, step_path+[(i, len(min_loops), loop.firstAddress())])
		diagram.collapseBack(loop)	
		
		seen.append(loop)
		diagram.setLoopUnavailable(loop)
		
	for l in reversed(seen):
		diagram.resetLoopAvailable(l)	
	
	
	
	
	
	

if __name__ == "__main__":

	KP = '2222'

	diagram = Diagram(7, kernelPath=KP)
	startTime = time()
		
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
	'''
[  34][lvl:29] off: -3 § K43212105454323212105454323210
|2222»[1∘4][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][5]
| current min off: -3  |  » ∘ «
	'''					
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	
	max_lvl_reached = 29
	min_off_reached = 1

	unicc = 0
	def uni(lvl=0, offset=0, path=[('K', f'|{KP}»')]):
		global unicc, max_lvl_reached, min_off_reached
		
		# kill early
		if offset	> 0:
			return

		# path = [(function index, function path), … ]
		if unicc % 1 == 0:
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}")
			# print(''.join([p for x,p in path]))
			# diagram.point(); show(diagram)
			# input2("[…]")
		unicc += 1

		# --- THE CHECKS --- #

		for ch in diagram.chains:
			if ch.avcount == 0:
				# diagram.pointers = ch.cycles
				# show(diagram)
				# print(f"[{unicc:>4}][lvl:{lvl}] off: {offset} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]))					
				# input2(f"| --- cycle very not available ---")
				return
						
		if lvl > max_lvl_reached:
			max_lvl_reached = lvl
			diagram.point()
			show(diagram)			
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]))			
			input2(f"| current max lvl: {max_lvl_reached}")

		if offset < min_off_reached:
			min_off_reached = offset
			show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]))			
			input2(f"| current min off: {min_off_reached}")

		if offset == -2:
			#show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]))
			#input2(f"| [off:-2]")
			#step(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} §")
																														
		if offset == -3:
			show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]))
			input2(f"| [off:-3]")
			step(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} §")
								
		if offset == -4:# and path[-1][0] == 0:
			show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]))
			input2(f"| [off:-4]")
			step(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} §")
		
		if diagram.openChain.tailNode.address.endswith('456'):
			show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]))
			input2(f"| […456]")			
		
		# --- THE ENGINE --- #								

		''' --- The Possibilities --- 
		id = "+" | links = [4,2,2,2,2] | segment =    "[+5]" | size = 12
		id =  9  | links = [3,3,2,2,2] | segment =  "[∘1∘4]" | size = 12
		id =  8  | links = [3,2,3,2,2] | segment =  "[∘2∘3]" | size = 12
		id =  7  | links = [3,2,2,3,2] | segment =  "[∘3∘2]" | size = 12
		id =  6  | links = [3,2,2,2,3] | segment =  "[∘4∘1]" | size = 12					
		id =  5  | links = [3,2,2,2,2] | segment =    "[∘5]" | size = 11
		id =  f  | links = [2,3,3,2,2] | segment = "[1∘1∘3]" | size = 12
		id =  e  | links = [2,3,2,3,2] | segment = "[1∘2∘2]" | size = 12
		id =  d  | links = [2,3,2,2,3] | segment = "[1∘3∘1]" | size = 12	
		id =  4  | links = [2,3,2,2,2] | segment =   "[1∘4]" | size = 11
		id =  c  | links = [2,2,3,3,2] | segment = "[2∘1∘2]" | size = 12
		id =  b  | links = [2,2,3,2,3] | segment = "[2∘2∘1]" | size = 12	
		id =  3  | links = [2,2,3,2,2] | segment =   "[2∘3]" | size = 11
		id =  a  | links = [2,2,2,3,3] | segment = "[3∘1∘1]" | size = 12
		id =  2  | links = [2,2,2,3,2] | segment =   "[3∘2]" | size = 11
		id =  1  | links = [2,2,2,2,3] | segment =   "[4∘1]" | size = 11	
		id =  0  | links = [2,2,2,2,2] | segment =     "[5]" | size = 10	
		'''
	
		# [0] ⇒ 2 // [5], [4∘1], [3∘2], [3∘1∘1], [2∘3], [2∘2∘1], [2∘1∘2], [1∘4], [1∘3∘1], [1∘2∘2], [1∘1∘3]
		if diagram.isOpenChainConnectable(2):
			diagram.connectOpenChain(2)
				
			## [1] ⇒ 2 // [5], [4∘1], [3∘2], [3∘1∘1], [2∘3], [2∘2∘1], [2∘1∘2]
			if diagram.isOpenChainConnectable(2):
				diagram.connectOpenChain(2)

				### [2] ⇒ 2 // [5], [4∘1], [3∘2], [3∘1∘1]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)
	
					#### [3] ⇒ 2 // [5], [4∘1]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)			

						##### [4] ⇒ 2 // [5]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)									
												
							uni(lvl+1, offset+(10-11), path+[('0', '[5]')])
											
							diagram.revertOpenChainConnect()											
						##### [4] ⇒ 2
										
						##### [4] ⇒ 3 // [4∘1]
						if diagram.isOpenChainConnectable(3):
							diagram.connectOpenChain(3)
												
							uni(lvl+1, offset+(11-11), path+[('1', '[4∘1]')])
												
							diagram.revertOpenChainConnect()											
						##### [4] ⇒ 3
	
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2
			
					#### [3] ⇒ 3 // [3∘2], [3∘1∘1]
					if diagram.isOpenChainConnectable(3):
						diagram.connectOpenChain(3)				
										
						##### [4] ⇒ 2 // [3∘2]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)									
											
							uni(lvl+1, offset+(11-11), path+[('2', '[3∘2]')])
											
							diagram.revertOpenChainConnect()											
						##### [4] ⇒ 2

						##### [4] ⇒ 3 // [3∘1∘1]
						if diagram.isOpenChainConnectable(3):
							diagram.connectOpenChain(3)
												
							uni(lvl+1, offset+(12-11), path+[('a', '[3∘1∘1]')])
												
							diagram.revertOpenChainConnect()											
						##### [4] ⇒ 3
												
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 3
							
					diagram.revertOpenChainConnect()		
				### [2] ⇒ 2
						
				### [2] ⇒ 3 // [2∘3], [2∘2∘1], [2∘1∘2]
				if diagram.isOpenChainConnectable(3):
					diagram.connectOpenChain(3)				
		
					#### [3] ⇒ 2 // [2∘3], [2∘2∘1]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
											
						##### [4] ⇒ 2 // [2∘3]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)					
																			
							uni(lvl+1, offset+(11-11), path+[(3, '[2∘3]')])
												
							diagram.revertOpenChainConnect()
						##### [4] ⇒ 2

						##### [4] ⇒ 3 // [2∘2∘1]
						if diagram.isOpenChainConnectable(3):
							diagram.connectOpenChain(3)
												
							uni(lvl+1, offset+(12-11), path+[('b', '[2∘2∘1]')])
												
							diagram.revertOpenChainConnect()											
						##### [4] ⇒ 3
						
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2
		
					#### [3] ⇒ 3 // [2∘1∘2]
					if diagram.isOpenChainConnectable(3):
						diagram.connectOpenChain(3)				
										
						##### [4] ⇒ 2 // [2∘1∘2]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)									
											
							uni(lvl+1, offset+(12-11), path+[('c', '[2∘1∘2]')])
											
							diagram.revertOpenChainConnect()											
						##### [4] ⇒ 2
												
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 3
							
					diagram.revertOpenChainConnect()		
				### [2] ⇒ 3

				diagram.revertOpenChainConnect()							
			## [1] ⇒ 2
	
			## [1] ⇒ 3 // [1∘4], [1∘3∘1], [1∘2∘2], [1∘1∘3]
			if diagram.isOpenChainConnectable(3):
				diagram.connectOpenChain(3)
						
				### [2] ⇒ 2 // [1∘4], [1∘3∘1], [1∘2∘2]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)				
										
					#### [3] ⇒ 2 // [1∘4], [1∘3∘1]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
																												
						##### [4] ⇒ 2 // [1∘4]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)
																							
							uni(lvl+1, offset+(11-11), path+[(4, '[1∘4]')])
											
							diagram.revertOpenChainConnect()
						##### [4] ⇒ 2

						##### [4] ⇒ 3 // [1∘3∘1]
						if diagram.isOpenChainConnectable(3):
							diagram.connectOpenChain(3)
												
							uni(lvl+1, offset+(12-11), path+[('d', '[1∘3∘1]')])
												
							diagram.revertOpenChainConnect()
						##### [4] ⇒ 3
																										
						diagram.revertOpenChainConnect()			
					#### [3] ⇒ 2

					#### [3] ⇒ 3 // [1∘2∘2]
					if diagram.isOpenChainConnectable(3):
						diagram.connectOpenChain(3)				
										
						##### [4] ⇒ 2 // [1∘2∘2]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)									
											
							uni(lvl+1, offset+(12-11), path+[('e', '[1∘2∘2]')])
											
							diagram.revertOpenChainConnect()											
						##### [4] ⇒ 2
												
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 3
					
					diagram.revertOpenChainConnect()
				### [2] ⇒ 2

				### [2] ⇒ 3 // [1∘1∘3]
				if diagram.isOpenChainConnectable(3):
					diagram.connectOpenChain(3)				
		
					#### [3] ⇒ 2 // [1∘1∘3]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
											
						##### [4] ⇒ 2 // [1∘1∘3]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)					
																			
							uni(lvl+1, offset+(12-11), path+[('f', '[1∘1∘3]')])
												
							diagram.revertOpenChainConnect()
						##### [4] ⇒ 2
						
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2
							
					diagram.revertOpenChainConnect()		
				### [2] ⇒ 3
						
				diagram.revertOpenChainConnect()
			## [1] ⇒ 3

			diagram.revertOpenChainConnect()			
		# [0] ⇒ 2 #
		
		# [0] ⇒ 3 // [∘5], [∘4∘1], [∘3∘2], [∘2∘3], [∘1∘4]
		if diagram.isOpenChainConnectable(3):
			diagram.connectOpenChain(3)		
			
			## [1] ⇒ 2 // [∘5], [∘4∘1], [∘3∘2], [∘2∘3]
			if diagram.isOpenChainConnectable(2):
				diagram.connectOpenChain(2)
													
				### [2] ⇒ 2 // [∘5], [∘4∘1], [∘3∘2]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)				
										
					#### [3] ⇒ 2 // [∘5], [∘4∘1]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
																													
						##### [4] ⇒ 2 // [∘5]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)					
																											
							uni(lvl+1, offset+(11-11), path+[(5, '[∘5]')])

							diagram.revertOpenChainConnect()
						##### [4] ⇒ 2
										
						##### [4] ⇒ 3 // [∘4∘1]
						if diagram.isOpenChainConnectable(3):
							diagram.connectOpenChain(3)
																							
							uni(lvl+1, offset+(12-11), path+[(6, '[∘4∘1]')])
												
							diagram.revertOpenChainConnect()
						##### [4] ⇒ 3

						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2
			
					#### [3] ⇒ 3 // [∘3∘2]
					if diagram.isOpenChainConnectable(3):
						diagram.connectOpenChain(3)				
																												
						##### [4] ⇒ 2 // [∘3∘2]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)									
																							
							uni(lvl+1, offset+(12-11), path+[(7, '[∘3∘2]')])
												
							diagram.revertOpenChainConnect()
						##### [4] ⇒ 2

						diagram.revertOpenChainConnect()
					#### [3] ⇒ 3

					diagram.revertOpenChainConnect()
				### [2] ⇒ 2
						
				### [2] ⇒ 3 // [∘2∘3]
				if diagram.isOpenChainConnectable(3):
					diagram.connectOpenChain(3)				
										
					#### [3] ⇒ 2 // [∘2∘3]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
																												
						##### [4] ⇒ 2 // [∘2∘3]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)					
																											
							uni(lvl+1, offset+(12-11), path+[(8, '[∘2∘3]')])
												
							diagram.revertOpenChainConnect()
						##### [4] ⇒ 2

						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2

					diagram.revertOpenChainConnect()
				### [2] ⇒ 2

				diagram.revertOpenChainConnect()
			## [1] ⇒ 2
	
			## [1] ⇒ 3 // [∘1∘4]
			if diagram.isOpenChainConnectable(3):
				diagram.connectOpenChain(3)
											
				### [2] ⇒ 2 // [∘1∘4]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)				
									
					#### [3] ⇒ 2 // [∘1∘4]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
																												
						##### [4] ⇒ 2 // [∘1∘4]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)									
																							
							uni(lvl+1, offset+(12-11), path+[(9, '[∘1∘4]')])
												
							diagram.revertOpenChainConnect()
						##### [4] ⇒ 2

						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2

					diagram.revertOpenChainConnect()
				### [2] ⇒ 2
	
				diagram.revertOpenChainConnect()
			## [1] ⇒ 3

			diagram.revertOpenChainConnect()			
		# [0] ⇒ 3
		
		# [0] ⇒ 4 // [+5]
		# if diagram.isOpenChainConnectable(4):
		# 	diagram.connectOpenChain(4)		
		# 
			## [1] ⇒ 2 // [+5]
		# 	if diagram.isOpenChainConnectable(2):
		# 		diagram.connectOpenChain(2)
		# 
				### [2] ⇒ 2 // [+5]
		# 		if diagram.isOpenChainConnectable(2):
		# 			diagram.connectOpenChain(2)				
		# 
					#### [3] ⇒ 2 // [+5]
		# 			if diagram.isOpenChainConnectable(2):
		# 				diagram.connectOpenChain(2)				
		# 
						##### [4] ⇒ 2 // [+5]
		# 				if diagram.isOpenChainConnectable(2):
		# 					diagram.connectOpenChain(2)									
		# 
		# 					uni(lvl+1, offset+(12-11), path+[('+', '[+5]')])
		# 
		# 					diagram.revertOpenChainConnect() 
						##### [4] ⇒ 2
		# 
		# 				diagram.revertOpenChainConnect() 
					#### [3] ⇒ 2
		# 
		# 			diagram.revertOpenChainConnect() 
				### [2] ⇒ 2
		# 
		# 		diagram.revertOpenChainConnect() 
			## [1] ⇒ 2
		# 
		# 	diagram.revertOpenChainConnect() 
		# [0] ⇒ 4
																					
	print("\n\n -------------- \n\n")		
	
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

	def pOc(segment):
		for i,x in enumerate(reversed(segment)):
			if x == ' ':
				pass
			elif x == 'b':
				assert diagram.prependOpenChain('l3b')
			elif x == '+':
				assert diagram.prependOpenChain(4)
			else:
				assert diagram.prependOpenChain(int(x))
				
	''' --- The Possibilities --- 
	id = "+" | links = [4,2,2,2,2] | segment =    "[+5]" | size = 12
	id =  9  | links = [3,3,2,2,2] | segment =  "[∘1∘4]" | size = 12
	id =  8  | links = [3,2,3,2,2] | segment =  "[∘2∘3]" | size = 12
	id =  7  | links = [3,2,2,3,2] | segment =  "[∘3∘2]" | size = 12
	id =  6  | links = [3,2,2,2,3] | segment =  "[∘4∘1]" | size = 12					
	id =  5  | links = [3,2,2,2,2] | segment =    "[∘5]" | size = 11
	id =  f  | links = [2,3,3,2,2] | segment = "[1∘1∘3]" | size = 12
	id =  e  | links = [2,3,2,3,2] | segment = "[1∘2∘2]" | size = 12
	id =  d  | links = [2,3,2,2,3] | segment = "[1∘3∘1]" | size = 12	
	id =  4  | links = [2,3,2,2,2] | segment =   "[1∘4]" | size = 11
	id =  c  | links = [2,2,3,3,2] | segment = "[2∘1∘2]" | size = 12
	id =  b  | links = [2,2,3,2,3] | segment = "[2∘2∘1]" | size = 12	
	id =  3  | links = [2,2,3,2,2] | segment =   "[2∘3]" | size = 11
	id =  a  | links = [2,2,2,3,3] | segment = "[3∘1∘1]" | size = 12
	id =  2  | links = [2,2,2,3,2] | segment =   "[3∘2]" | size = 11
	id =  1  | links = [2,2,2,2,3] | segment =   "[4∘1]" | size = 11	
	id =  0  | links = [2,2,2,2,2] | segment =     "[5]" | size = 10	
	'''			
	
	def cId(segment):
		for i,x in enumerate(segment):
			if   x == '0': cOc('22222')
			elif x == '1': cOc('22223')
			elif x == '2': cOc('22232')
			elif x == 'a': cOc('22233')			
			elif x == '3': cOc('22322')
			elif x == 'b': cOc('22323')
			elif x == 'c': cOc('22332')									
			elif x == '4': cOc('23222')
			elif x == 'd': cOc('23223')
			elif x == 'e': cOc('23232')
			elif x == 'f': cOc('23322')			
			elif x == '5': cOc('32222')
			elif x == '6': cOc('32223')
			elif x == '7': cOc('32232')
			elif x == '8': cOc('32322')
			elif x == '9': cOc('33222')			
			elif x == '+': cOc('42222')
	
	def pId(segment):
		for i,x in enumerate(reversed(segment)):
			if   x == '0': pOc('22222')
			
			elif x == '1': pOc('22223')
			elif x == '2': pOc('22232')
			
			elif x == 'a': pOc('22233')			
			
			elif x == '3': pOc('22322')
			
			elif x == 'b': pOc('22323')
			elif x == 'c': pOc('22332')						
			
			elif x == '4': pOc('23222')			
			
			elif x == 'd': pOc('23223')
			elif x == 'e': pOc('23232')
			elif x == 'f': pOc('23322')
						
			elif x == '5': pOc('32222')
						
			elif x == '6': pOc('32223')
			elif x == '7': pOc('32232')
			elif x == '8': pOc('32322')
			elif x == '9': pOc('33222')			
			
			elif x == '+': pOc('42222')
				
	# K        4  
	# sides = '23222'
	# 
	# cOc(sides)
	# pOc(list(reversed(sides)))
	# 
	# 
	# uni(1, 0, [('K4', f'«2232«2»2322»|{sides}|')])
	
	# [  26][lvl:24] off:  0 § K43210+43210+43210+432121
	#    43210+43210+43210+432121
	# |2222» [1∘4] [2∘3] [3∘2] #[4∘1]  [5]  [+5]  [1∘4] [2∘3] [3∘2] [4∘1]  [5]  [+5]  [1∘4] [2∘3] [3∘2] [4∘1]  [5]  [+5]  [1∘4] [2∘3] #[3∘2] [4∘1] [3∘2] [4∘1]		
	#cOc(    '23222 22322 22232')# 22223 22222 42222 23222 22322 22232 22223 22222 42222 23222 22322 22232 22223 22222 42222 23222 22322')# 22232 22223 22232 22223')
	#cOc('22322 22232 22223')
	#cId('3543254324325434')
	
	'''#[`]
	
	cId('45')
	
	#cId('54')
	
	diagram.headCycle = diagram.cycleByAddress['00045']
	diagram.openChain = diagram.headCycle.chain
	
	# setup open chain
	diagram.openChain.isOpen = True
	diagram.openChain.headNode = diagram.headCycle.nodes[0]
	diagram.openChain.tailNode = diagram.headCycle.nodes[-1]
	
	pId('054323212108210')
	pOc('22323')#'''
	#pOc('22232 22223 22322 23223 22222 32222 23222 22323 22222')
		
	# uni()#1, 0, [('Kx', '32222')])
		
	# diagram.extendLoop(diagram.nodeByAddress['003444'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['003453'].loop)

	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	'''
	base_unloops = set([l for l in diagram.loops if not l.available])
	added_unloops_per_avloop = {}
	min_chlen_per_avloop = {}
	
	for il, loop in enumerate(diagram.loops):
		if loop.available:
			
			assert diagram.extendLoop(loop)
			
			added_unloops_per_avloop[loop] = [l for l in diagram.loops if not l.available and l not in base_unloops]
			min_chlen_per_avloop[loop] = min([len(ch.avnodes) for ch in diagram.chains])
			
			diagram.collapseBack(loop)
			
			if len(added_unloops_per_avloop[loop]) > 10:
				print(f"[un]#{il}: {loop} | unloops: {len(added_unloops_per_avloop[loop])} | min chlen: {min_chlen_per_avloop[loop]}")
	
	for ic,chain in enumerate(diagram.chains):
		if len(chain.avnodes) > 0:
			chloops = set(added_unloops_per_avloop[chain.avnodes[0].loop])
			chloops.difference_update([n.loop for n in chain.avnodes])
			for node in chain.avnodes[1:]:
				chloops.intersection_update(added_unloops_per_avloop[node.loop])
		
		if len(chloops) > 0:
			print(f"[ch]#{ic}: {chain}⇒{chain.cycles[0]} | chloops: {len(chloops)} // {chloops}")	
		print(f"[ch]#{ic}: {chain}⇒{chain.cycles[0]} | total unloops: {sum([len(added_unloops_per_avloop[n.loop]) for n in chain.avnodes])}")
	'''
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
		
	#uni(0, 0, [('K…/2', '⁑')])
		
	uni()
		
	diagram.point()
	show(diagram)	
