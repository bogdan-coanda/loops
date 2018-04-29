from diagram import *
from time import time, sleep
from math import floor
import pickle
from functools import cmp_to_key

class Step (object):
	
	def __init__(self, cc, availablesCount, singlesCount, sparksCount, node):
		self.cc = cc
		self.availablesCount = availablesCount
		self.singlesCount = singlesCount
		self.sparksCount = sparksCount
		self.node = node


class Sol (object):
	
	def __init__(self, tdiff, jkcc, state, text, extended):
		self.tdiff = tdiff
		self.jkcc = jkcc
		self.state = state
		self.text = text
		self.extended = extended
		

def tstr(s):
	return "" + str(int(floor(s / 60))) + "m" + str(int(floor(s)) % 60) + "s." + str(int(s * 1000) % 1000)

def dtstr(new, old):
	if new == old:		
		return "@time: " + tstr(new) + " same as before"
	if new < old:
		return "@time: " + tstr(new) + " faster by " + tstr(old - new) + " (" + str(int(100*new/old)) + "%) than " + tstr(old)
	else:
		return "@time: " + tstr(new) + " slower by " + tstr(new - old) + " (" + str(int(100*old/new)) + "%) than " + tstr(old)
		
def jkstr(new, old):
	if new == old:		
		return "@jkcc: " + str(new) + " same as before"
	if new < old:
		return "@jkcc: " + str(new) + " faster by " + str(old - new) + " (" + str(int(100*new/old)) + "%) than " + str(old)
	else:
		return "@jkcc: " + str(new) + " slower by " + str(new - old) + " (" + str(int(100*old/new)) + "%) than " + str(old)

def sstr(state):
	return " ".join([str(step.cc) + "/" + str(step.availablesCount) + (("(" + str(step.singlesCount) + ")") if step.singlesCount > 0 else (("{" + str(step.sparksCount) + "}") if step.sparksCount > 0 else "")) + ":" + str(step.node) for step in state])

