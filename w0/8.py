from diagram import *
from uicanvas import *
from common import *


def extend(addr):
	assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	print(f"[ex] ⇒ extended {addr}")
	
def et(addr):
	for node in diagram.nodeByAddress[addr].tuple:
		assert diagram.extendLoop(node.loop)
	print(f"[et] ⇒ extended tuple for {addr}")		
		
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

def elt(addr, ktype):
	extended = 0
	parentLoop = diagram.nodeByAddress[addr].loop
	knodes = [node for node in itertools.chain(*[node.cycle.nodes for node in parentLoop.nodes]) if node.loop.availabled and node.loop.ktype == ktype]
	for i,node in enumerate(knodes):
		if not node.loop.extended:
			for n in node.tuple:
				assert diagram.extendLoop(n.loop)
				extended += 1
	print(f"[elt] ⇒ extended {extended} ktype:{ktype} loops for parent {parentLoop}")
	
def es(addr, ktype):
	parentLoop = diagram.nodeByAddress[addr].loop
	knodes = [node for node in itertools.chain(*[node.cycle.nodes for node in parentLoop.nodes]) if node.loop.availabled and node.loop.ktype == ktype and node.address[5] not in ['0', str(diagram.spClass-2)]]
	for i,node in enumerate(knodes):
		if not node.loop.extended:
			assert diagram.extendLoop(node.loop)
	print(f"[el] ⇒ extended ktype:{ktype} loops for parent {parentLoop}")
	
def ql():
	unavailed = 0 
	brokenCount = 0
	for parentLoop in diagram.loops:
		if parentLoop.ktype == 0:
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
			

