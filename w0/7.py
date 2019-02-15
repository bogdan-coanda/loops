from diagram import *
from uicanvas import *
from mx import *
from time import time


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
	# print(f"{key()}[mx] 1. min_chlen: {min_chlen}")	
	
	if min_chlen == 0:
		# print(f"{key()}[mx] ⇒ dead @ unconnectable")
		return
		
	unicycle_chains = mx.filter_unicycle_chains()	
	# print(f"{key()}[mx] 2. unicycle chains: {len(unicycle_chains)}")	
		
	if len(unicycle_chains) == 0:
		print(f"{key()}[mx] ⇒ all cycles covered by tuples")
		step([l for l in diagram.loops if l.availabled], lvl, path)
		# input2(f"[jump] « [step] // cc")
		return			
		
	avtuples = mx.filter_avtuples(avtuples)	
	# print(f"{key()}[mx] 3. avtuples: {len(avtuples)} / {len(diagram.loop_tuples)}")	

	if len(avtuples) == 0:
		print(f"{key()}[mx] ⇒ no tuples remaining")
		# step([l for l in diagram.loops if l.availabled], lvl, path)
		# input2(f"[jump] « [step] // nt")
		return			
				
	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	# print(f"{key()}[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")		

	if len(min_nodes) == 0:
		# print(f"{key()}[mx] ⇒ dead @ not coverable")
		return
		
	if lvl < 12 and len(min_nodes) > 1:
		# print(f"{key()}[mx] ⇒ not single choice, purging…")
		
		# [~] next_single_choices is unused ?
		avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
		# print(f"{key()}[mx][purge] avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

		if len(avtuples) == 0:
			print(f"{key()}[mx][purge] ⇒ no tuples remaining")
			# step([l for l in diagram.loops if l.availabled], lvl, path)
			# input2(f"[jump] « [step] // nt")
			return			
												
		min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)
		# print(f"{key()}[mx][purge] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
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
	
	diagram = Diagram(7, 1)
	mx = MX(diagram)
		
	import enav
	enav.diagram = diagram
	from enav import *



	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	
	
	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	
		
	avtuples = mx.filter_avtuples()	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")		


			
	#extend('000002')
	
	et('001006')
	et('001106')
	et('001206')
	et('001306')

	et('001401')
	et('001410')
	et('001430')
	et('001452')

	show(diagram)
	input2("---")

	'''
tuples: 001006 001106 001206 001306 001401 001410 001430 001452 002002 002011 002020 002053 002143 002233 013020 013044 013200 013224 013233 013251 022006 022106 022306 112005
loops: 000002 001052 001133 001311 002230 002251 002402 002453 003005 010001 011203 012110 021443 100014 100243 101152 101430 103023	
	'''
			
	startTime = time()
	jump(avtuples)
	
	
	'''
	# et('001312') # 0/3
	# et('112003') # 0/3
	# et('001206') # 0/2
	# et('001436') # 0/4
	# et('001302') # 0/1
	# et('001106') # 0/2
	
			
	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	
	
	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	
		
	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	
	
	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")
	
	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")
					
	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")


	# [mx] 1. min chain avloops length: 5
	# [mx] 2. unicycle chains: 690
	# [mx] 3. avtuples: 146 | all tuples: 168

	
	# [ex] ⇒ extended 000001
	# [mx] 1. min chain avloops length: 4
	# [mx] 2. unicycle chains: 685
	# [mx] 3. avtuples: 142 | all tuples: 168
	# [mx] ⇒ mr: 6 | mc: ⟨cycle:49@00131⟩ | mn: ['001313', '001312', '001311'] | mt: 3
	# [mx] 4. avtuples: 136 | sample lengths: [(1, 1), (2, 27), (3, 108)] | single choices: 1
	# [mx] ⇒ mr: 8 | mc: ⟨cycle:54@00140⟩ | mn: ['001406', '001401'] | mt: [3, 3]
	et('001406') # 0/2

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")


	# [et] ⇒ extended 5 loops in tuple for 001406
	# [mx] 1. min chain avloops length: 3
	# [mx] 2. unicycle chains: 656
	# [mx] 3. avtuples: 132 | all tuples: 168
	# [mx] ⇒ mr: 6 | mc: ⟨cycle:48@00130⟩ | mn: ['001304', '001303', '001302'] | mt: 3
	# [mx] 4. avtuples: 131 | sample lengths: [(1, 5), (2, 39), (3, 87)] | single choices: 5
	# [mx] ⇒ mr: 11 | mc: ⟨cycle:48@00130⟩ | mn: ['001303', '001304', '001302'] | mt: [2, 3, 3]
	et('001303') # 0/3

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
	
	
	# [et] ⇒ extended 5 loops in tuple for 001303
	# [mx] 1. min chain avloops length: 3
	# [mx] 2. unicycle chains: 627
	# [mx] 3. avtuples: 126 | all tuples: 168
	# [mx] ⇒ mr: 4 | mc: ⟨cycle:42@00120⟩ | mn: ['001206', '001205'] | mt: 2
	# [mx] 4. avtuples: 123 | sample lengths: [(1, 11), (2, 111), (3, 1)] | single choices: 11
	# [mx] ⇒ mr: 7 | mc: ⟨cycle:42@00120⟩ | mn: ['001205', '001206'] | mt: [2, 3]			
	et('001205') # 0/2

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
	
	
	# [et] ⇒ extended 5 loops in tuple for 001205
	# [mx] 1. min chain avloops length: 2
	# [mx] 2. unicycle chains: 603
	# [mx] 3. avtuples: 119 | all tuples: 168
	# [mx] ⇒ mr: 4 | mc: ⟨cycle:43@00121⟩ | mn: ['001213', '001212'] | mt: 2
	# [mx] 4. avtuples: 118 | sample lengths: [(1, 19), (2, 99)] | single choices: 19
	# [mx] ⇒ mr: 6 | mc: ⟨cycle:43@00121⟩ | mn: ['001213', '001212'] | mt: [2, 2]
	et('001213') # 0/2

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
	
		
	# [et] ⇒ extended 5 loops in tuple for 001213
	# [mx] 1. min chain avloops length: 2
	# [mx] 2. unicycle chains: 573
	# [mx] 3. avtuples: 114 | all tuples: 168
	# [mx] ⇒ mr: 4 | mc: ⟨cycle:49@00131⟩ | mn: ['001313', '001311'] | mt: 2
	# [mx] 4. avtuples: 112 | sample lengths: [(1, 21), (2, 91)] | single choices: 21
	# [mx] ⇒ mr: 6 | mc: ⟨cycle:49@00131⟩ | mn: ['001313', '001311'] | mt: [2, 2]			
	et('001313') # 0/2

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
	
						
	# [et] ⇒ extended 5 loops in tuple for 001313
	# [mx] 1. min chain avloops length: 2
	# [mx] 2. unicycle chains: 544
	# [mx] 3. avtuples: 107 | all tuples: 168
	# [mx] ⇒ mr: 4 | mc: ⟨cycle:53@00135⟩ | mn: ['001354', '001353'] | mt: 2
	# [mx] 4. avtuples: 105 | sample lengths: [(1, 19), (2, 86)] | single choices: 19
	# [mx] ⇒ mr: 6 | mc: ⟨cycle:53@00135⟩ | mn: ['001354', '001353'] | mt: [2, 2]											
	et('001354') # 0/2

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
	
	
	# [et] ⇒ extended 5 loops in tuple for 001354
	# [mx] 1. min chain avloops length: 3
	# [mx] 2. unicycle chains: 514
	# [mx] 3. avtuples: 102 | all tuples: 168
	# [mx] ⇒ mr: 4 | mc: ⟨cycle:66@00210⟩ | mn: ['002106', '002100'] | mt: 2
	# [mx] 4. avtuples: 99 | sample lengths: [(1, 14), (2, 84), (3, 1)] | single choices: 14
	# [mx] ⇒ mr: 7 | mc: ⟨cycle:66@00210⟩ | mn: ['002100', '002106'] | mt: [2, 3]	
	et('002100') # 0/2

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
	
		
	# [et] ⇒ extended 5 loops in tuple for 002100
	# [mx] 1. min chain avloops length: 2
	# [mx] 2. unicycle chains: 485
	# [mx] 3. avtuples: 93 | all tuples: 168
	# [mx] ⇒ mr: 4 | mc: ⟨cycle:30@00100⟩ | mn: ['001006', '001005'] | mt: 2
	# [mx] 4. avtuples: 91 | sample lengths: [(1, 18), (2, 73)] | single choices: 18
	# [mx] ⇒ mr: 4 | mc: ⟨cycle:30@00100⟩ | mn: ['001006', '001005'] | mt: [1, 1]			
	et('001006') # 0/2

	print(f"[mx] 0. next single choice: {next_single_choices[min_matched_tuples[0]]}")

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
	
		
	# [et] ⇒ extended 5 loops in tuple for 001006
	# [mx] 0. next single choice: [⟨node:6230415@001106§⟨chain:36|av:2⟩|Av⟩]
	# [mx] 1. min chain avloops length: 2
	# [mx] 2. unicycle chains: 460
	# [mx] 3. avtuples: 88 | all tuples: 168
	# [mx] ⇒ mr: 2 | mc: ⟨cycle:36@00110⟩ | mn: ['001106'] | mt: 1
	# [mx] 4. avtuples: 79 | sample lengths: [(1, 78), (2, 1)] | single choices: 78
	# [mx] ⇒ mr: 3 | mc: ⟨cycle:36@00110⟩ | mn: ['001106'] | mt: [2]
	et('001106') # 0/1

	print(f"[mx] 0. next single choice: {next_single_choices[min_matched_tuples[0]] if min_matched_tuples[0] in next_single_choices else None}")

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")


	# [et] ⇒ extended 5 loops in tuple for 001106
	# [mx] 0. next single choice: None
	# [mx] 1. min chain avloops length: 2
	# [mx] 2. unicycle chains: 440
	# [mx] 3. avtuples: 79 | all tuples: 168
	# [mx] ⇒ mr: 4 | mc: ⟨cycle:46@00124⟩ | mn: ['001242', '001245'] | mt: 2
	# [mx] 4. avtuples: 77 | sample lengths: [(1, 31), (2, 46)] | single choices: 31
	# [mx] ⇒ mr: 4 | mc: ⟨cycle:542@11202⟩ | mn: ['112026', '112021'] | mt: [1, 1]
	et('112026') # 0/2

	print(f"[mx] 0. next single choice: {next_single_choices[min_matched_tuples[0]] if min_matched_tuples[0] in next_single_choices else None}")

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")


	# [et] ⇒ extended 5 loops in tuple for 112026
	# [mx] 0. next single choice: [⟨node:5642301@002405§⟨chain:84|av:3⟩|Av⟩]
	# [mx] 1. min chain avloops length: 2
	# [mx] 2. unicycle chains: 425
	# [mx] 3. avtuples: 68 | all tuples: 168
	# [mx] ⇒ mr: 2 | mc: ⟨cycle:84@00240⟩ | mn: ['002405'] | mt: 1
	# [mx] 4. avtuples: 61 | sample lengths: [(1, 60), (2, 1)] | single choices: 60
	# [mx] ⇒ mr: 3 | mc: ⟨cycle:84@00240⟩ | mn: ['002405'] | mt: [2]
	et('002405') # 0/1

	print(f"[mx] 0. next single choice: {next_single_choices[min_matched_tuples[0]] if min_matched_tuples[0] in next_single_choices else None}")

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
	
	
	# [et] ⇒ extended 5 loops in tuple for 002405
	# [mx] 0. next single choice: None
	# [mx] 1. min chain avloops length: 2
	# [mx] 2. unicycle chains: 395
	# [mx] 3. avtuples: 61 | all tuples: 168
	# [mx] ⇒ mr: 4 | mc: ⟨cycle:45@00123⟩ | mn: ['001233', '001230'] | mt: 2
	# [mx] 4. avtuples: 60 | sample lengths: [(1, 39), (2, 21)] | single choices: 39
	# [mx] ⇒ mr: 4 | mc: ⟨cycle:50@00132⟩ | mn: ['001322', '001320'] | mt: [1, 1]	
	et('001322') # 0/2

	print(f"[mx] 0. next single choice: {next_single_choices[min_matched_tuples[0]] if min_matched_tuples[0] in next_single_choices else None}")

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
	
	
	# [et] ⇒ extended 5 loops in tuple for 001322
	# [mx] 0. next single choice: [⟨node:3250416@022330§⟨chain:321|av:2⟩|Av⟩]
	# [mx] 1. min chain avloops length: 2
	# [mx] 2. unicycle chains: 365
	# [mx] 3. avtuples: 59 | all tuples: 168
	# [mx] ⇒ mr: 2 | mc: ⟨cycle:321@02233⟩ | mn: ['022330'] | mt: 1
	# [mx] 4. avtuples: 55 | sample lengths: [(1, 55)] | single choices: 55
	# [mx] ⇒ mr: 2 | mc: ⟨cycle:51@00133⟩ | mn: ['001331'] | mt: [1]	
	et('022330') # 0/1 # from next single choice

	print(f"[mx] 0. next single choice: {next_single_choices[min_matched_tuples[0]] if min_matched_tuples[0] in next_single_choices else None}")

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")		
			
					
	# [et] ⇒ extended 5 loops in tuple for 022330
	# [mx] 0. next single choice: [⟨node:5320461@022141§⟨chain:310|av:3⟩|Av⟩]
	# [mx] 1. min chain avloops length: 2
	# [mx] 2. unicycle chains: 340
	# [mx] 3. avtuples: 55 | all tuples: 168
	# [mx] ⇒ mr: 2 | mc: ⟨cycle:310@02214⟩ | mn: ['022141'] | mt: 1
	# [mx] 4. avtuples: 53 | sample lengths: [(1, 52), (2, 1)] | single choices: 52
	# [mx] ⇒ mr: 3 | mc: ⟨cycle:300@02200⟩ | mn: ['022005'] | mt: [2]	
	et('022141') # 0/1 # from next single choice

	print(f"[mx] 0. next single choice: {next_single_choices[min_matched_tuples[0]] if min_matched_tuples[0] in next_single_choices else None}")

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")		
	

	# [et] ⇒ extended 5 loops in tuple for 022141
	# [mx] 0. next single choice: None
	# [mx] 1. min chain avloops length: 2
	# [mx] 2. unicycle chains: 315
	# [mx] 3. avtuples: 53 | all tuples: 168
	# [mx] ⇒ mr: 4 | mc: ⟨cycle:62@00202⟩ | mn: ['002026', '002025'] | mt: 2
	# [mx] 4. avtuples: 48 | sample lengths: [(1, 37), (2, 11)] | single choices: 37
	# [mx] ⇒ mr: 2 | mc: ⟨cycle:316@02224⟩ | mn: ['022245'] | mt: [1]
	et('022245') # 0/1

	print(f"[mx] 0. next single choice: {next_single_choices[min_matched_tuples[0]] if min_matched_tuples[0] in next_single_choices else None}")

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")				


	# [et] ⇒ extended 5 loops in tuple for 022245
	# [mx] 0. next single choice: [⟨node:6312045@013006§⟨chain:210|av:2⟩|Av⟩]
	# [mx] 1. min chain avloops length: 2
	# [mx] 2. unicycle chains: 290
	# [mx] 3. avtuples: 45 | all tuples: 168
	# [mx] ⇒ mr: 2 | mc: ⟨cycle:210@01300⟩ | mn: ['013006'] | mt: 1
	# [mx] 4. avtuples: 38 | sample lengths: [(1, 38)] | single choices: 38
	# [mx] ⇒ mr: 2 | mc: ⟨cycle:210@01300⟩ | mn: ['013006'] | mt: [1]		
	et('013006') # 0/1 # from next single choice

	print(f"[mx] 0. next single choice: {next_single_choices[min_matched_tuples[0]] if min_matched_tuples[0] in next_single_choices else None}")

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")				

		
	# [et] ⇒ extended 5 loops in tuple for 013006
	# [mx] 0. next single choice: [⟨node:4513620@022022§⟨chain:302|av:3⟩|Av⟩]
	# [mx] 1. min chain avloops length: 1
	# [mx] 2. unicycle chains: 265
	# [mx] 3. avtuples: 38 | all tuples: 168
	# [mx] ⇒ mr: 2 | mc: ⟨cycle:235@01341⟩ | mn: ['013416'] | mt: 1
	# [mx] 4. avtuples: 25 | sample lengths: [(1, 25)] | single choices: 25
	# [mx] ⇒ mr: 2 | mc: ⟨cycle:62@00202⟩ | mn: ['002026'] | mt: [1]						
	et('022022') # 0/1 # from next single choice

	print(f"[mx] 0. next single choice: {next_single_choices[min_matched_tuples[0]] if min_matched_tuples[0] in next_single_choices else None}")

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")				
	

	# [et] ⇒ extended 5 loops in tuple for 022022
	# [mx] 0. next single choice: [⟨node:6142305@002306§⟨chain:78|av:3⟩|Av⟩]
	# [mx] 1. min chain avloops length: 1
	# [mx] 2. unicycle chains: 250
	# [mx] 3. avtuples: 25 | all tuples: 168
	# [mx] ⇒ mr: 2 | mc: ⟨cycle:62@00202⟩ | mn: ['002026'] | mt: 1
	# [mx] 4. avtuples: 9 | sample lengths: [(1, 9)] | single choices: 9
	# [mx] ⇒ mr: 0 | mc: ⟨cycle:62@00202⟩ | mn: [] | mt: []
	et('002306') # 0/1 # from next single choice

	print(f"[mx] 0. next single choice: {next_single_choices[min_matched_tuples[0]] if min_matched_tuples[0] in next_single_choices else None}")

	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	

	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	

	avtuples = mx.filter_avtuples(avtuples)	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")	

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")

	avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
	print(f"[mx] 4. avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)	
	print(f"[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")				
	'''
	
	

	diagram.point() # .pointers = min_nodes # 
	show(diagram)
