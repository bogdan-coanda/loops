from diagram import *
from uicanvas import *
from common import *

		
					
def tl(ktype):
	unavailed = 0
	while True:
		currently = 0		
		for loop in diagram.loops:
			if loop.ktype == ktype:
				knodes = [node for node in itertools.chain(*[node.cycle.nodes for node in loop.nodes]) if node.loop.availabled and node.loop.ktype > 1]
				groups = groupby(knodes, K = lambda n: n.loop.ktype)
				for k,g in groups.items():
					if len(g) != diagram.spClass-1:
						#print(f"[tl] invalidating {len(g)} loops along base {loop} ")
						currently += len(g)
						for n in g:
							#print(f"[tl] {n.loop}")
							if n.loop.availabled:
								diagram.setLoopUnavailabled(n.loop)
		unavailed += currently
		if currently == 0:
			print(f"[tl] ⇒ invalidated {unavailed} loops for ktype:{ktype}")			
			return unavailed
	
def el(addr, ktype):
	extended = 0
	parentLoop = diagram.nodeByAddress[addr].loop
	knodes = [node for node in itertools.chain(*[node.cycle.nodes for node in parentLoop.nodes]) if node.loop.availabled and node.loop.ktype == ktype]
	for i,node in enumerate(knodes):
		if not node.loop.extended:
			assert diagram.extendLoop(node.loop)
			extended += 1
	print(f"[el] ⇒ extended {extended} ktype:{ktype} loops for parent {parentLoop}")

	
def es(addr, ktype):
	extended = 0
	parentLoop = diagram.nodeByAddress[addr].loop
	knodes = [node for node in itertools.chain(*[node.cycle.nodes for node in parentLoop.nodes]) if node.loop.availabled and node.loop.ktype == ktype and node.address[5] not in ['0', str(diagram.spClass-2)]]
	for i,node in enumerate(knodes):
		if not node.loop.extended:
			assert diagram.extendLoop(node.loop)
			extended += 1
	print(f"[es] ⇒ extended {extended} ktype:{ktype} loops for parent {parentLoop}")

def ql(parent_ktype):
	unavailed = 0 
	brokenCount = 0
	for parentLoop in diagram.loops:
		if parentLoop.ktype == parent_ktype:
			for ktype in range(2, diagram.spClass):
				knodes = [node for node in itertools.chain(*[node.cycle.nodes for node in parentLoop.nodes]) if node.loop.availabled and node.loop.ktype == ktype]
				
				ex = []
				broken = False
				
				for ni, node in enumerate(knodes):
					if not node.loop.extended:
						if diagram.extendLoop(node.loop):
							ex.append(node)
						else:
							broken = True
							break
					
				for node in reversed(ex):
					diagram.collapseBack(node.loop)
		
				if broken:
					brokenCount += 1
					for node in ex:
						diagram.setLoopUnavailabled(node.loop)
						unavailed += 1
					print(f"[ql] broken @ {parentLoop} with ktype:{ktype} | unavailed {unavailed} loops in {brokenCount} parents so far…")
	print(f"[ql] ⇒ unavailed {unavailed} loops in {brokenCount} parents")

def L2():
	for i in range(len(diagram.pointers)):
		diagram.pointers[i] = diagram.pointers[i].links[2].next if i % 2 == 0 else diagram.pointers[i].prevs[2].node
		
def L1():			
	for i in range(len(diagram.pointers)):
		diagram.pointers[i] = diagram.pointers[i].links[1].next if i % 2 == 0 else diagram.pointers[i].prevs[1].node
					
def JP(count):
	for i in range(count):
		for j in range(diagram.spClass-1):
			L1();
		L2()
																
def EX():
	for i in range(len(diagram.pointers)):
		if i % 2 == 0:
			diagram.extendLoop(diagram.pointers[i].loop)
		else:
			diagram.extendLoop(diagram.pointers[i].prevs[1].node.loop)





