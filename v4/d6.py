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
	
	'''
	extend('00002')
		
			
	cychain('0120')
	extend('01203')

	cychain('0102')
	extend('01024')

	cychain('0100')
	extend('01001')
					
	node = diagram.nodeByAddress['00002'].loopBrethren[-1]
	node.nextLink = node.links[3]

	node = diagram.nodeByAddress['01203'].loopBrethren[-1]
	node.nextLink = node.links[3]	
	
	node = diagram.nodeByAddress['01024'].loopBrethren[-1]
	node.nextLink = node.links[3]	
	
	node = diagram.nodeByAddress['01001'].loopBrethren[-1]
	node.nextLink = node.links[3]	
	'''
	'''
	diagram.makeChain([], [diagram.cycleByAddress['1100']])
	diagram.extendLoop(diagram.nodeByAddress['11005'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['1110']])
	diagram.extendLoop(diagram.nodeByAddress['11105'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['1120']])
	diagram.extendLoop(diagram.nodeByAddress['11205'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['1130']])
	diagram.extendLoop(diagram.nodeByAddress['11305'].loop)
	
	diagram.nodeByAddress['11045'].nextLink = diagram.nodeByAddress['11045'].links[3]
	diagram.nodeByAddress['11145'].nextLink = diagram.nodeByAddress['11145'].links[3]
	diagram.nodeByAddress['11245'].nextLink = diagram.nodeByAddress['11245'].links[3]
	diagram.nodeByAddress['11345'].nextLink = diagram.nodeByAddress['11345'].links[3]

	diagram.makeChain([diagram.cycleByAddress[addr].chain for addr in ['1100', '1110', '1120', '1130']], [])
	'''
	
	'''
	diagram.makeChain([], [diagram.cycleByAddress['1100']])
	diagram.extendLoop(diagram.nodeByAddress['11005'].loop)
	#diagram.makeChain([], [diagram.cycleByAddress['1110']])
	#diagram.extendLoop(diagram.nodeByAddress['11105'].loop)
	#diagram.makeChain([], [diagram.cycleByAddress['1120']])
	#diagram.extendLoop(diagram.nodeByAddress['11205'].loop)
	#diagram.makeChain([], [diagram.cycleByAddress['1130']])
	#diagram.extendLoop(diagram.nodeByAddress['11305'].loop)
	
	diagram.makeChain([], [diagram.cycleByAddress['1113']])
	#diagram.extendLoop(diagram.nodeByAddress['11140'].loop)
	diagram.nodeByAddress['11045'].nextLink = Link(3, diagram.nodeByAddress['11045'], diagram.nodeByAddress['11132'])
	#diagram.nodeByAddress['11145'].nextLink = diagram.nodeByAddress['11145'].links[3]
	#diagram.nodeByAddress['11245'].nextLink = diagram.nodeByAddress['11245'].links[3]
	#diagram.nodeByAddress['11345'].nextLink = diagram.nodeByAddress['11345'].links[3]

	#diagram.makeChain([diagram.cycleByAddress[addr].chain for addr in ['1100', '1110', '1120']], []) # , '1130'
	'''
	
	'''
	diagram.makeChain([], [diagram.cycleByAddress['1200']])
	diagram.extendLoop(diagram.nodeByAddress['12005'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['1210']])
	diagram.extendLoop(diagram.nodeByAddress['12105'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['1220']])
	diagram.extendLoop(diagram.nodeByAddress['12205'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['1230']])
	diagram.extendLoop(diagram.nodeByAddress['12305'].loop)
	
	diagram.nodeByAddress['12045'].nextLink = diagram.nodeByAddress['12045'].links[3]
	diagram.nodeByAddress['12145'].nextLink = diagram.nodeByAddress['12145'].links[3]
	diagram.nodeByAddress['12245'].nextLink = diagram.nodeByAddress['12245'].links[3]
	diagram.nodeByAddress['12345'].nextLink = diagram.nodeByAddress['12345'].links[3]

	diagram.makeChain([diagram.cycleByAddress[addr].chain for addr in ['1200', '1210', '1220', '1230']], [])
	'''
		
	'''
	diagram.makeChain([], [diagram.cycleByAddress['1000']])
	diagram.extendLoop(diagram.nodeByAddress['10005'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['1010']])
	diagram.extendLoop(diagram.nodeByAddress['10105'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['1020']])
	diagram.extendLoop(diagram.nodeByAddress['10205'].loop)
	diagram.makeChain([], [diagram.cycleByAddress['1030']])
	diagram.extendLoop(diagram.nodeByAddress['10305'].loop)
	
	diagram.nodeByAddress['10045'].nextLink = diagram.nodeByAddress['10045'].links[3]
	diagram.nodeByAddress['10145'].nextLink = diagram.nodeByAddress['10145'].links[3]
	diagram.nodeByAddress['10245'].nextLink = diagram.nodeByAddress['10245'].links[3]
	diagram.nodeByAddress['10345'].nextLink = diagram.nodeByAddress['10345'].links[3]

	diagram.makeChain([diagram.cycleByAddress[addr].chain for addr in ['1000', '1010', '1020', '1030']], [])
	'''

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
	for cycle in diagram.cycles:
		if cycle.chain is None:
			diagram.makeChain([], [cycle])		
					
					
	startTime = time()
	sols_superperms = []
	bcc = -1
	fcc = 0
		
	next()
	
	'''	
	extend('10111') # 0/3
	extend('11233') # 0/2
	extend('12111') # 0/2
	extend('12231') # 0/2
	extend('10233') # 0/2
	extend('11113')
	extend('11102') # 0/2
	extend('12200') # 0/2
	extend('11313')
	extend('11143')
	extend('10105')
	extend('11030')
	extend('10213')
	extend('10222')
	'''
	#extend('00343') # 7/8
	#extend('11122')
	#extend('11330')
	#extend('11025')
	
	#extend('01214') # 1/2
	#extend('01231')
	#extend('01341')
	#extend('01121')
	#extend('01102')
	#extend('02013')
	#extend('01231') # 1/2
	#extend('01103') # 1/2
	#extend('01323')
	#extend('02315')
	#extend('02035')
	#extend('02125')
	#extend('02230')
	#extend('02202')
	#extend('11122')
	#extend('01144') # 1/2	
	
	#extend('01301')
	#extend('02213')
	#extend('02322')
	#extend('02331')		
	#extend('02130')
	#extend('02001')
	#extend('11022')			
	#extend('02021')	# 1/2
	#extend('02044')	# 1/2

	#extend('01131')
	#extend('01013')
	#extend('01022')
	#extend('01214')
	#extend('01343')
	
	#extend('10205')
	#extend('10115')
			
	#extend('01235')
	#extend('01115')
	#extend('01015')
	#extend('01314')
	#extend('01342')
	
	#extend('02025')
	
	#extend('00301')
	#extend('12343')
	#extend('12143')
	#extend('12243')
	#extend('12043')
	
	#extend('02322')
	#extend('02122')

	# extend('01032')
	
	# extend('10232')
	
	#extend('00001')
	'''
	diagram.makeChain([], [diagram.cycleByAddress['0000']])
	diagram.extendLoop(diagram.nodeByAddress['00004'].loop)
	' ''
	
	diagram.extendLoop(diagram.nodeByAddress['00135'].loop)
	diagram.extendLoop(diagram.nodeByAddress['00225'].loop)
	diagram.extendLoop(diagram.nodeByAddress['00315'].loop)
		
	diagram.makeChain([], [diagram.cycleByAddress['0001']])
	diagram.makeChain([], [diagram.cycleByAddress['0002']])
	diagram.makeChain([], [diagram.cycleByAddress['0003']])
	
	diagram.nodeByAddress['00005'].nextLink = diagram.nodeByAddress['00005'].links[2]
	diagram.nodeByAddress['00015'].nextLink = diagram.nodeByAddress['00015'].links[2]
	diagram.nodeByAddress['00025'].nextLink = diagram.nodeByAddress['00025'].links[2]
			
	'''	
	show(diagram)
	
	sp = diagram.superperm('00000', '00000')
	print(len(sp), sp)
	
