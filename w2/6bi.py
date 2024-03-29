from diagram import *
from uicanvas import *
from mx import *
from time import time



step_cc = -1
step_id = -1
jump_id = -1
min_jump_chains_reached = 99999999
min_step_chains_reached = 99999999
jump_step_required_lvl = 30


def step(pre_key, avloops, jump_lvl, jump_path, step_lvl=0, step_path=[]):
	global step_cc, step_id, min_step_chains_reached
	if step_lvl == 0:
		step_cc += 1
	step_id += 1
	
	def key():
		return f"{pre_key}[{step_cc:>2}»{step_id:>4}][{tstr(time() - startTime):>11}][lvl:{jump_lvl}»{step_lvl}]"
			
	print(f"{key()}[ch:{len(diagram.chains)}|av:{len(avloops)}] {'.'.join([(str(x)+upper(t)) for x,t in jump_path])}\n» {'.'.join([(str(x)+upper(t)) for x,t in step_path])}")
	
	if len(diagram.chains) == 1:
		show(diagram)
		input2(f"{key()} sol found.")
		return
		
	if len(diagram.chains) < min_step_chains_reached:
		min_step_chains_reached = len(diagram.chains)
		show(diagram)
		input2(f"{key()} new min step chains: {min_step_chains_reached}")
				
	min_chain = sorted(diagram.chains, key = lambda chain: (len(chain.avnodes), chain.id))[0]
	# print(f"{key()} chosen min: {min_chain}")
	
	seen = []
	min_avlen = len(min_chain.avnodes)
	
	for i,n in enumerate(sorted(min_chain.avnodes, key = lambda n: n.address)):
		assert diagram.extendLoop(n.loop)		
		step(pre_key, [l for l in avloops if l.available], jump_lvl, jump_path, step_lvl+1, step_path+[(i, min_avlen)])
		diagram.collapseBack(n.loop)	
		
		seen.append(n.loop)
		diagram.setLoopUnavailable(n.loop)
		
	for l in reversed(seen):
		diagram.resetLoopAvailable(l)
		
		