def jk(diagram, lvl = 0, state = []):
	
	diagram.jkcc += 1	

	diagram.measureNodes()
	'''
	pq = [
		'123450',
		'450213',
		'354021',
		'021534',
		'534201',
		'210534',
		'412053',	
		'412503', # spark1		
		'205431',	
		'250431', # single
		'431520', # single
		'314025', # spark2	
		'314052', # spark3	
		'230541', # single
		'541320', # single
		'124530', # single
		'304251', # spark4	
		'304521', # spark5	
		'210354', # spark6	
		'124503', # single
		'412035', # single
		'501324', # single
		'501432', # spark7
		'451023'
	]
		
	if ([step.node.perm for step in state][:min(len(state), len(pq))] == pq[:min(len(state), len(pq))]):
# [10328][lvl:24] [state] jk: 10328 | lvl: 24 | » 0/24:[node:123450@00001§0] 0/31:[node:450213@11004§0] 0/31:[node:354021@11044§0] 0/29:[node:021534@11032§0] 0/29:[node:534201@02035§0] 7/27:[node:210534@12032§0] 1/26:[node:412053@01031§0] 0/1{1}:[node:412503@01022§1049] 4/28:[node:205431@01343§0] 0/1(1):[node:250431@01334§1049] 0/1(1):[node:431520@01322§1049] 0/1{3}:[node:314025@10120§1061] 0/1{5}:[node:314052@10111§1062] 0/1(1):[node:230541@00142§0] 0/1(1):[node:541320@02245§0] 0/1(1):[node:124530@00302§0] 0/1{8}:[node:304251@11111§1063] 0/1{8}:[node:304521@11102§1064] 0/1{7}:[node:210354@12041§1065] 0/1(2):[node:124503@01202§1049] 0/1(2):[node:412035@01040§1065] 0/1(1):[node:501324@02105§1049] 0/1{3}:[node:501432@02325§1066] 1/19:[node:451023@10004§0]
# [10328][lvl:24] [drawn] looped: 720 | availables: 5 | singles: 0 | sparks: 0 | unreachables: 0
# | chains: 0 1062 1064 1066 1049 | connected chains: 1061+1065 1061+1063 0+1065 |
# [10328][lvl:24] availables: [node:021453@11301§0] [node:032145@12200§1049] [node:053214@12214§1062] [node:045321@12303§1064] [node:014532@02302§1066]
		'' '
old » [5] lvl: 25 | 
0/24:123450 
0/31:450213 
0/31:354021 
0/29:021534 
0/29:534201 

7/27:210534 
1/26:412053 

5/25:205431 
12/17:451023 
0/1(3):124530 single
0/1(2):351042 spark4:304251
0/1(1):351402 spark2:314025
0/6:235410 spark6:210354
0/1(1):412035 single
4/7:230541 single
0/1(1):541320 single
  0/1:021453 
0/1(4):145032 single:124503
0/1(5):321045 spark5:304521
0/1(4):321405 spark3:314052
0/1(3):450312 spark1:412503
0/1(3):250431 single
0/1(3):431520 single
0/1(2):501324 single
0/1(1):532014 spark7:501432

new » [5] lvl: 25 | 
0/24:[node:123450@00001§0] 
0/31:[node:450213@11004§0] 
0/31:[node:354021@11044§0] 
0/29:[node:021534@11032§0] 
0/29:[node:534201@02035§0] 

14/27:[node:234510@10002§0]
5/18:[node:452103@12004§0] 0/1{4}:[node:032145@12200§1396] 0/1{3}:[node:032415@12110§1397] 0/1(1):[node:532401@02125§1397] 3/29:[node:521043@12315§0] 0/1{3}:[node:405213@11013§1405] 0/1{1}:[node:410523@10022§1406] 0/1(2):[node:215043@12333§0] 0/1(4):[node:451023@10004§0] 0/1(3):[node:451203@01004§0] 0/1(4):[node:431250@01331§0] 0/1(3):[node:431520@01322§0] 0/1(2):[node:532014@02305§1396] 0/1(2):[node:351402@10134§0] 0/1(1):[node:532041@02215§1397] 0/1(1):[node:354102@10044§0] 0/1{4}:[node:405312@01213§1407] 0/6:[node:210453@12301§1396] 0/3:[node:230451@00101§0]'' '
		print()
		diagram.log("lvl:"+str(lvl), "[state] jk: " + str(diagram.jkcc) + " | lvl: " + str(lvl) + " | » " + sstr(state), True)
		diagram.log("lvl:"+str(lvl), "[drawn] looped: " + str(diagram.drawn.looped_count) + " | availables: " + str(len(diagram.drawn.availables)) + " | singles: " + str(len(diagram.drawn.singles)) + " | sparks: " + str(len(diagram.drawn.sparks)) + " | unreachables: " + str(len(diagram.drawn.unreachable_cycles)) + "\n| chains: " + " ".join([str(ch) for ch in diagram.drawn.chains]) + " | connected chains: " + " ".join([str(a) + "+" + str(b) for a, b in diagram.connectedChainPairs if a < b]) + " |", True)# chain starters: " + " ".join([str(node) for node in diagram.chainStarters]))
		diagram.log("lvl:"+str(lvl), "availables: " + " ".join([str(node) for node in diagram.drawn.availables]), True)
		if len(diagram.drawn.singles) > 0:
			diagram.log("lvl:"+str(lvl), "singles: " + " ".join([str(node) for node in diagram.drawn.singles]), True)
		if len(diagram.drawn.sparks) > 0:			
			diagram.log("lvl:"+str(lvl), "sparks: " + " ".join([str(node) for node in diagram.drawn.sparks]), True)
		if len(diagram.drawn.unreachable_cycles) > 0:			
			diagram.log("lvl:"+str(lvl), "unreachables: " + " ".join([str(cycle) for cycle in diagram.drawn.unreachable_cycles]), True)
		#if diagram.jkcc % 100 == 0:
			#sleep(1)
			
		print("assert False")
	'' ' '''				
	if diagram.drawn.looped_count == len(diagram.perms) and len(diagram.drawn.availables) == 0:
			
		tdiff = time() - diagram.startTime
		text = "[" + str(len(diagram.sols)) + "] lvl: " + str(lvl) + " | " +  sstr(state)

		if len(diagram.drawn.chains) != 1:
			#print("\n# [Trojan] # @jkcc: " + str(diagram.jkcc) + " | @time: " + tstr(tdiff) + " » " + text)
			return
		extended = [step.node for step in state]
		diagram.sols.append(Sol(tdiff, diagram.jkcc, state, text, extended))		

		print()
		print("[state] jk: " + str(diagram.jkcc) + " | lvl: " + str(lvl) + " | » " + sstr(state))
		print("[drawn] looped: " + str(diagram.drawn.looped_count) + " | availables: " + str(len(diagram.drawn.availables)) + " | singles: " + str(len(diagram.drawn.singles)) + " | sparks: " + str(len(diagram.drawn.sparks)) + " | unreachable: " + str(len(diagram.drawn.unreachable_cycles)) + " | chains: " + " ".join([str(ch) for ch in diagram.drawn.chains]) + " | connected chains: " + " ".join([str(a) + "+" + str(b) for a, b in diagram.connectedChainPairs if a < b]) + " | chain starters: " + " ".join([str(node) for node in diagram.chainStarters]))					
															
		print()																												
		print("\n# Found # @jkcc: " + str(diagram.jkcc) + " | @time: " + tstr(tdiff) + " » " + text)
		print()
				
		if len(diagram.sols) > len(diagram.knowns):
			with open("sols."+str(diagram.spClass)+".pkl", 'wb') as outfile:
				pickle.dump(diagram.sols, outfile, 0)
			print("[NEW]")
					
		else: # len(diagram.sols) <= len(diagram.knowns):
			known = diagram.knowns[len(diagram.sols) - 1]
			sol = diagram.sols[-1]			
			if known.jkcc == sol.jkcc and known.text == sol.text: # jkcc & text
				print("[SAME] " + dtstr(sol.tdiff, known.tdiff))
			else:
				knownchain = [step.node for step in known.state]
				solchain = [step.node for step in sol.state]
				if set(knownchain) == set(solchain):
					if knownchain == solchain:
						print(">>> [ABSOLUTED] <<<\n" + dtstr(sol.tdiff, known.tdiff) + "\n" + jkstr(sol.jkcc, known.jkcc) + "\nold » " + " ".join([str(node) for node in knownchain]) + "\nnew » " + " ".join([str(node) for node in knownchain]))
					else:
						print(">>> [REORDERED] <<<\n" + dtstr(sol.tdiff, known.tdiff) + "\n" + jkstr(sol.jkcc, known.jkcc) + "\nold » " + " ".join([str(node) for node in knownchain]) + "\nnew » " + " ".join([str(node) for node in solchain]))
				else:
					𝒟 = Diagram(diagram.spClass)
					for step in known.state:
						𝒟.measureNodes()
						node = 𝒟.nodeByPerm[step.node.perm]
						print("𝒟:" + str(𝒟.drawn.looped_count) + " | extending: " + str(node))
						𝒟.extendLoop(node)
						
					np = diagram.startNode
					op = 𝒟.startNode
					pc = 0
					while True:
						if np.perm != op.perm:
							print("[" + str(pc) + "] diverges at " + str(np) + " | " + str(op) + " from " + str(np.prevLink.node) + " | " + str(op.prevLink.node))
							print(">>> !!![DIVERGENT]!!! <<<\n" + dtstr(sol.tdiff, known.tdiff) + "\n" + jkstr(sol.jkcc, known.jkcc) + "\nold » " + known.text + "\nnew » " + sol.text)			
							assert False
						else:
							np = np.nextLink.next
							op = op.nextLink.next
							if np == diagram.startNode:
								print("converges...")
								print(">>> [CONVERGENT] <<<\n" + dtstr(sol.tdiff, known.tdiff) + "\n" + jkstr(sol.jkcc, known.jkcc) + "\nold » " + known.text + "\nnew » " + sol.text)				
								return
						pc += 1
								
		return
					
	if len(diagram.drawn.unreachable_cycles) > 0:
