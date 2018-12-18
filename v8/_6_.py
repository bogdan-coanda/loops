from diagram import *
from uicanvas import *
from common import *
from measurement import *
from itertools import chain




if __name__ == "__main__":
	
	diagram = Diagram(6,1)
	show(diagram)
	
	mx = Measurement(diagram)
	print(mx)
