from superperms import *
from node import *
from cycle import *
from link import *
from chain import *
from loop import *
from common import *
from measures import *
from collections import defaultdict


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
		'changelog'
	]

		
	def __init__(self, N):
				
		self.spClass = N
			
		self.pointers = []
		self.draw_boxes = []
		self.changelog = []
		
		self.generateGraph()						
		
								
	def generateGraph(self):
		
		self.generateNodes()
		self.generateCycles()
		self.generateLinks()
		self.generateLoops()
		self.generateChains()
		self.generateKernel()		
		

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
			new_chain.avnodes = set(cycle.nodes)
			cycle.chain = new_chain
			
			# [~][dbg] start cycles list
			new_chain.cycles = [cycle]															
			# a new chain is born
			self.chains.add(new_chain)
			
	
	def generateKernel(self):
		
		self.headCycle = self.startNode.cycle
		self.openChain = self.headCycle.chain
		
		# set tail node
		self.openChain.isOpen = True
		self.openChain.tailNode = self.startNode.prevs[1].node
		
		# append enough cycles to be completable by extensions (extensions add [sp-2] new cycles ⇒ the kernel needs to be of size [y(sp-2)] ⇒ we append [sp-3] cycles)
		for _ in range(self.spClass-3):
			self.connectOpenChain(2)
			
		self.changelog.append(('kernel'))
	
	# --- generating ------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	# --- basic ops -------------------------------------------------------------------------------------------------------------------------------------------------------------- #
		
	def setLoopUnavailable(self, loop):
		# print(f"[setLoopUnavailable] called with {loop}")
		assert loop.available is True
		
		loop.available = False
		unavailabled_chain_node_pairs = []				
		self.changelog.append(('unavailabled', loop, unavailabled_chain_node_pairs))		
		
		for node in loop.nodes:
			if node in node.cycle.chain.avnodes: # [~] why would the loop not be here ? got removed twice ? got debugged twice over already and proven correct ? as is it needed during makeChain ?
				node.cycle.chain.avnodes.remove(node)
				unavailabled_chain_node_pairs.append((node.cycle.chain, node))
		# print(f"[+][changelog:setLoopUnavailable] {self.changelog[-1]}")
		# print(f"[setLoopUnavailable] ⇒ done")


	def resetLoopAvailable(self, loop):
		
		# print(f"[resetLoopAvailable] called with {loop}")
		# print(f"[-][changelog:resetLoopAvailable] {self.changelog[-1]}")		
		assert loop.available == False
		
		lastChange = self.changelog.pop()
		key, _loop, unavailabled_chain_node_pairs = lastChange
		assert key == 'unavailabled' and loop == _loop
								
		loop.available = True
		for ch, n in unavailabled_chain_node_pairs:
			ch.avnodes.add(n)
		# print(f"[resetLoopAvailable] ⇒ done")
		
		
	# --- basic ops -------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	# --- open chain ------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	
	def connectOpenChain(self, linkType):
		
		# print(f"[cOc] called with linkType: {linkType}")
		# print("\n".join([str((i, self.changelog[i])) for i in range(len(self.changelog))]))
		
		nextLink = self.openChain.tailNode.links[linkType]
		nextNode = nextLink.next
		nextChain = nextNode.cycle.chain
		# print(f"[cOc] nextChain: {nextChain} | openChain: {self.openChain}")
		if nextChain == self.openChain:
			# print(f"[cOc] ⇒ self-connect // giving up")
			return False
				
		# connect link
		self.openChain.tailNode.nextLink = nextNode.prevLink = nextLink
		self.openChain.tailNode = nextNode.prevs[1].node
				
		# update chain avnodes
		openLoops = set([n.loop for n in self.openChain.avnodes])
		assert len(openLoops) == len(self.openChain.avnodes)				
		nextLoops = set([n.loop for n in nextChain.avnodes])
		assert len(nextLoops) == len(nextChain.avnodes)		
		commonLoops = openLoops.intersection(nextLoops)
		commonLoops.add(nextLink.node.loop)
		commonLoops.add(nextLink.node.prevs[1].node.loop)
		commonLoops.add(nextLink.next.loop)
		commonLoops = list(commonLoops)
		prevNodes = set(self.openChain.avnodes)
		self.openChain.avnodes.difference_update([n for n in self.openChain.avnodes if n.loop in commonLoops])
		self.openChain.avnodes.update(nextChain.avnodes.difference([n for n in nextChain.avnodes if n.loop in commonLoops]))
		
		# kill common loops
		unavailabledCommonLoops = []
		for loop in commonLoops:
			if loop.available:
				self.setLoopUnavailable(loop)
				unavailabledCommonLoops.append(loop)				
				
		# add new cycle to chain
		nextNode.cycle.chain = self.openChain
		self.openChain.cycles.append(nextNode.cycle)

		# remove overwritten chain
		self.chains.remove(nextChain)
		self.changelog.append(('connected', linkType, nextLink, commonLoops, unavailabledCommonLoops, prevNodes, nextChain))
		# print(f"[+][changelog:connectOpenChain] {self.changelog[-1]}")
		# print(f"[cOc] ⇒ done")
		return True
		
	
	def revertOpenChain(self):
		
		# print(f"[rOc] called")
		# print("\n".join([str((i, self.changelog[i])) for i in range(len(self.changelog))]))
		
		# print(f"[-][changelog:revertOpenChain] {self.changelog[-1]}")
		lastChange = self.changelog.pop()
		key, linkType, nextLink, commonLoops, unavailabledCommonLoops, prevNodes, nextChain = lastChange
		assert key == 'connected'
		
		self.chains.add(nextChain)
		
		self.openChain.cycles.remove(nextLink.next.cycle)
		nextLink.next.cycle.chain = nextChain
		
		for loop in reversed(unavailabledCommonLoops):
			self.resetLoopAvailable(loop)
			
		self.openChain.avnodes = prevNodes
				
		self.openChain.tailNode = nextLink.node
		self.openChain.tailNode.nextLink = nextLink.next.prevLink = None
		# print(f"[rOc] ⇒ done")
		
		
if __name__ == "__main__":
	from uicanvas import *

	diagram = Diagram(6)	
	show(diagram)	
