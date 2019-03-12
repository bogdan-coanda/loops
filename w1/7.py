from diagram import *
from uicanvas import *
from chain import *
from time import time


min_total = 9999999999999999


def recalcSingles(diagram):
	
	top_unconnectable = []
	top_l2_singles = []
	top_l3_singles = []		
	bot_unconnectable = []
	bot_l2_singles = []
	bot_l3_singles = []		

	for chain in diagram.chains:		
									
		# § checking incoming sockets
		in2 = False
		in3 = False
		node = chain.headCycle.top_node()
		if node.prevLink == None:
			if node.prevs[2].available and node.prevs[2].node.nextLink == None and node.prevs[2].node.cycle.chain != node.cycle.chain:
				in2 = True
			if node.prevs[3].available and node.prevs[3].node.nextLink == None and node.prevs[3].node.cycle.chain != node.cycle.chain:
				in3 = True
										
			if not in2 and not in3: top_unconnectable.append(node)
			elif not in3: top_l2_singles.append(node)
			elif not in2: top_l3_singles.append(node)			
			
		# § checking outgoing sockets
		out2 = False
		out3 = False
		node = chain.tailCycle.bot_node()
		if node.nextLink == None:
			if node.links[2].available and node.links[2].next.prevLink == None and node.links[2].next.cycle.chain != node.cycle.chain:
				out2 = True
			if node.links[3].available and node.links[3].next.prevLink == None and node.links[3].next.cycle.chain != node.cycle.chain:
				out3 = True

			if not out2 and not out3: bot_unconnectable.append(node)
			elif not out3: bot_l2_singles.append(node)
			elif not out2: bot_l3_singles.append(node)	

	# if len(top_unconnectable):
	# 	print(f"top unconnectable: " + " ".join([n.cycle.address for n in top_unconnectable]))
	# if len(top_l2_singles):
	# 	print(f"top [2] singles: " + " ".join([n.cycle.address for n in top_l2_singles]))			
	# if len(top_l3_singles):
	# 	print(f"top [3] singles: " + " ".join([n.cycle.address for n in top_l3_singles]))						
	# if len(bot_unconnectable):
	# 	print(f"bot unconnectable: " + " ".join([n.cycle.address for n in bot_unconnectable]))
	# if len(bot_l2_singles):
	# 	print(f"bot [2] singles: " + " ".join([n.cycle.address for n in bot_l2_singles]))			
	# if len(bot_l3_singles):
	# 	print(f"bot [3] singles: " + " ".join([n.cycle.address for n in bot_l3_singles]))											
	return (top_unconnectable, top_l2_singles, top_l3_singles, bot_unconnectable, bot_l2_singles, bot_l3_singles)
	
			
def connectSingles(diagram):	
	
	connectable = True
	rv_chains = []
	
	while True:
		topU, top2, top3, botU, bot2, bot3 = recalcSingles(diagram)	
		if len(topU) + len(top2) + len(top3) + len(botU) + len(bot2) + len(bot3) == 0:
			# print(f'[connectSingles] ⇒ connected {len(rv_chains)} singles | connectable: {connectable}')
			break
		
		if len(topU) + len(botU) > 0:
			# if len(diagram.chains) > 1:
			# 	print(f'[connectSingles] --- unconnectable ---')
			# else:
			# 	print(f'[connectSingles] === everything connected ===')
			connectable = False
			break
			
		if len(bot2) > 0:
			node = bot2[0]
			# print(f'[connectSingles] bot 2: {node.cycle.address}')			
			ch = node.cycle.chain
			assert ch.tailCycle.bot_node() == node
			ch.connect(2)
			rv_chains.append(ch)
			continue
			
		if len(bot3) > 0:
			node = bot3[0]
			# print(f'[connectSingles] bot 3: {node.cycle.address}')			
			ch = node.cycle.chain
			assert ch.tailCycle.bot_node() == node
			ch.connect(3)
			rv_chains.append(ch)
			continue	
			
		assert len(top2) + len(top3) == 0
	return connectable, rv_chains


