from diagram import *
from uicanvas import *
from common import *
from mx import *
from time import time

max_jump_lvl_reached = 0
min_jump_unicycles = 99999999999999

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
	global max_jump_lvl_reached, min_jump_unicycles
	
	def key():
		return f"[{tstr(time() - startTime):>11}][lvl:{lvl}]" 
	
	print(f"{key()} {'.'.join([(str(x)+upper(t)) for x,t,_ in path])}")
	
	min_chlen = mx.min_chain_avloops_length()	
	# print(f"{key()}[mx] 1. min_chlen: {min_chlen}")	
	
	if min_chlen == 0:
		# print(f"{key()}[mx] ⇒ dead @ unconnectable")
		return
		
	unicycle_chains = mx.filter_unicycle_chains()	
	# print(f"{key()}[mx] 2. unicycle chains: {len(unicycle_chains)}")	
				
	if len(unicycle_chains) == 0:
		input2(f"{key()}[mx] ⇒ all cycles covered by tuples !!!")
		step([l for l in diagram.loops if l.availabled], lvl, path)
		input2(f"[jump] « [step] // cc")
		return			
		
	avtuples = mx.filter_avtuples(avtuples)	
	# print(f"{key()}[mx] 3. avtuples: {len(avtuples)} / {len(diagram.loop_tuples)}")	

	if len(unicycle_chains) <= min_jump_unicycles:
	#if lvl >= max_jump_lvl_reached:
		# t13-05 # t12-03
		with open('8d-t10-b0b1-min_unicycles_reached', 'a', encoding="utf8") as log:
			if len(unicycle_chains) < min_jump_unicycles:
			#if lvl > max_jump_lvl_reached:				
				log.write("-------------------------" + "\n\n")
			log.write(f"{key()} {'.'.join([(str(x)+upper(t)) for x,t,_ in path])}" + "\n")
			log.write(f"tuples: {' '.join([a for _,_,a in path])}" + "\n")
			log.write(f"{key()}[mx] 1. min_chlen: {min_chlen}" + "\n")	
			log.write(f"{key()}[mx] 2. unicycle chains: {len(unicycle_chains)}" + "\n")	
			log.write(f"{key()}[mx] 3. avtuples: {len(avtuples)} / {len(diagram.loop_tuples)}" + "\n\n")	
			#max_jump_lvl_reached = lvl		
			min_jump_unicycles = len(unicycle_chains)

	if len(avtuples) == 0:
		# print(f"{key()}[mx] ⇒ no tuples remaining")
		step([l for l in diagram.loops if l.availabled], lvl, path)
		input2(f"[jump] « [step] // nt")
		return			
				
	min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples)	
	# print(f"{key()}[mx] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {len(min_matched_tuples)}")		

	if len(min_nodes) == 0:
		# print(f"{key()}[mx] ⇒ dead @ not coverable")
		return
		
	if lvl < 1 and len(min_nodes) > 1:
		# print(f"{key()}[mx] ⇒ not single choice, purging…")
		
		# [~] next_single_choices is unused ?
		avtuples, next_sample_lengths, next_single_choices = mx.purge(avtuples, unicycle_chains)
		# print(f"{key()}[mx][purge] avtuples: {len(avtuples)} | sample lengths: {sorted(groupby(next_sample_lengths.items(), K = lambda p: p[1], G = lambda g: len(g)).items())} | single choices: {len(next_single_choices)}")

		if len(avtuples) == 0:
			# print(f"{key()}[mx][purge] ⇒ no tuples remaining")
			step([l for l in diagram.loops if l.availabled], lvl, path)
			input2(f"[jump] « [step] // nt")
			return			
												
		min_ratio, min_cycle, min_nodes, min_matched_tuples = mx.find_min_matched_tuples(unicycle_chains, avtuples, next_sample_lengths)
		# print(f"{key()}[mx][purge] ⇒ mr: {min_ratio} | mc: {min_cycle} | mn: {[n.address for n in min_nodes]} | mt: {[next_sample_lengths[t] for t in min_matched_tuples]}")
	else:
		# print(f"{key()}[mx] ⇒ single choice.")
		pass
		
	# go through all choices
	for it, t in enumerate(min_matched_tuples):
		# if lvl == 0 and it < 1:
		# 	avtuples.remove(t)
		# 	continue
		if t in avtuples: # [~][!] needed if no purge
						
			ec = 0
			for lt, l in enumerate(t):
				if diagram.extendLoop(l):
					ec += 1
				else:
					break
	
			if ec == len(t): # if we've extended all of the tuple's loops
				jump(avtuples, lvl+1, path+[(it,len(min_matched_tuples),t[0].nodes[0].address)])
	
			for l in reversed(t[:ec]):
				diagram.collapseBack(l)	
				
			# remove tested choice for further jumps		
			avtuples.remove(t)

	# print(f"{key()} ⇒ finished all choices")
	
	
