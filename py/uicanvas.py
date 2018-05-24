import ui
from diagram import *


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
			return '#f7d700'
		else:
			return '#f7f700'
	else:		
		if node.address[-1] in ['0', '4']:
			return 'darkred'#'#ffbbbb'
		else:
			return 'red'
						
			
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

def show(diagram):
	with ui.ImageContext(diagram.W, diagram.H) as ctx:
	
		ui.set_color('white')
		ui.fill_rect(0, 0, diagram.W, diagram.H)

		for node in diagram.nodes:
			if node.looped:
				if node.extended:
					for nln in node.loop.nodes:
						nln.color = 𝒞(nln)		
								
		for node in diagram.nodes:
			
			RR = 4
			DH = 2
			
			oval = ui.Path.oval(node.px - RR/2, node.py - RR/2, RR, RR)

			if node.looped:
				for i in range(21):
					if node.chainID is i or diagram.areConnected(i, node.chainID):
						ui.set_color(chainColors[i])
						break												
			else:
				ui.set_color('white')
			oval.fill()

			if node.color is not None:
				# getting personal				
				ui.set_color(node.color)
				oval.line_width = 6*DH
				oval.set_line_dash([1,1.05])				
			elif node.loop.color is not None:	
				# marked
				ui.set_color(node.loop.color)
				oval.line_width = 6*DH
				oval.set_line_dash([1,1.05])			
			elif node.extended:
				ui.set_color('red')				
				oval.line_width = DH
				oval.set_line_dash([1,1.05])			
			elif node.loop.seen:
				ui.set_color('white')				
				oval.line_width = DH
				oval.set_line_dash([1,1.05])			
			elif node.loop.availabled:
				ui.set_color('black')				
				oval.line_width = DH
				oval.set_line_dash([1,1.05])
			elif node.looped:
				ui.set_color('black')
				oval.line_width = 0.2
				oval.set_line_dash([1,0])
			else:
				oval.line_width = 0.2
				oval.set_line_dash([1,0])
			oval.stroke()

			if node.looped:
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
				
			if node.marked:
				mark = ui.Path.oval(node. px - 2*RR, node.py - 2*RR, 4*RR, 4*RR)
				ui.set_color((1, 0, 1, 0.25))
				mark.fill()
				mark.line_width = 4
				mark.set_line_dash([1,0])
				mark.stroke()				
				

		img = ctx.get_image()
		img.show()
		
		
