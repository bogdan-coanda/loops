from diagram import *
from uicanvas import *
from common import *
import itertools


def patch(diagram):
	
	for head in ['0001', '0002', '0003', '0004']:
								
		diagram.makeChain([], [diagram.cycleByAddress[head+'00']])
		diagram.extendLoop(diagram.nodeByAddress[head+'007'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'10']])
		diagram.extendLoop(diagram.nodeByAddress[head+'107'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'20']])
		diagram.extendLoop(diagram.nodeByAddress[head+'207'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'30']])
		diagram.extendLoop(diagram.nodeByAddress[head+'307'].loop)
		diagram.makeChain([], [diagram.cycleByAddress[head+'40']])
		diagram.extendLoop(diagram.nodeByAddress[head+'407'].loop)	
		diagram.makeChain([], [diagram.cycleByAddress[head+'50']])
		diagram.extendLoop(diagram.nodeByAddress[head+'507'].loop)			
		
		diagram.nodeByAddress[head+'067'].nextLink = diagram.nodeByAddress[head+'067'].links[3]
		diagram.nodeByAddress[head+'167'].nextLink = diagram.nodeByAddress[head+'167'].links[3]
		diagram.nodeByAddress[head+'267'].nextLink = diagram.nodeByAddress[head+'267'].links[3]
		diagram.nodeByAddress[head+'367'].nextLink = diagram.nodeByAddress[head+'367'].links[3]
		diagram.nodeByAddress[head+'467'].nextLink = diagram.nodeByAddress[head+'467'].links[3]
		diagram.nodeByAddress[head+'567'].nextLink = diagram.nodeByAddress[head+'567'].links[3]		
	
	diagram.nodeByAddress['0000567'].nextLink = Link(4, diagram.nodeByAddress['0000567'], diagram.nodeByAddress['0001000'])
	diagram.nodeByAddress['0001567'].nextLink = Link(4, diagram.nodeByAddress['0001567'], diagram.nodeByAddress['0002000'])
	diagram.nodeByAddress['0002567'].nextLink = Link(4, diagram.nodeByAddress['0002567'], diagram.nodeByAddress['0003000'])
	diagram.nodeByAddress['0003567'].nextLink = Link(4, diagram.nodeByAddress['0003567'], diagram.nodeByAddress['0004000'])
	diagram.nodeByAddress['0004567'].nextLink = Link(4, diagram.nodeByAddress['0004567'], diagram.nodeByAddress['0000000'])
		
	diagram.makeChain(list(diagram.chains), [])		
	
def jmp(x):
	diagram.jmp(x); show(diagram); input("[jmp] » "+str(x))
	
def adv(x):
	diagram.adv(x); show(diagram); input("[adv] » "+str(x))

def exp(addr=None):
	if addr:
		diagram.pointers = diagram.nodeByAddress[addr].tuple		
	for node in diagram.pointers:
		assert diagram.extendLoop(node.loop)	
		
def extendAddress(addr):
	assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
		
def extendColumn(column_addr, key):
	i = 0
	j = key
	while i < 6:
		extendAddress(column_addr+str(i)+str(j))
		if j > 0:
			i += 1
			j -= 1
		else:
			i += 2
			j = 4
		
def extendGreen(blue_column_addr):
	extendAddress(blue_column_addr+'07')
	extendAddress(blue_column_addr+'15')
	extendAddress(blue_column_addr+'24')
	extendAddress(blue_column_addr+'33')
	extendAddress(blue_column_addr+'42')
	extendAddress(blue_column_addr+'51')
	
def extendYellowDiag(addr):
	extendAddress(addr+'050')
	extendAddress(addr+'140')
	extendAddress(addr+'230')
	extendAddress(addr+'320')
	extendAddress(addr+'410')
	
def extendYellowColumn(addr):
	extendYellowDiag(addr+'0')
	extendGreen(addr+'14')
	extendGreen(addr+'23')
	extendGreen(addr+'32')
	extendGreen(addr+'41')
	
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
			SP = diagram.superperm('0000000', '0000000')
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
	
	diagram = Diagram(8)#, isDualWalkType=True, baseAddresses=['000001', '003402'])
	patch(diagram)
	
	#diagram.pointers = [n for n in diagram.nodes if n.tuple[0] is n.tuple[1]]; show(diagram); input("singled tuples after patch")
					
	for a in range(2):
		for b in range(3):
			for c in range(4):
				addr = str(a)+str(b)+str(c)
				if addr != '000' and addr != '123':
					extendYellowColumn(addr)

	show(diagram)	
	input("partial")

	# every cycle has its own chain at start
	for cycle in diagram.cycles:
		if cycle.chain is None:
			diagram.makeChain([], [cycle])		

	#show(diagram)	
	#input("partial chained")
					
	startTime = time()
	sols_superperms = []
	bcc = -1
	fcc = 0
	
	next()
												
	#'''
	
	diagram.pointers = [cycle.avnode() for cycle in diagram.cycles if cycle.chain is None and len([n for n in cycle.nodes if n.loop.availabled]) < 2]
	
	'''
	#diagram.pointers = list(diagram.nodeByAddress['123006'].tuple)	
	#diagram.pointers = [node for node in diagram.nodes if node.loop.availabled and len([nln for nln in node.loop.nodes if nln.address.startswith('123')]) >= 2]
	#diagram.pointers = [node for node in diagram.nodes if node.loop.availabled and node.ktype > -1 and len([nln for nln in node.loop.nodes if nln.address[0:3] in [
		#'002', '023', '113']]) > 3]
	'''

	show(diagram)
