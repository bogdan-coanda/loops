from diagram import *
from uicanvas import *
from common import *
from itertools import chain
from time import time
from collections import defaultdict

if __name__ == "__main__":
	
	diagram = Diagram(7, 4)
	
	def extend(addr):
		assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	def collapse(addr):
		diagram.collapseBack(diagram.nodeByAddress[addr].loop)
	def single():
		singles = []
		diagram.pointer_avlen = diagram.spClass
		while True:
			found = False
			for chain in diagram.chains:
				avlen = len(chain.avloops)
				if avlen == 0:
					diagram.pointer_avlen = 0
					return singles
				elif avlen == 1:
					avloop = list(chain.avloops)[0]
					singles.append(avloop)
					diagram.extendLoop(avloop)					
					found = True
					break
				elif avlen < diagram.pointer_avlen:
					diagram.pointer_avlen = avlen
			if not found:
				return singles
				
	zeroes = []
	with open("_7sync4zeroes.txt", 'r') as log:
		lines = log.read().splitlines()
		for line in lines:
			if line.startswith("===") is False:
				zeroes.append(tuple(line.split(' ')))
				
	extend('000001')
	
	extend('103032')
	extend('100342')
	singles = single()
	
	#extend('010033')
	
	diagram.pointers = itertools.chain(*[chain.cycles for chain in diagram.chains if len(chain.avloops) == 0])			
	show(diagram)
	print("singles: " + str(len(singles)))
	
	# 6 | loops: 013152 100106 120154 | dead cycles: 10005
	
	# 7 | loops: 013251 100005 120253 | dead cycles: 10015

	# 0 | loops: 023152 113023 001303 | dead cycles: 11310
	#11 | loops: 023152 113023 100102 | dead cycles: 11310
			
	# 2 | loops: 013430 120343 010303 | dead cycles: 10024	
	# 8 | loops: 013430 120343 100023 | dead cycles: 10024
	# 9 | loops: 013430 120343 100210 | dead cycles: 10024
	#10 | loops: 013430 120343 100220 | dead cycles: 10024	
	
	# 1 | loops: 103032 100342 010033 | dead cycles: 10002
	#12 | loops: 103032 100342 120032 | dead cycles: 10002
	#13 | loops: 103032 100342 120121 | dead cycles: 10002	
	# 5 | loops: 013134 100342 120121 | dead cycles: 10002		
	# 4 | loops: 013134 100206 120121 | dead cycles: 10002
	# 3 | loops: 013134 010354 120121 | dead cycles: 10002
					
	'''				
	ordered = [6, 7, 2, 8, 9, 10, 0, 11, 1, 3, 4, 5, 12, 13]
			
	for order in ordered:
		
		addrs = zeroes[order]
		
		for addr in addrs:
			extend(addr)
			
		diagram.pointers = itertools.chain(*[chain.cycles for chain in diagram.chains if len(chain.avloops) == 0])			
		show(diagram)		
		input(order)
		
		# print("#" + str(order) + " | loops: " + " ".join(addrs) + " | dead cycles: " + " ".join([cycle.address for cycle in diagram.pointers]))
		
		for addr in reversed(addrs):
			collapse(addr)
	'''
