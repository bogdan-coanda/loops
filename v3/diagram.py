from superperms import *
from groupby import *
from cycle import Cycle
from node import Node
from link import Link
from loop import Loop
from chain import Chain
from uicanvas import show
import itertools
import math


class Diagram (object):
	
	
	def __init__(self, N):
		self.spClass = N
		
		self.generateGraph()
																	
		self.startPerm = self.perms[0]	
		self.startNode = self.nodeByPerm[self.startPerm]									
																	
		self.bases = self.generateKernel()
		
		# subsets		
		self.pointers = []
		self.draw_boxes = []
		
		self.walk()
									
		
	def generateGraph(self):
				
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
		self.cycleByAddress = {}
		self.chains = set()
		
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
				cycle = Cycle(gn_cc, "".join([str(a) for a in gn_address[:-1]]), qx, qy)				
				cycle.available_loops_count = self.spClass
				self.cycles.append(cycle)
				self.cycleByAddress[cycle.address] = cycle
				 
				
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
				
		affected_cycles = []
		bases = []
		
		node = self.startNode.prevs[1].node
		
		while True:
		
			node.loop.extended = True
		
			for n in node.loop.nodes:				
				affected_cycles.append(n.cycle)
				n.cycle.isKernel = True

			#print("[gen:kernel] node: " + str(node) + " | last bro: " + str(node.loopBrethren[-1]))		
			node.loopBrethren[-1].nextLink = node.loopBrethren[-1].nextLink.next.prevLink = node.loopBrethren[-1].links[3]
			node = node.loopBrethren[-1].nextLink.next.prevs[1].node
			bases.append(node)
			#print("[gen:kernel] next node: " + str(node))		
																
			if node is self.startNode.prevs[1].node:
				break
			
		self.chainAutoInc = -1
		new_chain, affected_loops = self.makeChain([], affected_cycles)				
		
		#for base in bases:
			#assert len([node for node in base.loop.nodes if node.links[1].next.loop.availabled or node.prevs[1].node.loop.availabled]) is 0, "broken extension neighbours!!!"		
			
		print("generated kernel")			
		return [bases[-1]] + bases[:-1]
		

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
		affected_cycles = []
		
		for node in loop.nodes:
			if node.cycle.chain:
				affected_chains.append(node.cycle.chain)
			else:
				affected_cycles.append(node.cycle)
		
		new_chain, affected_loops = self.makeChain(affected_chains, affected_cycles)				
		
		#for node in loop.nodes:
			#assert not node.links[1].next.loop.availabled and not node.prevs[1].node.loop.availabled, "broken extension neighbours!!!"
			
		#for lp in self.loops:
			#if lp.availabled:
				#assert len(set([node.cycle.chain.marker for node in lp.nodes if node.cycle.chain and node.cycle.chain.marker])) <= 1, "broken marked loops!!!"
				#assert self.checkAvailability(lp), "broken checked loops"
				
		#assert len([node for node in loop.nodes if node.links[1].next.loop.availabled or node.prevs[1].node.loop.availabled]) is 0, "broken extension neighbours!!!"		
		loop.extension_result = (new_chain, affected_loops, affected_chains, affected_cycles)

		##assert set(list(itertools.chain(*[chain.avloops for chain in diagram.chains]))) == set([loop for loop in diagram.loops if loop.availabled and len([n for n in loop.nodes if n.cycle.chain])])
		
		return True
		
								
	def collapseBack(self, loop):	
		#print("[collapse] loop: " + str(loop))				
		self.breakChain(*(loop.extension_result))
		loop.extension_result = None
		loop.extended = False
																
	
	def checkAvailability(self, loop):
		for i in range(1, len(loop.nodes)):
			ichain = loop.nodes[i].cycle.chain
			if ichain:
				for j in range(0, i):
					jchain = loop.nodes[j].cycle.chain
					# if the loop would link back to the same chain, or to a different colored (marked) chain
					if jchain and (ichain is jchain or (ichain.marker and jchain.marker and ichain.marker is not jchain.marker)):
						return False
		return True
						
										
	def setLoopAvailabled(self, loop):
		#assert loop.availabled is False
		loop.availabled = True
		for node in loop.nodes:
			cycle = node.cycle
			cycle.available_loops_count += 1		
			if cycle.chain: # [~] massively unsafe!!!
				cycle.chain.avloops.add(loop)
		
		
	def setLoopUnavailabled(self, loop):
		#assert loop.availabled is True
		loop.availabled = False
		for node in loop.nodes:
			cycle = node.cycle
			cycle.available_loops_count -= 1
			if cycle.chain and loop in cycle.chain.avloops:
				cycle.chain.avloops.remove(loop)
																		
																											
	def makeChain(self, affected_chains, affected_cycles):

		# create new chain
		self.chainAutoInc += 1
		new_chain = Chain(self.chainAutoInc)
		affected_loops = []
		
		# for each old chain
		for index, old_chain in enumerate(affected_chains):
			
			# check marker			
			if old_chain.marker:
				#assert new_chain.marker is None or new_chain.marker is old_chain.marker, "broken availabled loops!!!"
				new_chain.marker = old_chain.marker
				
			# move cycles to new chain
			for cycle in old_chain.cycles:
				cycle.chain = new_chain
				new_chain.cycles.append(cycle)
										
			# kill chain
			#print("[makeChain] removing: " + str(old_chain))
			self.chains.remove(old_chain)			
			
		# for every other unlooped cycle
		for cycle in affected_cycles:

			# check marker
			if cycle.marker:
				#assert new_chain.marker is None or new_chain.marker is cycle.marker
				new_chain.marker = cycle.marker				
										
			# move cycle
			cycle.chain = new_chain
			new_chain.cycles.append(cycle)

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
						
		# for every other unlooped cycle
		for cycle in affected_cycles:
			for node in cycle.nodes:
				loop = node.loop
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
		
		
	def breakChain(self, new_chain, affected_loops, affected_chains, affected_cycles):
		#print("[breakChain] removing: " + str(new_chain))
		self.chains.remove(new_chain)
		for chain in affected_chains:
			#print("[breakChain] adding: " + str(chain))
			self.chains.add(chain)
			for cycle in chain.cycles:
				cycle.chain = chain
		for cycle in affected_cycles:
			cycle.chain = None
		for loop in affected_loops:
			self.setLoopAvailabled(loop)
					
					
	### ~~~ pointers ~~~ ###																																																				
	

	def walk(self):
		if self.spClass % 2 is 0:
			
			# define alternating movement methods
			
			def jmp(self, bid): # jmp(from 0 to len(loopBrethren)-1)
				for i in range(len(self.pointers)):
					if i % 2 == 0:
						self.pointers[i] = self.pointers[i].loopBrethren[bid]
					else:
						self.pointers[i] = self.pointers[i].loopBrethren[-1-bid]				
						
			def adv(self, cid): # adv(0) advances once, to match jmp(0) which jumps once
				for i in range(len(self.pointers)):
					if i % 2 == 0:
						for _ in range(1+cid):
							self.pointers[i] = self.pointers[i].links[1].next
					else:
						for _ in range(1+cid):
							self.pointers[i] = self.pointers[i].prevs[1].node
				
			Diagram.jmp = jmp
			Diagram.adv = adv
			
			# do the actual walking
			self.dualWalk()
		
		else: # self.spClass % 2 is 1
			
			# define unidirectional movement methods

			def jmp(self, bid): # jmp(from 0 to len(loopBrethren)-1)
				for i in range(len(self.pointers)):
					self.pointers[i] = self.pointers[i].loopBrethren[bid]
						
			def adv(self, cid): # adv(0) advances once, to match jmp(0) which jumps once
				for i in range(len(self.pointers)):
					for _ in range(1+cid):
						self.pointers[i] = self.pointers[i].links[1].next
							
			Diagram.jmp = jmp
			Diagram.adv = adv
			
			# do the actual walking			
			self.monowalk()


	def dualwalk(self): # generate alternating directional tuples
					
		self.tuples = []
		wq = [list(self.bases)]
		while len(wq) > 0:
			
			t = wq.pop()
			for node in t:
				node.tuple = t
				self.tuples.append(t)
				
			self.pointers = list(t)
			self.adv(1)
			if self.pointers[0].tuple is None:
				wq.append(list(self.pointers))
	
			self.pointers = list(t)
			self.jmp(0)
			if self.pointers[0].tuple is None:
				wq.append(list(self.pointers))
	
		#assert len([n for n in self.nodes if n.tuple is None]) is 0																																																				
		print("generated dual tuples")
		
		
	def monowalk(self): # generate unidirectional tuple
					
		self.tuples = []
		wq = [list(self.bases)]
		while len(wq) > 0:
			
			t = wq.pop()
			for node in t:
				node.tuple = t
				self.tuples.append(t)
				
			self.pointers = list(t)
			self.adv(1)
			if self.pointers[0].tuple is None:
				wq.append(list(self.pointers))
	
			self.pointers = list(t)
			self.jmp(0)
			if self.pointers[0].tuple is None:
				wq.append(list(self.pointers))
				
		#assert len([n for n in self.nodes if n.tuple is None]) is 0
		print("generated mono tuples")								
			
			
	def pointToAddressTuple(self, address):
		self.pointers = list(self.nodeByAddress[address].tuple)




