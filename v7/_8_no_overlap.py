from diagram import *
from uicanvas import *
from common import *
from measurement import *
from itertools import chain
from time import time
from collections import defaultdict
from random import *

FORCED_FREQUENCY = -1

def input2(text):
	input(text+"  |  » ∘ «")
	
history = True
history_move_index = 14530013
history_raw_jumps = "0⁶.0⁴.0⁴.0⁴.0⁴.0⁴.0².0².0³.0².0⁴.0³.0⁵.0³.0³.0¹.0³.0⁶.0⁴.0³.0³.0³.0⁴.0⁴.0².0³.0³.0².0³.0³.0².0².0³.0².0².0².0¹.0².0³.0¹.0¹.0².0¹.0².0⁴.0³.0³.0⁴.0².0³.0².0².0².0³.0¹.0¹.0².0¹.0².3⁵.1³.0¹.1².0¹.0¹.0¹.0¹.0¹.0¹.1².0¹.1².1².1².0¹.0¹.1².0¹.1².1².0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.1³.1².0¹.0².0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0².0¹.0¹.0¹.0¹.0¹.0¹.0².0¹.0¹.0¹.0¹.0¹.1².0¹.0¹.0¹.0¹.|⁶.|⁶"
history_raw_steps = "0².0¹.0².0¹.1².0².0².0².1².0¹.1².0².1².1².0².0².1².1².0².0².0¹.1².0².0².0².0².0¹.0¹.1².0².1².1².0¹.0².0².0¹.1².1².0¹.0¹.1².0².1².0¹.0².0¹.0¹.0¹.1².0².0².1².0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹.0¹"
history_jumps = [int(n) for n in "".join([x for x in history_raw_jumps if x in ".0123456789"]).split('.') if len(n)]
history_steps = [int(n) for n in "".join([x for x in history_raw_steps if x in ".0123456789"]).split('.') if len(n)]

def historic_jump(jump_lvl, min_matched_tuples):
	if history:
		it = history_jumps[jump_lvl]
		return list(enumerate(min_matched_tuples))[it:]
	else:
		return enumerate(min_matched_tuples)

def historic_step(step_lvl, min_nodes):
	global history, move_index
	
	if history:
		j = history_steps[step_lvl]
		if step_lvl == len(history_steps) - 1:
			history = False
			move_index = history_move_index - 1
			print("[history] turning off…")
		return list(enumerate(min_nodes))[j:]			
	else:
		return enumerate(min_nodes)
	

def wtc(diagram, mx, move_path, jump_lvl, step_lvl=None, move_nodes=None, frequency=1):
	global move_index, startTime
		
	if frequency != FORCED_FREQUENCY:
		move_index += 1

	if frequency == FORCED_FREQUENCY or move_index % frequency == 0:
		#show(diagram)		
		print("[*{}*][{:>11}][lvl:{}{}][uc:{}][𝒞:{}] {}{}".format(
			move_index, tstr(time() - startTime), 
			jump_lvl, '~'+str(step_lvl) if step_lvl else '',
			len(mx.unchained_cycles), len(diagram.chains), 
			'--- sol --- ' if len(diagram.chains) is 1 else ('- forced - ' if frequency is FORCED_FREQUENCY else ''),			
			".".join([str(x)+upper(t) for x,t in move_path])))
		if move_nodes is not None:
			print(f'jumps: {" ".join([n.address for n in move_nodes[:jump_lvl]])}')
			if step_lvl is not None:
				print(f'steps: {" ".join([n.address for n in move_nodes[jump_lvl:]])}')
			
			
def wtf(diagram, mx, move_path, jump_lvl, step_lvl=None, move_nodes=None, msg=None):
	global move_index, startTime
		
	with open("__8__js_14m__", 'a', encoding="utf8") as log:
		log.write("[*{}*][{:>11}][lvl:{}{}][uc:{}][𝒞:{}] {}{}\n".format(
			move_index, tstr(time() - startTime), 
			jump_lvl, '~'+str(step_lvl) if step_lvl else '',
			len(mx.unchained_cycles), len(diagram.chains),
			f'--- {msg} --- ' if msg else '',
			".".join([str(x)+upper(t) for x,t in move_path])))
		if move_nodes is not None:
			log.write(f'jumps: {" ".join([n.address for n in move_nodes[:jump_lvl]])}\n')
			if step_lvl is not None:
				log.write(f'steps: {" ".join([n.address for n in move_nodes[jump_lvl:]])}\n')		


def test_min_uc(diagram, mx, move_path, jump_lvl, move_nodes):
	global move_index, startTime, min_uc, min_cc	
	
	if len(mx.unchained_cycles) < min_uc:
		min_uc = len(mx.unchained_cycles)
		wtf(diagram, mx, move_path, jump_lvl, None, move_nodes, 'uc<')
	elif len(mx.unchained_cycles) == min_uc and len(diagram.chains) <= min_cc:
		min_cc = len(diagram.chains)
		wtf(diagram, mx, move_path, jump_lvl, None, move_nodes, 'uc=')		

				
def test_min_cc(diagram, mx, move_path, jump_lvl, step_lvl, move_nodes):
	global move_index, startTime, min_cc
	
	if len(diagram.chains) <= min_cc:
		min_cc = len(diagram.chains)
		wtf(diagram, mx, move_path, jump_lvl, step_lvl, move_nodes, 'cc')
					

