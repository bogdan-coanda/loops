import ui
from diagram import *



def show(diagram):
	with ui.ImageContext(diagram.W, diagram.H) as ctx:
	
		ui.set_color('white')
		ui.fill_rect(0, 0, diagram.W, diagram.H)
		
		for node in diagram.nodes:
			
			oval = ui.Path.oval(node.px - 32, node.py - 32, 64, 64)

			ui.set_color('yellow')
			oval.fill()

			ui.set_color('black')
			oval.line_width = 64
			oval.set_line_dash([8,8.8])
			oval.stroke()

		img = ctx.get_image()
		img.show()
		
def run():
	diagram = Diagram(7)
			
	jkinit(diagram)
	show(diagram)
	
	print("=== §§§ ===")

	
if __name__ == "__main__":
	from common import Step, Sol
	run()
