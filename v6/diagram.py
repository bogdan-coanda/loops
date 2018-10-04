from superperms import *
from common import *
from cycle import Cycle
from node import Node
from link import Link
from loop import Loop
from chain import Chain
from uicanvas import show
from extension_result import ExtensionResult
import itertools
import math
from time import time
import pickle


class Diagram (object):
	
	
	def __init__(self, N, kernelSize=1, startPerm=None):
		
		self.spClass = N
		self.kernelSize = kernelSize
		self.chainAutoInc = -1
		self.hasRadialCoords = False
		
		self.generateGraph(startPerm)
																																					
		self.startPerm = startPerm or self.perms[0]	
		self.startNode = self.nodeByPerm[self.startPerm]									

		# subsets		
		self.pointers = []
		
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
			
		self.cleanexCount = 0
									
		
	def generateGraph(self, startPerm):
				
		self.perms = ["".join([str(p) for p in perm]) for perm in Permutator(list(range(self.spClass))).results]
		
		self.generateNodes(startPerm)
		self.generateLinks()
		self.generateLoops()		
		
		
	def generateNodes(self, startPerm):
		
		self.nodes = []
		self.cycles = []
		self.nodeByPerm = {}
		self.nodeByAddress = {}
		self.cycleByAddress = {}
		self.chains = set()
		
		gn_address = [0] * (self.spClass-1)
		gn_perm = startPerm or self.perms[0]
		print("[generateNodes] gn_perm: ", gn_perm)
		gn_next = gn_perm
		gn_cc = 0
		gn_qq = 0
		gn_all = set()
		
		DM = 32
		RH = 8

		if self.spClass is 8:
			xydelta = [
				(0, DM*(self.spClass-2)*(self.spClass-1)), 
				(DM*((self.spClass-3)*(self.spClass-2)-1), 0), 
				(DM*(self.spClass-1), 0), 
				(0, DM*(self.spClass)), 
				(DM, 0), 
				(0, DM), 
				(0, 0)]				
		elif self.spClass is 7:
			xydelta = [
				(DM*((self.spClass-3)*(self.spClass-2)-1), 0), 
				(DM*(self.spClass-1), 0), 
				(0, DM*self.spClass), 
				(DM, 0), 
				(0, DM), 
				(0, 0)]
		elif self.spClass is 6:
			xydelta = [
				(0, DM*self.spClass), 
				(DM*(self.spClass-1), 0), 
				(DM, 0), 
				(0, DM), 
				(0, 0)]
		elif self.spClass is 5:
			xydelta = [
				(DM*(self.spClass-1), 0), 
				(DM, 0), 
				(0, DM), 
				(0, 0)]				
		elif self.spClass is 4:
			xydelta = [
				(DM, 0), 
				(0, DM), 
				(0, 0)]				
						
		def genNode(lvl = 2, qx = DM, qy = DM):
			nonlocal gn_address, gn_perm, gn_next, gn_cc, gn_qq, gn_all
			
			if lvl == self.spClass + 1:
				gn_perm = gn_next
				qLast = gn_address[-1]
				dx = RH*math.cos((2*qLast - (self.spClass-1)) * math.pi / self.spClass) # math.floor()
				dy = RH*math.sin((2*qLast - (self.spClass-1)) * math.pi / self.spClass)
				
				### 2 * math.pi * ([0..6] - 3 + 0.5) / self.spClass 
				
				node = Node(gn_perm, gn_qq, gn_cc, "".join([str(a) for a in gn_address]), qx+dx, qy+dy)
				self.nodes.append(node)
				self.cycles[-1].nodes.append(node)
				self.nodeByPerm[gn_perm] = node
				self.nodeByAddress[node.address] = node
				gn_all.add(gn_perm)
				gn_qq += 1
				gn_next = D1(gn_perm)
				return
				
			if lvl == self.spClass:
				cycle = Cycle(gn_cc, "".join([str(a) for a in gn_address[:-1]]), qx, qy)				
				#cycle.available_loops_count = self.spClass
				self.cycles.append(cycle)
				self.cycleByAddress[cycle.address] = cycle
				 
				
			for q in range(0, lvl):
				gn_address[lvl - 2] = q
				genNode(lvl + 1, qx + q * xydelta[lvl-2][0], qy + q * xydelta[lvl-2][1])
				gn_next = DX(self.spClass - lvl + 1, gn_perm)

			if lvl == self.spClass:
				gn_cc += 1
																	
		genNode()
		self.W = max([cycle.px for cycle in self.cycles]) + DM
		self.H = max([cycle.py for cycle in self.cycles]) + DM		
		#print("generated nodes | WxH: " + str(self.W) + "x" + str(self.H))
		#assert len(gn_all) == len(self.perms)		
		
		
	def generateLinks(self):
		
		self.links = [[]] * (self.spClass)
		
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
			
		#print("generated links")
		
				
	def generateLoops(self):
		
		self.loops = []
		lix = -1 # current loop index
		
		for node in self.nodes:			
			
			# everyone holds a link to its cycle center
			node.cycle = self.cycles[node.cycleIndex]
			node.cycleBrethren = [n for n in node.cycle.nodes if n != node]
			
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

		self.loopsByFirstPerm = {}		
		for loop in self.loops:
			# collapse ktype			
			ks = set([node.ktype for node in loop.nodes])
			assert len(ks) == 1
			loop.ktype = list(ks)[0]
			# also, memorize loops by smallest perm
			self.loopsByFirstPerm[loop.firstPerm()] = loop
			
		self.loopsByKType = [[] for _ in range(self.spClass)]
		self.loopsByKType[0] = sorted([loop for loop in self.loops if loop.ktype is 0], key = lambda loop: loop.firstAddress())
		print("[generateLoops] ktype[0][0]: " + str(self.loopsByKType[0][0]) + " | " + str(self.loopsByKType[0][0].firstAddress()))
		
		for index, blue_loop in enumerate(self.loopsByKType[0]):
			blue_loop.ktype_index = index
			for node in blue_loop.nodes:
				other_loop = node.links[1].next.links[1].next.prevs[2].node.loop
				other_loop.ktype_index = index
				assert len(self.loopsByKType[other_loop.ktype]) == index
				self.loopsByKType[other_loop.ktype].append(other_loop)
								
	
	def generateKernel(self):
				
		affected_chains = []
		bases = []
		
		node = self.nodeByPerm[self.perms[0]].prevs[1].node # self.startNode.prevs[1].node
		
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
		new_chain, affected_loops, touched_chains = self.makeChain(affected_chains)
				

	### ~~~ extensions ~~~ ###	
				
		
	def extendLoop(self, loop):		
		
		#print("[extend] loop: " + str(loop))
			
		##assert set(list(itertools.chain(*[chain.avloops for chain in diagram.chains]))) == set([loop for loop in diagram.loops if loop.availabled and len([node for node in loop.nodes if node.cycle.chain])])
		#assert set(list(itertools.chain(*[chain.loops for chain in diagram.chains]))) == set([loop for loop in diagram.loops if loop.availabled and len([node for node in loop if node.cycle.chain)])
			
		# assert/return false if not we can't or already did extend		
		if loop.availabled is False or loop.extended is True:
			return False
			
		loop.extended = True
						
		affected_chains = []
		
		for node in loop.nodes:
			affected_chains.append(node.cycle.chain)
		
		new_chain, affected_loops, touched_chains = self.makeChain(affected_chains)				
		
		#for node in loop.nodes:
			#assert not node.links[1].next.loop.availabled and not node.prevs[1].node.loop.availabled, "broken extension neighbours!!!"
			
		#for lp in self.loops:
			#if lp.availabled:
				#assert self.checkAvailability(lp), "broken checked loops"
				
		#assert len([node for node in loop.nodes if node.links[1].next.loop.availabled or node.prevs[1].node.loop.availabled]) is 0, "broken extension neighbours!!!"		
		loop.extension_result.setDetails(new_chain, affected_loops, affected_chains, touched_chains)

		##assert set(list(itertools.chain(*[chain.avloops for chain in diagram.chains]))) == set([loop for loop in diagram.loops if loop.availabled and len([n for n in loop.nodes if n.cycle.chain])])
		
		return True
										
																						
	def collapseBack(self, loop):	
		#print("[collapse] loop: " + str(loop))
		self.breakChain(loop.extension_result)
		#loop.extension_result = None
		loop.extended = False
																
	
	def checkAvailability(self, loop):
		for i in range(1, len(loop.nodes)):
			ichain = loop.nodes[i].cycle.chain
			for j in range(0, i):
				jchain = loop.nodes[j].cycle.chain
				# if the loop would link back to the same chain, or to a different colored (marked) chain
				if ichain is jchain:
					return False
		return True
						
										
	def setLoopAvailabled(self, loop):
		#assert loop.availabled is False
		loop.availabled = True
		for node in loop.nodes:
			cycle = node.cycle
			cycle.chain.avloops.add(loop)
		
		
	def setLoopUnavailabled(self, loop):
		#assert loop.availabled is True
		loop.availabled = False
		for node in loop.nodes:
			if loop in node.cycle.chain.avloops: # [~] why would the loop not be here ? got removed twice ? got debugged twice over already and proven correct ?
				node.cycle.chain.avloops.remove(loop)
																		
																											
	def makeChain(self, affected_chains):

		# create new chain
		self.chainAutoInc += 1
		new_chain = Chain(self.chainAutoInc)
		# print("creating new chain: " + str(new_chain))
		affected_loops = []
		touched_chains = set()
		
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
						touched_chains.update([node.cycle.chain for node in loop.nodes])
						affected_loops.append(loop)
					else:
						# move still available loop to new chain
						new_chain.avloops.add(loop)
																																					
		# a new chain is born
		#print("[makeChain] adding: " + str(new_chain))
		self.chains.add(new_chain)
		# if new_chain.id == 33013:
		# 	print("made chain: 33013")
		#touched_chains.remove(new_chain)
		return (new_chain, affected_loops, touched_chains)
		
		
	def breakChain(self, extension_result): # touched_chains is unused here
		#print("[breakChain] removing: " + str(new_chain))
		# if extension_result.new_chain.id == 33013:
		# 	print("breaking chain: 33013")
		# print("breaking chain: " + str(extension_result.new_chain))
		self.chains.remove(extension_result.new_chain)
		for chain in extension_result.affected_chains:
			#print("[breakChain] adding: " + str(chain))
			# if chain.id == 33013:
			# 	print("adding back chain: 33013 | while breaking chain: " + str(extension_result.new_chain.id))			
			self.chains.add(chain)
			for cycle in chain.cycles:
				cycle.chain = chain
		for loop in extension_result.affected_loops:
			self.setLoopAvailabled(loop)
					
					
	### ~~~ pointers ~~~ ###																																																				
				
			
	def pointToAddressTuple(self, address):
		self.pointers = list(self.nodeByAddress[address].tuple)


	def superperm(self, start_addr, end_addr):
		curr = self.nodeByAddress[start_addr]
		SP = curr.perm
		#print("SP: " + str(SP))		
		while True:
			nextLink = curr.nextLink if curr.nextLink else (curr.links[2] if curr.loop.extended else curr.links[1])	
			curr = nextLink.next
			if curr.address == start_addr:
				break
			SP += curr.perm[-nextLink.type:]
			if curr.address == end_addr:
				curr.nextLink = Link(0, curr, self.nodeByAddress[start_addr])
				break
		#print("SP: " + str(SP))
		return SP
		#for node in self.nodes:
			#assert node.perm in SP


	def loadExtenders(self):
		with open('extenders.'+str(self.spClass)+".pkl", 'rb') as infile:	
			self.extenders = list(pickle.load(infile))
		self.extenders = [[self.nodeByPerm[perm].loop.firstAddress() for perm in extender] for extender in self.extenders]
		print("Loaded "+str(len(self.extenders))+" extenders")		
					

