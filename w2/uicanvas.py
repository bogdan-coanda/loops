import ui
import itertools
from colorsys import hls_to_rgb
from random import random
from node import *
from link import *
from common import unitRoots, randomColor
import math


class colors (object):
	blue 				= '#08f'
	lightblue		= '#8cf'

	green 			= '#0d0'
	lightgreen 	= '#6f6'
	
	yellow			= '#dd0'
	lightyellow	= '#ff6'
	
	orange			= '#f90'
	lightorange	= '#fb6'
	
	red					= '#f00'
	lightred		= '#f66'
	
	violet			= '#f0f'
	lightviolet	= '#f6f'
	
	indigo			= '#808'
	lightindigo	= '#a3a'
	
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
			return colors.lightblue
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
	
def 𝒮(diagram, node):
	if node.loop.extended:
		return colors.normal(node.ktype)
	elif node.prevs[2].node.loop.extended:
		return colors.normal(node.prevs[2].node.ktype)
	else:
		return 'white'
	
	
	
def lc(diagram, cycle, marker):
	return colors.normal(marker)
	
	
def setRadialCoords(diagram):	
	
	diagram.hasRadialCoords = True
	
	diagram.W *= 2
	diagram.H *= 2
	
	MX = diagram.W / 2
	MY = diagram.H / 2
		
	RH = 8
								
	for cycle in diagram.cycles:
		cycle.setCoords(RH, 0, 32, 32)
		
	orderedCycles = [diagram.nodeByPerm[diagram.altgen.perms[i]].cycle for i in range(0, len(diagram.altgen.perms), diagram.spClass)]
	# internal node coords need to be corrected (rotated)
		
	PH = 2*16
	PJ = (math.sqrt(5)-1)*PH
		
	diagram.blue_right_inner_roots = unitRoots(5, PH, -0.5)		
	diagram.blue_right_outer_roots = unitRoots(5, PJ, 0)		
		
	for i in range(5):
		orderedCycles[i].setCoords(RH, (-6*i-3)/5, MX + diagram.blue_right_inner_roots[(-i)%5][0], MY + diagram.blue_right_inner_roots[(-i)%5][1])
				
	IH = 2*64
	IJ = (math.sqrt(5)-1)*IH
	IK = ((math.sqrt(5)-1)**2.4)*IJ
	IL = (math.sqrt(5)-1)*IK
	
	diagram.blue_left_inner_roots = unitRoots(5, PH, 1)
	diagram.blue_left_outer_roots = unitRoots(5, PJ, 1.5)			
	
	diagram.first_penta_inner_roots = unitRoots(5, IH, -0.5)	
	
	diagram.first_inner_blues = [1, 3, 9, 16, 12]
	diagram.first_inner_offs = [-1, 1, 0, 0, 0]
	
	for k in range(5):			
		for i in range(5*diagram.first_inner_blues[k],5*(diagram.first_inner_blues[k]+1)):
			orderedCycles[i].setCoords(RH, (6*(2+diagram.first_inner_offs[k]-i))/5, MX + diagram.first_penta_inner_roots[k][0] + diagram.blue_left_inner_roots[(1+diagram.first_inner_offs[k]-i)%5][0], MY + diagram.first_penta_inner_roots[k][1] + diagram.blue_left_inner_roots[(1+diagram.first_inner_offs[k]-i)%5][1])	

	diagram.first_penta_outer_roots = unitRoots(5, IJ, 0)
	
	diagram.first_outer_blues = [2, 6, 8, 13, 4]
	diagram.first_outer_offs = [0, 3, 3, 2, 2]
		
	for k in range(5):
		for i in range(5*diagram.first_outer_blues[k],5*(diagram.first_outer_blues[k]+1)):
			orderedCycles[i].setCoords(RH, (6*(2+diagram.first_outer_offs[k]-i))/5, MX + diagram.first_penta_outer_roots[k][0] + diagram.blue_left_inner_roots[(1+diagram.first_outer_offs[k]-i)%5][0], MY + diagram.first_penta_outer_roots[k][1] + diagram.blue_left_inner_roots[(1+diagram.first_outer_offs[k]-i)%5][1])	
			
	diagram.second_penta_inner_roots = unitRoots(5, IK, 2.5)

	diagram.second_inner_blues = [7, 14, 20, 22, 11]#, 11, 22, 20, 14]
	diagram.second_inner_offs = [0, 0, 4, 1, 0]
		
	diagram.second_outer_blues = [10, 15, 17, 21, 19]#, 10, 19, 21, 17]
	diagram.second_outer_offs = [3, 2, 2, 0, 3]
	
	for k in range(5):			
		for i in range(5*diagram.second_inner_blues[k],5*(diagram.second_inner_blues[k]+1)):
			orderedCycles[i].setCoords(RH, (6*(2+diagram.second_inner_offs[k]-i))/5, MX + diagram.second_penta_inner_roots[k][0] + diagram.blue_left_inner_roots[(1+diagram.second_inner_offs[k]-i)%5][0], MY + diagram.second_penta_inner_roots[k][1] + diagram.blue_left_inner_roots[(1+diagram.second_inner_offs[k]-i)%5][1])	

	diagram.second_penta_outer_roots = unitRoots(5, IL, 2)
	
	
	for k in range(5):			
		for i in range(5*diagram.second_outer_blues[k],5*(diagram.second_outer_blues[k]+1)):
			orderedCycles[i].setCoords(RH, (6*(2+diagram.second_outer_offs[k]-i))/5, MX + diagram.second_penta_outer_roots[k][0] + diagram.blue_left_inner_roots[(1+diagram.second_outer_offs[k]-i)%5][0], MY + diagram.second_penta_outer_roots[k][1] + diagram.blue_left_inner_roots[(1+diagram.second_outer_offs[k]-i)%5][1])		
			
	diagram.blue_23_inner_roots = unitRoots(5, 2*PH, -0.5)
	diagram.blue_23_outer_roots = unitRoots(5, 2*PJ, 0)
	
	for i in range(115, 120):
		orderedCycles[i].setCoords(RH, (-6*i-3)/5, MX + diagram.blue_23_inner_roots[(-i)%5][0], MY + diagram.blue_23_inner_roots[(-i)%5][1])		
		
	diagram.blue_5_inner_roots = unitRoots(5, 1.5*PH, 0)
	diagram.blue_5_outer_roots = unitRoots(5, 1.5*PJ, 0.5)		

	for i in range(25, 30):
		orderedCycles[i].setCoords(RH, (6*(5-i))/5, MX + diagram.blue_5_inner_roots[(-i)%5][0], MY + diagram.blue_5_inner_roots[(-i)%5][1])		
	
	diagram.blue_18_inner_roots = unitRoots(5, 2.5*PH, 0)
	diagram.blue_18_outer_roots = unitRoots(5, 2.5*PJ, 0.5)		

	for i in range(90, 95):
		orderedCycles[i].setCoords(RH, (6*(5-i))/5, MX + diagram.blue_18_inner_roots[(-i)%5][0], MY + diagram.blue_18_inner_roots[(-i)%5][1])		
															

