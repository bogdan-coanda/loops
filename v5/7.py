from diagram import *
from uicanvas import *
from extension_result import *
from common import *
import itertools
	

	
def checkForSolutions():
	global min_chains
	if len(diagram.chains) < min_chains:
		min_chains = len(diagram.chains)
		print("\n\nmin chains: "+str(min_chains)+"\n\n")
		if min_chains < 50:
			input()
			
	if len(diagram.chains) == 1:
		show(diagram)
		input("Found!…")

		

def single(loop, checkAllLoops, temporary): # ⇒ return reachable
	global mark
	singles = ordered_set()

	# check for unreachables and singles
	for chain in (loop.extension_result.touched_chains if not checkAllLoops else diagram.chains):
		
		if len(chain.avloops) is 0:
			#print("[singles] failed on initial extend from: " + str(loop))
			loop.extension_result.setReachability(False, temporary)
			return False
		elif len(chain.avloops) is 1:
			singles.add(list(chain.avloops)[0])
			#print("[singles] added: " + str(list(chain.avloops)[0]))
	
	# extend any singles
	while len(singles):
		single_loop = singles.pop()
		#print("[singles] popped: " + str(single_loop))
		assert diagram.extendLoop(single_loop)
		checkForSolutions()
		# if single_loop.addr() == '121010':
		# 	mark = single_loop.extension_result.new_chain.id
		# 	print("mark: " + str(mark))
		# if not temporary and mark in [chain.id for chain in single_loop.extension_result.affected_chains]:
		# 	print("[extend.s] " + single_loop.addr() + " ⇒ new chain: " + str(single_loop.extension_result.new_chain.id))
		loop.extension_result.coerce(single_loop, COERCED_EXTEND, temporary)	
	
		# check for unreachables and singles
		for chain in single_loop.extension_result.touched_chains:
			if len(chain.avloops) is 0:
				#print("[singles] failed extend after " + str(len(loop.extension_result.extended_loops)) + " loops from: " + str(loop))
				loop.extension_result.setReachability(False, temporary)
				return False
			elif len(chain.avloops) is 1:
				singles.add(list(chain.avloops)[0])		
				#print("[singles] added: " + str(list(chain.avloops)[0]) + " for " + str(chain))
				
	#if loop.extension_result.extended_count > 1:
		#print("[singles] extended " + str(loop.extension_result.extended_count) + " loops from: " + str(loop))
		
	loop.extension_result.setReachability(True, temporary)
	return True
		

def extendWithSingles(loop, temporary): # ⇒ return reachable
	
	# initial extend
	assert diagram.extendLoop(loop)
	checkForSolutions() # [~]
	# if not temporary and mark in [chain.id for chain in loop.extension_result.affected_chains]:
	# 	print("[extend.i] " + loop.addr() + " ⇒ new chain: " + str(loop.extension_result.new_chain.id))
	
	loop.extension_result.reset(temporary)	
	loop.extension_result.coerce(loop, COERCED_EXTEND, temporary)
		
	return single(loop, False, temporary)
	
	
def test(key, current_loop, reachable):
	if ((lvl == 0 and current_loop.nodes[0].address == '022200') 
	 or (lvl == 1 and current_loop.nodes[0].address == '123200')
	 or (lvl == 2 and current_loop.nodes[0].address == '111200')
	 or (lvl == 3 and current_loop.nodes[0].address == '123300')
	 or (lvl == 4 and current_loop.nodes[0].address == '012300')
	 or (lvl == 5 and current_loop.nodes[0].address in ['021300', '121300'])):
		print("[ -- "+str(lvl)+":["+key+"]:temp:"+current_loop.nodes[0].address+" -- ] ⟨ex:" + str(current_loop.extension_result.temporary_extended_count) + "|kd:" + str(current_loop.extension_result.temporary_killed_count) + "⟩"+("" if reachable else " NOT")+" reachable from root: " + current_loop.addr())										
		print("[…] " + str([(l.addr(),b) for l,b in current_loop.extension_result.temporary_coerced_loops]))
		
				
mark = 20744

