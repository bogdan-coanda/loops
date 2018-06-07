import ui
from diagram import *
from colorsys import hls_to_rgb
from random import random
from uicanvas import *
from itertools import chain


if __name__ == "__main__":
	
	diagram = Diagram(6)
	
	diagram.W = 2400
	diagram.H = 1600
	
	DM = 64 if diagram.spClass is not 9 else 10	
	RH = 8 if diagram.spClass is not 9 else 3
						
	def moveCycle(cycle, d, α, β, skipActualMove=False, bx=diagram.W/2, by=diagram.H/2, avg=(0,0), weight=1):
		cycle.moved = True
		if skipActualMove:
			return
		X = math.floor(d*DM*math.cos(α * 2*math.pi))
		Y = math.floor(d*DM*math.sin(α * 2*math.pi))		
		cycle.px = (bx + X + avg[0]) / weight
		cycle.py = (by + Y + avg[1]) / weight
		for node in cycle.nodes:
			qLast = int(node.address[-1])
			dx = math.floor(RH*math.cos((2*qLast - (diagram.spClass-1) +β ) * math.pi / diagram.spClass))
			dy = math.floor(RH*math.sin((2*qLast - (diagram.spClass-1) +β ) * math.pi / diagram.spClass))
			node.px = cycle.px + dx
			node.py = cycle.py + dy
		
	def showLinks(node):
		for n in node.loop.nodes:
			n.showLinksOfTypes.append(2)
			m = n.links[2].next
			for _ in range(diagram.spClass - 1):
				m.showLinksOfTypes.append(1)
				m = m.links[1].next
									
																					
	def isStar5Availabled(node):
		for nln in node.loop.nodes:
			if nln.cycle.moved:
				return False
			curr = nln.links[1].next	
			if curr.loopBrethren[0].cycle.moved:
				return False
			if curr.loopBrethren[1].cycle.moved:
				return False
			if curr.loopBrethren[2].cycle.moved:
				return False
		return True
							
	#move nodes away from canvas center	
	for n in diagram.nodes:
		n.px /= 4
		n.py /= 4
		
	
	# place starter in center
	
	'''
	# 5by6 [~][!]
	node = diagram.nodeByAddress['00005']
	#diagram.extendLoop(node.loop)
	showLinks(node)
	for i,nln in enumerate(node.loop.nodes):
		moveCycle(nln.cycle, 1, i/5, 1+i*12/5)#, True)
		curr = nln.links[1].next
		showLinks(curr)	
		moveCycle(curr.loopBrethren[0].cycle, 2, (i*4+1)/20, 0)#, True)
		moveCycle(curr.loopBrethren[1].cycle, 3, (i*4+2)/20, 0)#, True)
		moveCycle(curr.loopBrethren[2].cycle, 2, (i*4+3)/20, 0)#, True)
		
	#'''				
	''' # [!] search… failed
	
	pp = 0
	
	def mk(lvl=0, path=""):
		global pp
		
		if lvl >= 5:
			show(diagram)
			diagram.measure()
			input()
		
		if lvl is 6:
			return True
				
		cc = 0
		for node in diagram.nodes:
			alt = path+" "+str(cc)+"/"+str(len(diagram.nodes))
			if pp % 100000 == 0:
				print("["+str(lvl)+"] " + alt + " | testing " + str(node))
			pp += 1
			if isStar5Availabled(node):
				#print("["+str(lvl)+"] starring " + str(node))				
				# place starter in center
				#diagram.extendLoop(node.loop)
				#showLinks(node)
				for i,nln in enumerate(node.loop.nodes):
					moveCycle(nln.cycle, 1, i/5, 1+i*12/5, True)
					curr = nln.links[1].next
					#showLinks(curr)	
					moveCycle(curr.loopBrethren[0].cycle, 2, (i*4+1)/20, 0, True)
					moveCycle(curr.loopBrethren[1].cycle, 3, (i*4+2)/20, 0, True)
					moveCycle(curr.loopBrethren[2].cycle, 2, (i*4+3)/20, 0, True)
					
				if mk(lvl+1, alt):
					return True
				
				#diagram.collapseLoop(node.loop)
				for i,nln in enumerate(node.loop.nodes):
					nln.cycle.moved = False
					curr = nln.links[1].next
					curr.loopBrethren[0].cycle.moved = False
					curr.loopBrethren[1].cycle.moved = False
					curr.loopBrethren[2].cycle.moved = False
			cc += 1									
	mk()			
			
											
	#''' 
	# 6by5 [~][!]
	
	# place starter in center
	node = diagram.nodeByAddress['00000']
	moveCycle(node.cycle, 0, 0, 1)
	
	# center violet
	showLinks(node)
		
	moveCycle(node.loopBrethren[0].cycle, 9, 9/12, 7)
	moveCycle(node.loopBrethren[1].cycle, 3, 5/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)			
	# :: topleft-green.bro[0]
	#moveCycle(node.loopBrethren[2].cycle, 3, 5/12, 1, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)	
									
	# center red	
	node = node.links[1].next
	showLinks(node)

	moveCycle(node.loopBrethren[0].cycle, 9, 11/12, 7)
	moveCycle(node.loopBrethren[1].cycle, 3, 	7/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	# :: top-blue.bro[0]
	#moveCycle(node.loopBrethren[2].cycle, 3, 	7/12, 0, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
	
	# center orange
	node = node.links[1].next				
	showLinks(node)

	moveCycle(node.loopBrethren[0].cycle, 9, 1/12, 	7)
	moveCycle(node.loopBrethren[1].cycle, 3, 9/12,	1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	# :: topleft-violet.bro[0]
	#moveCycle(node.loopBrethren[2].cycle, 3, 9/12, -1, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)

	# center yellow	
	node = node.links[1].next				
	showLinks(node)

	moveCycle(node.loopBrethren[0].cycle, 9,	3/12,  7)
	moveCycle(node.loopBrethren[1].cycle, 3, 11/12,	-1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	# :: botleft-red.bro[0]
	moveCycle(node.loopBrethren[2].cycle, 3, 11/12, -1, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
			
	# center green
	node = node.links[1].next				
	showLinks(node)

	moveCycle(node.loopBrethren[0].cycle, 9, 5/12, 	 5)
	moveCycle(node.loopBrethren[1].cycle, 3, 1/12,	-1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	# :: bot-orange.bro[0]
	#moveCycle(node.loopBrethren[2].cycle, 3, 1/12, -1, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
		
	# center blue
	node = node.links[1].next				
	showLinks(node)

	moveCycle(node.loopBrethren[0].cycle, 9, 7/12,	9)
	moveCycle(node.loopBrethren[1].cycle, 3, 3/12, -7, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	# :: botright-yellow.bro[0]
	moveCycle(node.loopBrethren[2].cycle, 3, 3/12, -5, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)

	# back on '00000'
	node = node.links[1].next																	
	
	# top orange
	node = node.links[2].next
	showLinks(node)
	
	moveCycle(node.loopBrethren[0].cycle, 3, 7/12, 11, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 3/12, -3, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 3/12, -7, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)	
	
	# top yellow
	node = node.links[1].next
	showLinks(node)
	
	moveCycle(node.loopBrethren[0].cycle, 3, 9/12,  1, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 5/12, -5, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 5/12, -7, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
		
	# top green
	node = node.links[1].next
	showLinks(node)
	
	moveCycle(node.loopBrethren[0].cycle, 3, 11/12, 11, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1,  7/12, -5, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1,  7/12, -7, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
	
	# top blue
	node = node.links[1].next
	showLinks(node)
	
	moveCycle(node.loopBrethren[0].cycle, 3, 1/12, 3, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 9/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 9/12, 1, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)			
	
	# back on '00001'
	node = diagram.nodeByAddress['00001']
		
	# topleft yellow
	node = node.links[2].next
	showLinks(node)
	
	moveCycle(node.loopBrethren[0].cycle, 3, 9/12,  1, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 5/12, -5, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 5/12, -7, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
	
	# topleft green
	node = node.links[1].next
	showLinks(node)
	
	moveCycle(node.loopBrethren[0].cycle, 3, 11/12, 11, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1,  7/12, -5, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1,  7/12, -7, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		

	# topleft blue
	node = node.links[1].next
	showLinks(node)
	
	moveCycle(node.loopBrethren[0].cycle, 3, 1/12, 3, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 9/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 9/12, 1, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
	
	# topleft violet
	node = node.links[1].next
	showLinks(node)
	
	avg1 = (node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
	moveCycle(node.loopBrethren[0].cycle, 3,  3/12, 11, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 11/12, -3, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 11/12, -5, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
	
	# move to average
	node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py = avg1
	moveCycle(node.loopBrethren[1].cycle, 1, 11/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py, avg1, 2)		
	
	# back on '00002'
	node = diagram.nodeByAddress['00002']
		
	# botleft green
	node = node.links[2].next
	showLinks(node)
	
	moveCycle(node.loopBrethren[0].cycle, 3, 11/12, 11, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1,  7/12, -5, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1,  7/12, -7, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
	
	# botleft blue
	node = node.links[1].next
	showLinks(node)
	
	moveCycle(node.loopBrethren[0].cycle, 3, 1/12, 3, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 9/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 9/12, 1, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
	
	# botleft violet
	node = node.links[1].next
	showLinks(node)
	
	avg0 = (node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	avg1 = (node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
	moveCycle(node.loopBrethren[0].cycle, 3,  3/12,  7, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 11/12, 11, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 11/12,  7, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
	
	# move to average between top-yellow.bro[2] and botleft-violet.bro[1]
	node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py = avg1
	moveCycle(node.loopBrethren[1].cycle, 1, 11/12, 11, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py, avg1, 2)
	
	# move to average between top-orange.bro[0] and botleft-violet.bro[0]
	node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py = avg0
	moveCycle(node.loopBrethren[0].cycle, 3,  3/12,  7, False, node.cycle.px, node.cycle.py, avg0, 2)	
	
	# botleft red
	node = node.links[1].next
	showLinks(node)
	
	avg1 = (node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
	moveCycle(node.loopBrethren[0].cycle, 3, 5/12, 11, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 1/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 1/12, -5, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
	
	# move to average
	node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py = avg1
	moveCycle(node.loopBrethren[1].cycle, 1, 1/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py, avg1, 2)		
	
	# back on '00003'
	node = diagram.nodeByAddress['00003']
		
	# bot blue
	node = node.links[2].next
	showLinks(node)
	
	moveCycle(node.loopBrethren[0].cycle, 3, 1/12, 3, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 9/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 9/12, 1, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
	
	# bot violet
	node = node.links[1].next
	showLinks(node)
	
	avg0 = (node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[0].cycle, 3,  3/12, 1, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 11/12, 9, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 11/12, 7, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		

	# move to average between top-yellow.bro[0] and bot-violet.bro[0]
	node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py = avg0
	moveCycle(node.loopBrethren[0].cycle, 3, 3/12, 6, False, node.cycle.px, node.cycle.py, avg0, 2)																						
	
	# bot red
	node = node.links[1].next
	showLinks(node)
	
	avg0 = (node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	avg1 = (node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
	moveCycle(node.loopBrethren[0].cycle, 3, 5/12, 1, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 1/12, 9, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 1/12, 7, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
	
	# move to average between topleft-green.bro[2] and bot-red.bro[1]
	node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py = avg1
	moveCycle(node.loopBrethren[1].cycle, 1, 1/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py, avg1, 2)

	# move to average between topleft-yellow.bro[0] and bot-red.bro[0]
	node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py = avg0
	moveCycle(node.loopBrethren[0].cycle, 3, 5/12, 7, False, node.cycle.px, node.cycle.py, avg0, 2)			
		
	# bot orange
	node = node.links[1].next
	showLinks(node)

	avg1 = (node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
	moveCycle(node.loopBrethren[0].cycle, 3, 7/12, 1, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 3/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 3/12, 5, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
	
	# move to average
	node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py = avg1
	moveCycle(node.loopBrethren[1].cycle, 1, 3/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py, avg1, 2)					
	
	# back on '00004'
	node = diagram.nodeByAddress['00004']
		
	# botright violet
	node = node.links[2].next
	showLinks(node)
	
	avg0 = (node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[0].cycle, 3,  3/12, 11, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 11/12,  7, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 11/12,  5, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
	
	# move to average between botright-violet.bro[0] and top-green.bro[0]
	node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py = avg0
	moveCycle(node.loopBrethren[0].cycle, 3,  3/12, 5, False, node.cycle.px, node.cycle.py, avg0, 2)	
	
	# botright red
	node = node.links[1].next
	showLinks(node)
	
	avg0 = (node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	avg2 = (node.loopBrethren[2].cycle.px, node.loopBrethren[2].cycle.py)	
	moveCycle(node.loopBrethren[0].cycle, 3, 5/12, 11, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 1/12,  7, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 1/12,  3, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
	
	# move to average between botright-red.bro[2] and top-green.bro[1]
	node.loopBrethren[2].cycle.px, node.loopBrethren[2].cycle.py = avg2
	moveCycle(node.loopBrethren[2].cycle, 1, 1/12, 11, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py, avg2, 2)			
	
	# move to average between botright-red.bro[0] and topleft-green.bro[0]
	node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py = avg0
	moveCycle(node.loopBrethren[0].cycle, 3, 5/12, 4, False, node.cycle.px, node.cycle.py, avg0, 2)	
	
	# botright orange
	node = node.links[1].next
	showLinks(node)
	
	avg0 = (node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	avg1 = (node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
	moveCycle(node.loopBrethren[0].cycle, 3, 7/12, 5, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 3/12, 9, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 3/12, 3, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
	
	# move to average between botright-orange.bro[1] and botleft-blue.bro[2]
	node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py = avg1
	moveCycle(node.loopBrethren[1].cycle, 1, 3/12, 9, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py, avg1, 2)	
	
	# move to average between botleft-green.bro[0] and botright-orange.bro[0]
	node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py = avg0
	moveCycle(node.loopBrethren[0].cycle, 3, 7/12, 5, False, node.cycle.px, node.cycle.py, avg0, 2)	
	
	# botright yellow
	node = node.links[1].next
	showLinks(node)
	
	moveCycle(node.loopBrethren[0].cycle, 3, 9/12, 9, False, node.cycle.px, node.cycle.py)
	avg = (node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 5/12, 9, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 5/12, 3, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
	
	# move to average
	node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py = avg
	moveCycle(node.loopBrethren[1].cycle, 1, 5/12, 9, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py, avg, 2)																						
		
	# back on '00005'
	node = diagram.nodeByAddress['00005']
		
	# topright red
	node = node.links[2].next
	showLinks(node)
	
	avg0 = (node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	avg2 = (node.loopBrethren[2].cycle.px, node.loopBrethren[2].cycle.py)
	moveCycle(node.loopBrethren[0].cycle, 3, 5/12,  3, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 1/12, 11, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 1/12,  5, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		

	# move to average between top-blue.bro[1] and topright-red.bro[2]
	node.loopBrethren[2].cycle.px, node.loopBrethren[2].cycle.py = avg2
	moveCycle(node.loopBrethren[2].cycle, 1, 1/12,  5, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py, avg2, 2)																						
		
	# move to average between topright-red.bro[0] and topleft-blue.bro[0]
	node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py = avg0
	moveCycle(node.loopBrethren[0].cycle, 3, 5/12,  9, False, node.cycle.px, node.cycle.py, avg0, 2)	
			
	# topright orange
	node = node.links[1].next
	showLinks(node)
	
	avg0 = (node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	avg2 = (node.loopBrethren[2].cycle.px, node.loopBrethren[2].cycle.py)
	moveCycle(node.loopBrethren[0].cycle, 3, 7/12,  3, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 3/12, 11, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 3/12,  9, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		
	
	# move to average between top-blue.bro[1] and topright-red.bro[2]
	node.loopBrethren[2].cycle.px, node.loopBrethren[2].cycle.py = avg2
	moveCycle(node.loopBrethren[2].cycle, 1, 3/12, 5, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py, avg2, 2)																						
		
	# move to average between topright-orange.bro[0] and botleft-blue.bro[0]
	node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py = avg0
	moveCycle(node.loopBrethren[0].cycle, 3, 7/12,  8, False, node.cycle.px, node.cycle.py, avg0, 2)		
	
	# topright yellow
	node = node.links[1].next
	showLinks(node)
	
	avg0 = (node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	avg1 = (node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
	moveCycle(node.loopBrethren[0].cycle, 3, 9/12,  3, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1, 5/12, 11, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1, 5/12,  7, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)		

	# move to average between topright-yellow.bro[1] and bot-violet.bro[2]
	node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py = avg1
	moveCycle(node.loopBrethren[1].cycle, 1, 5/12,  3, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py, avg1, 2)	
	
	# move to average between bot-blue.bro[0] and topright-yellow.bro[0]
	node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py = avg0
	moveCycle(node.loopBrethren[0].cycle, 3, 9/12,  9, False, node.cycle.px, node.cycle.py, avg0, 2)	
	
	# topright green
	node = node.links[1].next
	showLinks(node)

	avg0 = (node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)	
	moveCycle(node.loopBrethren[0].cycle, 3, 11/12, 3, False, node.cycle.px, node.cycle.py)
	moveCycle(node.loopBrethren[1].cycle, 1,  7/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py)
	moveCycle(node.loopBrethren[2].cycle, 1,  7/12, 7, False, node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py)
	
	# move to average between topright-green.bro[1] and botright-violet.bro[2]
	node.loopBrethren[1].cycle.px, node.loopBrethren[1].cycle.py = avg0
	moveCycle(node.loopBrethren[1].cycle, 1,  7/12, 1, False, node.loopBrethren[0].cycle.px, node.loopBrethren[0].cycle.py, avg0, 2)																						
		
	#'''	
	
	show(diagram)
	diagram.measure()

