from diagram import *
from time import time
import pickle
from uicanvas import *
from itertools import zip_longest
from types import SimpleNamespace as _
from explorer import groupby


def rundmc(diagram, lvl, bases, avsc, exsc):
		
	print('['+str(lvl)+'] rundmc: ' + '|'.join([str(len(exs)) for exs in exsc]) + ' mx: ' + str(len(diagram.mx_singles)) + ':' + str(len(diagram.mx_sparks)) + '|' + str(len(diagram.mx_unreachable_cycles)))
	show(diagram)
		
	if len(diagram.mx_unreachable_cycles) is not 0:
		input('['+str(lvl)+'] refusing for unreachable cycles: ' + str(len(diagram.mx_unreachable_cycles)))
		return
	
	if len(diagram.mx_singles) is not 0:
		# if we're forced into singles
		print('['+str(lvl)+'] singling...')
		# filter singles for loop connectors
		avs = [n for n in diagram.mx_singles if n.chainID is not 0 and len([nlb for nlb in n.loopBrethren if nlb.looped]) is 0]
		if len(avs) == 0:
			input('['+str(lvl)+'] refusing for no availables in singles: ' + str(len(diagram.mx_singles)))
			return
		# select the first entry
		avs = avs[0:1]
		# find its group id
		id = [bid for bid, b in enumerate(bases) if b.chainID == avs[0].chainID][0]

	else: 
		# select chain with smallest number of extensions done
		id, _ = sorted(list(enumerate(exsc)), key=lambda d: len(d[1]))[0]
		avs = avsc[id]
		
	# [~] make sure to select only avs nodes that don't connect the chains together
	#avs = [n for n in avs if len([nlb for nlb in n.loopBrethren if nlb.looped]) is 0]
	if len(avs) is 0:		
		input('['+str(lvl)+'] refusing for no availables in group: ' + str(id))
		return		

	input('['+str(lvl)+'] carrying on with avs: ' + str(len(avs)) + ' for group: ' + str(id))

	lvl_seen = []		
	cc = 0
	for node in avs:
		if diagram.extendLoop(node):
			
			print('['+str(lvl)+'] extended ' + str(cc) + '/' + str(len(avs)) + " : " + str(node))			
			
			diagram.measureNodes()
			
			# for each extension group, pass down as is or with the current node appended
			next_exsc = [exs + [node] if eid == id else exs for eid, exs in enumerate(exsc)]
			# for each base: if never yet extended, then return the original avsc (passed down), else return filtered availables
			next_avsc = [avsc[bid] if len(next_exsc[bid]) == 0 else [av for av in diagram.drawn.availables if av.chainID == b.chainID and len([avlb for avlb in av.loopBrethren if avlb.looped]) is 0] for bid, b in enumerate(bases)]
			
			rundmc(diagram, lvl+1, bases, next_avsc, next_exsc)
			
			diagram.collapseLoop(node)
			print('['+str(lvl)+'] collapsed ' + str(cc) + '/' + str(len(avs)) + " : " + str(node))
						
			node.loop.availabled = False
			for nn in node.loop.nodes:
				nn.cycle.available_loops_count -= 1
			#sg, sp, un = len(diagram.mx_singles), len(diagram.mx_sparks), len(diagram.mx_unreachable_cycles)
			diagram.tryMakeUnavailable([node])
			#assert (sg, sp, un) == (len(diagram.mx_singles), len(diagram.mx_sparks), len(diagram.mx_unreachable_cycles))
			lvl_seen.append(node)				

		cc += 1
		
	for node in lvl_seen:
		node.loop.availabled = True
		for nn in node.loop.nodes:
			nn.cycle.available_loops_count += 1								
			
		

if __name__ == "__main__":	
	diagram = Diagram(6)
	diagram.startTime = time()
	
	# initial gathering
	splitNode = diagram.nodeByAddress['00001']
	diagram.extendLoop(splitNode)	
	bases = sorted(splitNode.loopBrethren, key = lambda n: n.address)
	#input(bases)
	avsc = [[ncn for ncn in b.cycle.nodes if ncn.loop.availabled and not ncn.extended and len([ncnlb for ncnlb in ncn.loopBrethren if ncnlb.looped]) is 0] for b in bases]
	#input(avsc)
	diagram.collapseLoop(splitNode)
	
	rundmc(diagram, 0, bases, avsc, [[]]*(diagram.spClass-2))
	
	print('~~~')#show(diagram)
