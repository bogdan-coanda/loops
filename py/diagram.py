from state import State
from drawn import Drawn
from forest import Forest
from superperms import *
from node import Node
from cycle import Cycle
from loop import Loop
from link import Link
from functools import cmp_to_key
from common import *
from jk import *
from time import time
import pickle
import math
from uicanvas import *
from random import choice
from explorer import groupby


class Diagram (object):
	
	def __init__(self, N, knownID = None):
		# defaults to remember
		#self.k3cc = -2
		#self.k2cc = -1
		#self.k1cc = -1

		self.spClass = N
		self.knownID = knownID
		
		self.generateGraph()
			
		self.arrowCount = [0, 0, 0]
		self.jkcc = 0	
		self.rx_looped_count = 0
		
		# interesting cycles
		self.rx_unreachables = set()
		self.rx_singles = set()
		
		self.chainAutoInc = 0 # first chain is the kernel
															
		self.generateKernel()

		self.startTime = time()
		
		# runtime
		self.chosenLoop = None

				
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
				if self.spClass is 8:
					q8 = gn_address[-1]
					dx = math.floor(RH*math.cos((q8 - 3.5) * 2 * math.pi / 8))
					dy = math.floor(RH*math.sin((q8 - 3.5) * 2 * math.pi / 8))
				elif self.spClass is 7:
					q7 = gn_address[-1]
					dx = math.floor(RH*math.cos((q7 - 3) * 2 * math.pi / 7))
					dy = math.floor(RH*math.sin((q7 - 3) * 2 * math.pi / 7))
				elif self.spClass is 6:
					q6 = gn_address[-1]
					dx = math.floor(RH*math.cos((q6 - 2.5) * 2 * math.pi / 6))
					dy = math.floor(RH*math.sin((q6 - 2.5) * 2 * math.pi / 6))
				
				
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
		#assert len(gn_all) == len(self.perms)
				
				
	def generateLinks(self):
		
		self.links = [[]] * (self.spClass)
		
		for node in self.nodes:
			node.links = [None]*self.spClass
			node.prevs = [None]*self.spClass
		
		for node in self.nodes:
			for type in range(1, self.spClass):
				next = self.nodeByPerm[DX(type, node.perm)]
				link = Link(type, node, next)
				node.links[type] = link
				next.prevs[type] = link
				self.links[type].append(link)
				
				
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
													
		
	def generateKernel(self):
		self.startPerm = self.perms[0]	
		self.startNode = self.nodeByPerm[self.startPerm]									
		return # [~] !!!
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
				for k in range(self.k1cc):
					node.chainID = self.chainAutoInc
					node = appendPath(node, 1)
					
				type = 2
			type = 3
		node.chainID = self.chainAutoInc			
		node = appendPath(node, 3) # circle back		
		assert node is self.startNode
		
		self.tryMakeUnavailable(walked)
		
		
	def loadKnowns(self):
		with open('sols.'+str(self.spClass)+".pkl", 'rb') as infile:
			self.knowns = pickle.load(infile)
			print("[diagram@"+tstr(time()-self.startTime)+"] loaded " + str(len(self.knowns)) + " known solutions found in " + str(self.knowns[-1].jkcc) + " steps | runtime: " + tstr(self.knowns[-1].tdiff))
		
		
	def generateDiagramForKnownID(self, knownID):
		known = self.knowns[knownID]
		𝒟 = Diagram(self.spClass, knownID)
		𝒟.startTime = self.startTime
		for step in known.state:
			𝒟.measureNodes(𝒟.startNode)
			node = 𝒟.nodeByPerm[step.perm]
			𝒟.extendLoop(node)
		return 𝒟

		
	def superperm(self):
		if self.cached_superperm == None:			
			node = self.startNode
			superperm = node.perm
			while node.nextLink.next != self.startNode:						
				node = node.nextLink.next
				superperm += node.perm[-(node.prevLink.type):]
			self.cached_superperm = superperm
			if self.knownID is not None and self.knownID % 1 == 0:			
				print("[diagram:"+str(self.knownID)+" @ "+tstr(time()-self.startTime)+"] generated superperm")
		return superperm
		
		
	def road(self):
		if self.cached_road == None:
			node = self.startNode
			road = str(self.startNode.prevLink.type)
			while node.nextLink.next != self.startNode:						
				node = node.nextLink.next
				road += str(node.prevLink.type)
			
			# reduce format	
			road = road.replace(self.C5, "§")
			road = road.replace("3", "-")
			road = road.replace("2", "|")	
			for i in range(5, 1, -1):
				road = road.replace("1"*i, str(i))
			
			walked = road
			# 'sort' to the first alphanumeric …
			parts = road.strip('-').split('-')
			halls = []
			for _ in range(len(parts)):
				parts = parts[1:] + [parts[0]]
				halls.append("-".join(parts))
				halls.append(halls[-1][::-1])
			road = '-'+sorted(halls)[0]			
										
			self.cached_road = road
			self.road_is_walked = road == walked
			if self.knownID is not None and self.knownID % 1000 == 0:			
				print("[diagram:"+str(self.knownID)+"@"+tstr(time()-self.startTime)+"] generated road: " + road)		
		return road
		
		
	def extender(self):
		if self.cached_extender == None:
			node = self.startNode
			extender = []
		
		def tryex(node):
			if node.nextLink.type == 1:
				return node.nextLink.next
			else:
				assert node.nextLink.type == 2	
				extender.append(node.perm)
				next = pushex(node.nextLink.next)
				assert node.links[1].next == next
				return next
			
		def pushex(node):
			for i in range(self.spClass - 2):
				for j in range(self.spClass - 1):
					
					node = tryex(node)
							
				assert node.nextLink.type == 2
				node = node.nextLink.next							
			return node
																
		for i in range(self.k3cc):
			for j in range(self.k2cc):
				for k in range(self.k1cc):				
								
					node = tryex(node)		
					
				assert (j == self.k2cc - 1 and node.nextLink.type == 3) or node.nextLink.type == 2
				node = node.nextLink.next
									
		self.cached_extender = extender
		if self.knownID is not None and self.knownID % 1000 == 0:			
			print("\n[diagram:"+str(self.knownID)+"@"+tstr(time()-self.startTime)+"] generated extender: " + " ".join([str(node) for node in extender]))		
		return extender
		
		
	def loadExtenders(self):
		with open('extenders.'+str(self.spClass)+".pkl", 'rb') as infile:	
			self.extenders = list(pickle.load(infile))
		self.extenders = [[self.nodeByPerm[perm] for perm in extender] for extender in self.extenders]
		print("Loaded "+str(len(self.extenders))+" extenders")		
		


	# » » » v2 « « « #
	
	# def appendPathV2(self, node, type):
	# 	assert node.nextLink is None
	# 	next = node.links[type].next
	# 	node.nextLink = next.prevLink = node.links[type]
	# 	return next # [~] can be optimized to no function call at all:
	#		# node.nextLink = node.nextLink.next.prevLink = node.links[1]
	# 
	# 
	# def deletePathV2(self, node):
	# 	assert node.nextLink is not None
	# 	next = node.nextLink.next
	# 	node.nextLink = next.prevLink = None		
	# 	return next # [~] can be optimized to no function call at all:
	#		# node.nextLink.next.prevLink = node.nextLink =  None
						
								
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


	def forceUnavailable(self, loops):
		for loop in loops:
			#assert loop.availabled
			loop.availabled = False
			loop.seen = True
			for node in loop.nodes:
				cycle = node.cycle
				cycle.available_loops_count -= 1								
				if cycle.available_loops_count == 0:
					self.rx_singles.discard(cycle)
					if cycle.chained_by_count is 0:
						self.rx_unreachables.add(cycle)
				elif cycle.available_loops_count == 1:
					if cycle.chained_by_count is 0:
						self.rx_singles.add(cycle) 			


	def forceAvailable(self, loops):
		for loop in loops:
			#assert not loop.availabled
			loop.availabled = True
			loop.seen = False
			for node in loop.nodes:
				cycle = node.cycle
				if cycle.available_loops_count == 0:
					self.rx_unreachables.discard(cycle)
					if cycle.chained_by_count is 0:
						self.rx_singles.add(cycle)
				elif cycle.available_loops_count == 1:
					self.rx_singles.discard(cycle)	
				cycle.available_loops_count += 1
						

	def tryMakeUnavailable(self, loops):						
		for loop in loops:
			if loop.availabled and not loop.seen:
				if not self.checkAvailability(loop):
					loop.availabled = False
					for node in loop.nodes:
						cycle = node.cycle
						cycle.available_loops_count -= 1								
						if cycle.available_loops_count == 0:
							self.rx_singles.discard(cycle)
							if cycle.chained_by_count is 0:
								self.rx_unreachables.add(cycle)
						elif cycle.available_loops_count == 1:
							if cycle.chained_by_count is 0:
								self.rx_singles.add(cycle) 
											

	def tryMakeAvailable(self, loops):
		for loop in loops:
			if not loop.availabled and not loop.seen:
				if self.checkAvailability(loop):
					loop.availabled = True
					for node in loop.nodes:
						cycle = node.cycle
						if cycle.available_loops_count == 0:
							self.rx_unreachables.discard(cycle)
							if cycle.chained_by_count is 0:
								self.rx_singles.add(cycle)
						elif cycle.available_loops_count == 1:
							self.rx_singles.discard(cycle)	
						cycle.available_loops_count += 1
				
						
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


	def extendAny(self): # [~]
		if len(self.rx_singles) is not 0:
			#print("singling")
			singleLoops = [[n for n in cy.nodes if n.loop.availabled][0].loop for cy in self.rx_singles]
			avs = [l for l in singleLoops if len([n for n in l.nodes if n.chainID is not None]) is not 0]
			if len(avs) is 0:
				avs = singleLoops
		else:
			avs = [l for l in self.loops if l.availabled and len([n for n in l.nodes if n.chainID is not None]) is not 0]
		if len(avs) is 0:
			return False
		self.chosenLoop = choice(avs)
		### print("[extend] chosen: " + str(self.chosenLoop))
		return self.extendLoop(self.chosenLoop)
		
		
	def collapseAny(self): # [~]
		exs = [l for l in self.loops if l.extended]
		if len(exs) is 0:
			return False
		loop = choice(exs)
		### print("[extend] collapse: " + str(loop))
		return self.collapseLoop(loop)
				
	def measure(self):
		cc, lc = counts(self)
		avs = [l for l in self.loops if l.availabled]
		
		print("[measure] " + str(len(avs))+":"+str(len(self.rx_singles))+":"+str(len(self.rx_unreachables)) + " | chain count: " + str(cc) + " | looped: " + str(lc) + "/" + str(len(self.nodes)) + " | remaining: " + str(len(self.nodes) - lc))		
		return (cc, lc)
			
