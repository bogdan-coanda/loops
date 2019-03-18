from diagram import *
from uicanvas import *
from time import time


step_id = 0
min_step_chains = 126


def step(lvl=0, path=[]):
	global step_id, min_step_chains
	
	def key():
		return f"[{step_id:>4}][{tstr(time() - startTime):>11}][lvl:{lvl}]"
		
	if step_id % 1000 == 0:
		print(f"{key()}[ch:{len(diagram.chains)}] {'.'.join([(str(x)+upper(t)) for x,t in path])}")
	step_id += 1

	if len(diagram.chains) == 1:
		show(diagram)
		input2(f"{key()} sol found.")
		return
		
	if len(diagram.chains) < min_step_chains:
		min_step_chains = len(diagram.chains)
		show(diagram)
		input2(f"{key()} min step chains: {min_step_chains} so far…")		
		
	min_chain = sorted(diagram.chains, key = lambda chain: (len(chain.avnodes), chain.id))[0]
	# print(f"{key()} chosen min: {min_chain}")
	
	seen = []
	
	# if len(min_chain.avnodes) > 1:	
	# 	loopResults = {}
	# 	for loop in diagram.loops:
	# 		if loop.available:
	# 			dead = False
	# 
	# 			assert diagram.extendLoop(loop)
	# 			result = min([len(ch.avnodes) for ch in diagram.chains])
	# 			if result == 0:
	# 				dead = True
	# 			else:
	# 				loopResults[loop] = result
	# 
	# 			diagram.collapseBack(loop)
	# 			if dead:
	# 				diagram.setLoopUnavailable(loop)
	# 				seen.append(loop)
	# 
		# if len(seen) > 0:
		# 	print(f"{key()} surviving loops: {len(loopResults)} | dead loops: {len(seen)}")
	# 
	# 	nextChainResults = []
	# 	for chain in list(diagram.chains):
	# 		nextChainResults.append((chain, sum([loopResults[n.loop] for n in chain.avnodes])))			
	# 	nextChainResults = sorted(nextChainResults, key = lambda cr: (cr[1], len(cr[0].avnodes), cr[0].id))
		# oldMinChainResult = [cr for cr in nextChainResults if cr[0] == min_chain][0][1]
		# if oldMinChainResult != nextChainResults[0][1]:
		# 	print(f"{key()} purging from min: {min_chain} with result: {oldMinChainResult} to min: {nextChainResults[0][0]} with result: {nextChainResults[0][1]}")
	# 	min_chain = nextChainResults[0][0]
		
	min_avlen = len(min_chain.avnodes)
	
	for i,n in enumerate(sorted(min_chain.avnodes, key = lambda n: n.address)):
		assert diagram.extendLoop(n.loop)		
		step(lvl+1, path+[(i, min_avlen)])
		diagram.collapseBack(n.loop)	
		
		seen.append(n.loop)
		diagram.setLoopUnavailable(n.loop)
		
	for l in reversed(seen):
		diagram.resetLoopAvailable(l)
		

