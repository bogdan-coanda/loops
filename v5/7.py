from diagram import *
from uicanvas import *
import itertools



def extendAddress(addr):
	loop = diagram.nodeByAddress[addr].loop
	assert diagram.extendLoop(loop)
	diagram.cleanExtension(loop)
	
		
def extendColumn(column_addr, key):
	i = 0
	j = key
	while i < diagram.spClass-1:
		extendAddress(column_addr+str(i)+str(j))
		if j > 0:
			i += 1
			j -= 1
		else:
			i += 2
			j = diagram.spClass - 3

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
	

def cleanup(lvl, extended_loop):
	diagram.cleanexCount += 1

	if diagram.cleanexCount == 274:
		
		diagram.pointers = extended_loop.nodes
		show(diagram)
		input("[cleanup] started for extended_loop: " + str(extended_loop))
									
	ice = 0	
	while True:			
		for chain in diagram.chains:
			if len(chain.avloops) is 0:
				return 
		
		avcount = 0
		potentcount = 0
		deadcount = 0
		for loop in diagram.loops:
			if loop.availabled:			
				avcount += 1
				
				if diagram.cleanexCount == 274 and avcount == 55:
					
					diagram.pointers = loop.nodes
					show(diagram)
					input("[cleanup] will extend: " + str(loop))
					
					diagram.pointers = itertools.chain(*[chain.cycles for chain in loop_lvl_extension_result[(loop, lvl-1)][3]])
					show(diagram)
					input("[cleanup] previous touched chains: " + str(loop_lvl_extension_result[(loop, lvl-1)][3]))
					
					
				# filtering, nice as it seems, doesn't work!									
				Δ = loop_lvl_extension_result[(loop, lvl-1)][3].intersection(loop_lvl_extension_result[(extended_loop, lvl)][3]) if lvl is not 0 else []
				hasPotential = lvl is 0 or len(Δ) 
				if hasPotential:
					potentcount += 1

				if diagram.cleanexCount == 274 and avcount == 55:
					
					diagram.pointers = itertools.chain(*[chain.cycles for chain in loop_lvl_extension_result[(extended_loop, lvl)][3]])
					show(diagram)					
					print("[cleanup] extended loop current touched chains: " + str(loop_lvl_extension_result[(extended_loop, lvl)][3]))								
					
					diagram.pointers = itertools.chain(*[chain.cycles for chain in Δ])
					show(diagram)										
					print("[cleanup] Δ: " + str(Δ))
																							
				assert diagram.extendLoop(loop)
				loop_lvl_extension_result[(loop, lvl)] = loop.extension_result	

				if diagram.cleanexCount == 274 and avcount == 55:
					
					diagram.pointers = itertools.chain(*[chain.cycles for chain in loop_lvl_extension_result[(loop, lvl-1)][3]])
					show(diagram)
					input("[cleanup] current touched chains: " + str(loop_lvl_extension_result[(loop, lvl)][3]))
															
				valid = True
				for touched_chain in loop.extension_result[3]:
					if len(touched_chain.avloops) is 0:
						
						if diagram.cleanexCount == 274 and avcount == 55:
							
							diagram.pointers = touched_chain.cycles
							show(diagram)
							input("[cleanup] failed chain: " + str(touched_chain.cycles))
											
						valid = False
						assert hasPotential, "no potential !?"
						break

				if diagram.cleanexCount == 274 and avcount == 55:
					diagram.pointers = loop.nodes
					show(diagram)
					input("[cleanup] will collapse back: " + str(loop))								
						
				diagram.collapseBack(loop)

				if not valid:
					diagram.setLoopUnavailabled(loop)
					deadcount += 1
					extended_loop.extension_result[1].append(loop)
					extended_loop.extension_result[3].update([node.cycle.chain for node in loop.nodes])
					loop_lvl_extension_result[(extended_loop, lvl)][1].append(loop)
					loop_lvl_extension_result[(extended_loop, lvl)][3].update([node.cycle.chain for node in loop.nodes])
		
		print("[cleanex:"+str(ice)+"@"+str(diagram.cleanexCount)+"] tried " + str(avcount) + " available loops | with " + str(potentcount) + " potentials ("+str(round(potentcount*100/avcount, 2))+"%) ⇒ " + str(deadcount) + " cleaned")
		if deadcount is 0:
			return
		ice += 1
		
			



