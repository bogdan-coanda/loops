from diagram import *
from uicanvas import *
from common import *
from mx import *


max_lvl_reached = 0


def leap(lvl=0, path=[]):
	global max_lvl_reached
	
	def key():
		return f"[{tstr(time() - startTime):>11}][lvl:{lvl}]" 
	
	print(f"{key()} {'.'.join([(str(x)+upper(t)) for x,t,_ in path])}")
	
	# basic check
	min_chlen = min([len(chain.avnodes) for chain in diagram.chains])
	if min_chlen == 0:
		return
		
	# save
	if lvl >= max_lvl_reached:
		with open('8b-leaps_reached', 'a', encoding="utf8") as log:
			if lvl > max_lvl_reached:
				log.write("-------------------------" + "\n\n")
			log.write(f"{key()} {'.'.join([(str(x)+upper(t)) for x,t,_ in path])}" + "\n")
			log.write(f"columns: {' '.join([c for _,_,c in path])}" + "\n\n")
			max_lvl_reached = lvl
		
	# purge
		
	unavailed = []
	avcolumns = []
	
	for ic, column in enumerate(diagram.columns):
		if column.isAvailabled():
			
			extended = []
			for tuple in column.tuples:
				for loop in tuple:
					if diagram.extendLoop(loop):
						extended.append(loop)
					else:
						break
				if len(extended) % (diagram.spClass - 2) != 0:
					break
					
			if len(extended) != len(column.tuples) * (diagram.spClass - 2) or len([ch for ch in diagram.chains if len(ch.avnodes) == 0]) > 0:
				unavailed.append(column)
				column.unavailabled = True
			else:
				avcolumns.append(column)						
						
			for loop in reversed(extended):
				diagram.collapseBack(loop)					
	
	# for each remaining
	
	avcolumns = sorted(avcolumns, key = lambda c: c.firstNode)
	print(f"{key()} avcolumns: {len(avcolumns)}")
	for ic, column in enumerate(avcolumns):
				
		extended = []
		for tuple in column.tuples:
			for loop in tuple:
				if diagram.extendLoop(loop):
					extended.append(loop)
				else:
					break
			if len(extended) % (diagram.spClass - 2) != 0:
				break
				
		assert len(extended) == len(column.tuples) * (diagram.spClass - 2)
			
		print(f"{key()} extended: {column}")
		leap(lvl+1, path+[(ic, len(avcolumns), column.firstNode.address)])
					
		for loop in reversed(extended):
			diagram.collapseBack(loop)							
		
		unavailed.append(column)
		column.unavailabled = True
		
	for column in unavailed:
		column.unavailabled = False
	
	
	
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

	# ---------------------------- #

	startTime = time()
	leap()

	# ============================ #
	
	elt('0001007', 5)
	elt('0001207', 3)
	elt('0010007', 6)
	elt('0010207', 4)
	elt('0002207', 7)
	elt('0002107', 5)
	elt('0002307', 4)
	elt('0002407', 4)
	elt('0011007', 4)
									
	print(f"avcolumns: {len([col for col in diagram.columns if col.isAvailabled()])}")
	
	unavailed = 0
	for column in diagram.columns:
		if column.isAvailabled():
			
			extended = []
			for tuple in column.tuples:
				for loop in tuple:
					if diagram.extendLoop(loop):
						extended.append(loop)
					else:
						break
				if len(extended) % (diagram.spClass - 2) != 0:
					break
					
			if len(extended) != len(column.tuples) * (diagram.spClass - 2):
				print(f"broken column | extended: {len(extended)} / {len(column.tuples) * (diagram.spClass - 2)}")
				unavailed += 1
				column.unavailabled = True
				
			for loop in reversed(extended):
				diagram.collapseBack(loop)				
			
	print(f"unavailed: {unavailed} | remaining avcolumns: {len([col for col in diagram.columns if col.isAvailabled()])}")
				
	# ---------------------------- #
	
	diagram.point()
	show(diagram)	