if __name__ == "__main__":

	diagram = Diagram(7, kernelPath='')
	
	# diagram.setOpenChain('123450')
	# node = diagram.nodeByAddress['123316']
	# diagram.openChain = node.cycle.chain
	# diagram.openChain.isOpen = True
	# diagram.openChain.tailNode = node

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

	# pOc('3 22232 22223 22222')
	
	# cOc('32222')# 23222 22323 22222 32222 23222 22322')

	# paths: (0, '[5]') - (1, '[4∘1]') - (2, '[3∘2]') - (3, '[2∘3]') - (4, '[1∘4]') - (5, '[∘5]') - (6, '[∘4∘1]') - (7, '[∘3∘2]') - (8, '[∘2∘3]') - (9, '[∘1∘4]')
	
	#       4     3     2     4     3     2     3     2     1     0     6    =0     5=    4     5     4     3     2     3     2     1     3     2     1     0
	#     [1∘4] [2∘3] [3∘2] [1∘4] [2∘3] [3∘2] [2∘3] [3∘2] [4∘1]  [5] [∘4∘1]  [5]  [∘5]  [1∘4] [∘5]  [1∘4] [2∘3] [3∘2] [2∘3] [3∘2] [4∘1] [2∘3] [3∘2] [4∘1]  [5]
	#cOc('23222 22322 22232 23222 22322 22232 22322 22232 22223 22222 32223 22222 3 22222 32223 22222 32222 23222 22322 23222 22322 22232 23222 22322 22232 2222')	
	#cOc('23222 22322 22232 23222 22322 22232 22322 22232 22223 22222 32223 22222 32222 23222 32222 23222 22322 22232 22322 22232 22223 22322 22232 22223 22222')
	#  5   1|4		2|3		3|2   1|4	  2|3   3|2   2|3   3|2   4|1    5   |4|1 	  5   |5		1|4   |5    1|4   2|3   3|2   2|3   3|2   4|1   2|3   3|2		4|1		 5
	#     6     6     6     3     6     6     4     6     6     6       4    6         6     4     6      6     6     4     6     6     3     6     6     6	

			
	
	# [show] chains: 571 | connected cycles: 150 | links: ℓ₁x900 ℓ₂x123 ℓ₃x26 ℓ₄x0 | total: 1224 | final: 5905.0	
	# [  34][lvl:29] off: -3 § 43212105454323212105454323210
	# cOc('23222 22322 22232 22223 22232 22223 22222 32222 23222 32222 23222 22322 22232 22322 22232 22223 22232 22223 22222 32222 23222 32222 23222 22322 22232 22322 22232 22223 22222')
	#    [1∘4] [2∘3] [3∘2] [4∘1] [3∘2] [4∘1]  [5]  [∘5]  [1∘4] [∘5]  [1∘4] [2∘3] [3∘2] [2∘3] [3∘2] [4∘1] [3∘2] [4∘1]  [5]  [∘5]  [1∘4] [∘5]  [1∘4] [2∘3] [3∘2] [2∘3] [3∘2] [4∘1]  [5]	


	# [show] chains: 561 | connected cycles: 160 | links: ℓ₁x960 ℓ₂x131 ℓ₃x28 ℓ₄x0 | total: 1306 | final: 5905.0
	# [  37][lvl:31] off: -3 § 4321210545432321210545432321210
	# [1∘4][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5]


	# [show] chains: 381 | connected cycles: 340 | links: ℓ₁x2040 ℓ₂x276 ℓ₃x63 ℓ₄x0 | total: 2781 | final: 5904.0
	# [58831][lvl:67] off: -4 § 4321210545432321210545432321210545437107132107132107107105454323210
	# [1∘4][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][∘3∘2][4∘1][5][∘3∘2][4∘1][2∘3][3∘2][4∘1][5][∘3∘2][4∘1][2∘3][3∘2][4∘1][5][∘3∘2][4∘1][5][∘3∘2][4∘1][5][∘5][1∘4][∘5][1∘4][2∘3][3∘2][2∘3][3∘2][4∘1][5]
	# | current min off: -4  |  » ∘ «

	# cOc('22222 32222 23222 22322 32222 23222 22322 23222 22322 22232 22223 22232 2222-3-2222 23222 32222 23222 22322 22232 22322 22232 22223 22322 22232 22223 22222')
	#       [5]  [∘5]  [1∘4] [2∘3] [∘5]  [1∘4] [2∘3] [1∘4] [2∘3] [3∘2] [4∘1] [3∘2]  [4 -∘- 4]  [1∘4] [∘5]  [1∘4] [2∘3] [3∘2] [2∘3] [3∘2] [4∘1] [2∘3] [3∘2] [4∘1]  [5]
	
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
	# K                2     1     0     6     0     5     4     5     4     3     2     3     2     1     0
	#        «K»     [3∘2] [4∘1]  [5] [∘4∘1]  [5]  [∘5]  [1∘4] [∘5]  [1∘4] [2∘3] [3∘2] [2∘3] [3∘2] [4∘1]  [5]
	cOc('2232-2-2322 22232 22223 22222 32223 22222 32222 23222 32222 23222 22322 22232 22322 22232 22223 22222')
	pOc(list(reversed('22232 22223 22222 32223 22222 32222 23222 32222 23222 22322 22232 22322 22232 22223 22222')))
	
	
	startTime = time()
	step()			
		
	diagram.point()
	show(diagram)


	'''
	[1000][   0m0s.894][lvl:59][ch:276] 0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0².0².0².0².0².0².0².0².0².0².0².0².0².0².0².0³.0².0³.0².0².0².0¹.0¹.0².0².0².0².1².0².1².1².0².0².1².0².0².0¹.1².1².1².0¹.1².0².0¹.0¹.0¹.0¹.1².0¹	
	[1000][    1m23s.2][lvl:55][ch:296] 0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0⁴.0¹.0⁴.0¹.0⁴.0¹.0³.0³.0².0¹.0⁴.0².0¹.0⁴.0¹.0⁴.0¹.0³.0⁴.0¹.0¹.0¹.0².0¹.1².0¹.0³.0¹.0¹.0⁴.0².0³.0¹.0⁶.0¹.0¹.0³.0¹.0¹.1³.0¹.0¹.3⁴.0¹.0¹
	'''
	
