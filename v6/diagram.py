from superperms import *
from common import *
from cycle import Cycle
from node import Node
from link import Link
from loop import Loop
from chain import Chain
from uicanvas import show, setRadialCoords
from extension_result import ExtensionResult
import itertools
import math
from time import time
import pickle
from measures import *


class Diagram (object):

		
	def __init__(self, N, kernelSize=1):
		
		self.spClass = N
		self.kernelSize = kernelSize
		self.chainAutoInc = -1
		self.hasRadialCoords = False
		
		self.generateGraph()

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
			
		self.cleanexCount = 0
									
		
	def generateGraph(self):
		
		self.generateNodes()
		self.generateCycles()
		self.generateLinks()
		self.generateLoops()		
						
		
	def generateNodes(self):

		self.startPerm = "".join([str(x) for x in range(self.spClass)])		
		self.spgen = SPGenerator(self.startPerm)	
		self.altgen = self.spgen
		self.nodes = [Node(i, self.spgen.perms[i], self.spgen.addrs[i]) for i in range(len(self.spgen.perms))]
		
		self.nodeByPerm = {}
		self.nodeByAddress = {}		
		for node in self.nodes:
			self.nodeByPerm[node.perm] = node
			self.nodeByAddress[node.address] = node
			
		self.startNode = self.nodeByPerm[self.startPerm]
					
		
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
		
		
	def readdress(self, addr):
		
		self.altgen = SPGenerator(self.nodeByAddress[addr].perm)

		# readdress cycles
		for i in range(0, len(self.altgen.perms), self.spClass):
			curr_cycle = self.nodeByPerm[self.altgen.perms[i]].cycle
			curr_address = self.altgen.addrs[i]
			
			qx = Measures.DM
			qy = Measures.DM
			for lvl, q in enumerate([int(x) for x in curr_address]):
				qx += q * Measures.xydelta[self.spClass][lvl][0]
				qy += q * Measures.xydelta[self.spClass][lvl][1]	
			curr_cycle.px = qx
			curr_cycle.py = qy			
			
		# readdress nodes
		for i in range(len(self.altgen.perms)):
			curr_node = self.nodeByPerm[self.altgen.perms[i]]
			curr_address = self.altgen.addrs[i]

			qLast = int(curr_address[-1])
			dx = Measures.RH*math.cos((2*qLast - (self.spClass-1)) * math.pi / self.spClass)
			dy = Measures.RH*math.sin((2*qLast - (self.spClass-1)) * math.pi / self.spClass)
			curr_node.px = curr_node.cycle.px+dx
			curr_node.py = curr_node.cycle.py+dy			
		
		
		
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
	
	
	def generateKernel(self):
				
		affected_chains = []
		bases = []
		
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
				

	### ~~~ extensions ~~~ ###	
				
		
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
	
	
	# [~] revert touched nodes partially, maybe, actually reconstruct it from affected loops, also document what's contained inside affected stuff		
	def coerceLoop(self, loop):		
		singles = []
		coerced = []
		#diagram.pointer_avlen = diagram.spClass		
						
		# gather around all currently touched chains
		next_touched_chains = set(itertools.chain(*[[n.cycle.chain for n in l.nodes]for l in loop.extension_result.affected_loops]))
		while len(next_touched_chains):
			curr_touched_chains = next_touched_chains
			# construct a new set of touched chains for new coercions
			next_touched_chains = set()
						
			for ic, chain in enumerate(curr_touched_chains):
				avlen = len(chain.avloops)
				
				if avlen == 0:
					self.pointer_avlen = 0
					loop.extension_result.singles = singles
					loop.extension_result.affected_loops += coerced
					return (singles, coerced) 
	
				elif avlen == 1:
					avloop = list(chain.avloops)[0]
					singles.append(avloop)
					self.extendLoop(avloop)
					next_touched_chains.update(set(itertools.chain(*[[n.cycle.chain for n in l.nodes]for l in avloop.extension_result.affected_loops])))
				
				elif avlen == 2:
					killingFields = [l.killingField() for l in chain.avloops]
					intersected = killingFields[0].intersection(killingFields[1])
					if len(intersected):
						for avloop in intersected:
							coerced.append(avloop)
							self.setLoopUnavailabled(avloop)
							next_touched_chains.update([n.cycle.chain for n in avloop.nodes])
					
				if avlen < self.pointer_avlen:
					self.pointer_avlen = avlen
											
		# singles will be collapsed on loop collapse
		# coerced loops will be appended to the rest of the affected loops to be re-availabled along with them
		loop.extension_result.addCoercionDetails(singles, coerced)
		# for printing
		return (singles, coerced)			
		
																						
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
		
		# collapse back singles (if any)
		for loop in reversed(extension_result.affected_singles):
			self.collapseBack(loop)
		extension_result.affected_singles.clear()
		
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
					
					
	### ~~~ pointers ~~~ ###																																																				
				
			
	def pointToAddressTuple(self, address):
		self.pointers = list(self.nodeByAddress[address].tuple)

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
		self.exloops = [[self.nodeByAddress[addr].loop for addr in addrs] for addrs in self.extenders]
		print("Loaded "+str(len(self.extenders))+" extenders")		
					



