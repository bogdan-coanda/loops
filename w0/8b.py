from diagram import *
from uicanvas import *
from common import *
from mx import *


max_lvl_reached = 0


def step(avloops, jump_lvl, jump_path, step_lvl=0, step_path=[]):
	
	def key():
		return f"[{tstr(time() - startTime):>11}][lvl:{jump_lvl}»{step_lvl}]"
		
	print(f"{key()}[ch:{len(diagram.chains)}|av:{len(avloops)}] {'.'.join([(str(x)+upper(t)) for x,t in jump_path])}\n» {'.'.join([(str(x)+upper(t)) for x,t in step_path])}")

	if len(diagram.chains) == 1:
		show(diagram)
		input2(f"{key()} sol found.")
		return
		
	min_chain = sorted(diagram.chains, key = lambda chain: (len(chain.avnodes), chain.id))[0]
	# print(f"{key()} chosen min: {min_chain}")
	
	seen = []
	min_avlen = len(min_chain.avnodes)
	
	for i,n in enumerate(sorted(min_chain.avnodes, key = lambda n: n.address)):
		assert diagram.extendLoop(n.loop)		
		step([l for l in avloops if l.availabled], jump_lvl, jump_path, step_lvl+1, step_path+[(i, min_avlen)])
		diagram.collapseBack(n.loop)	
		
		seen.append(n.loop)
		diagram.setLoopUnavailabled(n.loop)
		
	for l in seen:
		diagram.setLoopAvailabled(l)
	

