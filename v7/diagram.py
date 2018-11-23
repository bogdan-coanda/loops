from superperms import *
from node import *
from cycle import *
from link import *
from loop import *
from common import *
from measures import *
import pickle
import sys


class Diagram (object):
	__slots__ = [
		'spClass', 'kernelSize', 'chainAutoInc',
		'nodes', 'nodeByAddress', 'nodeByPerm', 'startNode',
		'cycles', 'cycleByAddress',
		'chains',
		'links',
		'loops', 'loopByFirstPerm',
		'W', 'H'
	]
	
	def __init__(self, N, kernelSize=1):
		
		self.spClass = N
		self.kernelSize = kernelSize
		self.chainAutoInc = -1
		# [!radial!] self.hasRadialCoords = False
		
		self.generateGraph()
		'''
		# subsets		
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
			
		self.cleanexCount = 0
		
		if self.spClass == 6:
			self.bases = [self.nodeByAddress[addr] for addr in ['00001', '00143', '00201', '00343']]						
		elif self.spClass == 7:
			self.bases = [self.nodeByAddress[addr] for addr in ['000001', '000101', '000201', '000301', '000401']]
		elif self.spClass == 8:
			self.bases = [self.nodeByAddress[addr] for addr in ['0000001', '0000165', '0000201', '0000365', '0000401', '0000565']]
			
		self.walk()
		'''
		
		
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
				if link.node == self.nodes[0]:
					print("[links] type: " + str(type) + " | link: " + str(link))
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
				self.loops[lix].head = sorted(loopNodes, key = lambda n: (n.address[-1], n.address[-2]))[0]
				self.loops[lix].nodes = loopNodes[loopNodes.index(self.loops[lix].head):] + loopNodes[:loopNodes.index(self.loops[lix].head)]
				for ln in loopNodes:
					ln.loop = self.loops[lix]
					lnindex = loopNodes.index(ln)
					ln.loopBrethren = loopNodes[lnindex+1:] + loopNodes[:lnindex]

		# memorize loops by smallest perm
		self.loopByFirstPerm = {}		
		for loop in self.loops:
			# collapse ktype			
			ks = set([node.ktype for node in loop.nodes])
			assert len(ks) == 1
			loop.ktype = list(ks)[0]
			# memorize
			self.loopByFirstPerm[loop.firstPerm()] = loop
		
		''' [!radial!] and maybe more ?…
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
		
		
	# --- pickling --------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
	
	
	def __getstate__(self):
		state = (None, { slot: getattr(self, slot) for slot in self.__slots__ })
					
		# destroy circular references
		for node in self.nodes:
			node.links = None
			node.prevs = None
			
		return state

				
	def __fix_pickling__(self):
		# restore circular references
		for node in self.nodes:
			node.links = [None]*self.spClass
			node.prevs = [None]*self.spClass
					
		for type in range(1, self.spClass):
			for link in self.links[type]:
				link.node.links[type] = link
				link.next.prevs[type] = link
					
							
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
	print("----------")
	print(diagram.nodes[0].links)
	dpkl = diagram.pickle()
	print("diagram pickle size: " + str(len(dpkl)))# + "\n\n" + str(dpkl) + "\n")
	print(diagram.nodes[0].links)
	d2 = Diagram.unpickle(dpkl)
	print(d2.nodes[0].links)
	print("==========")
