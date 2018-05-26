from diagram import *
from time import time
import pickle
from uicanvas import *
import itertools
from types import SimpleNamespace as _
from explorer import groupby
import random
import sys


def strstate(state):

	def pack(s):
		if s[2] > 0:
			return '('+str(s[1])+')'
		elif s[3] > 0:
			return '{'+str(s[1])+'}'
		else:
			return str(s[1])
		
	return ' '.join([str(s[0])+'/'+pack(s) for s in state])
	
	
class DMC (object):
	
	def __init__(self):
		
		self.dmc = 0
		self.bcs = []
		self.foundany = False

		self.diagram = Diagram(7)
		self.diagram.startTime = time()
		
		# initial gathering
		self.splitNode = self.diagram.nodeByAddress['000001']
		self.diagram.extendLoop(self.splitNode)	
		
		self.bases = sorted(self.splitNode.loopBrethren, key = lambda n: n.address)
		#input(self.bases)
		
		self.diagram.measureNodes()
		self.initials = [sorted(
			[
				ncn for ncn in b.cycle.nodes 
				if ncn.loop.availabled 
					and not ncn.extended 
					and len([ncnlb for ncnlb in ncn.loopBrethren if ncnlb.looped]) is 0
			], key = lambda n: n.address) for b in self.bases]
		#input(self.initials)
				
		self.diagram.collapseLoop(self.splitNode)
		
		self.diagram.connectedChainPairs.update([(0,1),(0,2),(0,3),(0,4),(0,5)])
		#print('ccp: ' + str(ccp) + ' | chains: ' + str(self.diagram.drawn.chains) + ' | connected: ' + str(self.diagram.connectedChainPairs))
	
		self.seed()		
		#self.load()
		
		print("---------")


	def seed(self):
		seed = random.randrange(sys.maxsize)
		random.seed(seed)
		print("Seed is:", seed)
		with open("ante7.rnd.pkl", 'wb') as outfile:
			pickle.dump(random.getstate(), outfile, 0)

				
	def load(self):			
		# "ante7.rnd.0.pkl" - max T: 108 @ dmc: 28629 / 32k
		# "ante7.rnd.1.pkl" - max T: 108 @ dmc: 851 / 32k
		# "ante7.rnd.2.pkl" - max T: 110 @ dmc: 79146, 181273 / 272k …
		# "ante7.rnd.3.pkl" - max T: 109 @ dmc: 16995, 42059, 117243
		with open("ante7.rnd.2.pkl", 'rb') as infile:
			random.setstate(pickle.load(infile))
			print("Loaded prev. seed")
		
				
	def filterOut(self, nodes, lbcs):	
		return [
			n for n in nodes
			# select nodes with at most a single connection to any of the base chains
			if len([nln for nln in n.loop.nodes if nln.looped and len(set(self.diagram.allConnectedChains(nln.chainID)).intersection(lbcs)) is not 0]) <= 1
		]
				

	def run(self, lvl, state):		
		self.diagram.measureNodes()		
		R = 109
		T = 110
		if lvl >= R or self.dmc % 4000 is 0:
			avg = groupby(self.filterOut(self.diagram.drawn.availables, self.bcs + [0]), K = lambda n: n.chainID)
			ng = groupby([n for n in self.diagram.nodes if n.looped], K = lambda n: n.chainID)
			print('['+str(self.dmc)+']['+str(lvl)+'] @ ' + tstr(time() - self.diagram.startTime) + ' mx: ' + str(len(self.diagram.mx_singles)) + '|' + str(len(self.diagram.mx_sparks)) + '|' + str(len(self.diagram.mx_unreachable_cycles)) + ' | avg: ' + ' '.join([str(d[0])+'§'+str(d[1])+'/'+str(d[2]) for d in sorted([(chainID, len(avg.get(chainID) or []), len(ng[chainID])) for chainID in self.bcs])]))
			print(strstate(state))
			if lvl >= R:
				self.foundany = True
			if lvl >= T:
				print(str(lvl)+'» '+str(T))
				show(self.diagram)
				input()
			#print(' | chains: ' + str(self.diagram.drawn.chains) + ' | connected: ' + str(self.diagram.connectedChainPairs))
			#print(' | /g: ' + ' '.join([str(chainID)+'§'+str(len(ng[chainID])) for chainID in ng.keys() if chainID not in self.bcs]))
		#assert (1,2) not in self.diagram.connectedChainPairs and (1,3) not in self.diagram.connectedChainPairs and (1,4) not in self.diagram.connectedChainPairs and (1,5) not in self.diagram.connectedChainPairs and (2,3) not in self.diagram.connectedChainPairs and (2,4) not in self.diagram.connectedChainPairs and (2,5) not in self.diagram.connectedChainPairs and (3,4) not in self.diagram.connectedChainPairs and (3,5) not in self.diagram.connectedChainPairs and (4,5) not in self.diagram.connectedChainPairs , "connected stuff: " + str(self.diagram.connectedChainPairs)	
			
		self.dmc += 1			
		
		#if len(self.diagram.mx_unreachable_cycles) is not 0:
			#print('['+str(lvl)+'] refusing for unreachable cycles: ' + str(len(self.diagram.mx_unreachable_cycles)))
			#return
										
		if lvl in range(0, self.diagram.spClass-2):
			avs = [n for n in self.initials[lvl] if len([nln for nln in n.loop.nodes if nln.looped]) is 0]
			#print("initials: " + str(len(avs)) + " from " + str(len(self.initials[lvl])))
			random.shuffle(avs)
			
		elif len(self.diagram.mx_singles) is not 0:
			# if we're forced into singles
			#print('['+str(lvl)+'] singling...')
	
			# [~] filter out kernel singles.
			avs = sorted(self.filterOut(self.diagram.mx_singles, self.bcs), key = lambda n: n.address)
			random.shuffle(avs)
			#print("singling: " + str(len(avs)) + " from " + str(len(self.diagram.mx_singles)))
	
		elif len(self.diagram.mx_sparks) is not 0:
			avs = sorted(self.diagram.mx_sparks, key = lambda n: n.address)
			random.shuffle(avs)
			#print("sparkling: " + str(len(avs)) + " from " + str(len(self.diagram.mx_sparks)))
	
		else: 
			avg = groupby(self.filterOut(self.diagram.drawn.availables, self.bcs + [0]), K = lambda n: n.chainID)
			ng = groupby([n for n in self.diagram.nodes if n.looped], K = lambda n: n.chainID)
			# [~] no chain should be left without an available node in it to connect it to the rest
			if len([c for c in self.bcs + [0] if not avg.get(c)]) is not 0: # [~] currently just checking the forced bases and kernel
				return		
			# order by base chain with smallest number of extensions done
			'''pair[1]'''
			avs = list(itertools.chain(*[pp[1] for pp in sorted([pp for pp in avg.items()if pp[0] is not 0], key = lambda pair: len(ng[pair[0]]) if pair[0] in self.bcs else 999999999)]))
			#print("normal: " + str(len(avs)))
			
			
		# if no node remains…						
		if len(avs) is 0:		
			#print('['+str(lvl)+'] refusing for no availables in group: ' + str(id))
			return		
	
		#print('['+str(lvl)+'] carrying on with avs: ' + str(len(avs)) + ' for group: ' + str(id))
	
		lvl_seen = []		
		cc = 0
		singlesCount = len(self.diagram.mx_singles)
		sparksCount = len(self.diagram.mx_sparks)
		
		#random.shuffle(avs)
		
		for node in avs:
			if self.diagram.extendLoop(node):			
				#input('['+str(lvl)+'] extended ' + str(cc) + '/' + str(len(avs)) + " : " + str(node))			
	
				if lvl < self.diagram.spClass-2:
					self.bcs = [b.chainID for b in self.bases if b.looped]
	
				if len(self.diagram.mx_unreachable_cycles) is 0:
					self.run(lvl+1, state + [(cc, len(avs), singlesCount, sparksCount)])
				
				self.diagram.collapseLoop(node)
				#print('['+str(lvl)+'] collapsed ' + str(cc) + '/' + str(len(avs)) + " : " + str(node))
							
				if singlesCount > 0 or sparksCount > 0:
					return ###
					
				if self.dmc > 20000 and not self.foundany:
					return # hardcore
							
				node.loop.availabled = False
				for nn in node.loop.nodes:
					nn.cycle.available_loops_count -= 1
				#sg, sp, un = len(self.diagram.mx_singles), len(self.diagram.mx_sparks), len(self.diagram.mx_unreachable_cycles)
				self.diagram.tryMakeUnavailable([node])
				#assert (sg, sp, un) == (len(self.diagram.mx_singles), len(self.diagram.mx_sparks), len(self.diagram.mx_unreachable_cycles))
				lvl_seen.append(node)				
	
			cc += 1
			
		for node in lvl_seen:
			node.loop.availabled = True
			for nn in node.loop.nodes:
				nn.cycle.available_loops_count += 1								
			
		

if __name__ == "__main__":	
	
	dmc = 0
	while True:
		print("~~~ dmc: " + str(dmc) + " ~~~")
		DMC().run(0, [])
		dmc += 1
	
	print('~~~')
	
