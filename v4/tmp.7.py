from diagram import *
from uicanvas import *
import itertools


def patch(diagram):
	
	for head in ['001', '002', '003']:
								
		diagram.makeChain([], [diagram.cycleByAddress[head+'00']])
		diagram.extendLoop(diagram.nodeByAddress[head+'006'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'10']])
		diagram.extendLoop(diagram.nodeByAddress[head+'106'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'20']])
		diagram.extendLoop(diagram.nodeByAddress[head+'206'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'30']])
		diagram.extendLoop(diagram.nodeByAddress[head+'306'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'40']])
		diagram.extendLoop(diagram.nodeByAddress[head+'406'].loop)	
		
		diagram.nodeByAddress[head+'056'].nextLink = diagram.nodeByAddress[head+'056'].links[3]
		diagram.nodeByAddress[head+'156'].nextLink = diagram.nodeByAddress[head+'156'].links[3]
		diagram.nodeByAddress[head+'256'].nextLink = diagram.nodeByAddress[head+'256'].links[3]
		diagram.nodeByAddress[head+'356'].nextLink = diagram.nodeByAddress[head+'356'].links[3]
		diagram.nodeByAddress[head+'456'].nextLink = diagram.nodeByAddress[head+'456'].links[3]
		
	diagram.nodeByAddress['000456'].nextLink = Link(4, diagram.nodeByAddress['000456'], diagram.nodeByAddress['001000'])
	diagram.nodeByAddress['001456'].nextLink = Link(4, diagram.nodeByAddress['001456'], diagram.nodeByAddress['002000'])
	diagram.nodeByAddress['002456'].nextLink = Link(4, diagram.nodeByAddress['002456'], diagram.nodeByAddress['003000'])
	diagram.nodeByAddress['003456'].nextLink = Link(4, diagram.nodeByAddress['003456'], diagram.nodeByAddress['000000'])
	
	diagram.makeChain(list(diagram.chains), [])		
	

def extendAddress(addr):
	assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
		
def extendColumn(column_addr, key):
	i = 0
	j = key
	while i < diagram.spClass-1:
		extendAddress(column_addr+str(i)+str(j))
		if j > 0:
			i += 1
			j -= 1
		else:
			i += 2
			j = diagram.spClass - 3

def point(diagram):
	diagram.pointers = []
		
	if len(diagram.chains) is 1 and len(list(diagram.chains)[0].cycles) is len(diagram.cycles):
		return
		
	cycle_avlen, smallest_cycle_group = (len(diagram.cycles), [])
	sorted_empty_cycles = sorted(groupby([cycle for cycle in diagram.cycles if cycle.chain is None], K = lambda cycle: len([n for n in cycle.nodes if n.loop.availabled])).items())
	if len(sorted_empty_cycles):
		cycle_avlen, smallest_cycle_group = sorted_empty_cycles[0]
	
	chain_avlen, smallest_chain_group = (len(diagram.cycles), [])
	sorted_chain_groups = sorted(groupby(diagram.chains, K = lambda chain: len(chain.avloops)).items())
	if len(sorted_chain_groups) > 0:
		chain_avlen, smallest_chain_group	= sorted_chain_groups[0]		

	min_avlen = min(cycle_avlen, chain_avlen)
	if min_avlen == cycle_avlen:
		diagram.pointers += [cycle.avnode() if min_avlen is not 0 else cycle for cycle in smallest_cycle_group]
	if min_avlen == chain_avlen:
		diagram.pointers += itertools.chain(*[[[n for n in loop.nodes if n.cycle.chain is chain][0] for loop in chain.avloops] if min_avlen is not 0 else chain.cycles for chain in smallest_chain_group])																				
	print("[pointing] cycle avlen: " + str(cycle_avlen) + " | chain avlen: " + str(chain_avlen))
									
def tonoavail(addr):
	loop = diagram.nodeByAddress[addr].loop
	loop.seen = True
	diagram.setLoopUnavailabled(loop)
	