if __name__ == "__main__":
	
	diagram = Diagram(7)
	road = []
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	def measure():
		unlooped_cycle_count = len([c for c in diagram.cycles if c.chain is None])
		grouped_cycles_by_av = sorted(groupby([c for c in diagram.cycles if c.chain is None], 
			K = lambda c: (c.available_loops_count, -len([node for node in c.nodes if node.loop.availabled and len([n for n in node.loop.nodes if n.cycle.chain is not None]) > 0]))
		).items())
		avcycle = grouped_cycles_by_av[0][1][0] if len(grouped_cycles_by_av) else None
		avnodes = sorted([node for node in avcycle.nodes if node.loop.availabled], key = lambda node: (-len([n for n in node.loop.nodes if n.cycle.chain is not None]), node.address)) if avcycle else None
		available_loops_count = len([loop for loop in diagram.loops if loop.availabled])	
		# print("--- measure ---")
		# print("unlooped cycles: " + str(unlooped_cycle_count))
		# print("cycle av counts: " + str([((k, q), len(v)) for (k,q),v in grouped_cycles_by_av]))			
		# print("cycles[" + str(grouped_cycles_by_av[0][0]) + "]: " + str(grouped_cycles_by_av[0][1]))		
		# print("avnodes[:"+str(len(avnodes))+"]: " + str(avnodes))
		# print("available loops: " + str(available_loops_count) + "/" + str(len(diagram.loops)) + " | chains: " + str(len(diagram.chains)))
		# print("---------------")
		return (unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes)
								
	def choose(index):
		road.append((index, len(avnodes)))
		print("[road] " + " ".join([str(k)+'/'+str(n) for k,n in road]))
		diagram.pointers = list(avnodes[index].tuple);
								
	def extendPointers():
		for i,node in enumerate(diagram.pointers):
			assert diagram.extendLoop(node.loop)								
								
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	print(" | " + str((len(set(list(itertools.chain(*[chain.avloops for chain in diagram.chains])))), len(set([loop for loop in diagram.loops if loop.availabled and len([node for node in loop.nodes if node.cycle.chain])])))))
									
	diagram.pointers = list(diagram.bases)
	
	for i,n in enumerate(diagram.nodeByAddress['000001'].loopBrethren):
		n.cycle.marker = ((i+0)%5)+1 # 1+colormap[0][i] # 
		diagram.makeChain([], [n.cycle])
		
	for i,n in enumerate(diagram.nodeByAddress['000101'].loopBrethren):
		n.cycle.marker = ((i+1)%5)+1 # 1+colormap[1][i] # 
		diagram.makeChain([], [n.cycle])

	for i,n in enumerate(diagram.nodeByAddress['000201'].loopBrethren):
		n.cycle.marker = ((i+2)%5)+1 # 1+colormap[2][i] # 
		diagram.makeChain([], [n.cycle])
		
	for i,n in enumerate(diagram.nodeByAddress['000301'].loopBrethren):
		n.cycle.marker = ((i+3)%5)+1 # 1+colormap[3][i] # 
		diagram.makeChain([], [n.cycle])
		
	for i,n in enumerate(diagram.nodeByAddress['000401'].loopBrethren):
		n.cycle.marker = ((i+4)%5)+1 # 1+colormap[4][i] # 	
		diagram.makeChain([], [n.cycle])

	#unlooped_cycle_count, grouped_cycles_by_av, available_loops_count = measure()

	print(" | " + str((len(set(list(itertools.chain(*[chain.avloops for chain in diagram.chains])))), len(set([loop for loop in diagram.loops if loop.availabled and len([node for node in loop.nodes if node.cycle.chain])])))))
				
	processed_loops = []						
	for loop in diagram.loops:
		if loop.hasKernelNodes() and loop.availabled:
			
			processed_loops.append(loop)
			diagram.setLoopUnavailabled(loop)
			
			for chain in diagram.chains:
				if loop in chain.avloops:
					chain.avloops.remove(loop)

	print("processed " + str(len(processed_loops)) + " loops | " + str((len(set(list(itertools.chain(*[chain.avloops for chain in diagram.chains])))), len(set([loop for loop in diagram.loops if loop.availabled and len([node for node in loop.nodes if node.cycle.chain])])))))
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
		
	bcc = -1
	ncc = -1
	min = len(diagram.loops) + 1
	
	def next(lvl, road, path = []):
		global bcc, ncc, min
		bcc += 1
		
		chloops = list(sorted(diagram.chains, key = lambda chain: len(chain.avloops))[0].avloops)
		if len(diagram.chains) < min:
			min = len(diagram.chains)
			diagram.pointers = list(itertools.chain(*[l.nodes for l in chloops]))
			show(diagram)
			input("{lvl:"+str(lvl)+"§"+str(ncc)+"§"+str(bcc)+"} | Ongoing | min: " + str(min) + " chains reached | chloops: " + str(len(chloops)))
						
		if bcc % 1000 is 0:
			print("{lvl:"+str(lvl)+"§"+str(ncc)+"§"+str(bcc)+"} | chains: " + str(len(diagram.chains)) + " | chloops: " + str(len(chloops)) + " | road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in road]) + " | " + " ".join([str(k)+'/'+str(n) for k,n,_ in path]))
		#print("{lvl:"+str(lvl)+"} addr: " + " ".join([node.address for _,_,node in road]) + " | " + " ".join([loop.head.address for _,_,loop in path]))							
							
		# checks
		if len(chloops) is 0:
			#show(diagram)
			#print("{lvl:"+str(lvl)+"§"+str(bcc)+"} road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in road]) + " | " + " ".join([str(k)+'/'+str(n) for k,n,_ in path]))
			#print("{lvl:"+str(lvl)+"§"+str(bcc)+"} addr: " + " ".join([node.address for _,_,node in road]) + " | " + " ".join([loop.head.address for _,_,loop in path]))
			#input("Found no chloops")
			
			if len(diagram.chains) is 1:
				show(diagram)
				print("{lvl:"+str(lvl)+"§"+str(bcc)+"} road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in road]) + " | " + " ".join([str(k)+'/'+str(n) for k,n,_ in path]))
				print("{lvl:"+str(lvl)+"§"+str(bcc)+"} addr: " + " ".join([node.address for _,_,node in road]) + " | " + " ".join([loop.head.address for _,_,loop in path]))
				input("Found a solution")
				return True
			else:
				return False
						
		# check if not enough loops to connect all the chains
		#if len(avloops) < (len(diagram.chains) - 1) / 5:
			#return False

		# check if any chains are unreachable
		#if len([chain for chain in diagram.chains if len(chain.avloops) is 0]) > 0:
			#return False
						
		# choose
		#chloops = list(sorted(diagram.chains, key = lambda chain: len(chain.avloops))[0].avloops)
		
		lvl_seen = []
		for chindex, chloop in enumerate(chloops):
			
			#diagram.pointers = list(avloop.nodes)					
			#show(diagram)
			#print("{lvl:"+str(lvl)+"} | avloop: " + str(avloop) + " | .availabled: " + str(avloop.availabled) + " | .extended: " + str(avloop.extended))
			#input("{lvl:"+str(lvl)+"} choosing " + str(avloop) + " | " + str(avindex) + "/" + str(len(avloops)))
			
			# extend
			##assert len(set([n.cycle.chain for n in chloop.nodes if n.cycle.chain])) is len([n.cycle.chain for n in chloop.nodes if n.cycle.chain])
			if diagram.extendLoop(chloop):
				
				# deactivate loops (hack needed because the chain.loops shortcut used in makeChain is broken while next'ing)
				deactivated_loops = []
				for loop in diagram.loops:
					if loop.availabled:
						if not diagram.checkAvailability(loop):
							deactivated_loops.append(loop)
							diagram.setLoopUnavailabled(loop)
				#print("Deactivated " + str(len(deactivated_loops)) + " loops")			
		
				#print("{lvl:"+str(lvl)+"} | » avloop: " + str(avloop) + " | .availabled: " + str(avloop.availabled) + " | .extended: " + str(avloop.extended))
				
				# carry on
				if next(lvl+1, road, path+[(chindex, len(chloops), chloop)]):
					return True
	
				# reactivate loops
				for loop in deactivated_loops:
					diagram.setLoopAvailabled(loop)
	
				# revert
				#print("{lvl:"+str(lvl)+"} | « avloop: " + str(avloop) + " | .availabled: " + str(avloop.availabled) + " | .extended: " + str(avloop.extended))
				#print("{lvl:"+str(lvl)+"} | « .extension_result: " + str('\n'.join([str(x) for x in avloop.extension_result])))
				diagram.collapseBack(chloop)

			# remember
			lvl_seen.append(chloop)
			chloop.seen = True
			diagram.setLoopUnavailabled(chloop)

		# forget
		for loop in lvl_seen:
			diagram.setLoopAvailabled(loop)
			loop.seen = False
						
		return False			


	def back(lvl = 0, road = []):
		global bcc, ncc, min
		bcc += 1
			
		if bcc % 100 is 0:
			print("[lvl:"+str(lvl)+"§"+str(bcc)+"] road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in road]))
		#print("[lvl:"+str(lvl)+"] addr: " + " ".join([node.address for _,_,node in road]))		
	
		# measure	
		unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
		
		# checks
		if avnodes is None:
			#show(diagram)
			print("[lvl:"+str(lvl)+"§"+str(bcc)+"] road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in road]))			
			print("Found no avnodes")
			
			# unmark chains&cycles
			chain_markers = []
			for chain in diagram.chains:
				if chain.marker:
					chain_markers.append((chain, chain.marker))
					chain.marker = None
			cycle_markers = []
			for cycle in diagram.cycles:
				if cycle.marker:
					cycle_markers.append((cycle, cycle.marker))
					cycle.marker = None
			
			##assert set(list(itertools.chain(*[chain.avloops for chain in diagram.chains]))) == set([loop for loop in diagram.loops if loop.availabled and len([n for n in loop.nodes if n.cycle.chain])])
						
			# reactivate loops
			reactivated_loops = []
			for loop in diagram.loops:
				if not loop.availabled and diagram.checkAvailability(loop):
					reactivated_loops.append(loop)
					diagram.setLoopAvailabled(loop)
					# for node in loop.nodes:
					# 	if node.cycle.chain:
					# 		node.cycle.chain.loops.append(loop) # add back to chain.loops shortcut
			#avloops = [loop for loop in diagram.loops if loop.availabled]
			#diagram.pointers = list(itertools.chain(*[l.nodes for l in avloops]))
				
			#min = len(diagram.chains)
			ncc += 1
			
			#show(diagram)
			print("{lvl:"+str(lvl)+"§"+str(ncc)+"§"+str(bcc)+"} | Reactivating " + str(len(reactivated_loops)) + " loops | chains: " + str(len(diagram.chains)))						
			
			# push forward
			if next(lvl, road):
				return True				
								
			# deactivate loops
			for loop in reactivated_loops:
				diagram.setLoopUnavailabled(loop)
				
			# remark chains&cycles
			for chain, marker in chain_markers:
				chain.marker = marker
			for cycle, marker in cycle_markers:
				cycle.marker = marker
					
			return False
					
		if grouped_cycles_by_av[0][0][0] is 0:
			return False
					
		if unlooped_cycle_count is 0 or available_loops_count is 0:
			show(diagram)
			input("Found Something | unlooped:" + str(unlooped_cycle_count) + " | avloops: " + str(available_loops_count))
				
		# choose
		lvl_seen = []
		for avindex in range(len(avnodes)):
			tuple = avnodes[avindex].tuple				
			#diagram.pointers = list(tuple);
								
			# extend
			excc = 0
			for tindex, node in enumerate(tuple):				
				if diagram.extendLoop(node.loop):
					excc += 1
				else:
					break

			# carry on
			if excc is len(tuple):
				if back(lvl+1, road+[(avindex, len(avnodes), avnodes[avindex])]):
					return True
	
			# revert
			for tindex in range(excc)[::-1]:
				diagram.collapseBack(tuple[tindex].loop)

			# remember
			for node in tuple:
				if node.loop.availabled:
					lvl_seen.append(node.loop)
					node.loop.seen = True
					diagram.setLoopUnavailabled(node.loop)

		# forget
		for loop in lvl_seen:
			diagram.setLoopAvailabled(loop)
			loop.seen = False
			
		return False
			
	back()

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	'''
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(0); extendPointers()
	
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(0); extendPointers()

	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(0); extendPointers()
									
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(1); extendPointers()									

	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(0); extendPointers()

	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(0); extendPointers()

	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(0); extendPointers()

	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(0); extendPointers()

	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(1); extendPointers()
	
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(1); extendPointers()
	
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(1); extendPointers()

	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(0); extendPointers()
		
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(1); extendPointers()
	
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(1); extendPointers()
	'#''
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(1); extendPointers()
	
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(1); extendPointers()
	
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(0); extendPointers()
	
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(0); extendPointers()
	
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(1); extendPointers()
	
	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(0); extendPointers()

	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(0); extendPointers()

	unlooped_cycle_count, grouped_cycles_by_av, available_loops_count, avnodes = measure()	
	choose(0); extendPointers()
			
	#for i,node in enumerate(diagram.pointers):
		#show(diagram)
		#input(i)
		#assert diagram.extendLoop(node.loop)
									
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # '''
	show(diagram)
	print("[road] " + " ".join([str(k)+'/'+str(n) for k,n in road]))		
