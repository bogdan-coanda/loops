from diagram import *
from universe import *
from mx import *
from time import time

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
min_step_chains_reached = 111
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
						
	while min([len(ch.avnodes) for ch in diagram.chains]) > 1: # step_lvl % 14 == 0 and 
		killedSomething = False
	
		for il, loop in enumerate(diagram.loops):
			if loop.available:
				
				assert diagram.extendLoop(loop)
				min_chlen_per_current_avloop = min([len(ch.avnodes) for ch in diagram.chains])				
				diagram.collapseBack(loop)
				
				if min_chlen_per_current_avloop == 0:
					diagram.setLoopUnavailable(loop)
					seen.append(loop)
					killedSomething = True
					
				# print(f"[un]#{il}: {loop} | min chlen: {min_chlen_per_current_avloop}")	
				
				if min([len(n.cycle.chain.avnodes) for n in loop.nodes]) == 0:
					killedSomething = False
					break
	
		# print(f"current min chlen: {min([len(ch.avnodes) for ch in diagram.chains])}")
		if not killedSomething:
			break
			
	if len(seen) > 0:
		print(f"{key()}[ch:{len(diagram.chains)}|av:{len([l for l in diagram.loops if l.available])}] {'.'.join([(str(x)+upper(t)) for x,t,_ in step_path])}")		
		print(f"{key()}[purge] ⇒ killed: {len(seen)} | ⇒ min chlen: {min([len(ch.avnodes) for ch in diagram.chains])}")

	min_chain = sorted(diagram.chains, key = lambda chain: (len(chain.avnodes), chain.id))[0]
	# print(f"{key()} chosen min: {min_chain}")
	
	min_avlen = len(min_chain.avnodes)
		
	for i,n in enumerate(sorted(min_chain.avnodes, key = lambda n: n.address)):
		assert diagram.extendLoop(n.loop)		
		step(pre_key, step_lvl+1, step_path+[(i, min_avlen, n.loop.firstAddress())])
		diagram.collapseBack(n.loop)	
		
		seen.append(n.loop)
		diagram.setLoopUnavailable(n.loop)
		
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
			if len(ch.avnodes) == 0:
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