def purge():

	next_sample_lengths_per_loop_tuple = {}
	unavailed = []
	unsuccess = 0
	
	for it, tuple in enumerate(diagram.loop_tuples):
		if it % 100 == 0:
			print(f"[purge] @ {it}/{len(diagram.loop_tuples)}")
		
		if tuple[0].availabled: # [!] need only full tuples here (need ot() to have run previously)
			
			# try extend tuple
			ec = 0
			for loop in tuple:
				if not diagram.extendLoop(loop):
					break
				else:
					ec += 1
			
			# note successfulness
			if ec != len(tuple):
				next_sample_lengths_per_loop_tuple[tuple] = -1
			else:
				next_sample_lengths_per_loop_tuple[tuple] = len(diagram.point())
							
			# collapse back
			for loop in reversed(tuple[:ec]):
				diagram.collapseBack(loop)

			# purge if unsuccessful
			if next_sample_lengths_per_loop_tuple[tuple] <= 0:
				unsuccess += 1
				for loop in tuple:
					if loop.availabled:
						diagram.setLoopUnavailabled(loop)
						unavailed.append(loop)
						
	print(f"[purge] ⇒ unavailabled {len(unavailed)} loops in {unsuccess} failed tuples | tuples per sample length: {sorted(groupby(next_sample_lengths_per_loop_tuple.items(), K = lambda p: p[1], G = lambda g: len(g)).items())}")
	return (unavailed, next_sample_lengths_per_loop_tuple)




def jump(lvl=0, path=[]):
	global sols
	
	# remove partial tuples
	seen = ot()
	
	uc = len([c for c in diagram.cycles if c.isUnchained])
	print(f"[lvl:{lvl}][uc:{uc}] {'.'.join([(str(x)+upper(t)) for x,t in path])}")
	
	# if solution	
	if uc == 0:
		show(diagram)
		input2(f"[lvl:{lvl}][sols:{sols}] {'.'.join([(str(x)+upper(t)) for x,t in path])}")	
		
	else: 
		
		# choose smallest sample tuple group
		sample = [n.tuple for n in sorted(diagram.point(), key = lambda node: node.address)]
		for it, tuple in enumerate(sample):
			
			# try extend tuple
			ec = 0
			for node in tuple:
				if not diagram.extendLoop(node.loop):
					break
				else:
					ec += 1
			
			# if successful, carry on
			if ec == len(tuple):				
				jump(lvl+1, path+[(it, len(sample))])
			
			# collapse back
			for node in reversed(tuple[:ec]):
				diagram.collapseBack(node.loop)
	
			# remove tested tuples			
			for node in tuple:
				if node.loop.availabled:
					diagram.setLoopUnavailabled(node.loop)
					seen.append(node.loop)

	# readd all seen
	for l in seen:
		diagram.setLoopAvailabled(l)









