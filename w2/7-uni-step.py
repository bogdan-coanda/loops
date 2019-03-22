from diagram import *
from uicanvas import *
from mx import *
from time import time



step_cc = -1
step_id = -1
min_step_chains_reached = 99999999


def step(pre_key, step_lvl=0, step_path=[]):
	global step_cc, step_id, min_step_chains_reached
	if step_lvl == 0:
		step_cc += 1
	step_id += 1
	
	def key():
		return f"{pre_key}[{step_cc:>2}»{step_id:>4}][{tstr(time() - startTime):>11}][lvl:{step_lvl}]"
			
	print(f"{key()}[ch:{len(diagram.chains)}|av:{len([l for l in diagram.loops if l.available])}] {'.'.join([(str(x)+upper(t)) for x,t in step_path])}")
	
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
		step(pre_key, step_lvl+1, step_path+[(i, min_avlen)])
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
				
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	
	max_lvl_reached = 75
	min_off_reached = 0

	unicc = 0
	def uni(lvl=0, offset=0, path=[('K', f'|{KP}»')]):
		global unicc, max_lvl_reached, min_off_reached
		
		# kill early
		if offset	> 0:
			return

		# path = [(function index, function path), … ]
		if unicc % 100 == 0:
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}")
		unicc += 1

		# --- THE CHECKS --- #

		for ch in diagram.chains:
			if len(ch.avnodes) == 0:
				# diagram.pointers = ch.cycles
				# show(diagram)
				# print(f"[{unicc:>4}][lvl:{lvl}] off: {offset} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')					
				# input2(f"| --- cycle very not available ---")
				return
						
		if lvl > max_lvl_reached:
			max_lvl_reached = lvl
			show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')			
			input2(f"| current max lvl: {max_lvl_reached}")

		if offset < min_off_reached:
			min_off_reached = offset
			show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')			
			input2(f"| current min off: {min_off_reached}")

		if offset == -2:
			# show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')
			# input2(f"| [off:-2]")
			# step(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} §")
																														
		if offset == -3:
			show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')
			input2(f"| [off:-3]")
			step(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} §")
								
		if offset == -4:# and path[-1][0] == 0:
			show(diagram)
			print(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')
			input2(f"| [off:-4]")
			step(f"[{unicc:>4}][lvl:{lvl}] off: {offset:>2} §")
			
		# --- THE ENGINE --- #								

		''' --- The Possibilities --- 
		id = "+" | links = [4,2,2,2,2] | segment =   "[+5]" | size = 12
		id =  9  | links = [3,3,2,2,2] | segment = "[∘1∘4]" | size = 12
		id =  8  | links = [3,2,3,2,2] | segment = "[∘2∘3]" | size = 12
		id =  7  | links = [3,2,2,3,2] | segment = "[∘3∘2]" | size = 12
		id =  6  | links = [3,2,2,2,3] | segment = "[∘4∘1]" | size = 12					
		id =  5  | links = [3,2,2,2,2] | segment =   "[∘5]" | size = 11
		id =  4  | links = [2,3,2,2,2] | segment =  "[1∘4]" | size = 11
		id =  3  | links = [2,2,3,2,2] | segment =  "[2∘3]" | size = 11
		id =  2  | links = [2,2,2,3,2] | segment =  "[3∘2]" | size = 11
		id =  1  | links = [2,2,2,2,3] | segment =  "[4∘1]" | size = 11	
		id =  0  | links = [2,2,2,2,2] | segment =    "[5]" | size = 10	
		'''
	
		# [0] ⇒ 2 // [5], [4∘1], [3∘2], [2∘3], [1∘4]
		if diagram.isOpenChainConnectable(2):
			diagram.connectOpenChain(2)
				
			## [1] ⇒ 2 // [5], [4∘1], [3∘2], [2∘3]
			if diagram.isOpenChainConnectable(2):
				diagram.connectOpenChain(2)

				### [2] ⇒ 2 // [5], [4∘1], [3∘2]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)
	
					#### [3] ⇒ 2 // [5], [4∘1]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)			

						##### [4] ⇒ 2 // [5]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)									
												
							uni(lvl+1, offset+(10-11), path+[(0, '[5]')])
											
							diagram.revertOpenChainConnect()											
						##### [4] ⇒ 2
										
						##### [4] ⇒ 3 // [4∘1]
						if diagram.isOpenChainConnectable(3):
							diagram.connectOpenChain(3)
												
							uni(lvl+1, offset+(11-11), path+[(1, '[4∘1]')])
												
							diagram.revertOpenChainConnect()											
						##### [4] ⇒ 3
	
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2
			
					#### [3] ⇒ 3 // [3∘2]
					if diagram.isOpenChainConnectable(3):
						diagram.connectOpenChain(3)				
										
						##### [4] ⇒ 2 // [3∘2]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)									
											
							uni(lvl+1, offset+(11-11), path+[(2, '[3∘2]')])
											
							diagram.revertOpenChainConnect()											
						##### [4] ⇒ 2
			
						diagram.revertOpenChainConnect()
					#### [3] ⇒ 3
							
					diagram.revertOpenChainConnect()		
				### [2] ⇒ 2
						
				### [2] ⇒ 3 // [2∘3]
				if diagram.isOpenChainConnectable(3):
					diagram.connectOpenChain(3)				
		
					#### [3] ⇒ 2 // [2∘3]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
											
						##### [4] ⇒ 2 // [2∘3]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)					
																			
							uni(lvl+1, offset+(11-11), path+[(3, '[2∘3]')])
												
							diagram.revertOpenChainConnect()
						##### [4] ⇒ 2

						diagram.revertOpenChainConnect()
					#### [3] ⇒ 2
		
					diagram.revertOpenChainConnect()		
				### [2] ⇒ 3

				diagram.revertOpenChainConnect()							
			## [1] ⇒ 2
	
			## [1] ⇒ 3 // [1∘4]
			if diagram.isOpenChainConnectable(3):
				diagram.connectOpenChain(3)
						
				### [2] ⇒ 2 // [1∘4]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)				
										
					#### [3] ⇒ 2 // [1∘4]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				
																												
						##### [4] ⇒ 2 // [1∘4]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)
																							
							uni(lvl+1, offset+(11-11), path+[(4, '[1∘4]')])
											
							diagram.revertOpenChainConnect()
						##### [4] ⇒ 2
										
						diagram.revertOpenChainConnect()			
					#### [3] ⇒ 2

					diagram.revertOpenChainConnect()
				### [2] ⇒ 2

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
		if diagram.isOpenChainConnectable(4):
			diagram.connectOpenChain(4)		

			## [1] ⇒ 2 // [+5]
			if diagram.isOpenChainConnectable(2):
				diagram.connectOpenChain(2)

				### [2] ⇒ 2 // [+5]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)				

					#### [3] ⇒ 2 // [+5]
					if diagram.isOpenChainConnectable(2):
						diagram.connectOpenChain(2)				

						##### [4] ⇒ 2 // [+5]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)									
							
							uni(lvl+1, offset+(12-11), path+[('+', '[+5]')])
							
							diagram.revertOpenChainConnect() 
						##### [4] ⇒ 2

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
		id = "+" | links = [4,2,2,2,2] | segment =   "[+5]" | size = 12
		id =  9  | links = [3,3,2,2,2] | segment = "[∘1∘4]" | size = 12
		id =  8  | links = [3,2,3,2,2] | segment = "[∘2∘3]" | size = 12
		id =  7  | links = [3,2,2,3,2] | segment = "[∘3∘2]" | size = 12
		id =  6  | links = [3,2,2,2,3] | segment = "[∘4∘1]" | size = 12					
		id =  5  | links = [3,2,2,2,2] | segment =   "[∘5]" | size = 11
		id =  4  | links = [2,3,2,2,2] | segment =  "[1∘4]" | size = 11
		id =  3  | links = [2,2,3,2,2] | segment =  "[2∘3]" | size = 11
		id =  2  | links = [2,2,2,3,2] | segment =  "[3∘2]" | size = 11
		id =  1  | links = [2,2,2,2,3] | segment =  "[4∘1]" | size = 11	
		id =  0  | links = [2,2,2,2,2] | segment =    "[5]" | size = 10	
		'''			
	# K        4  
	# sides = '23222'
	# 
	# cOc(sides)
	# pOc(list(reversed(sides)))
	# 
	# 
	# uni(1, 0, [('K4', f'«2232«2»2322»|{sides}|')])
	
	uni()
		
	show(diagram)	
