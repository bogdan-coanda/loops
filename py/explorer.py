from diagram import *
from time import time
import pickle
from uicanvas import *
from itertools import zip_longest
from types import SimpleNamespace as _

def id(x): return x

def groupby(L, K = id, V = id, G = id, S = id):
	r = {}
	for e in L:
		k = K(e)
		if k not in r.keys():
			r[k] = []
		r[k].append(V(e))
	return S({ k:G(g) for k,g in r.items() })


if __name__ == "__main__":
	from common import Step, Sol
	
	diagram = Diagram(6)
	diagram.loadKnowns()
	diagram.startTime = time()

	# --- superperms --- #
			
	#superperms = [d.generateDiagramForKnownID(ik).superperm() for ik in range(len(d.knowns))]
	#print("Found " + str(len(set(superperms))) + " distinct superperms")
	
	# --- roads --- #
	
	#roads = [diagram.generateDiagramForKnownID(ik).road() for ik in range(12)]#len(diagram.knowns))]
	#print("Found " + str(len(set(roads))) + " distinct roads")	
	
	#with open("roads."+str(diagram.spClass)+".pkl", 'wb') as outfile:
		#pickle.dump(set(roads), outfile, 0)

	#with open('roads.'+str(diagram.spClass)+".pkl", 'rb') as infile:	
		#roads = list(pickle.load(infile))
	#print("Loaded "+str(len(roads))+" unique roads")
	
	'''# --- extenders --- #
	
	extenders = []
	#ec = 0
	for ik in range(len(diagram.knowns)):
		𝒟 = diagram.generateDiagramForKnownID(ik)
#		𝒟.road()
#		if 𝒟.road_is_walked:
		extenders.append(𝒟.extender())
		#ec += 1
		#print(str(ec) + " / " + str(ik+1))
	
	print("Found " + str(len(extenders)) + " distinct extenders")	
	
	with open("extenders."+str(diagram.spClass)+".pkl", 'wb') as outfile:
		pickle.dump(extenders, outfile, 0)	
	'''
	
	with open('extenders.'+str(diagram.spClass)+".pkl", 'rb') as infile:	
		extenders = list(pickle.load(infile))
	print("Loaded "+str(len(extenders))+" extenders")
		
	extenders = [[diagram.nodeByPerm[perm] for perm in extender] for extender in extenders]
	
#	g5 = groupby(extenders, lambda e: len([n for n in e if n.address[-1] == '5']))
	