def extend(loop): # ⇒ return reachable
	global mark
	# initial extend with singles
	if not extendWithSingles(loop, False): # [TEMP] not temporary ---
		print("[ --- "+str(lvl)+":extend --- ] failed init (ex:"+str(loop.extension_result.extended_count)+"|kd:"+str(loop.extension_result.killed_count)+") from root: " + loop.addr())		
		return False

	# do … while we killed something			
	while True:
	
		killedSomething = False
				
		# further test extend all available loops
		avloops = [l for l in diagram.loops if l.availabled]
		
		for current_loop in avloops:
			
			temporary_reachable = extendWithSingles(current_loop, True) # [TEMP] temporary +++
			for coerced_loop,coercion_type in reversed(current_loop.extension_result.temporary_coerced_loops):
				assert coercion_type == COERCED_EXTEND
				diagram.collapseBack(coerced_loop)
				
			# [dbg] test('Ex', current_loop, reachable)
										
			if not temporary_reachable:
				diagram.setLoopUnavailabled(current_loop)
				loop.extension_result.coerce(current_loop, COERCED_KILL, False) # [TEMP] not temporary ---
				killedSomething = True

		if not killedSomething:
			print("[ --- "+str(lvl)+":extend --- ] ⟨ex:" + str(loop.extension_result.extended_count) + "|kd:" + str(loop.extension_result.killed_count) + "⟩ successful from root: " + loop.addr())
			return True
		else:
			if not single(loop, True, False): # [TEMP] not temporary ---
				print("[ --- "+str(lvl)+":extend --- ] failed post (ex:"+str(loop.extension_result.extended_count)+"|kd:"+str(loop.extension_result.killed_count)+") from root: " + loop.addr())		
				return False
								
					
def collapse(loop):
	print("[ -- "+str(lvl)+":collapse -- ] ⟨ex:" + str(loop.extension_result.extended_count) + "|kd:" + str(loop.extension_result.killed_count) + "⟩ from root: " + loop.addr())
			
	for coerced_loop,coercion_type in reversed(loop.extension_result.coerced_loops):
		if coercion_type == COERCED_EXTEND:
			# if mark in [chain.id for chain in coerced_loop.extension_result.affected_chains]:
			# 	print("[collapse] " + coerced_loop.addr() + " ⇒ new chain: " + str(coerced_loop.extension_result.new_chain.id))
			diagram.collapseBack(coerced_loop)
		else:
			diagram.setLoopAvailabled(coerced_loop)
			
	# further RE-test extend all available loops
	avloops = [l for l in diagram.loops if l.availabled]		
	for current_loop in avloops:	
		temporary_reachable = extendWithSingles(current_loop, True) # [TEMP] temporary +++						
		for coerced_loop,coercion_type in reversed(current_loop.extension_result.temporary_coerced_loops):
			assert coercion_type == COERCED_EXTEND
			diagram.collapseBack(coerced_loop)			
		# [dbg] test("Co", current_loop, reachable)

def unavail(loop, previous_loop):
	print("[ - "+str(lvl)+":unavailabled - ] ⟨ex:" + str(loop.extension_result.extended_count) + "|kd:" + str(loop.extension_result.killed_count) + "⟩ from root: " + loop.addr())
	
	diagram.setLoopUnavailabled(loop)
	previous_loop.extension_result.coerce(loop, COERCED_KILL, False) # [TEMP] not temporary ---
	
	# further RE-test extend all available loops
	avloops = [l for l in diagram.loops if l.availabled]		
	for current_loop in avloops:	
		temporary_reachable = extendWithSingles(current_loop, True) # [TEMP] temporary +++						
		for coerced_loop,coercion_type in reversed(current_loop.extension_result.temporary_coerced_loops):
			assert coercion_type == COERCED_EXTEND
			diagram.collapseBack(coerced_loop)		
			
	return single(previous_loop, True, False) # [TEMP] not temporary ---			
		# [dbg] test("Un", current_loop, reachable)			

