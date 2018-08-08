from diagram import *
from uicanvas import *
import itertools


def cychain(addr):
	diagram.makeChain([], [diagram.cycleByAddress[addr]])

def extend(addr):
	assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)	

def annex(addr):
	diagram.nodeByAddress[addr].nextLink = diagram.nodeByAddress[addr].links[2]
	
	
def next(lvl=0, path = []):
	global bcc, fcc, sols_superperms
	bcc += 1
	
	# measure
	chloops = sorted(sorted(diagram.chains, key = lambda chain: len(chain.avloops))[0].avloops, key = lambda loop: loop.firstNode().address)
		
	if bcc % 1000 is 0:
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
			#show(diagram)
			print("{lvl:"+str(lvl)+"§"+str(bcc)+"@"+tstr(time() - startTime)+"} road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in path]))
			print("{lvl:"+str(lvl)+"§"+str(bcc)+"@"+tstr(time() - startTime)+"} addr: " + " ".join([loop.head.address for _,_,loop in path]))
			print("len:"+str(len(SP)) + "\n" + SP)
			#input("Found solution #"+str(fcc))								
			
			return True
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
	
	sp = diagram.superperm('000000', '000000')
	print(len(sp), sp)
	