def jump(pre_key, mx, avtuples, lvl=0, path=[]):
	global jump_id, min_jump_chains_reached
	jump_id += 1
		
	def key():
		return f"{pre_key}[{jump_id:>4}][{tstr(time() - startTime):>11}][lvl:{lvl}]" 
	
	if jump_id % 100 == 0:
		print(f"{key()} {'.'.join([(str(x)+upper(t)) for x,t in path])}")
	
	if len(diagram.chains) < min_jump_chains_reached:
		min_jump_chains_reached = len(diagram.chains)
		show(diagram)
		input2(f"{key()} new min jump chains: {min_jump_chains_reached}")
	
	min_chlen = mx.min_chain_avloops_length()	
	# print(f"{key()}[mx] 1. min_chlen: {min_chlen}")	
	
	if min_chlen == 0:
		# print(f"{key()}[mx] ⇒ dead @ unconnectable")
		return
		
	unicycle_chains = mx.filter_unicycle_chains()	
	# print(f"{key()}[mx] 2. unicycle chains: {len(unicycle_chains)}")	
		
	if len(unicycle_chains) == 0:
		print(f"{key()}[mx] ⇒ all cycles covered by tuples")
		step(f"{pre_key}[{jump_id:>4}]", [l for l in diagram.loops if l.available], lvl, path)
		input2(f"[jump] « [step] // cc")
		return			
		
	avtuples = mx.filter_avtuples(avtuples)	
	# print(f"{key()}[mx] 3. avtuples: {len(avtuples)} / {len(diagram.loop_tuples)}")	

	if len(avtuples) == 0:
		if lvl >= jump_step_required_lvl:
			print(f"{key()}[mx] ⇒ no tuples remaining")			
			step(f"{pre_key}[{jump_id:>4}]", [l for l in diagram.loops if l.available], lvl, path)
			# input2(f"[jump] « [step] // nt")
		return			
				
	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	# print(f"{key()}[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")		

	if len(min_nodes) == 0:
		if lvl >= jump_step_required_lvl:
			print(f"{key()}[mx] ⇒ not coverable by tuples | {min_cycle}")
			step(f"{pre_key}[{jump_id:>4}]", [l for l in diagram.loops if l.available], lvl, path)
			# input2(f"[jump] « [step] // nc")		
		return
		
	if lvl < 12 and len(min_nodes) > 1:
		# print(f"{key()}[mx] ⇒ not single choice, purging…")
		
		# [~] next_single_choices is unused ?
		avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
		# print(f"{key()}[mx][purge] avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

		if len(avtuples) == 0:
			if lvl >= jump_step_required_lvl:
				print(f"{key()}[mx][purge] ⇒ no tuples remaining")
				step(f"{pre_key}[{jump_id:>4}]", [l for l in diagram.loops if l.available], lvl, path)
				# input2(f"[jump] « [step] // nt")
			return			
												
		min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)
		# print(f"{key()}[mx][purge] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
		
		if len(min_nodes) == 0:
			if lvl >= jump_step_required_lvl:
				print(f"{key()}[mx] ⇒ not coverable by tuples | {min_cycle}")
				step(f"{pre_key}[{jump_id:>4}]", [l for l in diagram.loops if l.available], lvl, path)
				# input2(f"[jump] « [step] // nc")		
			return
				
	else:
		# print(f"{key()}[mx] ⇒ single choice.")
		pass
		
	# go through all choices
	for it, t in enumerate(min_matched_tuples):
		if t in avtuples: # [~][!] needed if no purge
						
			ec = 0
			for lt, l in enumerate(t):
				if diagram.extendLoop(l):
					ec += 1
				else:
					break
	
			if ec == len(t): # if we've extended all of the tuple's loops
				jump(pre_key, mx, avtuples, lvl+1, path+[(it,len(min_matched_tuples))])
	
			for l in reversed(t[:ec]):
				diagram.collapseBack(l)	
				
			# remove tested choice for further jumps		
			avtuples.remove(t)

	# print(f"{key()} ⇒ finished all choices")
	
	
	
	
	
	
	

