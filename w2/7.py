from diagram import *
from uicanvas import *


if __name__ == "__main__":

	diagram = Diagram(7)
	
	def dc(path):
		for i in range(len(path)):
			if not diagram.connectOpenChain(path[i]):
				for _ in range(i):
					diagram.revertOpenChain()
				return False
		return True
	
	def dc_x5():
		return dc([4,2,2,2,2])
	dc_x5.__setattr__('path', '[+5]')	
	dc_x5.__setattr__('size', 12)
	
	def dc_014():
		return dc([3,3,2,2,2])
	dc_014.__setattr__('path', '[∘1∘4]')
	dc_014.__setattr__('size', 12)
	
	def dc_023():
		return dc([3,2,3,2,2])
	dc_023.__setattr__('path', '[∘2∘3]')
	dc_023.__setattr__('size', 12)
						
	def dc_032():
		return dc([3,2,2,3,2])
	dc_032.__setattr__('path', '[∘3∘2]')			
	dc_032.__setattr__('size', 12)

	def dc_041():
		return dc([3,2,2,2,3])
	dc_041.__setattr__('path', '[∘4∘1]')			
	dc_041.__setattr__('size', 12)
					
	def dc_05():
		return dc([3,2,2,2,2])
	dc_05.__setattr__('path', '[∘5]')
	dc_05.__setattr__('size', 11)
						
	def dc_14():		
		return dc([2,3,2,2,2])
	dc_14.__setattr__('path', '[1∘4]')
	dc_14.__setattr__('size', 11)
		
	def dc_23():
		return dc([2,2,3,2,2])
	dc_23.__setattr__('path', '[2∘3]')	
	dc_23.__setattr__('size', 11)
		
	def dc_32():
		return dc([2,2,2,3,2])
	dc_32.__setattr__('path', '[3∘2]')	
	dc_32.__setattr__('size', 11)

	def dc_41():
		return dc([2,2,2,2,3])
	dc_41.__setattr__('path', '[4∘1]')	
	dc_41.__setattr__('size', 11)
					
	def dc_5():
		return dc([2,2,2,2,2])
	dc_5.__setattr__('path', '[5]')	
	dc_5.__setattr__('size', 10)
		
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	
	max_lvl_reached = 85
	min_off_reached = 0

	btcc = 0
	def bt(lvl=0, offset=0, path=[]):
		global btcc, max_lvl_reached, min_off_reached
		
		# kill early
		if offset	> 0:
			return
		if lvl > 35:
			return
		if len([c for c in diagram.cycles if c.address.startswith('00') and c.address[2] != '0' and c.chain.isOpen]) > 0:
			return

		# path = [(function index, function path), … ]
		if btcc % 1000 == 0:
			print(f"[{btcc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}") # + '\n' + ''.join([p for x,p in path]))
		btcc += 1

		# --- THE CHECKS --- #

		for ch in diagram.chains:
			if len(ch.avnodes) == 0:
				assert len(ch.cycles) == 1
				# if ch.cycles[0].nodes[0].prevs[2].node.cycle.chain == diagram.openChain and ch.cycles[0].nodes[0].prevs[3].node.cycle.chain == diagram.openChain:
				# 	diagram.pointers = ch.cycles + [ch.cycles[0].nodes[0].prevs[2].node, ch.cycles[0].nodes[0].prevs[3].node]
				# 	show(diagram)
				# 	print(f"[{btcc:>4}][lvl:{lvl}] off: {offset} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')					
				# 	input2(f"--- cycle very not available ---")
				return
						
		if lvl > max_lvl_reached:
			max_lvl_reached = lvl
			show(diagram)
			print(f"[{btcc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')			
			input2(f"| current max lvl: {max_lvl_reached}")

		if offset < min_off_reached:
			min_off_reached = offset
			show(diagram)
			print(f"[{btcc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')			
			input2(f"| current min off: {min_off_reached}")
		
		if offset == -4 and path[-1][0] == 0:
			show(diagram)
			print(f"[{btcc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')
			input2(f"| [-4]")

		if diagram.openChain.tailNode.address.endswith('000456'):
			show(diagram)
			print(f"[{btcc:>4}][lvl:{lvl}] off: {offset:>2} § {''.join([str(x) for x,p in path])}" + '\n' + ''.join([p for x,p in path]) + '\n')
			input2(f"| [:456]")
			
		# --- THE ENGINE --- #								

		# 2 ⇐ [0] // dc_5, dc_41, dc_32, dc_23, dc_14
		if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
			diagram.connectOpenChain(2)		
			
			## 2 ⇐ [1] // dc_5, dc_41, dc_32, dc_23
			if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
				diagram.connectOpenChain(2)
				
				### 2 ⇐ [2] // dc_5, dc_41, dc_32
				if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
					diagram.connectOpenChain(2)				

					#### 2 ⇐ [3] // dc_5, dc_41
					if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(2)				
															
						##### 2 ⇐ [4] // dc_5
						if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
							diagram.connectOpenChain(2)									
							bt(lvl+1, offset+(10-11), path+[(0, '[5]')])
							diagram.revertOpenChain() 
						##### 2 ⇐ [4]
						
						##### 3 ⇐ [4] // dc_41
						if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
							diagram.connectOpenChain(3)
							bt(lvl+1, offset+(11-11), path+[(1, '[4∘1]')])
							diagram.revertOpenChain() 
						##### 3 ⇐ [4]

						diagram.revertOpenChain() 
					#### 2 ⇐ [3]

					#### 3 ⇐ [3] // dc_32
					if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(3)				
															
						##### 2 ⇐ [4] // dc_32
						if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
							diagram.connectOpenChain(2)									
							bt(lvl+1, offset+(11-11), path+[(2, '[3∘2]')])
							diagram.revertOpenChain() 
						##### 2 ⇐ [4]

						diagram.revertOpenChain() 
					#### 3 ⇐ [3]

					diagram.revertOpenChain() 
				### 2 ⇐ [2]
				
				### 3 ⇐ [2] // dc_23
				if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
					diagram.connectOpenChain(3)				

					#### 2 ⇐ [3] // dc_23
					if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(2)				
															
						##### 2 ⇐ [4] // dc_23
						if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
							diagram.connectOpenChain(2)									
							bt(lvl+1, offset+(11-11), path+[(3, '[2∘3]')])
							diagram.revertOpenChain() 
						##### 2 ⇐ [4]
						
						diagram.revertOpenChain() 
					#### 2 ⇐ [3]

					diagram.revertOpenChain() 
				### 3 ⇐ [2]

				diagram.revertOpenChain() 
			## 2 ⇐ [1]

			## 3 ⇐ [1] // dc_14
			if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
				diagram.connectOpenChain(3)
				
				### 2 ⇐ [2] // dc_14
				if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
					diagram.connectOpenChain(2)				

					#### 2 ⇐ [3] // dc_14
					if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(2)				
															
						##### 2 ⇐ [4] // dc_14
						if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
							diagram.connectOpenChain(2)									
							bt(lvl+1, offset+(11-11), path+[(4, '[1∘4]')])
							diagram.revertOpenChain() 
						##### 2 ⇐ [4]

						diagram.revertOpenChain() 
					#### 2 ⇐ [3]

					diagram.revertOpenChain() 
				### 2 ⇐ [2]

				diagram.revertOpenChain() 
			## 3 ⇐ [1]

			diagram.revertOpenChain() 
		# 2 ⇐ [0]

		# 3 ⇐ [0] // dc_05, dc_041, dc_032, dc_023, dc_014
		if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
			diagram.connectOpenChain(3)		
			
			## 2 ⇐ [1] // dc_05, dc_041, dc_032, dc_023
			if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
				diagram.connectOpenChain(2)
				
				### 2 ⇐ [2] // dc_05, dc_041, dc_032
				if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
					diagram.connectOpenChain(2)				

					#### 2 ⇐ [3] // dc_05, dc_041
					if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(2)				
															
						##### 2 ⇐ [4] // dc_05
						if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
							diagram.connectOpenChain(2)									
							bt(lvl+1, offset+(11-11), path+[(5, '[∘5]')])
							diagram.revertOpenChain() 
						##### 2 ⇐ [4]
						
						##### 3 ⇐ [4] // dc_041
						if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
							diagram.connectOpenChain(3)
							bt(lvl+1, offset+(12-11), path+[(6, '[∘4∘1]')])
							diagram.revertOpenChain() 
						##### 3 ⇐ [4]

						diagram.revertOpenChain() 
					#### 2 ⇐ [3]

					#### 3 ⇐ [3] // dc_032
					if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(3)				
															
						##### 2 ⇐ [4] // dc_032
						if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
							diagram.connectOpenChain(2)									
							bt(lvl+1, offset+(12-11), path+[(7, '[∘3∘2]')])
							diagram.revertOpenChain() 
						##### 2 ⇐ [4]

						diagram.revertOpenChain() 
					#### 3 ⇐ [3]

					diagram.revertOpenChain() 
				### 2 ⇐ [2]
				
				### 3 ⇐ [2] // dc_023
				if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
					diagram.connectOpenChain(3)				

					#### 2 ⇐ [3] // dc_023
					if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(2)				
															
						##### 2 ⇐ [4] // dc_023
						if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
							diagram.connectOpenChain(2)									
							bt(lvl+1, offset+(12-11), path+[(8, '[∘2∘3]')])
							diagram.revertOpenChain() 
						##### 2 ⇐ [4]
						
						diagram.revertOpenChain() 
					#### 2 ⇐ [3]

					diagram.revertOpenChain() 
				### 3 ⇐ [2]

				diagram.revertOpenChain() 
			## 2 ⇐ [1]

			## 3 ⇐ [1] // dc_014
			if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
				diagram.connectOpenChain(3)
				
				### 2 ⇐ [2] // dc_014
				if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
					diagram.connectOpenChain(2)				

					#### 2 ⇐ [3] // dc_014
					if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(2)				
															
						##### 2 ⇐ [4] // dc_014
						if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
							diagram.connectOpenChain(2)									
							bt(lvl+1, offset+(12-11), path+[(9, '[∘1∘4]')])
							diagram.revertOpenChain() 
						##### 2 ⇐ [4]

						diagram.revertOpenChain() 
					#### 2 ⇐ [3]

					diagram.revertOpenChain() 
				### 2 ⇐ [2]

				diagram.revertOpenChain() 
			## 3 ⇐ [1]

			diagram.revertOpenChain() 
		# 3 ⇐ [0]
		
		# 4 ⇐ [0] // dc_x5
		# if diagram.openChain.tailNode.links[4].next.cycle.chain != diagram.openChain:
		# 	diagram.connectOpenChain(4)		
		# 
			## 2 ⇐ [1] // dc_x5
		# 	if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
		# 		diagram.connectOpenChain(2)
		# 
				### 2 ⇐ [2] // dc_x5
		# 		if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
		# 			diagram.connectOpenChain(2)				
		# 
					#### 2 ⇐ [3] // dc_x5
		# 			if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
		# 				diagram.connectOpenChain(2)				
		# 
						##### 2 ⇐ [4] // dc_x5
		# 				if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
		# 					diagram.connectOpenChain(2)									
		# 					bt(lvl+1, offset+(12-11), path+[('+', '[+5]')])
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
	
	bt()	
	
	# assert dc_14()
	# assert dc_23()
	# assert dc_32()
	# assert dc_41()
	# assert dc_14()
	
	# diagram.openChain = diagram.nodeByAddress['000420'].prevs[3].node.links[1].next.prevs[2].node.cycle.chain
	# diagram.openChain.isOpen = True
	# diagram.openChain.tailNode = diagram.nodeByAddress['000420'].prevs[3].node.links[1].next.prevs[2].node
	# 
	# assert dc_14()	

	# diagram.openChain = diagram.nodeByAddress['001310'].prevs[3].node.cycle.chain
	# diagram.openChain.isOpen = True
	# diagram.openChain.tailNode = diagram.nodeByAddress['001310'].prevs[3].node
	# 
	# assert dc_05()
	# assert dc_14()

			
	# diagram.openChain = diagram.nodeByAddress['000406'].cycle.chain
	# diagram.openChain.isOpen = True
	# diagram.openChain.tailNode = diagram.nodeByAddress['000406']
	# 
	# assert dc_5()
	
																			
	# 
	# assert dc_23()
	# assert dc_32()
	# assert dc_41()
	# assert dc_5()
	# assert dc_41()
	# assert dc_14()
	# 
	# assert dc_23()
	# assert dc_32()
	# assert dc_41()
	# assert dc_14()			
	# dc_32()
	# dc_41()
	# dc_5()
	# dc_05()
	# dc_14()
	# dc_05()
	# dc_14()
	# dc_23()
	# dc_32()	
	# dc_23()
	# dc_32()	
	# dc_41()
	# dc_5()
	# 
	# dc_x5()
	# dc_14()
	# dc_23()
	# dc_32()
	# dc_41()
	# dc_32()
	# dc_41()
	# dc_5()	
	# dc_05()	
	# dc_14()
	# dc_05()	
	# dc_14()
	# assert dc_23()				
	'''
[show] chains: 691 | connected cycles: 30 | links: ℓ₁x180 ℓ₂x25 ℓ₃x4 ℓ₄x0 | total: 242 | final: 5907.0	
[   6][lvl:5] off: -1 § 43210
[1∘4][2∘3][3∘2][4∘1][5]	
| current min off: -1  |  » ∘ «

[show] chains: 631 | connected cycles: 90 | links: ℓ₁x540 ℓ₂x74 ℓ₃x15 ℓ₄x0 | total: 733 | final: 5906.0
[  20][lvl:17] off: -2 § 43212105454323210
[1∘4][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][5]
| current min off: -2  |  » ∘ «
	
[show] chains: 571 | connected cycles: 150 | links: ℓ₁x900 ℓ₂x123 ℓ₃x26 ℓ₄x0 | total: 1224 | final: 5905.0	
[  34][lvl:29] off: -3 § 43212105454323212105454323210
[1∘4][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][5]
| current min off: -3  |  » ∘ «

[show] chains: 471 | connected cycles: 250 | links: ℓ₁x1500 ℓ₂x204 ℓ₃x45 ℓ₄x0 | total: 2043 | final: 5904.0
[  56][lvl:49] off: -4 § 4321210545432321210545432321210545435432432343210
[1∘4][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][∘5][1∘4][2∘3][3∘2][1∘4][2∘3][3∘2][2∘3][1∘4][2∘3][3∘2][4∘1][5]
| current min off: -4  |  » ∘ «
			
[show] chains: 381 | connected cycles: 340 | links: ℓ₁x2040 ℓ₂x276 ℓ₃x63 | total: 2781 | final: 5904.0	
[160968][lvl:67] off: -4 § 4321210545432321210545432321210545437107132107132107107105454323210
[1∘4][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][∘3∘2][4∘1][5][∘3∘2][4∘1][2∘3][3∘2][4∘1][5][∘3∘2][4∘1][2∘3][3∘2][4∘1][5][∘3∘2][4∘1][5][∘3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][5]  |  » ∘ «	
| current min off: -4

[show] chains: 411 | connected cycles: 310 | links: ℓ₁x1860 ℓ₂x252 ℓ₃x57 | total: 2535 | final: 5904.0
[227609][lvl:61] off: -4 § 4321210545432321210545432321210545437107132123212105454323210
[1∘4][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][∘3∘2][4∘1][5][∘3∘2][4∘1][2∘3][3∘2][4∘1][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][5]  |  » ∘ «
| current min off: -4
	'''
	
	show(diagram)	
