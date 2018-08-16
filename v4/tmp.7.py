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

	# ⟨02⟩ 
	extendAddress('020040')
	extendAddress('020130')
	extendAddress('020220')
	extendAddress('020310')
	extendAddress('020400')

	#±# extendAddress('023040')
	extendAddress('023130')
	extendAddress('023220')
	extendAddress('023310')
	extendAddress('023400')
	
	extendAddress('020351') # 0/3
	extendAddress('020341')
	extendAddress('020332')	
	extendAddress('023205')
	extendAddress('023305')
	extendAddress('022305')
	extendAddress('022405')
	extendAddress('021405')
	extendAddress('021005')	
		
	extendAddress('023046')
	extendAddress('021255')	# 0/2
	extendAddress('022155')
	
	extendAddress('021015')	# 1/2
	extendAddress('021333')	# 0/3
	
	extendAddress('022322')	# 0/3
	extendAddress('022411')	# 0/2
	
	extendAddress('010142')	# 0/2
	
	extendAddress('013040')
	extendAddress('013130')
	extendAddress('013220')
	extendAddress('013310')
	extendAddress('013400')

	extendAddress('012040')
	extendAddress('012130')
	extendAddress('012220')
	extendAddress('012310')
	extendAddress('012400')

	extendAddress('013105')
	extendAddress('013205')

	extendAddress('012205')
	extendAddress('012305')
	
	extendAddress('010105')
	extendAddress('010405')
	
	extendAddress('010001') # 0/2
	extendAddress('010006') # 1/2
	
	extendAddress('011324') # 0/2
	extendAddress('011441')
	
	extendAddress('020330')	# !
	extendAddress('011405')
	extendAddress('011231')
	extendAddress('011006') # 1/2
	#extendAddress('011052') # 0/2
	
	# every cycle has its own chain at start
	for cycle in diagram.cycles:
		if cycle.chain is None:
			diagram.makeChain([], [cycle])		
	startTime = time()
	sols_superperms = []
	bcc = -1
	fcc = 0
	
	next()
	
	#diagram.pointers = diagram.nodeByAddress['023040'].loop.nodes; show(diagram); input('missing yellow');
					
	''' # ⟨10⟩ 
	extendAddress('100040')
	extendAddress('100130')
	extendAddress('100220')
	extendAddress('100310')
	extendAddress('100400')

	#±# extendAddress('103040')
	extendAddress('103130')
	extendAddress('103220')
	extendAddress('103310')
	extendAddress('103400')
	
	extendAddress('100351') # 0/3
	extendAddress('100341')
	extendAddress('100332')	
	extendAddress('103205')
	extendAddress('103305')
	extendAddress('102305')
	extendAddress('102405')
	extendAddress('101405')
	extendAddress('101005')
	
	extendAddress('102231')
	extendAddress('101331')
	extendAddress('101151')
	extendAddress('102155')
			
	diagram.pointers = diagram.nodeByAddress['103040'].loop.nodes; show(diagram); input('missing yellow');
	'''
	
	
	diagram.pointers = []
	
		
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