def jump(avtuples, lvl=0, path=[]):
	
	def key():
		return f"[{tstr(time() - startTime):>11}][lvl:{lvl}]" 
	
	print(f"{key()} {'.'.join([(str(x)+upper(t)) for x,t in path])}")
	
	min_chlen = mx.min_chain_avloops_length()	
	print(f"{key()}[mx] 1. min_chlen: {min_chlen}")	
	
	if min_chlen == 0:
		print(f"{key()}[mx] ⇒ dead @ unconnectable")
		return
		
	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"{key()}[mx] 2. unicycle chains: {len(unicycle_chains)}")	
		
	if len(unicycle_chains) == 0:
		print(f"{key()}[mx] ⇒ all cycles covered by tuples")
		step([l for l in diagram.loops if l.availabled], lvl, path)
		input2(f"[jump] « [step] // cc")
		return			
		
	avtuples = mx.filter_avtuples(avtuples)	
	print(f"{key()}[mx] 3. avtuples: {len(avtuples)} / {len(diagram.loop_tuples)}")	

	if len(avtuples) == 0:
		print(f"{key()}[mx] ⇒ no tuples remaining")
		step([l for l in diagram.loops if l.availabled], lvl, path)
		input2(f"[jump] « [step] // nt")
		return			
				
	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"{key()}[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")		

	if len(min_nodes) == 0:
		print(f"{key()}[mx] ⇒ dead @ not coverable")
		return
		
	if lvl < 12 and len(min_nodes) > 1:
		print(f"{key()}[mx] ⇒ not single choice, purging…")
		
		# [~] next_single_choices is unused ?
		avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
		print(f"{key()}[mx][purge] avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

		if len(avtuples) == 0:
			print(f"{key()}[mx][purge] ⇒ no tuples remaining")
			step([l for l in diagram.loops if l.availabled], lvl, path)
			input2(f"[jump] « [step] // nt")
			return			
												
		min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)
		print(f"{key()}[mx][purge] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
	else:
		print(f"{key()}[mx] ⇒ single choice.")
		pass
		
	# go through all choices
	for it, t in enumerate(min_matched_tuples):
		if t in avtuples: # [~][!] needed if no purge
						
			ec = 0
			for lt, l in enumerate(t):
				if diagram.extendLoop(l):
					ec += 1
				else:
					break
	
			if ec == len(t): # if we've extended all of the tuple's loops
				jump(avtuples, lvl+1, path+[(it,len(min_matched_tuples))])
	
			for l in reversed(t[:ec]):
				diagram.collapseBack(l)	
				
			# remove tested choice for further jumps		
			avtuples.remove(t)

	print(f"{key()} ⇒ finished all choices")


def leap(lvl=0, path=[]):
	global max_lvl_reached
	
	def key():
		return f"[{tstr(time() - startTime):>11}][lvl:{lvl}]" 
	
	print(f"{key()} {'.'.join([(str(x)+upper(t)) for x,t,_ in path])}")
	
	# basic check
	min_chlen = min([len(chain.avnodes) for chain in diagram.chains])
	if min_chlen == 0:
		return
		
	# save
	if lvl >= max_lvl_reached:
		with open('8b-leaps_reached_3', 'a', encoding="utf8") as log:
			if lvl > max_lvl_reached:
				log.write("-------------------------" + "\n\n")
			log.write(f"{key()} {'.'.join([(str(x)+upper(t)) for x,t,_ in path])}" + "\n")
			log.write(f"columns: {' '.join([c for _,_,c in path])}" + "\n\n")
			max_lvl_reached = lvl
		
	# purge
		
	unavailed = []
	avcolumns = []
	nextavlen = {}
	
	for ic, column in enumerate(diagram.columns):
		if column.isAvailabled():
			
			extended = []
			for tuple in column.tuples:
				for loop in tuple:
					if diagram.extendLoop(loop):
						extended.append(loop)
					else:
						break
				if len(extended) % (diagram.spClass - 2) != 0:
					break
					
			if len(extended) != len(column.tuples) * (diagram.spClass - 2) or len([ch for ch in diagram.chains if len(ch.avnodes) == 0]) > 0:
				unavailed.append(column)
				column.unavailabled = True
			else:
				nextavlen[column.firstNode.address] = len([col for col in diagram.columns if col.isAvailabled()])
				avcolumns.append(column)						
																	
			for loop in reversed(extended):
				diagram.collapseBack(loop)					
	
	# for each remaining
	
	avcolumns = sorted(avcolumns, key = lambda c: (-nextavlen[c.firstNode.address], c.firstNode.address))
	print(f"{key()} avcolumns: {len(avcolumns)}")
	for ic, column in enumerate(avcolumns):
				
		extended = []
		for tuple in column.tuples:
			for loop in tuple:
				if diagram.extendLoop(loop):
					extended.append(loop)
				else:
					break
			if len(extended) % (diagram.spClass - 2) != 0:
				break
				
		assert len(extended) == len(column.tuples) * (diagram.spClass - 2)
			
		print(f"{key()} extended: {column}")
		leap(lvl+1, path+[(ic, len(avcolumns), column.firstNode.address)])
					
		for loop in reversed(extended):
			diagram.collapseBack(loop)							
		
		unavailed.append(column)
		column.unavailabled = True
		
	for column in unavailed:
		column.unavailabled = False
	
	
	
if __name__ == "__main__":

	diagram = Diagram(8, 1)			
	mx = MX(diagram)
		
	import enav
	enav.diagram = diagram
	from enav import *	
	
	input2('∘')
	
	# ∘ bases ∘ ['0000001', '0000002', '0000003', '0000012', '0000013', '0000021', '0000022', '0000044', '0000045', '0000053', '0000054', '0000063', '0000064', '0000065'] ∘ #
	extend('0000001'); ot()
	
	# x0 = et('0000001') # {0:a}	
	# x0 = et('0000002') # {1:b}
	# x1 = et('0000064') # {0:y}	
	# x1 = et('0000065') # {1:z}
	
	# x0 = et('0000003') # {0:c}
	# x1 = et('0000063') # {1:x}		
	# et('0000012') # {0:p0}
	# et('0000013') # {1:p1}	
	# et('0000021') # {0:p2}
	# et('0000022') # {1:p3}
	# et('0000044') # {0:q3}
	# et('0000045') # {1:q2}
	# et('0000053') # {0:q1}
	# et('0000054') # {1:q0}

	# ∘ blue
	x2 = eb('1000', 1) # {az}
	# x2 = eg('1000', 1) # {by}
	
	# ∘ long column 
	x3 = elt('1000007', 5) # {a}	
	# x3 = elt('1000006', 5) # {y}	
	# x3 = elt('1000206', 2) # {b}	
	# x3 = elt('1000207', 2) # {z}
			
	# ∘ short column
	x4 = est('1000207', 2) # {a}	
	# x4 = est('1000206', 2) # {y}
	# x4 = est('1000006', 5) # {b}	
	# x4 = est('1000007', 5) # {z}
	
	# ∘ green
	x5 = et('1000206') # {a}
	# et('1000207') # {y}
	# et('1000007') # {b}
	# et('1000006') # {z}

	# ---------------------------- #

	# columns: 0002504 0002002 0002404 0010101 0001201 0010403 0034300 0023404 0122501 0024504 0023504 0032501 0024304 0011100 0122000 0121100 0131001 0131304 0134201
	# elt('0002507', diagram.nodeByAddress['0002504'].ktype)
	# elt('0002007', diagram.nodeByAddress['0002002'].ktype)
	# elt('0002407', diagram.nodeByAddress['0002404'].ktype)
	# elt('0010107', diagram.nodeByAddress['0010101'].ktype)
	# elt('0001207', diagram.nodeByAddress['0001201'].ktype)
	# elt('0010407', diagram.nodeByAddress['0010403'].ktype)
	# elt('0034307', diagram.nodeByAddress['0034300'].ktype)
	# elt('0023407', diagram.nodeByAddress['0023404'].ktype)
	elt('0122507', diagram.nodeByAddress['0122501'].ktype)
	elt('0024507', diagram.nodeByAddress['0024504'].ktype)
	elt('0023507', diagram.nodeByAddress['0023504'].ktype)
	elt('0032507', diagram.nodeByAddress['0032501'].ktype)
	elt('0024307', diagram.nodeByAddress['0024304'].ktype)
	elt('0011107', diagram.nodeByAddress['0011100'].ktype)
	elt('0122007', diagram.nodeByAddress['0122000'].ktype)
	elt('0121107', diagram.nodeByAddress['0121100'].ktype)
	elt('0131007', diagram.nodeByAddress['0131001'].ktype)
	elt('0131307', diagram.nodeByAddress['0131304'].ktype)
	elt('0134207', diagram.nodeByAddress['0134201'].ktype)

	# show(diagram)
	# input2("...")
	
	# ---------------------------- #
	
	startTime = time()
	leap()
	#jump(mx.filter_avtuples())
	#step([l for l in diagram.loops if l.availabled], 0, [])
	input2(f"[leap] « [step] // nl")

	# ============================ #
	
	elt('0001007', 5)
	elt('0001207', 3)
	elt('0010007', 6)
	elt('0010207', 4)
	elt('0002207', 7)
	elt('0002107', 5)
	elt('0002307', 4)
	elt('0002407', 4)
	elt('0011007', 4)
									
	print(f"avcolumns: {len([col for col in diagram.columns if col.isAvailabled()])}")
	
	unavailed = 0
	for column in diagram.columns:
		if column.isAvailabled():
			
			extended = []
			for tuple in column.tuples:
				for loop in tuple:
					if diagram.extendLoop(loop):
						extended.append(loop)
					else:
						break
				if len(extended) % (diagram.spClass - 2) != 0:
					break
					
			if len(extended) != len(column.tuples) * (diagram.spClass - 2):
				print(f"broken column | extended: {len(extended)} / {len(column.tuples) * (diagram.spClass - 2)}")
				unavailed += 1
				column.unavailabled = True
				
			for loop in reversed(extended):
				diagram.collapseBack(loop)				
			
	print(f"unavailed: {unavailed} | remaining avcolumns: {len([col for col in diagram.columns if col.isAvailabled()])}")
				
	# ---------------------------- #
	
	diagram.point()
	show(diagram)	

