from diagram import *
from time import time
import pickle
from uicanvas import *
import itertools
from types import SimpleNamespace as _
from explorer import groupby


def filterOut(diagram, nodes, bcs):
#	input('[filterOut] bcs: ' + str(bcs))
#	for n in nodes:
#		print(str(n) + ' : ' + str([str(nlb.looped) for nlb in n.loopBrethren]) + ' : ' + str(n.chainID) + ' : ' + str([set(diagram.allConnectedChains(nlb.chainID)) for nlb in n.loopBrethren]) + ':' + str(len([nlb for nlb in n.loopBrethren ## if any brethren
#					if nlb.looped ## are looped
#					and (nlb.chainID == 0 # are kernel nodes 
#						or len(set(diagram.allConnectedChains(nlb.chainID)).difference([n.chainID]).intersection(bcs)) is not 0) ## or intersect a base
#					])))
	return [
		n for n in nodes
		# select nodes with at most a single connection to any of the base chains
		if len([nln for nln in n.loop.nodes if nln.looped and len(set(diagram.allConnectedChains(nln.chainID)).intersection(bcs)) is not 0]) <= 1
	]

#	return [n for n in nodes 
#			if n.chainID is not 0 # no kernel nodes
#			and len([nlb for nlb in n.loopBrethren ## if any brethren
#					if nlb.looped ## are looped
#					and (nlb.chainID == 0 # are kernel nodes 
#						or len(set(diagram.allConnectedChains(nlb.chainID)).difference([n.chainID]).intersection(bcs)) is not 0) ## or intersect a base
#					]) is 0 # no chain connectors
#			]

dmc = 0

def rundmc(diagram, lvl, bases, initials):
	global dmc
	
	bcs = [b.chainID for b in bases if b.looped]
	
	diagram.measureNodes()		
	avg = groupby(filterOut(diagram, diagram.drawn.availables, bcs + [0]), K = lambda n: n.chainID)
	ng = groupby([n for n in diagram.nodes if n.looped], K = lambda n: n.chainID)

	print('['+str(dmc)+']['+str(lvl)+'] mx: ' + str(len(diagram.mx_singles)) + '|' + str(len(diagram.mx_sparks)) + '|' + str(len(diagram.mx_unreachable_cycles)) + ' | avg: ' + ' '.join([str(d[0])+'§'+str(d[1])+'/'+str(d[2]) for d in sorted([(chainID, len(avg.get(chainID) or []), len(ng[chainID])) for chainID in bcs])]))
	
	dmc += 1
				
	#print(' | chains: ' + str(diagram.drawn.chains) + ' | connected: ' + str(diagram.connectedChainPairs))
	#print(' | /g: ' + ' '.join([str(chainID)+'§'+str(len(ng[chainID])) for chainID in ng.keys() if chainID not in bcs]))
	assert (1,2) not in diagram.connectedChainPairs and (1,3) not in diagram.connectedChainPairs and (1,4) not in diagram.connectedChainPairs and (1,5) not in diagram.connectedChainPairs and (2,3) not in diagram.connectedChainPairs and (2,4) not in diagram.connectedChainPairs and (2,5) not in diagram.connectedChainPairs and (3,4) not in diagram.connectedChainPairs and (3,5) not in diagram.connectedChainPairs and (4,5) not in diagram.connectedChainPairs , "connected stuff: " + str(diagram.connectedChainPairs)	
			
	if lvl >= 104:
		show(diagram)
		input()
				
	if len(diagram.mx_unreachable_cycles) is not 0:
		#print('['+str(lvl)+'] refusing for unreachable cycles: ' + str(len(diagram.mx_unreachable_cycles)))
		return
	
	# [~] no chain should be left without an available node in it to connect it to the rest
	if len([c for c in bcs + [0] if not avg.get(c)]) is not 0: # [~] currently just checking the forced bases and kernel
		return
		
	if lvl in range(0, diagram.spClass-2):
		avs = [n for n in initials[lvl] if len([nln for nln in n.loop.nodes if nln.looped]) is 0]
		
	elif len(diagram.mx_singles) is not 0:
		# if we're forced into singles
		#print('['+str(lvl)+'] singling...')

		# [~] filter out kernel singles.
		avs = filterOut(diagram, diagram.mx_singles, bcs)

	elif len(diagram.mx_sparks) is not 0:
		avs = list(diagram.mx_sparks)

	else: 
		# order by base chain with smallest number of extensions done
		avs = list(itertools.chain(*[pp[1] for pp in sorted([pp for pp in avg.items() if pp[0] is not 0], key = lambda pair: len(pair[1]) if pair[0] in bcs else 999999999)]))
		
	# if no node remains…						
	if len(avs) is 0:		
		#print('['+str(lvl)+'] refusing for no availables in group: ' + str(id))
		return		

	#print('['+str(lvl)+'] carrying on with avs: ' + str(len(avs)) + ' for group: ' + str(id))

	lvl_seen = []		
	cc = 0
	for node in avs:
		if diagram.extendLoop(node):			
			#print('['+str(lvl)+'] extended ' + str(cc) + '/' + str(len(avs)) + " : " + str(node))			

			rundmc(diagram, lvl+1, bases, initials)
			
			diagram.collapseLoop(node)
			#print('['+str(lvl)+'] collapsed ' + str(cc) + '/' + str(len(avs)) + " : " + str(node))
						
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
	diagram = Diagram(7)
	diagram.startTime = time()
	
	# initial gathering
	splitNode = diagram.nodeByAddress['000001']
	diagram.extendLoop(splitNode)	
	bases = sorted(splitNode.loopBrethren, key = lambda n: n.address)
	#input(bases)
	diagram.measureNodes()
	initials = [[ncn for ncn in b.cycle.nodes if ncn.loop.availabled and not ncn.extended and len([ncnlb for ncnlb in ncn.loopBrethren if ncnlb.looped]) is 0] for b in bases]
	input(initials)
	
	ccp = splitNode.ext_connectedChains
	
	diagram.collapseLoop(splitNode)
	
	diagram.connectedChainPairs.update(ccp)
	
	rundmc(diagram, 0, bases, initials)
	
	print('~~~')#show(diagram)
	
