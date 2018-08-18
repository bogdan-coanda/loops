from diagram import *
from uicanvas import *
import itertools


def patch(diagram):
	
	for head in ['001', '002']:#, '003']:
								
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
		#diagram.nodeByAddress[head+'456'].nextLink = diagram.nodeByAddress[head+'456'].links[3]
		
	diagram.nodeByAddress['000456'].nextLink = Link(4, diagram.nodeByAddress['000456'], diagram.nodeByAddress['001000'])
	diagram.nodeByAddress['001456'].nextLink = Link(4, diagram.nodeByAddress['001456'], diagram.nodeByAddress['002000'])
	diagram.nodeByAddress['002456'].nextLink = Link(4, diagram.nodeByAddress['002456'], diagram.nodeByAddress['000000'])
	#diagram.nodeByAddress['003456'].nextLink = Link(4, diagram.nodeByAddress['003456'], diagram.nodeByAddress['000000'])
	
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


def next(lvl=0, path = []):
	global bcc, fcc, sols_superperms
	bcc += 1
	
	# measure
	chloops = sorted(sorted(diagram.chains, key = lambda chain: len(chain.avloops))[0].avloops, key = lambda loop: loop.firstNode().address)
		
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

	
	extendAddress('003050')
	extendAddress('003150')
	extendAddress('003250')
	extendAddress('003350')
	extendAddress('003450')

	extendColumn('0034', 2)
	extendColumn('0134', 0)
	extendColumn('0131', 3)
	extendColumn('0132', 2)
	
	extendAddress('010206')
	extendAddress('011106')
	extendAddress('012006')

	extendAddress('020106')	
	extendAddress('021006')	
	
	extendAddress('000002')
	extendAddress('003353')
	
	extendColumn('0200', 4)
	
	extendColumn('0202', 2)
	extendColumn('0203', 1)
		
	#extendAddress('010203') # 0/7
	
	#extendAddress('013130')
	#extendAddress('013220')
		
	
	diagram.pointers = []
	#diagram.pointers = diagram.nodeByAddress['103202'].loop.nodes
		
	nodes = [cycle.avnode() if len([n for n in cycle.nodes if n.loop.availabled]) is 1 else cycle for cycle in diagram.cycles if cycle.chain is None and len([n for n in cycle.nodes if n.loop.availabled]) < 2]
	if len(nodes):
		diagram.pointers += list(nodes)
	
	chain = sorted(diagram.chains, key = lambda chain: len(chain.avloops))[0]
	print(chain, len(chain.avloops))
	if len(chain.avloops) is 1:
		diagram.pointers += [[n for n in loop.nodes if n.cycle.chain is chain][0] for loop in chain.avloops]
	elif len(chain.avloops) is 0:
		diagram.pointers += [cycle.avnode() if len([n for n in cycle.nodes if n.loop.availabled]) is 1 else cycle for cycle in chain.cycles]
	
	if len(diagram.pointers) is 0:
		diagram.pointers = sorted([cycle for cycle in diagram.cycles if cycle.chain is None], key = lambda cycle: (len([n for n in cycle.nodes if n.loop.availabled]), cycle.address))[0:1]
		
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
	