#		diagram.log("lvl:"+str(lvl), "popping for unreachables: " + str(len(diagram.drawn.unreachable_cycles)))
		return
		
	singlesCount = len(diagram.drawn.singles)
	sparksCount = len(diagram.drawn.sparks)
	# [~] if sparks then start new chain
	# take linkedChains(a,b) into account when measuring bros
	if singlesCount > 0:
		availables = [sorted(diagram.drawn.singles, key = cmp_to_key(lambda x, y: 0 if x.perm == y.perm else (1 if x.perm > y.perm else -1)))[0]]
#		diagram.log("lvl:"+str(lvl)+"|singles", " ".join([str(node) for node in diagram.drawn.singles]))
	elif sparksCount > 0:		
		availables = [sorted(diagram.drawn.sparks, key = cmp_to_key(lambda x, y: 0 if x.perm == y.perm else (1 if x.perm > y.perm else -1)))[0]]
#		diagram.log("lvl:"+str(lvl)+"|sparks", " ".join([str(node) for node in diagram.drawn.sparks]))
	else:
		availables = diagram.drawn.availables
#		diagram.log("lvl:"+str(lvl)+"|availables", " ".join([str(node) for node in diagram.drawn.availables]))
		
	availables = [node for node in availables if not node.seen]
	
	lvl_seen = []
			
	# if diagram.jkcc == 2674:
	# 	assert False, "jk: " + str(diagram.jkcc)		
		
	cc = 0

	for node in availables:
		if not node.seen:				
			
