from diagram import *
from uicanvas import *
from mx import *
from time import time



step_cc = -1
step_id = -1
min_step_chains_reached = 99999999
sols_cc = 0


def step(pre_key, step_lvl=0, step_path=[]):
	global step_cc, step_id, min_step_chains_reached, sols_cc
	if step_lvl == 0:
		step_cc += 1
	step_id += 1
	
	def key():
		return f"{pre_key}[{step_cc:>2}»{step_id:>4}][{tstr(time() - startTime):>11}][lvl:{step_lvl}]"

	if step_id % 1 == 0:							
		print(f"{key()}[ch:{len(diagram.chains)}|av:{len([l for l in diagram.loops if l.available])}] {'.'.join([(str(x)+upper(t)) for x,t,_ in step_path])}")
	
	if len(diagram.chains) == 1:
		show(diagram)
		
		with open('6.sols.txt', 'a', encoding="utf8") as log:
			log.write(' '.join([addr for _,_,addr in step_path]) + "\n")
		with open('6.path.txt', 'a', encoding="utf8") as log:
			log.write('.'.join([(str(x)+upper(t)) for x,t,_ in step_path]) + "\n")
					
		input2(f"{key()} #{sols_cc} sol found.")
		sols_cc += 1
		return
		
	# if len(diagram.chains) < min_step_chains_reached:
	# 	min_step_chains_reached = len(diagram.chains)
	# 	diagram.point()
	# 	show(diagram)
	# 	input2(f"{key()} new min step chains: {min_step_chains_reached}")

	# unloops/chloops
	seen = []
						
	while step_lvl % 10 == 0 and min([len(ch.avnodes) for ch in diagram.chains]) > 1:
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
			
	# if len(seen) > 0:
	# 	print(f"{key()}[ch:{len(diagram.chains)}|av:{len([l for l in diagram.loops if l.available])}] {'.'.join([(str(x)+upper(t)) for x,t in step_path])}")		
	# print(f"{key()}[purge] ⇒ killed: {len(seen)} | ⇒ min chlen: {min([len(ch.avnodes) for ch in diagram.chains])}")
										
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

	KP = '222'

	diagram = Diagram(6, kernelPath=KP)
	startTime = time()
		
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
				
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	
	max_lvl_reached = -1
	min_off_reached = 1

	unicc = 0
	def uni(lvl=0, offset=0, path=[('K', f'|{KP}»')]):
		global unicc, max_lvl_reached, min_off_reached
		
		# kill early
		if offset	> 2:
			return

		# path = [(function index, function path), … ]
		if unicc % 100 == 0:
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
			show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]))
			input2(f"| [off:-2]")
			step(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} §")
																														
		if offset == -3:
			show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]))
			input2(f"| [off:-3]")
			step(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} §")
								
		if offset == -4:# and path[-1][0] == 0:
			show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')
			input2(f"| [off:-4]")
			step(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} §")

		if diagram.openChain.tailNode.address.endswith('456'):
			show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]))
			input2(f"| […456]")			
									
		# --- THE ENGINE --- #								

		''' --- The Possibilities --- 
		id = "+" | links = [4,2,2,2] | segment =    "[+4]" | size = 10
		id =  7  | links = [3,3,2,2] | segment =  "[∘1∘3]" | size = 10
		id =  6  | links = [3,2,3,2] | segment =  "[∘2∘2]" | size = 10					
		id =  5  | links = [3,2,2,3] | segment =  "[∘3∘1]" | size = 10
		id =  4  | links = [3,2,2,2] | segment =    "[∘4]" | size = 9
		id =  c  | links = [2,3,3,2] | segment = "[1∘1∘2]" | size = 10		
		id =  b  | links = [2,3,2,3] | segment = "[1∘2∘1]" | size = 10
		id =  3  | links = [2,3,2,2] | segment =   "[1∘3]" | size = 9
		id =  a  | links = [2,2,3,3] | segment = "[2∘1∘1]" | size = 10
		id =  2  | links = [2,2,3,2] | segment =   "[2∘2]" | size = 9
		id =  1  | links = [2,2,2,3] | segment =   "[3∘1]" | size = 9	
		id =  0  | links = [2,2,2,2] | segment =     "[4]" | size = 8
		'''
			
		# [0] ⇒ 2 // [4], [3∘1], [2∘2], [2∘1∘1], [1∘3], [1∘2∘1], [1∘1∘2]
		if diagram.isOpenChainConnectable(2):
			diagram.connectOpenChain(2)
				
			## [1] ⇒ 2 // [4], [3∘1], [2∘2], [2∘1∘1]
			if diagram.isOpenChainConnectable(2):
				diagram.connectOpenChain(2)

				### [2] ⇒ 2 // [4], [3∘1]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)
	
					#### [3] ⇒ 2 // [4]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)			
												
						uni(lvl+1, offset+(8-9), path+[(0, '[4]')])
												
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2
			
					#### [3] ⇒ 3 // [3∘1]
					if diagram.isOpenChainConnectable(3):
						diagram.connectOpenChain(3)				
																					
						uni(lvl+1, offset+(9-9), path+[(1, '[3∘1]')])			
			
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 3
							
					diagram.revertOpenChainConnect()		
				### [2] ⇒ 2
						
				### [2] ⇒ 3 // [2∘2], [2∘1∘1]
				if diagram.isOpenChainConnectable(3):
					diagram.connectOpenChain(3)				
		
					#### [3] ⇒ 2 // [2∘2]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
																														
						uni(lvl+1, offset+(9-9), path+[(2, '[2∘2]')])

						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2

					#### [3] ⇒ 3 // [2∘1∘1]
					if diagram.isOpenChainConnectable(3):
						diagram.connectOpenChain(3)				
																					
						uni(lvl+1, offset+(10-9), path+[('a', '[2∘1∘1]')])			
			
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 3
									
					diagram.revertOpenChainConnect()		
				### [2] ⇒ 3

				diagram.revertOpenChainConnect()							
			## [1] ⇒ 2
	
			## [1] ⇒ 3 // [1∘3], [1∘2∘1], [1∘1∘2]
			if diagram.isOpenChainConnectable(3):
				diagram.connectOpenChain(3)
						
				### [2] ⇒ 2 // [1∘3], [1∘2∘1]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)				
										
					#### [3] ⇒ 2 // [1∘3]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
																							
						uni(lvl+1, offset+(9-9), path+[(3, '[1∘3]')])
										
						diagram.revertOpenChainConnect()			
					#### [3] ⇒ 2

					#### [3] ⇒ 3 // [1∘2∘1]
					if diagram.isOpenChainConnectable(3):
						diagram.connectOpenChain(3)				
																					
						uni(lvl+1, offset+(10-9), path+[('b', '[1∘2∘1]')])			
			
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 3
					
					diagram.revertOpenChainConnect()
				### [2] ⇒ 2

				### [2] ⇒ 3 // [1∘1∘2]
				if diagram.isOpenChainConnectable(3):
					diagram.connectOpenChain(3)				
		
					#### [3] ⇒ 2 // [1∘1∘2]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
																														
						uni(lvl+1, offset+(10-9), path+[('c', '[1∘1∘2]')])

						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2
					
					diagram.revertOpenChainConnect()		
				### [2] ⇒ 3					
					
				diagram.revertOpenChainConnect()
			## [1] ⇒ 3

			diagram.revertOpenChainConnect()			
		# [0] ⇒ 2 #
		
		# [0] ⇒ 3 // [∘4], [∘3∘1], [∘2∘2], [∘1∘3]
		if diagram.isOpenChainConnectable(3):
			diagram.connectOpenChain(3)		
			
			## [1] ⇒ 2 // [∘4], [∘3∘1], [∘2∘2]
			if diagram.isOpenChainConnectable(2):
				diagram.connectOpenChain(2)
													
				### [2] ⇒ 2 // [∘4], [∘3∘1]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)				
										
					#### [3] ⇒ 2 // [∘4]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
																													
						uni(lvl+1, offset+(9-9), path+[(4, '[∘4]')])

						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2
			
					#### [3] ⇒ 3 // [∘3∘1]
					if diagram.isOpenChainConnectable(3):
						diagram.connectOpenChain(3)				
																							
						uni(lvl+1, offset+(10-9), path+[(5, '[∘3∘1]')])
												
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 3

					diagram.revertOpenChainConnect()
				### [2] ⇒ 2
						
				### [2] ⇒ 3 // [∘2∘2]
				if diagram.isOpenChainConnectable(3):
					diagram.connectOpenChain(3)				
										
					#### [3] ⇒ 2 // [∘2∘2]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				

						uni(lvl+1, offset+(10-9), path+[(6, '[∘2∘2]')])

						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2

					diagram.revertOpenChainConnect()
				### [2] ⇒ 3

				diagram.revertOpenChainConnect()
			## [1] ⇒ 2
	
			## [1] ⇒ 3 // [∘1∘3]
			if diagram.isOpenChainConnectable(3):
				diagram.connectOpenChain(3)
											
				### [2] ⇒ 2 // [∘1∘3]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)				
									
					#### [3] ⇒ 2 // [∘1∘3]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
																												
						uni(lvl+1, offset+(10-9), path+[(7, '[∘1∘3]')])
												
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2

					diagram.revertOpenChainConnect()
				### [2] ⇒ 2
	
				diagram.revertOpenChainConnect()
			## [1] ⇒ 3

			diagram.revertOpenChainConnect()			
		# [0] ⇒ 3

		# [0] ⇒ 4 // [+4]
		if diagram.isOpenChainConnectable(4):
			diagram.connectOpenChain(4)		
				
			## [1] ⇒ 2 // [+4]
			if diagram.isOpenChainConnectable(2):
				diagram.connectOpenChain(2)
						
				### [2] ⇒ 2 // [+4]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)				

					#### [3] ⇒ 2 // [+4]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
										
						uni(lvl+1, offset+(10-9), path+[('+', '[+4]')])
						
						diagram.revertOpenChainConnect()			
					#### [3] ⇒ 2

					diagram.revertOpenChainConnect()			
				### [2] ⇒ 2
				
				diagram.revertOpenChainConnect()
			## [1] ⇒ 2
				
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
	id = "+" | links = [4,2,2,2] | segment =    "[+4]" | size = 10
	id =  7  | links = [3,3,2,2] | segment =  "[∘1∘3]" | size = 10
	id =  6  | links = [3,2,3,2] | segment =  "[∘2∘2]" | size = 10					
	id =  5  | links = [3,2,2,3] | segment =  "[∘3∘1]" | size = 10
	id =  4  | links = [3,2,2,2] | segment =    "[∘4]" | size = 9
	id =  c  | links = [2,3,3,2] | segment = "[1∘1∘2]" | size = 10		
	id =  b  | links = [2,3,2,3] | segment = "[1∘2∘1]" | size = 10
	id =  3  | links = [2,3,2,2] | segment =   "[1∘3]" | size = 9
	id =  a  | links = [2,2,3,3] | segment = "[2∘1∘1]" | size = 10
	id =  2  | links = [2,2,3,2] | segment =   "[2∘2]" | size = 9
	id =  1  | links = [2,2,2,3] | segment =   "[3∘1]" | size = 9	
	id =  0  | links = [2,2,2,2] | segment =     "[4]" | size = 8
	'''

	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #	

	'''
	cOc('2322 2232 2223 2222 4222 2322 2232 2223 2222 4222 2322 2232 2223 2222')
	diagram.extendLoop(diagram.nodeByAddress['11005'].loop)
	diagram.extendLoop(diagram.nodeByAddress['11105'].loop)
	diagram.extendLoop(diagram.nodeByAddress['11205'].loop)
	diagram.extendLoop(diagram.nodeByAddress['11305'].loop)
	diagram.extendLoop(diagram.nodeByAddress['10104'].loop)
	#diagram.extendLoop(diagram.nodeByAddress['00042'].loop)
	'''	

	#cOc('2322 2232 2223 2222')
	cOc('2322 2232 2223 2222 4222 2322 2232 2223 2222 4222 2322 2232 2223 2222')
		
	# n0 = diagram.nodeByAddress['00001']
	# diagram.extendLoop(n0.loop)
	# 
	# n1 = diagram.nodeByAddress['00211']
	# diagram.extendLoop(n1.loop)
	# 
	# n2 = diagram.nodeByAddress['00111']
	# diagram.extendLoop(n2.loop)
	
	# n3 = diagram.nodeByAddress['00043']
	# diagram.extendLoop(n3.loop)
		
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
		
	
	step(f"§")
	# uni()
		
	diagram.point()
	show(diagram)	
