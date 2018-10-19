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
	with open("_7sync4zeroessingled.txt", 'r') as log:
		lines = log.read().splitlines()
		for line in lines:
			if line.startswith("===") is False:
				zeroes.append(tuple(line.split(' ')[3:]))
				
	extend('000001')
	
	extend('013430')
	# 
	extend('100023')	
	# extend('100210')	
	# extend('100220')
	# 
	# extend('120343')
	
	# extend('100242')
	# extend('100243')
	
	singles = single()
		
	diagram.point()
	print("pointers: " + str(len(diagram.pointers)))
	show(diagram)
	print("singles: " + str(len(singles)))
	
	l1 = diagram.nodeByAddress['100242'].loop;
	l2 = diagram.nodeByAddress['100243'].loop;
	lq = diagram.nodeByAddress['120343'].loop;
			
	print("lq: " + str(lq))
	print("l1.killingField: " + str(l1.killingField()))
	print("l2.killingField: " + str(l2.killingField()))
	print("intersected: " + str(l1._killingField.intersection(l2._killingField)))
	
	# 6 | loops: 013152 100106 120154 | dead cycles: 10005

	# 7 | loops: 013251 100005 120253 | dead cycles: 10015

	# 0 | loops: 023152 113023 001303 | dead cycles: 11310	
	#11 | loops: 023152 113023 100102 | dead cycles: 11310
					
	# 3 | loops: 013134 120121 010354 | dead cycles: 10002
	# 4 | loops: 013134 120121 100206 | dead cycles: 10002
	# 5 | loops: 013134 120121 100342 | dead cycles: 10002
	# 1 | loops: 010033 103032 100342 | dead cycles: 10002	
		
	# 2 | loops: 013430 120343 010303 | dead cycles: 10024	
	# 8 | loops: 013430 120343 100023 | dead cycles: 10024
	# 9 | loops: 013430 120343 100210 | dead cycles: 10024
	#10 | loops: 013430 120343 100220 | dead cycles: 10024

	# ----------------------------------------------------	
	
	# 6 | loops: 013152 100106 120154 | dead cycles: 10005
	
	# 7 | loops: 013251 100005 120253 | dead cycles: 10015
	
	# 0 | loops: 001303 023152 113023 | dead cycles: 11310
	#11 | loops: 023152 100102 113023 | dead cycles: 11310
	
	# 3 | loops: 010354 013134 120121 | dead cycles: 10002
	# 4 | loops: 013134 100206 120121 | dead cycles: 10002
	# 5 | loops: 013134 100342 120121 | dead cycles: 10002
	# 1 | loops: 010033 100342 103032 | dead cycles: 10002
	
	# 2 | loops: 010303 013430 120343 | dead cycles: 10024
	# 8 | loops: 013430 100023 120343 | dead cycles: 10024
	# 9 | loops: 013430 100210 120343 | dead cycles: 10024
	#10 | loops: 013430 100220 120343 | dead cycles: 10024

	# ----------------------------------------------------	
	
	# 0 | loops: 001303 023152 113023 | dead cycles: 11310
	# 1 | loops: 010033 100342 103032 | dead cycles: 10002
	# 2 | loops: 010303 013430 120343 | dead cycles: 10024
	# 3 | loops: 010354 013134 120121 | dead cycles: 10002
	
	# 4 | loops: 013134 100206 120121 | dead cycles: 10002
	# 5 | loops: 013134 100342 120121 | dead cycles: 10002
	
	# 6 | loops: 013152 100106 120154 | dead cycles: 10005
	# 7 | loops: 013251 100005 120253 | dead cycles: 10015
	
	# 8 | loops: 013430 100023 120343 | dead cycles: 10024
	# 9 | loops: 013430 100210 120343 | dead cycles: 10024
	#10 | loops: 013430 100220 120343 | dead cycles: 10024
	
	#11 | loops: 023152 100102 113023 | dead cycles: 11310
																		
	#ordered = [6, 7, 0, 11, 3, 4, 5, 1, 2, 8, 9, 10]
				
	'''
	for index, addrs in enumerate(zeroes):
	#for index in ordered:
		#addrs = zeroes[index]
		
		for addr in addrs:
			extend(addr)
			
		singles = single()
			
		diagram.pointers = itertools.chain(*[chain.cycles for chain in diagram.chains if len(chain.avloops) == 0])			
		#show(diagram)		
		print("#" + str(index) + " | loops: " + " ".join(addrs) + " | dead cycles: " + " ".join([cycle.address for cycle in diagram.pointers]))	
		#input(str(index) + " | singles: " + str(len(singles)))
		
		for l in reversed(singles):
			diagram.collapseBack(l)
		
		
		for addr in reversed(addrs):
			collapse(addr)
	'''
	