# ========================================== #


def simple_step(lvl=0, path=[]):
	global sid
	
	def key():
		return f"[{sid}][{tstr(time() - startTime):>11}][lvl:{lvl}]"
		
	if sid % 1 == 0:
		print(f"{key()}[ch:{len(diagram.chains)}|av:{len([l for l in diagram.loops if l.availabled])}] {'.'.join([(str(x)+upper(t)) for x,t in path])}")
	sid += 1

	if len(diagram.chains) == 1:
		show(diagram)
		input2(f"{key()} sol found.")
		return
	
	seen, mcpel = clean()
	
	min_avsum = 99999999999
	min_chain = list(diagram.chains)[0]
	for chain in diagram.chains:
		avsum = sum([mcpel[n.loop] for n in chain.avnodes])+len(chain.avnodes)
		if avsum < min_avsum:
			min_avsum = avsum
			min_chain = chain

	input2(f"{key()} chosen min: {min_chain} with sum: {min_avsum}")
																					
	#min_chain = sorted(diagram.chains, key = lambda chain: (len(chain.avnodes), chain.id))[0]
	
	min_avlen = len(min_chain.avnodes)
		
	for i,n in enumerate(sorted(min_chain.avnodes, key = lambda n: n.address)):
		assert diagram.extendLoop(n.loop)		
		simple_step(lvl+1, path+[(i, min_avlen)])
		diagram.collapseBack(n.loop)	
		
		seen.append(n.loop)
		diagram.setLoopUnavailabled(n.loop)
		
	for l in seen:
		diagram.setLoopAvailabled(l)
		

def clean():
	
	avloops = [l for l in diagram.loops if l.availabled]
	print(f"[clean] avloops: {len(avloops)}")

	unavailed = []
	min_chlen_per_extended_loop = {}
	
	for il,loop in enumerate(avloops):
		
		passed = diagram.extendLoop(loop)
		#print(f"[clean] {loop} | extend: {passed}")
		if passed:
			min_chlen = min([len(ch.avnodes) for ch in diagram.chains])
			if min_chlen == 0:
				passed = False
			else:
				min_chlen_per_extended_loop[loop] = min_chlen
			#print(f"[clean] {loop} | min_chlen: {passed}")
			diagram.collapseBack(loop)		
					
		if not passed:
			unavailed.append(loop)
			diagram.setLoopUnavailabled(loop)
		
	print(f"[clean] ⇒ unavailed: {len(unavailed)}")
	return unavailed, min_chlen_per_extended_loop	
	