if __name__ == "__main__":

	diagram = Diagram(6, 1)
	diagram.loadExtenders()
	
	print("len: " + str(len(diagram.extenders[0])) + " | " + str(diagram.extenders[0]))
	
	for i1, l1 in enumerate(diagram.extenders):
		for i2, l2 in enumerate(diagram.extenders):
			if i2 > i1:
				lx = set(l1).intersection(l2)
				if len(lx) >= 24:
					# print("l1: " + str(loops1))
					# print("l2: " + str(loops2))
					# print("lx: " + str(lx)) 
					cloops = [diagram.nodeByAddress[addr].loop for addr in lx]
					blue_count = len([loop for loop in cloops if loop.ktype == 0])
					print(str(i1) + "⋂" + str(i2) + " ⇒ " + str(len(lx)) + " | blues: " + str(blue_count))
					
					if blue_count >= 10:
						for loop in cloops:
							diagram.extendLoop(loop)			
							
						show(diagram); input("roots")
						aloop = diagram.nodeByAddress[list(set(l1).difference(lx))[0]].loop
						print("trying to extend by aloop: " + str(aloop))
						diagram.extendLoop(aloop)
						show(diagram); input("@"+str(i1))																
						diagram.collapseBack(aloop)
						bloop = diagram.nodeByAddress[list(set(l2).difference(lx))[0]].loop
						print("trying to extend by bloop: " + str(bloop))
						diagram.extendLoop(bloop)
						show(diagram); input("@"+str(i2))																
						diagram.collapseBack(bloop)
												
						for loop in reversed(cloops):
							diagram.collapseBack(loop)							
							
	
	grex_blue = groupby(diagram.extenders, K = lambda loops: len([loop for loop in loops if loop.ktype == 0]))
	# grex_blue_14 = groupby(grex_blue[14], K = lambda loops: str(sorted(groupby([loop.ktype for loop in loops], G = lambda g: len(g)).items())))
	# print("\n".join(sorted([str(key)+":"+str(len(vals)) for key,vals in grex_blue_14.items()])))
	# ks = sorted([sorted(groupby([loop.ktype for loop in loops], G = lambda g: len(g)).items()) for loops in grex_blue[14]])
	# print("\n".join([str(k) for k in ks]))
									
	for index, loops in enumerate(grex_blue[14]):
		ktypes = sorted(groupby([loop.ktype for loop in loops], G = lambda g: len(g)).items())
		
		for loop in loops:
			diagram.extendLoop(loop)			
		show(diagram); input(str(index) + " | " + str(ktypes))					
		for loop in reversed(loops):
			diagram.collapseBack(loop)	
			
	# diagram = Diagram(7, 4)								
	# 
	# diagram.extendLoop(diagram.nodeByAddress['000001'].loop)
	#diagram.extendLoop(diagram.nodeByAddress['123001'].loop)
	# diagram.collapseBack(diagram.nodeByAddress['123001'].loop)
	# diagram.collapseBack(diagram.nodeByAddress['000001'].loop)
	# 
	# show(diagram)
	# 
	# diagram.pointers = []
	# affected_nodes = list(itertools.chain(*[loop.nodes for loop in diagram.nodeByAddress['000001'].loop.extension_result.affected_loops]))
	# for cycle in diagram.cycles:
	# 	if cycle.chain in diagram.nodeByAddress['000001'].loop.extension_result.touched_chains:
	# 		diagram.pointers += [node for node in cycle.nodes if node in affected_nodes]
	# show(diagram)
	# 
	# diagram.pointers = []	
	# for cycle in diagram.cycles:
	# 	if cycle.chain in diagram.nodeByAddress['000001'].loop.extension_result.touched_chains:
	# 		diagram.pointers.append(cycle)
	# show(diagram)	
