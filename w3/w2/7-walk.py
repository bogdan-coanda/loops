from diagram import *
from uicanvas import *
from mx import *
from time import time

step_cc = -1
step_id = -1
jump_id = -1
min_jump_chains_reached = 136 # 141 chains
min_step_chains_reached = 116
jump_step_required_lvl = 30

def step(avloops, jump_lvl, jump_path, step_lvl=0, step_path=[]):
	global step_cc, step_id, min_step_chains_reached
	if step_lvl == 0:
		step_cc += 1
	step_id += 1
	
	def key():
		return f"[{step_cc:>2}»{step_id:>4}][{tstr(time() - startTime):>11}][lvl:{jump_lvl}»{step_lvl}]"
			
	print(f"{key()}[ch:{len(diagram.chains)}|av:{len(avloops)}] {'.'.join([(str(x)+upper(t)) for x,t in jump_path])}\n» {'.'.join([(str(x)+upper(t)) for x,t in step_path])}")
	
	if len(diagram.chains) == 1:
		show(diagram)
		input2(f"{key()} sol found.")
		return
		
	if len(diagram.chains) < min_step_chains_reached:
		min_step_chains_reached = len(diagram.chains)
		show(diagram)
		input2(f"{key()} new min step chains: {min_step_chains_reached}")
				
	min_chain = sorted(diagram.chains, key = lambda chain: (len(chain.avnodes), chain.id))[0]
	# print(f"{key()} chosen min: {min_chain}")
	
	seen = []
	min_avlen = len(min_chain.avnodes)
	
	for i,n in enumerate(sorted(min_chain.avnodes, key = lambda n: n.address)):
		assert diagram.extendLoop(n.loop)		
		step([l for l in avloops if l.available], jump_lvl, jump_path, step_lvl+1, step_path+[(i, min_avlen)])
		diagram.collapseBack(n.loop)	
		
		seen.append(n.loop)
		diagram.setLoopUnavailable(n.loop)
		
	for l in reversed(seen):
		diagram.resetLoopAvailable(l)
		
		
def jump(avtuples, lvl=0, path=[]):
	global jump_id, min_jump_chains_reached
	jump_id += 1
		
	def key():
		return f"[{jump_id:>4}][{tstr(time() - startTime):>11}][lvl:{lvl}]" 
	
	if jump_id % 100 == 0:
		print(f"{key()} {'.'.join([(str(x)+upper(t)) for x,t in path])}")
	
	if len(diagram.chains) < min_jump_chains_reached:
		min_jump_chains_reached = len(diagram.chains)
		show(diagram)
		input2(f"{key()} new min jump chains: {min_jump_chains_reached}")
	
	min_chlen = mx.min_chain_avloops_length()	
	# print(f"{key()}[mx] 1. min_chlen: {min_chlen}")	
	
	if min_chlen == 0:
		# print(f"{key()}[mx] ⇒ dead @ unconnectable")
		return
		
	unicycle_chains = mx.filter_unicycle_chains()	
	# print(f"{key()}[mx] 2. unicycle chains: {len(unicycle_chains)}")	
		
	if len(unicycle_chains) == 0:
		print(f"{key()}[mx] ⇒ all cycles covered by tuples")
		step([l for l in diagram.loops if l.available], lvl, path)
		input2(f"[jump] « [step] // cc")
		return			
		
	avtuples = mx.filter_avtuples(avtuples)	
	# print(f"{key()}[mx] 3. avtuples: {len(avtuples)} / {len(diagram.loop_tuples)}")	

	if len(avtuples) == 0:
		if lvl >= jump_step_required_lvl:
			print(f"{key()}[mx] ⇒ no tuples remaining")			
			step([l for l in diagram.loops if l.available], lvl, path)
			# input2(f"[jump] « [step] // nt")
		return			
				
	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	# print(f"{key()}[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")		

	if len(min_nodes) == 0:
		if lvl >= jump_step_required_lvl:
			print(f"{key()}[mx] ⇒ not coverable by tuples | {min_cycle}")
			step([l for l in diagram.loops if l.available], lvl, path)
			# input2(f"[jump] « [step] // nc")		
		return
		
	if lvl < 12 and len(min_nodes) > 1:
		# print(f"{key()}[mx] ⇒ not single choice, purging…")
		
		# [~] next_single_choices is unused ?
		avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
		# print(f"{key()}[mx][purge] avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

		if len(avtuples) == 0:
			if lvl >= jump_step_required_lvl:
				print(f"{key()}[mx][purge] ⇒ no tuples remaining")
				step([l for l in diagram.loops if l.available], lvl, path)
				# input2(f"[jump] « [step] // nt")
			return			
												
		min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)
		# print(f"{key()}[mx][purge] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
		
		if len(min_nodes) == 0:
			if lvl >= jump_step_required_lvl:
				print(f"{key()}[mx] ⇒ not coverable by tuples | {min_cycle}")
				step([l for l in diagram.loops if l.available], lvl, path)
				# input2(f"[jump] « [step] // nc")		
			return
				
	else:
		# print(f"{key()}[mx] ⇒ single choice.")
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

	# print(f"{key()} ⇒ finished all choices")
			

