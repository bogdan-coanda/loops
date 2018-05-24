from diagram import *
from time import time
import pickle
from uicanvas import *
from itertools import zip_longest
from types import SimpleNamespace as _
from explorer import groupby

def extendBy(diagram, nodes):
	vn = []
	for n in nodes:
		if not diagram.extendLoop(diagram.nodeByAddress[n.address]):
			vn.append(n)
		while(len(vn) > 0):
			ws = []
			for n in vn:
				if not diagram.extendLoop(n):
					ws.append(n)
			if vn == ws:
				print("Failed extending by: " + " ".join([str(n) for n in ws]))
				break
			vn = ws
			

class Extender (object):
	
	def __init__(self, nodes):
		self.nodes = nodes
		self.pseudos = [n.loop.pseudo() for n in nodes]
		self.roots = groupby(nodes, K = lambda n: n.loop.root())
		self.shadow = sorted(groupby(self.roots.items(), K = lambda k: len(k[0]), V = lambda v: len(v[1]), G = lambda g: sum(g)).items())
		self.knodes = [n for n in nodes if n.loop.hasKernelNodes()]
		self.mnodes = [n for n in nodes if not n.loop.hasKernelNodes()]
		self.kroots = groupby(self.knodes, K = lambda n: n.loop.root())
		self.mroots = groupby(self.mnodes, K = lambda n: n.loop.root())
		self.kshadow = groupby(self.kroots.items(), K = lambda k: len(k[0]), V = lambda v: len(v[1]), G = lambda g: sum(g))
		self.mshadow = groupby(self.mroots.items(), K = lambda k: len(k[0]), V = lambda v: len(v[1]), G = lambda g: sum(g))
		self.kshadowstr = "|".join([str(d[0])+":"+str(d[1]) for d in sorted(self.kshadow.items())])
		self.mshadowstr = "|".join([str(d[0])+":"+str(d[1]) for d in sorted(self.mshadow.items())])

	def __str__(self):
		return self.kshadowstr + "§" + self.mshadowstr

	def __repr__(self):
		return str(self)

if __name__ == "__main__":	
	diagram = Diagram(6)
	diagram.startTime = time()

	diagram.loadExtenders()
	
	ex = [Extender(e) for e in diagram.extenders] 
	
	ek = groupby(ex, K = lambda e: e.kshadowstr) 
	#print("ek:")
	#print(sorted(ek.keys()))
	
	em = groupby(ex, K = lambda e: e.mshadowstr) 
	#print("em:")
	#print(sorted(em.keys()))	
	
	pp = [e for e in ex if e.mshadowstr.endswith('0:10|1:2|2:4|3:8')]
	
	nodes = [n for n in pp[0].knodes if n.loop.pseudo() not in ['01105', '01305', '02005', '02205', '10105', '10305', '11005', '11205', 
		'01022', '02013', '10022', '11013',
		'01001', '01010', '01033', '01042', '01211', '01220', '02302', '02311', '02320', '02343']]
	
	d = Diagram(6); extendBy(d, nodes); show(d)
	
	#extendBy(diagram, ek['0:4|1:4'][0].knodes)
	
	#gl = [groupby(extender, K = lambda n: n.loop.root()) for extender in diagram.extenders]
	
	#sh = [sorted(groupby(gg.items(), K = lambda k: len(k[0]), V = lambda v: len(v[1]), G = lambda g: sum(g)).items()) for gg in gl]
	#'0:10|1:5|2:7|3:3'
	
	#hk = groupby(diagram.extenders, K = lambda e: len([n for n in e if n.loop.hasKernelNodes()]), V = lambda e: [n for n in e if not n.loop.hasKernelNodes()])
	# [(1, 13360), (2, 10896), (3, 8832), (4, 5840), (5, 1632), (6, 1264), (7, 368), (8, 16), (9, 80)]
	
	#gl9 = [groupby(extender, K = lambda n: n.loop.root()) for extender in hk[9]]
	#sh9 = [sorted(groupby(gg.items(), K = lambda k: len(k[0]), V = lambda v: len(v[1]), G = lambda g: sum(g)).items()) for gg in gl9]
	
	#h = gl[0]#[g for g in gl if '123' in g.keys() and '122' in g.keys() and '121' in g.keys() and '120' in g.keys()][0]
	'''
	vs = []
	for v in h.values():
		for n in v:
			if not diagram.extendLoop(n):
				vs.append(n)
		while(len(vs) > 0):
			ws = []
			for n in vs:
				if not diagram.extendLoop(n):
					ws.append(n)
			vs = ws
	'''
	#show(diagram)
	print("~~~")