'''
def next(lvl=0, path = [], lastExtendedNode = None):
	global bcc, fcc, sols_superperms
	bcc += 1
	
	lvl_seen = []
		
	# measure
	chloops = sorted(sorted(diagram.chains, key = lambda chain: len(chain.avloops))[0].avloops, key = lambda loop: (loop.firstNode().ktype, loop.firstNode().address))
		
	if bcc % 1 is 0:
		print("\n{lvl:"+str(lvl)+"§"+str(bcc)+"@"+tstr(time() - startTime)+"} | chains: " + str(len(diagram.chains)) + " | chloops: " + str(len(chloops)) + " | " + " ".join([str(k)+'/'+str(n) for k,n,_ in path]))
	#print("{lvl:"+str(lvl)+"} addr: " + " ".join([loop.head.address for _,_,loop in path]))
						
	# checks
	if len(chloops) is 0:
		#show(diagram)
		#print("{lvl:"+str(lvl)+"§"+str(bcc)+"} road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in path]))
		#print("{lvl:"+str(lvl)+"§"+str(bcc)+"} addr: " + " ".join([loop.head.address for _,_,loop in path]))
		#input("Found no chloops")
		
		if len(diagram.chains) is 1:# and len([c for c in diagram.cycles if not c.chain]) is 0:
			SP = diagram.superperm('000000', '000000')
			for node in diagram.nodes:
				assert node.perm in SP	
							
			dup = None
			if SP in sols_superperms: 
				dup = sols_superperms.index(SP)
			else:
				sols_superperms.append(SP)
				
			with open("sols."+str(diagram.spClass)+".log", 'a') as log:
				log.write("Found solution #"+str(fcc)+"\n")				
				log.write("{lvl:"+str(lvl)+"@"+str(bcc)+"@"+tstr(time() - startTime)+"} road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in path])+"\n")
				log.write("{lvl:"+str(lvl)+"@"+str(bcc)+"@"+tstr(time() - startTime)+"} addr: " + " ".join([loop.head.address for _,_,loop in path])+"\n")
				if dup is None:
					log.write(SP+"\n\n")
				else:
					log.write("duplicate of " + str(dup)+"\n\n")
								
			fcc += 1
			show(diagram)
			print("{lvl:"+str(lvl)+"§"+str(bcc)+"@"+tstr(time() - startTime)+"} road: " + " ".join([str(k)+'/'+str(n) for k,n,_ in path]))
			print("{lvl:"+str(lvl)+"§"+str(bcc)+"@"+tstr(time() - startTime)+"} addr: " + " ".join([loop.head.address for _,_,loop in path]))
			print("len:"+str(len(SP)) + "\n" + SP)
			input("Found solution #"+str(fcc))								
			
			# cleanup as we 'see' loops before this check
			# for loop in lvl_seen:
			# 	diagram.setLoopAvailabled(loop)
			# 	loop.seen = False
		
			return False
		else:
			# cleanup as we 'see' loops before this check
			# for loop in lvl_seen:
			# 	diagram.setLoopAvailabled(loop)
			# 	loop.seen = False
				
			return False
					
	# check if not enough loops to connect all the chains
	#if len(avloops) < (len(diagram.chains) - 1) / 5:
		#return False

						
	# run through and test available smallest chain loops
	for chindex, chloop in enumerate(chloops):
				
		# extend
		reachable, extended_loops, killed_loops = extend(chloop)
		print("{lvl:"+str(lvl)+"§"+str(bcc)+"} | extended @ " + str((chindex, len(chloops))) + " | ex: " + str(len(extended_loops)) + " | killed: " + str(len(killed_loops)) + " | " + str(chloop))
			
		if reachable:
				
			# carry on
			if next(lvl+1, path+[(chindex, len(chloops), chloop)]):
				return True

		# revert
		collapse(extended_loops, killed_loops)
		#print("{lvl:"+str(lvl)+"§"+str(bcc)+"} | collapsed back " + str((chindex, len(chloops))))
				
		# remember
		lvl_seen.append(chloop)
		chloop.seen = True
		diagram.setLoopUnavailabled(chloop)

	# forget
	for loop in lvl_seen:
		diagram.setLoopAvailabled(loop)
		loop.seen = False

	#print("{lvl:"+str(lvl)+"§"+str(bcc)+"} | forgotten")
										
	return False			
'''	

def extendAddress(addr):
	loop = diagram.nodeByAddress[addr].loop
	return extend(loop)
	
def point(diagram):
	diagram.pointers = []
		
	if len(diagram.chains) is 1 and len(list(diagram.chains)[0].cycles) is len(diagram.cycles):
		return
			
	chain_avlen, smallest_chain_group = (len(diagram.cycles), [])
	sorted_chain_groups = sorted(groupby(diagram.chains, K = lambda chain: len(chain.avloops)).items())
	if len(sorted_chain_groups) > 0:
		chain_avlen, smallest_chain_group	= sorted_chain_groups[0]		
	
	diagram.pointers += itertools.chain(*[[[n for n in loop.nodes if n.cycle.chain is chain][0] for loop in chain.avloops] if chain_avlen is not 0 else chain.cycles for chain in smallest_chain_group])																				
	print("[pointing] chain avlen: " + str(chain_avlen))
	
