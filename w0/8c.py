from diagram import *
from uicanvas import *
from common import *
from mx import *
	

def jmp(bid): # jmp(from 0 to len(loopBrethren)-1)
	for i in range(len(diagram.pointers)):
		if i % 2 == 0:
			diagram.pointers[i] = diagram.pointers[i].loopBrethren[bid]
		else:
			diagram.pointers[i] = diagram.pointers[i].loopBrethren[-1-bid]				
			
def adv(cid): # adv(0) advances once, to match jmp(0) which jumps once
	for i in range(len(diagram.pointers)):
		if i % 2 == 0:
			for _ in range(1+cid):
				diagram.pointers[i] = diagram.pointers[i].links[1].next
		else:
			for _ in range(1+cid):
				diagram.pointers[i] = diagram.pointers[i].prevs[1].node


if __name__ == "__main__":

	diagram = Diagram(8, 1)
	
	import enav
	enav.diagram = diagram
	from enav import *	
		
	# ---------------------------- #
		
	# for column in diagram.columns:
	# 	print(f"{column}\n{'.'.join(sorted(column.box_addrs))}")
	
	gc = groupby(diagram.columns, K = lambda c: '.'.join(sorted(c.box_addrs)), G = lambda g: len(g))
	ks = list(gc.keys())
	
	for k in ks:
		print(k)
		for c in diagram.columns:
			if k == '.'.join(sorted(c.box_addrs)):
				print(c)
				
	print(f"distinct keys: {len(ks)}")
	
	ks = [k.split('.') for k in ks]
	
	print(ks[0])
	
	target = len(set(itertools.chain(*ks)))
	print(target)
	
	ps = {
		"A": set(ks[0]).union(ks[31]),
		"B": set(ks[1]).union(ks[30]),
		
		"C": set(ks[2]).union(ks[21]),
		"D₁": set(ks[3]).union(ks[20]),
		"D₂": set(ks[4]).union(ks[22]),
		"E": set(ks[5]).union(ks[16]),
		
		"F": set(ks[8]).union(ks[29]),
		"G": set(ks[9]).union(ks[17]),
		"H": set(ks[6]).union(ks[19]),
		"J": set(ks[7]).union(ks[18]),
		
		"K": set(ks[10]).union(ks[25]),
		"L": set(ks[11]).union(ks[27]),
		"M": set(ks[12]).union(ks[24]),
		"N": set(ks[13]).union(ks[23]),
		
		"P₁": set(ks[14]).union(ks[28]),
		"P₂": set(ks[15]).union(ks[26])
	}
	
	assert ps["D₁"] == ps["D₂"] and ps["P₁"] == ps["P₂"]
	ps["D"] = ps["D₁"]
	ps["P"] = ps["P₁"]
	del ps["D₁"] 
	del ps["D₂"] 
	del ps["P₁"] 
	del ps["P₂"]	
	
	keys = sorted(ps.keys())
	countsA = {x:0 for x in keys}
	countsB = {x:0 for x in keys}
	
	for i0 in range(0, len(ps)):
		for i1 in range(i0+1, len(ps)):
			for i2 in range(i1+1, len(ps)):
				for i3 in range(i2+1, len(ps)):
					for i4 in range(i3+1, len(ps)):
						indexes = [i0, i1, i2, i3, i4]
						if len(set(itertools.chain(*[ps[keys[i]] for i in indexes]))) == target:
							print([keys[i] for i in indexes])
							if keys[i0] == 'A':
								for i in indexes:
									countsA[keys[i]] += 1
							elif keys[i0] == 'B':
								for i in indexes:
									countsB[keys[i]] += 1								
									
	for k,v in sorted(countsA.items(), key = lambda p: -p[1]):
		if v > 0:
			print(f"({k}): {v}")

	for k,v in sorted(countsB.items(), key = lambda p: -p[1]):
		if v > 0:
			print(f"({k}): {v}")		
			
	# ---------------------------- #

	# avcolumns = [col for col in diagram.columns if col.isAvailabled()]
	# print(f"avcolumns: {len(avcolumns)}")	
	# for col in diagram.columns:
	# 	if not col.isAvailabled():
	# 		print(f'not av: {col}')
			
	# extend('0000001'); # ex:a0	
	# x0 = et('0000001') # {0:a}	
	# x0 = et('0000002') # {1:b}
	# x1 = et('0000064') # {0:y}	
	# x1 = et('0000065') # {1:z}
				
	# ex:a[0-5]
	# for node in diagram.bases:
	# 	extend(node.address)
	# 	print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
	# 	for col in avcolumns:
	# 		if not col.isAvailabled():
	# 			print(f'not av: {col}')		
	# 	diagram.collapseBack(node.loop)
	# 
	# ex:b[0-5]
	# diagram.pointers = diagram.bases
	# L1()	
	# for node in diagram.pointers:
	# 	extend(node.address)
	# 	print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
	# 	for col in avcolumns:
	# 		if not col.isAvailabled():
	# 			print(f'not av: {col}')		
	# 	diagram.collapseBack(node.loop)

	# ex:y[0-5]
	# diagram.pointers = diagram.bases
	# adv(5); jmp(5); adv(4)
	# for node in diagram.pointers:
	# 	extend(node.address)
	# 	print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
	# 	for col in avcolumns:
	# 		if not col.isAvailabled():
	# 			print(f'not av: {col}')		
	# 	diagram.collapseBack(node.loop)				

	# ex:z[0-5]
	# diagram.pointers = diagram.bases
	# adv(5); jmp(5); adv(5)
	# for node in diagram.pointers:
	# 	extend(node.address)
	# 	print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
	# 	for col in avcolumns:
	# 		if not col.isAvailabled():
	# 			print(f'not av: {col}')		
	# 	diagram.collapseBack(node.loop)				
				
	# ---------------------------- #			
			
	''' §.
	avcolumns: 122
	not av: ⟨column:0@0000005(ktype:2)|t:3|cL:18|bb:13⟩
	not av: ⟨column:1@0000004(ktype:3)|t:6|cL:36|bb:13⟩
	not av: ⟨column:2@0000003(ktype:4)|t:6|cL:36|bb:13⟩
	not av: ⟨column:3@0000002(ktype:5)|t:6|cL:36|bb:13⟩
	not av: ⟨column:4@0000001(ktype:6)|t:6|cL:36|bb:13⟩
	not av: ⟨column:5@0000000(ktype:7)|t:3|cL:18|bb:13⟩	
	'''
	''' §.ex:a.
	[ex] ⇒ extended 0000001
	[ex] ⇒ extended 0000165	
	[ex] ⇒ extended 0000201	
	[ex] ⇒ extended 0000365	
	[ex] ⇒ extended 0000401	
	[ex] ⇒ extended 0000565	
	avcolumns: 119
	not av: ⟨column:18@0001303(ktype:6)|t:6|cL:36|bb:27⟩
	not av: ⟨column:25@0001501(ktype:6)|t:6|cL:36|bb:27⟩
	not av: ⟨column:34@0002204(ktype:5)|t:6|cL:36|bb:15⟩
	'''
	''' $.ex:b
	[ex] ⇒ extended 0000002
	[ex] ⇒ extended 0000164
	[ex] ⇒ extended 0000202
	[ex] ⇒ extended 0000364
	[ex] ⇒ extended 0000402
	[ex] ⇒ extended 0000564
	avcolumns: 119
	not av: ⟨column:13@0001201(ktype:3)|t:6|cL:36|bb:27⟩
	not av: ⟨column:16@0001300(ktype:3)|t:6|cL:36|bb:27⟩
	not av: ⟨column:49@0010200(ktype:4)|t:6|cL:36|bb:15⟩	
	'''
	''' §.ex:y.
	[ex] ⇒ extended 0000064
	[ex] ⇒ extended 0000102
	[ex] ⇒ extended 0000264
	[ex] ⇒ extended 0000302
	[ex] ⇒ extended 0000464
	[ex] ⇒ extended 0000502
	avcolumns: 119
	not av: ⟨column:9@0001000(ktype:6)|t:6|cL:36|bb:27⟩
	not av: ⟨column:15@0001204(ktype:6)|t:6|cL:36|bb:27⟩
	not av: ⟨column:28@0002000(ktype:5)|t:6|cL:36|bb:15⟩	
	'''
	''' §.ex:z.
	[ex] ⇒ extended 0000065
	[ex] ⇒ extended 0000101
	[ex] ⇒ extended 0000265
	[ex] ⇒ extended 0000301
	[ex] ⇒ extended 0000465
	[ex] ⇒ extended 0000501
	avcolumns: 119
	not av: ⟨column:10@0001102(ktype:3)|t:6|cL:36|bb:27⟩
	not av: ⟨column:22@0001504(ktype:3)|t:6|cL:36|bb:27⟩
	not av: ⟨column:47@0010101(ktype:4)|t:6|cL:36|bb:15⟩	
	'''
	# for id in [0, 1, 2, 3, 4, 5,
	# 	18, 25, 34,
	# 	13, 16, 49,
	# 	 9, 15, 28,
	# 	10, 22, 47
	# ]:
	# 	diagram.columnByID[id].unavailabled = True
						
	avcolumns = [col for col in diagram.columns if col.isAvailabled()]
	print(f"avcolumns: {len(avcolumns)}")	
	
	# ---------------------------- #			
	
	# ∘ long column 
	# ec('0001003') # [C] [⟨column:6@0001003(ktype:3)|t:6|cL:36|bb:27⟩]	# x3 = elt('1000007', 5) # {a}		
	# x3 = elt('1000006', 5) # {y}	
	# x3 = elt('1000206', 2) # {b}	
	# ec('0001402') # [E] [⟨column:21@0001402(ktype:6)|t:6|cL:36|bb:27⟩] # x3 = elt('1000207', 2) # {z}		
	
	''' §.0:elt:a.
	[elt] ⇒ extended 36 ktype:3 loops for parent ⟨loop:[blue:6]:0001007|⟩ # column:6
	avcolumns: 105
	not av: ⟨column:6@0001003(ktype:3)|t:6|cL:36|bb:27⟩
	not av: ⟨column:7@0001002(ktype:4)|t:6|cL:36|bb:27⟩
	not av: ⟨column:42@0010005(ktype:2)|t:6|cL:36|bb:15⟩
	not av: ⟨column:66@0014001(ktype:6)|t:6|cL:36|bb:27⟩
	not av: ⟨column:73@0023002(ktype:5)|t:6|cL:36|bb:26⟩	
	'''
	''' §.0:elt:z.
	[elt] ⇒ extended 36 ktype:6 loops for parent ⟨loop:[blue:10]:0001407|⟩ # column:21
	avcolumns: 105
	not av: ⟨column:20@0001403(ktype:5)|t:6|cL:36|bb:27⟩
	not av: ⟨column:21@0001402(ktype:6)|t:6|cL:36|bb:27⟩
	not av: ⟨column:29@0002003(ktype:7)|t:6|cL:36|bb:15⟩
	not av: ⟨column:83@0024001(ktype:5)|t:6|cL:36|bb:27⟩
	not av: ⟨column:98@0032204(ktype:6)|t:6|cL:36|bb:26⟩	
	'''
	# for id in [
	# 	 6,  7, 42, 66, 73,
	# 	21, 20, 29, 83, 98
	# ]:
	# 	diagram.columnByID[id].unavailabled = True	
		
	# ---------------------------- #			

	avcolumns = [col for col in diagram.columns if col.isAvailabled()]
			
	# ex:a[0-5]
	# for node in diagram.bases:
	# 	extend(node.address)
	# 	print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
	# 	for col in avcolumns:
	# 		if not col.isAvailabled():
	# 			print(f'not av: {col}')		
	# 	diagram.collapseBack(node.loop)

	# ex:z[0-5]
	# diagram.pointers = diagram.bases
	# adv(5); jmp(5); adv(5)
	# for node in diagram.pointers:
	# 	extend(node.address)
	# 	print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
	# 	for col in avcolumns:
	# 		if not col.isAvailabled():
	# 			print(f'not av: {col}')		
	# 	diagram.collapseBack(node.loop)						

	''' §.0:elt:a.ex:a
	[ex] ⇒ extended 0000001…
	not av: ⟨column:50@0010204(ktype:6)|t:6|cL:36|bb:26⟩
	not av: ⟨column:53@0010401(ktype:2)|t:3|cL:18|bb:15⟩	
	'''
	''' §.0:elt:z.ex:z
	[ex] ⇒ extended 0000065…
	not av: ⟨column:30@0002101(ktype:3)|t:6|cL:36|bb:26⟩
	not av: ⟨column:41@0002504(ktype:7)|t:3|cL:18|bb:15⟩	
	'''
	# for id in [
	# 	50, 53,
	# 	30, 41
	# ]:
	# 	diagram.columnByID[id].unavailabled = True	
		
	print(f"avcolumns: {len([col for col in diagram.columns if col.isAvailabled()])}")			
	for col in avcolumns:
		if not col.isAvailabled():
			print(f'not av: {col}')			

	# ---------------------------- #			

	avcolumns = [col for col in diagram.columns if col.isAvailabled()]
	print(f"avcolumns: {len(avcolumns)}")			

	# ec('0010104') # [K] ⟨column:46@0010104(ktype:2)|t:6|cL:36|bb:15⟩ # 1:elt:a
	# ec('0002102') # [G] ⟨column:32@0002102(ktype:7)|t:6|cL:36|bb:15⟩ # 1:elt:z
	for col in avcolumns:
		if not col.isAvailabled():
			print(f'not av: {col}')			
				
	avcolumns = [col for col in diagram.columns if col.isAvailabled()]
	print(f"avcolumns: {len(avcolumns)}")
			
	# ex:a[0-5]
	# for node in diagram.bases:
	# 	extend(node.address)
	# 	print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
	# 	for col in avcolumns:
	# 		if not col.isAvailabled():
	# 			print(f'not av: {col}')		
	# 	diagram.collapseBack(node.loop)			

	# ex:z[0-5]
	# diagram.pointers = diagram.bases
	# adv(5); jmp(5); adv(5)
	# for node in diagram.pointers:
	# 	extend(node.address)
	# 	print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
	# 	for col in avcolumns:
	# 		if not col.isAvailabled():
	# 			print(f'not av: {col}')		
	# 	diagram.collapseBack(node.loop)						


	''' §.0:elt:a.1:elt:a
	[elt] ⇒ extended 36 ktype:2 loops for parent ⟨loop:[blue:31]:0010107|⟩
	not av: ⟨column:45@0010000(ktype:6)|t:6|cL:36|bb:26⟩
	not av: ⟨column:46@0010104(ktype:2)|t:6|cL:36|bb:15⟩
	not av: ⟨column:59@0011000(ktype:5)|t:6|cL:36|bb:15⟩	
	'''
	''' §.0:elt:z.1:elt:z
	[elt] ⇒ extended 36 ktype:7 loops for parent ⟨loop:[blue:13]:0002107|⟩
	not av: ⟨column:32@0002102(ktype:7)|t:6|cL:36|bb:15⟩
	not av: ⟨column:33@0002200(ktype:3)|t:6|cL:36|bb:26⟩
	not av: ⟨column:60@0011100(ktype:4)|t:6|cL:36|bb:15⟩	
	'''
	# for id in [
	# 	46, 45, 59,
	# 	32, 33, 60
	# ]:
	# 	diagram.columnByID[id].unavailabled = True	
		
	avcolumns = [col for col in diagram.columns if col.isAvailabled()]
	print(f"avcolumns: {len(avcolumns)}")

	# ---------------------------- #			

	# ∘ blue {az} # 2:blue
	# et('1000107') 
	
	# ∘ green # 3:green
	# et('1000206') # {a}
	# et('1000006') # {z}

	avcolumns = [col for col in diagram.columns if col.isAvailabled()]
	print(f"avcolumns: {len(avcolumns)}")
	
	# ∘ blue {az} follow-up # 4:blue
	# et('1000307') 
	# et('1000407')
	# et('1000507')	
					
	# ex:a[0-5]
	# for node in diagram.bases:
	# 	extend(node.address)
	# 	print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
	# 	for col in avcolumns:
	# 		if not col.isAvailabled():
	# 			print(f'not av: {col}')		
	# 	diagram.collapseBack(node.loop)

	# ex:z[0-5]
	# diagram.pointers = diagram.bases
	# adv(5); jmp(5); adv(5)
	# for node in diagram.pointers:
	# 	extend(node.address)
	# 	print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
	# 	for col in avcolumns:
	# 		if not col.isAvailabled():
	# 			print(f'not av: {col}')		
	# 	diagram.collapseBack(node.loop)						
		
	''' §.0:elt:{az}.1:elt:{az}.2:blue
	[et] ⇒ extended 6 loops in tuple for 1000107
	avcolumns: 88
	not av: ⟨column:23@0001503(ktype:4)|t:6|cL:36|bb:27⟩
	not av: ⟨column:24@0001502(ktype:5)|t:6|cL:36|bb:27⟩	
	'''
	''' §.0:elt:a.1:elt:a.2:blue.3:green:a
	[et] ⇒ extended 6 loops in tuple for 1000206
	avcolumns: 86
	not av: ⟨column:12@0001100(ktype:5)|t:6|cL:36|bb:27⟩
	not av: ⟨column:14@0001200(ktype:4)|t:6|cL:36|bb:27⟩
	[ex] ⇒ extended 0000001…
	not av: ⟨column:48@0010100(ktype:5)|t:6|cL:36|bb:27⟩	
	'''
	''' §.0:elt:z.1:elt:z.2:blue.3:green:z
	[et] ⇒ extended 6 loops in tuple for 1000006
	avcolumns: 86
	not av: ⟨column:12@0001100(ktype:5)|t:6|cL:36|bb:27⟩
	not av: ⟨column:14@0001200(ktype:4)|t:6|cL:36|bb:27⟩
	[ex] ⇒ extended 0000065…
	avcolumns: 85	
	not av: ⟨column:31@0002100(ktype:4)|t:6|cL:36|bb:27⟩	
	'''
	''' §.0:elt:a.1:elt:a.2:blue.3:green:a.4:blue
	[et] ⇒ extended 6 loops in tuple for 1000307
	[et] ⇒ extended 6 loops in tuple for 1000407
	[et] ⇒ extended 6 loops in tuple for 1000507
	avcolumns: 84
	not av: ⟨column:11@0001101(ktype:4)|t:6|cL:36|bb:27⟩
	not av: ⟨column:17@0001304(ktype:5)|t:6|cL:36|bb:27⟩
	[ex] ⇒ extended 0000001…
	avcolumns: 83
	not av: ⟨column:48@0010100(ktype:5)|t:6|cL:36|bb:27⟩	
	'''
	''' §.0:elt:z.1:elt:z.2:blue.3:green:z.4:blue
	[et] ⇒ extended 6 loops in tuple for 1000307
	[et] ⇒ extended 6 loops in tuple for 1000407
	[et] ⇒ extended 6 loops in tuple for 1000507
	avcolumns: 84
	not av: ⟨column:11@0001101(ktype:4)|t:6|cL:36|bb:27⟩
	not av: ⟨column:17@0001304(ktype:5)|t:6|cL:36|bb:27⟩
	[ex] ⇒ extended 0000065
	avcolumns: 83
	not av: ⟨column:31@0002100(ktype:4)|t:6|cL:36|bb:27⟩	
	'''
	# for id in [
	# 	23, 24,
	# 	12, 14, 
	# 	48, 31,
	# 	11, 17
	# ]:
	# 	diagram.columnByID[id].unavailabled = True # ⇒ avcolumns: 82
		
	avcolumns = [col for col in diagram.columns if col.isAvailabled()]
	print(f"avcolumns: {len(avcolumns)}")			
	
	# ---------------------------- #			

	# ∘ short column # 5:est
	# est('1000207', 2) # [E] [⟨column:21@0001402(ktype:6)|t:6|cL:36|bb:27⟩] # {a} ~> 0:elt:z
	# x4 = est('1000206', 2) # {y}
	# x4 = est('1000006', 5) # {b}	
	# est('1000007', 5) # [C] [⟨column:6@0001003(ktype:3)|t:6|cL:36|bb:27⟩] # {z} ~> 0:elt:a

	print(f"avcolumns: {len([col for col in diagram.columns if col.isAvailabled()])}")			
	avcolumns = [col for col in diagram.columns if col.isAvailabled()]

	# ---------------------------- #			

	# nx = est('1220507', 2) # [C] [⟨column:93@0024403(ktype:5)|t:6|cL:36|bb:27⟩]
	# nx = est('1220507', 3) # [G] [⟨column:32@0002102(ktype:7)|t:6|cL:36|bb:15⟩] # ~> 1:elt:z
	# nx = est('1220507', 5) # [C] [⟨column:95@0024502(ktype:5)|t:6|cL:36|bb:27⟩]
	# nx = est('1220507', 7) # [K] [⟨column:109@0034300(ktype:6)|t:3|cL:18|bb:15⟩]

	print(f"avcolumns: {len([col for col in diagram.columns if col.isAvailabled()])}")			
	for col in avcolumns:
		if not col.isAvailabled():
			print(f'not av: {col}')			
	avcolumns = [col for col in diagram.columns if col.isAvailabled()]

	# nx += elt('1220007', 7)
	# nx += elt('1220107', 3)
	# nx += elt('1220207', 2)
	# 
	# nx += elt('1234007', 6)
	
	# nx = est('0232307', 7)

	# »»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»» #
	 
	print(f"avcolumns: {len([col for col in diagram.columns if col.isAvailabled()])}")			
	avcolumns = [col for col in diagram.columns if col.isAvailabled()]
		
	nx = []
	
	nx += elt('1000007', 5)
	nx += elt('1200407', 3)
	nx += est('1200507', 2)
	nx += est('1200107', 6)
	
	nx = est('1000207', 2)
	nx = est('1002107', 4)
	nx = elt('1002007', 5)
	nx = elt('1002407', 7)
									
	diagram.pointers = list(itertools.chain(*[itertools.chain(*[ntn.loop.nodes for ntn in n.tuple]) for n in nx]))
	show(diagram)

	print(f"avcolumns: {len([col for col in diagram.columns if col.isAvailabled()])}")			
	for col in avcolumns:
		if not col.isAvailabled():
			print(f'not av: {col}')			
	avcolumns = [col for col in diagram.columns if col.isAvailabled()]
	
	'''
	[ex] ⇒ extended 0000001… 
	avcolumns: 80
	not av: ⟨column:15@0001204(ktype:6)|t:6|cL:36|bb:27⟩
	not av: ⟨column:16@0001300(ktype:3)|t:6|cL:36|bb:27⟩
	not av: ⟨column:34@0002204(ktype:5)|t:6|cL:36|bb:15⟩
	not av: ⟨column:46@0010104(ktype:2)|t:6|cL:36|bb:15⟩
	not av: ⟨column:50@0010204(ktype:6)|t:6|cL:36|bb:26⟩
	not av: ⟨column:72@0023003(ktype:4)|t:6|cL:36|bb:27⟩
	not av: ⟨column:78@0023300(ktype:4)|t:6|cL:36|bb:27⟩
	not av: ⟨column:88@0024200(ktype:4)|t:6|cL:36|bb:27⟩
	'''		
	for id in [15, 16, 34, 46, 50, 72, 78, 88]:
		diagram.columnByID[id].unavailabled = True # ⇒ avcolumns: 80j
	
	print(f"avcolumns: {len([col for col in diagram.columns if col.isAvailabled()])}")			
	
	# »»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»» #
	
	# ex:a[0-5]
	# for node in diagram.bases:
	# 	extend(node.address)
	# 	print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
	# 	for col in avcolumns:
	# 		if not col.isAvailabled():
	# 			print(f'not av: {col}')		
	# 	diagram.collapseBack(node.loop)

	# ex:z[0-5]
	# diagram.pointers = diagram.bases
	# adv(5); jmp(5); adv(5)
	# for node in diagram.pointers:
	# 	extend(node.address)
	# 	print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
	# 	for col in avcolumns:
	# 		if not col.isAvailabled():
	# 			print(f'not av: {col}')		
	# 	diagram.collapseBack(node.loop)						
	
	'''	[C] [⟨column:93@0024403(ktype:5)|t:6|cL:36|bb:27⟩]
	[est] ⇒ extended 12 ktype:2 loops for parent ⟨loop:[blue:665]:1220507|Av|kF:16⟩
	avcolumns: 79
	not av: ⟨column:93@0024403(ktype:5)|t:6|cL:36|bb:27⟩
	not av: ⟨column:109@0034300(ktype:6)|t:3|cL:18|bb:15⟩
	not av: ⟨column:112@0113200(ktype:5)|t:3|cL:18|bb:15⟩
	'''
	''' # [G] [⟨column:32@0002102(ktype:7)|t:6|cL:36|bb:15⟩] # ~> 1:elt:z
	[est] ⇒ extended 24 ktype:3 loops for parent ⟨loop:[blue:665]:1220507|Av|kF:20⟩
	avcolumns: 77
	not av: ⟨column:39@0002503(ktype:3)|t:6|cL:36|bb:26⟩
	not av: ⟨column:94@0024503(ktype:4)|t:6|cL:36|bb:27⟩
	not av: ⟨column:95@0024502(ktype:5)|t:6|cL:36|bb:27⟩
	not av: ⟨column:108@0034201(ktype:6)|t:6|cL:36|bb:15⟩
	not av: ⟨column:125@0134201(ktype:5)|t:3|cL:18|bb:13⟩
	'''
	''' # [C] [⟨column:95@0024502(ktype:5)|t:6|cL:36|bb:27⟩]
	# [est] ⇒ extended 24 ktype:5 loops for parent ⟨loop:[blue:665]:1220507|⟩
	# avcolumns: 78
	# not av: ⟨column:26@0002002(ktype:3)|t:6|cL:36|bb:26⟩
	# not av: ⟨column:39@0002503(ktype:3)|t:6|cL:36|bb:26⟩
	# not av: ⟨column:52@0010303(ktype:6)|t:6|cL:36|bb:26⟩
	# not av: ⟨column:55@0010402(ktype:6)|t:6|cL:36|bb:26⟩	
	'''
	''' # [K] [⟨column:109@0034300(ktype:6)|t:3|cL:18|bb:15⟩]
	# [est] ⇒ extended 24 ktype:7 loops for parent ⟨loop:[blue:665]:1220507|⟩
	# avcolumns: 77
	# not av: ⟨column:37@0002404(ktype:3)|t:6|cL:36|bb:26⟩
	# not av: ⟨column:92@0024404(ktype:4)|t:6|cL:36|bb:27⟩
	# not av: ⟨column:93@0024403(ktype:5)|t:6|cL:36|bb:27⟩
	# not av: ⟨column:109@0034300(ktype:6)|t:3|cL:18|bb:15⟩
	# not av: ⟨column:124@0134102(ktype:5)|t:6|cL:36|bb:13⟩	
	'''
	
	print(f"avcolumns: {len([col for col in diagram.columns if col.isAvailabled()])}")			
	avcolumns = [col for col in diagram.columns if col.isAvailabled()]
				
	# ---------------------------- #			
															
	# [13] A / B 
	# [27] C / E 
	# [27] D₁ / D₂ 
	# [15] F / L 
	# [15] G / K	
	# [26] H / N 
	# [27] J / M 
	# [15] P₁ / P₂
	
	# - (A) - upper - [0:13] ~ 0000.0001.0002.0003.0004.0030.0031.0120.0210.1000.1001.1010.1100
	# - dead(§) -	# ⟨column:4@0000001(ktype:6)|t:6|cL:36|bb:13⟩
	# - dead(§) -	# ⟨column:2@0000003(ktype:4)|t:6|cL:36|bb:13⟩
	# - dead(§) -	# ⟨column:0@0000005(ktype:2)|t:3|cL:18|bb:13⟩		
	# - (A) - lower - [31:13] ~ 0134.0224.0233.0234.1024.1114.1203.1204.1230.1231.1232.1233.1234
	# ec('0134002') # ⟨column:123@0134002(ktype:6)|t:6|cL:36|bb:13⟩	
	# ec('0134200') # ⟨column:126@0134200(ktype:6)|t:6|cL:36|bb:13⟩	
	# ec('0134404') # ⟨column:127@0134404(ktype:6)|t:3|cL:18|bb:13⟩	
	
	# - (B) - upper - [1:13] ~ 0000.0001.0004.0010.0013.0022.0031.0100.0200.0201.0210.1000.1100
	# - dead(§) -	# ⟨column:1@0000004(ktype:3)|t:6|cL:36|bb:13⟩
	# - dead(§) - # ⟨column:3@0000002(ktype:5)|t:6|cL:36|bb:13⟩
	# - dead(§) - # ⟨column:5@0000000(ktype:7)|t:3|cL:18|bb:13⟩
	# - (B) - lower - [30:13] ~ 0134.0234.1024.1033.1034.1134.1203.1212.1221.1224.1230.1233.1234
	# ec('0134003')	# ⟨column:122@0134003(ktype:5)|t:6|cL:36|bb:13⟩
	# ec('0134102')	# ⟨column:124@0134102(ktype:5)|t:6|cL:36|bb:13⟩
	# ec('0134201')	# ⟨column:125@0134201(ktype:5)|t:3|cL:18|bb:13⟩
		
	# - (C) - upper - [2:27] ~ 0001.0004.0010.0013.0014.0022.0023.0031.0032.0100.0104.0200.0201.0210.0214.0223.0231.0232.1000.1004.1100.1101.1110.1131.1200.1201.1210
	# - .(0:elt:a). - # ⟨column:6@0001003(ktype:3)|t:6|cL:36|bb:27⟩
	# - dead(ex:z) - # ⟨column:10@0001102(ktype:3)|t:6|cL:36|bb:27⟩
	# - dead(ex:b) - # ⟨column:13@0001201(ktype:3)|t:6|cL:36|bb:27⟩
	# - dead(ex:b) - # ⟨column:16@0001300(ktype:3)|t:6|cL:36|bb:27⟩
	# - dead(ex:z) - # ⟨column:22@0001504(ktype:3)|t:6|cL:36|bb:27⟩
	# - (C) - lower - [21:27] ~ 0024.0033.0034.0103.0124.0133.0134.0230.0234.1002.1003.1011.1020.1024.1033.1034.1130.1134.1202.1203.1211.1212.1220.1221.1224.1230.1233
	# - dead(0:elt:z) - # ⟨column:83@0024001(ktype:5)|t:6|cL:36|bb:27⟩
	# ec('0024100') # ⟨column:86@0024100(ktype:5)|t:6|cL:36|bb:27⟩
	# ec('0024304') # ⟨column:90@0024304(ktype:5)|t:6|cL:36|bb:27⟩
	# ec('0024403') # ⟨column:93@0024403(ktype:5)|t:6|cL:36|bb:27⟩ # [~]
	# ec('0024502') # ⟨column:95@0024502(ktype:5)|t:6|cL:36|bb:27⟩ # [~]
		
	# - (D₁) - upper - [3:27] ~ 0001.0004.0031.0032.0121.0122.0210.0211.0212.0213.0214.1000.1004.1013.1014.1030.1031.1032.1100.1101.1102.1103.1104.1120.1122.1131.1210
	# - dead(0:elt:a) - # ⟨column:7@0001002(ktype:4)|t:6|cL:36|bb:27⟩
	# - dead(4:blue) - # ⟨column:11@0001101(ktype:4)|t:6|cL:36|bb:27⟩
	# - dead(3:green) - # ⟨column:14@0001200(ktype:4)|t:6|cL:36|bb:27⟩
	# ec('0001404') # ⟨column:19@0001404(ktype:4)|t:6|cL:36|bb:27⟩
	# - dead(2:blue) - # ⟨column:23@0001503(ktype:4)|t:6|cL:36|bb:27⟩
	# - (D₁) - lower - [20:27] ~ 0024.0103.0112.0114.0130.0131.0132.0133.0134.0202.0203.0204.0220.0221.0230.0234.1020.1021.1022.1023.1024.1112.1113.1202.1203.1230.1233
	# ec('0024002') # ⟨column:82@0024002(ktype:4)|t:6|cL:36|bb:27⟩
	# ec('0024101') # ⟨column:85@0024101(ktype:4)|t:6|cL:36|bb:27⟩
	# ec('0024200') # ⟨column:88@0024200(ktype:4)|t:6|cL:36|bb:27⟩
	# ec('0024404') # ⟨column:92@0024404(ktype:4)|t:6|cL:36|bb:27⟩
	# ec('0024503') # ⟨column:94@0024503(ktype:4)|t:6|cL:36|bb:27⟩	
	
	# - (D₂) - upper - [4:27] ~ 0001.0004.0031.0032.0122.0131.0202.0204.0210.0211.0213.0214.0220.1000.1004.1013.1022.1031.1100.1101.1102.1104.1113.1120.1122.1131.1210
	# ec('0001001') # ⟨column:8@0001001(ktype:5)|t:6|cL:36|bb:27⟩
	# - dead(3:green) - # ⟨column:12@0001100(ktype:5)|t:6|cL:36|bb:27⟩
	# - dead(4:blue) - # ⟨column:17@0001304(ktype:5)|t:6|cL:36|bb:27⟩
	# - dead(0:elt:z) - # ⟨column:20@0001403(ktype:5)|t:6|cL:36|bb:27⟩
	# - dead(2:blue) - # ⟨column:24@0001502(ktype:5)|t:6|cL:36|bb:27⟩
	# - (D₂) - lower - [22:27] ~ 0024.0103.0112.0114.0121.0130.0132.0133.0134.0203.0212.0221.0230.0234.1014.1020.1021.1023.1024.1030.1032.1103.1112.1202.1203.1230.1233
	# ec('0024003') # ⟨column:84@0024003(ktype:7)|t:6|cL:36|bb:27⟩
	# ec('0024102') # ⟨column:87@0024102(ktype:7)|t:6|cL:36|bb:27⟩
	# ec('0024201') # ⟨column:89@0024201(ktype:7)|t:6|cL:36|bb:27⟩
	# ec('0024300') # ⟨column:91@0024300(ktype:7)|t:6|cL:36|bb:27⟩
	# ec('0024504') # ⟨column:96@0024504(ktype:7)|t:6|cL:36|bb:27⟩	
	
	# - (E) - upper - [5:27] ~ 0001.0002.0003.0004.0030.0031.0032.0033.0034.0120.0124.0210.0214.1000.1001.1002.1003.1004.1010.1011.1100.1101.1130.1131.1210.1211.1220
	# - dead(ex:y) - # ⟨column:9@0001000(ktype:6)|t:6|cL:36|bb:27⟩
	# - dead(ex:y) - # ⟨column:15@0001204(ktype:6)|t:6|cL:36|bb:27⟩
	# - dead(ex:a) - # ⟨column:18@0001303(ktype:6)|t:6|cL:36|bb:27⟩
	# - .(0:elt:z). - # ⟨column:21@0001402(ktype:6)|t:6|cL:36|bb:27⟩
	# - dead(ex:a) - # ⟨column:25@0001501(ktype:6)|t:6|cL:36|bb:27⟩
	# - (E) - lower - [16:27] ~ 0014.0023.0024.0103.0104.0133.0134.0223.0224.0230.0231.0232.0233.0234.1020.1024.1110.1114.1200.1201.1202.1203.1204.1230.1231.1232.1233
	# ec('0014003') # ⟨column:64@0014003(ktype:4)|t:6|cL:36|bb:27⟩
	# - dead(0:elt:a) - # ⟨column:66@0014001(ktype:6)|t:6|cL:36|bb:27⟩
	# ec('0014102') # ⟨column:67@0014102(ktype:4)|t:6|cL:36|bb:27⟩
	# ec('0014100') # ⟨column:69@0014100(ktype:6)|t:6|cL:36|bb:27⟩
	# ec('0014201') # ⟨column:70@0014201(ktype:4)|t:6|cL:36|bb:27⟩

	# - (F) - upper - [8:15] ~ 0002.0003.0030.0120.0121.0130.0203.0212.1001.1010.1014.1023.1030.1032.1103
	# - dead(ex:y) - # ⟨column:28@0002000(ktype:5)|t:6|cL:36|bb:15⟩
	# - dead(ex:a) - # ⟨column:34@0002204(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0002303') # ⟨column:36@0002303(ktype:5)|t:3|cL:18|bb:15⟩
	# - (F) - lower - [29:15] ~ 0131.0202.0204.0211.0220.0224.0233.1022.1031.1104.1113.1114.1204.1231.1232
	# ec('0131001') # ⟨column:119@0131001(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0131100') # ⟨column:120@0131100(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0131304') # ⟨column:121@0131304(ktype:5)|t:3|cL:18|bb:15⟩

	# - (G) - upper - [9:15] ~ 0002.0003.0011.0012.0021.0030.0034.0101.0110.0111.0120.1001.1002.1010.1220
	# - dead(0:elt:z) - # ⟨column:29@0002003(ktype:7)|t:6|cL:36|bb:15⟩
	# - .1:elt:z. - # ⟨column:32@0002102(ktype:7)|t:6|cL:36|bb:15⟩
	# - dead(0:elt:z) - # ⟨column:41@0002504(ktype:7)|t:3|cL:18|bb:15⟩
	# - (G) - lower - [17:15] ~ 0014.0224.0232.0233.1114.1123.1124.1133.1200.1204.1213.1222.1223.1231.1232
	# ec('0014002') # ⟨column:65@0014002(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0014101') # ⟨column:68@0014101(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0014200') # ⟨column:71@0014200(ktype:5)|t:3|cL:18|bb:15⟩
														
	# - (H) - upper - [6:26] ~ 0002.0003.0011.0012.0020.0021.0024.0030.0033.0101.0102.0103.0110.0111.0120.0124.0133.0230.1001.1003.1010.1011.1020.1130.1202.1211
	# ec('0002002') # ⟨column:26@0002002(ktype:3)|t:6|cL:36|bb:26⟩
	# - dead(0:elt:z) - # ⟨column:30@0002101(ktype:3)|t:6|cL:36|bb:26⟩
	# - dead(1:elt:z) - # ⟨column:33@0002200(ktype:3)|t:6|cL:36|bb:26⟩
	# ec('0002404') # ⟨column:37@0002404(ktype:3)|t:6|cL:36|bb:26⟩
	# ec('0002503') # ⟨column:39@0002503(ktype:3)|t:6|cL:36|bb:26⟩
	# - (H) - lower - [19:26] ~ 0023.0032.0104.0214.0223.0224.0231.0233.1004.1101.1110.1114.1123.1124.1131.1132.1133.1201.1204.1210.1213.1214.1222.1223.1231.1232
	# - dead(0:elt:a) - # ⟨column:73@0023002(ktype:5)|t:6|cL:36|bb:26⟩
	# ec('0023101') # ⟨column:75@0023101(ktype:5)|t:6|cL:36|bb:26⟩
	# ec('0023200') # ⟨column:77@0023200(ktype:5)|t:6|cL:36|bb:26⟩
	# ec('0023404') # ⟨column:79@0023404(ktype:5)|t:6|cL:36|bb:26⟩
	# ec('0023503') # ⟨column:81@0023503(ktype:5)|t:6|cL:36|bb:26⟩
		
	# - (J) - upper - [7:27] ~ 0002.0003.0030.0033.0120.0121.0122.0123.0124.0212.0213.1001.1003.1010.1011.1012.1013.1014.1030.1032.1102.1103.1120.1121.1122.1130.1211
	# ec('0002001') # ⟨column:27@0002001(ktype:4)|t:6|cL:36|bb:27⟩
	# - dead(3:green:z) - # ⟨column:31@0002100(ktype:4)|t:6|cL:36|bb:27⟩
	# ec('0002304') # ⟨column:35@0002304(ktype:4)|t:6|cL:36|bb:27⟩
	# ec('0002403') # ⟨column:38@0002403(ktype:4)|t:6|cL:36|bb:27⟩
	# ec('0002502') # ⟨column:40@0002502(ktype:4)|t:6|cL:36|bb:27⟩
	# - (J) - lower - [18:27] ~ 0023.0104.0112.0113.0114.0131.0132.0202.0204.0220.0221.0222.0223.0224.0231.0233.1021.1022.1110.1111.1112.1113.1114.1201.1204.1231.1232
	# ec('0023003') # ⟨column:72@0023003(ktype:4)|t:6|cL:36|bb:27⟩
	# ec('0023102') # ⟨column:74@0023102(ktype:4)|t:6|cL:36|bb:27⟩
	# ec('0023201') # ⟨column:76@0023201(ktype:4)|t:6|cL:36|bb:27⟩
	# ec('0023300') # ⟨column:78@0023300(ktype:4)|t:6|cL:36|bb:27⟩
	# ec('0023504') # ⟨column:80@0023504(ktype:4)|t:6|cL:36|bb:27⟩
		
	# - (K) - upper - [10:15] ~ 0010.0011.0012.0013.0014.0021.0022.0100.0101.0110.0111.0200.0201.0232.1200
	# - dead(0:elt:a) - # ⟨column:42@0010005(ktype:2)|t:6|cL:36|bb:15⟩
	# - .1:elt:a. - # ⟨column:46@0010104(ktype:2)|t:6|cL:36|bb:15⟩
	# - dead(0:elt:a) - # ⟨column:53@0010401(ktype:2)|t:3|cL:18|bb:15⟩
	# - (K) - lower - [25:15] ~ 0034.1002.1033.1034.1123.1124.1133.1134.1212.1213.1220.1221.1222.1223.1224
	# ec('0034003') # ⟨column:107@0034003(ktype:6)|t:6|cL:36|bb:15⟩
	# ec('0034201') # ⟨column:108@0034201(ktype:6)|t:6|cL:36|bb:15⟩
	# ec('0034300') # ⟨column:109@0034300(ktype:6)|t:3|cL:18|bb:15⟩
		
	# - (L) - upper - [11:15] ~ 0010.0013.0022.0100.0130.0131.0200.0201.0202.0203.0204.0220.1022.1023.1113
	# ec('0010002') # ⟨column:43@0010002(ktype:4)|t:3|cL:18|bb:15⟩
	# - dead(ex:z) - # ⟨column:47@0010101(ktype:4)|t:6|cL:36|bb:15⟩
	# - dead(ex:b) - # ⟨column:49@0010200(ktype:4)|t:6|cL:36|bb:15⟩
	# - (L) - lower - [27:15] ~ 0121.0211.0212.1014.1030.1031.1032.1033.1034.1103.1104.1134.1212.1221.1224
	# ec('0121001') # ⟨column:113@0121001(ktype:6)|t:3|cL:18|bb:15⟩
	# ec('0121100') # ⟨column:114@0121100(ktype:6)|t:6|cL:36|bb:15⟩
	# ec('0121304') # ⟨column:115@0121304(ktype:6)|t:6|cL:36|bb:15⟩
		
	# - (M) - upper - [12:27] ~ 0010.0013.0022.0023.0100.0104.0113.0122.0131.0200.0201.0202.0204.0213.0220.0222.0223.0231.1013.1022.1102.1110.1111.1113.1120.1122.1201
	# ec('0010001') # ⟨column:44@0010001(ktype:5)|t:6|cL:36|bb:27⟩
	# - dead(3:green:a) - # ⟨column:48@0010100(ktype:5)|t:6|cL:36|bb:27⟩
	# ec('0010304') # ⟨column:51@0010304(ktype:5)|t:6|cL:36|bb:27⟩
	# ec('0010403') # ⟨column:54@0010403(ktype:5)|t:6|cL:36|bb:27⟩
	# ec('0010502') # ⟨column:56@0010502(ktype:5)|t:6|cL:36|bb:27⟩
	# - (M) - lower - [24:27] ~ 0033.0112.0114.0121.0123.0124.0132.0212.0221.1003.1011.1012.1014.1021.1030.1032.1033.1034.1103.1112.1121.1130.1134.1211.1212.1221.1224
	# ec('0033003') # ⟨column:102@0033003(ktype:7)|t:6|cL:36|bb:27⟩
	# ec('0033102') # ⟨column:103@0033102(ktype:7)|t:6|cL:36|bb:27⟩
	# ec('0033201') # ⟨column:104@0033201(ktype:7)|t:6|cL:36|bb:27⟩
	# ec('0033300') # ⟨column:105@0033300(ktype:7)|t:6|cL:36|bb:27⟩
	# ec('0033504') # ⟨column:106@0033504(ktype:7)|t:6|cL:36|bb:27⟩
		
	# - (N) - upper - [13:26] ~ 0010.0011.0012.0013.0020.0021.0022.0023.0024.0100.0101.0102.0103.0104.0110.0111.0133.0200.0201.0223.0230.0231.1020.1110.1201.1202
	# - dead(1:elt:a) - # ⟨column:45@0010000(ktype:6)|t:6|cL:36|bb:26⟩
	# - dead(0:elt:a) - # ⟨column:50@0010204(ktype:6)|t:6|cL:36|bb:26⟩
	# ec('0010303') # ⟨column:52@0010303(ktype:6)|t:6|cL:36|bb:26⟩
	# ec('0010402') # ⟨column:55@0010402(ktype:6)|t:6|cL:36|bb:26⟩
	# ec('0010501') # ⟨column:57@0010501(ktype:6)|t:6|cL:36|bb:26⟩
	# - (N) - lower - [23:26] ~ 0032.0033.0124.0214.1003.1004.1011.1033.1034.1101.1123.1124.1130.1131.1132.1133.1134.1210.1211.1212.1213.1214.1221.1222.1223.1224
	# ec('0032000') # ⟨column:97@0032000(ktype:6)|t:6|cL:36|bb:26⟩
	# - dead(0:elt:z) - # ⟨column:98@0032204(ktype:6)|t:6|cL:36|bb:26⟩
	# ec('0032303') # ⟨column:99@0032303(ktype:6)|t:6|cL:36|bb:26⟩
	# ec('0032402') # ⟨column:100@0032402(ktype:6)|t:6|cL:36|bb:26⟩
	# ec('0032501') # ⟨column:101@0032501(ktype:6)|t:6|cL:36|bb:26⟩
		
	# - (P₁) - upper - [14:15] ~ 0011.0012.0021.0101.0110.0111.0112.0113.0114.0132.0221.0222.1021.1111.1112
	# ec('0011001') # ⟨column:58@0011001(ktype:4)|t:6|cL:36|bb:15⟩
	# - dead(1:elt:z) - # ⟨column:60@0011100(ktype:4)|t:6|cL:36|bb:15⟩
	# ec('0011502') # ⟨column:63@0011502(ktype:4)|t:3|cL:18|bb:15⟩
	# - (P₁) - lower - [28:15] ~ 0122.0123.0213.1012.1013.1102.1120.1121.1122.1123.1124.1133.1213.1222.1223
	# ec('0122000') # ⟨column:116@0122000(ktype:6)|t:6|cL:36|bb:15⟩
	# ec('0122204') # ⟨column:117@0122204(ktype:6)|t:6|cL:36|bb:15⟩
	# ec('0122501') # ⟨column:118@0122501(ktype:6)|t:3|cL:18|bb:15⟩

	# - (P₂) - upper - [15:15] ~ 0011.0012.0021.0101.0110.0111.0112.0114.0123.0132.0221.1012.1021.1112.1121
	# - dead(1:elt:a) - # ⟨column:59@0011000(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0011204') # ⟨column:61@0011204(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0011303') # ⟨column:62@0011303(ktype:5)|t:3|cL:18|bb:15⟩
	# - (P₂) - lower - [26:15] ~ 0113.0122.0213.0222.1013.1102.1111.1120.1122.1123.1124.1133.1213.1222.1223
	# ec('0113002') # ⟨column:110@0113002(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0113101') # ⟨column:111@0113101(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0113200') # ⟨column:112@0113200(ktype:5)|t:3|cL:18|bb:15⟩
	
	# ---------------------------- #
	
	print(f"avcolumns: {len([col for col in diagram.columns if col.isAvailabled()])}")			
	for col in avcolumns:
		if not col.isAvailabled():
			print(f'not av: {col}')			
	avcolumns = [col for col in diagram.columns if col.isAvailabled()]
	
	# ex:a[0-5]
	for i,node in enumerate(diagram.bases):
		extend(node.address)
		print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
		for col in avcolumns:
			if not col.isAvailabled():
				print(f'not av: {col}')		
		diagram.collapseBack(node.loop)

	# ex:z[0-5]
	# diagram.pointers = diagram.bases
	# adv(5); jmp(5); adv(5)
	# for node in diagram.pointers:
	# 	extend(node.address)
	# 	print(f"avcolumns: {len([col for col in avcolumns if col.isAvailabled()])}")		
	# 	for col in avcolumns:
	# 		if not col.isAvailabled():
	# 			print(f'not av: {col}')		
	# 	diagram.collapseBack(node.loop)					
	
	''' ec('0001404') # (D₁) ⟨column:19@0001404(ktype:4)|t:6|cL:36|bb:27⟩ # [~]
	[elt] ⇒ extended 36 ktype:4 loops for parent ⟨loop:[blue:10]:0001407|⟩
	avcolumns: 73
	not av: ⟨column:19@0001404(ktype:4)|t:6|cL:36|bb:27⟩
	not av: ⟨column:35@0002304(ktype:4)|t:6|cL:36|bb:27⟩
	not av: ⟨column:99@0032303(ktype:6)|t:6|cL:36|bb:26⟩
	not av: ⟨column:100@0032402(ktype:6)|t:6|cL:36|bb:26⟩
	not av: ⟨column:103@0033102(ktype:7)|t:6|cL:36|bb:27⟩
	not av: ⟨column:107@0034003(ktype:6)|t:6|cL:36|bb:15⟩
	not av: ⟨column:108@0034201(ktype:6)|t:6|cL:36|bb:15⟩
	not av: ⟨column:115@0121304(ktype:6)|t:6|cL:36|bb:15⟩
	not av: ⟨column:117@0122204(ktype:6)|t:6|cL:36|bb:15⟩
	[ex] ⇒ extended 0000001…
	avcolumns: 72
	not av: ⟨column:112@0113200(ktype:5)|t:3|cL:18|bb:15⟩	
	'''		
	''' ec('0001001') # (D₂) ⟨column:8@0001001(ktype:5)|t:6|cL:36|bb:27⟩ # [~]
	[elt] ⇒ extended 36 ktype:5 loops for parent ⟨loop:[blue:6]:0001007|⟩
	avcolumns: 73
	not av: ⟨column:8@0001001(ktype:5)|t:6|cL:36|bb:27⟩
	not av: ⟨column:44@0010001(ktype:5)|t:6|cL:36|bb:27⟩
	not av: ⟨column:65@0014002(ktype:5)|t:6|cL:36|bb:15⟩
	not av: ⟨column:68@0014101(ktype:5)|t:6|cL:36|bb:15⟩
	not av: ⟨column:72@0023003(ktype:4)|t:6|cL:36|bb:27⟩
	not av: ⟨column:79@0023404(ktype:5)|t:6|cL:36|bb:26⟩
	not av: ⟨column:81@0023503(ktype:5)|t:6|cL:36|bb:26⟩
	not av: ⟨column:110@0113002(ktype:5)|t:6|cL:36|bb:15⟩
	not av: ⟨column:119@0131001(ktype:5)|t:6|cL:36|bb:15⟩
	[ex] ⇒ extended 0000001… 
	avcolumns: 72
	not av: ⟨column:19@0001404(ktype:4)|t:6|cL:36|bb:27⟩
	'''
				
	# ---------------------------- #	
	# diagram.point()
	# show(diagram)
