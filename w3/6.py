from diagram import *
from uicanvas import *


if __name__ == "__main__":

	diagram = Diagram(6)

	def dc(path):
		if not diagram.connectOpenChain(path[0]):
			return False
		if not diagram.connectOpenChain(path[1]):
			diagram.revertOpenChain()
			return False
		if not diagram.connectOpenChain(path[2]):
			diagram.revertOpenChain()
			diagram.revertOpenChain()
			return False
		if not diagram.connectOpenChain(path[3]):
			diagram.revertOpenChain()
			diagram.revertOpenChain()
			diagram.revertOpenChain()								
			return False
		return True

	def dc_013():
		return dc([3,3,2,2])
	dc_013.__setattr__('path', '[∘1∘3]')
	dc_013.__setattr__('size', 10)
	
	def dc_022():
		return dc([3,2,3,2])
	dc_022.__setattr__('path', '[∘2∘2]')
	dc_022.__setattr__('size', 10)
						
	def dc_031():
		return dc([3,2,2,3])
	dc_031.__setattr__('path', '[∘3∘1]')			
	dc_031.__setattr__('size', 10)
		
	def dc_04():
		return dc([3,2,2,2])
	dc_04.__setattr__('path', '[∘4]')
	dc_04.__setattr__('size', 9)
						
	def dc_13():		
		return dc([2,3,2,2])
	dc_13.__setattr__('path', '[1∘3]')
	dc_13.__setattr__('size', 9)
		
	def dc_22():
		return dc([2,2,3,2])
	dc_22.__setattr__('path', '[2∘2]')	
	dc_22.__setattr__('size', 9)
		
	def dc_31():
		return dc([2,2,2,3])
	dc_31.__setattr__('path', '[3∘1]')	
	dc_31.__setattr__('size', 9)
		
	def dc_4():
		return dc([2,2,2,2])
	dc_4.__setattr__('path', '[4]')	
	dc_4.__setattr__('size', 8)

	max_lvl_reached = 27
	min_off_reached = 0

	btcc = 0
	def bt(lvl=0, offset=0, path=[]):
		global btcc, max_lvl_reached, min_off_reached
		
		# kill early
		if offset	> 3:
			return
				
		# path = [(function index, function path), … ]
		if btcc % 1000 == 0:
			print(f"[{btcc:>4}][lvl:{lvl}] off: {offset} § {''.join([str(x) for x,p in path])}") # + '\n' + ''.join([p for x,p in path]))
		btcc += 1		
		
		if lvl > max_lvl_reached:
			max_lvl_reached = lvl
			show(diagram)
			input2(f"| current max lvl: {max_lvl_reached}")

		if offset < min_off_reached:
			min_off_reached = offset
			show(diagram)
			input2(f"| current min off: {min_off_reached}")
							
		# 2 ⇐ [0] // dc_4, dc_31, dc_22, dc_13
		if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
			diagram.connectOpenChain(2)		
			
			## 2 ⇐ [1] // dc_4, dc_31, dc_22
			if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
				diagram.connectOpenChain(2)
				
				### 2 ⇐ [2] // dc_4, dc_31
				if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
					diagram.connectOpenChain(2)				
					
					#### 2 ⇐ [3] // dc_4
					if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(2)									
						bt(lvl+1, offset+(8-9), path+[(0, '[4]')])
						diagram.revertOpenChain() 
					#### 2 ⇐ [3]
					
					#### 3 ⇐ [3] // dc_31
					if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(3)
						bt(lvl+1, offset+(9-9), path+[(1, '[3∘1]')])
						diagram.revertOpenChain() 
					#### 3 ⇐ [3]
												
					diagram.revertOpenChain() 
				### 2 ⇐ [2]
					
				### 3 ⇐ [2] // dc_22
				if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
					diagram.connectOpenChain(3)				
					
					#### 2 ⇐ [3] // dc_22
					if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(2)									
						bt(lvl+1, offset+(9-9), path+[(2, '[2∘2]')])
						diagram.revertOpenChain() 
					#### 2 ⇐ [3]
					
					diagram.revertOpenChain() 
				### 3 ⇐ [2]									
					
				diagram.revertOpenChain() 
			## 2 ⇐ [1]
			
			## 3 ⇐ [1] // dc_13
			if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
				diagram.connectOpenChain(3)
				
				### 2 ⇐ [2] // dc_13
				if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
					diagram.connectOpenChain(2)				
					
					#### 2 ⇐ [3] // dc_13
					if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(2)									
						bt(lvl+1, offset+(9-9), path+[(3, '[1∘3]')])
						diagram.revertOpenChain() 
					#### 2 ⇐ [3]
					
					diagram.revertOpenChain() 
				### 2 ⇐ [2]													
				
				diagram.revertOpenChain() 
			## 3 ⇐ [1]
										
			diagram.revertOpenChain() 
		# 2 ⇐ [0]
		
		# 3 ⇐ [0] // dc_04, dc_031, dc_022, dc_013
		if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
			diagram.connectOpenChain(3)

			## 2 ⇐ [1] // dc_04, dc_031, dc_022
			if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
				diagram.connectOpenChain(2)

				### 2 ⇐ [2] // dc_04, dc_031
				if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
					diagram.connectOpenChain(2)

					#### 2 ⇐ [3] // dc_04
					if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(2)									
						bt(lvl+1, offset+(9-9), path+[(4, '[∘4]')])
						diagram.revertOpenChain() 
					#### 2 ⇐ [3]
					
					#### 3 ⇐ [3] // dc_031
					if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(3)
						bt(lvl+1, offset+(10-9), path+[(5, '[∘3∘1]')])
						diagram.revertOpenChain() 
					#### 3 ⇐ [3]
												
					diagram.revertOpenChain() 
				### 2 ⇐ [2]
				
				### 3 ⇐ [2] // dc_022
				if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
					diagram.connectOpenChain(3)				
					
					#### 2 ⇐ [3] // dc_022
					if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(2)									
						bt(lvl+1, offset+(10-9), path+[(6, '[∘2∘2]')])
						diagram.revertOpenChain() 
					#### 2 ⇐ [3]
					
					diagram.revertOpenChain() 
				### 3 ⇐ [2]														
					
				diagram.revertOpenChain() 
			## 2 ⇐ [1]

			## 3 ⇐ [1] // dc_013
			if diagram.openChain.tailNode.links[3].next.cycle.chain != diagram.openChain:
				diagram.connectOpenChain(3)
				
				### 2 ⇐ [2] // dc_013
				if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
					diagram.connectOpenChain(2)				
					
					#### 2 ⇐ [3] // dc_013
					if diagram.openChain.tailNode.links[2].next.cycle.chain != diagram.openChain:
						diagram.connectOpenChain(2)									
						bt(lvl+1, offset+(10-9), path+[(7, '[∘1∘3]')])
						diagram.revertOpenChain() 
					#### 2 ⇐ [3]
					
					diagram.revertOpenChain() 
				### 2 ⇐ [2]													
				
				diagram.revertOpenChain() 
			## 3 ⇐ [1]
													
			diagram.revertOpenChain() 
		# 3 ⇐ [0]
															
	print("\n\n -------------- \n\n")

	# bt()

	r = dc_13()
	r = dc_22()
	r = dc_31()
	r = dc_4()
	# r = dc_31()
	# r = dc_4()
	# r = dc_022()
	# r = dc_4()
	# r = dc_022()
	# r = dc_04()
							
	# diagram.connectOpenChain(2)
	# diagram.connectOpenChain(2)
	# diagram.revertOpenChain()
	
	# dc_13()
	# dc_22()
	# dc_31()
	# dc_22()
	# dc_13()
	# dc_22()
	# dc_13()
	# dc_22()
	# dc_31()
	# dc_4()
	# dc_022()
	# dc_31()
	# dc_13()
	# r = dc_4()
	# assert dc_031()
	# 
	# diagram.connectOpenChain(3)
	# 
	# 
	show(diagram)
	if not r:
		print("--- failed last command ---")