def tonoavail(addr):
	loop = diagram.nodeByAddress[addr].loop
	loop.seen = True
	diagram.setLoopUnavailabled(loop)
		

# ------------------------------------------------ #

def choose(): # ⇒ returns loop
	global lvl
	
	lvl += 1
	
	sorted_tuples = sorted([(-loop.extension_result.temporary_reachable, -loop.extension_result.temporary_extended_count, -loop.extension_result.temporary_killed_count, loop.firstNode().address, loop) for loop in diagram.loops if loop.availabled])
	loop = sorted_tuples[0][4]
			
	print("\n[ --- "+str(lvl)+":choose --- ] chosen: " + str(loop) + " with ⟨ex:"+str(loop.extension_result.temporary_extended_count)+"|kd:"+str(loop.extension_result.temporary_killed_count)+"⟩")
	return loop
	
	
def tryExtend(previous_loop):
	print("[ --- - --- try extend --- - --- ]")
	loop = choose()
	while not extend(loop):
		collapse(loop)
		if not unavail(loop, previous_loop): # [!!!] need to undo unavailabled loops from final single() call inside unavail(), but whence?
			# point(diagram)
			# show(diagram)
			print(str(lvl)+": utterly dead")
			return loop
		loop = choose()
		if lvl % 2000 is 0:
			point(diagram)
			show(diagram)
			input(str(lvl)+": %2000")	
	if not loop.extension_result.reachable:
		collapse(loop)
		unavail(loop, previous_loop)
		return loop
	print("[ --- - --- try extend --- - --- ] succesful with ⟨ex:" + str(loop.extension_result.extended_count) + "|kd:" + str(loop.extension_result.killed_count) + "⟩ from root: " + loop.addr())
	return loop
				
# ------------------------------------------------ #

if __name__ == "__main__":
	
	diagram = Diagram(7, 4)
	min_chains = len(diagram.chains)

	for node in diagram.nodes:
		if node.loop.availabled and node.ktype is 6:
			diagram.setLoopUnavailabled(node.loop)

	lvl = 0 # [~] current lvl is the one currently chosen
	
	extendAddress('100002')
	extendAddress('100011')
	extendAddress('100020')
	extendAddress('100044')
	extendAddress('100053')
	
	extendAddress('101005')
	extendAddress('101105')
	extendAddress('101205')
	extendAddress('101305')

	extendAddress('102005')
	extendAddress('102105')
	extendAddress('102205')
	extendAddress('102305')

	extendAddress('103005')
	extendAddress('103105')
	extendAddress('103205')
	extendAddress('103305')

	extendAddress('113005')
	extendAddress('113105')
	extendAddress('113205')
	extendAddress('113305')
	
	extendAddress('123005')
	extendAddress('123105')
	extendAddress('123205')
	extendAddress('123305')

	extendAddress('112005')
	extendAddress('112105')
	extendAddress('112205')
	extendAddress('112305')
	
	extendAddress('122005')
	extendAddress('122105')
	extendAddress('122205')
	extendAddress('122305')

	extendAddress('023005')
	extendAddress('023105')
	extendAddress('023205')
	extendAddress('023305')

	extendAddress('013005')
	extendAddress('013105')
	extendAddress('013205')
	extendAddress('013305')
																															
	l0 = diagram.nodeByAddress['000001'].loop
	print("[l0] " + l0.addr())
	extend(l0)

	point(diagram)
	show(diagram)
	input('partial')
															
	max_lvl = 0				
	def next(lvl, previous_loop):
		global max_lvl
		
		while True:
			current_loop = tryExtend(previous_loop)
			print("[L:"+str(lvl)+"] ⟨ex:" + str(current_loop.extension_result.extended_count) + "|kd:" + str(current_loop.extension_result.killed_count) + "⟩ from root: " + current_loop.addr() + " | reachable: " + str(current_loop.extension_result.reachable))
			if lvl > max_lvl:
				max_lvl = lvl
				input("max_lvl: " + str(max_lvl))

			if current_loop.extension_result.reachable == False:
				return
			else:
				next(lvl+1, current_loop)

				collapse(current_loop)					 
				assert unavail(current_loop, previous_loop)
					# return

	next(1, l0)



	point(diagram)
	show(diagram)
	
	# input('partial')
	# 
	# 
	# startTime = time()
	# sols_superperms = []
	# bcc = -1
	# fcc = 0
	# 
	# next()
	# 
	# show(diagram)
	# input('done.')
	
