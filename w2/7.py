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
	
	max_lvl_reached = 106
	min_off_reached = 0

	btcc = 0
	def bt(lvl=0, offset=0, path=[]):
		global btcc, max_lvl_reached, min_off_reached
		
		# kill early
		if offset	> 1:
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
									
	print("\n\n -------------- \n\n")
				
	bt()	
	
	# 
	# dc_14()
	# dc_23()
	# dc_32()
	# dc_41()
	# dc_5()
	# 
	# 
	# show(diagram)	