#	h14 = [e for e in g5[14] if diagram.nodeByPerm['123450'] in e

		# q = []
	# for h in g5[12]:
	# 	e = [n for n in h if n.address[-1] == '5']
	# 	g = groupby(e, 
	# 		K = lambda n: n.address[:-3])
	# 	if len(g) == 3:
	# 		q.append(h)
	# 
			
	#V = [[n for n in e if n.perm != '123450' and n.address[-1] != '5'] for e in h14]
	'''''' # [~] to run

	characters = []
	for i in range(len(extenders)):
		q5 = [n for n in extenders[i] if n.address[-1] == '5']
		q04 = [n for n in extenders[i] if int(n.address[-1]) + int(n.address[-2]) == 4]
		q123 = [[nln for nln in n.loop.nodes if nln.address[-1] == '0'][0] for n in extenders[i] if n.address[-1] is not '5' and int(n.address[-1]) + int(n.address[-2]) is not 4]
		g5 = groupby(q5, K = lambda k: k.address[:2])
		h04 = groupby(q04, K = lambda k: k.address[:2])
		k123 = groupby(q123, K = lambda k: k.address[:2])
		q5=[(k,len(v)) for k,v in g5.items()], 
		q04=[(k,len(v)) for k,v in h04.items()], 
		q123=[(k,len(v)) for k,v in k123.items()],
		characters.append(_(
			index=i,
			q5=q5, 
			q04=q04, 
			q123=q123,
			q={ "q5":q5, "q04":q04, "q123":q123 },
			l5=len(g5), l04=len(h04), l123=len(k123),
			s5=sum([len(v) for k,v in g5.items()]),
			s04=sum([len(v) for k,v in h04.items()]),
			s123=sum([len(v) for k,v in k123.items()]),
			g5=g5, h04=h04, k123=k123
		))
				
	# [±][~] [ch for ch in characters if max([len(v) for v in ch.k123.values()]) == 12][0].index
	# [±][~] show(loadE(extenders[[ch for ch in characters if max([len(v) for v in ch.k123.values()]) == 12 and ch.l123 == 2 and ch.s123 == 13][0].index]))

	g5 = groupby(extenders, lambda e: len([n for n in e if n.address[-1] == '5']))
	print("g5: " + str(sorted(g5.keys())))

	h04 = groupby(extenders, lambda e: len([n for n in e if int(n.address[-1]) + int(n.address[-2]) == 4]))
	print("h04: " + str(sorted(h04.keys())))
			
	k123 = groupby(extenders, lambda e: len([n for n in e if n.address[-1] is not '5' and int(n.address[-1]) + int(n.address[-2]) is not 4]))
	print("k123: " + str(sorted(k123.keys())))
	
	
	g5h04 = groupby(extenders, 
		K = lambda e: len([n for n in e if n.address[-1] == '5']), 
		G = lambda g: groupby(g, 
			K = lambda e: len([n for n in e if int(n.address[-1]) + int(n.address[-2]) == 4])))

	print("g5h04: " + str(sorted(g5h04.keys())))
		
	rows = []
	for i in sorted(g5h04.keys()):
		h04 = sorted(g5h04[i].keys())
		rows.append([str(h04[0] + i), str(h04[-1] + i), str(i), str(h04)])
	rows.sort(key = lambda row: row[1])
	for row in reversed(rows):
		print("tmin: " + str(row[0]) + " | tmax: " + str(row[1]) + " | g5: " + str(row[2]) + " | h04: " + str(row[3]))


	g5k123 = groupby(extenders, 
		K = lambda e: len([n for n in e if n.address[-1] == '5']), 
		G = lambda g: groupby(g, 
			K = lambda e: len([n for n in e if n.address[-1] is not '5' and int(n.address[-1]) + int(n.address[-2]) is not 4])))

	print("g5k123: " + str(sorted(g5k123.keys())))

	rows = []
	for i in sorted(g5k123.keys()):
		k123 = sorted(g5k123[i].keys())
		rows.append([str(k123[0] + i), str(k123[-1] + i), str(i), str(k123)])
	rows.sort(key = lambda row: row[1])
	for row in reversed(rows):
		print("tmin: " + str(row[0]) + " | tmax: " + str(row[1]) + " | g5: " + str(row[2]) + " | k123: " + str(row[3]))

				
	h04k123 = groupby(extenders, 
		K = lambda e: len([n for n in e if int(n.address[-1]) + int(n.address[-2]) == 4]), 
		G = lambda g: groupby(g, 
			K = lambda e: len([n for n in e if n.address[-1] is not '5' and int(n.address[-1]) + int(n.address[-2]) is not 4])))

	print("h04k123: " + str(sorted(h04k123.keys())))

	rows = []
	for i in sorted(h04k123.keys()):
		k123 = sorted(h04k123[i].keys())
		rows.append([str(k123[0] + i), str(k123[-1] + i), str(i), str(k123)])
	rows.sort(key = lambda row: row[1])
	for row in reversed(rows):
		print("tmin: " + str(row[0]) + " | tmax: " + str(row[1]) + " | h04: " + str(row[2]) + " | k123: " + str(row[3]))
		
								
	yg = 0
	yh = 6

	print()
	print("g5h04["+str(yg)+"]["+str(yh)+"].len: " + str(len(g5h04[yg][yh])))
	
	by5 = []
	for ext in g5h04[yg][yh]:
		by5.append(list(reversed(sorted(groupby(groupby([n for n in ext if n.address[-1] is '5'], 
				K = lambda n: n.address[:2], 
				G = lambda g: len(g)).items(), 
			K = lambda k: k[1], 
			G = lambda g: len(g)).items()))))
	
	by04 = []	
	for ext in g5h04[yg][yh]:
		by04.append(list(reversed(sorted(groupby(groupby([n for n in ext if int(n.address[-1]) + int(n.address[-2]) == 4], 
				K = lambda n: n.address[:2], 
				G = lambda g: len(g)).items(), 
			K = lambda k: k[1], 
			G = lambda g: len(g)).items()))))
		
	by123 = []
	for ext in g5h04[yg][yh]:
		by123.append(list(reversed(sorted(groupby(groupby([n for n in ext if n.address[-1] is not '5' and int(n.address[-1]) + int(n.address[-2]) is not 4], 
				K = lambda n: [nln for nln in n.loop.nodes if nln.address[-1] == '0'][0].address[:2], 
				G = lambda g: len(g)).items(), 
			K = lambda k: k[1], 
			G = lambda g: len(g)).items()))))	
		
	yb = 0
	for pair in zip(by5, by04, by123):
		print("# " + str(yb) + " # ".join([str(elem) for elem in pair]))
		yb += 1

	'''
	diagram.measureNodes(diagram.startNode)
	av0 = diagram.drawn.availables
	tree = {}
	for n0 in av0:
		e0 = [e for e in extenders if n0.perm in e]
		diagram.extendLoop(n0)
		diagram.measureNodes(diagram.startNode)
		av1 = diagram.drawn.availables		
		tree[n0.perm] = {}
		for n1 in av1:
			e1 = [e for e in e0 if n1.perm in e]
			diagram.extendLoop(n1)
			diagram.measureNodes(diagram.startNode)
			av2 = diagram.drawn.availables
			tree[n0.perm][n1.perm] = {}
			for n2 in av2:			
				tree[n0.perm][n1.perm][n2.perm] = [e for e in e1 if n2.perm in e]
				if len(tree[n0.perm][n1.perm][n2.perm]) == 0:
					print("No sols found for path: " + n0.perm + " " + n1.perm + " " + n2.perm)
		diagram.collapseLoop(n0)
	'''
	