def revertSingles(rv_chains):
	for chain in reversed(rv_chains):
		chain.revert()


def calcTotal():			
	links_types = { 1: 0, 2: 0, 3: 0 }			
	for cycle in diagram.cycles:
		links_types[1] += 5								
		if cycle.bot_node().nextLink:
			links_types[cycle.bot_node().nextLink.type] += 1
	return links_types[1] + 2 * links_types[2] + 3 * links_types[3]


def purge():
	purgedStuff = []
	nextLines = []
	conn = True
	
	while True:		
	
		linksToPurge = []
		nextLines = [] # reset next lines
		
		for chain in list(diagram.chains):		
			for type in [2, 3]:
				chain.connect(type)
				conn, rv = connectSingles(diagram)
				if conn: nextLines.append([chain, type, len(rv)])
				else: linksToPurge.append(chain.tailCycle.bot_node().links[type])
				revertSingles(rv)
				chain.revert()	
				
		if not len(linksToPurge):
			break
			
		for link in linksToPurge:
			link.available = False
		purgedStuff.append(('links', linksToPurge))					
		print(f"[purge] purged {len(linksToPurge)} links")
		
		conn, rv = connectSingles(diagram)
		purgedStuff.append(('rv', rv))
		print(f"[purge] singles: {len(rv)} | conn: {conn}")
		if not conn:
			return (conn, purgedStuff, nextLines)

	print(f"[purge] ⇒ {len(purgedStuff)} stuff purged")#:\n" + "\n".join([str(line) for line in purgedLinks]))
	nextLines = sorted([line for line in nextLines], key = lambda l: [-l[2], l[1], l[0].id])
	print(f"[purge] ⇒ remaining {len(nextLines)} links")#:\n" + "\n".join([str(line) for line in nextLines]))
	return (conn, purgedStuff, nextLines)


sid = 0
def step(lvl=0, path=[]):
	global min_total, sid
	
	def key():
		return f"[{tstr(time() - startTime):>11}][lvl:{lvl}]" 

	def test():
		if len(diagram.chains) == 1:
			total = calcTotal()
			if total < min_total:
				min_total = total
				show(diagram)
				input2('found smth')

	def unpurge():
		for stuff in reversed(purgedStuff):
			if stuff[0] == 'links':
				for link in stuff[1]:
					link.available = True
			else: # 'rv'
				revertSingles(stuff[1])


	if sid % 100 == 0:
		print(f"{key()} {'.'.join([(str(x)+upper(t)) for x,t in path])}")
	sid += 1
		
	# purge
	# conn, purgedStuff, nextLines = purge()
	# 
	# if not conn:
	# 	test()
	# 	unpurge()
	# 	return			
	# 
	# if len(purgedStuff):
	# 	for stuff in purgedStuff:
	# 		path = path+[('|' if stuff[0] == 'links' else '§', len(stuff[1]))]
	# 
	# headChain = nextLines[0][0]
	headChain = headCycle.chain
					
	# extend 2-link
	headChain.connect(2)
	conn, rv = connectSingles(diagram)
	
	if not conn:
		test()
	else:
		step(lvl+1, path+[(0, len(rv))])
					
	revertSingles(rv)
	headChain.revert()	

	# extend 3-link
	headChain.connect(3)
	conn, rv = connectSingles(diagram)
	
	if not conn:
		test()
	else:
		step(lvl+1, path+[(1, len(rv))])
	
	revertSingles(rv)
	headChain.revert()		
	
	# unpurge()
	

