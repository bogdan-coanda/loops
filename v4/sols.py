from diagram import *
from uicanvas import *
from common import *

addrs = [
	'''001114 001214 001014 001005 001401 112006 001224 001042 001452 002053 002011 002020 002322 011001 002143 013010 013222 013322 013402 022005 022014 022032 013453 022042 | 111000 120140 020140 103206 020440 101240 100106 121110 122100 110210 102430 001420 023010 003006 021330 002200 020300 022210''',
	'''001114 001214 001014 001005 001401 112006 001224 001042 001452 002053 002011 002020 002322 011001 002143 013010 013222 013322 013402 022005 022014 022032 013453 022042 | 001406 003030 103010 012240 121200 010000 110206 100120 120230 111106 012400 012040 021310 023400 020440 122240 013410 113310''',
	'''001114 001214 001014 001005 001401 112006 001224 001042 001452 002053 002011 002020 002322 011001 002143 013010 013222 013322 013402 022005 022014 022032 013453 022042 | 001406 003020 103100 113310 101440 110230 021306 111410 101100 102340 120000 100110 010140 012400 013030 101240 122210 022406''',
	'''001114 001214 001014 001005 001401 112006 001224 001042 001452 002053 002011 002020 002322 011001 002143 013010 013222 013322 013402 022005 022014 022032 013453 022042 | 001410 021320 022300 002340 010140 010340 013440 003006 121110 100130 102200 010000 020300 110206 023130 120110 103010 113006''',
	'''001114 001214 001014 001005 001401 112006 001224 001042 001452 002053 002011 002020 002322 011001 002143 013010 013222 013322 013402 022005 022014 022032 013453 022042 | 111410 002040 001430 100106 113400 101100 021306 110220 122330 121306 002200 002340 003010 013300 012040 023040 102310 022210''',
	
	'''001114 001214 001014 001005 001403 002020 002110 002200 002420 002444 002045 002140 002453 001224 013115 013133 013322 013412 013445 022005 022014 022032 013053 112006 | 020200 012300 023100 103006 020000 003006 113030 122440 022340 021330 013410 001420 120230 100106 110210 020340 010040 111130''',
	'''001114 001214 001014 001005 001403 002020 002110 002200 002420 002444 002045 002140 002453 001224 013115 013133 013322 013412 013445 022005 022014 022032 013053 112006 | 020200 122300 120340 101300 022206 101000 021306 121330 002240 102430 001406 100110 003020 110230 101140 023010 113440 103230''',
	'''001114 001214 001014 001005 001403 002020 002110 002200 002420 002444 002045 002140 002453 001224 013115 013133 013322 013412 013445 022005 022014 022032 013053 112006 | 120200 102040 101000 010200 010040 010400 003006 001410 110206 021320 121240 022430 013030 122210 113306 012440 100130 111130''',
	'''001114 001214 001014 001005 001403 002020 002110 002200 002420 002444 002045 002140 002453 001224 013115 013133 013322 013412 013445 022005 022014 022032 013053 112006 | 102400 002400 121106 002100 010400 100106 103230 013140 020340 023130 021306 003010 110220 001430 002240 120110 111040 113030''',
	'''001114 001214 001014 001005 001403 002020 002110 002200 002420 002444 002045 002140 002453 001224 013115 013133 013322 013412 013445 022005 022014 022032 013053 112006 | 111406 012300 012100 013000 002100 001406 022430 101140 023240 122330 110206 021310 100120 003030 012440 102310 103140 121330''',
	
	'''001116 001016 001216 001306 001401 012422 002213 002204 002322 002143 002042 002440 002053 001425 013215 013035 013420 013142 013411 022016 022106 022326 013453 112005 | 012100 012400 111150 122100 020300 110250 112230 002410 121340 023040 010030 010140 010010 112420 001450 012040 020130 112130''',
	'''001116 001016 001216 001306 001401 012422 002213 002204 002322 002143 002042 002440 002053 001425 013215 013035 013420 013142 013411 022016 022106 022326 013453 112005 | 002200 013300 102340 010200 022440 010140 010000 101310 003050 112330 020330 113050 020440 112230 112020 020310 110250 002030''',		
	'''001116 001016 001216 001306 001401 012422 002213 002204 002322 002143 002042 002440 002053 001425 013215 013035 013420 013142 013411 022016 022106 022326 013453 112005 | 002200 012400 023400 002400 121350 021350 112030 010210 113040 013440 101130 101240 101110 112220 100150 002340 012230 112430''',	
	'''001116 001016 001216 001306 001401 012422 002213 002204 002322 002143 002042 002440 002053 001425 013215 013035 013420 013142 013411 022016 022106 022326 013453 112005 | 010000 102200 120140 101300 103240 012040 101100 020010 012410 022450 012430 021350 010330 112320 101240 112130 001450 112030''',
	'''001116 001016 001216 001306 001401 012422 002213 002204 002322 002143 002042 002440 002053 001425 013215 013035 013420 013142 013411 022016 022106 022326 013453 112005 | 120000 101100 020000 020300 103250 100150 112430 112330 122240 020440 111140 012110 112120 003050 002210 002230 101430 002340''',
	
	'''001116 001016 001216 001306 001403 112005 001410 001430 001454 002453 002312 002020 002420 011203 002444 013204 013240 022306 022016 022106 022230 013322 013035 013313 | 101440 101140 022250 122440 020340 021350 112110 001450 002210 010330 101000 020010 120200 113300 002100 112320 002230 112010''',
	'''001116 001016 001216 001306 001403 112005 001410 001430 001454 002453 002312 002020 002420 011203 002444 013204 013240 022306 022016 022106 022230 013322 013035 013313 | 002240 012440 013140 012240 111450 001450 112110 020130 103000 101130 112420 023100 002410 012300 112210 101000 110250 101110''',
	'''001116 001016 001216 001306 001403 112005 001410 001430 001454 002453 002312 002020 002420 011203 002444 013204 013240 022306 022016 022106 022230 013322 013035 013313 | 002240 121150 002040 102040 010040 100150 112410 012230 111400 020330 112220 002100 010210 013000 020310 020200 021350 112010''',
	'''001116 001016 001216 001306 001403 112005 001410 001430 001454 002453 002312 002020 002420 011203 002444 013204 013240 022306 022016 022106 022230 013322 013035 013313 | 023240 020140 012440 112310 101430 003050 022200 100150 112120 020340 010030 103050 020200 012110 112410 122300 010400 010010''',
	'''001116 001016 001216 001306 001403 112005 001410 001430 001454 002453 002312 002020 002420 011203 002444 013204 013240 022306 022016 022106 022230 013322 013035 013313 | 010040 113350 010340 120340 101140 110250 112210 002030 121100 012430 112020 010400 101310 102400 012410 012300 112310 003050'''
]

