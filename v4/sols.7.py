from diagram import *
from uicanvas import *
from common import *
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
	extendAddress(blue_column_addr+'06')
	extendAddress(blue_column_addr+'14')
	extendAddress(blue_column_addr+'23')
	extendAddress(blue_column_addr+'32')
	extendAddress(blue_column_addr+'41')
	

	
	
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
	
	diagram = Diagram(7)#, isDualWalkType=True, baseAddresses=['000001', '003402'])
	patch(diagram)

	#diagram.pointers = [n for n in diagram.nodes if n.tuple[0] is n.tuple[1]]; show(diagram); input("singled tuples after patch")
					
	# ⟨010⟩ #
	extendAddress('010040')
	extendAddress('010130')
	extendAddress('010220')
	extendAddress('010310')

	# ⟨01⟩ #		
	extendGreen('0113')
	extendGreen('0122')
	extendGreen('0131')
	
	# ⟨020⟩ #
	extendAddress('020040')
	extendAddress('020130')
	extendAddress('020220')
	extendAddress('020310')

	# ⟨02⟩ #				
	extendGreen('0213')
	extendGreen('0222')
	extendGreen('0231')
			
	# ⟨100⟩ #
	extendAddress('100040')
	extendAddress('100130')
	extendAddress('100220')
	extendAddress('100310')

	# ⟨10⟩ #		
	extendGreen('1013')
	extendGreen('1022')
	extendGreen('1031')			
			
	# ⟨110⟩ #
	# extendAddress('110040')
	# extendAddress('110130')
	# extendAddress('110220')
	# extendAddress('110310')

	# ⟨11⟩ #		
	# extendGreen('1113')
	# extendGreen('1122')
	# extendGreen('1131')
	
	# ⟨120⟩ #
	# extendAddress('120040')
	# extendAddress('120130')
	# extendAddress('120220')
	# extendAddress('120310')

	# ⟨12⟩ #				
	# extendGreen('1213')
	# extendGreen('1222')
	# extendGreen('1231')

	show(diagram)	
	input("partial")

	# every cycle has its own chain at start
	for cycle in diagram.cycles:
		if cycle.chain is None:
			diagram.makeChain([], [cycle])		

	show(diagram)	
	input("partial chained")
					
	startTime = time()
	sols_superperms = []
	bcc = -1
	fcc = 0
	
	next()
												
	# extendAddress('010416')	# 1/2
	# extendAddress('020416')	# 1/2
	# extendAddress('100416')	# 1/2				
	# extendAddress('110416')	# 1/2
	# extendAddress('120416')	# 1/2				
	
	#extendAddress('010001')	# 1/2
	#extendAddress('010151')	# 0/1
	#extendAddress('100000')	# 0/1
	#extendAddress('100242')	# 0/1
	#extendAddress('110350')	# 0/1
	
	#extendAddress('010025')	# 1/2
	#extendAddress('010203')	# 0/1
	#extendAddress('020151')	# 0/1
	#extendAddress('020330')	# 0/1
	#extendAddress('020350')	# 0/1
	#extendAddress('020203')	# 0/1
	
	# extendAddress('020001')	# 1/2
	# extendAddress('110151')	# 0/1
	# extendAddress('110114')	# 0/1
	# extendAddress('110335')	# 0/1
	# extendAddress('020020')	# 0/1
	# extendAddress('020110')	# 0/1
	# extendAddress('020200')	# 0/1
	# extendAddress('020340')	# 0/1
	# extendAddress('020105')	# 0/1
	
	'''
	# ⟨000⟩ #
	extendGreen('0000')
	
	extendAddress('000324')
	extendAddress('000234')
	extendAddress('000144')
	extendAddress('000054')
	#extendAddress('000003')
	
	# ⟨021⟩ #
	extendGreen('0210')
	
	# ⟨001⟩ #
	extendGreen('0120')
		
	# ~~~ #
	#extendColumn('0030', 3)
	# extendAddress('003105')
	# extendAddress('003205')
	# extendAddress('003305')
	# extendAddress('003405')
	
	# ⟨010⟩ #
	extendGreen('0100')
	extendAddress('010324')
	extendAddress('010234')
	extendAddress('010144')
	extendAddress('010054')
	
	# ⟨001⟩ #
	extendGreen('0010')
	
	# ⟨022⟩ #
	extendGreen('0220')
		
	# ⟨020⟩ #
	extendGreen('0200')
	extendAddress('020324')
	extendAddress('020234')
	extendAddress('020144')
	extendAddress('020054')

	# ⟨011⟩ #
	extendGreen('0110')
	
	# ⟨002⟩ #
	extendGreen('0020')
	
	
	# extendAddress('003002')	

	# ⟨100⟩ #
	extendGreen('1000')
	extendAddress('100054')
	extendAddress('100144')
	extendAddress('100234')
	extendAddress('100324')

	# ⟨101⟩ #
	extendGreen('1010')
	
	# ⟨102⟩ #
	extendGreen('1020')
				
	# ⟨110⟩ #
	extendGreen('1100')
	extendAddress('110054')
	extendAddress('110144')
	extendAddress('110234')
	extendAddress('110324')
		
	# ⟨111⟩ #
	extendGreen('1110')	

	# ⟨112⟩ #
	extendGreen('1120')
			
	# ⟨120⟩ #
	extendGreen('1200')
	extendAddress('120054')
	extendAddress('120144')
	extendAddress('120234')
	extendAddress('120324')
		
	# ⟨121⟩ #
	extendGreen('1210')	

	# ⟨122⟩ #
	extendGreen('1220')	

	extendAddress('003004')
	'''
	
	diagram.pointers = [cycle.avnode() for cycle in diagram.cycles if cycle.chain is None and len([n for n in cycle.nodes if n.loop.availabled]) < 2]
	
	'''
	#diagram.pointers = list(diagram.nodeByAddress['123006'].tuple)	
	#diagram.pointers = [node for node in diagram.nodes if node.loop.availabled and len([nln for nln in node.loop.nodes if nln.address.startswith('123')]) >= 2]
	#diagram.pointers = [node for node in diagram.nodes if node.loop.availabled and node.ktype > -1 and len([nln for nln in node.loop.nodes if nln.address[0:3] in [
		#'002', '023', '113']]) > 3]
	'''

	show(diagram)
