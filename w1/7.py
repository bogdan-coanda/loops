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
			if node.prevs[2].node.nextLink == None and node.prevs[2].node.cycle.chain != node.cycle.chain:
				in2 = True
			if node.prevs[3].node.nextLink == None and node.prevs[3].node.cycle.chain != node.cycle.chain:
				in3 = True
										
			if not in2 and not in3: top_unconnectable.append(node)
			elif not in3: top_l2_singles.append(node)
			elif not in2: top_l3_singles.append(node)			
			
		# § checking outgoing sockets
		out2 = False
		out3 = False
		node = chain.tailCycle.bot_node()
		if node.nextLink == None:
			if node.links[2].next.prevLink == None and node.links[2].next.cycle.chain != node.cycle.chain:
				out2 = True
			if node.links[3].next.prevLink == None and node.links[3].next.cycle.chain != node.cycle.chain:
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
			# print(f'[connectSingles] ⇒ connected {len(rv_chains)} singles')
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

sid = 0

def step(lvl=0, path=[]):
	global min_total, sid
	
	def key():
		return f"[{tstr(time() - startTime):>11}][lvl:{lvl}]" 

	if sid % 1000 == 0:
		print(f"{key()} {'.'.join([(str(x)+upper(t)) for x,t in path])}")
	sid += 1
	
	# extend 2-link
	headCycle.chain.connect(2)
	conn, rv = connectSingles(diagram)
	
	if not conn:
		if len(diagram.chains) == 1:
			total = calcTotal()
			if total < min_total:
				min_total = total
				show(diagram)
				input2('found smth')
	else:
		step(lvl+1, path+[(0, len(rv))])
		
	revertSingles(rv)
	headCycle.chain.revert()	
	
	# extend 3-link
	headCycle.chain.connect(3)
	conn, rv = connectSingles(diagram)
	
	if not conn:
		if len(diagram.chains) == 1:
			total = calcTotal()
			if total < min_total:
				min_total = total			
				show(diagram)
				input2('found smth')
	else:
		step(lvl+1, path+[(1, len(rv))])
	
	revertSingles(rv)
	headCycle.chain.revert()		
	

if __name__ == "__main__":

	diagram = Diagram(7)
	headCycle = diagram.cycleByAddress['00000']
	
	startTime = time()
	step()
	
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
	
	# revertSingles(rv)
	# headCycle.chain.revert()	
													
	show(diagram)
	