if __name__ == "__main__":

	diagram = Diagram(7, kernelPath='')
	
	def cOc(segment):
		for i,x in enumerate(segment):
			if x in [' ', '-']:
				pass
			elif x == 'b':
				assert diagram.connectOpenChain('l3b')
			elif x == '+':
				assert diagram.connectOpenChain(4)
			else:
				assert diagram.connectOpenChain(int(x))		

	def pOc(segment):
		for i,x in enumerate(reversed(segment)):
			if x == ' ':
				pass
			elif x == 'b':
				assert diagram.prependOpenChain('l3b')
			elif x == '+':
				assert diagram.prependOpenChain(4)
			else:
				assert diagram.prependOpenChain(int(x))
	
	''' --- The Possibilities --- 
	id = "+" | links = [4,2,2,2,2] | segment =   "[+5]" | size = 12
	id =  9  | links = [3,3,2,2,2] | segment = "[∘1∘4]" | size = 12
	id =  8  | links = [3,2,3,2,2] | segment = "[∘2∘3]" | size = 12
	id =  7  | links = [3,2,2,3,2] | segment = "[∘3∘2]" | size = 12
	id =  6  | links = [3,2,2,2,3] | segment = "[∘4∘1]" | size = 12					
	id =  5  | links = [3,2,2,2,2] | segment =   "[∘5]" | size = 11
	id =  4  | links = [2,3,2,2,2] | segment =  "[1∘4]" | size = 11
	id =  3  | links = [2,2,3,2,2] | segment =  "[2∘3]" | size = 11
	id =  2  | links = [2,2,2,3,2] | segment =  "[3∘2]" | size = 11
	id =  1  | links = [2,2,2,2,3] | segment =  "[4∘1]" | size = 11	
	id =  0  | links = [2,2,2,2,2] | segment =    "[5]" | size = 10	
	'''
	
	'''# [  18][lvl:15] off: -2 § K210605454323210
	#         K          2     1     0     6     0     5     4     5     4     3     2     3     2     1     0
	#   «2232«2»2322»  [3∘2] [4∘1]  [5] [∘4∘1]  [5]  [∘5]  [1∘4] [∘5]  [1∘4] [2∘3] [3∘2] [2∘3] [3∘2] [4∘1]  [5]
	cOc('2232-2-2322   22232 22223 22222 32223 22222 32222 23222 32222 23222 22322 22232 22322 22232 22223 22222')
	pOc(list(reversed('22232 22223 22222 32223 22222 32222 23222 32222 23222 22322 22232 22322 22232 22223 22222'))) #'''
	
	# [  19][lvl:16] off: -2 § K2106054543232105
	#         K          2     1     0     6     0     5     4     5     4     3     2     3     2     1     0     5
	#   «2232«2»2322»  [3∘2] [4∘1]  [5] [∘4∘1]  [5]  [∘5]  [1∘4] [∘5]  [1∘4] [2∘3] [3∘2] [2∘3] [3∘2] [4∘1]  [5]  [∘5]
	cOc('2232-2-2322   22232 22223 22222 32223 22222 32222 23222 32222 23222 22322 22232 22322 22232 22223 22222 32222')
	pOc(list(reversed('22232 22223 22222 32223 22222 32222 23222 32222 23222 22322 22232 22322 22232 22223 22222 32222'))) #'''
	
	'''# [  21][lvl:17] off: -2 § K21060545432321060
	#         K          2     1     0     6     0     5     4     5     4     3     2     3     2     1     0     6     0
	#   «2232«2»2322»  [3∘2] [4∘1]  [5] [∘4∘1]  [5]  [∘5]  [1∘4] [∘5]  [1∘4] [2∘3] [3∘2] [2∘3] [3∘2] [4∘1]  [5] [∘4∘1]  [5]
	cOc('2232-2-2322   22232 22223 22222 32223 22222 32222 23222 32222 23222 22322 22232 22322 22232 22223 22222 32223 22222')
	pOc(list(reversed('22232 22223 22222 32223 22222 32222 23222 32222 23222 22322 22232 22322 22232 22223 22222 32223 22222'))) #'''
	
	'''#[   27][lvl:21] off: -2 § K210605454323210623210
	#         K          2     1     0     6     0     5     4     5     4     3     2     3     2     1     0     6     2     3     2     1     0
	#   «2232«2»2322»  [3∘2] [4∘1]  [5] [∘4∘1]  [5]  [∘5]  [1∘4] [∘5]  [1∘4] [2∘3] [3∘2] [2∘3] [3∘2] [4∘1]  [5] [∘4∘1] [3∘2] [2∘3] [3∘2] [4∘1]  [5]
	cOc('2232-2-2322   22232 22223 22222 32223 22222 32222 23222 32222 23222 22322 22232 22322 22232 22223 22222 32223 22232 22322 22232 22223 22222')
	pOc(list(reversed('22232 22223 22222 32223 22222 32222 23222 32222 23222 22322 22232 22322 22232 22223 22222 32223 22232 22322 22232 22223 22222'))) #'''
	
	show(diagram)
	input2('---')
	
	print(f"[mx] 0. walk | loop tuples: {len(diagram.loop_tuples)}")
	diagram.walk([diagram.openChain.headNode, diagram.openChain.tailNode.prevs[1].node], True)				
	print(f"[mx] 0. walk | loop tuples: {len(diagram.loop_tuples)}")						
	mx = MX(diagram)
		
	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	
	
	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	
	
	print(f"[mx] 3. loop tuples: {len(diagram.loop_tuples)} | av loops: {len([l for l in diagram.loops if l.available])}")
	avtuples = mx.filter_avtuples()	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")		
	
	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")			
	
	startTime = time()
	jump(avtuples)			
		
		
	diagram.point()
	show(diagram)

	
