from diagram import *
from jk import *

def 𝒞(node):
	if node.address[-1] == '6':
		return 'deepskyblue'
	elif int(node.address[-1]) + int(node.address[-2]) == 5:
		if node.address[-1] in ['0', '5']:
			return 'green'#'#99ff99'
		else:
			return 'limegreen'
	else:
		if node.address[-1] in ['0', '5']:
			return 'darkred'#'#ffbbbb'
		else:
			return 'red'
			
			
def run():
	diagram = Diagram(7)
	
	def extendAddress(address):
		node = diagram.nodeByAddress[address]
		assert diagram.extendLoop(
			sorted(node.loop.nodes, key = lambda n: n.looped).pop()
			if not node.looped and len([n for n in node.loop.nodes if n.looped]) is not 0
			else node)
		for nln in node.loop.nodes:
			nln.color = 𝒞(nln)
		return node.loop
				
	extendAddress("123040")

	extendAddress("123130")
				
	extendAddress("123220")

	extendAddress("123310")

	extendAddress("123400")
	
	# ~~~~~~~~~~~~~~~~~~~	#
	
	# extendAddress("103106")
	# extendAddress("113406")
	# extendAddress("102206")
	# extendAddress("122406")
	# extendAddress("023406")
	# extendAddress("013106")
	
	show(diagram)
	return diagram
	
	
if __name__ == "__main__":
	from common import Step, Sol
	diagram = run()
