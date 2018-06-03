import ui
from diagram import *
from colorsys import hls_to_rgb
from random import random
from enum import Enum


class colors (object):
	blue 				= '#08f'

	green 			= '#0d0'
	lightgreen 	= '#9f9'
	
	yellow			= '#ff0'
	lightyellow	= '#ff9'
	
	orange			= '#f90'
	lightorange	= '#fd9'
	
	red					= '#f00'
	lightred		= '#fbb'
	
	violet			= '#f0f'
	lightviolet	= '#fbf'
	
	indigo			= '#808'
	lightindigo	= '#d9d'
	
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
			

def ℓ(diagram, node):
	if diagram.spClass is 6:
		return ℓ6(node)
	elif diagram.spClass is 7:
		return ℓ7(node)
	elif diagram.spClass is 8:
		return ℓ8(node)
	elif diagram.spClass is 9:
		return ℓ9(node)		
	else:
		assert False, "no ℓ function for " + str(diagram.spClass)
		

def ℓ6(node):
	if node.loop.type() == 2:
		return colors.blue
	elif node.loop.type() == 3:
		return colors.green if node.address[-1] is '0' else colors.lightgreen
	elif node.loop.type() == 4:
		return colors.yellow if node.address[-1] is '0' else colors.lightyellow
	elif node.loop.type() == 5:		
		return 'black'  if node.address[-1] is '0' else 'lightgray'
		if (int(node.loop.head.address[-3]) + int(node.loop.head.address[-2]) ) % 4 == (2 - int(node.loop.head.address[-4])) % 3:
			return colors.orange  if node.address[-1] is '0' else colors.lightorange
		elif (int(node.loop.head.address[-3]) + int(node.loop.head.address[-2]) ) % 4 == (1 - int(node.loop.head.address[-4])) % 3:
			return colors.red  if node.address[-1] is '0' else colors.lightred			
		elif (int(node.loop.head.address[-3]) + int(node.loop.head.address[-2]) ) % 4 == (0 - int(node.loop.head.address[-4])) % 3:			
			return colors.violet  if node.address[-1] is '0' else colors.lightviolet			
		
		
def ℓ7(node):
	if node.loop.type() == 2:
		return colors.blue
	elif node.loop.type() == 3:
		return colors.green if node.address[-1] is '0' else colors.lightgreen
	elif node.loop.type() == 4:
		return colors.yellow if node.address[-1] is '0' else colors.lightyellow
	elif node.loop.type() == 5:
		return colors.orange if node.address[-1] is '0' else colors.lightorange		
	elif node.loop.type() == 6:
		return 'black'  if node.address[-1] is '0' else 'lightgray'


def ℓ8(node):
	if node.loop.type() == 2:
		return colors.blue
	elif node.loop.type() == 3:
		return colors.green if node.address[-1] is '0' else colors.lightgreen
	elif node.loop.type() == 4:
		return colors.yellow if node.address[-1] is '0' else colors.lightyellow
	elif node.loop.type() == 5:
		return colors.orange if node.address[-1] is '0' else colors.lightorange		
	elif node.loop.type() == 6:
		return colors.red  if node.address[-1] is '0' else colors.lightred
	elif node.loop.type() == 7:
		return 'black'  if node.address[-1] is '0' else 'lightgray'										


def ℓ9(node):
	if node.loop.type() == 2:
		return colors.blue
	elif node.loop.type() == 3:
		return colors.green if node.address[-1] is '0' else colors.lightgreen
	elif node.loop.type() == 4:
		return colors.yellow if node.address[-1] is '0' else colors.lightyellow
	elif node.loop.type() == 5:
		return colors.orange if node.address[-1] is '0' else colors.lightorange		
	elif node.loop.type() == 6:
		return colors.red  if node.address[-1] is '0' else colors.lightred
	elif node.loop.type() == 7:
		return colors.violet if node.address[-1] is '0' else colors.lightviolet
	elif node.loop.type() == 8:
		return 'black'  if node.address[-1] is '0' else 'lightgray'										
		
														
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
				oval.line_width = 0.2
				oval.set_line_dash([1,0])
			oval.stroke()			
			
			if node.chainID is not None:
				line = ui.Path()
				line.move_to(node.px, node.py)
				line.line_to(node.nextLink.next.px, node.nextLink.next.py)
				line.line_width = node.nextLink.type * 0.5
				if node.nextLink.type == 1:					
					ui.set_color('red')
				elif node.nextLink.type == 2:
					ui.set_color('#0066ff')
				elif node.nextLink.type == 3:
					ui.set_color('#008800')
				line.line_cap_style = ui.LINE_CAP_ROUND
				line.stroke()				
			
			nc += 1
			
		img = ctx.get_image()
		img.show()
		print("[show] chain count: " + str(len(chainColors)) + " | looped: " + str(loopedCount) + "/" + str(len(diagram.nodes)) + " | remaining: " + str(len(diagram.nodes) - loopedCount))
		return (len(chainColors), loopedCount)
		
		
def show9(diagram):
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
				LH = DH
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
			

			
			if node.chainID is not None:
				line = ui.Path()
				line.move_to(node.px, node.py)
				line.line_to(node.nextLink.next.px, node.nextLink.next.py)
				line.line_width = node.nextLink.type * 0.25
				if node.nextLink.type == 1:					
					ui.set_color('red')
				elif node.nextLink.type == 2:
					ui.set_color('#0066ff')
				elif node.nextLink.type == 3:
					ui.set_color('#008800')
				line.line_cap_style = ui.LINE_CAP_ROUND
				line.stroke()				
			
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
