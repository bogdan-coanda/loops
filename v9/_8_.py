from diagram import *
from uicanvas import *
from common import *
from measurement import *
from itertools import chain
from time import time
from collections import defaultdict
from random import *


if __name__ == "__main__":
	
	diagram = Diagram(8, 1)
	loop = diagram.nodeByAddress['0000001'].loop
	
	print(sorted(loop.killingField(), key = lambda l: (l.ktype, l.ktype_radialIndex)))
	
	diagram.extendLoop(loop)
	
	print(sorted(loop.extension_result.affected_loops, key = lambda l: (l.ktype, l.ktype_radialIndex)))
	
	grx = sorted(groupby([l for l in diagram.loops if l.availabled], K = lambda l: len(l.killingField()), G = lambda g: len(g)).items())
	print("grx: ("+str(len(grx))+")\n"+"\n".join([str(x[0])+":"+str(x[1]) for x in grx]))
	
	show(diagram)