def circular_dash(diameter, slices):
	length = 3.1415926*diameter
	return [length/2/slices, length/2/slices]
	

def draw(diagram, **kwargs):
	superpermutation = kwargs['sp'] if 'sp' in kwargs else None
	cyclePath = kwargs['cp'] if 'cp' in kwargs else None
	
	def drawLink(link):
		line = ui.Path()
		line.move_to(link.node.px, link.node.py)
		#if link.next.address[-2:] == '00' and link.type == 2:
		if link.node.px == link.next.px:
			line.add_quad_curve(link.next.px, link.next.py, link.next.px - abs(link.node.py - link.next.py)/10, (link.node.py + link.next.py) / 2) # 20
		else:
			line.line_to(link.next.px, link.next.py)			
		line.line_cap_style = ui.LINE_CAP_ROUND			
		if link.type is 1:
			line.line_width = 0.25
			ui.set_color('red')
		elif link.type is 2:
			line.line_width = 1
			ui.set_color(ℓ(diagram, link.node, True))
		elif link.type is 3:
			line.line_width = 1.25
			ui.set_color('green')
		elif link.type is 4:
			line.line_width = 1.5			
			ui.set_color('orange')
		else:
			line.line_width = 2		
			ui.set_color('fuchsia')
		line.stroke()		
	
	def drawNodePointer(node, color='black'):
		ui.set_color(color)
		# draw cycle circle
		oval = ui.Path.oval(node.cycle.px - HD/2, node.cycle.py - HD/2, HD, HD)
		oval.line_width = 0.25 if color == 'black' else 1
		if color != 'black':
			oval.set_line_dash(circular_dash(HD, 16))
		oval.stroke()		
		# draw node circle
		oval = ui.Path.oval(node.px - RR, node.py - RR, 2*RR, 2*RR)
		oval.line_width = 0.25 if color == 'black' else 1
		if color != 'black':
			oval.set_line_dash(circular_dash(2*RR, 8))
		oval.stroke()								
		
	
	with ui.ImageContext(diagram.W, diagram.H) as ctx:
	
		ui.set_color('white')
		ui.fill_rect(0, 0, diagram.W, diagram.H)		
								
		# draw boxes first, if any
		for box_addr, ktype in diagram.draw_boxes:
			box_nodes = [node for node in diagram.nodes if node.address.startswith(box_addr)]
			minX = min([node.px for node in box_nodes])
			maxX = max([node.px for node in box_nodes])
			minY = min([node.py for node in box_nodes])
			maxY = max([node.py for node in box_nodes])
			
			rect = ui.Path.rect(minX - 12 - 1.6*ktype, minY - 12 - 1.6*ktype, maxX - minX + 24 + 3.2*ktype, maxY - minY + 24 + 3.2*ktype)
			rect.line_width = 1.2
			ui.set_color(colors.normal(ktype))
			rect.stroke()								
								
		HD = 32
							
		nc = 0
		
		RR = 4
		DH = 2
		
		C2 = 1.5
		C3 = 3.5

		top_unconnectable = []
		top_l2_singles = []
		top_l3_singles = []		
		bot_unconnectable = []
		bot_l2_singles = []
		bot_l3_singles = []		
				
		links_types = { 1: 0, 2: 0, 3: 0, 4: 0 }
							
		for node in diagram.nodes:

			oval = ui.Path.oval(node.px - RR/2, node.py - RR/2, RR, RR)

			# § drawing chained node color fills
			if len(node.cycle.chain.cycles) > 1:
				if node.cycle.chain.color == None:
					node.cycle.chain.color = 'orange' if node.cycle.chain.isOpen else randomColor()
				ui.set_color(node.cycle.chain.color)
			else:
				ui.set_color('white')
			oval.fill()

			# § drawing chained node strokes
			if node.cycle.chain:
				ui.set_color('gray')
				oval.line_width = 0.2
			else:
				ui.set_color('black')
				oval.line_width = 0.1
			oval.stroke()			
			'''						
			# § drawing outgoing sockets
			out2 = False
			out3 = False
			if node == node.cycle.bot_node():
				if node.nextLink == None:
					if node.links[2].next.prevLink == None and (node.links[2].next.cycle.chain == None or node.links[2].next.cycle.chain != node.cycle.chain):
						out2 = True
						o2 = ui.Path.oval(node.px - RR/2 - C2/2, node.py - RR/2 - C2/2, RR + C2, RR + C2)
						o2.line_width = 0.8
						ui.set_color(ui.set_color(colors.normal(node.ktype)))
						o2.stroke()
					if node.links[3].next.prevLink == None and (node.links[3].next.cycle.chain == None or node.links[3].next.cycle.chain != node.cycle.chain):
						out3 = True
						o3 = ui.Path.oval(node.px - RR/2 - C3/2, node.py - RR/2 - C3/2, RR + C3, RR + C3)						
						o3.line_width = 1.2
						o3.set_line_dash(circular_dash(RR + C3, 8))						
						ui.set_color(ui.set_color('limegreen'))
						o3.stroke()						

					if not out2 and not out3: bot_unconnectable.append(node)
					elif not out3: bot_l2_singles.append(node)
					elif not out2: bot_l3_singles.append(node)
			'''
			
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
																
			nc += 1														

		# draw loop labels
		for cycle in diagram.cycles:
			for node in cycle.nodes:
				if node.loop.available or node.loop.extended:
					next = node.links[1].next
					centerX = (node.px + next.px)/2
					centerY = (node.py + next.py)/2
					centerX = cycle.px + (centerX - cycle.px)*1.6
					centerY = cycle.py + (centerY - cycle.py)*1.6
					text = str(node.loop.ktype_radialIndex)# + ":" + str(len(node.loop.sols))
					#text = str(node.loop.ktype_columnIndex)
					color = colors.normal(node.loop.ktype)
					width, height = ui.measure_string(text, 0, ('HelveticaNeue-MediumItalic', 6), ui.ALIGN_CENTER, ui.LB_CHAR_WRAP)
					ui.draw_string(text, (centerX - width / 2, centerY - height / 2, width, height), ('HelveticaNeue-MediumItalic', 6), color, ui.ALIGN_CENTER, ui.LB_CHAR_WRAP)	
					if node.loop.extended:
						border = ui.Path.oval(centerX - 5, centerY - 5, 10, 10)
						ui.set_color(color)
						border.stroke()
					if diagram.draw_sol_counts:
						text = str(len(node.loop.sols))
						width, height = ui.measure_string(text, 0, ('HelveticaNeue-MediumItalic', 4), ui.ALIGN_CENTER, ui.LB_CHAR_WRAP)
						ui.draw_string(text, (centerX - width / 2, centerY - height / 2 - 5, width, height), ('HelveticaNeue-MediumItalic', 4), 'black', ui.ALIGN_CENTER, ui.LB_CHAR_WRAP)					
		
		# draw cycle centers
		# for cycle in diagram.cycles:
			# text = str(sum([len(node.loop.sols) for node in cycle.nodes]))
			# width, height = ui.measure_string(text, 0, ('HelveticaNeue-MediumItalic', 4), ui.ALIGN_CENTER, ui.LB_CHAR_WRAP)
			# ui.draw_string(text, (cycle.px - width / 2, cycle.py - height / 2, width, height), ('HelveticaNeue-MediumItalic', 4), 'black', ui.ALIGN_CENTER, ui.LB_CHAR_WRAP)
			
		RR = 6
		
		if diagram.openChain:
			drawNodePointer(diagram.openChain.headNode)
			drawNodePointer(diagram.openChain.tailNode)
			#drawNodePointer(diagram.openChain.tailNode.links[2].next, colors.normal(0))
			#drawNodePointer(diagram.openChain.tailNode.links[3].next, colors.normal(1))
		
		for i,node_or_cycle in enumerate(diagram.pointers):
			if isinstance(node_or_cycle, Node):
				oval = ui.Path.oval(node_or_cycle.cycle.px - HD/2, node_or_cycle.cycle.py - HD/2, HD, HD)
			else:
				oval = ui.Path.oval(node_or_cycle.px - HD/2, node_or_cycle.py - HD/2, HD, HD)
			oval.line_width = 0.25
			#if diagram.spClass % 2 is 0 and i % 2 is not 0:
				#oval.set_line_dash([1,1.05])
			ui.set_color('black')
			oval.stroke()
			
			if isinstance(node_or_cycle, Node):
				oval = ui.Path.oval(node_or_cycle.px - RR, node_or_cycle.py - RR, 2*RR, 2*RR)
				oval.line_width = 0.25
				#if diagram.spClass % 2 is 0 and i % 2 is not 0:
					#oval.set_line_dash([1,1.05])
				ui.set_color('black')
				oval.stroke()								
						
		img = ctx.get_image()
		#img.show()
		
		connected_cycles = sum([len(chain.cycles) for chain in diagram.chains if len(chain.cycles) > 1])
		extension_length = diagram.spClass * (diagram.spClass - 1) - 1
		total = links_types[1]+2*links_types[2]+3*links_types[3]+4*links_types[4] - (len([ch for ch in diagram.chains if len(ch.cycles) > 1]) - 1) * diagram.spClass
		final = diagram.spClass + total + (len(diagram.chains) - 1) / (diagram.spClass - 2) * extension_length
		
		# print(f"[show] connected cycles: {connected_cycles}")
		# print(f"[show] extension length: {extension_length}")
	
		print(f"[show] chains: {len(diagram.chains)} ({len([ch for ch in diagram.chains if len(ch.cycles) == 1])}/{len([ch for ch in diagram.chains if len(ch.cycles) != 1])}) | connected cycles: {connected_cycles} | links: ℓ₁x{links_types[1]} ℓ₂x{links_types[2]} ℓ₃x{links_types[3]} ℓ₄x{links_types[4]} | total: {total} | final: {final}")
		'''
		for chain in diagram.chains:
			print(chain)
		if len(top_unconnectable):
			print(f"top unconnectable: " + " ".join([n.cycle.address for n in top_unconnectable]))
		if len(top_l2_singles):
			print(f"top [2] singles: " + " ".join([n.cycle.address for n in top_l2_singles]))			
		if len(top_l3_singles):
			print(f"top [3] singles: " + " ".join([n.cycle.address for n in top_l3_singles]))						
		if len(bot_unconnectable):
			print(f"bot unconnectable: " + " ".join([n.cycle.address for n in bot_unconnectable]))
		if len(bot_l2_singles):
			print(f"bot [2] singles: " + " ".join([n.cycle.address for n in bot_l2_singles]))			
		if len(bot_l3_singles):
			print(f"bot [3] singles: " + " ".join([n.cycle.address for n in bot_l3_singles]))									
		'''
		print(img.size)
		return img
		

