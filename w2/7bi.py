from diagram import *
from uicanvas import *


if __name__ == "__main__":

	diagram = Diagram(7, kernelPath='223222322')
			
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	
	max_lvl_reached = 42 # [2866099]
	min_off_reached = 0

	bicc = 0
	def bi(lvl=0, offset=0, path=[('K', '«2232«2»2322»')]):
		global bicc, max_lvl_reached, min_off_reached
		
		# kill early
		if offset	> 0:
			return

		# path = [(function index, function path), … ]
		if bicc % 100 == 0:
			print(f"[{bicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}") # + '\n' + ''.join([p for x,p in path]))
		bicc += 1

		# --- THE CHECKS --- #

		for ch in diagram.chains:
			if len(ch.avnodes) == 0:
				assert len(ch.cycles) == 1
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
						
		if offset == -3:
			show(diagram)
			print(f"[{bicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')
			input2(f"| [off:-3]")
					
		if offset == -4:# and path[-1][0] == 0:
			show(diagram)
			print(f"[{bicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')
			input2(f"| [off:-4]")

		# if diagram.openChain.tailNode.address.endswith('000456'):
		# 	show(diagram)
		# 	print(f"[{bicc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')
		# 	input2(f"| [:456]")
			
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
			if diagram.isOpenChainPrependable(2):
				diagram.prependOpenChain(2)
				
				## [1] ⇒ 2 // [5], [4∘1], [3∘2], [2∘3]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)
					if diagram.isOpenChainPrependable(2):
						diagram.prependOpenChain(2)

						### [2] ⇒ 2 // [5], [4∘1], [3∘2]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)
							if diagram.isOpenChainPrependable(2):
								diagram.prependOpenChain(2)
	
								#### [3] ⇒ 2 // [5], [4∘1]
								if diagram.isOpenChainConnectable(2):
									diagram.connectOpenChain(2)			
									if diagram.isOpenChainPrependable(2):
										diagram.prependOpenChain(2)

										##### [4] ⇒ 2 // [5]
										if diagram.isOpenChainConnectable(2):
											diagram.connectOpenChain(2)									
											if diagram.isOpenChainPrependable(2):
												diagram.prependOpenChain(2)
												
												bi(lvl+1, offset+(10-11), path+[(0, '[5]')])
											
												diagram.revertOpenChainPrepend()
											diagram.revertOpenChainConnect()											
										##### [4] ⇒ 2
										
										##### [4] ⇒ 3 // [4∘1]
										if diagram.isOpenChainConnectable(3):
											diagram.connectOpenChain(3)
											if diagram.isOpenChainPrependable(3):
												diagram.prependOpenChain(3)
												
												bi(lvl+1, offset+(11-11), path+[(1, '[4∘1]')])
												
												diagram.revertOpenChainPrepend()
											diagram.revertOpenChainConnect()											
										##### [4] ⇒ 3
	
										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()
								#### [3] ⇒ 2
			
								#### [3] ⇒ 3 // [3∘2]
								if diagram.isOpenChainConnectable(3):
									diagram.connectOpenChain(3)				
									if diagram.isOpenChainPrependable(3):
										diagram.prependOpenChain(3)
										
										##### [4] ⇒ 2 // [3∘2]
										if diagram.isOpenChainConnectable(2):
											diagram.connectOpenChain(2)									
											if diagram.isOpenChainPrependable(2):
												diagram.prependOpenChain(2)											
											
												bi(lvl+1, offset+(11-11), path+[(2, '[3∘2]')])
											
												diagram.revertOpenChainPrepend()
											diagram.revertOpenChainConnect()											
										##### [4] ⇒ 2
			
										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()
								#### [3] ⇒ 3
							
								diagram.revertOpenChainPrepend()
							diagram.revertOpenChainConnect()		
						### [2] ⇒ 2
						
						### [2] ⇒ 3 // [2∘3]
						if diagram.isOpenChainConnectable(3):
							diagram.connectOpenChain(3)				
							if diagram.isOpenChainPrependable(3):
								diagram.prependOpenChain(3)
		
								#### [3] ⇒ 2 // [2∘3]
								if diagram.isOpenChainConnectable(2):
									diagram.connectOpenChain(2)				
									if diagram.isOpenChainPrependable(2):
										diagram.prependOpenChain(2)
											
										##### [4] ⇒ 2 // [2∘3]
										if diagram.isOpenChainConnectable(2):
											diagram.connectOpenChain(2)					
											if diagram.isOpenChainPrependable(2):
												diagram.prependOpenChain(2)
																			
												bi(lvl+1, offset+(11-11), path+[(3, '[2∘3]')])
												
												diagram.revertOpenChainPrepend()
											diagram.revertOpenChainConnect()
										##### [4] ⇒ 2

										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()
								#### [3] ⇒ 2
		
								diagram.revertOpenChainPrepend()
							diagram.revertOpenChainConnect()		
						### [2] ⇒ 3

						diagram.revertOpenChainPrepend()
					diagram.revertOpenChainConnect()							
				## [1] ⇒ 2
	
				## [1] ⇒ 3 // [1∘4]
				if diagram.isOpenChainConnectable(3):
					diagram.connectOpenChain(3)
					if diagram.isOpenChainPrependable(3):
						diagram.prependOpenChain(3)					
						
						### [2] ⇒ 2 // [1∘4]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)				
							if diagram.isOpenChainPrependable(2):
								diagram.prependOpenChain(2)
										
								#### [3] ⇒ 2 // [1∘4]
								if diagram.isOpenChainConnectable(2):
									diagram.connectOpenChain(2)				
									if diagram.isOpenChainPrependable(2):
										diagram.prependOpenChain(2)
																												
										##### [4] ⇒ 2 // [1∘4]
										if diagram.isOpenChainConnectable(2):
											diagram.connectOpenChain(2)
											if diagram.isOpenChainPrependable(2):
												diagram.prependOpenChain(2)
																							
												bi(lvl+1, offset+(11-11), path+[(4, '[1∘4]')])
											
												diagram.revertOpenChainPrepend()
											diagram.revertOpenChainConnect()
										##### [4] ⇒ 2
										
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
		
		# [0] ⇒ 3 // [∘5], [∘4∘1], [∘3∘2], [∘2∘3], [∘1∘4]
		if diagram.isOpenChainConnectable(3):
			diagram.connectOpenChain(3)		
			if diagram.isOpenChainPrependable(3):
				diagram.prependOpenChain(3)								
			
				## [1] ⇒ 2 // [∘5], [∘4∘1], [∘3∘2], [∘2∘3]
				if diagram.isOpenChainConnectable(2):
					diagram.connectOpenChain(2)
					if diagram.isOpenChainPrependable(2):
						diagram.prependOpenChain(2)
													
						### [2] ⇒ 2 // [∘5], [∘4∘1], [∘3∘2]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)				
							if diagram.isOpenChainPrependable(2):
								diagram.prependOpenChain(2)
										
								#### [3] ⇒ 2 // [∘5], [∘4∘1]
								if diagram.isOpenChainConnectable(2):
									diagram.connectOpenChain(2)				
									if diagram.isOpenChainPrependable(2):
										diagram.prependOpenChain(2)
																													
										##### [4] ⇒ 2 // [∘5]
										if diagram.isOpenChainConnectable(2):
											diagram.connectOpenChain(2)					
											if diagram.isOpenChainPrependable(2):
												diagram.prependOpenChain(2)
																											
												bi(lvl+1, offset+(11-11), path+[(5, '[∘5]')])

												diagram.revertOpenChainPrepend()
											diagram.revertOpenChainConnect()
										##### [4] ⇒ 2
										
										##### [4] ⇒ 3 // [∘4∘1]
										if diagram.isOpenChainConnectable(3):
											diagram.connectOpenChain(3)
											if diagram.isOpenChainPrependable(3):
												diagram.prependOpenChain(3)
																							
												bi(lvl+1, offset+(12-11), path+[(6, '[∘4∘1]')])
												
												diagram.revertOpenChainPrepend()
											diagram.revertOpenChainConnect()
										##### [4] ⇒ 3

										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()
								#### [3] ⇒ 2
			
								#### [3] ⇒ 3 // [∘3∘2]
								if diagram.isOpenChainConnectable(3):
									diagram.connectOpenChain(3)				
									if diagram.isOpenChainPrependable(3):
										diagram.prependOpenChain(3)
																												
										##### [4] ⇒ 2 // [∘3∘2]
										if diagram.isOpenChainConnectable(2):
											diagram.connectOpenChain(2)									
											if diagram.isOpenChainPrependable(2):
												diagram.prependOpenChain(2)
																							
												bi(lvl+1, offset+(12-11), path+[(7, '[∘3∘2]')])
												
												diagram.revertOpenChainPrepend()
											diagram.revertOpenChainConnect()
										##### [4] ⇒ 2

										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()
								#### [3] ⇒ 3

								diagram.revertOpenChainPrepend()
							diagram.revertOpenChainConnect()
						### [2] ⇒ 2
						
						### [2] ⇒ 3 // [∘2∘3]
						if diagram.isOpenChainConnectable(3):
							diagram.connectOpenChain(3)				
							if diagram.isOpenChainPrependable(3):
								diagram.prependOpenChain(3)
										
								#### [3] ⇒ 2 // [∘2∘3]
								if diagram.isOpenChainConnectable(2):
									diagram.connectOpenChain(2)				
									if diagram.isOpenChainPrependable(2):
										diagram.prependOpenChain(2)
																												
										##### [4] ⇒ 2 // [∘2∘3]
										if diagram.isOpenChainConnectable(2):
											diagram.connectOpenChain(2)					
											if diagram.isOpenChainPrependable(2):
												diagram.prependOpenChain(2)
																											
												bi(lvl+1, offset+(12-11), path+[(8, '[∘2∘3]')])
												
												diagram.revertOpenChainPrepend()
											diagram.revertOpenChainConnect()
										##### [4] ⇒ 2

										diagram.revertOpenChainPrepend()
									diagram.revertOpenChainConnect()
								#### [3] ⇒ 2

								diagram.revertOpenChainPrepend()
							diagram.revertOpenChainConnect()
						### [2] ⇒ 2

						diagram.revertOpenChainPrepend()
					diagram.revertOpenChainConnect()
				## [1] ⇒ 2
	
				## [1] ⇒ 3 // [∘1∘4]
				if diagram.isOpenChainConnectable(3):
					diagram.connectOpenChain(3)
					if diagram.isOpenChainPrependable(3):
						diagram.prependOpenChain(3)
											
						### [2] ⇒ 2 // [∘1∘4]
						if diagram.isOpenChainConnectable(2):
							diagram.connectOpenChain(2)				
							if diagram.isOpenChainPrependable(2):
								diagram.prependOpenChain(2)	
									
								#### [3] ⇒ 2 // [∘1∘4]
								if diagram.isOpenChainConnectable(2):
									diagram.connectOpenChain(2)				
									if diagram.isOpenChainPrependable(2):
										diagram.prependOpenChain(2)
																												
										##### [4] ⇒ 2 // [∘1∘4]
										if diagram.isOpenChainConnectable(2):
											diagram.connectOpenChain(2)									
											if diagram.isOpenChainPrependable(2):
												diagram.prependOpenChain(2)
																							
												bi(lvl+1, offset+(12-11), path+[(9, '[∘1∘4]')])
												
												diagram.revertOpenChainPrepend()
											diagram.revertOpenChainConnect()
										##### [4] ⇒ 2

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
		
		# 4 ⇐ [0] // dc_x5
		# if diagram.isOpenChainConnectable(4):
		# 	diagram.connectOpenChain(4)		
		# 
			## 2 ⇐ [1] // dc_x5
		# 	if diagram.isOpenChainConnectable(2):
		# 		diagram.connectOpenChain(2)
		# 
				### 2 ⇐ [2] // dc_x5
		# 		if diagram.isOpenChainConnectable(2):
		# 			diagram.connectOpenChain(2)				
		# 
					#### 2 ⇐ [3] // dc_x5
		# 			if diagram.isOpenChainConnectable(2):
		# 				diagram.connectOpenChain(2)				
		# 
						##### 2 ⇐ [4] // dc_x5
		# 				if diagram.isOpenChainConnectable(2):
		# 					diagram.connectOpenChain(2)									
		# 					bi(lvl+1, offset+(12-11), path+[('+', '[+5]')])
		# 					diagram.revertOpenChain() 
						##### 2 ⇐ [4]
		# 
		# 				diagram.revertOpenChain() 
					#### 2 ⇐ [3]
		# 
		# 			diagram.revertOpenChain() 
				### 2 ⇐ [2]
		# 
		# 		diagram.revertOpenChain() 
			## 2 ⇐ [1]
		# 
		# 	diagram.revertOpenChain() 
		# 4 ⇐ [0]
		
																					
	print("\n\n -------------- \n\n")		
	
	bi()	
		
	show(diagram)	
	
	'''
	[24013][lvl:24] off: -2 § K454323210605454354323210
	«2222«3»2222»[1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][5][∘4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][5]	
	| current min off: -2  |  » ∘ «	
	
	[157039][lvl:29] off: -2 § K32108254323210710605454323210
	«2223«2»3222»[2∘3][3∘2][4∘1][5][∘2∘3][3∘2][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][5][∘3∘2][4∘1][5][∘4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][5]
	| current min off: -2  |  » ∘ «
	
	
	[show] chains: 561 | connected cycles: 160 | links: ℓ₁x960 ℓ₂x131 ℓ₃x28 ℓ₄x0 | total: 1306 | final: 5905.0
￼	[  18][lvl:15] off: -2 § K210605454323210
	«2232«2»2322»[3∘2][4∘1][5][∘4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][5]
	| current min off: -2  |  » ∘ «
	
	
	'''	
