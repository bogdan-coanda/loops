from diagram import *
from uicanvas import *
from extension_result import *
from common import *
import itertools


def extend(addr):
	loop = diagram.nodeByAddress[addr].loop
	return diagram.extendLoop(loop)
	

if __name__ == "__main__":
	
	diagram = Diagram(5, 1)
	
	extend('0001') # 0
	
	# extend('1003') # 1: 0/2
	# extend('1021') # 2!
	# extend('1131') # 3!
	
	extend('1104') # 1: 1/2
	extend('1033') # 2!
	extend('1234') # 3!
	
	
	
	
	show(diagram)
	
