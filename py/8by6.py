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
	
	def extendNode(node):
		node.marked = True
		assert diagram.extendLoop(
			sorted(node.loop.nodes, key = lambda n: n.looped).pop()
			if not node.looped and len([n for n in node.loop.nodes if n.looped]) is not 0
			else node)
		for nln in node.loop.nodes:
			nln.color = 𝒞(nln)
		return node.loop		
	
	def extendAddress(address):
		extendNode(diagram.nodeByAddress[address])

	def extendReverse(last):
		return extendNode(last.prevs[1].node)
		
	def collapseNode(node):
		diagram.collapseLoop(node)

	def collapseReverse(last):
		collapseNode(last.prevs[1].node)
				
	def drawBlock(address, reverse = False):
		
		for i in range(diagram.spClass-2): # 0:5
			for j in range(1, diagram.spClass-3): # 1:4
				extendAddress(address + str(i) + str(j) + '0')
			extendAddress(address + str(i) + ('0' if (reverse ^ (i % 2 == 0)) else str(diagram.spClass-3)) + '0') # 0/5

	
	def measure():
		diagram.measureNodes()	
		avs = [node for node in diagram.drawn.availables if len([bro for bro in node.loopBrethren if bro.looped]) == 0 and node.chainID == 1]
		for node in diagram.drawn.availables:
			if node not in avs:
				node.loop.seen = True
		return avs
							
	def look(avs):			
		def mark(val, against=0):
			return str(val) if val is against else "»»» " + str(val) + " «««" 
		g = len([n for n in avs if n.address[-1] == '7'])
		h = len([n for n in avs if int(n.address[-1]) + int(n.address[-2]) == 6])
		k = len(avs) - g - h
		print("           | " + str(len(avs)) + " {"+str(g)+":"+str(h)+":"+str(k)+"}" + " | availables: " + str(len(diagram.drawn.availables)) + " | chains: " + mark(len(diagram.drawn.chains), diagram.spClass-1) + " | singles: " + mark(len(diagram.mx_singles)) + " | sparks: " + mark(len(diagram.mx_sparks)) + " | unreachables: " + mark(len(diagram.mx_unreachable_cycles)))			

										
										
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
	
	#show(diagram)
		
	α = diagram.nodeByAddress['1234040']
	β = diagram.nodeByAddress['1234127']
	γ = diagram.nodeByAddress['1234240']
	δ = diagram.nodeByAddress['1234327']
	ε = diagram.nodeByAddress['1234440']
	ζ = diagram.nodeByAddress['1234527']
		
	nodes = { α: α, β: β, γ: γ, δ: δ, ε: ε, ζ: ζ }		
	
	def extend():
		for n in [α, γ, ε]:
			extendNode(nodes[n])	
		for n in [β, δ, ζ]:
			extendReverse(nodes[n])					
				
	def collapse():
		for n in [α, γ, ε]:
			collapseNode(nodes[n])	
		for n in [β, δ, ζ]:
			collapseReverse(nodes[n])					

	def next():
		for n in [α, γ, ε]:
			nodes[n] = nodes[n].nextLink.next	
		for n in [β, δ, ζ]:
			nodes[n] = nodes[n].prevLink.node				
		
	memory = None
	def remember():
		nonlocal memory
		memory = [len(avs), len(diagram.drawn.availables), len(diagram.drawn.chains), len(diagram.mx_singles), len(diagram.mx_sparks), len(diagram.mx_unreachable_cycles)]
		
	def reminisce():
		assert memory == [len(avs), len(diagram.drawn.availables), len(diagram.drawn.chains), len(diagram.mx_singles), len(diagram.mx_sparks), len(diagram.mx_unreachable_cycles)]	

	
	𝒮 = []
	def extendSkip(skip):
		nonlocal nodes, avs, 𝒮
		nodes = { α: α, β: β, γ: γ, δ: δ, ε: ε, ζ: ζ }
		saux = skip
		avs = measure()			
		while nodes[α] not in avs or skip > 0: # skip mechanism [~]
			if nodes[α] in avs:
				skip -= 1
			next()
		print("### Extending α: " + str(nodes[α]) + " @ skip: " + str(saux))
		𝒮.append((saux, nodes[α]))
		extend()
		
		
	def tryCrash(avs):
		if len(diagram.mx_unreachable_cycles) is not 0:
			print("𝒞rashing for unreachables...")
			look(avs)
			print("𝒮o far: ")
			for i in range(len(𝒮)):
				print("lvl: " + str(i) + " | " + str(𝒮[i]))		
			assert False
		elif len(diagram.mx_singles) is not 0:
			avs = [n for n in avs if n in diagram.mx_singles]
			print("𝒞onstraining for singles to: " + str(len(avs)))
			return avs
		elif len(diagram.mx_sparks) is not 0:
			print("Ignoring for sparks: " + str(len(diagram.mx_sparks)))
		return avs # else
			
			
		
	### [60] [node:21756403@1224055§1|λA]
	#extendSkip(60)
	
	### [65] [node:31725640@0124045§1|λA]
	#extendSkip(65)
	
	### [67] [node:64013725@0214042§1|λA]
	#extendSkip(67)
	
	### [103] [node:01723564@0004035§1|λA]
	#extendSkip(103)
	
	### [24] [node:21506743@1233102§1|λA]
	#extendSkip(24)
	
	
	currs = ""
	
	'''lvl: 0 | (60, [node:21756403@1224055§1|λε])
lvl: 1 | (65, [node:31725640@0124045§1|λε])
lvl: 2 | (67, [node:64013725@0214042§1|λε])
lvl: 3 | (103, [node:01723564@0004035§1|λε])
lvl: 4 | (24, [node:21506743@1233102§1|λε])
lvl: 5 | (30, [node:31520674@0132201§1|λε])
lvl: 6 | (158, [node:41720356@0104025§1|λε])
lvl: 7 | (165, [node:61724035@0122015§1|λε])
lvl: 8 | (37, [node:74152036@0101307§1|λε])
lvl: 9 | (216, [node:72035461@0104117§1|λε])
lvl: 10 | (258, [node:72563401@0003047§1|λε])
lvl: 11 | (147, [node:13726540@0214555§1|λε])
lvl: 12 | (157, [node:65140372@1223551§1|λε])
lvl: 13 | (215, [node:35176240@0122164§1|λε])
lvl: 14 | (289, [node:72356041@0013037§1|λε])
lvl: 15 | (184, [node:64107235@1004033§1|λε])
lvl: 16 | (179, [node:54610723@1004122§1|λε])
lvl: 17 | (103, [node:32761504@1233465§1|λε])
lvl: 18 | (405, [node:70516432@0233137§1|λε])
lvl: 19 | (214, [node:07263541@1004456§1|λε])
lvl: 20 | (126, [node:25406137@0214220§1|λε])
lvl: 21 | (373, [node:75640321@1224057§1|λε])
lvl: 22 | (139, [node:37625401@0214466§1|λε])
lvl: 23 | (311, [node:35760412@0013065§1|λε])
lvl: 24 | (320, [node:56047123@0013023§1|λε])
lvl: 25 | (33, [node:41752036@0101325§1|λε])
lvl: 26 | (146, [node:40371265@0124544§1|λε])
lvl: 27 | (94, [node:27615304@1112466§1|λε])
lvl: 28 | (189, [node:34615072@1001431§1|λε])
lvl: 29 | (4, [node:43216570@1233511§1|λε])
lvl: 30 | (227, [node:61742035@0113015§1|λε])
lvl: 31 | (204, [node:41702635@1004445§1|λε])
lvl: 32 | (197, [node:41072635@1004454§1|λε])
lvl: 33 | (108, [node:61237540@0004233§1|λε])
lvl: 34 | (53, [node:74315026@1032207§1|λε])
lvl: 35 | (105, [node:40621375@1104231§1|λε])
lvl: 36 | (135, [node:71246503@0120537§1|λε])
lvl: 37 | (140, [node:72516403@1223137§1|λε])
lvl: 38 | (230, [node:03651724@0122522§1|λε])'''
		
	#look(measure())
	#for skip, step in [(int(curr.split("(")[1].split(',')[0]), curr.split(' | ')[1]) for curr in currs.split("\n")]:
		#extendSkip(skip)
		#look(tryCrash(measure()))
	#print("Done reloading...")
	### lvl ###	
	
	for qq in range(24):
		nodes = { α: α, β: β, γ: γ, δ: δ, ε: ε, ζ: ζ }
		avs = measure()		
		look(avs)
		
		avs = tryCrash(avs)

		next()
		cc = 0
		maxavs2len = 0
		maxavs2cc = 0
		minavs2len = 9999999
		minavs2cc = 9999999
		maxavailslen = 0
		maxavailscc = 0
		minavailslen = 9999999
		minavailscc = 9999999
		
		while nodes[α] is not α:
			if nodes[α] in avs:
				print("["+str(qq)+"|"+str(cc)+"/"+str(len(avs))+"] "+str(nodes[α]))
				# [~] remember()	
				extend()															
				avs2 = measure()
				
				if len(avs2) > maxavs2len:
					maxavs2len = len(avs2)
					maxavs2cc = cc
				if len(avs2) < minavs2len:
					minavs2len = len(avs2)
					minavs2cc = cc
				if len(diagram.drawn.availables) > maxavailslen:
					maxavailslen = len(diagram.drawn.availables)
					maxavailscc = cc
				if len(diagram.drawn.availables) < minavailslen:
					minavailslen = len(diagram.drawn.availables)
					minavailscc = cc										
					
				look(avs2)
						
				collapse()							
				# [~] measure()
				# [~] reminisce()
				cc += 1
			next()
						
		print("max avs2: " + str(maxavs2len) + " @ " + str(maxavs2cc))
		print("min avs2: " + str(minavs2len) + " @ " + str(minavs2cc))		
		print("max avails: " + str(maxavailslen) + " @ " + str(maxavailscc))
		print("min avails: " + str(minavailslen) + " @ " + str(minavailscc))	
		extendSkip(minavs2cc)
	#skip = 11
	#while nodes[α] not in avs or skip > 0: # skip mechanism [~]
		#if nodes[α] in avs:
			#skip -= 1
		#next()
	
	# remember()	
	# extend()												
	# measure()
	# 
	# collapse()							
	# measure()
	# reminisce()

	print("𝒮o far: ")
	for i in range(len(𝒮)):
		print("lvl: " + str(i) + " | " + str(𝒮[i]))		

	show(diagram)
	return diagram
	
	
if __name__ == "__main__":
	from common import Step, Sol
	diagram = run()
	print("§§§")
