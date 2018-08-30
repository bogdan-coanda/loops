def extendAddress(diagram, addr):
	loop = diagram.nodeByAddress[addr].loop
	assert diagram.extendLoop(loop)
	
		
def extendColumn(diagram, column_addr, key):
	i = 0
	j = key
	while i < diagram.spClass-1:
		extendAddress(column_addr+str(i)+str(j))
		if j > 0:
			i += 1
			j -= 1
		else:
			i += 2
			j = diagram.spClass - 3

def point(diagram):
	diagram.pointers = []
		
	if len(diagram.chains) is 1 and len(list(diagram.chains)[0].cycles) is len(diagram.cycles):
		return
			
	chain_avlen, smallest_chain_group = (len(diagram.cycles), [])
	sorted_chain_groups = sorted(groupby(diagram.chains, K = lambda chain: len(chain.avloops)).items())
	if len(sorted_chain_groups) > 0:
		chain_avlen, smallest_chain_group	= sorted_chain_groups[0]		
	
	diagram.pointers += itertools.chain(*[[[n for n in loop.nodes if n.cycle.chain is chain][0] for loop in chain.avloops] if chain_avlen is not 0 else chain.cycles for chain in smallest_chain_group])																				
	print("[pointing] chain avlen: " + str(chain_avlen))
	
									
def tonoavail(diagram, addr):
	loop = diagram.nodeByAddress[addr].loop
	loop.seen = True
	diagram.setLoopUnavailabled(loop)