def next(lvl=0, path = [], lastExtendedNode = None):
	global bcc, fcc, sols_superperms
	bcc += 1
	
	lvl_seen = []
		
	# measure
	chloops = sorted(sorted(diagram.chains, key = lambda chain: len(chain.avloops))[0].avloops, key = lambda loop: (loop.firstNode().ktype, loop.firstNode().address))
		
	if bcc % 10 is 0:
		print("{lvl:"+str(lvl)+"§"+str(bcc)+"@"+tstr(time() - startTime)+"} | chains: " + str(len(diagram.chains)) + " | chloops: " + str(len(chloops)) + " | " + " ".join([str(k)+'/'+str(n) for k,n,_ in path]))
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
				assert nod;fe.perm in SP	
							
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
		if diagram.extendLoop(chloop):	
			#print("{lvl:"+str(lvl)+"§"+str(bcc)+"} | extended " + str((chindex, len(chloops), chloop)))
			
			valid = True
			for touched_chain in chloop.extension_result[3]:
				if len(touched_chain.avloops) is 0:
					valid = False
					#print("{lvl:"+str(lvl)+"§"+str(bcc)+"} | has unreachable chains " + str((chindex, len(chloops), chloop)))
					break

			if valid:		
				
				loop_lvl_extension_result[(chloop, lvl)] = chloop.extension_result
				
				#diagram.cleanExtension(chloop)
				cleanup(lvl, chloop)
				#print("{lvl:"+str(lvl)+"§"+str(bcc)+"} | cleaned " + str((chindex, len(chloops), chloop)))
				
				# carry on
				if next(lvl+1, path+[(chindex, len(chloops), chloop)]):
					return True

			# revert
			diagram.collapseBack(chloop)
			#print("{lvl:"+str(lvl)+"§"+str(bcc)+"} | collapsed back " + str((chindex, len(chloops), chloop)))
				
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
	
																																					
			
if __name__ == "__main__":
	
	diagram = Diagram(7, 4)

	loop_lvl_extension_result = {}
		
	# tonoavail('100006')
	# 
	# tonoavail('103006')
	# tonoavail('103106')
	# tonoavail('103206')
	# tonoavail('103306')
	# tonoavail('103406')
	# 
	# tonoavail('122006')
	# tonoavail('122106')
	# tonoavail('122206')
	# tonoavail('122306')
	# tonoavail('122406')
	# 
	# tonoavail('111006')
	# tonoavail('111106')
	# tonoavail('111206')
	# tonoavail('111306')
	# tonoavail('111406')
	# 
	# tonoavail('103405')

	# for node in diagram.nodes:
	# 	if node.address.endswith('06') and node.cycle.chain is None and node.loop.availabled and not node.address.startswith('0') and not node.address.startswith('113') and not node.address.startswith('101') and not node.address.startswith('112') and not node.address.startswith('111') and not node.address.startswith('102'):
	# 		diagram.extendLoop(node.loop)
		
	# for node in diagram.nodes:
	# 	if (
	# 		node.address.startswith('101') or
	# 		node.address.startswith('102') or
	# 		node.address.startswith('011') or
	# 		node.address.startswith('022') or
	# 		node.address.startswith('121') or
	# 		node.address.startswith('122')
	# 	) and node.address[-2] != '0' and node.address[-2] != '5' and node.ktype > 1 and node.loop.availabled and node.cycle.chain is None:
	# 		tonoavail(node.address)
	# 
	# tonoavail('103405')
		
	# ~~~ #
	
	# extendAddress('000001')
	# 
	# extendAddress('100106')
	# extendAddress('100206')
	# extendAddress('100306')
	# extendAddress('100406')
	# 
	# extendAddress('103005')
	# extendAddress('103105')
	# extendAddress('103205')
	# extendAddress('103305')
	# 
	# extendAddress('100020')
	# 
	# extendAddress('123001')
	# extendAddress('123003')
	# extendAddress('123005')
	# extendAddress('123111')
	# extendAddress('123113')
	# extendAddress('123115')
	
	#extendAddress('102142')
		
	# point(diagram)
	# 
	# show(diagram)
	# input('partial')
	# 
	# while True:
	# 	deadloops = []
	# 	for loop in diagram.loops:
	# 		if loop.availabled:			
	# 			assert diagram.extendLoop(loop)
	# 			valid = True
	# 			for touched_chain in loop.extension_result[3]:
	# 				if len(touched_chain.avloops) is 0:
	# 					valid = False
	# 					break
	# 			diagram.collapseBack(loop)
	# 			if not valid:
	# 				diagram.setLoopUnavailabled(loop)
	# 				deadloops.append(loop)
	# 
	# 	diagram.pointers = itertools.chain(*[loop.nodes for loop in deadloops])
	# 	show(diagram)
	# 	input("[deadloops] count: " + str(len(deadloops)) + " | " + str(deadloops))
	# 
	# 	if len(deadloops) is 0:
	# 		break
			
				
	startTime = time()
	sols_superperms = []
	bcc = -1
	fcc = 0
					
	next()
	
	show(diagram)
	input('done.')
	
