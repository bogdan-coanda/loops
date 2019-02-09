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
	extended = 0
	parentLoop = diagram.nodeByAddress[addr].loop
	knodes = [node for node in itertools.chain(*[node.cycle.nodes for node in parentLoop.nodes]) if node.loop.availabled and node.loop.ktype == ktype and node.address[5] not in ['0', str(diagram.spClass-2)]]
	for i,node in enumerate(knodes):
		if not node.loop.extended:
			assert diagram.extendLoop(node.loop)
			extended += 1
	print(f"[es] ⇒ extended {extended} ktype:{ktype} loops for parent {parentLoop}")

def est(addr, ktype):
	extended = 0
	parentLoop = diagram.nodeByAddress[addr].loop
	knodes = [node for node in itertools.chain(*[node.cycle.nodes for node in parentLoop.nodes]) if node.loop.availabled and node.loop.ktype == ktype and node.address[5] not in ['0', str(diagram.spClass-2)]]
	for i,node in enumerate(knodes):
		if not node.loop.extended:
			for n in node.tuple:
				assert diagram.extendLoop(n.loop)
				extended += 1
	print(f"[est] ⇒ extended {extended} ktype:{ktype} loops for parent {parentLoop}")
			
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
			

if __name__ == "__main__":
	
	diagram = Diagram(8, 1)			
	
	#diagram.pointers = [(n if i % 2 == 0 else n.links[1].next) for i,n in enumerate(diagram.bases)]
			
	# ∘ bases # [0.]
	extend('0000001')	
	#et('0000001')	

	# ∘ blue # [1.]
	et('1000107')
	et('1000307')
	et('1000507')

	et('1001007')
	et('1001207')
	et('1001407') 
	
	# ∘ green # [2.]
	# et('1000206') # 0/2 - green2

	# ∘ long column # [3.]
	elt('1000007', 5) # 0/3 - violet5/red4/orange3
	elt('1200407', 3)	# 3c.
	
	# ∘ 1st blue # [3..]
	et('1004007') # 3d.
	et('1004207') # 3d.
	et('1004407') # 3d.

	et('1114007') # 3e.
	et('1114207') # 3e.
	et('1114407') # 3e.		
			
	et('0013007') # 3f.
	et('0013207') # 3f.
	et('0013407') # 3f.		

	et('0104007') # 3g.
	et('0104207') # 3g.
	et('0104407') # 3g.

	et('1123007') # 3h.
	et('1123207') # 3h.
	et('1123407') # 3h.
	
	# ∘ short column # [4.]
	est('1000207', 2) # 0/3 - yellow2/orange3/red4
	est('1033107', 4) # 4c.

	# ∘ 2nd blue # [4..]
	et('1033007') # 4d.
	et('1033207') # 4d.
	et('1033407') # 4d.	

	et('0033007') # 4e.
	et('0033207') # 4e.
	et('0033407') # 4e.
	
	# ∘ alt diag # [5.]
	elt('1000206', 3) # 0/2 - orange3/green1
	elt('1220007', 7) # 5b. long column
	elt('1220207', 5) # 5c.
	
	# ∘ 3rd blue # [5..]
	et('0011007') # 5d.
	et('0011207') # 5d.
	et('0011407') # 5d.	

	et('0024007') # 5e.
	et('0024207') # 5e.
	et('0024407') # 5e.

	et('0234007') # 5f.
	et('0234207') # 5f.
	et('0234407') # 5f.
				
	# ∘ 1st green # [5.]
	# et('1001106') # 5a.	
	# et('1003406') # 5b.
	# et('1004306') # 5c.
	# et('1033106') # 5d.
	# et('1123106') # 5e.
	
	# pair # [6.]
	# et('0001200') # 0/2 red:0/blue:7
	# et('1000400') # 0/2 orange:0/yellow:1
	# et('1003202') # 0/2 violet:2/blue:7
	# et('0214502') # 0/2 black:2/blue:7
	# et('1033502') # 0/2 orange:2/blue:7
	
	
	# et('1003107') # 4d.
	# et('1003307') # 4d.
	# et('1003507') # 4d.

	# 
	# 
	# 
	# et('0013007') # 3k.
	# et('0013207') # 3k.
	# et('0013407') # 3k.
	# 
	# et('0023107') # 3k.
	# et('0023307') # 3k.
	# et('0023507') # 3k.
	# 
	# ∘ blue extra
	# et('1000407') # 4a.
	# et('1001307') # 4a.		
	# et('1003207') # 4a.		
	# et('1004107') # 4a.
	# 
	# et('1033507') # 4b.			
	# et('1110007') # 4b.			
	# et('1114507') # 4b.
	# et('1123507') # 4b.
	
	# et('0010207') # 4c.
	
	# elt('1003007', 5) # 5.
	# elt('1001507', 7) # 5c.			

	# ∘ 2nd-ish green		
	# et('0010406')	# 6a.
	# et('0023206')	# 6a.
	# 
	# et('1233106') # 6b.
	# et('1232206') # 6b.
	# 
	# et('0011306')	# 6c.	
	# et('0024106')	# 6c.	
					
	# ∘ 2nd blue
	# et('1024007') # 7a.
	# et('1024207') # 7a.
	# et('1024407') # 7a.	
	# 
	# et('1020107') # 7b.
	# et('1020307') # 7b.
	# et('1020507') # 7b.
	# 
	# et('0011007') # 7c.
	# et('0011207') # 7c.
	# et('0011407') # 7c.		
	
	
	
	# ∘ 2nd blue extra
	#et('1020007')	# 8a.
	#et('1024507')	# 8a.
	# diagram.pointers = diagram.nodeByAddress['1024507'].tuple
		
	# et('0011107')	# 8b.	
	#et('0011100') # 8bx.
	
	#diagram.pointers = diagram.nodeByAddress['0011100'].tuple
	
	#est('0010407', 6) # 9a. 2/3 - yellow2/violet5/indigo6
	#est('1233107', 5) # 9b. 1/2 - yellow2/violet5
	#et('0020100')
	
	# est('0024107', 7) # 9c. 1/2 - indigo6/black7
	# est('0224407', 6) # 9d. 1/2 - orange3/indigo6
	
	# extend('1234107') # 1/2
	# extend('1234250') # 0/1
	# extend('1234201') # 0/1
	# extend('1234307') # 0/1
	# extend('1234067') # 0/1
	
	# extend('1234106') # 0/2
	# extend('1234151') # 0/1
	# extend('1234506') # 0/2
	# extend('1234551') # 0/1
	# extend('1234306') # 0/2
	# extend('1234351') # 0/1	
	
	# ================================================================================================================================ #
	
	'''
		
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
	
	# long column
	# et('1234000') # 4. 0/2? - orange3/yellow2
	# et('1234025')
	# et('1234034')
		
	# short column
	# et('1234014') # 4b. - yellow2
	# et('1234023')
	

	# blue
	# et('1233007')
	# et('1233207')	
	# et('1233407')	

	# extend('1220107') # 5a. 0/1
	# extend('1002067') # 5b. 0/1
	# extend('0001207') # 6. 0/2
	# extend('0032467') # 7. 0/2
	# extend('0033367') # 8. 0/2
	# extend('0124507') # 9. 0/2
	# extend('0210067') # 10. 0/2
	# extend('0214507') # 11. 0/2
	# extend('1003207') # 12. 0/2
	# extend('1004107') # 13. 0/2
	# extend('1011067') # 14. 0/2
	# extend('1101067') # 15. 0/2
	# extend('1130467') # 16. 0/2
	# extend('1131367') # 17. 0/2
	# extend('1210207') # 18. 0/2
	# extend('1211107') # 19. 0/2	
	# 
	# 
	# extend('1002307') # 20. 0/2	
	# extend('0034267') # 21. 0/2	
	# extend('0034507') # 22. 0/2	
	# extend('1220467') # 23. 0/2	
	
	
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
	
	#L2(); JP(5); L1(); # EX()
		
	'''

	

	diagram.point()
	show(diagram)
			
	# tl(1); 
	# 
	# diagram.point()
	# show(diagram)
		
	# ql(1);
	# 
	# diagram.point()
	# show(diagram)	
