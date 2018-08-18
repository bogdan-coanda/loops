from diagram import *
from uicanvas import *
from common import *
import itertools


def patch(diagram):
	
	for head in ['01']:
								
		diagram.makeChain([], [diagram.cycleByAddress[head+'00']])
		diagram.extendLoop(diagram.nodeByAddress[head+'005'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'10']])
		diagram.extendLoop(diagram.nodeByAddress[head+'105'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'20']])
		diagram.extendLoop(diagram.nodeByAddress[head+'205'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'30']])
		diagram.extendLoop(diagram.nodeByAddress[head+'305'].loop)
		
		diagram.nodeByAddress[head+'045'].nextLink = diagram.nodeByAddress[head+'045'].links[3]
		diagram.nodeByAddress[head+'145'].nextLink = diagram.nodeByAddress[head+'145'].links[3]
		diagram.nodeByAddress[head+'245'].nextLink = diagram.nodeByAddress[head+'245'].links[3]
		diagram.nodeByAddress[head+'345'].nextLink = diagram.nodeByAddress[head+'345'].links[3]
		
	diagram.nodeByAddress['00345'].nextLink = Link(4, diagram.nodeByAddress['00345'], diagram.nodeByAddress['01000'])
	diagram.nodeByAddress['01345'].nextLink = Link(4, diagram.nodeByAddress['01345'], diagram.nodeByAddress['00000'])
	
	diagram.makeChain(list(diagram.chains), [])		
	
def extendAddress(addr):
	assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
		

if __name__ == "__main__":
	
	diagram = Diagram(6)#, withKernel=False)
	patch(diagram)
	
	'''
	# ⟨orange⟩
	extendAddress('00101')
	extendAddress('00133')
	extendAddress('00142')
			
	# ⟨left yellow⟩
	extendAddress('10030')
	extendAddress('10120')
	extendAddress('10210')
	extendAddress('10300')
	
	# ⟨right yellow⟩
	extendAddress('12030')
	extendAddress('12120')
	extendAddress('12210')
	extendAddress('12300')
	
	# ⟨fuchsia⟩
	extendAddress('12020')
	extendAddress('12110')
	extendAddress('12330')
	
	# ⟨top blue⟩
	# extendAddress('02045')
	# extendAddress('02145')
	# extendAddress('02345')
	
	# ⟨bot leftovers⟩
	# extendAddress('10140')
	# extendAddress('11045')
	# extendAddress('11300')	
					
	show(diagram)
	input()
	'''
	
	with open('sols.6.partial_2_4D.txt', 'r') as file:
		lines = file.read().splitlines()
		
	#print(len(lines))
					
	sols = []
	for id in range(len(lines)//5):
		addrs = lines[id*5+2].split('addr: ')[1].split(' ')
		sols.append(sorted([diagram.nodeByAddress[addr].loop.firstNode().address for addr in addrs]))
		
	sols = sorted(sols)

	ktypes = []
	for id, sol in enumerate(sols):
		ktypes.append(groupby(sol, K = lambda addr: diagram.nodeByAddress[addr].ktype, G = lambda g: len(g)))

	# for id, sol in enumerate(sols):
	# 	keys = ktypes[id]
	# 	print("@sol: " + str(id) + " | ktypes: " + str(keys))


	for id, sol in enumerate(sols):
		keys = ktypes[id]
		if 2 in keys and keys[2] >= 8:
		
			print("@sol: " + str(id) + " | blue: " + str(len([addr for addr in sol if addr.endswith('5')])))
		
			𝒟 = Diagram(6)		
			patch(𝒟)
			
			for addr in sol:
				𝒟.extendLoop(𝒟.nodeByAddress[addr].loop)
							
			#if 𝒟.nodeByAddress['10030'].loop.extended and not 𝒟.nodeByAddress['10120'].loop.extended and not 𝒟.nodeByAddress['10210'].loop.extended and not 𝒟.nodeByAddress['10300'].loop.extended and 𝒟.nodeByAddress['10040'].loop.extended and 𝒟.nodeByAddress['10140'].loop.extended and 𝒟.nodeByAddress['10240'].loop.extended:
			#if 𝒟.nodeByAddress['10030'].loop.extended and 𝒟.nodeByAddress['10120'].loop.extended and 𝒟.nodeByAddress['10210'].loop.extended and 𝒟.nodeByAddress['10300'].loop.extended:
			show(𝒟)
			input("#" + str(id) + " | keys: " + str(sorted(keys.items())))		
	
	print("done.")
	
	

