from superperms import *
from node import *
from cycle import *
from link import *
from chain import *
from common import *
from measures import *
from collections import defaultdict
from colorsys import hls_to_rgb
from random import random


class Diagram (object):
	
	__slots__ = [
		'spClass',
		'nodes', 'nodeByAddress', 'nodeByPerm', 'startNode',
		'cycles', 'cycleByAddress',
		'links', 'l3s', 'p3s',
		'chains',
		'W', 'H',
		'pointers', 'draw_boxes'
	]

		
	def __init__(self, N):
				
		self.spClass = N
		
		self.generateGraph()

		self.chains = []
		self.pointers = []
		self.draw_boxes = []
		
		# every cycle has its own chain initially
		for cycle in self.cycles:
			_ = Chain(self, cycle.address, hls_to_rgb(random(), 0.5, 1))


	def generateGraph(self):
		
		self.generateNodes()
		self.generateCycles()
		self.generateLinks()


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
		
		
		
		
if __name__ == "__main__":

	diagram = Diagram(6)		
