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
			SP = diagram.superperm('00000', '00000')
			for node in diagram.nodes:
				assert node.perm in SP	
							
			dup = None
			if SP in sols_superperms:
				dup = sols_superperms.index(SP)
			else:
				sols_superperms.append(SP)
				
			with open("sols."+str(diagram.spClass)+".partial_2_4D.log", 'a') as log:
				log.write("Found solution #"+str(fcc)+"\n")				
				log.write("{lvl:"+str(lvl)+"@"+str(bcc)+"@"+tstr(time() - startTime)+"} road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in path])+"\n")
				log.write("{lvl:"+str(lvl)+"@"+str(bcc)+"@"+tstr(time() - startTime)+"} addr: " + " ".join([loop.head.address for _,_,loop in path])+"\n")
				if dup is None:
					log.write(SP+"\n\n")
				else:
					log.write("duplicate of " + str(dup)+"\n\n")
								
			fcc += 1
			# show(diagram)
			# print("{lvl:"+str(lvl)+"§"+str(bcc)+"@"+tstr(time() - startTime)+"} road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in path]))
			# print("{lvl:"+str(lvl)+"§"+str(bcc)+"@"+tstr(time() - startTime)+"} addr: " + " ".join([loop.head.address for _,_,loop in path]))
			#print("len:"+str(len(SP)) + "\n" + SP)
			# input("Found solution #"+str(fcc))								
			
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
	
	diagram = Diagram(6)#, withKernel=False)
	
	
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
	
	
	'''
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
	'''
	
	diagram.nodeByAddress['00345'].nextLink = Link(4, diagram.nodeByAddress['00345'], diagram.nodeByAddress['01000'])
	diagram.nodeByAddress['01345'].nextLink = Link(4, diagram.nodeByAddress['01345'], diagram.nodeByAddress['00000'])
	
	diagram.makeChain(list(diagram.chains), [])
	
	show(diagram)
	input()
	
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
	
	sp = diagram.superperm('00000', '00000')
	print(len(sp), sp)

	print("Found superperms: " + str(len(sols_superperms)))
	

