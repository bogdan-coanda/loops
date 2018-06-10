import ui
from diagram import *
from colorsys import hls_to_rgb
from random import random
from uicanvas import *
from itertools import chain


if __name__ == "__main__":
	
	diagram = Diagram(6)
	
	diagram.W = 1800
	diagram.H = 1200
	
	DM = 64 if diagram.spClass is not 9 else 10	
	RH = 8 if diagram.spClass is not 9 else 3
						
	def moveCycle(cycle, d, α, β, skipActualMove=False, bx=diagram.W/2, by=diagram.H/2, avg=(0,0), weight=1):
		if cycle.moved:
			return # [~]
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
								
	#move nodes away from canvas center	
	for n in diagram.nodes:
		n.px /= 4
		n.py /= 4
		
	
	# place starter in center	
	# 5by6 [~][!]
	node = diagram.nodeByAddress['00005']
	
	'''	
	for w in diagram.nodes:
		if w.cycle in chain(*[[nln.cycle for nln in n.links[1].next.loop.nodes] for n in node.loop.nodes]):
			w.px = w.px*4 + 200
			w.py = w.py*4 + 100
	'''		
	
	
	
	diagram.extendLoop(node.loop)
	
	#showLinks(node)	
	
	for i,nln in enumerate(node.loop.nodes):
		moveCycle(nln.cycle, 2, i/5, 2+i*12/5+5+6)#, True)		
		curr = nln#.prevs[1].node
		for j in range(1):#diagram.spClass-2):
			curr = curr.prevs[1].node
			showLinks(curr)	
			moveCycle(curr.loopBrethren[0].cycle, 3, i/5-3/20+j/20, 0)
			moveCycle(curr.loopBrethren[1].cycle, 4, i/5-3/20+j/20, 0)
			moveCycle(curr.loopBrethren[2].cycle, 5, i/5-3/20+j/20, 0)
			moveCycle(curr.loopBrethren[3].cycle, 6, i/5-3/20+j/20, 0)
	#'''
	'''
	kn = node.links[1].next.links[1].next.links[1].next.links[1].next
	showLinks(kn)
	for i, bro in enumerate(kn.loopBrethren):
		moveCycle(bro.cycle, 2+i, -3/20, 0)

	kn = kn.prevs[1].node
	showLinks(kn)
	for i, bro in enumerate(kn.loopBrethren):
		moveCycle(bro.cycle, 2+i, -2/20, 0)				
		
	kn = kn.prevs[1].node
	showLinks(kn)
	for i, bro in enumerate(kn.loopBrethren):
		moveCycle(bro.cycle, 2+i, -1/20, 0)			
		
	moveCycle(node.links[1].next.loopBrethren[0].cycle, 2, 0/5, 0)
								
	#'''				
	show(diagram)
	diagram.measure()
