from superperms import *
from node import *
from cycle import *
from link import *
from chain import *
from loop import *
from common import *
from measures import *
from collections import defaultdict
import functools


class Diagram (object):
	
	
	__slots__ = [
		'spClass',
		'nodes', 'nodeByAddress', 'nodeByPerm', 'startNode',
		'cycles', 'cycleByAddress',
		'links', 'l3s', 'p3s',
		'chains',
		'headCycle', 'openChain',
		'loops', 'loopByFirstAddress', 'radialLoopsByKType',
		'W', 'H',
		'pointers', 'draw_boxes',
		'changelog',
		'__adv__', '__jmp__', #'__nxt__',
		'bases', 'node_tuples', 'loop_tuples',
		'draw_sol_counts'
	]

		
	def __init__(self, N, **kwargs):
				
		self.spClass = N
			
		self.pointers = []
		self.draw_boxes = []
		self.draw_sol_counts = False if 'drawSolCounts' not in kwargs else kwargs['drawSolCounts']
		self.changelog = []
		
		self.loop_tuples = []
		self.openChain = None
		
		self.generateGraph(**kwargs)						


	# --- slots∘init ------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	# --- generators ------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	
	
	def generateGraph(self, **kwargs):
		
		self.generateNodes()
		self.generateCycles()
		self.generateLinks()
		self.generateLoops()
		self.generateChains()
		self.generateKernel(kernelPath=(None if 'kernelPath' not in kwargs else kwargs['kernelPath']), noKernel=(False if 'noKernel' not in kwargs else kwargs['noKernel']))		
		

	def generateNodes(self):

		startPerm = "".join([str(x) for x in range(self.spClass)])		
		spgen = SPGenerator(startPerm)	
		# [!readdr!] self.altgen = self.spgen
		self.nodes = [Node(i, spgen.perms[i], spgen.addrs[i]) for i in range(len(spgen.perms))]
		
		self.nodeByPerm = {}
		self.nodeByAddress = {}		
		for node in self.nodes:
			self.nodeByPerm[node.perm] = node
			self.nodeByAddress[node.address] = node
			
		self.startNode = self.nodeByPerm[startPerm]


	def generateCycles(self):
		
		self.cycles = [Cycle(i, k, v) for i,(k,v) in enumerate(sorted(groupby(self.nodes, K = lambda node: node.address[:-1]).items()))]
					
		self.cycleByAddress = {}
		for cycle in self.cycles:
			self.cycleByAddress[cycle.address] = cycle
										
		for cycle in self.cycles:
			qx = Measures.DM
			qy = Measures.DM
			for lvl, q in enumerate([int(x) for x in cycle.address]):
				qx += q * Measures.xydelta[self.spClass][lvl][0]
				qy += q * Measures.xydelta[self.spClass][lvl][1]
			cycle.px = qx
			cycle.py = qy
			for node in cycle.nodes:
				qLast = int(node.address[-1])
				dx = Measures.RH*math.cos((2*qLast - (self.spClass-1)) * math.pi / self.spClass)
				dy = Measures.RH*math.sin((2*qLast - (self.spClass-1)) * math.pi / self.spClass)
				node.px = qx+dx
				node.py = qy+dy

		self.W = max([cycle.px for cycle in self.cycles]) + Measures.DM
		self.H = max([cycle.py for cycle in self.cycles]) + Measures.DM		
		#print("generated nodes | WxH: " + str(self.W) + "x" + str(self.H))						


	def generateLinks(self):
		
		self.links = [[] for _ in range(self.spClass)]
		self.l3s = {} # node ⇒ [l3a, l3b, l3c]
		self.p3s = defaultdict(lambda: [None]*3)
		
		for node in self.nodes:
			node.links = [None]*self.spClass
			node.prevs = [None]*self.spClass
		
		nc = 0
		for node in self.nodes:
			#if nc % 10000 is 0:
				#print("[links] " + str(nc) + "/" + str(len(self.nodes)))
			for type in range(1, self.spClass):
				next = self.nodeByPerm[DX(type, node.perm)]
				link = Link(type, node, next)
				node.links[type] = link
				next.prevs[type] = link
				self.links[type].append(link)
			# alternative l3s & p3s
			next3a = self.nodeByPerm[L3a(node.perm)]
			next3b = self.nodeByPerm[L3b(node.perm)]
			next3c = self.nodeByPerm[L3c(node.perm)]
			link3a = Link(3, node, next3a)
			link3b = Link(3, node, next3b)
			link3c = Link(3, node, next3c)
			self.l3s[node] = [link3a, link3b, link3c]
			self.p3s[next3a][0] = link3a
			self.p3s[next3b][1] = link3b
			self.p3s[next3c][2] = link3c
			nc += 1
			
		assert len([n for n,ls in self.p3s.items() if len([l for l in ls if l is None])]) == 0
		# assert len([l for l in self.links[1] if l.type is not 1]) is 0 # the original self.links = [[]] * self.spClass was basically broken…
		#print("generated links")
		
				
	def generateLoops(self):
		
		self.loops = []
		lix = -1 # current loop index
		
		for node in self.nodes:			
						
			# if this node has yet to be included in a loop
			if node.loop is None:
				# adapt current loop details to a new loop
				lix += 1				
				# create a new loop
				self.loops.append(Loop(lix))
										
				# collect loop nodes
				loopNodes = [node]
				next = node			
				# for each cycle in the loop extension
				for j in range(self.spClass-2):
					# make the jump into the cycle
					next = next.links[2].next
					# jump the 1-paths												
					for i in range(self.spClass-1):
						next = next.links[1].next
					# the last node is a loop extender
					loopNodes.append(next)
				
				# update loop & nodes details
				self.loops[lix].setNodes(loopNodes)
				for ln in loopNodes:
					ln.loop = self.loops[lix]
					lnindex = loopNodes.index(ln)
					ln.loopBrethren = loopNodes[lnindex+1:] + loopNodes[:lnindex]

		# memorize loops by smallest perm
		self.loopByFirstAddress = {}		
		for loop in self.loops:
			# collapse ktype			
			ks = set([node.ktype for node in loop.nodes])
			assert len(ks) == 1
			loop.ktype = list(ks)[0]
			# memorize
			self.loopByFirstAddress[loop.firstAddress()] = loop
		
		# I. assign radial indexes to ktype loops based on radial connectivity		
		self.radialLoopsByKType = [[] for _ in range(self.spClass)]
		
		# Ia. assign blue radial indexes (will be the same as the blue column indexes)
		self.radialLoopsByKType[0] = sorted([loop for loop in self.loops if loop.ktype is 0], key = lambda loop: loop.firstAddress())
		print("[generateLoops] ktype[0][0]: " + str(self.radialLoopsByKType[0][0]) + " | " + str(self.radialLoopsByKType[0][0].firstAddress()))
		
		for index, blue_loop in enumerate(self.radialLoopsByKType[0]):
			blue_loop.ktype_radialIndex = index
			for node in blue_loop.nodes:
				other_loop = node.links[1].next.links[1].next.prevs[2].node.loop
				other_loop.ktype_radialIndex = index # memo its own radial index
				assert len(self.radialLoopsByKType[other_loop.ktype]) == index
				self.radialLoopsByKType[other_loop.ktype].append(other_loop)
				
								
	def generateChains(self):
		
		self.chains = set()
				
		# every cycle has its own chain initially
		for cycle in self.cycles:

			# create new chain
			new_chain = Chain()
																			
			# move cycle
			new_chain.set_loops([node.loop for node in cycle.nodes])
			cycle.chain = new_chain
			
			# [~][dbg] start cycles list
			new_chain.cycles = [cycle]															
			# a new chain is born
			self.chains.add(new_chain)
			
	
	def generateKernel(self, kernelPath=None, noKernel=False):
		if not noKernel:		
			
			self.headCycle = self.startNode.cycle
			self.openChain = self.headCycle.chain
			
			# setup open chain
			self.openChain.isOpen = True
			self.openChain.headNode = self.startNode
			self.openChain.tailNode = self.startNode.prevs[1].node
			
			# manually turn off loops surrounding the opening		
			self.setLoopUnavailable(self.openChain.headNode.loop)
			self.setLoopUnavailable(self.openChain.tailNode.loop)
			self.setLoopUnavailable(self.openChain.tailNode.prevs[1].node.loop)
				
			if kernelPath == None:
				# append enough cycles to be completable by extensions (extensions add [sp-2] new cycles ⇒ the kernel needs to be of size [y(sp-2)] ⇒ we append [sp-3] cycles)
				for _ in range(self.spClass-3):
					self.connectOpenChain(2)			
			else:
				# append given path 
				for linkType in [int(x) for x in kernelPath if x in '0123456789']:
					self.connectOpenChain(linkType)			
				
		self.changelog.append(('kernel'))
	
	
	# --- generators ------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	# --- internals -------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	
	
	def __makeChain__(self, affected_chains):

		# create new chain
		new_chain = Chain()
		affected_loops = []
		
		# gather together all non-repeating available nodes.loops, this is checkAvailability() behaviour
		seenOnceLoops = []
																	
		# for each old chain
		for index, old_chain in enumerate(affected_chains):
			
			# for each available loop
			for loop in old_chain._loops_: # no need to duplicate list for safety reasons
					
				# if still available
				if loop.available:

					# if not yet seen
					if loop not in seenOnceLoops:
						# seen once
						seenOnceLoops.append(loop)
							
					# if seen once (seen more condition not possible as we're guarded by loop.availabled)
					else:
						# seen more
						seenOnceLoops.remove(loop)
						self.setLoopUnavailable(loop)
						# remember erased loop						
						affected_loops.append(loop)
										
			# kill chain
			self.chains.remove(old_chain)			
																		
		# no need to filter all corresponding remaining nodes
		new_chain.set_loops(seenOnceLoops) # if node.loop.available])
		# [~][dbg] merge cycles lists
		new_chain.cycles = list(itertools.chain(*[chain.cycles for chain in affected_chains]))
		
		# move all cycles new chain (will have to be undone on breakChain())
		for cycle in new_chain.cycles:
			cycle.chain = new_chain
																																					
		# a new chain is born
		self.chains.add(new_chain)
		new_chain.affected_chains = affected_chains
		new_chain.affected_loops = affected_loops
		
		# is open chain?
		if self.openChain in affected_chains:
			new_chain.isOpen = True
			# assume details didn't change (true for extending loops, will be updated afterwards when extending the open chain)
			new_chain.headNode = self.openChain.headNode
			new_chain.tailNode = self.openChain.tailNode
			self.openChain = new_chain
		
		return new_chain
	

	def __breakChain__(self, new_chain):
				
		# remove/add chains
		self.chains.remove(new_chain)
		for chain in new_chain.affected_chains:
			self.chains.add(chain)			
			# remap cycles
			for cycle in chain.cycles:
				cycle.chain = chain
							
		# re-available affected loops
		for loop in reversed(new_chain.affected_loops):
			self.resetLoopAvailable(loop)
			
		# reverse open chain?
		if self.openChain == new_chain:
			oldChain = [chain for chain in new_chain.affected_chains if chain.isOpen]
			assert len(oldChain) == 1
			self.openChain = oldChain[0]
			
	
	# --- internals -------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	# --- basic ops -------------------------------------------------------------------------------------------------------------------------------------------------------------- #
				
				
	def setLoopUnavailable(self, loop):
		# print(f"[setLoopUnavailable] called with {loop}")
		assert loop.available is True
		
		loop.available = False
		self.changelog.append(('unavailabled', loop))		
		
		for node in loop.nodes:
			node.cycle.chain.avcount -= 1

		# print(f"[+][changelog:setLoopUnavailable] {self.changelog[-1]}")
		# print(f"[setLoopUnavailable] ⇒ done")


	def resetLoopAvailable(self, loop):		
		# print(f"[resetLoopAvailable] called with {loop}")
		# print(f"[-][changelog:resetLoopAvailable] {self.changelog[-1]}")		
		assert loop.available == False
		
		lastChange = self.changelog.pop()
		key, _loop = lastChange
		assert key == 'unavailabled' and loop == _loop
								
		loop.available = True
		for node in loop.nodes:
			node.cycle.chain.avcount += 1

		# print(f"[resetLoopAvailable] ⇒ done")
		
		
	# --- basic ops -------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	# --- extending -------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	
	
	def extendLoop(self, loop):				
		# print(f"[extend] loop: {loop}")
						
		# assert/return false if not we can't or already did extend		
		if loop.available is False or loop.extended is True:
			return False
			
		loop.extended = True																		
		new_chain = self.__makeChain__([node.cycle.chain for node in loop.nodes])				

		self.changelog.append(('extended', loop, new_chain))												
		return True
			
																						
	def collapseBack(self, loop):	
		# print(f"[collapse] loop: {loop}")		
		
		lastChange = self.changelog.pop()
		key, _loop, new_chain = lastChange
		assert key == 'extended' and loop == _loop
								
		self.__breakChain__(new_chain)
		loop.extended = False
			
	
	# --- extending -------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
	# --- open chain ------------------------------------------------------------------------------------------------------------------------------------------------------------- #

	
	def isOpenChainPrependable(self, linkType):
		# [~] incorrect, we could also connect to singled extensions
		return len(self.openChain.headNode.prevs[linkType].node.cycle.chain.cycles) == 1
					

	def prependOpenChain(self, linkType):		
		# print(f"[cOc] called with linkType: {linkType}")
		
		if linkType == '3b':
			prevLink = self.p3s[self.openChain.headNode][1]
		else:
			prevLink = self.openChain.headNode.prevs[linkType]
			
		prevNode = prevLink.node
		prevChain = prevNode.cycle.chain

		assert prevChain != self.openChain, 'should have called .isOpenChainPrependable() first'
				
		# manually connect link
		self.openChain.headNode.prevLink = prevNode.nextLink = prevLink		
				
		# make new chain
		new_chain = self.__makeChain__([self.openChain, prevChain])
				
		# update head node
		new_chain.headNode = prevNode.links[1].next
				
		# manually unavail loops surrounding connected link
		def test(loop):
			if loop.available:
				self.setLoopUnavailable(loop)
				new_chain.affected_loops.append(loop)		
		test(prevLink.node.loop)
		test(prevLink.node.prevs[1].node.loop)
		test(prevLink.node.links[1].next.loop)
		# if nextLink.next.loop.available:
		# 	self.setLoopUnavailable(nextLink.next.loop)
		# 	new_chain.affected_loops.append(nextLink.next.loop)			
		# if nextLink.next.prevs[1].node.loop.available:
		# 	self.setLoopUnavailable(nextLink.next.prevs[1].node.loop)
		# 	new_chain.affected_loops.append(nextLink.next.prevs[1].node.loop)						
		# if nextLink.next.prevs[1].node.prevs[1].node.loop.available:
		# 	self.setLoopUnavailable(nextLink.next.prevs[1].node.prevs[1].node.loop)
		# 	new_chain.affected_loops.append(nextLink.next.prevs[1].node.prevs[1].node.loop)									

		self.changelog.append(('prepended', linkType, prevLink, new_chain))
		# print(f"[cOc] ⇒ done")
		return True
		
		
	def revertOpenChainPrepend(self):		
		# print(f"[rOc] called")
		
		key, linkType, prevLink, new_chain = self.changelog.pop()
		assert key == 'prepended'

		self.__breakChain__(new_chain)						
								
		assert self.openChain.headNode.prevLink == prevLink
		
		# manually remove link
		self.openChain.headNode.prevLink = prevLink.node.nextLink = None
		# print(f"[rOc] ⇒ done")
				
		
	def isOpenChainConnectable(self, linkType):
		# [~] incorrect, we could also connect to singled extensions
		return len(self.openChain.tailNode.links[linkType].next.cycle.chain.cycles) == 1

								
	def connectOpenChain(self, linkType):		
		# print(f"[cOc] called with linkType: {linkType}")
		
		if linkType == '3b':
			nextLink = self.l3s[self.openChain.tailNode][1]
		else:
			nextLink = self.openChain.tailNode.links[linkType]
			
		nextNode = nextLink.next
		nextChain = nextNode.cycle.chain

		assert nextChain != self.openChain, 'should have called .isOpenChainConnectable() first'
				
		# manually connect link
		self.openChain.tailNode.nextLink = nextNode.prevLink = nextLink		
				
		# make new chain
		new_chain = self.__makeChain__([self.openChain, nextChain])
				
		# update tail node
		new_chain.tailNode = nextNode.prevs[1].node
				
		# manually unavail loops surrounding connected link
		if nextLink.next.loop.available:
			self.setLoopUnavailable(nextLink.next.loop)
			new_chain.affected_loops.append(nextLink.next.loop)			
		if nextLink.next.prevs[1].node.loop.available:
			self.setLoopUnavailable(nextLink.next.prevs[1].node.loop)
			new_chain.affected_loops.append(nextLink.next.prevs[1].node.loop)						
		if nextLink.next.prevs[1].node.prevs[1].node.loop.available:
			self.setLoopUnavailable(nextLink.next.prevs[1].node.prevs[1].node.loop)
			new_chain.affected_loops.append(nextLink.next.prevs[1].node.prevs[1].node.loop)						
													
		self.changelog.append(('connected', linkType, nextLink, new_chain))
		# print(f"[cOc] ⇒ done")
		return True
		
	
	def revertOpenChainConnect(self):		
		# print(f"[rOc] called")
		
		key, linkType, nextLink, new_chain = self.changelog.pop()
		assert key == 'connected'

		self.__breakChain__(new_chain)						
								
		assert self.openChain.tailNode.nextLink == nextLink
		
		# manually remove link
		self.openChain.tailNode.nextLink = nextLink.next.prevLink = None
		# print(f"[rOc] ⇒ done")
		
		
	# --- open chain ------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
	# --- walk/tuples ------------------------------------------------------------------------------------------------------------------------------------------------------------ #
	
	def walk(self, bases, alternating):
		
		if alternating:
			
			# define alternating movement methods
			# [!] needs to be called with bases like [.openChain.headNode, .openChain.tailNode.prevs[1].node]
			# ... because we need to keep the odd pointers on the starting nodes for extending loops corresponding to loops starting at the even pointers
			# ... in this regard, we are forced to call adv/jmp instead of a generic nxt function to advance the pointers
			def jmp(pointers, bid): # jmp(from 0 to len(loopBrethren)-1)
				for i in range(len(pointers)):
					if i % 2 == 0:
						pointers[i] = pointers[i].loopBrethren[bid]
					else:
						pointers[i] = pointers[i].loopBrethren[-1-bid]				
						
			def adv(pointers, cid): # adv(0) advances once, to match jmp(0) which jumps once
				for i in range(len(pointers)):
					if i % 2 == 0:
						for _ in range(1+cid):
							pointers[i] = pointers[i].links[1].next
					else:
						for _ in range(1+cid):
							pointers[i] = pointers[i].prevs[1].node			
			
			# def nxt(pointers, lid): # go to the next node by link type
			# 	for i in range(len(pointers)):
			# 		if i % 2 == 0:
			# 			pointers[i] = pointers[i].links[lid].next
			# 		else:
			# 			pointers[i] = pointers[i].prevs[lid].node				
				
		else: 
			
			# define unidirectional movement methods

			def jmp(pointers, bid): # jmp(from 0 to len(loopBrethren)-1)
				for i in range(len(pointers)):
					pointers[i] = pointers[i].loopBrethren[bid]
						
			def adv(pointers, cid): # adv(0) advances once, to match jmp(0) which jumps once
				for i in range(len(pointers)):
					for _ in range(1+cid):
						pointers[i] = pointers[i].links[1].next
				
			# def nxt(pointers, lid): # go to the next node by link type
			# 	for i in range(len(pointers)):
			# 		pointers[i] = pointers[i].links[lid].next
										
		self.__jmp__ = jmp
		self.__adv__ = adv
		self.bases = bases
		
		# do the actual walking			
		self.__walk__(self.bases, adv, jmp)
											
											
	def __walk__(self, base_nodes, adv, jmp):
					
		self.node_tuples = []
		self.loop_tuples = []
		for node in self.nodes:
			node.tuple = node.loop.tuple = None
		
		adv_queue = [list(base_nodes)]
		jmp_queue = []
		while len(adv_queue) > 0 or len(jmp_queue) > 0:
			
			curr_node_tuple = adv_queue.pop() if len(adv_queue) else jmp_queue.pop()
			if curr_node_tuple[0].tuple is not None:
				continue
				
			self.node_tuples.append(curr_node_tuple)			
			for node in curr_node_tuple:
				node.tuple = curr_node_tuple				
								
			curr_loop_tuple = tuple([node.loop for node in curr_node_tuple])
			if curr_loop_tuple[0].tuple is None:
				self.loop_tuples.append(curr_loop_tuple)				
				for loop in curr_loop_tuple:
					loop.tuple = curr_loop_tuple				

			# for i in range(1, self.spClass):																						
			# 	pointers = list(curr_node_tuple)
			# 	nxt(pointers, i)
			# 	if pointers[0].tuple is None:
			# 		queue.append(pointers)
			
			pointers = list(curr_node_tuple)
			adv(pointers, 1)
			if pointers[0].tuple is None:
				adv_queue.append(pointers)
	
			pointers = list(curr_node_tuple)
			jmp(pointers, 0)
			if pointers[0].tuple is None:
				jmp_queue.append(pointers)

																																																											
		if len([n for n in self.nodes if n.tuple is None]) is not 0:
			self.pointers = [n for n in self.nodes if n.tuple is None]
			import uicanvas
			uicanvas.show(self)
			input2(f"[__walk__] broken!")
		print("generated tuples")
		
																								
	# --- walk/tuples ------------------------------------------------------------------------------------------------------------------------------------------------------------ #	
	# --- pointers --------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
	
	def point(self):
		self.pointers = []
			
		if len(self.chains) is 1 and len(list(self.chains)[0].cycles) is len(self.cycles):
			return
				
		chain_avlen, smallest_chain_group = (len(self.cycles), [])
		sorted_chain_groups = sorted(groupby(self.chains, K = lambda chain: chain.avcount).items())
		if len(sorted_chain_groups) > 0:
			chain_avlen, smallest_chain_group	= sorted_chain_groups[0]		
		
		self.pointers = list(itertools.chain(*[[[n for n in loop.nodes if n.cycle.chain is chain][0] for loop in chain.avloops()] if chain_avlen is not 0 else chain.cycles for chain in smallest_chain_group]))

	def point_next_tuple(self, linkType):
		if len(self.pointers):
			self.pointers = self.pointers[0].links[linkType].next.tuple

	# --- pointers --------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

				
if __name__ == "__main__":
	from uicanvas import *

	diagram = Diagram(6, kernelPath='')	
	
	diagram.connectOpenChain(2)
	diagram.revertOpenChainConnect()

	diagram.prependOpenChain(3)
	diagram.revertOpenChainPrepend()

	diagram.extendLoop(diagram.nodeByAddress['00041'].loop)
	diagram.collapseBack(diagram.nodeByAddress['00041'].loop)

	assert sum([len(chain.cycles) for chain in diagram.chains]) == len(diagram.cycles)
	assert sum([chain.avcount for chain in diagram.chains]) == len([n for n in diagram.nodes if n.loop.available])

	diagram.walk([diagram.openChain.headNode, diagram.openChain.tailNode], True)
	diagram.pointers = [diagram.openChain.headNode, diagram.openChain.tailNode]
	diagram.__jmp__(diagram.pointers, 1)
			
	show(diagram)	
