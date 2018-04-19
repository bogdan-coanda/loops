from diagram import *
from time import time
from math import floor
import pickle
from functools import cmp_to_key


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

def jk(diagram, lvl = 0, state = []):
					
	diagram.jkcc += 1	

	diagram.measureNodes()
	
	if diagram.drawn.looped_count == len(diagram.perms):
		tdiff = time() - diagram.startTime
		text = "[" + str(len(diagram.sols)) + "] lvl: " + str(lvl) + " | " + " ".join([str(pair[0]) + "/" + str(pair[1]) + (("(" + str(pair[2]) + ")") if pair[2] > 0 else "") + ":" + pair[3] for pair in state])
		extended = [pair[3] for pair in state]
		diagram.sols.append((tdiff, diagram.jkcc, state, text, extended))
		print("\n# Found # @jkcc: " + str(diagram.jkcc) + " | @time: " + tstr(tdiff) + " » " + text)
		
		if len(diagram.sols) > len(diagram.knowns):
			with open("sols."+str(diagram.spClass)+".pkl", 'wb') as outfile:
				pickle.dump(diagram.sols, outfile, 0)
			print("[NEW]")
					
		else: # len(diagram.sols) <= len(diagram.knowns):
			known = diagram.knowns[len(diagram.sols) - 1]
			sol = diagram.sols[-1]			
			if known[1] == sol[1] and known[3] == sol[3]: # jkcc & text
				print("[SAME] " + dtstr(sol[0], known[0]))
			else:
				knownchain = [e.split(':')[1] for e in known[3].split(' ')[4:]]
				solchain = [e.split(':')[1] for e in sol[3].split(' ')[4:]]
				if set(knownchain) == set(solchain):
					if knownchain == solchain:
						print(">>> [ABSOLUTED] <<<\n" + dtstr(sol[0], known[0]) + "\n" + jkstr(sol[1], known[1]) + "\nold » " + " ".join([e.split(':')[0] for e in known[3].split(' ')[4:]]) + "\nnew » " + " ".join([e.split(':')[0] for e in sol[3].split(' ')[4:]]))
					else:
						print(">>> [REORDERED] <<<\n" + dtstr(sol[0], known[0]) + "\n" + jkstr(sol[1], known[1]) + "\nold » " + ":".join(knownchain) + "\nnew » " + ":".join(solchain))
				else:
					print(">>> !!![DIVERGENT]!!! <<<\n" + dtstr(sol[0], known[0]) + "\n" + jkstr(sol[1], known[1]) + "old » " + known[3] + "\nnew » " + sol[3])
					assert False
		
		return
		
	if diagram.drawn.unreachable_cycle_count > 0:
#		print("[lvl:"+str(lvl)+"] popping for unreachables: " + str(diagram.drawn.unreachable_cycle_count))
		return
		
	singlesCount = len(diagram.drawn.singles)
	availables = [sorted(diagram.drawn.singles, key = cmp_to_key(lambda x, y: 0 if x.perm == y.perm else (1 if x.perm > y.perm else -1)))[0]] if singlesCount > 0 else diagram.drawn.availables
	availables = [node for node in availables if not node.seen]
	lvl_seen = []
	
#	print("[lvl:"+str(lvl)+"] availables: " + " ".join([node.perm for node in availables]))
	
	cc = 0
	for node in availables:
		if not node.seen:
			
			if diagram.extendLoop(node):
#				print("[lvl:"+str(lvl)+"] pushing by " + node.perm)
				jk(diagram, lvl + 1, state + [(cc, len(availables), singlesCount, node.perm)])
				diagram.collapseLoop(node)

			node.seen = True
			for bro in node.loopBrethren:
				bro.seen = True
			lvl_seen.append(node)				
		cc += 1
		
	for node in lvl_seen:
		node.seen = False
		for bro in node.loopBrethren:
			bro.seen = False
#	print("[lvl:"+str(lvl)+"] popping normally")
	return			




if __name__ == "__main__":
	
	diagram = Diagram(6)
	diagram.startTime = time()
	diagram.sols = []
	
	# with open('sols.'+str(diagram.spClass)+".pkl", 'wb') as outfile:
	# 	pickle.dump(diagram.sols, outfile, 0)

	with open('sols.'+str(diagram.spClass)+".pkl", 'rb') as infile:
		diagram.knowns = pickle.load(infile)

	print("knowns: " + str(len(diagram.knowns)))
			
	jk(diagram)
	print("---")


