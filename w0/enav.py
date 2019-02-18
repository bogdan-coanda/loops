import itertools

diagram = None

def extend(addr):
	assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	print(f"[ex] ⇒ extended {addr}")
	return [diagram.nodeByAddress[addr]]
		
def et(addr):
	extended = []
	for i,node in enumerate(diagram.nodeByAddress[addr].tuple):
		assert diagram.extendLoop(node.loop)
		extended.append(node)
	print(f"[et] ⇒ extended {len(extended)} loops in tuple for {addr}")
	return extended
					
def eb(box_addr, key):	
	extended = []
	for i in range(int(diagram.spClass/2-1)):
		for node in diagram.nodeByAddress[box_addr+str(key+2*i)+'0'+str(diagram.spClass-1)].tuple:
			assert diagram.extendLoop(node.loop)
			extended.append(node)
	print(f"[eb] ⇒ extended {len(extended)} loops in blue box tuples for addr:{box_addr} in key:{key}")			
	return extended
	
def eg(box_addr, key):
	extended = []
	for i in range(int(diagram.spClass/2-1)):
		for node in diagram.nodeByAddress[box_addr+str(key+2*i)+'0'+str(diagram.spClass-2)].tuple:
			assert diagram.extendLoop(node.loop)
			extended.append(node)
	print(f"[eg] ⇒ extended {len(extended)} loops in green box tuples for addr:{box_addr} in key:{key}")
	return extended
	
def el(addr, ktype):
	extended = []
	parentLoop = diagram.nodeByAddress[addr].loop
	knodes = [node for node in itertools.chain(*[node.cycle.nodes for node in parentLoop.nodes]) if node.loop.availabled and node.loop.ktype == ktype]
	for i,node in enumerate(knodes):
		if not node.loop.extended:
			assert diagram.extendLoop(node.loop)
			extended.append(node)
	print(f"[el] ⇒ extended {len(extended)} ktype:{ktype} loops for parent {parentLoop}")	
	return extended
		
def elt(addr, ktype):
	extended = []
	parentLoop = diagram.nodeByAddress[addr].loop
	knodes = [node for node in itertools.chain(*[node.cycle.nodes for node in parentLoop.nodes]) if node.loop.availabled and node.loop.ktype == ktype]
	for i,node in enumerate(knodes):
		if not node.loop.extended:
			for n in node.tuple:
				assert diagram.extendLoop(n.loop)
				extended.append(n)
	print(f"[elt] ⇒ extended {len(extended)} ktype:{ktype} loops for parent {parentLoop}")	
	return extended
	
def ec(addr):
	return elt(addr[:-1]+str(diagram.spClass-1), diagram.nodeByAddress[addr].ktype)
	
def est(addr, ktype):
	extended = []
	parentLoop = diagram.nodeByAddress[addr].loop
	knodes = [node for node in itertools.chain(*[node.cycle.nodes for node in parentLoop.nodes]) if node.loop.availabled and node.loop.ktype == ktype]
	headLoops = [node.loop for node in knodes if node.address[-2] in ['0', str(diagram.spClass-2)]]
	knodes = [node for node in knodes if node.loop not in headLoops]	
	for i,node in enumerate(knodes):
		if not node.loop.extended:
			for n in node.tuple:
				assert diagram.extendLoop(n.loop)
				extended.append(n)
	print(f"[est] ⇒ extended {len(extended)} ktype:{ktype} loops for parent {parentLoop}")	
	return extended
	
# ============================================================================================ #

def ot():	
	# keep only full tuples available
	unavailed = []
	nt = 0
	ft = 0
	for t in diagram.loop_tuples:
		if len([l for l in t if not l.availabled]) > 0: #  and not l.extended
			ct = False
			for l in t:
				if l.availabled:
					diagram.setLoopUnavailabled(l)
					unavailed.append(l)
					ct = True
			nt += ct
		else:
			ft += 1
	print(f"[ot] ⇒ unavailabled {len(unavailed)} loops in {nt} incomplete tuples | remaining tuples: {ft}")
	return unavailed	
	
# ============================================================================================ #

def ab(key_addr):
	for node in diagram.nodeByAddress[key_addr].tuple:
		assert diagram.extendLoop(node.loop)
		diagram.collapseBack(node.loop)

# ============================================================================================ #
				
