from diagram import *
from uicanvas import *
from common import *
import itertools


def patch(diagram):
	
	diagram.makeChain([], [diagram.cycleByAddress['0100']])
	diagram.extendLoop(diagram.nodeByAddress['01005'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['0110']])
	diagram.extendLoop(diagram.nodeByAddress['01105'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['0120']])
	diagram.extendLoop(diagram.nodeByAddress['01205'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['0130']])
	diagram.extendLoop(diagram.nodeByAddress['01305'].loop)
	
	diagram.nodeByAddress['01045'].nextLink = diagram.nodeByAddress['01045'].links[3]
	diagram.nodeByAddress['01145'].nextLink = diagram.nodeByAddress['01145'].links[3]
	diagram.nodeByAddress['01245'].nextLink = diagram.nodeByAddress['01245'].links[3]
	diagram.nodeByAddress['01345'].nextLink = diagram.nodeByAddress['01345'].links[3]

	diagram.makeChain([diagram.cycleByAddress[addr].chain for addr in ['0100', '0110', '0120', '0130']], [])	
	
	
	
	diagram.makeChain([], [diagram.cycleByAddress['0200']])
	diagram.extendLoop(diagram.nodeByAddress['02005'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['0210']])
	diagram.extendLoop(diagram.nodeByAddress['02105'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['0220']])
	diagram.extendLoop(diagram.nodeByAddress['02205'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['0230']])
	diagram.extendLoop(diagram.nodeByAddress['02305'].loop)
	
	diagram.nodeByAddress['02045'].nextLink = diagram.nodeByAddress['02045'].links[3]
	diagram.nodeByAddress['02145'].nextLink = diagram.nodeByAddress['02145'].links[3]
	diagram.nodeByAddress['02245'].nextLink = diagram.nodeByAddress['02245'].links[3]
	diagram.nodeByAddress['02345'].nextLink = diagram.nodeByAddress['02345'].links[3]

	diagram.makeChain([diagram.cycleByAddress[addr].chain for addr in ['0200', '0210', '0220', '0230']], [])
	
	diagram.nodeByAddress['00345'].nextLink = Link(4, diagram.nodeByAddress['00345'], diagram.nodeByAddress['01000'])
	diagram.nodeByAddress['01345'].nextLink = Link(4, diagram.nodeByAddress['01345'], diagram.nodeByAddress['02000'])
	diagram.nodeByAddress['02345'].nextLink = Link(4, diagram.nodeByAddress['02345'], diagram.nodeByAddress['00000'])
	
	diagram.makeChain(list(diagram.chains), [])
	
	# every cycle has its own chain at start
	#for cycle in diagram.cycles:
		#if cycle.chain is None:
			#diagram.makeChain([], [cycle])		
			
			

def poex(diagram, addrs):
	nodes = [diagram.nodeByAddress[addr] for addr in addrs]
	for node in nodes:
		assert diagram.extendLoop(node.loop)
	diagram.pointers = nodes
			


