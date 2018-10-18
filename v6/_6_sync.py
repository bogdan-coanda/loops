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
					
									
	results = defaultdict(int)		
	zeroes = []
	
	startTime = time()
	extend('000001')
	
	avloops = [l for l in diagram.loops if l.availabled]
	avlen = len(avloops)
	print("avlen: " + str(avlen))
	
	for i0 in range(avlen):
		loop0 = avloops[i0]		
		diagram.extendLoop(loop0)
				
		for i1 in range(i0+1, avlen):
			loop1 = avloops[i1]
			if loop1.availabled:
				diagram.extendLoop(loop1)
				
				for i2 in range(i1+1, avlen): 
					loop2 = avloops[i2]
					if loop2.availabled:
						diagram.extendLoop(loop2)						
						singles = single()
						
						if diagram.pointer_avlen == 0:
							zeroes.append((loop0.firstAddress(), loop1.firstAddress(), loop2.firstAddress()))
							
						'''
						if diagram.pointer_avlen == 0:
							results[(0, 0, -len(singles))] += 1
						else:
							results[(len([l for l in avloops if l.availabled]), diagram.pointer_avlen, -len(singles))] += 1
						'''
						
						if i2 % 300 == 0:
							print("["+tstr(time() - startTime)+"] @ " + str(i0) + " " + str(i1) + " " + str(i2) + " /" + str(avlen))	
	
						for l in reversed(singles):
							diagram.collapseBack(l)		
										
						diagram.collapseBack(loop2)
				diagram.collapseBack(loop1)
		diagram.collapseBack(loop0)
		'''
		with open("_7sync4results.txt", 'a') as log:
			for k,v in results.items():
				log.write(str(k) + " : " + str(v) + "\n")
		results.clear()
		'''
		with open("_7sync4zeroes.txt", 'a') as log:
			log.write("=== i0: " + str(i0) + " | " + str(len(zeroes)) + " ===\n")			
			for addrs in zeroes:
				log.write(" ".join(addrs) + "\n")
		zeroes.clear()
			
		# log.write(str(0 if diagram.pointer_avlen is 0 else len([l for l in avloops if l.availabled])) + " " + str(diagram.pointer_avlen) + " " + str(-len(singles)) + " " + loop0.firstAddress() + " " + loop1.firstAddress() + " " + loop2.firstAddress() + "\n")		
			
	print("["+tstr(time() - startTime)+"][trial] »»» ---")
	with open("_7sync4results.txt", 'r') as log:
		lines = log.read().splitlines()
		for line in lines:
			key = tuple(int(x) for x in line.split(" : ")[0][1:-1].split(", "))
			val = int(lines[0].split(" : ")[1])
			results[key] += val
		
	grouped = sorted(results.items())
	#diagram.pointers = [diagram.nodeByAddress[addr] for addr in set(chain(*grouped[0][1]))]
	show(diagram)
	print("["+tstr(time() - startTime)+"](availabled | pointer_avlen | -singles): loop_count\n" + "\n".join(str(g[0])+": "+str(g[1]) for g in grouped))				