##			diagram.measureNodes()
##			lastDrawn = diagram.drawn.clone()
			
			if diagram.extendLoop(node):
#				diagram.log("lvl:"+str(lvl), "pushing by " + str(node))
				jk(diagram, lvl + 1, state + [Step(cc, len(availables), singlesCount, sparksCount, node)])
#				diagram.log("lvl:"+str(lvl), "collapsing back " + str(node))
				diagram.collapseLoop(node)
				
##				diagram.measureNodes()
##				assert lastDrawn == diagram.drawn, str(lastDrawn.looped_count) + " » " + str(diagram.drawn.looped_count)
		
			node.seen = True
			for bro in node.loopBrethren:
				bro.seen = True
			lvl_seen.append(node)				
		cc += 1
		
	for node in lvl_seen:
		node.seen = False
		for bro in node.loopBrethren:
			bro.seen = False
#	diagram.log("lvl:"+str(lvl), "popping normally")
	return			




if __name__ == "__main__":
	
	diagram = Diagram(6)
	diagram.startTime = time()
	diagram.sols = []
	
	# with open('sols.'+str(diagram.spClass)+".pkl", 'wb') as outfile:
	# 	pickle.dump(diagram.sols, outfile, 0)

	with open('sols.'+str(diagram.spClass)+".pkl", 'rb') as infile:
		diagram.knowns = pickle.load(infile)

	for i in range(len(diagram.knowns)):
		if type(diagram.knowns[i]) is tuple:
			diagram.knowns[i] = Sol(diagram.knowns[i][0], diagram.knowns[i][1], [Step(step[0], step[1], step[2], 0, diagram.nodeByPerm[step[3]]) for step in diagram.knowns[i][2]], diagram.knowns[i][3], diagram.knowns[i][4])

	print("knowns: " + str(len(diagram.knowns)))
			
	jk(diagram)
	print("---")


