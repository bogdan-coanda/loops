import ui
from diagram import *
from colorsys import hls_to_rgb
from random import random
from enum import Enum
from itertools import chain


class colors (object):
	blue 				= '#08f'

	green 			= '#0d0'
	lightgreen 	= '#bfb'
	
	yellow			= '#ff0'
	lightyellow	= '#ffb'
	
	orange			= '#f90'
	lightorange	= '#feb'
	
	red					= '#f00'
	lightred		= '#fdd'
	
	violet			= '#f0f'
	lightviolet	= '#fdf'
	
	indigo			= '#808'
	lightindigo	= '#ece'
	
	def normal(index):
		if index is 0:
			return colors.blue
		elif index is 1:
			return colors.green
		elif index is 2:
			return colors.yellow
		elif index is 3:
			return colors.orange			
		elif index is 4:
			return colors.red	
		elif index is 5:
			return colors.violet
		elif index is 6:
			return colors.indigo
		else:
			return 'black'
			
	def light(index):
		if index is 0:
			return colors.blue
		elif index is 1:
			return colors.lightgreen
		elif index is 2:
			return colors.lightyellow
		elif index is 3:
			return colors.lightorange			
		elif index is 4:
			return colors.lightred	
		elif index is 5:
			return colors.lightviolet
		elif index is 6:
			return colors.lightindigo
		else:
			return 'lightgray'
			
									
xq = ['#ffff00','#00ffff','#ff00ff']

chainColors = ['#ffdd22',
	'#ffcccc', '#ccffcc', '#ccccff', '#ffccff',
	'#008800', '#00dd00', '#88ff88', '#ccffcc',
	'#000088', '#4444ff', '#8888ff', '#ccccff',
	'#008888', '#00dddd', '#88ffff', '#ccffff',
	'#880088', '#ff00ff', '#ff88ff', '#ffccff',	
]

def 𝒞(node):
	spClass = len(node.address)
	if len(node.loop.root()) == spClass-2:
		return 'deepskyblue'
	elif len(node.loop.root()) == spClass-3: #int(node.address[-1]) + int(node.address[-2]) == 4:
		if node.address[-1] in ['0', '4']:
			return 'green'#'#99ff99'
		else:
			return 'limegreen'
	elif len(node.loop.root()) == spClass-4:
		if node.address[-1] in ['0', '4']:
			return '#ffb700'
		else:
			return '#f7f700'
	else:		
		if node.address[-1] in ['0', '4']:
			return 'darkred'#'#ffbbbb'
		else:
			return 'red'
			

def ℓ(diagram, node, forceNormal=True):	
	return colors.normal(node.ktype) if node.address[-1] is '0' or forceNormal else colors.light(node.ktype)
					
																
def loadE(extender):
	from diagram import Diagram
	d = Diagram(6)
	for node in extender:
		n = d.nodeByPerm[node.perm]
		#n.loop.color = 𝒞(n)
		for nln in n.loop.nodes:
			nln.color = 𝒞(nln)
		d.extendLoop(n)
	return d				
			
def loadS(sol):
	from diagram import Diagram
	d = Diagram(6)
	for step in sol.state:
		n = d.nodeByPerm[step.perm]
		#n.loop.color = 𝒞(n)
		for nln in n.loop.nodes:
			nln.color = 𝒞(nln)
		d.extendLoop(n)
	return d


def counts(diagram):
	chains = []
	loopedCount = 0
							
	for node in diagram.nodes:
		if node.chainID is not None:
			loopedCount += 1
			if node.chainID not in chains:
				chains.append(node.chainID)
	return (len(chains), loopedCount)
				