mkfound = 0

def mk(diagram, lvl=0, a=0, b=0, c=0, seen=[]): # [~] !!! needed so we don't repeat sols
	global mkfound
	
	if lvl == 24:
		show(diagram)
		diagram.measure()
		input("Found #" + str(mkfound))
		input("\n".join(sorted([str(loop) for loop in diagram.loops if loop.extended])))
		mkfound += 1
		return
		
	def inc(fa, fb, fc):
		fc += 1
		if fc is 4:
			fc = 0
			fb += 1
			if fb is 3:
				fb = 0
				fa += 1
		return fa, fb, fc
		
	ra, rb, rc = inc(a, b, c)
	while ra is not 2:
		ravs = [l for l in diagram.loops if l.type() == 5 and len([nln for nln in l.nodes if nln.chainID is not None]) is 0 and l.availabled and not l.seen and l.head.address[0] == str(ra) and l.head.address[1] == str(rb) and l.head.address[2] == str(rc)]		
		ra, rb, rc = inc(ra, rb, rc)
		if len(ravs) is 0:
			return
		
		
	avs = [l for l in diagram.loops if l.type() == 5 and len([nln for nln in l.nodes if nln.chainID is not None]) is 0 and l.availabled and not l.seen and l.head.address[0] == str(a) and l.head.address[1] == str(b) and l.head.address[2] == str(c)]