if __name__ == "__main__":
	
	with open('sols.6.txt', 'r') as file:
		lines = file.read().splitlines()
		
	print(len(lines))

	diagram = Diagram(6)
					
	sols = []
	for id in range(36):
		sols.append(sorted([diagram.nodeByAddress[addr].loop.firstNode().address for addr in lines[id*5+2].split('addr: ')[1].split(' ')]))
	sols = sorted(sols)
	
	'''	
	for i in range(6):
		for j in range(6):
			if i < j:
				print(i,j,set(sols[i]).intersection(sols[j]))
	#'''
		
	patch(diagram)
	
	diagram.extendLoop(diagram.nodeByAddress['00001'].loop)
	diagram.extendLoop(diagram.nodeByAddress['02302'].loop)
	diagram.extendLoop(diagram.nodeByAddress['01033'].loop)

	#poex(diagram, '11005 11105 11205 11305'.split(' '))
	#poex(diagram, '10012 10022 10003'.split(' '))
	#poex(diagram, '10012 10022 10031'.split(' '))
	#poex(diagram, '10111 12105 10201'.split(' '))
	#poex(diagram, '10111 12105 12005'.split(' '))
	#poex(diagram, '10105 12022 11031'.split(' '))
	#poex(diagram, '10105 12022 11005'.split(' '))
	
	#show(diagram)
	#input('[xxx]')

	'''	
	diagram.extendLoop(diagram.nodeByAddress['10012'].loop) # - |	
	diagram.extendLoop(diagram.nodeByAddress['10022'].loop) # - | 
	diagram.extendLoop(diagram.nodeByAddress['11305'].loop) # - |	BC:s ⋂ F:t	
	diagram.extendLoop(diagram.nodeByAddress['12305'].loop) # - |	BC:s ⋂ D:t
	
	#diagram.extendLoop(diagram.nodeByAddress['10143'].loop) # - |
	#diagram.extendLoop(diagram.nodeByAddress['10233'].loop) # - |
	#diagram.extendLoop(diagram.nodeByAddress['11013'].loop) # - |
	#diagram.extendLoop(diagram.nodeByAddress['12004'].loop) # - |
	#'''
	''' sol B|#0 | sol: 00001 01033 02302 | 10012 10022 : 10143 10233 11013 11305 12004 12305 | 10003 : 10030 10120 10210
	diagram.extendLoop(diagram.nodeByAddress['10003'].loop) # x | 
	diagram.extendLoop(diagram.nodeByAddress['10030'].loop) # x | B:t ⋂ EF:s
	
	#diagram.extendLoop(diagram.nodeByAddress['10120'].loop) # x | -- B:t ⋂ AD:s
	#diagram.extendLoop(diagram.nodeByAddress['10210'].loop) # x | -- B:t ⋂ A:t
	#'''
	''' sol C|#1 | sol: 00001 01033 02302 | 10012 10022 : 10143 10233 11013 11305 12004 12305 | 10031 : 10004 11022 12013
	diagram.extendLoop(diagram.nodeByAddress['10031'].loop) # x | 
	diagram.extendLoop(diagram.nodeByAddress['10004'].loop) # x |	C:t ⋂ AD:s
	
	#diagram.extendLoop(diagram.nodeByAddress['11022'].loop) # x | -- C:t ⋂ E:t	
	#diagram.extendLoop(diagram.nodeByAddress['12013'].loop) # x | -- C:t ⋂ EF:s
	#'''
	
	
	''' 
	diagram.extendLoop(diagram.nodeByAddress['10111'].loop) # - |
	diagram.extendLoop(diagram.nodeByAddress['12105'].loop) # - |	
	diagram.extendLoop(diagram.nodeByAddress['10004'].loop) # - | AD:s ⋂ C:t
	diagram.extendLoop(diagram.nodeByAddress['11004'].loop) # - |	AD:s ⋂ E:t

	#diagram.extendLoop(diagram.nodeByAddress['10120'].loop) # - |
	#diagram.extendLoop(diagram.nodeByAddress['10143'].loop) # - |
	#diagram.extendLoop(diagram.nodeByAddress['10305'].loop) # - |				
	#diagram.extendLoop(diagram.nodeByAddress['11205'].loop) # - |
	#'''
	''' sol A|#2 | sol: 00001 01033 02302 | 10111 12105 : 10004 10120 10143 10305 11004 11205 | 10201 : 10210 10233 10242
	diagram.extendLoop(diagram.nodeByAddress['10201'].loop) # x | 
	diagram.extendLoop(diagram.nodeByAddress['10242'].loop) # x |	A:t ⋂ EF:s
	
	#diagram.extendLoop(diagram.nodeByAddress['10210'].loop) # x |
	#diagram.extendLoop(diagram.nodeByAddress['10233'].loop) # x |
	#'''	
	''' sol D|#3 | sol: 00001 01033 02302 | 10111 12105 : 10004 10120 10143 10305 11004 11205 | 12005 : 10205 11105 12305
	diagram.extendLoop(diagram.nodeByAddress['12005'].loop) # x |	
	diagram.extendLoop(diagram.nodeByAddress['12305'].loop) # x | D:t ⋂ BC:s
	
	#diagram.extendLoop(diagram.nodeByAddress['10205'].loop) # x |
	#diagram.extendLoop(diagram.nodeByAddress['11105'].loop) # x |	
	#'''					
	
	
	'''
	diagram.extendLoop(diagram.nodeByAddress['10105'].loop) # - | 
	diagram.extendLoop(diagram.nodeByAddress['12022'].loop) # - |		
	diagram.extendLoop(diagram.nodeByAddress['10030'].loop) # - | EF:s ⋂ B:t
	diagram.extendLoop(diagram.nodeByAddress['10242'].loop) # - | EF:s ⋂ A:t
	
	#diagram.extendLoop(diagram.nodeByAddress['10205'].loop) # - |
	#diagram.extendLoop(diagram.nodeByAddress['10305'].loop) # - |
	#diagram.extendLoop(diagram.nodeByAddress['12004'].loop) # - |	
	#diagram.extendLoop(diagram.nodeByAddress['12013'].loop) # - |		
	#'''
	''' sol E|#4 | sol: 00001 01033 02302 | 10105 12022 : 10030 10205 10242 10305 12004 12013 | 11031 : 11004 11013 11022 	
	diagram.extendLoop(diagram.nodeByAddress['11031'].loop) # x |
	diagram.extendLoop(diagram.nodeByAddress['11004'].loop) # x | E:t ⋂ AD:s
		
	#diagram.extendLoop(diagram.nodeByAddress['11013'].loop) # x | 
	#diagram.extendLoop(diagram.nodeByAddress['11022'].loop) # x |
	#'''
	''' sol F|#5 | sol: 00001 01033 02302 | 10105 12022 : 10030 10205 10242 10305 12004 12013 |  11005 : 11105 11205 11305
	diagram.extendLoop(diagram.nodeByAddress['11005'].loop) # x | 
	diagram.extendLoop(diagram.nodeByAddress['11305'].loop) # x | F:t ⋂ BC:s
		
	#diagram.extendLoop(diagram.nodeByAddress['11105'].loop) # x |
	#diagram.extendLoop(diagram.nodeByAddress['11205'].loop) # x |
	#'''
					
	min_chain = sorted(diagram.chains, key = lambda chain: len(chain.avloops))[0]
	chloops = sorted(sorted(diagram.chains, key = lambda chain: len(chain.avloops))[0].avloops, key = lambda loop: loop.firstNode().address)
	#diagram.pointers = itertools.chain(*[loop.nodes for loop in chloops]) if len(chloops) else [cycle.avnode() for cycle in min_chain.cycles]
	show(diagram)
	input("chloops: " + str(chloops))
	
	'''
	BC:s ⋂ A:t = { 10233 }
	BC:s ⋂ D:t = { 12305 }
	BC:s ⋂ E:t = { 11013 }
	BC:s ⋂ F:t = { 11305 }	
	BC:s ⋂ AD:s = { 10143 }	
	BC:s ⋂ EF:s = { 12004 }	
	AD:s ⋂ EF:s = { 10305 }
	A:t ⋂ EF:s = { 10242 }
	D:t ⋂ EF:s = { 10205 }
	B:t ⋂ EF:s = { 10030 }
	C:t ⋂ EF:s = { 12013 }
	AD:s ⋂ C:t = { 10004 }
	AD:s ⋂ B:t = { 10120 }
	E:t ⋂ AD:s = { 11004 }
	F:t ⋂ AD:s = { 11205 }
	
	D:t ⋂ F:t = { 11105 }
	B:t ⋂ A:t = { 10210 }	
	C:t ⋂ E:t = { 11022 }
	'''		
		
	for id, sol in enumerate(sols[0:6]):
		
		𝒟 = Diagram(6)		
		patch(𝒟)
		
		for addr in sol:
			if addr[0] == '1':
				𝒟.extendLoop(𝒟.nodeByAddress[addr].loop)
				
		𝒟.pointers = [node for node in 𝒟.nodes if node.loop.availabled and node.cycle.chain and len(node.cycle.chain.cycles) is 1]
		show(𝒟)
		input("#" + str(id) + " | sol: " + str(" ".join(sol)))		