def drawCircledText(text, centerX, centerY, radius, textSize, color, borderWidth):
	oval = ui.Path.oval(centerX - radius/2, centerY - radius/2, radius, radius)
	ui.set_color('white')
	oval.fill()
	ui.set_color(color)
	oval.line_width = borderWidth
	oval.stroke()
	width, height = ui.measure_string(text, 0, ('HelveticaNeue-MediumItalic', textSize), ui.ALIGN_CENTER, ui.LB_CHAR_WRAP)
	ui.draw_string(text, (centerX - width / 2, centerY - height / 2, width, height), ('HelveticaNeue-MediumItalic', textSize), color, ui.ALIGN_CENTER, ui.LB_CHAR_WRAP)	

	
def drawBoxes5(cornerX, cornerY, inner_roots, outer_roots, diagram, cycleIndex, inner_off):
	for i in range(5):
		box = ui.Path()
		box.move_to(cornerX, cornerY)
		box.line_to(cornerX + inner_roots[i][0], cornerY + inner_roots[i][1])
		box.line_to(cornerX + outer_roots[i][0], cornerY + outer_roots[i][1])	
		box.line_to(cornerX + inner_roots[(i+1)%5][0], cornerY + inner_roots[(i+1)%5][1])
		box.close()
		
		node = diagram.cycles[5*cycleIndex+(inner_off-i)%5].nodes[0]		
		ui.set_color('white' if node.loop.extended or not node.loop.available else colors.light(node.ktype))
		box.fill()				