from images2gif import writeGif
import console

save_index = 0
def save(img, name):
	if save_index > 137:
		with open('frames/'+name+'.png', 'wb') as f:
			f.write(img.to_png())

if __name__ == "__main__":
	
	diagram = Diagram(7)
	
	sps = []
	
	with open('superperms.7.txt', 'r') as superperms:
		sps = superperms.read().splitlines()
		
	for index, line in enumerate(sps):
		assert line not in sps[:index], 'duplicate sp'
		assert len(line) == 5907, len(line)
		
		for node in diagram.nodes:
			assert node.perm in line, 'missing perm'

		
	images = []
	
	which = { 
		0: 0, 1: 1, 2: 4, 3: 3, 4: 2,
		5: 5, 6: 9, 7: 8, 8: 7, 9: 6,
		10: 14, 11: 10, 12: 12, 13: 11, 14: 13,
		15: 18, 16: 16, 17: 17, 18: 19, 19: 15
	}	
	
	for addr_index in [5]:
		index = which[addr_index]
		addr = addrs[index]
		
		halves = addr.split(' | ')
		tuple_addrs = sorted(halves[0].split(' '))
		next_addrs = sorted(halves[1].split(' '))
		
		𝒟 = Diagram(7)
				
		all_nodes = []
		tuple_nodes = []
		next_nodes = []
		kernel_node = None
		for tuple_addr in tuple_addrs:
			for node in 𝒟.nodeByAddress[tuple_addr].tuple:
				curr = node.loop.firstNode()
				all_nodes.append(curr)
				tuple_nodes.append(curr)
		for next_addr in next_addrs:
			curr = 𝒟.nodeByAddress[next_addr].loop.firstNode()
			if curr.loop.hasKernelNodes():
				kernel_node = curr			
			all_nodes.append(curr)
			next_nodes.append(curr)
		all_nodes = sorted(all_nodes, key = lambda n: n.address)
		tuple_nodes = sorted(tuple_nodes, key = lambda n: n.address)
		next_nodes = sorted(next_nodes, key = lambda n: n.address)				
		
		for node in next_nodes:
			if len([n for n in node.tuple if n in next_nodes]) is not 1:
				print(str(node) + " | partial tuple " + str(len([n for n in node.tuple if n in next_nodes])))
										
		print("#" + str(index) + ": " + str(len(tuple_addrs)) + " | " + str(len(next_addrs)) + " | knode: " + str(kernel_node))

		
		if index < 5:
			𝒟.pointers = 𝒟.nodeByAddress['000053'].tuple
		elif index < 10:
			𝒟.pointers = 𝒟.nodeByAddress['000002'].tuple	
		elif index < 15:
			𝒟.pointers = 𝒟.nodeByAddress['000002'].tuple	
		else: # < 20:
			𝒟.pointers = 𝒟.nodeByAddress['000053'].tuple
			
		show(𝒟); input("[started] tuples remaining: " + str(len(tuple_addrs)) + " | chains: " + str(len(𝒟.chains)))
		#images.append(ui2pil(draw(𝒟)))
		#save(draw(𝒟), "frame."+"{:0>3}".format(save_index)); save_index += 1
									
		colormaps = list(𝓖5())
		colormapindex = 0		
		for k, base in enumerate(𝒟.bases):
			for i,n in enumerate(base.loopBrethren):
				n.cycle.marker = 1+colormaps[colormapindex][k][i]
				𝒟.makeChain([], [n.cycle])
				
		show(𝒟); input("[colored] tuples remaining: " + str(len(tuple_addrs)) + " | chains: " + str(len(𝒟.chains)))
		#images.append(ui2pil(draw(𝒟)))
		#save(draw(𝒟), "frame."+"{:0>3}".format(save_index)); save_index += 1													

		foundMarker = True
		while foundMarker and len(tuple_addrs):
			foundMarker = False
			for tuple_addr in tuple_addrs:
				if len([n for n in 𝒟.nodeByAddress[tuple_addr].tuple[0].loop.nodes if n.cycle.chain and n.cycle.chain.marker]):
					#𝒟.pointers = [[n for n in node.loop.nodes if n.cycle.chain and n.cycle.chain.marker][0] for node in 𝒟.nodeByAddress[tuple_addr].tuple]
					#show(𝒟); input("[foundMarker:pointed] tuples remaining: " + str(len(tuple_addrs)) + " | chains: " + str(len(𝒟.chains)))
					for node in 𝒟.nodeByAddress[tuple_addr].tuple:
						assert 𝒟.extendLoop(node.loop)
					foundMarker = True
					tuple_addrs.remove(tuple_addr)
					#show(𝒟); input("[foundMarker:extended] tuples remaining: " + str(len(tuple_addrs)) + " | chains: " + str(len(𝒟.chains)))
					continue
					
					
		# unmark chains&cycles
		chain_markers = []
		for chain in 𝒟.chains:
			if chain.marker:
				chain_markers.append((chain, chain.marker))
				chain.marker = None
		cycle_markers = []
		for cycle in 𝒟.cycles:
			if cycle.marker:
				cycle_markers.append((cycle, cycle.marker))
				cycle.marker = None

		# reactivate loops
		reactivated_loops = []
		for loop in 𝒟.loops:
			if not loop.availabled and 𝒟.checkAvailability(loop):
				reactivated_loops.append(loop)
				𝒟.setLoopAvailabled(loop)
													
		show(𝒟); input("[uncolored] tuples remaining: " + str(len(tuple_addrs)) + " | chains: " + str(len(𝒟.chains)))			
		
		𝒟.pointers = next_nodes
		show(𝒟); input("[nexts] all: " + str(len(𝒟.pointers)))			
		
		𝒟.pointers = [node for node in next_nodes if len([n for n in node.loop.nodes if n.cycle.chain])]
		show(𝒟); input("[nexts] chained: " + str(len(𝒟.pointers)))

		𝒟.pointers = [node for node in next_nodes if len([n for n in node.loop.nodes if n.cycle.chain]) is 1]
		show(𝒟); input("[nexts] extending: " + str(len(𝒟.pointers)))

		𝒟.pointers = [node for node in next_nodes if len([n for n in node.loop.nodes if n.cycle.chain]) > 1]
		show(𝒟); input("[nexts] breaking markers: " + str(len(𝒟.pointers)) + " | " + " ".join([str(len([n for n in node.loop.nodes if n.cycle.chain])) for node in 𝒟.pointers]))
														
		'''					
		while len(nodes) > 0:
			for node in nodes:
				#print(str(node) + " | " + str(len([nln for nln in node.loop.nodes if node.cycle.chain is not None])))
				if len([nln for nln in node.loop.nodes if nln.cycle.chain is not None]):
					#print(node)
					assert 𝒟.extendLoop(node.loop)
					nodes.remove(node)
					save(draw(𝒟), "frame."+"{:0>3}".format(save_index)); save_index += 1
		'''
							
		'''
		for tuple_addr in tuple_addrs:
			for node in 𝒟.nodeByAddress[tuple_addr].tuple:
				assert 𝒟.extendLoop(node.loop)
			#images.append(ui2pil(draw(𝒟)))
			save(draw(𝒟), "frame."+"{:0>3}".format(save_index)); save_index += 1
				
		for next_addr in next_addrs:
			assert 𝒟.extendLoop(𝒟.nodeByAddress[next_addr].loop)
			#images.append(ui2pil(draw(𝒟)))
			save(draw(𝒟), "frame."+"{:0>3}".format(save_index)); save_index += 1
		'''
		
		assert len(𝒟.chains) is 1, "!!!incomplete!!!"
		
		#img = draw(𝒟)
		#img.show()
		#input("@" + str(index) + " | α. chains: " + str(len(𝒟.chains)))				
		
		#images.append(ui2pil(img))
		print("@" + str(index) + " | done")
		
		#writeGif('02.gif', images, 0.8)
		#console.quicklook('02.gif')