if __name__ == "__main__":

	KP = '232 2 223'

	diagram = Diagram(6, kernelPath=KP)
	startTime = time()
		
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
	
	def lazarus(pre_key):
		print(f"{pre_key}[mx] 0. walk | loop tuples: {len(diagram.loop_tuples)}")
		diagram.walk([diagram.openChain.headNode, diagram.openChain.tailNode.prevs[1].node], True)				
		print(f"{pre_key}[mx] 0. walk | loop tuples: {len(diagram.loop_tuples)}")			
		mx = MX(diagram)
			
		min_chlen = mx.min_chain_avloops_length()	
		print(f"{pre_key}[mx] 1. min chain avloops length: {min_chlen}")	
		
		unicycle_chains = mx.filter_unicycle_chains()	
		print(f"{pre_key}[mx] 2. unicycle chains: {len(unicycle_chains)}")	
			
		print(f"{pre_key}[mx] 3. loop tuples: {len(diagram.loop_tuples)} | av loops: {len([l for l in diagram.loops if l.available])}")
		avtuples = mx.filter_avtuples()	
		print(f"{pre_key}[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")		
		
		min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
		print(f"{pre_key}[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")			
		
		jump(pre_key, mx, avtuples)			
			
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	
	max_lvl_reached = 0
	min_off_reached = 0

	bicc = 0
	def bi(lvl=0, offset=0, path=[('K', f'«{KP[:3]}«{KP[3]}»{KP[4:]}»')]):
		global bicc, max_lvl_reached, min_off_reached
		
		# kill early
		if offset	> 2:
			return

		# path = [(function index, function path), … ]
		if bicc % 100 == 0:
			print(f"[{bicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}") # + '\n' + ''.join([p for x,p in path]))
		bicc += 1

		# --- THE CHECKS --- #

		for ch in diagram.chains:
			if len(ch.avnodes) == 0:
				# assert len(ch.cycles) == 1
				# diagram.pointers = ch.cycles
				# show(diagram)
				# print(f"[{bicc:>4}][lvl:{lvl}] off: {offset} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')					
				# input2(f"| --- cycle very not available ---")
				return
						
		if lvl > max_lvl_reached:
			max_lvl_reached = lvl
			show(diagram)
			print(f"[{bicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')			
			input2(f"| current max lvl: {max_lvl_reached}")

		if offset < min_off_reached:
			min_off_reached = offset
			show(diagram)
			print(f"[{bicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')			
			input2(f"| current min off: {min_off_reached}")

		if offset == -2:
			# show(diagram)
			print(f"[{bicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')
			# input2(f"| [off:-2]")
			lazarus(f"[{bicc:>4}][lvl:{lvl}]")
																														
		if offset == -3:
			show(diagram)
			print(f"[{bicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')
			input2(f"| [off:-3]")
			lazarus(f"[{bicc:>4}][lvl:{lvl}]")
					
		if offset == -4:# and path[-1][0] == 0:
			show(diagram)
			print(f"[{bicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')
			input2(f"| [off:-4]")
			lazarus(f"[{bicc:>4}][lvl:{lvl}]")
			
		# --- THE ENGINE --- #								

		''' --- The Possibilities --- 
		id = "+" | links = [4,2,2,2] | segment =   "[+4]" | size = 10
		id =  7  | links = [3,3,2,2] | segment = "[∘1∘3]" | size = 10
		id =  6  | links = [3,2,3,2] | segment = "[∘2∘2]" | size = 10					
		id =  5  | links = [3,2,2,3] | segment = "[∘3∘1]" | size = 10
		id =  4  | links = [3,2,2,2] | segment =   "[∘4]" | size = 9
		id =  3  | links = [2,3,2,2] | segment =  "[1∘3]" | size = 9
		id =  2  | links = [2,2,3,2] | segment =  "[2∘2]" | size = 9
		id =  1  | links = [2,2,2,3] | segment =  "[3∘1]" | size = 9	
		id =  0  | links = [2,2,2,2] | segment =    "[4]" | size = 8
		'''
	
		# [0] ⇒ 2 // [4], [3∘1], [2∘2], [1∘3]
		if diagram.isOpenChainConnectable(2):
			diagram.connectOpenChain(2)
			if diagram.isOpenChainPrependable(2):
				diagram.prependOpenChain(2)
				
				## [1] ⇒ 2 // [4], [3∘1], [2∘2]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)
					if diagram.isOpenChainPrependable(2):
						diagram.prependOpenChain(2)

						### [2] ⇒ 2 // [4], [3∘1]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)
							if diagram.isOpenChainPrependable(2):
								diagram.prependOpenChain(2)
	
								#### [3] ⇒ 2 // [4]
								if diagram.isOpenChainConnectable(2):
									diagram.connectOpenChain(2)			
									if diagram.isOpenChainPrependable(2):
										diagram.prependOpenChain(2)
												
										bi(lvl+1, offset+(8-9), path+[(0, '[4]')])
												
										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()
								#### [3] ⇒ 2
			
								#### [3] ⇒ 3 // [3∘1]
								if diagram.isOpenChainConnectable(3):
									diagram.connectOpenChain(3)				
									if diagram.isOpenChainPrependable(3):
										diagram.prependOpenChain(3)
																					
										bi(lvl+1, offset+(9-9), path+[(1, '[3∘1]')])			
			
										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()
								#### [3] ⇒ 3
							
								diagram.revertOpenChainPrepend()
							diagram.revertOpenChainConnect()		
						### [2] ⇒ 2
						
						### [2] ⇒ 3 // [2∘2]
						if diagram.isOpenChainConnectable(3):
							diagram.connectOpenChain(3)				
							if diagram.isOpenChainPrependable(3):
								diagram.prependOpenChain(3)
		
								#### [3] ⇒ 2 // [2∘2]
								if diagram.isOpenChainConnectable(2):
									diagram.connectOpenChain(2)				
									if diagram.isOpenChainPrependable(2):
										diagram.prependOpenChain(2)
																														
										bi(lvl+1, offset+(9-9), path+[(2, '[2∘2]')])

										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()
								#### [3] ⇒ 2
		
								diagram.revertOpenChainPrepend()
							diagram.revertOpenChainConnect()		
						### [2] ⇒ 3

						diagram.revertOpenChainPrepend()
					diagram.revertOpenChainConnect()							
				## [1] ⇒ 2
	
				## [1] ⇒ 3 // [1∘3]
				if diagram.isOpenChainConnectable(3):
					diagram.connectOpenChain(3)
					if diagram.isOpenChainPrependable(3):
						diagram.prependOpenChain(3)					
						
						### [2] ⇒ 2 // [1∘3]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)				
							if diagram.isOpenChainPrependable(2):
								diagram.prependOpenChain(2)
										
								#### [3] ⇒ 2 // [1∘3]
								if diagram.isOpenChainConnectable(2):
									diagram.connectOpenChain(2)				
									if diagram.isOpenChainPrependable(2):
										diagram.prependOpenChain(2)
																							
										bi(lvl+1, offset+(9-9), path+[(3, '[1∘3]')])
										
										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()			
								#### [3] ⇒ 2

								diagram.revertOpenChainPrepend()
							diagram.revertOpenChainConnect()
						### [2] ⇒ 2

						diagram.revertOpenChainPrepend()
					diagram.revertOpenChainConnect()
				## [1] ⇒ 3

				diagram.revertOpenChainPrepend()			
			diagram.revertOpenChainConnect()			
		# [0] ⇒ 2 #
		
		# [0] ⇒ 3 // [∘4], [∘3∘1], [∘2∘2], [∘1∘3]
		if diagram.isOpenChainConnectable(3):
			diagram.connectOpenChain(3)		
			if diagram.isOpenChainPrependable(3):
				diagram.prependOpenChain(3)								
			
				## [1] ⇒ 2 // [∘4], [∘3∘1], [∘2∘2]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)
					if diagram.isOpenChainPrependable(2):
						diagram.prependOpenChain(2)
													
						### [2] ⇒ 2 // [∘4], [∘3∘1]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)				
							if diagram.isOpenChainPrependable(2):
								diagram.prependOpenChain(2)
										
								#### [3] ⇒ 2 // [∘4]
								if diagram.isOpenChainConnectable(2):
									diagram.connectOpenChain(2)				
									if diagram.isOpenChainPrependable(2):
										diagram.prependOpenChain(2)
																													
										bi(lvl+1, offset+(9-9), path+[(4, '[∘4]')])

										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()
								#### [3] ⇒ 2
			
								#### [3] ⇒ 3 // [∘3∘1]
								if diagram.isOpenChainConnectable(3):
									diagram.connectOpenChain(3)				
									if diagram.isOpenChainPrependable(3):
										diagram.prependOpenChain(3)
																							
										bi(lvl+1, offset+(10-9), path+[(5, '[∘3∘1]')])
												
										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()
								#### [3] ⇒ 3

								diagram.revertOpenChainPrepend()
							diagram.revertOpenChainConnect()
						### [2] ⇒ 2
						
						### [2] ⇒ 3 // [∘2∘2]
						if diagram.isOpenChainConnectable(3):
							diagram.connectOpenChain(3)				
							if diagram.isOpenChainPrependable(3):
								diagram.prependOpenChain(3)
										
								#### [3] ⇒ 2 // [∘2∘2]
								if diagram.isOpenChainConnectable(2):
									diagram.connectOpenChain(2)				
									if diagram.isOpenChainPrependable(2):
										diagram.prependOpenChain(2)

										bi(lvl+1, offset+(10-9), path+[(6, '[∘2∘2]')])

										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()
								#### [3] ⇒ 2

								diagram.revertOpenChainPrepend()
							diagram.revertOpenChainConnect()
						### [2] ⇒ 3

						diagram.revertOpenChainPrepend()
					diagram.revertOpenChainConnect()
				## [1] ⇒ 2
	
				## [1] ⇒ 3 // [∘1∘3]
				if diagram.isOpenChainConnectable(3):
					diagram.connectOpenChain(3)
					if diagram.isOpenChainPrependable(3):
						diagram.prependOpenChain(3)
											
						### [2] ⇒ 2 // [∘1∘3]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)				
							if diagram.isOpenChainPrependable(2):
								diagram.prependOpenChain(2)	
									
								#### [3] ⇒ 2 // [∘1∘3]
								if diagram.isOpenChainConnectable(2):
									diagram.connectOpenChain(2)				
									if diagram.isOpenChainPrependable(2):
										diagram.prependOpenChain(2)
																												
										bi(lvl+1, offset+(10-9), path+[(7, '[∘1∘3]')])
												
										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()
								#### [3] ⇒ 2

								diagram.revertOpenChainPrepend()
							diagram.revertOpenChainConnect()
						### [2] ⇒ 2
	
						diagram.revertOpenChainPrepend()
					diagram.revertOpenChainConnect()
				## [1] ⇒ 3

				diagram.revertOpenChainPrepend()			
			diagram.revertOpenChainConnect()			
		# [0] ⇒ 3

		# [0] ⇒ 4 // [+4]
		if diagram.isOpenChainConnectable(4):
			diagram.connectOpenChain(4)		
			if diagram.isOpenChainPrependable(4):
				diagram.prependOpenChain(4)								
				
				# [1] ⇒ 2 // [+4]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)
					if diagram.isOpenChainPrependable(2):
						diagram.prependOpenChain(2)
						
						## [2] ⇒ 2 // [+4]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)				
							if diagram.isOpenChainPrependable(2):
								diagram.prependOpenChain(2)	

								### [3] ⇒ 2 // [+4]
								if diagram.isOpenChainConnectable(2):
									diagram.connectOpenChain(2)				
									if diagram.isOpenChainPrependable(2):
										diagram.prependOpenChain(2)
										
										bi(lvl+1, offset+(10-9), path+[('+', '[+4]')])
						
										diagram.revertOpenChainPrepend()			
									diagram.revertOpenChainConnect()			
								### [3] ⇒ 2

								diagram.revertOpenChainPrepend()			
							diagram.revertOpenChainConnect()			
						## [2] ⇒ 2
				
						diagram.revertOpenChainPrepend()
					diagram.revertOpenChainConnect()
				## [1] ⇒ 2
				
				diagram.revertOpenChainPrepend()			
			diagram.revertOpenChainConnect()			
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
	id = "+" | links = [4,2,2,2] | segment =   "[+4]" | size = 10
	id =  7  | links = [3,3,2,2] | segment = "[∘1∘3]" | size = 10
	id =  6  | links = [3,2,3,2] | segment = "[∘2∘2]" | size = 10					
	id =  5  | links = [3,2,2,3] | segment = "[∘3∘1]" | size = 10
	id =  4  | links = [3,2,2,2] | segment =   "[∘4]" | size = 9
	id =  3  | links = [2,3,2,2] | segment =  "[1∘3]" | size = 9
	id =  2  | links = [2,2,3,2] | segment =  "[2∘2]" | size = 9
	id =  1  | links = [2,2,2,3] | segment =  "[3∘1]" | size = 9	
	id =  0  | links = [2,2,2,2] | segment =    "[4]" | size = 8
	'''
			
	# K        4  
	# sides = '23222'
	# 
	# cOc(sides)
	# pOc(list(reversed(sides)))
	# 
	# 
	# bi(1, 0, [('K4', f'«2232«2»2322»|{sides}|')])
	
	bi()
		
	show(diagram)	

