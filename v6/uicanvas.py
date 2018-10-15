import ui
from itertools import chain
from colorsys import hls_to_rgb
from random import random
from node import *
from common import unitRoots
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
		
												

def draw(diagram):
	with ui.ImageContext(diagram.W, diagram.H) as ctx:
	
		ui.set_color('white')
		ui.fill_rect(0, 0, diagram.W, diagram.H)		
				
		if diagram.hasRadialCoords:
			MX = diagram.W / 2
			MY = diagram.H / 2
			
			ui.set_color('black')
			line = ui.Path()
			line.move_to(0, MY)
			line.line_to(diagram.W, MY)
			line.stroke()
			line = ui.Path()
			line.move_to(MX, 0)
			line.line_to(MX, diagram.H)
			line.stroke()
			
			PH = 2*16
			PJ = (math.sqrt(5)-1)*PH
							
			IH = 2*48
			IJ = (math.sqrt(5)-1)*IH
	
			base_ktype = diagram.nodeByPerm[diagram.altgen.perms[0]].prevs[1].node.ktype
			orderedLoops_ktype_index = [loop.ktype_columnIndex for loop in diagram.radialLoopsByKType[base_ktype]]
							
			centerPentaColor = colors.normal(base_ktype) # '#003b81' 
			offsetPentaColor = colors.light(base_ktype) # '#138fff'
	
	
			drawBoxes5(MX, MY, diagram.blue_18_inner_roots, diagram.blue_18_outer_roots, diagram, 18, -1)	
	
			drawCircledText(str(orderedLoops_ktype_index[18]), MX, MY, 40, 20, offsetPentaColor, 2.5)
			
			drawBoxes5(MX, MY, diagram.blue_23_inner_roots, diagram.blue_23_outer_roots, diagram, 23, -1)
	
			drawCircledText(str(orderedLoops_ktype_index[23]), MX, MY, 32, 16, centerPentaColor, 2)
	
			drawBoxes5(MX, MY, diagram.blue_5_inner_roots, diagram.blue_5_outer_roots,  diagram, 5, -1)
			
			drawCircledText(str(orderedLoops_ktype_index[5]), MX, MY, 24, 12, offsetPentaColor, 1.5)
																															
			drawBoxes5(MX, MY, diagram.blue_right_inner_roots, diagram.blue_right_outer_roots, diagram, 0, -1)
	
			drawCircledText(str(orderedLoops_ktype_index[0]), MX, MY, 16, 8, centerPentaColor, 1)
	
			for k in range(5):
				drawBoxes5(MX+diagram.first_penta_inner_roots[k][0], MY+diagram.first_penta_inner_roots[k][1], diagram.blue_left_inner_roots, diagram.blue_left_outer_roots, diagram, diagram.first_inner_blues[k], diagram.first_inner_offs[k])
				drawCircledText(str(orderedLoops_ktype_index[diagram.first_inner_blues[k]]), MX+diagram.first_penta_inner_roots[k][0], MY+diagram.first_penta_inner_roots[k][1], 16, 8, offsetPentaColor, 1)
			
			for k in range(5):
				drawBoxes5(MX+diagram.first_penta_outer_roots[k][0], MY+diagram.first_penta_outer_roots[k][1], diagram.blue_left_inner_roots, diagram.blue_left_outer_roots, diagram, diagram.first_outer_blues[k], diagram.first_outer_offs[k])
				
				drawCircledText(str(orderedLoops_ktype_index[diagram.first_outer_blues[k]]), MX+diagram.first_penta_outer_roots[k][0], MY+diagram.first_penta_outer_roots[k][1], 16, 8, centerPentaColor, 1)
			
			for k in range(5):
				drawBoxes5(MX+diagram.second_penta_inner_roots[k][0], MY+diagram.second_penta_inner_roots[k][1], diagram.blue_left_inner_roots, diagram.blue_left_outer_roots, diagram, diagram.second_inner_blues[k], diagram.second_inner_offs[k])
				drawCircledText(str(orderedLoops_ktype_index[diagram.second_inner_blues[k]]), MX+diagram.second_penta_inner_roots[k][0], MY+diagram.second_penta_inner_roots[k][1], 16, 8, centerPentaColor, 1)
	
		
			for k in range(5):
				drawBoxes5(MX+diagram.second_penta_outer_roots[k][0], MY+diagram.second_penta_outer_roots[k][1], diagram.blue_left_inner_roots, diagram.blue_left_outer_roots, diagram, diagram.second_outer_blues[k], diagram.second_outer_offs[k])
				drawCircledText(str(orderedLoops_ktype_index[diagram.second_outer_blues[k]]), MX+diagram.second_penta_outer_roots[k][0], MY+diagram.second_penta_outer_roots[k][1], 16, 8, offsetPentaColor, 1)
				
			RH = 8
			for cycle in diagram.cycles:
				drawBoxes6(cycle)				
				drawCircledText(str(cycle.index), cycle.px, cycle.py, RH, 4, 'black', 0.5)
						

		# for dx, dy in diagram.first_penta_inner_roots:
		# 	oval = ui.Path.oval(MX + dx - 4, MY + dy - 4, 8, 8)
		# 	ui.set_color('green')
		# 	oval.fill()
		# 
		# pwq = ui.Path()
		# pwq.move_to(MX + diagram.first_penta_inner_roots[0][0], MY + diagram.first_penta_inner_roots[0][1])
		# pwq.line_to(MX + diagram.first_penta_inner_roots[1][0], MY + diagram.first_penta_inner_roots[1][1])
		# pwq.line_to(MX + diagram.first_penta_inner_roots[2][0], MY + diagram.first_penta_inner_roots[2][1])
		# pwq.line_to(MX + diagram.first_penta_inner_roots[3][0], MY + diagram.first_penta_inner_roots[3][1])
		# pwq.line_to(MX + diagram.first_penta_inner_roots[4][0], MY + diagram.first_penta_inner_roots[4][1])
		# pwq.close()
		# ui.set_color('black')
		# pwq.stroke()
		# 
		# for dx, dy in diagram.first_penta_outer_roots:
		# 	oval = ui.Path.oval(MX + dx - 4, MY + dy - 4, 8, 8)
		# 	ui.set_color('red')
		# 	oval.fill()
		# 
		# pwq = ui.Path()
		# pwq.move_to(MX + diagram.first_penta_outer_roots[0][0], MY + diagram.first_penta_outer_roots[0][1])
		# pwq.line_to(MX + diagram.first_penta_outer_roots[1][0], MY + diagram.first_penta_outer_roots[1][1])
		# pwq.line_to(MX + diagram.first_penta_outer_roots[2][0], MY + diagram.first_penta_outer_roots[2][1])
		# pwq.line_to(MX + diagram.first_penta_outer_roots[3][0], MY + diagram.first_penta_outer_roots[3][1])
		# pwq.line_to(MX + diagram.first_penta_outer_roots[4][0], MY + diagram.first_penta_outer_roots[4][1])
		# pwq.close()
		# ui.set_color('black')
		# pwq.stroke()
		# 
		# for dx, dy in diagram.second_penta_inner_roots:
		# 	oval = ui.Path.oval(MX + dx - 4, MY + dy - 4, 8, 8)
		# 	ui.set_color('purple')
		# 	oval.fill()
		# 
		# pwq = ui.Path()
		# pwq.move_to(MX + diagram.second_penta_inner_roots[0][0], MY + diagram.second_penta_inner_roots[0][1])
		# pwq.line_to(MX + diagram.second_penta_inner_roots[1][0], MY + diagram.second_penta_inner_roots[1][1])
		# pwq.line_to(MX + diagram.second_penta_inner_roots[2][0], MY + diagram.second_penta_inner_roots[2][1])
		# pwq.line_to(MX + diagram.second_penta_inner_roots[3][0], MY + diagram.second_penta_inner_roots[3][1])
		# pwq.line_to(MX + diagram.second_penta_inner_roots[4][0], MY + diagram.second_penta_inner_roots[4][1])
		# pwq.close()
		# ui.set_color('black')
		# pwq.stroke()
		# 
		# for dx, dy in diagram.second_penta_outer_roots:
		# 	oval = ui.Path.oval(MX + dx - 4, MY + dy - 4, 8, 8)
		# 	ui.set_color('red')
		# 	oval.fill()
		# 
		# pwq = ui.Path()
		# pwq.move_to(MX + diagram.second_penta_outer_roots[0][0], MY + diagram.second_penta_outer_roots[0][1])
		# pwq.line_to(MX + diagram.second_penta_outer_roots[1][0], MY + diagram.second_penta_outer_roots[1][1])
		# pwq.line_to(MX + diagram.second_penta_outer_roots[2][0], MY + diagram.second_penta_outer_roots[2][1])
		# pwq.line_to(MX + diagram.second_penta_outer_roots[3][0], MY + diagram.second_penta_outer_roots[3][1])
		# pwq.line_to(MX + diagram.second_penta_outer_roots[4][0], MY + diagram.second_penta_outer_roots[4][1])
		# pwq.close()
		# ui.set_color('black')
		# pwq.stroke()
		

								
		HD = 32
		for cycle in diagram.cycles:
			marker = cycle.marker or (cycle.chain and cycle.chain.marker) or None
			if marker:
				oval = ui.Path.oval(cycle.px - HD/2, cycle.py - HD/2, HD, HD)
				ui.set_color(lc(diagram, cycle, marker))
				oval.fill()

		chainColors = { }	
		diagram.sh_looped_count = 0
							
		nc = 0
		
		RR = 4
		DH = 2
			
		for node in diagram.nodes:

			oval = ui.Path.oval(node.px - RR/2, node.py - RR/2, RR, RR)
			#if node.address.startswith('0000'):
				#print("draw " + node.address + " | " + str((node.px - RR/2, node.py - RR/2, RR, RR)))

			# § drawing chained node color fills
			if node.cycle.chain is not None and len(node.cycle.chain.cycles) > 1:
				diagram.sh_looped_count += 1
				if node.cycle.chain.id not in chainColors:
					chainColors[node.cycle.chain.id] = 'white' if node.cycle.chain.id == (0 if diagram.startNode.cycle.chain is None else diagram.startNode.cycle.chain.id) else hls_to_rgb(random(), 0.5, 1)
				ui.set_color(chainColors[node.cycle.chain.id])
			else:
				ui.set_color('white')
			oval.fill()

			# § drawing chained node strokes
			if node.cycle.chain is not None and (node.loop.extended or node.prevs[2].node.loop.extended):
				# getting personal				
				# ui.set_color(ℓ(diagram, node)) # 𝒞(node))
				# oval.line_width = 4*DH
				# oval.set_line_dash([1,1.05])
				# ui.set_color('black')
				#print("[nn] 𝒮: ", 𝒮(diagram, node))
				ui.set_color(𝒮(diagram, node))
				oval.fill()
				oval.line_width = 1
				oval.set_line_dash([1,0])
			elif node.loop.availabled:
				ui.set_color('black')
				oval = ui.Path.oval(node.px - 1/2, node.py - 1/2, 1, 1)				
				oval.line_width = 0.2
				oval.set_line_dash([1,0])				
				#ui.set_color(ℓ(diagram, node))
				#oval.line_width = DH
				#oval.set_line_dash([1,1.05])
			elif node.cycle.chain is not None and len(node.cycle.chain.cycles) > 1:
				ui.set_color('black')
				oval.line_width = 0.2
				oval.set_line_dash([1,0])
			else:
				ui.set_color('gray')
				oval.line_width = 0.1
				oval.set_line_dash([1,0])
			oval.stroke()			
			
			# § drawing links
			if node.cycle.chain is not None and len(node.cycle.chain.cycles) > 1:
				nextLink = node.nextLink if node.nextLink else (node.links[2] if node.loop.extended else node.links[1])
				if nextLink.type is 2:
					line = ui.Path()
					line.move_to(node.px, node.py)
					line.line_to(nextLink.next.px, nextLink.next.py)
					line.line_width = nextLink.type * 0.5
					ui.set_color(ℓ(diagram, node, True))
					line.line_cap_style = ui.LINE_CAP_ROUND
					line.stroke()			
										
				else:
					line = ui.Path()
					line.move_to(node.px, node.py)
					line.line_to(nextLink.next.px, nextLink.next.py)
					line.line_width = nextLink.type * 0.25
					ui.set_color('red' if nextLink.type is 1 else 'green')
					line.line_cap_style = ui.LINE_CAP_ROUND
					line.stroke()									
			
			nc += 1			
		
		# draw loop labels
		for cycle in diagram.cycles:
			for node in cycle.nodes:
				if node.loop.availabled or node.loop.extended:
					next = node.links[1].next
					centerX = (node.px + next.px)/2
					centerY = (node.py + next.py)/2
					centerX = cycle.px + (centerX - cycle.px)*1.6
					centerY = cycle.py + (centerY - cycle.py)*1.6
					text = str(node.loop.ktype_radialIndex)
					#text = str(node.loop.ktype_columnIndex)
					color = colors.normal(node.loop.ktype)
					width, height = ui.measure_string(text, 0, ('HelveticaNeue-MediumItalic', 6), ui.ALIGN_CENTER, ui.LB_CHAR_WRAP)
					ui.draw_string(text, (centerX - width / 2, centerY - height / 2, width, height), ('HelveticaNeue-MediumItalic', 6), color, ui.ALIGN_CENTER, ui.LB_CHAR_WRAP)	
					if node.loop.extended:
						border = ui.Path.oval(centerX - 5, centerY - 5, 10, 10)
						ui.set_color(color)
						border.stroke()
		
		for i,node_or_cycle in enumerate(diagram.pointers if diagram.pointers else []):
			if isinstance(node_or_cycle, Node):
				oval = ui.Path.oval(node_or_cycle.cycle.px - HD/2, node_or_cycle.cycle.py - HD/2, HD, HD)
			else:
				oval = ui.Path.oval(node_or_cycle.px - HD/2, node_or_cycle.py - HD/2, HD, HD)
			oval.line_width = 2
			#if diagram.spClass % 2 is 0 and i % 2 is not 0:
				#oval.set_line_dash([1,1.05])
			ui.set_color('black')
			oval.stroke()
			
			if isinstance(node_or_cycle, Node):
				oval = ui.Path.oval(node_or_cycle.px - RR, node_or_cycle.py - RR, 2*RR, 2*RR)
				oval.line_width = 0.5
				#if diagram.spClass % 2 is 0 and i % 2 is not 0:
					#oval.set_line_dash([1,1.05])
				ui.set_color('black')
				oval.stroke()			
			
			
		img = ctx.get_image()
		#img.show()
		print("[show] chain count: " + str(len([c for c in diagram.chains if len(c.cycles) > 1])) + " | available loops: " + str(len([l for l in diagram.loops if l.availabled]))  + " | looped: " + str(diagram.sh_looped_count) + "/" + str(len(diagram.nodes)) + " (" + "{0:.2f}".format(diagram.sh_looped_count*100.0/len(diagram.nodes)) + "%)" + " | remaining: " + str(len(diagram.nodes) - diagram.sh_looped_count))
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
		ui.set_color('white' if node.loop.extended or not node.loop.availabled else colors.light(node.ktype))
		box.fill()				

