import ui
from diagram import *



def show(diagram):
	with ui.ImageContext(diagram.W, diagram.H) as ctx:
	
		ui.set_color('white')
		ui.fill_rect(0, 0, diagram.W, diagram.H)
		
		for node in diagram.nodes:
			
			RR = 8
			DH = 4
			
			oval = ui.Path.oval(node.px - RR/2, node.py - RR/2, RR, RR)

			if node.looped:				
				if node.chainID is 0 or diagram.areConnected(0, node.chainID):
					ui.set_color('#ffdd22')
				elif node.chainID is 1 or diagram.areConnected(1, node.chainID):
					ui.set_color('red')
				else:
					ui.set_color(diagram.chainColors.get(node.chainID) or ('#00dd00' if node.chainID % 2 == 1 else '#0077ff'))
			else:
				ui.set_color('white')
			oval.fill()

			if node.loop.color is not None:	
				# marked
				ui.set_color(node.loop.color)
				oval.line_width = 6*DH
				oval.set_line_dash([1,1.05])			
			elif node.extended:
				ui.set_color('red')				
				oval.line_width = DH
				oval.set_line_dash([1,1.05])			
			elif node.loop.availabled:
				ui.set_color('black')				
				oval.line_width = DH
				oval.set_line_dash([1,1.05])			
			else:
				oval.line_width = 0.2
				oval.set_line_dash([1,0])
			oval.stroke()

		img = ctx.get_image()
		img.show()
		
		
def run():
	diagram = Diagram(7)
			
	jkinit(diagram)
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
	
	print("=== §§§ ===")

	
if __name__ == "__main__":
	from common import Step, Sol
	run()