if __name__ == "__main__":

	diagram = Diagram(8, 1)
	mx = MX(diagram)
		
	import enav
	enav.diagram = diagram
	from enav import *	

	nx = []

	# ---------------------------- #
	
	extend('0000001')
	# extend('0000165')
	# extend('0000201')
	# extend('0000365')	
	# extend('0000401')
	# extend('0000565')	
	
	nx += elt('1000007', 5)
	nx += elt('1200407', 3)
	nx += est('1200507', 2)
	nx += est('1200107', 6)
	
	nx = est('1000207', 2)
	nx = est('1002107', 4)
	nx = elt('1002007', 5)
	nx = elt('1002407', 7)

	# ============================ #

	# - (A) - upper - [0:13] ~ 0000.0001.0002.0003.0004.0030.0031.0120.0210.1000.1001.1010.1100
	# - dead(§) -	# ⟨column:4@0000001(ktype:6)|t:6|cL:36|bb:13⟩
	# - dead(§) -	# ⟨column:2@0000003(ktype:4)|t:6|cL:36|bb:13⟩
	# - dead(§) -	# ⟨column:0@0000005(ktype:2)|t:3|cL:18|bb:13⟩		
	# - (A) - lower - [31:13] ~ 0134.0224.0233.0234.1024.1114.1203.1204.1230.1231.1232.1233.1234
	# ec('0134002') # ⟨column:123@0134002(ktype:6)|t:6|cL:36|bb:13⟩	
	# ec('0134200') # ⟨column:126@0134200(ktype:6)|t:6|cL:36|bb:13⟩	
	# ec('0134404') # ⟨column:127@0134404(ktype:6)|t:3|cL:18|bb:13⟩	
	
	# - (N) - upper - [13:26] ~ 0010.0011.0012.0013.0020.0021.0022.0023.0024.0100.0101.0102.0103.0104.0110.0111.0133.0200.0201.0223.0230.0231.1020.1110.1201.1202
	# - dead(1:elt:a) - # ⟨column:45@0010000(ktype:6)|t:6|cL:36|bb:26⟩
	# - dead(0:elt:a) - # ⟨column:50@0010204(ktype:6)|t:6|cL:36|bb:26⟩
	# ec('0010303') # ⟨column:52@0010303(ktype:6)|t:6|cL:36|bb:26⟩
	# ec('0010402') # ⟨column:55@0010402(ktype:6)|t:6|cL:36|bb:26⟩
	# ec('0010501') # ⟨column:57@0010501(ktype:6)|t:6|cL:36|bb:26⟩
	# - (N) - lower - [23:26] ~ 0032.0033.0124.0214.1003.1004.1011.1033.1034.1101.1123.1124.1130.1131.1132.1133.1134.1210.1211.1212.1213.1214.1221.1222.1223.1224
	# ec('0032000') # ⟨column:97@0032000(ktype:6)|t:6|cL:36|bb:26⟩
	# - dead(0:elt:z) - # ⟨column:98@0032204(ktype:6)|t:6|cL:36|bb:26⟩
	# ec('0032303') # ⟨column:99@0032303(ktype:6)|t:6|cL:36|bb:26⟩
	# ec('0032402') # ⟨column:100@0032402(ktype:6)|t:6|cL:36|bb:26⟩
	# ec('0032501') # ⟨column:101@0032501(ktype:6)|t:6|cL:36|bb:26⟩
		
	# - (F) - upper - [8:15] ~ 0002.0003.0030.0120.0121.0130.0203.0212.1001.1010.1014.1023.1030.1032.1103
	# - dead(ex:y) - # ⟨column:28@0002000(ktype:5)|t:6|cL:36|bb:15⟩
	# - dead(ex:a) - # ⟨column:34@0002204(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0002303') # ⟨column:36@0002303(ktype:5)|t:3|cL:18|bb:15⟩
	# - (F) - lower - [29:15] ~ 0131.0202.0204.0211.0220.0224.0233.1022.1031.1104.1113.1114.1204.1231.1232
	# ec('0131001') # ⟨column:119@0131001(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0131100') # ⟨column:120@0131100(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0131304') # ⟨column:121@0131304(ktype:5)|t:3|cL:18|bb:15⟩
	
	# - (P₁) - upper - [14:15] ~ 0011.0012.0021.0101.0110.0111.0112.0113.0114.0132.0221.0222.1021.1111.1112
	# ec('0011001') # ⟨column:58@0011001(ktype:4)|t:6|cL:36|bb:15⟩
	# - dead(1:elt:z) - # ⟨column:60@0011100(ktype:4)|t:6|cL:36|bb:15⟩
	# ec('0011502') # ⟨column:63@0011502(ktype:4)|t:3|cL:18|bb:15⟩
	# - (P₁) - lower - [28:15] ~ 0122.0123.0213.1012.1013.1102.1120.1121.1122.1123.1124.1133.1213.1222.1223
	# ec('0122000') # ⟨column:116@0122000(ktype:6)|t:6|cL:36|bb:15⟩
	# ec('0122204') # ⟨column:117@0122204(ktype:6)|t:6|cL:36|bb:15⟩
	# ec('0122501') # ⟨column:118@0122501(ktype:6)|t:3|cL:18|bb:15⟩

	# - (P₂) - upper - [15:15] ~ 0011.0012.0021.0101.0110.0111.0112.0114.0123.0132.0221.1012.1021.1112.1121
	# - dead(1:elt:a) - # ⟨column:59@0011000(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0011204') # ⟨column:61@0011204(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0011303') # ⟨column:62@0011303(ktype:5)|t:3|cL:18|bb:15⟩
	# - (P₂) - lower - [26:15] ~ 0113.0122.0213.0222.1013.1102.1111.1120.1122.1123.1124.1133.1213.1222.1223
	# ec('0113002') # ⟨column:110@0113002(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0113101') # ⟨column:111@0113101(ktype:5)|t:6|cL:36|bb:15⟩
	# ec('0113200') # ⟨column:112@0113200(ktype:5)|t:3|cL:18|bb:15⟩
				
	# ============================ #	
		
	caddrs = [
		# [t10-a1a4] unicycle chains: 108
		'0001110', # a0
		'0001511', # a1
		'0002225', # a2
		'0023413', # a3
		'0023512', # a4
		#'0113011',
		
		# '0010225', # b0
		# '0033210', # b1
		'0023111', # b2
		#'0001225', 	
		'0002413', # b3
		'0002025', # b4
		'0010110', # b5
		'0134012'  # b6
	]
	ctuples = itertools.chain(*[c.tuples for c in diagram.columns if c.firstNode.address in caddrs])
	
	extended = []
	for tuple in ctuples:
		for loop in tuple:
			if diagram.extendLoop(loop):
				extended.append(loop)
			else:
				break
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #		
		
	min_chlen = mx.min_chain_avloops_length()	
	print(f"[mx] 1. min chain avloops length: {min_chlen}")	
	
	unicycle_chains = mx.filter_unicycle_chains()	
	print(f"[mx] 2. unicycle chains: {len(unicycle_chains)}")	
		
	avtuples = mx.filter_avtuples()	
	print(f"[mx] 3. avtuples: {len(avtuples)} | all tuples: {len(diagram.loop_tuples)}")		
	
	# diagram.pointers = list(itertools.chain(*[l.nodes for l in extended]))
	# show(diagram)
	
	startTime = time()
	jump(avtuples)
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #		
		
	# nx = et('1000206')
	# nx = et('1000107')
	# nx = et('1000307')
	# nx = et('1000407')
	# nx = et('1000507')
	# 
	# nx = et('1001106')
	# nx = et('1001007')
	# nx = et('1001207')
	# nx = et('1001307')
	# nx = et('1001407')
	# 
	# nx = et('1003406')
	# nx = et('1003107')
	# nx = et('1003207')
	# nx = et('1003307')
	# nx = et('1003507')
	# 
	# nx = et('1004306')
	# nx = et('1004007')
	# nx = et('1004107')
	# nx = et('1004207')
	# nx = et('1004407')
	# 
	# nx = et('1020406')
	# nx = et('1020007')
	# nx = et('1020107')
	# nx = et('1020307')
	# nx = et('1020507')
	# 
	# nx = et('1024106')
	# nx = et('1024007')
	# nx = et('1024207')
	# nx = et('1024407')
	# nx = et('1024507')		
	# 
	# nx = et('1033106')
	# nx = et('1033007')
	# nx = et('1033207')
	# nx = et('1033407')
	# nx = et('1033507')
	# 
	# nx = et('1110406')
	# nx = et('1110007')
	# nx = et('1110107')
	# nx = et('1110307')
	# nx = et('1110507')
	# 
	# nx = et('1114106')
	# nx = et('1114007')
	# nx = et('1114207')
	# nx = et('1114407')
	# nx = et('1114507')
	# 
	# nx = et('1123106')
	# nx = et('1123007')
	# nx = et('1123207')
	# nx = et('1123407')
	# nx = et('1123507')
	# 
	# nx = et('0010406')
	# nx = et('0010107')
	# nx = et('0010207')
	# nx = et('0010307')
	# nx = et('0010507')
	# 
	# nx = et('0011306')
	# nx = et('0011007')
	# nx = et('0011107')
	# nx = et('0011207')
	# nx = et('0011407')

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #		

	# nx = extend('0020015') # 0/2 {5:g,7:b}
	# nx = extend('0020151') # 0/1 {g}
	# nx = extend('0020020') # 0/2 {0:k,4:g}
	# nx = extend('0020115') # 0/1 {g}
	# nx = extend('0020124') # 0/1 {g}
	# nx = extend('0020415') # 0/1 {g}
	# nx = extend('0020460') # 0/1 {g}

	# et('1234006') # 0/2 {g}
	
	# clean()
	
	# startTime = time(); sid = 0; step()

	# nx = extend('1234015') # 0/2 {5:g,7:b}
	# nx = extend('1234151') # 0/1 {g}
	# nx = extend('1234024') # 1/2 {0:v,4:g}
	# nx = extend('1234124') # 0/1 {g}
	# nx = extend('1234115') # 0/1 {g}
	# nx = extend('1234042') # 1/2 {0:k,2:g}
	
	# nx = extend('1234110') # 1/5
	# nx = extend('1234040') # 0/3
	# nx = extend('1234240') # 0/4
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #		
			
	# nx = extend('0010000')
	# 
	# nx = extend('0020006')
	# nx = extend('0020106')
	# nx = extend('0020206')
	# nx = extend('0020306')
	# nx = extend('0020406')
	# nx = extend('0020506')
	# 
	# nx = extend('0020036')
	# nx = extend('0020146')
	
	# ---------------------------- #

	# extend('0000501')	
	# 
	# el('0001407', 6)
	# el('1002307', 3)
	# el('1002207', 4)
	# el('1002107', 5)
	# el('1002007', 2)	
	
	# extend('0000401')	
	# 
	# el('0004507', 7)
	# el('0014407', 4)
	# el('0014307', 5)
	# el('0014207', 6)
	# el('0014107', 3)
	# 
	# extend('0000301')
	# 
	# el('0031307', 2)
	# el('0034407', 5)
	# el('0034307', 6)
	# el('0034207', 7)
	# el('0034107', 4)
	# 
	# extend('0000201')
	# 
	# el('0210207', 3)
	# el('0232207', 6)
	# el('0232107', 7)
	# el('0232007', 2)
	# el('0232507', 5)
	# 
	# extend('0000101')
	# 
	# el('1100107', 4)
	# el('1220107', 7)
	# el('1220007', 2)
	# el('1220507', 3)
	# el('1220407', 6)
	# 
	# extend('0000001')
	# 
	# el('1000007', 5)
	# el('1200007', 2)
	# el('1200507', 3)
	# el('1200407', 4)
	# el('1200307', 7)	
	# 
	# nx = []
	# nx += extend('0000065')
	# 
	# nx += el('0004107', 4)
	# nx += el('0034307', 6)
	# nx += el('0034407', 5)
	# nx += el('0034507', 2)		
	# nx += el('0034007', 3)		
		
	# ---------------------------- #

	# extend('0000001')
	# 
	# el('1000007', 2)
	# el('1000507', 3)
	# el('1000407', 4)
	# el('1000307', 5)
	# el('1004107', 7)
	# 
	# el('1010007', 2)
	# el('1010507', 3)
	# el('1010407', 4)
								
	# ---------------------------- #
	
	# el('1000007', 5)
	# el('0100007', 2)
	# el('1210007', 7)
	# el('1201007', 4)
	# el('1200007', 3)
	# 
	# extend('0000001')
	# 
	# el('1001007', 5)
	# el('0102007', 3)
	# el('1211007', 2)
	# el('1212407', 6)
	# el('1213307', 7)
	# el('1221407', 4)
	# 
	# el('1000107', 3)
	# el('1031107', 2)
	# el('1004207', 7)
	# el('1030207', 5)
	# el('1020307', 6)
	# el('1013207', 4)
	
	# ---------------------------- #
		
	#diagram.point()
	#diagram.pointers += list(itertools.chain(*[n.loop.nodes for n in nx]))	
	# diagram.pointers = list(itertools.chain(*[n.loop.nodes for n in diagram.nodes if n.loop.availabled and n.ktype > 1 and n.address.startswith('00200')]))
	#show(diagram)
	print('[done]')
