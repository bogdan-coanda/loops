from diagram import *
from time import time
from math import floor
import pickle
from functools import cmp_to_key

def tstr(s):
	return "" + str(int(floor(s / 60))) + "m" + str(int(floor(s)) % 60) + "s." + str(int(s * 1000) % 1000)


def jk(diagram, lvl = 0, state = []):
					
	diagram.jkcc += 1	

	diagram.measureNodes()
	
	if diagram.drawn.looped_count == len(diagram.perms):
		tdiff = time() - diagram.startTime
		text = "[" + str(len(diagram.sols)) + "] lvl: " + str(lvl) + " | " + " ".join([str(pair[0]) + "/" + str(pair[1]) + (("(" + str(pair[2]) + ")") if pair[2] > 0 else "") + ":" + pair[3] for pair in state])
		diagram.sols.append((tdiff, diagram.jkcc, state, text))
		print("!!!Found!!! @jkcc: " + str(diagram.jkcc) + " | @time: " + tstr(tdiff) + " » " + text)
		
		if len(diagram.sols) > len(diagram.knowns):
			with open("sols."+str(diagram.spClass)+".pkl", 'wb') as outfile:
				pickle.dump(diagram.sols, outfile, 0)
			print("[NEW]")
					
		else: # len(diagram.sols) <= len(diagram.knowns):
			known = diagram.knowns[len(diagram.sols) - 1]
			sol = diagram.sols[-1]
			if known[1] == sol[1] and known[3] == sol[3]:
				print("[SAME] " + (("faster by " + tstr(known[0] - sol[0])) if sol[0] < known[0] else ("slower by " + tstr(sol[0] - known[0]))))
			else:
				print(">>> [DIVERGENT] <<<\nold jkcc: " + str(known[1]) + " » " + known[3] + "\nnew jkcc: " + str(sol[1]) + " » " + sol[3])
		
		return
		
	if diagram.drawn.unreachable_cycle_count > 0:
		return
		
	singlesCount = len(diagram.drawn.singles)
	availables = [sorted(diagram.drawn.singles, key = cmp_to_key(lambda x, y: 0 if x.perm == y.perm else (1 if x.perm > y.perm else -1)))[0]] if singlesCount > 0 else diagram.drawn.availables
	lvl_seen = []
	
	cc = 0
	for node in availables:
		if not node.seen:
			
			if diagram.extendLoop(node):
				jk(diagram, lvl + 1, state + [(cc, len(availables), singlesCount, node.perm)])
				diagram.collapseLoop(node)

			node.seen = True
			lvl_seen.append(node)				
		cc += 1
		
	for node in lvl_seen:
		node.seen = False
	return			




if __name__ == "__main__":
	
	diagram = Diagram(6)
	diagram.startTime = time()
	diagram.sols = []
	
#	with open('sols.'+str(diagram.spClass)+".pkl", 'wb') as outfile:
#		pickle.dump(diagram.sols, outfile, 0)

	with open('sols.'+str(diagram.spClass)+".pkl", 'rb') as infile:
		diagram.knowns = pickle.load(infile)

	print("knowns: " + str(len(diagram.knowns)))
			
	jk(diagram)
	print("---")