def run():
	diagram = Diagram(6)
			
	jkinit(diagram)
	
	def extendAddress(address):
		node = diagram.nodeByAddress[address]
		for nln in node.loop.nodes:
			nln.color = 𝒞(nln)
		assert diagram.extendLoop(
			sorted(node.loop.nodes, key = lambda n: n.looped).pop()
			if not node.looped and len([n for n in node.loop.nodes if n.looped]) is not 0
			else node)
		return node.loop


	extendAddress('12000') 
	#diagram.nodeByAddress['12000'].marked = True
	extendAddress('12010')
	extendAddress('12020')
	
	extendAddress('12110')
	extendAddress('12120')
	extendAddress('12130')
	
	extendAddress('12200')
	extendAddress('12210')
	extendAddress('12220')
	
	extendAddress('12310')
	extendAddress('12320')
	extendAddress('12330')
	
	
	extendAddress('11004')
	extendAddress('11204')
	
	extendAddress('02004')
	extendAddress('02204')
	
	extendAddress('10104')
	extendAddress('10304')
	
	extendAddress('01104')
	extendAddress('01304')
	
	extendAddress('11105')
	extendAddress('02105')
	extendAddress('10205')
	extendAddress('01205')
				
	# extendAddress('11013').color = chainColors[1]
	# extendAddress('11022').color = chainColors[2]
	
	# extendAddress('11120').color = chainColors[3]	
	# extendAddress('11210').color = chainColors[4]		
	# extendAddress('11030').color = chainColors[5]	
	# extendAddress('11300').color = chainColors[6]
			
	# Columns
	# extendAddress('12005')
	# extendAddress('12245')
	# extendAddress('12145')
	# extendAddress('12045')
	# 
	# extendAddress('11325')
	# extendAddress('11235')
	# extendAddress('11105')
	# extendAddress('11015')
	# 
	# extendAddress('10335')
	# extendAddress('10205')
	# extendAddress('10115')
	# extendAddress('10025')
	# 
	# extendAddress('02335')
	# extendAddress('02245')
	# extendAddress('02115')
	# extendAddress('02025')
	# 
	# extendAddress('01335')
	# extendAddress('01205')
	# extendAddress('01115')
	# extendAddress('01025')
	#
	
	
	# V0 - [14]
	# extendAddress('00001').color = 'yellow'
	# extendAddress('00243').color = 'yellow'
	# extendAddress('01112').color = 'red'
	# extendAddress('10240').color = 'orange'
	# extendAddress('10341').color = 'lightgreen'
	# extendAddress('11021').color = 'green'
	# extendAddress('12012').color = 'darkgreen'
	# extendAddress('12203').color = 'blue'
	# extendAddress('12213').color = 'orange'
	# extendAddress('12222').color = 'darkorange'
	# extendAddress('12320').color = 'red'
			
	# V1 - [14]
	# extendAddress('00001').color = 'yellow'
	# extendAddress('00243').color = 'yellow'
	# extendAddress('01123').color = 'green'
	# extendAddress('10004').color = 'orange'
	# extendAddress('10303').color = 'darkgreen'
	# extendAddress('11032').color = 'lightblue'
	# extendAddress('12032').color = 'lightgreen'
	# extendAddress('12124').color = 'blue'
	# extendAddress('12222').color = 'red'
	# extendAddress('12231').color = 'orange'
	# extendAddress('12241').color = 'darkblue'
	
	# V2 - [14]
	# extendAddress('00001')	
	# extendAddress('00142')	
	# extendAddress('01023')	
	# extendAddress('10003')	
	# extendAddress('10012')	
	# extendAddress('10034')	
	# extendAddress('10344')	
	# extendAddress('11242')	
	# extendAddress('12141')	
	# extendAddress('12303')	
	# extendAddress('12313')	
	
	# Q0 - [12]
	# extendAddress('00011').color = 'red'
	# extendAddress('10102').color = chainColors[1]
	# extendAddress('10012').color = chainColors[2]
	# extendAddress('10233').color = chainColors[3]
	# extendAddress('10143').color = chainColors[4]
	# extendAddress('11102').color = chainColors[5]
	# extendAddress('12144').color = chainColors[6]
	# extendAddress('12234').color = chainColors[7]
	# extendAddress('12334').color = chainColors[8]
	# extendAddress('11013').color = 'orange'
	# extendAddress('11022').color = 'darkorange'	
	# extendAddress('12304').color = 'orange'
	# extendAddress('12322').color = 'darkorange'
	'''
	# Diagonals
	# extendAddress('12304')
	# extendAddress('12244')
	# extendAddress('12104')
	# extendAddress('12004')
	
	#diagram.nodeByAddress['00001'].loop.color = 'red'								
	extendAddress('00001'])					
	
	#diagram.nodeByAddress['10020'].loop.color = 'red'
	#diagram.nodeByAddress['10044'].loop.color = 'purple'
	assert diagram.extendLoop(diagram.nodeByAddress['12121'])					
	
	#diagram.nodeByAddress['10222'].loop.color = 'green'
	assert diagram.extendLoop(diagram.nodeByAddress['10313'])					

	#diagram.nodeByAddress['10110'].loop.color = 'red'
	assert diagram.extendLoop(diagram.nodeByAddress['12211'])					
	
	#diagram.nodeByAddress['10141'].loop.color = 'red'
	assert diagram.extendLoop(diagram.nodeByAddress['00243'])


	#diagram.nodeByAddress['10303'].loop.color = 'red'
	assert diagram.extendLoop(diagram.nodeByAddress['10303'])


	diagram.nodeByAddress['12011'].loop.color = 'salmon'
#	assert diagram.extendLoop(diagram.nodeByAddress['12011'])
	
	diagram.nodeByAddress['02313'].loop.color = 'violet'
#	assert diagram.extendLoop(diagram.nodeByAddress['02313'])	


	diagram.nodeByAddress['02031'].loop.color = 'red'
	
	diagram.nodeByAddress['11331'].loop.color = 'lightblue'
	assert diagram.extendLoop(diagram.nodeByAddress['11113'])	
	'''