def step(diagram, old_mx, move_path, move_nodes, jump_lvl, step_lvl=0):
	
	# write to console
	wtc(diagram, old_mx, move_path, jump_lvl, step_lvl, frequency=100)
	
	# remeasure
	new_mx = old_mx.remeasure()
	
	# find current choices
	min_nodes = new_mx.find_min_chain()
	
	# test for minimum number of chains found so far
	test_min_cc(diagram, new_mx, move_path, jump_lvl, step_lvl, move_nodes)
	
	if len(diagram.chains) is 1: # we found a solution
		wtf(diagram, new_mx, move_path, jump_lvl, step_lvl, move_nodes, '[sol]')
		wtc(diagram, new_mx, move_path, jump_lvl, step_lvl, move_nodes, FORCED_FREQUENCY)
		show(diagram)
		input2("[found a solution]")
		return
	
	if len(min_nodes) is 0: # can't further connect chains
		# diagram.point(); show(diagram); input(f"[step] === @ can't {min_nodes} ===")
		return
		
	# go through all choices
	for j,n in historic_step(step_lvl, min_nodes):		
		if diagram.extendLoop(n.loop):		
			step(diagram, new_mx, move_path+[(j,len(min_nodes))], move_nodes+[n], jump_lvl, step_lvl+1)
			diagram.collapseBack(n.loop)		
		
		

def jump(diagram, old_mx, move_path=[], move_nodes=[], jump_lvl=0):
	
	# write to console
	wtc(diagram, old_mx, move_path, jump_lvl, frequency=100)
			
	# remeasure
	new_mx = old_mx.remeasure()
	new_mx.measure_untouched_tuples()
							
	# find current choices
	min_cycle, min_nodes, min_matched_tuples = Measurement._find_min_simple(diagram, new_mx.unchained_cycles, new_mx.avtuples)
		
	# test for minimum number of unchained cycles found so far		
	test_min_uc(diagram, new_mx, move_path, jump_lvl, move_nodes)
			
	if new_mx.min_chlen is 0 or len(min_matched_tuples) is 0: # can't further connect chains
		# diagram.pointers = list(itertools.chain(*[chain.cycles for chain in diagram.chains if not len(chain.avloops)])) if min_chlen is 0 else [min_cycle]
		# show(diagram); input("[jump] === @ can't {},{} === ".format(min_chlen, len(min_matched_tuples)))
		return

	if new_mx.min_chlen is 1: # we found a `single`
		# extend just singles (faster…)
		new_mx.single()
		
		# append path
		move_path += [('|', len(new_mx.singles))]
		
		# diagram.point()
		# show(diagram)
		
		wtf(diagram, new_mx, move_path, jump_lvl, None, move_nodes, f'[mx|s:{len(new_mx.singles)}|c:{len(new_mx.coerced)}|z:{len(new_mx.zeroes)}]')							
		#print(new_mx)		
		#print("=== -1- ===")

	if len(new_mx.unchained_cycles) is 0: # all cycles have been looped	
		wtf(diagram, new_mx, move_path, jump_lvl, None, move_nodes, '[smth]')		
		# show(diagram)
		wtc(diagram, new_mx, move_path, jump_lvl, None, move_nodes, FORCED_FREQUENCY)
		
		if not new_mx.reduced:
			new_mx.reduce()
		else:
			newer_mx = new_mx.remeasure()
			newer_mx.reduce()
			newer_mx.singles = new_mx.singles + newer_mx.singles
			new_mx = newer_mx

		if len(new_mx.singles) or len(new_mx.coerced) or len(new_mx.zeroes):
			move_path += [('|', len(new_mx.singles))]
			wtf(diagram, new_mx, move_path, jump_lvl, None, move_nodes, f'[smth:mx|s:{len(new_mx.singles)}|c:{len(new_mx.coerced)}|z:{len(new_mx.zeroes)}]')							
			print(new_mx)		
			print("=== +1+ ===")			
								
		if new_mx.min_chlen is 0:
			wtf(diagram, new_mx, move_path, jump_lvl, None, move_nodes, "±±± didn't find anything ±±±")			
			print("±±± didn't find anything ±±±")			
		else:
			print("~~~ found smth ~~~")
			# start stepping
			step(diagram, new_mx, move_path+[("~","")], move_nodes, jump_lvl)		
		
	else:															
		# go through all choices
		for it, t in historic_jump(jump_lvl, min_matched_tuples):
							
			ec = 0
			for lt, l in enumerate(t):
				if diagram.extendLoop(l):
					ec += 1
				else:
					# print("[*{}*][{}][lvl:{}] failed extending it: {} | mc: {}".format(move_index, tstr(time() - startTime), lvl, it, new_mx.mc))
					break
	
			if ec == len(t): # if we've extended all of the tuple's loops
				jump(diagram, new_mx, move_path+[(it,len(min_matched_tuples))], move_nodes+[min_nodes[it]], jump_lvl+1)
	
			for l in reversed(t[:ec]):
				diagram.collapseBack(l)

	# we might have extended singles
	new_mx.clean()


if __name__ == "__main__":
	
	diagram = Diagram(8, 1)
						
	print("diagram.loop_tuples: " + str(len(diagram.loop_tuples)))
	
	startTime = time()
	move_index = -1
	min_uc = len(diagram.cycles)
	min_cc = len(diagram.chains)
			
	mx = Measurement(diagram)
	mx.measure_untouched_tuples()	
			
	jump(diagram, mx)

	input2("⇒ done !?!!?!!??!??!?!?!??!")					
	# diagram.point()
	# show(diagram)	