def countColors(loops):
	return sorted(groupby([loop.ktype for loop in loops], G = lambda g: len(g)).items())
	
	
def kstr(loops):	
	return ", ".join([color_string(k) + ":" + str(v) for k, v in countColors(loops)])


if __name__ == "__main__":
	
	diagram = Diagram(6, 3)
	
	def extend(addr):
		assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	def collapse(addr):
		diagram.collapseBack(diagram.nodeByAddress[addr].loop)
	def single():
		singles = []
		diagram.point()
		while diagram.pointer_avlen == 1 and len(diagram.pointers):
			singles.append(diagram.pointers[0].loop)
			diagram.extendLoop(diagram.pointers[0].loop)
			diagram.point()
		return singles			
	def trial(loops, __show__=False):
		results = []
		for loop in loops:
			if loop.availabled:			
				diagram.extendLoop(loop)
				diagram.point()
				if __show__:
					show(diagram)
					if diagram.pointer_avlen == 0:
						print(" === !!! " + str(0) + " !!! === ")			
					input("#x | avloops: " + str(len([l for l in diagram.loops if l.availabled])) + " | " + str(loop))
				
				singles = single()
				if __show__:
					show(diagram)
					if diagram.pointer_avlen == 0:
						print(" === !!! " + str(0) + " !!! === ")			
					input("#x | avloops: " + str(len([l for l in diagram.loops if l.availabled])) + " | " + str(loop) + " | s: " + str(len(singles)))		
				
				result = ((diagram.pointer_avlen, -len(singles), len([l for l in diagram.loops if l.availabled]), -len(diagram.pointers)), loop)
				print("[trial] " + str(result))
				results.append(result)
				
				for l in reversed(singles):
					diagram.collapseBack(l)					
				diagram.collapseBack(loop)				
				
		print("[trial] ---")
		grouped = sorted(groupby(results, 
			K = lambda result: result[0],
			V = lambda result: result[1]#,
			#G = lambda g: len(g)
		).items())
		print("xxx: " + str([l.firstNode() for l in grouped[0][1]]))
		diagram.pointers = [l.firstNode() for l in grouped[0][1]]
		show(diagram)
		input("(avlen | -singles | availabled | -pointers): loop_count\n" + "\n".join(str(g[0])+": "+str(len(g[1])) for g in grouped) + "\nloops: \n"+"\n".join([str(l) for l in grouped[0][1]]) + "\naddrs: \n"+" ".join([l.firstAddress() for l in grouped[0][1]]))		
		return grouped[0][1]
	# diagram.readdress('10041')

	# diagram.readdress('10205')
	#setRadialCoords(diagram)
			
	# diagram.extendLoop(diagram.nodeByAddress['00001'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['01033'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['02302'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['10030'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['10105'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['10205'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['10305'].loop)	
	# diagram.extendLoop(diagram.nodeByAddress['11005'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['11105'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['11205'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['11305'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['12013'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['12022'].loop)			

	# diagram.extendLoop(diagram.nodeByAddress['10242'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['12004'].loop)
			
	# --- #
			
	# diagram.extendLoop(diagram.nodeByAddress['12003'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['10204'].loop)	
	# diagram.extendLoop(diagram.nodeByAddress['10004'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['10015'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['10021'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['10111'].loop)
	# diagram.extendLoop(diagram.nodeByAddress['10242'].loop)
	
	# extend('11005')
	# extend('11105')
	# extend('11205')
	# extend('11305')
	
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['01042'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['02042'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['01343'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['00311'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['00302'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['00343'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['01302'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['01311'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['02302'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['02311'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['02343'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['10003'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['10030'].loop)
	# diagram.setLoopUnavailabled(diagram.nodeByAddress['11004'].loop)
	'''
	# (2, 0, 48, -2): 18
	# 00001 00033 00042 00302 00311 00343 01001 01033 01042 01302 01311 01343 02001 02033 02042 02302 02311 02343
	extend('00001')
	
	# 00001 ⇒ (2, -3, 34, -14): 2
	# 01302 02033
	extend('01302')

	# extend('00033')
	# extend('01302')
	# extend('10233')
	# extend('11104')
	# extend('12205')
	# extend('10113')
	'''
	diagram.point()
	show(diagram)
	input("=== av loops: " + str(len([loop for loop in diagram.loops if loop.availabled])))
	
	pointloops0 = [l for l in diagram.loops if l.availabled] # [node.loop for node in diagram.pointers]

	pointloops0 = trial(pointloops0)
	
	for loop0 in pointloops0:
		if loop0.availabled:			
			diagram.extendLoop(loop0)
			diagram.point()
			show(diagram)
			if diagram.pointer_avlen == 0:
				print(" === !!! " + str(0) + " !!! === ")			
			input("#0 | avloops: " + str(len([l for l in diagram.loops if l.availabled])) + " | " + str(loop0))
			
			singles0 = single()
			show(diagram)
			if diagram.pointer_avlen == 0:
				print(" === !!! " + str(0) + " !!! === ")			
			input("#0 | avloops: " + str(len([l for l in diagram.loops if l.availabled])) + " | " + str(loop0) + " | s: " + str(len(singles0)))
						
			# pointloops1 = [node.loop for node in diagram.pointers]
			# for loop1 in pointloops1:
			# 	if loop1.availabled:
			# 		diagram.extendLoop(loop1)
			# 		diagram.point()
			# 		show(diagram)
			# 		if diagram.pointer_avlen == 0:
			# 			print(" === !!! " + str(0) + " !!! === ")					
			# 		input("#0: " + str(loop0) + " | s: " + str(len(singles0)) + "\n#1: " + str(loop1))
			# 
			# 		singles1 = single()
			# 		show(diagram)
			# 		if diagram.pointer_avlen == 0:
			# 			print(" === !!! " + str(0) + " !!! === ")
			# 		input("#0: " + str(loop0) + " | s: " + str(len(singles0)) + "\n#1: " + str(loop1) + " | s: " + str(len(singles1)))
			# 
			# 		pointloops2 = [node.loop for node in diagram.pointers]																										
			# 		for loop2 in pointloops2:
			# 			if loop2.availabled:
			# 				diagram.extendLoop(loop2)
			# 				diagram.point()
			# 				show(diagram)
			# 				if diagram.pointer_avlen == 0:
			# 					print(" === !!! " + str(0) + " !!! === ")							
			# 				input("#0: " + str(loop0) + " | s: " + str(len(singles0)) + "\n#1: " + str(loop1) + " | s: " + str(len(singles1)) + "\n#2: " + str(loop2))
			# 
			# 				singles2 = single()
			# 				show(diagram)
			# 				if diagram.pointer_avlen == 0:
			# 					print(" === !!! " + str(0) + " !!! === ")							
			# 				input("#0: " + str(loop0) + " | s: " + str(len(singles0)) + "\n#1: " + str(loop1) + " | s: " + str(len(singles1)) + "\n#2: " + str(loop2) + " | s: " + str(len(singles2)))
			# 
			# 				pointloops3 = [node.loop for node in diagram.pointers]
			# 				for loop3 in pointloops3:
			# 					if loop3.availabled:			
			# 						diagram.extendLoop(loop3)
			# 						diagram.point()
			# 						show(diagram)
			# 						if diagram.pointer_avlen == 0:
			# 							print(" === !!! " + str(0) + " !!! === ")			
			# 						input("#0: " + str(loop0) + " | s: " + str(len(singles0)) + "\n#1: " + str(loop1) + " | s: " + str(len(singles1)) + "\n#2: " + str(loop2) + " | s: " + str(len(singles2)) + "\n#3: " + str(loop3))									
			# 						singles3 = single()
			# 						show(diagram)
			# 						if diagram.pointer_avlen == 0:
			# 							print(" === !!! " + str(0) + " !!! === ")			
			# 						input("#0: " + str(loop0) + " | s: " + str(len(singles0)) + "\n#1: " + str(loop1) + " | s: " + str(len(singles1)) + "\n#2: " + str(loop2) + " | s: " + str(len(singles2)) + "\n#3: " + str(loop3) + " | s: " + str(len(singles3)))									
			# 
			# 						for loop in reversed(singles3):
			# 							diagram.collapseBack(loop)					
			# 						diagram.collapseBack(loop3)
			# 				for loop in reversed(singles2):
			# 					diagram.collapseBack(loop)
			# 				diagram.collapseBack(loop2)										
			# 		for loop in reversed(singles1):
			# 			diagram.collapseBack(loop)							
			# 		diagram.collapseBack(loop1)	
			for loop in reversed(singles0):
				diagram.collapseBack(loop)					
			diagram.collapseBack(loop0)
			
# [~] for each loop test to choose the one that leaves the smallest chain_avlen behind			

# [~] for a loop, test all available combinations of chaining its cycles without this loop
			
		
		
							