#	diagram.nodeByAddress['10041'].loop.color = 'red'
##	diagram.nodeByAddress['10042'].loop.color = 'red'
#	diagram.nodeByAddress['10043'].loop.color = 'red'
#	diagram.nodeByAddress['10044'].loop.color = 'red'
			
	# diagram.nodeByAddress['123015'].loop.color = 'red'			
	# diagram.nodeByAddress['123025'].loop.color = 'red'			
	# diagram.nodeByAddress['123035'].loop.color = 'red'			
	# diagram.nodeByAddress['123045'].loop.color = 'red'			
	# diagram.nodeByAddress['123001'].loop.color = 'orange'			
	# diagram.nodeByAddress['123002'].loop.color = 'yellow'			
	# diagram.nodeByAddress['123003'].loop.color = 'green'			
	# diagram.nodeByAddress['123004'].loop.color = 'blue'			
	# diagram.nodeByAddress['123005'].loop.color = 'violet'			
	# diagram.nodeByAddress['123006'].loop.color = 'indigo'			
	# 
	# node = diagram.nodeByAddress['123005']
	# for i in range(6):
	# 	print(str(node))
	# 	node = node.links[2].next.prevs[1].node
	'''
	assert diagram.extendLoop(diagram.nodeByAddress['123005'])
	diagram.chainColors[diagram.nodeByAddress['123005'].chainID] = 'red'
	assert diagram.extendLoop(diagram.nodeByAddress['123146'])
	assert diagram.extendLoop(diagram.nodeByAddress['123236'])
	assert diagram.extendLoop(diagram.nodeByAddress['123326'])
	assert diagram.extendLoop(diagram.nodeByAddress['123416'])	
	
	
	assert diagram.extendLoop(diagram.nodeByAddress['123025'])
	diagram.chainColors[diagram.nodeByAddress['123025'].chainID] = '#00cc00'
	assert diagram.extendLoop(diagram.nodeByAddress['102026'])
	assert diagram.extendLoop(diagram.nodeByAddress['102116'])	
	assert diagram.extendLoop(diagram.nodeByAddress['013014'])
	assert diagram.extendLoop(diagram.nodeByAddress['103014'])
	assert diagram.extendLoop(diagram.nodeByAddress['013016'])
	assert diagram.extendLoop(diagram.nodeByAddress['013246'])
	assert diagram.extendLoop(diagram.nodeByAddress['013336'])
	assert diagram.extendLoop(diagram.nodeByAddress['013426'])			
	assert diagram.extendLoop(diagram.nodeByAddress['103016'])
	assert diagram.extendLoop(diagram.nodeByAddress['103246'])
	assert diagram.extendLoop(diagram.nodeByAddress['103336'])
	assert diagram.extendLoop(diagram.nodeByAddress['103426'])	
	# assert diagram.extendLoop(diagram.nodeByAddress['102020'])
	# diagram.nodeByAddress['102020'].loop.color = 'indigo'
					
					
	assert diagram.extendLoop(diagram.nodeByAddress['123045'])
	diagram.chainColors[diagram.nodeByAddress['123045'].chainID] = '#00aaff'		
	assert diagram.extendLoop(diagram.nodeByAddress['122046'])
	assert diagram.extendLoop(diagram.nodeByAddress['122136'])	
	assert diagram.extendLoop(diagram.nodeByAddress['023041'])
	assert diagram.extendLoop(diagram.nodeByAddress['113041'])
	assert diagram.extendLoop(diagram.nodeByAddress['023046'])
	assert diagram.extendLoop(diagram.nodeByAddress['023136'])
	assert diagram.extendLoop(diagram.nodeByAddress['023226'])
	assert diagram.extendLoop(diagram.nodeByAddress['023316'])			
	assert diagram.extendLoop(diagram.nodeByAddress['113046'])
	assert diagram.extendLoop(diagram.nodeByAddress['113136'])
	assert diagram.extendLoop(diagram.nodeByAddress['113226'])
	assert diagram.extendLoop(diagram.nodeByAddress['113316'])			
	
	diagram.nodeByAddress['013111'].loop.color = 'violet'
	diagram.nodeByAddress['013112'].loop.color = 'indigo'
	diagram.nodeByAddress['013113'].loop.color = 'pink'	
	'''
	# assert diagram.extendLoop(diagram.nodeByAddress['000001'])
	# 
	# assert diagram.extendLoop(diagram.nodeByAddress['100035'])
	# diagram.chainColors[diagram.nodeByAddress['100035'].chainID] = 'violet'					
	# 
	# assert diagram.extendLoop(diagram.nodeByAddress['100055'])
	# diagram.chainColors[diagram.nodeByAddress['100055'].chainID] = 'pink'								
	# 
	# assert diagram.extendLoop(diagram.nodeByAddress['110004'])
			
	show(diagram)
	return diagram
	#print("=== §§§ ===")

	
if __name__ == "__main__":
	from common import Step, Sol
	diagram = run()
