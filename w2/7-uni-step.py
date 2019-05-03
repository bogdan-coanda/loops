from diagram import *
from uicanvas import *
from mx import *
from time import time
from collections import defaultdict
from functools import reduce
import pathlib

'''
'''


step_cc = -1
step_id = -1
min_step_chains_reached = 106
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
		
		with open('7.Ω.sols.txt', 'a', encoding="utf8") as log:
			log.write(' '.join([addr for _,_,addr in step_path]) + "\n")
		with open('7.Ω.path.txt', 'a', encoding="utf8") as log:
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
	
	# ∘∘∘ ∘∘∘ ∘∘∘ #

	min_chain = None
	for ch in diagram.chains:
		if min_chain == None or ch.avcount < min_chain.avcount or (ch.avcount == min_chain.avcount and ch.id < min_chain.id):
			min_chain = ch
	
	if min_chain.avcount > 1: # and step_id % 4 == 0: 
	
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
			singles_per_loop = {}
			
			for loop in diagram.loops:
				if loop.available:
	
					diagram.extendLoop(loop)
					min_chlen = min([ch.avcount for ch in diagram.chains])
					chain_count = len(diagram.chains)
					singles_per_loop[loop] = set([ch.avloops()[0] for ch in diagram.chains if ch.avcount == 1])
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
															
				avg_has_singles = sum([len(singles_per_loop[l]) > 0 for l in chavloops]) / ch.avcount
					
				avg_sum_singles = sum([len(singles_per_loop[l]) for l in chavloops]) / ch.avcount
					
				# print(f"#{ic} ⇒ common singles: {len(common_singles)} | avg kills: {avg_killed:.2} | has singles: {avg_has_singles:.2} | sum singles: {avg_sum_singles}")
				if max_killed == None or (
					len(ch.cycles) <= len(min_chain.cycles) and avg_has_singles > max_has_singles or (
					avg_has_singles == max_has_singles and (ch.avcount < min_chain.avcount or (
					ch.avcount == min_chain.avcount and (avg_sum_singles > max_sum_singles or (
					avg_sum_singles == max_sum_singles and (avg_killed > max_killed or (
					avg_killed == max_killed and ch.id < min_chain.id)))))))):					
																						
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
		# input2(f"{key()}[{i}/{min_chain.avcount}] extending {loop}")
		
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

[  37][lvl:31] off: -3 § K4321210545432321210545432321210
|2222»[1∘4][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5]
| [off:-3]  |  » ∘ «

--- ∘ ---

[ 146][lvl:29] off: -3 § K43212105454343212105454343210
|2222»[1∘4][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][1∘4][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][1∘4][2∘3][3∘2][4∘1][5]
| [off:-3] § u3: 2 | u4: 0  |  » ∘ «
	'''					
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	
	max_lvl_reached = 93 # 82 // [+5] 93
	min_off_reached = -3 # 1

	unicc = 0
	u3 = 0
	u4 = 0
	
	U1 = 7  # from [lvl:5][off:-1]
	U2 = 19 # from [lvl:17][off:-2]
	U3 = 31 # from [lvl:29][off:-3]
	UCC = { -3: 0, -4: 0 } # 3: 34
	
	def uni(lvl=0, offset=0, path=[('K', f'|{KP}»')]):
		global unicc, u3, u4, max_lvl_reached, min_off_reached
		
		# kill early
		if offset	> 0:
			return



		# kill by upper bound
		if lvl >= U1 and offset > -1:
			return 
		if lvl >= U2 and offset > -2: 
			return 
		if lvl >= U3 and offset > -3: 
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

		# if offset == -2:
		# 	pass
		# 	show(diagram)
		# 	print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]))
		# 	input2(f"| [off:-2]")
		# 	step(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} §")
																														
		if offset <= -3 and offset >= -4:

			curr_path = ''.join([str(x) for x,p in path])
			
			is_done = False
			done_cfg = pathlib.Path('7.Ω.u.done.txt') 
			if done_cfg.is_file(): 
				with open('7.Ω.u.done.txt', 'r', encoding="utf8") as log:
					for line_index, line in enumerate(log):			
						_, _, _, _, _, _, _, u_path = line.split()
						if u_path == curr_path:
							is_done = True
							break
		
			if not is_done:
				
				is_seen = False
				seen_cfg = pathlib.Path('7.Ω.u.seen.txt')
				
				u_index = 0
				u_counts = "counts:0/0"
				
				if seen_cfg.is_file():
					with open('7.Ω.u.seen.txt', 'r', encoding="utf8") as log:
						for line_index, line in enumerate(log):
							u_index, u_reachts, u_offset, u_counts, u_bounds, u_unicc, u_lvl, u_path = line.split()
							if u_path == curr_path:
								is_seen = True
								break
				
				u_index = int(u_index) + 1
				u_counts = [int(x) for x in u_counts.split(':')[1].split('/')]
				u_counts[abs(offset)-3] += 1

				if not is_seen:
					with open('7.Ω.u.seen.txt', 'a', encoding="utf8") as log:
						log.write(f"{u_index:>4}  {tstr(time()-startTime):>12}  off:{offset}  counts:{'/'.join([str(x) for x in u_counts])}  bounds:{U1}/{U2}/{U3}  unicc:{unicc:<4}  lvl:{lvl}  {curr_path}" + "\n")
						show(diagram)
						print(f"#{u_index} [{unicc:>4}][lvl:{lvl}] off: {offset} § {''.join([str(x) for x,p in path])}")
						input2(f"| [off:{offset}] § counts:{'/'.join([str(x) for x in u_counts])}")
						
					step_enter_ts = time()
					step(f"[{unicc:>4}][lvl:{lvl}] off: {offset} §")						
					with open('7.Ω.u.done.txt', 'a', encoding="utf8") as log:
						log.write(f"{u_index:>4}  {tstr(time() - step_enter_ts):>12}  off:{offset}  counts:{'/'.join([str(x) for x in u_counts])}  bounds:{U1}/{U2}/{U3}  unicc:{unicc:<4}  lvl:{lvl}  {curr_path}" + "\n")
						input2(f"#{u_index} [{unicc}][lvl:{lvl}] off: {offset} » done: {''.join([str(x) for x,_ in path])}")
												
				else: # is seen
					input2(f"[{unicc:>4}][lvl:{lvl}] off: {offset} § already seen: {''.join([str(x) for x,p in path])}")
									
			else: # is done
				input2(f"[{unicc}][lvl:{lvl}] off: {offset} § already done: {''.join([str(x) for x,p in path])}")			
									
		if offset <= -4:
			show(diagram)
			print(f"[{unicc}][lvl:{lvl}] off: {offset} § {''.join([str(x) for x,p in path])}")
			input2(f"| [off:{offset}] § u3: {u3} | u4: {u4} | u?: !")
						
		#if diagram.openChain.tailNode.address.endswith('456'):
		#	show(diagram)
		#	print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]))
		#	input2(f"| […456]")			
		
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
