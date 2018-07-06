import ui
from itertools import chain
from colorsys import hls_to_rgb
from random import random


class colors (object):
	blue 				= '#08f'

	green 			= '#0d0'
	lightgreen 	= '#bfb'
	
	yellow			= '#dd0'
	lightyellow	= '#ff9'
	
	orange			= '#f90'
	lightorange	= '#feb'
	
	red					= '#f00'
	lightred		= '#fdd'
	
	violet			= '#f0f'
	lightviolet	= '#fdf'
	
	indigo			= '#808'
	lightindigo	= '#cac'
	
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
			
			
def ℓ(diagram, node, forceNormal=True):	
	return colors.normal(node.ktype) if node.address[-1] is '0' or forceNormal else colors.light(node.ktype)
	
	
def show(diagram):
	with ui.ImageContext(diagram.W, diagram.H) as ctx:
	
		ui.set_color('white')
		ui.fill_rect(0, 0, diagram.W, diagram.H)

		HD = 32
		for cycle in diagram.cycles:
			if cycle.marker is not None:
				oval = ui.Path.oval(cycle.px - HD/2, cycle.py - HD/2, HD, HD)
				ui.set_color(lc(diagram, cycle))
				oval.fill()

		chainColors = { }	
		diagram.sh_looped_count = 0
							
		nc = 0
		
		RR = 4
		DH = 2
			
		for node in diagram.nodes:

			oval = ui.Path.oval(node.px - RR/2, node.py - RR/2, RR, RR)

			if node.chainID is not None:
				diagram.sh_looped_count += 1
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
		
		
		for i,node in enumerate(diagram.pointers):
			oval = ui.Path.oval(node.cycle.px - HD/2, node.cycle.py - HD/2, HD, HD)
			oval.line_width = 2
			if i % 2 is not 0:
				oval.set_line_dash([1,1.05])
			ui.set_color('black')
			oval.stroke()
			
			oval = ui.Path.oval(node.px - RR, node.py - RR, 2*RR, 2*RR)
			oval.line_width = 1
			if i % 2 is not 0:
				oval.set_line_dash([1,1.05])
			ui.set_color('black')
			oval.stroke()			
			
			
		img = ctx.get_image()
		img.show()
		print("[show] chain count: " + str(len(chainColors)) + " | looped: " + str(diagram.sh_looped_count) + "/" + str(len(diagram.nodes)) + " | remaining: " + str(len(diagram.nodes) - diagram.sh_looped_count))
		return (len(chainColors), diagram.sh_looped_count)