if __name__ == "__main__":

	diagram = Diagram(7)
	headCycle = diagram.cycleByAddress['00000']
			
	def connect(ccs):
		for ix,x in enumerate(ccs):
			if x != ' ':
				cc = int(x)
				if ix == 0 and headCycle.chain.cycleCount > 1:	
					headCycle.chain.connect(2)
				for _ in range(cc-1): 
					headCycle.chain.connect(2)
				if ix != len(ccs)-1:
					headCycle.chain.connect(3)	
			elif ix == 0:
				headCycle.chain.connect(3)
				
	def connex(path):
		for x in path:
			if x == '.':
				headCycle.chain.connect(2)
			elif x == '∘':
				headCycle.chain.connect(3)
			elif x in ['0','1','2','3','4','5','6','7','8','9']:
				cc = int(x)
				for _ in range(cc-1): 
					headCycle.chain.connect(2)
		

	# connect('4 6666 2 666 2 6666')

	# ~~~ k01:
	# connect('66666')
	# ---
	# connect('5') # 8
	# connect('14') # 11
	# connect('23') # 11
	# connect('32') # 11
	# connect('41') # 11
	# connect('5') # 10	
	# 30 cycles | 5 segments | ℓ₃: 4
	# 6 cycles/segment

	# ~~~ xxx:
	# connect('6666 3 6666 3')
	# 54 cycles | 10 segments | ℓ₃: 9
	# 5.4 cycles/segment
							
	# ~~~ ---:
	# connect('4 6666 2 2 6666 4 4 6666 2 3 6666 3 2 6666 4')	
	# 150 cycles | 30 segments | ℓ₃: 29
	# 5 cycles/segment
	
	# ~~~ nsk: 
	# connect('666 3 66 4 666 4 66 4 666 4 66 3 666')		
	# connect('5') # 8 # §5
	# connect('14') # 11 # §64
	# connect('23') # 11 # §663
	# connect('32') # 11 # §6662
	# connect('14') # 11 # §66634
	# connect('23') # 11 # §666363
	# connect('32') # 11 # §6663662
	# connect('23') # 11 # §66636643
	# connect('32') # 11 # §666366462
	# connect('41') # 11 # §6663664661
	# connect('5') # 10 # §6663664666
	# connect(' 41') # 12 # §666366466641
	# connect('5') # 10 # §666366466646
	# connect(' 5') # 11 # §6663664666465
	# connect('14') # 11 # §66636646664664
	# connect(' 5') # 11 # §666366466646645
	# connect('14') # 11 # §6663664666466464
	# connect('23') # 11 # §66636646664664663
	# connect('32') # 11 # §666366466646646662
	# connect('23') # 11 # §6663664666466466643
	# connect('32') # 11 # §66636646664664666462
	# connect('41') # 11 # §666366466646646664661
	# connect('23') # 11 # §6663664666466466646633
	# connect('32') # 11 # §66636646664664666466362
	# connect('41') # 11 # §666366466646646664663661
	# connect('5') # 10 # §666366466646646664663666
	
			
	# connect('5') ⇒ 
	# connect('14')	
	# connect(' 5')
	
	# connect('14') ⇒ 
	# connect('23')
	# connect('14')
	# connect(' 5')
	
	# connect('23') ⇒ 
	# connect('32')
	# connect('23')
	# connect('14')
	# connect(' 5')
	
	# connect('32') ⇒ 
	# connect('41')
	# connect('32')
	# connect('23')
	# connect('14')
	# connect(' 5')
			
	# connect('41') ⇒ 
	# connect('5')
	# connect('41')
	# connect('32')
	# connect('23')
	# connect('14')
	# connect(' 5')
	
	# connex('5 .1∘4 .2∘3 .3∘2 .1∘4 .2∘3 .3∘2 .2∘3 .3∘2 .4∘1 .5 [∘4∘1] .5 ∘5 .1∘4 ∘5 .1∘4 .2∘3 .3∘2 .2∘3 .3∘2 .4∘1 .2∘3 .3∘2 .4∘1 .5')	
	# ∘5  ⇒  .1 / ∘5
	# .1  ⇒  .2 / .1 / ∘5
	# .2  ⇒  .3 / .2 / .1 / ∘5
	# .3  ⇒  .4 / .3 / .2 / .1 / ∘5
	# .4  ⇒  .5 / .4 / .3 / .2 / .1 / ∘5
	# .5  ⇒  ∘4 / ∘5
	# ∘4  ⇒  .5
	#         §  0/2  0/3  0/4  0/5  0/6  ⇒  K01
	# connex('5 .1∘4 .2∘3 .3∘2 .4∘1   .5 ')
	#       §  0/2  0/3  0/4  0/5  2/6  0/5  0/6   0/2    1/2  0/2  0/3  2/4  0/3  0/4  0/5  2/6  0/5  0/6   0/2    1/2  0/2  0/3  2/4  0/3  0/4  0/5  2/6  0/5  2/6 
	connex('5 .1∘4 .2∘3 .3∘2 .4∘1 .3∘2 .4∘1   .5 [∘4∘1].5  ∘5 .1∘4 .2∘3 .1∘4 .2∘3 .3∘2 .4∘1 .3∘2 .4∘1   .5 [∘4∘1].5  ∘5 .1∘4 .2∘3 .1∘4 .2∘3 .3∘2 .4∘1 .3∘2 .4∘1 .3∘2 .2∘3 .3∘2 .4∘1 .3∘2 .4∘1 .5 [∘4∘1].5 ∘5 .1∘4 .2∘3 .1∘4 .2∘3 .3∘2 .4∘1 .3∘2 .4∘1 .5 [∘4∘1].5 ∘5 .1∘4 .2∘3 .1∘4 .2∘3 .3∘2 .4∘1 .5')
			
	# 
	# connect('23') # §66643
	# connect('32') # §666462
	# connect('41') # §6664661
	# connect('5 ') # 10 !!! # §6664666∘
	# connect(' 41') # 12 !!! # §666466641
	# connect('5 ') # 10 !!! # §666466646∘
	# connect(' 5') # 11 # §6664666465
	# 
	# connect('14') # 11 # §66646664664	
	# connect('23') # 11 # §666466646663
	# 
	# connect('14') # §6664666466644
	# connect('23') # §66646664666463
	# 
	# connect('32') # 11 
	# connect('23') # 11
	# connect('32') # 11
	# connect('41') # 11
	# headCycle = diagram.cycleByAddress['12114']
	# connect('5 ') # 10 !!!
	# connect(' 41') # 12 !!!
	# connect('5 ') # 10 !!!
	# connect(' 41') # 11
	# 
	# 
	# 
	# connect('5')
	
	# connect('14 ') # 11
	# connect(' 5') # 11
	# connect('14') # 11
	# connect('23') # 11
	# connect('32') # 11
	# connect('23') # 11
	# connect('32') # 11
	# connect('41') # 11
	# connect('23') # 11
	# connect('32') # 11
	# connect('41') # 11
	# connect('5') # 10
	# 130 cycles | 24 segments | ℓ₃: 23
	# 5.41666… cycles per segment
	
	
	# rv = connectSingles(diagram)
	
	#connect('6666 2 6666 4')	
	
	# startTime = time()
	# step()
	
	# diagram.cycleByAddress['00005'].chain.connect(3)
	# rv = connectSingles(diagram)		
	# 
	# diagram.cycleByAddress['00000'].chain.connect(2)
	# rv = connectSingles(diagram)		
	# 
	# diagram.cycleByAddress['00001'].chain.connect(3)
	# rv = connectSingles(diagram)		
	# 
	# diagram.cycleByAddress['10005'].chain.connect(2)
	# rv = connectSingles(diagram)		
									
	'''

	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(3)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)

	headCycle.chain.connect(3)
	rv = connectSingles(diagram)

	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
		
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
		
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
		
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)

	headCycle.chain.connect(2)
	rv = connectSingles(diagram)

	headCycle.chain.connect(2)
	rv = connectSingles(diagram)

	headCycle.chain.connect(3)
	rv = connectSingles(diagram)

	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
		
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)

	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)

	headCycle.chain.connect(2)
	rv = connectSingles(diagram)

	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(3)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(3)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(3)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(3)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
																																																														
	# purge
	conn, purgedStuff, nextLines = purge()
	
	'''
	'''		
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	purge()
				
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)

	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	headCycle.chain.connect(2)
	rv = connectSingles(diagram)
	
	# headCycle.chain.connect(2)
	# rv = connectSingles(diagram)
	
	
	# revertSingles(rv)
	# headCycle.chain.revert()	
	'''
													
	show(diagram)
	