#	show(diagram)
#	diagram.measure()
#	input("[mk:"+str(lvl)+"] avs: " + str(len(avs)))
		
	lvl_seen = []
		
	for loop in avs:  # [~] need loop.seen…
		
		print("[mk:"+str(lvl)+"] extending: " + str(loop))
		diagram.extendLoop(loop)
		
		flipped = []
		for n in diagram.nodes:
			if n.chainID is not None and n.loop.availabled:
				diagram.forceUnavailable([n.loop])
				flipped.append(n.loop)
				
		if len(diagram.rx_unreachables) is 0:
			ma, mb, mc = inc(a, b, c)
			mk(diagram, lvl+1, ma, mb, mc, seen+lvl_seen)

		diagram.forceAvailable(flipped)
			
		print("[mk:"+str(lvl)+"] collapsing: " + str(loop))
		diagram.collapseLoop(loop)

		lvl_seen.append(loop)
		diagram.forceUnavailable([loop])		
		
	diagram.forceAvailable(lvl_seen)		
		
				
if __name__ == "__main__":
	
	diagram = Diagram(6)
	
	#gloops = groupby(diagram.loops, K = lambda l: l.type())
	#sloops = sorted(diagram.loops, key = lambda l: (l.type(), l.pseudo()))
	
	# groupby(gloops[5], K = lambda loop: groupby([n.address[:2] for n in loop.nodes], G = lambda g: len(g), S = lambda s: ":".join([str(r) for r in reversed(sorted(s.values()))])), G = lambda g: len(g))
	# » » » {'3:1:1': 36, '2:2:1': 36}

	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 5])
			
	mk(diagram)
	
	'''
	diagram = Diagram(7)
	
	while True:
		
		while len(diagram.rx_unreachables) is 0:
			if not diagram.extendAny():
				break
			diagram.measure()
			input()
						
		#show(diagram)
		cc, lc = diagram.measure()
		if lc == len(diagram.nodes):
			if cc is 1:
				show(diagram)
				print("Found…")
				break
			else:
				show(diagram)
				input()
				for _ in range(diagram.spClass):
					diagram.collapseAny()
		elif len(diagram.nodes) - lc < 280:
			show(diagram)
			input()
	
		while len(diagram.rx_unreachables) is not 0:
			while True:
				old_unreachables_count = len(diagram.rx_unreachables)
				l = choice([l for l in diagram.loops if l.extended])
				#print("[xxx] collapsing: " + str(l))
				diagram.collapseLoop(l);
				if len(diagram.rx_unreachables) < old_unreachables_count:
					#print("[xxx] committing")
					break
				else:
					diagram.extendLoop(l)
					#print("[xxx] reverting")

		#show(diagram)
		diagram.measure()
		input()
	'''
	'''
	diagram = Diagram(7)
	show(diagram)
	avs = [l for l in diagram.loops if l.availabled]
	input(str(len(avs))+":"+str(len(diagram.rx_singles))+":"+str(len(diagram.rx_unreachables)))		
				
	while True:
		if len(avs) is 0 or len(diagram.rx_unreachables) is not 0:
			#print("collapsing")
			diagram.collapseLoop(choice([l for l in diagram.loops if l.extended]))
		else:
			if len(diagram.rx_singles) is not 0:
				#print("singling")
				avs = [[n for n in list(diagram.rx_singles)[0].nodes if n.loop.availabled][0].loop]
			#print("extending")
			diagram.extendLoop(choice(avs))
			
		cc, lc = counts(diagram)
		avs = [l for l in diagram.loops if l.availabled]
		
		input("[diagram] " + str(len(avs))+":"+str(len(diagram.rx_singles))+":"+str(len(diagram.rx_unreachables)) + " | chain count: " + str(cc) + " | looped: " + str(lc) + "/" + str(len(diagram.nodes)) + " | remaining: " + str(len(diagram.nodes) - lc))
		
		if cc == 1 and lc == len(diagram.nodes):
			show(diagram)
			print("Found…")
			break
		else:
			#continue
			if  len(diagram.nodes) - lc <= 800:
				show(diagram)
				input()
	'''
	
	# console
	# d = Diagram(6); show(d); d.measure()
	# d.extendAny(); show(d); d.measure()
	# cy = list(d.rx_unreachables)[0]; cy
	# l = [d.nodeByAddress[cy.address+str(i)].loop for i in range(d.spClass)]
	# x = [[n for n in sorted(l[i].nodes, key = lambda n: n.address) if n.chainID is not None and (n.prevLink.type is not 1 or n.nextLink.type is not 1 or n.nextLink.next.nextLink.type is not 1)] for i in range(d.spClass)]


