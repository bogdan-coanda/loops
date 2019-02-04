from diagram import *
from uicanvas import *





if __name__ == "__main__":
	
	diagram = Diagram(6, 0)
	
	def extend(addr):
		assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	
	#extend('00001')		

	
	extend('00005')
	extend('10005')
	extend('10105')
	extend('11005')
	
	n1 = diagram.nodeByAddress['00005']
	n2 = diagram.nodeByAddress['10005']
	n3 = diagram.nodeByAddress['10105']
	n4 = diagram.nodeByAddress['11005']	
	
	extend('00104')
	extend('00204')
	extend('00304')
	
	#extend('00310')
	extend('00311')
	extend('00224')
	extend('00134')
								
	extend('01205')
	extend('01004')
	extend('01104')
	extend('01304')

	extend('02105')
	extend('02004')
	extend('02204')
	extend('02304')
	
	extend('11041')
	
	extend('11102')
	
	extend('11233')
	extend('11324')
	
	extend('12304')
	extend('10301')

	extend('10342')
	
	#extend('11111')
	#extend('10304')

	headset = set(['000', '100', '101', '110'])

	assert len(headset) == 4

	for loop in diagram.loops:
		if loop.availabled:
			if len(set([node.address[0:3] for node in loop.nodes]).intersection(headset)) > 1:
				print(f'breaking {loop}')
				diagram.setLoopUnavailabled(loop) 

	#'''

	diagram.point()
	show(diagram)
	