def show(diagram):
	if diagram.spClass == 9:
		return show9(diagram)
		
	with ui.ImageContext(diagram.W, diagram.H) as ctx:
	
		ui.set_color('white')
		ui.fill_rect(0, 0, diagram.W, diagram.H)

		chainColors = { }	
		loopedCount = 0
							
		nc = 0
		
		RR = 4
		DH = 2
			
		for node in diagram.nodes:

			oval = ui.Path.oval(node.px - RR/2, node.py - RR/2, RR, RR)

			if node.chainID is not None:
				loopedCount += 1
				if node.chainID not in chainColors:
					chainColors[node.chainID] = 'white' if node.chainID == diagram.startNode.chainID else hls_to_rgb(random(), 0.5, 1)
				ui.set_color(chainColors[node.chainID])
			else:
				ui.set_color('white')
			oval.fill()

			if node.chainID is not None and node.loop.extended:				
				# getting personal				
				ui.set_color(ℓ(diagram, node)) # 𝒞(node))
				oval.line_width = 4*DH
				oval.set_line_dash([1,1.05])
			elif node.loop.availabled:
				ui.set_color(ℓ(diagram, node))
				oval.line_width = DH
				oval.set_line_dash([1,1.05])
			elif node.chainID is not None:
				ui.set_color('black')
				oval.line_width = 0.2
				oval.set_line_dash([1,0])
			else:
				ui.set_color('gray')
				oval.line_width = 0.1
				oval.set_line_dash([1,0])
			oval.stroke()			
			
			if node.chainID is not None or len(node.showLinksOfTypes) is not 0:
				for nextLink in set(chain([node.nextLink], [node.links[t] for t in node.showLinksOfTypes]) if node.chainID is not None else [node.links[t] for t in node.showLinksOfTypes]):
					if nextLink.type is 2:
						line = ui.Path()
						line.move_to(node.px, node.py)
						line.line_to(nextLink.next.px, nextLink.next.py)
						line.line_width = nextLink.type * 0.5
						ui.set_color(ℓ(diagram, node, True))
						line.line_cap_style = ui.LINE_CAP_ROUND
						line.stroke()			
						
						circle = ui.Path.oval(node.px - 1.5*RR/2, node.py - 1.5*RR/2, 1.5*RR, 1.5*RR)
						ui.set_color(ℓ(diagram, node, True))
						circle.line_width = 1
						circle.stroke()
					else:
						line = ui.Path()
						line.move_to(node.px, node.py)
						line.line_to(nextLink.next.px, nextLink.next.py)
						line.line_width = nextLink.type * 0.25
						ui.set_color('red' if nextLink.type is 1 else 'green')
						line.line_cap_style = ui.LINE_CAP_ROUND
						line.stroke()									
			
			nc += 1
			
		img = ctx.get_image()
		img.show()
		print("[show] chain count: " + str(len(chainColors)) + " | looped: " + str(loopedCount) + "/" + str(len(diagram.nodes)) + " | remaining: " + str(len(diagram.nodes) - loopedCount))
		return (len(chainColors), loopedCount)
		
		
def show9(diagram):
	#assert False, "stale code"
	with ui.ImageContext(diagram.W, diagram.H) as ctx:
	
		print("show()")
		
		ui.set_color('white')
		ui.fill_rect(0, 0, diagram.W, diagram.H)

		chainColors = { }	
		loopedCount = 0
							
		nc = 0
		
		RR = 4 if diagram.spClass is not 9 else 2
		DH = 2 if diagram.spClass is not 9 else 1
			
		for node in diagram.nodes:
			if nc % 10000 is 0:
				print("[show] " + str(nc) + "/" + str(len(diagram.nodes)))
			#if nc == 4*len(diagram.nodes)/6:
				#break
			#oval = ui.Path.oval(node.px - RR/2, node.py - RR/2, RR, RR)

			if node.chainID is not None and node.loop.extended:				
				# getting personal				
				ui.set_color(ℓ(diagram, node)) # 𝒞(node))
				LH = 4*DH
				MQ = 1.5
			elif node.loop.availabled:
				ui.set_color(ℓ(diagram, node))
				LH = 4*DH
				MQ = 1.5
			elif node.chainID is not None:
				ui.set_color('black')
				LH = 0.2
				MQ = 0.5
			else:
				LH = 0.2
				MQ = 0.5

			ui.fill_rect(node.px - LH/2, node.py - LH/2, LH, LH)
			ui.set_color('white')
			ui.fill_rect(node.px - (LH-MQ)/2, node.py - (LH-MQ)/2, LH-MQ, LH-MQ)
												
			
			if node.chainID is not None:
				loopedCount += 1
				if node.chainID not in chainColors:
					chainColors[node.chainID] = 'white' if node.chainID == diagram.startNode.chainID else hls_to_rgb(random(), 0.5, 1)
				ui.set_color(chainColors[node.chainID])
			else:
				ui.set_color('white')
			ui.fill_rect(node.px - RR/2, node.py - RR/2, RR, RR)
			

			if node.chainID is not None or len(node.showLinksOfTypes) is not 0:
				for nextLink in set(chain([node.nextLink], [node.links[t] for t in node.showLinksOfTypes]) if node.chainID is not None else [node.links[t] for t in node.showLinksOfTypes]):
					if nextLink.type is 2:
						line = ui.Path()
						line.move_to(node.px, node.py)
						line.line_to(nextLink.next.px, nextLink.next.py)
						line.line_width = nextLink.type * 0.25
						ui.set_color(ℓ(diagram, node, True))
						line.line_cap_style = ui.LINE_CAP_ROUND
						line.stroke()			
						
						circle = ui.Path.oval(node.px - 1.5*RR/2, node.py - 1.5*RR/2, 1.5*RR, 1.5*RR)
						ui.set_color(ℓ(diagram, node, True))
						circle.line_width = 1
						circle.stroke()
			
			nc += 1
			
		img = ctx.get_image()
		img.show()
		print("[show] chain count: " + str(len(chainColors)) + " | looped: " + str(loopedCount) + "/" + str(len(diagram.nodes)) + " | remaining: " + str(len(diagram.nodes) - loopedCount))
		return (len(chainColors), loopedCount)
		
		
def run():
	
	diagram = Diagram(9)
		
	show(diagram)
	return diagram

	
if __name__ == "__main__":
	from common import Step, Sol
	diagram = run()