if __name__ == "__main__":
	
	diagram = Diagram(8, 1)			
	
	diagram.pointers = [(n if i % 2 == 0 else n.links[1].next) for i,n in enumerate(diagram.bases)]
			
	#extend('0000001')	
	et('0000001')	
	
	L2(); JP(5); L1(); # EX()
	elt('1000007', 5) # 1. 0/3 - violet5/red4/orange3
	elt('1200407', 3)	# 1c.
			
	# ∘ blue
	et('1000107')
	et('1000307')
	et('1000507')
			
	#diagram.pointers = diagram.nodeByAddress['1200401'].tuple
			
	'''
	et('1001007')
	et('1001207')
	et('1001407')
		
	et('1000206') # 1. 0/2 - green2
	el('1000007', 3) # 2. 0/3 - orange3/red4/violet5
	el('1004207', 7) # 2b. black7
	el('1004407', 4) # 2b. red4
	
	#es('0004107', 4) # 3. 0/2 - red4/violet5
	#
	
	#extend('0034325') # T - indigo6
	#es('1133407', 6) # T - indigo6
	#extend('0034525') # T - yellow2
	#es('0030407', 2) # T - yellow2
			
	tl(0); ql()
	'''
	'''
	
	et('1001007')
	et('1010007')
	et('1100007')
	
	#diagram.pointers = diagram.bases
	
	# 
	#et('0010007')
	#et('0020007')
	#et('0020106')
	
	# --- ∘ blue/green ∘ ------------------------------------------- #
	
	# --- 1 --- #
	
	# {1} 0000
	# et('0000007')
	
	# {1} 1234
	# et('1234007')

	# --- 2 --- #

	# {2} 0020 | 0102
	# et('0020007')
					
	# {2} 1132 | 1214
	# et('1132007')

	# --- 6:3/3 --- #
		
	# {6:3/3} 0011 0012 0021 | 0101 0110 0111
	# et('0011007')
	# et('0011106')
	# et('0011207')

	# {6:3/3} 1123 1124 1133 | 1213 1222 1223
	# et('1123007')
	# et('1123106')
	# et('1123207')
	
	# --- 6:3/2/1 --- #
		
	# {6:3/2/1} 0002 0003 0030 | 0120 | 1001 1010
	# et('0002007')
	# et('0002106')
	# et('0002207')
	
	# {6:3/2/1} 0010 0013 0022 | 0100 | 0200 0201
	# et('0010007')
	# et('0010106')
	# et('0010207')
	
	# {6:3/2/1} 0224 0233 | 1114 | 1204 1231 1232
	# et('0224007')
	# et('0224106')
	# et('0224207')
	
	# {6:3/2/1} 1033 1034 | 1134 | 1212 1221 1224
	# et('1033007')
	# et('1033106')
	# et('1033207')
		
	# --- 6:2/1/1/1/1 --- #

	# {6:2/1/1/1/1} 0023 | 0104 | 0223 0231 | 1110 | 1201
	# et('0023007')
	# et('0023106')
	# et('0023207')
	
	# {6:2/1/1/1/1} 0024 | 0103 0133 | 0230 | 1020 | 1202
	# et('0024007')
	# et('0024106')
	# et('0024207')
	
	# {6:2/1/1/1/1} 0032 | 0214 | 1004 | 1101 1131 | 1210
	# et('0032007')
	# et('0032106')
	# et('0032207')
					
	# {6:2/1/1/1/1} 0033 | 0124 | 1003 1011 | 1130 | 1211
	# et('0033007')
	# et('0033106')
	# et('0033207')	
	
	# --- 3 --- #
	
	# {3} 0014 | 0232 | 1200
	# et('0014007')

	# {3} 0034 | 1002 | 1220
	# et('0034007')

	# {3} 0113 | 0222 | 1111
	# et('0113007')
	
	# {3} 0211 | 1031 | 1104
	# et('0211007')	

	# {3} 0123 | 1012 | 1121
	# et('0123007')
	
	# {3} 0130 | 0203 | 1023
	# et('0130007')
		
	# --- 6:3/1/1/1 --- #
	
	# {6:3/1/1/1} 0001 0004 0031 | 0210 | 1000 | 1100
	# et('0001007')
	# et('0001106')
	# et('0001207')
	
	# {6:3/1/1/1} 0112 0114 0132 | 0221 | 1021 | 1112
	# et('0112007')
	# et('0112106')
	# et('0112207')	
	
	# {6:3/1/1/1} 0121 | 0212 | 1014 1030 1032 | 1103
	# et('0121007')
	# et('0121106')
	# et('0121207')
	
	# {6:3/1/1/1} 0122 | 0213 | 1013 | 1102 1120 1122
	# et('0122007')
	# et('0122106')
	# et('0122207')
	
	# {6:3/1/1/1} 0131 | 0202 0204 0220 | 1022 | 1113
	# et('0131007')
	# et('0131106')
	# et('0131207')
	
	# {6:3/1/1/1} 0134 | 0234 | 1024 | 1203 1230 1233
	# et('0134007')
	# et('0134106')
	# et('0134207')	
			
	# --- ∘ ----/----- ∘ ------------------------------------------- #
	# --- ∘ columns ∘ ---------------------------------------------- #
	
	# et('0011111')
	# et('0011120')
	# et('0011145')
	# et('0011154')
	
	# et('0011112')
	# et('0011121')
	# et('0011130')
	# et('0011155')	
	'''
	'''
	# long column
	et('1234000')
	et('1234025')
	et('1234034')

	# short column
	et('1234014')
	et('1234023')

	# green
	et('1233106')
	et('1232206')
							
	# blue
	et('1233007')
	et('1233207')	
	et('1233407')	
	
	et('1232107')
	et('1232307')		
	et('1232507') 
									
	tl(0); ql();
	'''
	'''

	# blue
	et('1233307')
	et('1233407')
	

	et('1224007')
	et('1224407')
	
	unavailed = 0
	for tuple in diagram.loop_tuples:
		avloops = [loop for loop in tuple if loop.availabled]
		if len(avloops) != 0 and len(avloops) != 6:
			unavailed += len(avloops)
			for loop in avloops:
				diagram.setLoopUnavailabled(loop)

	print(f"unavailed: {unavailed}")
	'''
	'''
	diagram.pointers = diagram.nodeByAddress['0020007'].tuple
	for node in diagram.pointers:
		diagram.extendLoop(node.loop)

	diagram.pointers = diagram.nodeByAddress['0020106'].tuple	
	for node in diagram.pointers:
		diagram.extendLoop(node.loop)

	diagram.pointers = diagram.nodeByAddress['0020207'].tuple	
	for node in diagram.pointers:
		diagram.extendLoop(node.loop)

	diagram.pointers = diagram.nodeByAddress['0020311'].tuple	
	for node in diagram.pointers:
		diagram.extendLoop(node.loop)

	diagram.pointers = diagram.nodeByAddress['0020320'].tuple	
	for node in diagram.pointers:
		diagram.extendLoop(node.loop)

	diagram.pointers = diagram.nodeByAddress['0020345'].tuple	
	for node in diagram.pointers:
		diagram.extendLoop(node.loop)

	diagram.pointers = diagram.nodeByAddress['0020354'].tuple	
	for node in diagram.pointers:
		diagram.extendLoop(node.loop)
								
	#diagram.extendLoop(diagram.nodeByAddress['0000004'].loop)
	'''
	
	diagram.point()
	show(diagram)
