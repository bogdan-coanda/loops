from superperms import *
from cycle import *
from node import *
from link import *
from loop import *
import math


class Diagram (object):
	
	def __init__(self, N):
		# defaults to remember
		#self.k3cc = -2
		#self.k2cc = -1
		#self.k1cc = -1

		self.spClass = N
		
		self.generateGraph()
							
		self.chainAutoInc = 0 # first chain is the kernel
										
		self.startPerm = self.perms[0]	
		self.startNode = self.nodeByPerm[self.startPerm]									
																						
		# [~] !!! self.generateKernel()
				
		# subsets
		self.pointers = []
		
		
	def generateGraph(self):
		self.k3cc = self.spClass - 2
		self.k2cc = self.spClass - 1
		self.k1cc = self.spClass - 1
		
		self.perms = ["".join([str(p) for p in perm]) for perm in Permutator(list(range(self.spClass))).results]
		self.pids = {}
		for i in range(len(self.perms)):
			self.pids[self.perms[i]] = i		
		
		self.generateNodes()
		self.generateLinks()
		self.generateLoops()		
		
		
	def generateNodes(self):
		
		self.nodes = []
		self.cycles = []
		self.nodeByPerm = {}
		self.nodeByAddress = {}
		
		gn_address = [0] * (self.spClass-1)
		gn_perm = self.perms[0]
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
		
		def genNode(lvl = 2, qx = DM, qy = DM):
			nonlocal gn_address, gn_perm, gn_next, gn_cc, gn_qq, gn_all
			
			if lvl == self.spClass + 1:
				gn_perm = gn_next
				qLast = gn_address[-1]
				dx = math.floor(RH*math.cos((2*qLast - (self.spClass-1)) * math.pi / self.spClass))
				dy = math.floor(RH*math.sin((2*qLast - (self.spClass-1)) * math.pi / self.spClass))				
				
				node = Node(gn_perm, gn_qq, gn_cc, "".join([str(a) for a in gn_address]), qx+dx, qy+dy)
				self.nodes.append(node)
				self.cycles[-1].nodes.add(node)
				self.nodeByPerm[gn_perm] = node
				self.nodeByAddress[node.address] = node
				gn_all.add(gn_perm)
				gn_qq += 1
				gn_next = D1(gn_perm)
				return
				
			if lvl == self.spClass:
				self.cycles.append(Cycle(gn_cc, "".join([str(a) for a in gn_address[:-1]]), qx, qy))
				self.cycles[-1].available_loops_count = self.spClass
				
			for q in range(0, lvl):
				gn_address[lvl - 2] = q
				genNode(lvl + 1, qx + q * xydelta[lvl-2][0], qy + q * xydelta[lvl-2][1])
				gn_next = DX(self.spClass - lvl + 1, gn_perm)

			if lvl == self.spClass:
				gn_cc += 1
																	
		genNode()
		max([node.px for node in self.nodes])
		self.W = max([cycle.px for cycle in self.cycles]) + DM
		self.H = max([cycle.py for cycle in self.cycles]) + DM		
		print("generated nodes | WxH: " + str(self.W) + "x" + str(self.H))
		#assert len(gn_all) == len(self.perms)		
		
		
	def reorder(self, startPerm):
		
		self.nodeByReaddress = {}
		
		gn_address = [0] * (self.spClass-1)
		gn_perm = startPerm
		gn_next = gn_perm
		gn_cc = 0
		
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
		
		def genNode(lvl = 2, qx = DM, qy = DM):
			nonlocal gn_address, gn_perm, gn_next, gn_cc
			
			if lvl == self.spClass + 1:				
				gn_perm = gn_next
				qLast = gn_address[-1]
				dx = math.floor(RH*math.cos((2*qLast - (self.spClass-1)) * math.pi / self.spClass))
				dy = math.floor(RH*math.sin((2*qLast - (self.spClass-1)) * math.pi / self.spClass))				
				
				node = self.nodeByPerm[gn_perm]
				node.readdress = "".join([str(a) for a in gn_address])
				node.px = qx+dx
				node.py = qy+dy
				self.nodeByReaddress[node.readdress] = node

				cycle = node.cycle
				cycle.address = "".join([str(a) for a in gn_address[:-1]])
				cycle.px = qx
				cycle.py = qy
				
				gn_next = D1(gn_perm)
				return
			
			'''	
			if lvl == self.spClass:
			'''	
			for q in range(0, lvl):
				gn_address[lvl - 2] = q
				genNode(lvl + 1, qx + q * xydelta[lvl-2][0], qy + q * xydelta[lvl-2][1])
				gn_next = DX(self.spClass - lvl + 1, gn_perm)

			if lvl == self.spClass:
				gn_cc += 1
																	
		genNode()
		print("reordered nodes")
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
			
		print("generated links")
		
				
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

		print("generated loops")								
		
		
	def generateKernel(self):
		node = self.startNode
		walked = set()
								
		def appendPath(node, type):					
			walked.add(node.loop)
			node.nextLink = node.nextLink.next.prevLink = node.links[type] # self.appendPath(curr, type)
			return node.nextLink.next
	
		type = None							
		for i in range(self.k3cc):
			for j in range(self.k2cc):
				
				if type is not None:
					node.chainID = self.chainAutoInc
					node = appendPath(node, type)
					
				node.cycle.chained_by_count = 1 # generically chained by kernel
				node.cycle.isKernel = True
				for k in range(self.k1cc):
					node.chainID = self.chainAutoInc
					node = appendPath(node, 1)
					
				type = 2
			type = 3
		node.chainID = self.chainAutoInc			
		node = appendPath(node, 3) # circle back		
		assert node is self.startNode
		
		self.tryMakeUnavailable(walked)
		print("generated kernel")		
		
		
	def setLoopAvailabled(self, loop):
		loop.availabled = True
		for node in loop.nodes:
			cycle = node.cycle
			cycle.available_loops_count += 1		
		
		
	def setLoopUnavailabled(self, loop):
		loop.availabled = False
		for node in loop.nodes:
			cycle = node.cycle
			cycle.available_loops_count -= 1								
		
		
	def tryMakeUnavailable(self, loops):						
		for loop in loops:
			if loop.availabled and not loop.seen:
				if not self.checkAvailability(loop):
					self.setLoopUnavailabled(loop)		
					

	def tryMakeAvailable(self, loops):
		for loop in loops:
			if not loop.availabled and not loop.seen:
				if self.checkAvailability(loop):
					self.setLoopAvailabled(loop)
					
																									
	def checkAvailability(self, loop):		
		chainsIDs = set()
		for node in loop.nodes:
			if node.chainID is not None and (node.prevLink is None or node.nextLink is None or node.nextLink.next.nextLink is None):
				print("broken chain!!!")
			if node.chainID is not None:
				if (node.prevLink.type is not 1
				or node.nextLink.type is not 1
				or node.nextLink.next.nextLink.type is not 1
				or node.chainID in chainsIDs):
					return False
				else:
					chainsIDs.add(node.chainID)
		return True
		

	def extendLoop(self, loop):

		# assert/return false if not we can't or already did extend		
		if loop.availabled is False or loop.extended is True:
			return False
		loop.extended = True
									
		# will hold all touched loops			
		walked = set()

		# generate a new chain id			
		self.chainAutoInc += 1
										
		# for each loop node
		for node in loop.nodes:

			# mark & walk the loop node as looped inside the new chain
			node.chainID = self.chainAutoInc
			walked.add(node.loop)
			if node.cycle.chained_by_count is not 0:
				# deletepath(1)
				node.nextLink.next.prevLink = node.nextLink =  None # self.deletePath(node)
										
		# for each loop node (again)
		for node in loop.nodes:																														
			# if its cycle is already looped in
			if node.cycle.chained_by_count is not 0:
				# starting from next(1)
				curr = node.links[1].next
				# until back to the loop node
				while curr is not node:
					# mark & walk the current node
					curr.chainID = self.chainAutoInc
					walked.add(curr.loop)
					# » advance »
					curr = curr.nextLink.next					
					
													
			# else, its cycle is not yet looped it	
			else:
				# starting from next(1)
				curr = node.links[1].next
				# for every 1-path that will be added within this cycle
				for _ in range(self.spClass-1):
					# appendpath(1)
					curr.nextLink = curr.nextLink.next.prevLink = curr.links[1] # self.appendPath(curr, 1)
					# mark & walk the current node
					curr.chainID = self.chainAutoInc
					walked.add(curr.loop)
					# » advance »
					curr = curr.nextLink.next
					
			# the cycle is now looped in
			node.cycle.chained_by_count += 1
			# append the 2-path
			node.nextLink = node.nextLink.next.prevLink = node.links[2] # self.appendPath(node, 2)		

		# for ALL walked nodes, try make unavailable									
		self.tryMakeUnavailable(walked)

		# [~] short-circuit around empty unreachable cycles				
		if len([cycle for cycle in self.cycles if cycle.chained_by_count is 0 and cycle.available_loops_count is 0]) is not 0:
			#print("[short-circuit]")
			self.collapseLoop(loop)
			return False
				
		# extendLoop succeded
		return True
		
																										
	def collapseLoop(self, loop):
		
		# assert/return false if not we can't or did already collapse		
		if not loop.extended:
			return False
		loop.extended = False
			
		# will hold all touched loops			
		walked = set()
					
		# for each loop node
		for node in loop.nodes:
			# print("deleting 2-path: " + str(node.nextLink)) # delete the 2-path
			node.nextLink.next.prevLink = node.nextLink =  None # self.deletePath(node)
			# the cycle is now looped out
			node.cycle.chained_by_count -= 1											
								
		# for each loop node (again)
		for node in loop.nodes:		
			# if its cycle is still looped in
			if node.cycle.chained_by_count is not 0:			
				# appendpath(1)
				node.nextLink = node.nextLink.next.prevLink = node.links[1] # self.appendPath(node, 1)
				# generate a new chain id	
				self.chainAutoInc += 1				
				# mark & walk the loop node as looped inside the new chain
				node.chainID = self.chainAutoInc
				walked.add(node.loop)										
				# starting from next(1)
				curr = node.links[1].next
				# until back to the loop node
				while curr is not node:
					# mark & walk the current node
					curr.chainID = self.chainAutoInc
					walked.add(curr.loop)
					# » advance »
					curr = curr.nextLink.next									

			# else, its cycle is no longer looped in
			else:
				# mark & walk the loop node as unlooped
				node.chainID = None
				walked.add(node.loop)										
				# starting from next(1)
				curr = node.links[1].next
				# for every 1-path that will be removed from this cycle
				for _ in range(self.spClass-1):					
					# print("deleting 1-path: " + str(curr.nextLink)) # deletepath(1)
					next = curr.nextLink.next
					curr.nextLink.next.prevLink = curr.nextLink =  None # self.deletePath(curr)
					# mark & walk the current node
					curr.chainID = None
					walked.add(curr.loop)
					# » advance »
					curr = next				
																
		# for All walked nodes, try make available				
		self.tryMakeAvailable(walked)
		
		# collapseLoop succeded
		return True				

	### ~~~ pointers ~~~ ###																																																				
	
	def walk(self, nodes): # generate tuples
		def jmp(bid):
			for i in range(len(nodes)):
				if i % 2 == 0:
					nodes[i] = nodes[i].loopBrethren[bid]
				else:
					nodes[i] = nodes[i].loopBrethren[-1-bid]
			self.pointers = nodes				
			#print("[jmp]", nodes[0])
				
		def adv(cid):
			for i in range(len(nodes)):
				if i % 2 == 0:
					for _ in range(cid):
						nodes[i] = nodes[i].links[1].next
				else:
					for _ in range(cid):
						nodes[i] = nodes[i].prevs[1].node
			self.pointers = nodes					
			#print("[adv] cid: "+str(cid))
					
		self.tuples = []
		wq = [list(nodes)]
		while len(wq) > 0:
			
			t = wq.pop()
			for node in t:
				node.tuple = t
				self.tuples.append(t)
				
			nodes = list(t)
			adv(1)
			if nodes[0].tuple is None:
				wq.append(list(nodes))
	
			nodes = list(t)
			jmp(0)
			if nodes[0].tuple is None:
				wq.append(list(nodes))
	
		assert len([n for n in self.nodes if n.tuple is None]) is 0																																																				
		
	
	def pointToAddressTuple(self, address):
		self.pointers = list(self.nodeByAddress[address].tuple)

				
	def jmp(self, bid):
		for i in range(len(self.pointers)):
			if i % 2 == 0:
				self.pointers[i] = self.pointers[i].loopBrethren[bid]
			else:
				self.pointers[i] = self.pointers[i].loopBrethren[-1-bid]
		#print("[jmp]", nodes[0])

						
	def adv(self, cid):
		for i in range(len(self.pointers)):
			if i % 2 == 0:
				for _ in range(cid):
					self.pointers[i] = self.pointers[i].links[1].next
			else:
				for _ in range(cid):
					self.pointers[i] = self.pointers[i].prevs[1].node
		#print("[adv] cid: "+str(cid))		
		
