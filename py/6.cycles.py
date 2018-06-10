import ui
from diagram import *
from colorsys import hls_to_rgb
from random import random
from uicanvas import *
from itertools import chain


if __name__ == "__main__":
	
	diagram = Diagram(6)
	diagram.loadExtenders()

	maxlvl = -1

	def qp(lvl=0):
		global maxlvl
		if lvl > maxlvl:
			maxlvl = lvl
			
		show(diagram)
		diagram.measure()
		input()
			
		avs = [loop for loop in diagram.loops if loop.availabled and len([node for node in loop.nodes if node.chainID is not None]) is 0]
		
		for loop in avs:
			
			diagram.extendLoop(loop)
			
			flipped = []
			for ln in loop.nodes:
				for n in ln.cycle.nodes:
					if n.loop.availabled:
						n.loop.availabled = False
						flipped.append(n.loop)
			
			qp(lvl+1)
			
			diagram.collapseLoop(loop)
			for l in flipped:
				l.availabled = True
		
		
	qp()
		
	# loop = diagram.nodeByAddress['00005'].loop	
	# loop.availabled = False
	# for node in loop.nodes:
	# 	node.links[1].next.loop.availabled = False
	
	'''
	diagram.extendLoop(diagram.nodeByAddress['00005'].loop)
	diagram.extendLoop(diagram.nodeByAddress['00022'].loop)
	diagram.extendLoop(diagram.nodeByAddress['00012'].loop)
	diagram.extendLoop(diagram.nodeByAddress['00002'].loop)
	diagram.extendLoop(diagram.nodeByAddress['00042'].loop)
	diagram.extendLoop(diagram.nodeByAddress['00032'].loop)
	'''
	
	show(diagram)
	diagram.measure()
	
	# print(sorted(groupby(diagram.extenders, K = lambda extender: "|".join([str(pair[0])+":"+str(pair[1]) for pair in sorted(groupby(groupby(list(chain(*[[node.cycle for node in loop.nodes] for loop in extender])), G = lambda g: len(g)).items(), K = lambda pair: pair[1], V = lambda pair: pair[0], G = lambda g: len(g)).items(), key = lambda pair: -pair[0])]), G = lambda g: len(g)).items())[::-1])
	# » » » 
	'''
	[
		('3:3|2:17|1:82', 48), ('3:3|2:16|1:84', 32), 
		('3:2|2:20|1:79', 272), ('3:2|2:19|1:81', 224), ('3:2|2:18|1:83', 112), ('3:2|2:17|1:85', 80), 
		('3:1|2:22|1:78', 2528), ('3:1|2:21|1:80', 2416), ('3:1|2:20|1:82', 1376), ('3:1|2:19|1:84', 976), ('3:1|2:18|1:86', 240), ('3:1|2:17|1:88', 128), ('3:1|2:16|1:90', 16), 
		('2:24|1:77', 10560), ('2:23|1:79', 8208), ('2:22|1:81', 7312), ('2:21|1:83', 4784), ('2:20|1:85', 1392), ('2:19|1:87', 1136), ('2:18|1:89', 352), ('2:17|1:91', 16), ('2:16|1:93', 80)
	]
	''' # » » » solutions without tricycles 'should' be easier to find; solutions with more bicycles 'should be easier to find'
	# 𝓖 = groupby(diagram.extenders, K = lambda extender: "|".join([str(pair[0])+":"+str(pair[1]) for pair in sorted(groupby(groupby(list(chain(*[[node.cycle for node in loop.nodes] for loop in extender])), G = lambda g: len(g)).items(), K = lambda pair: pair[1], V = lambda pair: pair[0], G = lambda g: len(g)).items(), key = lambda pair: -pair[0])]))
	# 𝓖['2:24|1:77']
	# groupby(list(chain(*[[node.cycle for node in loop.nodes] for loop in 𝓖['2:24|1:77'][0]])), G = lambda g: len(g), S = lambda s: [pair[0] for pair in s.items() if pair[1] is 2])
	# "|".join([str(pair[0])+":"+str(pair[1]) for pair in sorted(groupby([pair for pair in groupby(list(chain(*[loop.nodes for loop in 𝓖['2:24|1:77'][0]])), K = lambda node: node.cycle).items() if len(pair[1]) is 2], K = lambda pair: (int(pair[1][0].address[-1]) - int(pair[1][1].address[-1])) % diagram.spClass, G = lambda g: len(g)).items())[::-1]])
	# 𝒽 = groupby(𝓖['2:24|1:77'], K = lambda extender: "|".join([str(pair[0])+":"+str(pair[1]) for pair in sorted(groupby([pair for pair in groupby(list(chain(*[loop.nodes for loop in extender])), K = lambda node: node.cycle).items() if len(pair[1]) is 2], K = lambda pair: (int(pair[1][0].address[-1]) - int(pair[1][1].address[-1])) % diagram.spClass, G = lambda g: len(g)).items())[::-1]]))
	'''
	[
		'4:10|3:10|2:4', '4:10|3:11|2:3', '4:10|3:4|2:10', '4:10|3:5|2:9', '4:10|3:6|2:8', '4:10|3:7|2:7', '4:10|3:8|2:6', '4:10|3:9|2:5', 
		'4:11|3:10|2:3', '4:11|3:11|2:2', '4:11|3:4|2:9', '4:11|3:5|2:8', '4:11|3:6|2:7', '4:11|3:7|2:6', '4:11|3:8|2:5', '4:11|3:9|2:4', 
		'4:12|3:4|2:8', '4:12|3:5|2:7', '4:12|3:6|2:6', '4:12|3:7|2:5', '4:12|3:8|2:4', '4:12|3:9|2:3', 
		'4:13|3:4|2:7', '4:13|3:5|2:6', '4:13|3:6|2:5', '4:13|3:7|2:4', '4:13|3:8|2:3', 
		'4:14|3:2|2:8', '4:14|3:5|2:5', '4:14|3:8|2:2', 
		'4:15|3:4|2:5', '4:15|3:6|2:3', 
		'4:2|3:11|2:11', '4:2|3:8|2:14', 
		'4:3|3:10|2:11', '4:3|3:11|2:10', '4:3|3:6|2:15', '4:3|3:8|2:13', '4:3|3:9|2:12', 
		'4:4|3:10|2:10', '4:4|3:11|2:9', '4:4|3:12|2:8', '4:4|3:7|2:13', '4:4|3:8|2:12', '4:4|3:9|2:11', 
		'4:5|3:10|2:9', '4:5|3:11|2:8', '4:5|3:12|2:7', '4:5|3:4|2:15', '4:5|3:5|2:14', '4:5|3:6|2:13', '4:5|3:7|2:12', '4:5|3:8|2:11', '4:5|3:9|2:10', 
		'4:6|3:10|2:8', '4:6|3:11|2:7', '4:6|3:12|2:6', '4:6|3:5|2:13', '4:6|3:6|2:12', '4:6|3:7|2:11', '4:6|3:8|2:10', '4:6|3:9|2:9', 
		'4:7|3:10|2:7', '4:7|3:11|2:6', '4:7|3:12|2:5', '4:7|3:4|2:13', '4:7|3:5|2:12', '4:7|3:6|2:11', '4:7|3:7|2:10', '4:7|3:8|2:9', '4:7|3:9|2:8', 
		'4:8|3:10|2:6', '4:8|3:11|2:5', '4:8|3:12|2:4', '4:8|3:2|2:14', '4:8|3:4|2:12', '4:8|3:5|2:11', '4:8|3:6|2:10', '4:8|3:7|2:9', '4:8|3:8|2:8', '4:8|3:9|2:7', 
		'4:9|3:10|2:5', '4:9|3:11|2:4', '4:9|3:4|2:11', '4:9|3:5|2:10', '4:9|3:6|2:9', '4:9|3:7|2:8', '4:9|3:8|2:7', '4:9|3:9|2:6'
	]
	'''
	# 𝒽 = groupby(𝓖['2:24|1:77'], K = lambda extender: "|".join([str(pair[0])+":"+str(pair[1]) for pair in sorted(groupby([pair for pair in groupby(list(chain(*[loop.nodes for loop in extender])), K = lambda node: node.cycle).items() if len(pair[1]) is 2], K = lambda pair: ((int(pair[1][0].address[-1]) - int(pair[1][1].address[-1])) % diagram.spClass) % 2, G = lambda g: len(g)).items())[::-1]]), G = lambda g: len(g))
	'''
	[
		('1:2|0:22', 16), 
		('1:4|0:20', 128), 
		('1:5|0:19', 448), 
		('1:6|0:18', 1440), 
		('1:7|0:17', 1664), 
		('1:8|0:16', 2528), 
		('1:9|0:15', 2864),
		('1:10|0:14', 1168), 
		('1:11|0:13', 208), 
		('1:12|0:12', 96)
	]
	'''
	# 𝒽 = groupby(diagram.extenders, K = lambda extender: "|".join([str(pair[0])+":"+str(pair[1]) for pair in sorted(groupby([pair for pair in groupby(list(chain(*[loop.nodes for loop in extender])), K = lambda node: node.cycle).items() if len(pair[1]) is 2], K = lambda pair: ((int(pair[1][0].address[-1]) - int(pair[1][1].address[-1])) % diagram.spClass) % 2, G = lambda g: len(g)).items())[::-1]]), G = lambda g: len(g))
	'''
[
	('1:1|0:17', 16), ('1:1|0:19', 16), ('1:1|0:21', 16), 
	('1:2|0:14', 16), ('1:2|0:16', 32), ('1:2|0:17', 16), ('1:2|0:19', 48), ('1:2|0:20', 32), ('1:2|0:22', 16), 
	('1:3|0:13', 16), ('1:3|0:15', 32), ('1:3|0:16', 96), ('1:3|0:17', 64), ('1:3|0:18', 160), ('1:3|0:19', 16), 
	('1:4|0:12', 16), ('1:4|0:13', 64), ('1:4|0:14', 48), ('1:4|0:15', 176), ('1:4|0:16', 272), ('1:4|0:17', 352), ('1:4|0:18', 448), ('1:4|0:19', 240), ('1:4|0:20', 128), 
	('1:5|0:11', 32), ('1:5|0:12', 16), ('1:5|0:13', 80), ('1:5|0:14', 368), ('1:5|0:15', 480), ('1:5|0:16', 880), ('1:5|0:17', 960), ('1:5|0:18', 576), ('1:5|0:19', 448), 
	('1:6|0:11', 80), ('1:6|0:12', 144), ('1:6|0:13', 416), ('1:6|0:14', 480), ('1:6|0:15', 1216), ('1:6|0:16', 1536), ('1:6|0:17', 1136), ('1:6|0:18', 1440), 
	('1:7|0:11', 224), ('1:7|0:12', 464), ('1:7|0:13', 672), ('1:7|0:14', 1504), ('1:7|0:15', 1936), ('1:7|0:16', 1808), ('1:7|0:17', 1664), ('1:7|0:9', 16), 
	('1:8|0:10', 80), ('1:8|0:11', 352), ('1:8|0:12', 400), ('1:8|0:13', 1696), ('1:8|0:14', 1824), ('1:8|0:15', 1968), ('1:8|0:16', 2528), ('1:8|0:8', 16), ('1:8|0:9', 16), 
	('1:9|0:10', 240), ('1:9|0:11', 368), ('1:9|0:12', 720), ('1:9|0:13', 1792), ('1:9|0:14', 1360), ('1:9|0:15', 2864), ('1:9|0:7', 16), ('1:9|0:8', 64), ('1:9|0:9', 16),	
	('1:10|0:10', 176), ('1:10|0:11', 432), ('1:10|0:12', 880), ('1:10|0:13', 784), ('1:10|0:14', 1168), ('1:10|0:7', 32), ('1:10|0:8', 32), ('1:10|0:9', 144), 
	('1:11|0:10', 128), ('1:11|0:11', 304), ('1:11|0:12', 288), ('1:11|0:13', 208), ('1:11|0:8', 32), ('1:11|0:9', 32), 
	('1:12|0:10', 48), ('1:12|0:11', 48), ('1:12|0:12', 96), ('1:12|0:7', 16), ('1:12|0:8', 64), ('1:12|0:9', 32), 
	('1:13|0:6', 16), ('1:13|0:7', 16), ('1:13|0:8', 16), ('1:13|0:9', 32), 
	('1:14|0:7', 16), ('1:14|0:8', 16)
]
	'''
