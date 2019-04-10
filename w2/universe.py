#import console; 
import os;
#import ui;
import webbrowser

from node import *
from loop import color_string
from common import randomColor


def show(diagram):	

	svg = '<?xml version="1.0" encoding="UTF-8" ?>'
	
	windowWidth = 1800 # ui.get_window_size().width
	if windowWidth * diagram.H / diagram.W > 920: # ui.get_window_size().height:
		windowWidth = 920 * diagram.W / diagram.H # ui.get_window_size().height
	
	svg += f'<svg width="{windowWidth}" height="{windowWidth * diagram.H / diagram.W}" viewBox="0 0 {diagram.W} {diagram.H}" xmlns="http://www.w3.org/2000/svg">'


	def drawLink(link):
		nonlocal svg
		path = f"M {link.node.px} {link.node.py}"
		
		if link.type > 1 and link.node.px == link.next.px:
			path += f"Q {link.next.px - abs(link.node.py - link.next.py)/4} {(link.node.py + link.next.py) / 2} {link.next.px} {link.next.py}"
		else:
			path += f"L {link.next.px} {link.next.py}"
		
		if link.type is 1:
			line_width = 0.25
			line_color = 'red'
		elif link.type is 2:
			line_width = 1
			line_color = color_string(link.node.ktype)
		elif link.type is 3:
			line_width = 1.25
			line_color = 'green'
		elif link.type is 4:
			line_width = 1.5			
			line_color = 'orange'
		else:
			line_width = 2		
			line_color = 'fuchsia'

		svg += f'<path d="{path}" stroke="{line_color}" stroke-width="{line_width}" fill="none"/>'
						
						
	def drawNodePointer(node, color='black'):
		nonlocal svg
		
		# draw cycle circle
		svg += f'<circle cx="{node.cycle.px}" cy="{node.cycle.py}" r="16" stroke="{color}" stroke-width="0.25" fill="none" />'		
		# draw node circle
		svg += f'<circle cx="{node.px}" cy="{node.py}" r="6" stroke="{color}" stroke-width="0.25" fill="none" />'		
		
														
	links_types = { 1: 0, 2: 0, 3: 0, 4: 0 }
		
	# ---  draw nodes and links --- #
	for node in diagram.nodes:				
		
		# -§-  choose node fill color  -§- #
		# if the node is part of the (potentially partial) solution
		if len(node.cycle.chain.cycles) > 1 or node.cycle.chain.isOpen:
			# make sure the node's chain has color set
			if node.cycle.chain.color == None:
				node.cycle.chain.color = 'orange' if node.cycle.chain.isOpen else randomColor()
			fill_color = node.cycle.chain.color
		else:
			fill_color = 'white'
		
		# -$-  draw node  -$- #
		svg += f'<circle cx="{node.px}" cy="{node.py}" r="3" stroke="gray" stroke-width="0.2" fill="{fill_color}" />'

		# -§-	 draw outward link, if any  -§- #
		if diagram.openChain and node == diagram.openChain.tailNode: # the only node without a nextLink
			pass
		elif node.nextLink: # explicitly set in appendChain(), 
			drawLink(node.nextLink)						
			links_types[node.nextLink.type] += 1				
		elif node.loop.extended: # implicit ℓ₂, by extendLoop(),
			drawLink(node.links[2])
			links_types[2] += 1
		elif len(node.cycle.chain.cycles) > 1: # implicit ℓ₁, drawn only for multicycle chains
			drawLink(node.links[1])
			links_types[1] += 1					

	# draw loop labels
	for cycle in diagram.cycles:
		for node in cycle.nodes:
			if node.loop.available or node.loop.extended:
				next = node.links[1].next
				centerX = (node.px + next.px)/2
				centerY = (node.py + next.py)/2
				centerX = cycle.px + (centerX - cycle.px)*1.6
				centerY = cycle.py + (centerY - cycle.py)*1.6
				
				svg += f'<text x="{centerX}" y="{centerY}" dominant-baseline="middle" text-anchor="middle" fill="{color_string(node.loop.ktype)}" font-family="HelveticaNeue-MediumItalic" font-size="5">{node.loop.ktype_radialIndex}</text>'
				
				if node.loop.extended:
					svg += f'<circle cx="{centerX}" cy="{centerY}" r="4.5" stroke="{color_string(node.loop.ktype)}" stroke-width="1" fill="none" />'

	if diagram.openChain:
		drawNodePointer(diagram.openChain.headNode)
		drawNodePointer(diagram.openChain.tailNode)

	for i,node_or_cycle in enumerate(diagram.pointers):
		if isinstance(node_or_cycle, Node):
			drawNodePointer(node_or_cycle)
		else:
			svg += f'<circle cx="{node_or_cycle.px}" cy="{node_or_cycle.py}" r="16" stroke="black" stroke-width="0.25" fill="none" />'					
			
	svg += '</svg>'
	
	connected_cycles = sum([len(chain.cycles) for chain in diagram.chains if len(chain.cycles) > 1])
	extension_length = diagram.spClass * (diagram.spClass - 1) - 1
	total = links_types[1]+2*links_types[2]+3*links_types[3]+4*links_types[4] - (len([ch for ch in diagram.chains if len(ch.cycles) > 1]) - 1) * diagram.spClass
	final = diagram.spClass + total + (len(diagram.chains) - 1) / (diagram.spClass - 2) * extension_length
	
	print(f"[show] chains: {len(diagram.chains)} ({len([ch for ch in diagram.chains if len(ch.cycles) == 1])}/{len([ch for ch in diagram.chains if len(ch.cycles) != 1])}) | connected cycles: {connected_cycles} | links: ℓ₁x{links_types[1]} ℓ₂x{links_types[2]} ℓ₃x{links_types[3]} ℓ₄x{links_types[4]} | total: {total} | final: {final}")
	
	file = f'__diagram_{diagram.spClass}__.svg'
	with open(file, 'w') as out_file:
		out_file.write(svg)

	webbrowser.open('file://' + os.path.realpath(file))
	# console.quicklook(os.path.abspath(file))
	
	
	
	
if __name__ == "__main__":	
	from diagram import *
	diagram = Diagram(6)
	
	diagram.extendLoop(diagram.nodeByAddress['00001'].loop)

	
	diagram.point()
	diagram.pointers += [diagram.cycleByAddress['1234']]	
	show(diagram)