def drawBoxes6(cycle):											
	for i in range(6):
		box = ui.Path()
		box.move_to(cycle.px, cycle.py)
		box.line_to(cycle.px+cycle.inner_roots[i][0], cycle.py+cycle.inner_roots[i][1])
		box.line_to(cycle.px+cycle.outer_roots[i][0], cycle.py+cycle.outer_roots[i][1])	
		box.line_to(cycle.px+cycle.inner_roots[(i+1)%6][0], cycle.py+cycle.inner_roots[(i+1)%6][1])
		box.close()
		ui.set_color('white' if cycle.nodes[i].loop.extended or not cycle.nodes[i].loop.availabled else colors.normal(cycle.nodes[i].ktype))
		box.fill()
				
				
def show(diagram):
	img = draw(diagram)
	img.show()
	return img
	
	
if __name__ == "__main__":
	from diagram import *
	diagram = Diagram(6, 3)
	
	### « #5 | sol » @ sols.6.py ###
	
	'''
	diagram.extendLoop(diagram.nodeByAddress['00001'].loop)
	diagram.extendLoop(diagram.nodeByAddress['01033'].loop)
	diagram.extendLoop(diagram.nodeByAddress['02302'].loop)
	diagram.extendLoop(diagram.nodeByAddress['10030'].loop)
	diagram.extendLoop(diagram.nodeByAddress['10105'].loop)
	diagram.extendLoop(diagram.nodeByAddress['10205'].loop)
	diagram.extendLoop(diagram.nodeByAddress['10242'].loop)
	diagram.extendLoop(diagram.nodeByAddress['10305'].loop)
	diagram.extendLoop(diagram.nodeByAddress['11005'].loop)
	diagram.extendLoop(diagram.nodeByAddress['11105'].loop)
	diagram.extendLoop(diagram.nodeByAddress['11205'].loop)
	diagram.extendLoop(diagram.nodeByAddress['11305'].loop)
	diagram.extendLoop(diagram.nodeByAddress['12004'].loop)
	diagram.extendLoop(diagram.nodeByAddress['12013'].loop)
	diagram.extendLoop(diagram.nodeByAddress['12022'].loop)
	'''
	
	diagram.readdress('00005')
	setRadialCoords(diagram)	
	show(diagram)
	