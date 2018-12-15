from superperms import *
from node import *
from cycle import *
from link import *
from loop import *
from chain import *
from common import *
from measures import *
from uicanvas import *
import pickle
import sys


class Diagram (object):
	__slots__ = [
		'spClass', 'kernelSize', 'chainAutoInc',
		'nodes', 'nodeByAddress', 'nodeByPerm', 'startNode',
		'cycles', 'cycleByAddress',
		'chains',
		'links',
		'loops', 'loopByFirstAddress',
		'W', 'H',
		'pointers', 'pointer_avlen',
		'tobex_base_count',
		'bases', 'node_tuples', 'loop_tuples',
		'radialLoopsByKType'
	]
	
	def __init__(self, N, kernelSize=1):
		
		self.spClass = N
		self.kernelSize = kernelSize
		self.chainAutoInc = -1
		# [!radial!] self.hasRadialCoords = False
		
		self.generateGraph()

		self.pointers = []
		self.pointer_avlen = self.spClass
		
		# every cycle has its own chain at start
		for cycle in self.cycles:

			# create new chain
			self.chainAutoInc += 1
			new_chain = Chain(self.chainAutoInc)
																			
			# move cycle
			cycle.chain = new_chain
			new_chain.cycles.append(cycle)								
			new_chain.avloops = set([node.loop for node in cycle.nodes])
																																					
			# a new chain is born
			self.chains.add(new_chain)
								
		if self.kernelSize > 0:
			self.generateKernel()

		# tobex = number of chains to be brought together /over/ number of chains added by an extension loop 
		self.tobex_base_count = int((len(self.chains) - 1) / (self.spClass - 2)) # [~] int conversion is always correct here (we can always fully divide)
		# add back already extended (by kernel) loops as they will always be found and extracted when measuring current tobex count
		self.tobex_base_count += len([loop for loop in self.loops if loop.extended])
		print("[diagram] tobex: " + str(self.tobex_base_count))
		
		if self.spClass == 6:
			self.bases = [self.nodeByAddress[addr] for addr in ['00001', '00143', '00201', '00343']]						
		elif self.spClass == 7:
			self.bases = [self.nodeByAddress[addr] for addr in ['000001', '000101', '000201', '000301', '000401']]
		elif self.spClass == 8:
			self.bases = [self.nodeByAddress[addr] for addr in ['0000001', '0000165', '0000201', '0000365', '0000401', '0000565']]
			
		self.walk()
		
		
	def measureTobex(self):
		return self.tobex_base_count - len([loop for loop in self.loops if loop.extended])
		
		
	def generateGraph(self):
		
		self.generateNodes()
		self.generateCycles()
		self.generateLinks()
		self.generateLoops()		
		
		
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

		self.chains = set()								
		self.W = max([cycle.px for cycle in self.cycles]) + Measures.DM
		self.H = max([cycle.py for cycle in self.cycles]) + Measures.DM		
		#print("generated nodes | WxH: " + str(self.W) + "x" + str(self.H))						


	def generateLinks(self):
		
		self.links = [[] for _ in range(self.spClass)]
		
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
			nc += 1
			
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
				
		''' [!radial!] and maybe more ?…								
		# generate <perm, addr> pairing lists for the rest of the nodes in the zeroth cycle, ordered by ktype
		self.kgens = [self.spgen]
		curr_start_node = self.startNode
		for ktype in range(1, self.spClass):
			curr_start_node = curr_start_node.prevs[1].node			
			self.kgens.append(SPGenerator(curr_start_node.perm))	
	
		self.columnLoopsByKType = []
		for ktype in range(self.spClass):
			curr_loops = [self.nodeByPerm[self.kgens[ktype].perms[j]].prevs[1].node.loop for j in range(0, len(self.kgens[ktype].perms), self.spClass)][::(self.spClass-1)]
			for index, loop in enumerate(curr_loops):
				loop.ktype_columnIndex = index # memo its own column index
			self.columnLoopsByKType.append(curr_loops)
			# print(ktype)			
			# for loop in curr_loops:
			# 	print("ktype: " + str(loop.ktype) + " | " + str(loop) + " | ktype_columnIndex: " + str(loop.ktype_columnIndex) + " | ktype_radialIndex: " + str(loop.ktype_radialIndex))	
			
		'''
		
		
	def generateKernel(self):
				
		affected_chains = []
		
		node = self.startNode.prevs[1].node # self.startNode.prevs[1].node
		
		for kern_index in range(self.kernelSize):			
			for column_index in range(self.spClass - 2):
			
				#print("[kernel] k: " + str(kern_index) + " | c: " + str(column_index) + " | node: " + str(node))	
				node.loop.extended = True
			
				for n in node.loop.nodes:				
					affected_chains.append(n.cycle.chain)
					n.cycle.isKernel = True

				# connect last bro
				node.loopBrethren[-1].nextLink = node.loopBrethren[-1].nextLink.next.prevLink = (
					node.loopBrethren[-1].links[3] if column_index != self.spClass - 3 else (node.loopBrethren[-1].links[4] if kern_index != self.kernelSize - 1 else Link(4, node.loopBrethren[-1], self.startNode))
				)

				node = node.loopBrethren[-1].nextLink.next.prevs[1].node																		
																							
		self.chainAutoInc = -1
		new_chain, affected_loops = self.makeChain(affected_chains)
		

	# --- generating ------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	# --- extending -------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	
	
	def extendLoop(self, loop):		
		
		#print("[extend] loop: " + str(loop))
			
		##assert set(list(itertools.chain(*[chain.avloops for chain in diagram.chains]))) == set([loop for loop in diagram.loops if loop.availabled and len([node for node in loop.nodes if node.cycle.chain])])
		#assert set(list(itertools.chain(*[chain.loops for chain in diagram.chains]))) == set([loop for loop in diagram.loops if loop.availabled and len([node for node in loop if node.cycle.chain)])
			
		# assert/return false if not we can't or already did extend		
		if loop.availabled is False or loop.extended is True:
			return False
			
		loop.extended = True
						
		# affected chains are the ones that will be tied together by this extension
		# they're the chains that need to be added back on collapse
		affected_chains = [node.cycle.chain for node in loop.nodes]
						
		# affected loops are avloops set to unavailabled because we're connecting these chains together
		# they're the loops that are re-availabled on collapse
		new_chain, affected_loops = self.makeChain(affected_chains)				
				
		#for node in loop.nodes:
			#assert not node.links[1].next.loop.availabled and not node.prevs[1].node.loop.availabled, "broken extension neighbours!!!"
			
		#for lp in self.loops:
			#if lp.availabled:
				#assert self.checkAvailability(lp), "broken checked loops"
				
		#assert len([node for node in loop.nodes if node.links[1].next.loop.availabled or node.prevs[1].node.loop.availabled]) is 0, "broken extension neighbours!!!"		
		loop.extension_result.setExtensionDetails(new_chain, affected_loops, affected_chains)

		##assert set(list(itertools.chain(*[chain.avloops for chain in diagram.chains]))) == set([loop for loop in diagram.loops if loop.availabled and len([n for n in loop.nodes if n.cycle.chain])])
						
		return True
			
																						
	def collapseBack(self, loop):	
		#print("[collapse] loop: " + str(loop))
		self.breakChain(loop.extension_result)
		loop.extended = False
		
				
	def checkAvailability(self, loop):
		for i in range(1, len(loop.nodes)):
			ichain = loop.nodes[i].cycle.chain
			for j in range(0, i):
				jchain = loop.nodes[j].cycle.chain
				# if the loop would link back to the same chain
				if ichain is jchain:
					return False
		return True
		
			
	def setLoopAvailabled(self, loop):
		# assert len(set([node.cycle.chain for node in loop.nodes])) == len(loop.nodes)
		# assert loop.availabled is False
		loop.availabled = True
		for node in loop.nodes:
			cycle = node.cycle
			cycle.chain.avloops.add(loop)
		
		
	def setLoopUnavailabled(self, loop):
		# assert loop.availabled is True
		loop.availabled = False
		for node in loop.nodes:
			if loop in node.cycle.chain.avloops: # [~] why would the loop not be here ? got removed twice ? got debugged twice over already and proven correct ?
				node.cycle.chain.avloops.remove(loop)
									
	
	def makeChain(self, affected_chains):

		# assert len(set(affected_chains)) == len(affected_chains), "broken affected chains"

		# create new chain
		self.chainAutoInc += 1
		new_chain = Chain(self.chainAutoInc)
		# print("creating new chain: " + str(new_chain))
		affected_loops = []
		
		#assert new_chain.id != 40298
		
		# for each old chain
		for index, old_chain in enumerate(affected_chains):
							
			# move cycles to new chain
			for cycle in old_chain.cycles:
				cycle.chain = new_chain
				new_chain.cycles.append(cycle)
										
			# kill chain
			#print("[makeChain] removing: " + str(old_chain))
			self.chains.remove(old_chain)			
			# if old_chain.id == 33013:
			# 	print("removed old chain: 33013 | while making new chain: " + str(new_chain.id))
																		
		# move/remember loops												
		# for each old chain
		for old_chain in affected_chains:												
			for loop in old_chain.avloops:
				if loop.availabled:
					if not self.checkAvailability(loop):
						# remember erased loop
						self.setLoopUnavailabled(loop)
						affected_loops.append(loop)
					else:
						# move still available loop to new chain
						new_chain.avloops.add(loop)
																																					
		# a new chain is born
		#print("[makeChain] adding: " + str(new_chain))
		self.chains.add(new_chain)
		return (new_chain, affected_loops)	
	

	def breakChain(self, extension_result):
		#print("[breakChain] removing: " + str(new_chain))
				
		# remove/add chains
		self.chains.remove(extension_result.new_chain)
		for chain in extension_result.affected_chains:
			self.chains.add(chain)
			# remap cycles
			for cycle in chain.cycles:
				cycle.chain = chain
			
		# re-available affected loops	(including coerced, if any)
		for loop in extension_result.affected_loops:
			self.setLoopAvailabled(loop)
			
															
	# --- extending -------------------------------------------------------------------------------------------------------------------------------------------------------------- #
	# --- walking ---------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
	
	
	def walk(self):
				
		if self.spClass % 2 is 0:
			
			# define alternating movement methods
			
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
						
			# do the actual walking
			self.__walk(self.bases, adv, jmp)
		
		else: # self.spClass % 2 is 1
			
			# define unidirectional movement methods

			def jmp(pointers, bid): # jmp(from 0 to len(loopBrethren)-1)
				for i in range(len(pointers)):
					pointers[i] = pointers[i].loopBrethren[bid]
						
			def adv(pointers, cid): # adv(0) advances once, to match jmp(0) which jumps once
				for i in range(len(pointers)):
					for _ in range(1+cid):
						pointers[i] = pointers[i].links[1].next
							
			# do the actual walking			
			self.__walk(self.bases, adv, jmp)
			
											
	def __walk(self, base_nodes, adv, jmp): # generate unidirectional tuple
					
		self.node_tuples = []
		self.loop_tuples = []
		queue = [list(base_nodes)]
		
		while len(queue) > 0:
			
			curr_node_tuple = queue.pop()
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
						
				
			pointers = list(curr_node_tuple)
			adv(pointers, 1)
			if pointers[0].tuple is None:
				queue.append(pointers)
	
			pointers = list(curr_node_tuple)
			jmp(pointers, 0)
			if pointers[0].tuple is None:
				queue.append(pointers)
				
		#assert len([n for n in self.nodes if n.tuple is None]) is 0
		print("generated tuples")

			
	# --- walking ---------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
	# --- pointing --------------------------------------------------------------------------------------------------------------------------------------------------------------- #	


	def pointToAddressTuple(self, address):
		self.pointers = list(self.nodeByAddress[address].tuple)

	def measure_avlen(self):
		self.pointer_avlen = min(*[len(chain.avloops) for chain in self.chains])
		return self.pointer_avlen

	def point(self):
		self.pointers = []
			
		if len(self.chains) is 1 and len(list(self.chains)[0].cycles) is len(self.cycles):
			return
				
		chain_avlen, smallest_chain_group = (len(self.cycles), [])
		sorted_chain_groups = sorted(groupby(self.chains, K = lambda chain: len(chain.avloops)).items())
		if len(sorted_chain_groups) > 0:
			chain_avlen, smallest_chain_group	= sorted_chain_groups[0]		
		
		self.pointer_avlen = chain_avlen
		self.pointers += itertools.chain(*[[[n for n in loop.nodes if n.cycle.chain is chain][0] for loop in chain.avloops] if chain_avlen is not 0 else chain.cycles for chain in smallest_chain_group])																				
		#print("[pointing] chain avlen: " + str(chain_avlen))


	# --- pointing --------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
	# --- pickling --------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
	
	
	def __getstate__(self):
		state = (None, { slot: getattr(self, slot) for slot in self.__slots__ })
					
		# destroy self.nodes .links and .prevs
		for node in self.nodes:
			node.links = None
			node.prevs = None
		
		# destroy self.loops.nodes
		for loop in self.loops:
			loop.nodes = [n.address for n in loop.nodes]
			
		# destroy self.nodes.loopBrethren
		for node in self.nodes:
			node.loopBrethren = [n.address for n in node.loopBrethren]
			
		# destroy self .nodes and .loops .tuples
		for node in self.nodes:
			node.tuple = [n.address for n in node.tuple]
		for loop in self.loops:
			loop.tuple = [l.firstAddress() for l in loop.tuple]
			
		return state

				
	def __fix_pickling__(self):
		
		# restore self.nodes .links and .prevs
		for node in self.nodes:
			node.links = [None]*self.spClass
			node.prevs = [None]*self.spClass
					
		for type in range(1, self.spClass):
			for link in self.links[type]:
				link.node.links[type] = link
				link.next.prevs[type] = link
				
		# restore self.loops.nodes
		for loop in self.loops:
			loop.nodes = [self.nodeByAddress[addr] for addr in loop.nodes]
					
		# restore self.nodes.loopBrethren
		for node in self.nodes:
			node.loopBrethren = [self.nodeByAddress[addr] for addr in node.loopBrethren]
			
		# restore self .nodes and .loops .tuples			
		for node in self.nodes:
			node.tuple = [self.nodeByAddress[addr] for addr in node.tuple]
		for loop in self.loops:
			loop.tuple = [self.loopByFirstAddress[addr] for addr in loop.tuple]
							
	def pickle(self):
		pkl = pickle.dumps(self, pickle.HIGHEST_PROTOCOL)
		self.__fix_pickling__()
		return pkl
		
		
	def unpickle(pkl):
		self = pickle.loads(pkl)
		self.__fix_pickling__()
		return self
								
								
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #


if __name__ == "__main__":
		
	diagram = Diagram(6, 1)
	diagram.extendLoop(diagram.nodeByAddress['00001'].loop)
	diagram.collapseBack(diagram.nodeByAddress['00001'].loop)
	show(diagram)
	input()
			
	print("----------")
	print(diagram.nodes[0].links)
	dpkl = diagram.pickle()
	print("diagram pickle size: " + str(len(dpkl)))# + "\n\n" + str(dpkl) + "\n")
	print(diagram.nodes[0].links)
	d2 = Diagram.unpickle(dpkl)
	print(d2.nodes[0].links)
	print("==========")
	
	diagram.extendLoop(diagram.nodeByAddress['00001'].loop)
	diagram.collapseBack(diagram.nodeByAddress['00001'].loop)
	show(diagram)
	input()