def drawBoxes6(cycle):											
	for i in range(6):
		box = ui.Path()
		box.move_to(cycle.px, cycle.py)
		box.line_to(cycle.px+cycle.inner_roots[i][0], cycle.py+cycle.inner_roots[i][1])
		box.line_to(cycle.px+cycle.outer_roots[i][0], cycle.py+cycle.outer_roots[i][1])	
		box.line_to(cycle.px+cycle.inner_roots[(i+1)%6][0], cycle.py+cycle.inner_roots[(i+1)%6][1])
		box.close()
		ui.set_color('white' if cycle.nodes[i].loop.extended or not cycle.nodes[i].loop.available else colors.normal(cycle.nodes[i].ktype))
		box.fill()
				
				
def show(diagram, **kwargs):
	img = draw(diagram, **kwargs)
	img.show()
	return img
	
	
if __name__ == "__main__":	
	from diagram import *
	diagram = Diagram(6)
	
	def connect(cycle_addr, link_type):
		cycle = diagram.cycleByAddress[cycle_addr]
		cycle.bot_node().nextLink = cycle.bot_node().links[link_type]			
		cycle.bot_node().nextLink.next.prevLink = cycle.bot_node().links[link_type]
		
	connect('0010', 2)
	connect('0011', 2)
	connect('0012', 2)
	connect('0013', 2)
	connect('0014', 2)
			
	show(diagram)
	