def next(lvl=0, path = []):
	global bcc, fcc, sols_superperms
	bcc += 1
	
	# measure
	chloops = sorted(sorted(diagram.chains, key = lambda chain: len(chain.avloops))[0].avloops, key = lambda loop: (loop.firstNode().ktype, loop.firstNode().address))
		
	if bcc % 10000 is 0:
		print("{lvl:"+str(lvl)+"§"+str(bcc)+"@"+tstr(time() - startTime)+"} | chains: " + str(len(diagram.chains)) + " | chloops: " + str(len(chloops)) + " | " + " ".join([str(k)+'/'+str(n) for k,n,_ in path]))
	#print("{lvl:"+str(lvl)+"} addr: " + " ".join([loop.head.address for _,_,loop in path]))
						
	# checks
	if len(chloops) is 0:
		#show(diagram)
		#print("{lvl:"+str(lvl)+"§"+str(bcc)+"} road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in path]))
		#print("{lvl:"+str(lvl)+"§"+str(bcc)+"} addr: " + " ".join([loop.head.address for _,_,loop in path]))
		#input("Found no chloops")
		
		if len(diagram.chains) is 1:# and len([c for c in diagram.cycles if not c.chain]) is 0:
			SP = diagram.superperm('000000', '000000')
			for node in diagram.nodes:
				assert node.perm in SP	
							
			dup = None
			if SP in sols_superperms:
				dup = sols_superperms.index(SP)
			else:
				sols_superperms.append(SP)
				
			with open("sols."+str(diagram.spClass)+".log", 'a') as log:
				log.write("Found solution #"+str(fcc)+"\n")				
				log.write("{lvl:"+str(lvl)+"@"+str(bcc)+"@"+tstr(time() - startTime)+"} road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in path])+"\n")
				log.write("{lvl:"+str(lvl)+"@"+str(bcc)+"@"+tstr(time() - startTime)+"} addr: " + " ".join([loop.head.address for _,_,loop in path])+"\n")
				if dup is None:
					log.write(SP+"\n\n")
				else:
					log.write("duplicate of " + str(dup)+"\n\n")
								
			fcc += 1
			show(diagram)
			print("{lvl:"+str(lvl)+"§"+str(bcc)+"@"+tstr(time() - startTime)+"} road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in path]))
			print("{lvl:"+str(lvl)+"§"+str(bcc)+"@"+tstr(time() - startTime)+"} addr: " + " ".join([loop.head.address for _,_,loop in path]))
			print("len:"+str(len(SP)) + "\n" + SP)
			input("Found solution #"+str(fcc))								
			
			return False
		else:
			return False
					
	# check if not enough loops to connect all the chains
	#if len(avloops) < (len(diagram.chains) - 1) / 5:
		#return False

	# check if any chains are unreachable
	#if len([chain for chain in diagram.chains if len(chain.avloops) is 0]) > 0:
		#return False
					
	# choose
	#chloops = list(sorted(diagram.chains, key = lambda chain: len(chain.avloops))[0].avloops)
	
	lvl_seen = []
	for chindex, chloop in enumerate(chloops):
				
		# extend
		if diagram.extendLoop(chloop):
							
			# carry on
			if next(lvl+1, path+[(chindex, len(chloops), chloop)]):
				return True

			# revert
			diagram.collapseBack(chloop)

		# remember
		lvl_seen.append(chloop)
		chloop.seen = True
		diagram.setLoopUnavailabled(chloop)

	# forget
	for loop in lvl_seen:
		diagram.setLoopAvailabled(loop)
		loop.seen = False
					
	return False			
	
																																					
			
if __name__ == "__main__":
	
	diagram = Diagram(7)#, withKernel=False)
	patch(diagram)

	tonoavail('100006')

	tonoavail('103006')
	tonoavail('103106')
	tonoavail('103206')
	tonoavail('103306')
	tonoavail('103406')

	tonoavail('122006')
	tonoavail('122106')
	tonoavail('122206')
	tonoavail('122306')
	tonoavail('122406')

	tonoavail('111006')
	tonoavail('111106')
	tonoavail('111206')
	tonoavail('111306')
	tonoavail('111406')

	tonoavail('103405')

	for node in diagram.nodes:
		if node.address.endswith('06') and node.cycle.chain is None and node.loop.availabled and not node.address.startswith('0') and not node.address.startswith('113') and not node.address.startswith('101') and not node.address.startswith('112') and not node.address.startswith('111') and not node.address.startswith('102'):
			diagram.extendLoop(node.loop)
		
	# ~~~ #
	
	extendAddress('000001')
	
	extendAddress('103005')
	extendAddress('103105')
	extendAddress('103205')
	extendAddress('103305')
	
	extendAddress('100020')
	extendAddress('100040')
	
	extendAddress('103451')
	extendAddress('103404')
	extendAddress('103225')
	extendAddress('103135')

	# extendAddress('122005')
	# extendAddress('122105')
	# extendAddress('122205')
	# extendAddress('122305')

	extendAddress('122451')
	extendAddress('122135')
	extendAddress('122225')
	extendAddress('122315')
	
	#extendAddress('111114')
	#extendAddress('111241')
	#extendAddress('111214')
	#extendAddress('111232')
	extendAddress('111451')
	extendAddress('111404')
	extendAddress('111225')
	extendAddress('111135')

	#extendAddress('100242')
					
	print(sorted(groupby(diagram.chains, K = lambda chain: len(chain.avloops), G = lambda g: len(g)).items()))

		
	point(diagram)
		
	show(diagram)
	input('partial')
	
	# every cycle has its own chain at start
	for cycle in diagram.cycles:
		if cycle.chain is None:
			diagram.makeChain([], [cycle])		
	startTime = time()
	sols_superperms = []
	bcc = -1
	fcc = 0
	
	next()
	
	show(diagram)
	input('done.')
	
