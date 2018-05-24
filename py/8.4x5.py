from diagram import *
from jk import *

def 𝒞(node):
	if node.address[-1] == '7':
		return 'deepskyblue'
	elif int(node.address[-1]) + int(node.address[-2]) == 6:
		if node.address[-1] in ['0', '6']:
			return 'green'#'#99ff99'
		else:
			return 'limegreen'
	else:
		if node.address[-1] in ['0', '6']:
			return 'darkred'#'#ffbbbb'
		else:
			return 'red'
			
			
def run():
	diagram = Diagram(8)
	
	def extendAddress(address):
		node = diagram.nodeByAddress[address]
		assert diagram.extendLoop(
			sorted(node.loop.nodes, key = lambda n: n.looped).pop()
			if not node.looped and len([n for n in node.loop.nodes if n.looped]) is not 0
			else node)
		for nln in node.loop.nodes:
			nln.color = 𝒞(nln)
		return node.loop


	def drawBlock(address, reverse = False):
		
		for i in range(diagram.spClass-2): # 0:5
			for j in range(1, diagram.spClass-3): # 1:4
				extendAddress(address + str(i) + str(j) + '0')
			extendAddress(address + str(i) + ('0' if (reverse ^ (i % 2 == 0)) else str(diagram.spClass-3)) + '0') # 0/5

	# run. #

	extendAddress('0000001')

	'''									
	drawBlock('1234')
	
	extendAddress('1233107')
	extendAddress('1233006')
	extendAddress('1233206')
	extendAddress('1233306')
	extendAddress('1233406')
		
	extendAddress('1230407')
	extendAddress('1230106')
	extendAddress('1230206')
	extendAddress('1230306')
	extendAddress('1230506')
		
	extendAddress('1203207')
	extendAddress('1203106')
	extendAddress('1203306')
	extendAddress('1203406')
	extendAddress('1203506')
	
	extendAddress('1024107')
	extendAddress('1024006')
	extendAddress('1024206')
	extendAddress('1024406')
	extendAddress('1024506')
	
	extendAddress('0234307')
	extendAddress('0234006')
	extendAddress('0234106')
	extendAddress('0234206')
	extendAddress('0234406')
	
	extendAddress('0134407')
	extendAddress('0134006')
	extendAddress('0134106')
	extendAddress('0134306')
	extendAddress('0134506')
	
	extendAddress('1233001')
	extendAddress('1203101')
	extendAddress('0134301')
	extendAddress('1230565')
	extendAddress('0234465')
	extendAddress('1024265')'''
		
	
	# diagram.nodeByAddress["1202215"].loop.color = 'red'
	
		
	show(diagram)
	return diagram
	
	
if __name__ == "__main__":
	from common import Step, Sol
	diagram = run()
	print("§§§")