if __name__ == "__main__":

	diagram = Diagram(8, 1)			

	import enav
	enav.diagram = diagram
	from enav import *
	
	# ∘ bases ∘ ['0000001', '0000002', '0000003', '0000012', '0000013', '0000021', '0000022', '0000044', '0000045', '0000053', '0000054', '0000063', '0000064', '0000065'] ∘ #
	extend('0000001'); ot()
	
	# x0 = et('0000001') # {0:a}	
	# x0 = et('0000002') # {1:b}
	# x1 = et('0000064') # {0:y}	
	# x1 = et('0000065') # {1:z}
	
	# x0 = et('0000003') # {0:c}
	# x1 = et('0000063') # {1:x}		
	# et('0000012') # {0:p0}
	# et('0000013') # {1:p1}	
	# et('0000021') # {0:p2}
	# et('0000022') # {1:p3}
	# et('0000044') # {0:q3}
	# et('0000045') # {1:q2}
	# et('0000053') # {0:q1}
	# et('0000054') # {1:q0}

	# ∘ blue
	x2 = eb('1000', 1) # {az}
	# x2 = eg('1000', 1) # {by}
	
	# ∘ long column 
	x3 = elt('1000007', 5) # {a}	
	# x3 = elt('1000006', 5) # {y}	
	# x3 = elt('1000206', 2) # {b}	
	# x3 = elt('1000207', 2) # {z}
			
	# ∘ short column
	x4 = est('1000207', 2) # {a}	
	# x4 = est('1000206', 2) # {y}
	# x4 = est('1000006', 5) # {b}	
	# x4 = est('1000007', 5) # {z}
	
	# ∘ green
	x5 = et('1000206') # {a}
	# et('1000207') # {y}
	# et('1000007') # {b}
	# et('1000006') # {z}

	ot()
			
	# §.
	# [choose] min_ratio: 2.4 | min_chain: ⟨chain:61|av:5⟩ | min_nodes:
	# (1, '0001252')
	# (1, '0001256')
	# (2, '0001250')
	# (3, '0001253')
	# (5, '0001257')
	et('0001252') # 0/5

	# §.0⁵
	# [choose] min_ratio: 3.0 | min_chain: ⟨chain:62|av:1⟩ | min_nodes:
	# (3, '0001262')
	et('0001262') # 0/1
	
	# $.0⁵0¹
	# [choose] min_ratio: 1.5714285714285714 | min_chain: ⟨chain:1361|av:7⟩ | min_nodes:
	# (1, '0122230')
	# (1, '0122236')
	# (1, '0122237')
	# (2, '0122231')
	# (2, '0122232')
	# (2, '0122233')
	# (2, '0122234')
	et('0122230') # 0/7

	# $.0⁵0¹0⁷
	# [choose] min_ratio: 3.0 | min_chain: ⟨chain:60|av:1⟩ | min_nodes:
	# (3, '0001244')
	et('0001244') # 0/1

	# $.0⁵0¹0⁷0¹
	# [choose] min_ratio: 2.6666666666666665 | min_chain: ⟨chain:398|av:6⟩ | min_nodes:
	# (2, '0014262')
	# (2, '0014264')
	# (3, '0014261')
	# (3, '0014263')
	# (3, '0014265')
	# (3, '0014266')
	et('0014262') # 0/6

	# $.0⁵0¹0⁷0¹0⁶
	# [choose] min_ratio: 1.75 | min_chain: ⟨chain:3311|av:8⟩ | min_nodes:
	# (1, '1033500')
	# (1, '1033504')
	# (2, '1033501')
	# (2, '1033502')
	# (2, '1033503')
	# (2, '1033505')
	# (2, '1033506')
	# (2, '1033507')
	et('1033500') # 0/8

	# $.0⁵0¹0⁷0¹0⁶0⁸ 
	# [choose] min_ratio: 3.0 | min_chain: ⟨chain:56|av:1⟩ | min_nodes:
	# (3, '0001204')
	et('0001204') # 0/1

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹
	# [choose] min_ratio: 2.5 | min_chain: ⟨chain:397|av:6⟩ | min_nodes:
	# (2, '0014250')
	# (2, '0014253')
	# (2, '0014255')
	# (2, '0014256')
	# (3, '0014252')
	# (4, '0014254')	
	et('0014250') # 0/6

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶
	# [choose] min_ratio: 1.6666666666666667 | min_chain: ⟨chain:1938|av:6⟩ | min_nodes:
	# (1, '0211066')
	# (1, '0211067')
	# (2, '0211060')
	# (2, '0211061')
	# (2, '0211063')
	# (2, '0211064')
	et('0211066') # 0/6

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶
	# [choose] min_ratio: 3.0 | min_chain: ⟨chain:57|av:1⟩ | min_nodes:
	# (3, '0001213')
	et('0001213') # 0/1

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹
	# [choose] min_ratio: 2.3333333333333335 | min_chain: ⟨chain:1322|av:6⟩ | min_nodes:
	# (2, '0121261')
	# (2, '0121264')
	# (2, '0121266')
	# (2, '0121267')
	# (3, '0121263')
	# (3, '0121265')	
	et('0121261') # 0/6

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶
	# [choose] min_ratio: 1.25 | min_chain: ⟨chain:725|av:8⟩ | min_nodes:
	# (1, '0032140')
	# (1, '0032141')
	# (1, '0032142')
	# (1, '0032144')
	# (1, '0032145')
	# (1, '0032146')
	# (2, '0032143')
	# (2, '0032147')
	et('0032140') # 0/8

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶0⁸
	# [choose] min_ratio: 1.0 | min_chain: ⟨chain:727|av:1⟩ | min_nodes:
	# (1, '0032161')
	et('0032161') # 0/1

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶0⁸0¹
	# [choose] min_ratio: 3.0 | min_chain: ⟨chain:1932|av:1⟩ | min_nodes:
	# (3, '0211000')
	et('0211000') # 0/1

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶0⁸0¹0¹
	# [choose] min_ratio: 2.0 | min_chain: ⟨chain:1321|av:6⟩ | min_nodes:
	# (1, '0121251')
	# (2, '0121250')
	# (2, '0121253')
	# (2, '0121254')
	# (2, '0121255')
	# (3, '0121252')
	et('0121251') # 0/6

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶0⁸0¹0¹0⁶
	# [choose] min_ratio: 3.0 | min_chain: ⟨chain:761|av:1⟩ | min_nodes:
	# (3, '0033053')
	et('0033053') # 0/1

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶0⁸0¹0¹0⁶0¹
	# [choose] min_ratio: 2.2 | min_chain: ⟨chain:111|av:5⟩ | min_nodes:
	# (2, '0002360')
	# (2, '0002361')
	# (2, '0002364')
	# (2, '0002365')
	# (3, '0002366')
	et('0002360') # 0/5

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶0⁸0¹0¹0⁶0¹0⁵
	# [choose] min_ratio: 1.5714285714285714 | min_chain: ⟨chain:122|av:28⟩ | min_nodes:
	# (1, '0100060')
	# (1, '0100066')
	# (1, '0120065')
	# (1, '0120067')
	# (1, '1200152')
	# (1, '1200162')
	# (1, '1201060')
	# (1, '1210153')
	# (1, '1210160')
	# (1, '1210162')
	# (1, '1220066')
	# (1, '1220067')
	# (2, '0100064')
	# (2, '0100065')
	# (2, '0120060')
	# (2, '0120061')
	# (2, '0120066')
	# (2, '1200064')
	# (2, '1200154')
	# (2, '1200155')
	# (2, '1200163')
	# (2, '1200164')
	# (2, '1201061')
	# (2, '1201062')
	# (2, '1201063')
	# (2, '1210155')
	# (2, '1210164')
	# (2, '1211063')	
	et('0100060') # 0/28
	
	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶0⁸0¹0¹0⁶0¹0⁵0²⁸
	# [choose] min_ratio: 3.0 | min_chain: ⟨chain:98|av:1⟩ | min_nodes:
	# (3, '0002201')	
	et('0002201') # 0/1

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶0⁸0¹0¹0⁶0¹0⁵0²⁸0¹		
	# [choose] min_ratio: 1.5 | min_chain: ⟨chain:85|av:4⟩ | min_nodes:
	# (1, '0002010')
	# (1, '0002016')
	# (2, '0002011')
	# (2, '0002017')
	et('0002010') # 0/4
	
	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶0⁸0¹0¹0⁶0¹0⁵0²⁸0¹0⁴
	# [choose] min_ratio: 2.0 | min_chain: ⟨chain:1324|av:1⟩ | min_nodes:
	# (2, '0121313')
	et('0121313') # 0/1

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶0⁸0¹0¹0⁶0¹0⁵0²⁸0¹0⁴0¹
	# [choose] min_ratio: 1.5 | min_chain: ⟨chain:90|av:4⟩ | min_nodes:
	# (1, '0002063')
	# (1, '0002064')
	# (2, '0002060')
	# (2, '0002061')
	et('0002063') # 0/4

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶0⁸0¹0¹0⁶0¹0⁵0²⁸0¹0⁴0¹0⁴
	# [choose] min_ratio: 1.0 | min_chain: ⟨chain:104|av:1⟩ | min_nodes:
	# (1, '0002265')
	et('0002265') # 0/1

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶0⁸0¹0¹0⁶0¹0⁵0²⁸0¹0⁴0¹0⁴0¹
	# [choose] min_ratio: 1.0 | min_chain: ⟨chain:272|av:1⟩ | min_nodes:
	# (1, '0011260')
	et('0011260') # 0/1

	# $.0⁵0¹0⁷0¹0⁶0⁸0¹0⁶0⁶0¹0⁶0⁸0¹0¹0⁶0¹0⁵0²⁸0¹0⁴0¹0⁴0¹0¹
	# [choose] min_ratio: 2.0 | min_chain: ⟨chain:769|av:1⟩ | min_nodes:
	# (2, '0033160')
	et('0033160') # 0/1
	
	ot()
	
	# diagram.point()
	# show(diagram)	
	
	# ~ purge ~ #

	purge_unavailed, next_sample_lengths_per_loop_tuple = purge()

	# ~ choose next ~ #
	
	next_sample_length_ratios_per_chain = {}
	for chain in diagram.chains:		
		next_sample_length_ratios_per_chain[chain] = sum([next_sample_lengths_per_loop_tuple[node.loop.tuple] for node in chain.avnodes]) / len(chain.avnodes) # [!] need no empty chains here			

	singles = [chain for chain in diagram.chains if len(chain.avnodes) == 1]
	if len(singles):
		print(f"[choose] singles: {len(singles)}")
		min_ratio = min([r for c,r in next_sample_length_ratios_per_chain.items() if c in singles])
		min_chain = sorted([c for c,r in next_sample_length_ratios_per_chain.items() if r == min_ratio and c in singles], key = lambda c: c.avnodes[0].address)[0]		
		min_nodes = min_chain.avnodes
	else:
		min_ratio = min([r for c,r in next_sample_length_ratios_per_chain.items()])
		min_chain = sorted([c for c,r in next_sample_length_ratios_per_chain.items() if r == min_ratio], key = lambda c: (len(c.avnodes), c.id))[0]
		min_nodes = sorted(min_chain.avnodes, key = lambda n: (next_sample_lengths_per_loop_tuple[n.loop.tuple], n.address))
		
	print(f"[choose] min_ratio: {min_ratio} | min_chain: {min_chain} | min_nodes:\n{NEWLINE.join([str((next_sample_lengths_per_loop_tuple[n.loop.tuple], n.address)) for n in min_nodes])}")
								
	# ~ back ~ #
	# jump()
	
	# x6 = et('1000400') # 0/3 {0o4v7b}
	# x6 = et('1000422') # 0/2 {2v3r}
	# x6 = et('1000462') # 0/3 {2y5v6r}
	# x6 = et('1000431') # 0/4 {1v2r4o5y}
	# x6 = et('1000450') # 0/4 {0r2o3y6v}
	
	
	
	
	# ---
	# elt('0210007', 3) # {a}		
	# eb('0201', 1) # {a}			
	# et('0201406') # {a}		
	# est('0022307', 2) # {a}	
	# x6 = elt('1220407', 2) # {a}				
	
	
	# diagram.draw_boxes += [(addr, 5) for addr in set(itertools.chain(*[[nln.address[:diagram.spClass-4] for nln in node.loop.nodes] 
	# 	for node in diagram.nodeByAddress['0000001'].tuple]))]
	# diagram.draw_boxes += [(addr, 3) for addr in set(itertools.chain(*[[nln.address[:diagram.spClass-4] for nln in node.loop.nodes] 
	# 	for node in diagram.nodeByAddress['0000065'].tuple]))]
	# diagram.draw_boxes += [(addr, 0) for addr in set(itertools.chain(*[[nln.address[:diagram.spClass-4] for nln in node.loop.nodes] 
	# 	for node in x2]))]
	# diagram.draw_boxes += [(addr, 7) for addr in set(itertools.chain(*[[nln.address[:diagram.spClass-4] for nln in node.loop.nodes] 
	# 	for node in x3]))]
	# diagram.draw_boxes += [(addr, 4) for addr in set(itertools.chain(*[[nln.address[:diagram.spClass-4] for nln in node.loop.nodes] 
	# 	for node in x4]))]
	# diagram.draw_boxes += [(addr, 1) for addr in set(itertools.chain(*[[nln.address[:diagram.spClass-4] for nln in node.loop.nodes] 
	# 	for node in x5]))]		
	# diagram.draw_boxes += [(addr, 1) for addr in set(itertools.chain(*[[nln.address[:diagram.spClass-4] for nln in node.loop.nodes] 
	# 	for node in x6]))]		

	# ab('0000001') # {a}
	# ab('0000002') # {b}
	# ab('0000064') # {y}
	# ab('0000065') # {z}

	diagram.pointers = min_nodes
	show(diagram)

	# ot()
	# 
	# diagram.point()
	# show(diagram)
	
	# ls = ot()			
	# diagram.pointers = itertools.chain(*[l.nodes for l in ls])
	# show(diagram)

	# tl(1); 
	# 
	# diagram.point()
	# show(diagram)
	# 
	# ql(1);
	# 
	# diagram.point()
	# show(diagram)	
