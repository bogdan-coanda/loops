from diagram import *
from uicanvas import *


if __name__ == "__main__":
	
	diagram = Diagram(7, 4)
	
	def extend(addr):
		assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	def collapse(addr):
		diagram.collapseBack(diagram.nodeByAddress[addr].loop)
	def single():
		singles = []
		diagram.point()
		while diagram.pointer_avlen == 1 and len(diagram.pointers):
			singles.append(diagram.pointers[0].loop)
			diagram.extendLoop(diagram.pointers[0].loop)
			diagram.point()
		return singles			
	def trial(loops, __show__=False):
		zeroes = []
		avLoop = None
		bestAv = None
		for loop in loops:
			if loop.availabled:			
				diagram.extendLoop(loop)
				singles = single()		
				if diagram.pointer_avlen == 0:
					zeroes.append(loop)
				elif len(zeroes) == 0:
					currAv = len([l for l in diagram.loops if l.availabled])
					if bestAv is None or currAv < bestAv:
						avLoop = loop
						bestAv = currAv						
				#result = ((diagram.pointer_avlen, -len(singles), len([l for l in diagram.loops if l.availabled]), -len(diagram.pointers)), loop)				
				for l in reversed(singles):
					diagram.collapseBack(l)					
				diagram.collapseBack(loop)						
		return (zeroes, avLoop, bestAv)
		
	qq = -1
	def next(lvl=0):
		global qq
		if len(diagram.chains) is 1 and len(list(diagram.chains)[0].cycles) is len(diagram.cycles):
			show(diagram); input("[lvl:"+str(lvl)+"|ext:"+str(len([l for l in diagram.loops if l.extended]))+"] SOLUTION!!!")
			
		lvl_seen = []
		
		while True:		
			qq += 1
			avloops = [l for l in diagram.loops if l.availabled]
			if len(avloops) == 0 or len([chain for chain in diagram.chains if len(chain.avloops) == 0]): # no loops to trial or has unreachable chains
				break
			
			print("[qq:"+str(qq)+"][lvl:"+str(lvl)+"|ext:"+str(len([l for l in diagram.loops if l.extended]))+"|seen:"+str(len(lvl_seen))+"] avloops: " + str(len(avloops)))					
			zeroes, avLoop, bestAv = trial(avloops)			
			
			if len(zeroes):
				print("[qq:"+str(qq)+"][lvl:"+str(lvl)+"|ext:"+str(len([l for l in diagram.loops if l.extended]))+"|seen:"+str(len(lvl_seen))+"] trial | zeroes: " + str(len(zeroes)))
				for loop in zeroes:
					diagram.setLoopUnavailabled(loop)
					lvl_seen.append(loop)
				
			else:
				diagram.extendLoop(avLoop)
				singles = single()
				print("[qq:"+str(qq)+"][lvl:"+str(lvl)+"|ext:"+str(len([l for l in diagram.loops if l.extended]))+"|seen:"+str(len(lvl_seen))+"] trial: " + str(bestAv) + " | loop: " + str(avLoop))				
				if lvl > 17:
					show(diagram); input()
				
				next(lvl+1)
				
				for loop in reversed(singles):
					diagram.collapseBack(loop)					
				diagram.collapseBack(avLoop)									
				
				diagram.setLoopUnavailabled(avLoop)
				lvl_seen.append(avLoop)
				
		# after while
		for loop in lvl_seen:
			diagram.setLoopAvailabled(loop)
			
			
	next()
		
		
		
		
		
		
		
	'''	
	# (4, 0, 629, -16): 108
	# 010033 010302 010311 010320 010353 010443 011024 011203 011221 011230 011254 011434 013010 013020 013100 013133 013142 013151 013200 013224 013233 013251 013420 013430 020010 020100 020133 020142 020151 020420 021033 021302 021311 021320 021353 021443 100012 100102 100120 100144 100153 100333 101020 101200 101224 101233 101251 101430 120004 120005 120006 120013 120014 120022 120023 120031 120032 120040 120041 120103 120106 120112 120121 120130 120154 120202 120206 120211 120220 120244 120253 120301 120306 120310 120334 120343 120352 120406 121005 121006 121014 121023 121032 121041 121106 121206 121306 121406 122005 122006 122014 122023 122032 122041 122106 122206 122306 122406 123005 123006 123014 123023 123032 123041 123106 123206 123306 123406
	extend('010033')
	
	# (2, 0, 622, -2): 1
	# 120032
	extend('120032')
		
	# (2, 0, 611, -2): 4
	# 001044 001134 002043 010443
	extend('001044')
		
	# (2, 0, 596, -2): 2
	# 010353 010443
	extend('010353')
	
	# (2, 0, 583, -4): 1
	# 010302
	extend('010302')
	
	# (2, -1, 569, -2): 2
	# 011024 020100
	extend('011024')
	
	# (2, -1, 556, -2): 1
	# 000053
	extend('000053')
			
	# (2, -1, 539, -2): 1
	# 000002
	extend('000002')
	
	# (2, -1, 525, -4): 1
	# 003134
	extend('003134')
	
	# (2, -1, 513, -4): 1
	# 100031
	extend('100031')
	
	# (2, -1, 497, -6): 2
	# 000421 020022
	extend('000421')
	
	# (2, -1, 477, -12): 1
	# 001303
	extend('001303')
	
	# (2, -3, 447, -24): 1
	# 020411
	extend('020411')
	
	# (0, 0, 436, -1): 1
	# 120023
	diagram.setLoopUnavailabled(diagram.nodeByAddress['120023'].loop)
	
	# (2, -4, 412, -18): 1
	# 012421
	extend('012421')
	
	# (2, -5, 367, -34): 1
	# 010005
	extend('010005')
	
	# (0, -26, 194, -1): 1
	# 012053
	diagram.setLoopUnavailabled(diagram.nodeByAddress['012053'].loop)
	
	# (0, -7, 302, -1): 1
	# 012006
	diagram.setLoopUnavailabled(diagram.nodeByAddress['012006'].loop)
	
	# (0, -3, 321, -2): 1
	# 122006
	diagram.setLoopUnavailabled(diagram.nodeByAddress['122006'].loop)
	
	# (0, -3, 327, -1): 1
	# 013251
	diagram.setLoopUnavailabled(diagram.nodeByAddress['013251'].loop)
	
	# (0, 0, 354, -1): 1
	# 101053
	diagram.setLoopUnavailabled(diagram.nodeByAddress['101053'].loop)
	
	# (2, -8, 295, -86): 1
	# 101454
	diagram.setLoopUnavailabled(diagram.nodeByAddress['101454'].loop)
	#extend('101454')
	
	# (0, -3, 337, -1): 1
	# zeroes: 110121
	diagram.setLoopUnavailabled(diagram.nodeByAddress['110121'].loop)
	
	# (2, -8, 307, -64): 1
	# 011106
	diagram.setLoopUnavailabled(diagram.nodeByAddress['011106'].loop)	

	# (2, -7, 311, -66): 2
	# 002053 010253
	diagram.setLoopUnavailabled(diagram.nodeByAddress['002053'].loop)	
	diagram.setLoopUnavailabled(diagram.nodeByAddress['010244'].loop)	
	#extend('002053')
	
	# (2, -6, 320, -38): 1
	# 122041
	diagram.setLoopUnavailabled(diagram.nodeByAddress['122041'].loop)
	'' '
	# zeroes: 
	for addr in "110334 102321 003403 102312 010321 013420 013032 110343 020130 021042 020402 020453 000454 012134 000403".split(' '):
		diagram.setLoopUnavailabled(diagram.nodeByAddress[addr].loop)
	
	for addr in "101143 023403 013100 101032 123032 023242 120005 020220 020310 012110 023152 020312 101101 110211 020321 110301 023002 110244 102133 001402 102402 001453".split(' '):
		diagram.setLoopUnavailabled(diagram.nodeByAddress[addr].loop)
		
	for addr in "111006 013110 101014 101200 110220 013303 101110 013106 110112 101152 011302 102420 010001 003303 110202 122206 112406 110253 013020 012430 012454 013330 121206 100210 110310 010310 020301 003421 120310 123206 010343 112023 120244 023430 013242 011230 020334 020244 022406 100054 012224 023200 013354 023306 111014 100253 101206 102406 101106 100041 003044 102014 001052 003052 102142 001001 102306 012101 003453 003402 123106 010330 023412 100351 121014 120014 000402 003053 011353 102151 003444 003321 101412 101233 123014 012023 012251 013023 001034 120343 122106 100342 121306 010052 012200 021353 121032 020343 003454".split(' '):
		diagram.setLoopUnavailabled(diagram.nodeByAddress[addr].loop)
	
	for addr in "122206 013142 113005 003444 100144 013306 101403 111206 122023 010320 013403 010321".split(' '):
		diagram.setLoopUnavailabled(diagram.nodeByAddress[addr].loop)
		
	for addr in "023002 120022 021203 120013 021306 022005 112005 003321 121023 010330 100234 103206 012200 123306 013006 003412 012242 113206 122306 102321".split(' '):
		diagram.setLoopUnavailabled(diagram.nodeByAddress[addr].loop)
		
	for addr in "121041 120004 100342 100310 122032 010343 000454 111106 013444 100252 020133 120352 122106 021106 100334 001034 023306 020334 000312 013101 123106 113032 100343 013034 020211 021206 102133 022006 021033 101206 012110 020343 100300 120106 120103 113014 010244 010344 011033 012106 013110 013200 013430 023023 000402 011212 020041 023251 110253 120040 021221 120154 002143 010221 012020 020202 012403 120041 102330 102124 102005 120310 010052 001011 013412 100054 023152 013100 013124 110041 021051 012143 020310 102402 101233 023101 020301 013052 003421 021353 100333 110310 013010 113023 020402 103006 102312 100301 123006 102406 100406 103406 013053 100324 120301 001444 100201 010310 013233 101101 010453 013106 013420 100023 123014 102206 013242 102052 100021 121032 020130 101200 013406 101306 023242".split(' '):
		diagram.setLoopUnavailabled(diagram.nodeByAddress[addr].loop)
		
	
	diagram.setLoopUnavailabled(diagram.nodeByAddress['012200'].loop)
					
	# (2, -20, 187, -114): 1
	# 013110
	diagram.setLoopUnavailabled(diagram.nodeByAddress['013110'].loop)
	diagram.setLoopUnavailabled(diagram.nodeByAddress['100243'].loop)
	
	# (2, -16, 207, -104): 1
	# 113306
	diagram.setLoopUnavailabled(diagram.nodeByAddress['113306'].loop)
	diagram.setLoopUnavailabled(diagram.nodeByAddress['113206'].loop)
	
	for addr in "003403 110253 110202".split(' '):
		diagram.setLoopUnavailabled(diagram.nodeByAddress[addr].loop)
		
	# (2, -15, 201, -134): 1					
	# 013330
	diagram.setLoopUnavailabled(diagram.nodeByAddress['013330'].loop)
		
	for addr in "001444 023412 000454".split(' '):
		diagram.setLoopUnavailabled(diagram.nodeByAddress[addr].loop)								

	for addr in "021033 120301".split(' '):
		diagram.setLoopUnavailabled(diagram.nodeByAddress[addr].loop)								
		
	# (2, -15, 215, -92): 1		
	# 013233
	diagram.setLoopUnavailabled(diagram.nodeByAddress['013233'].loop)								
				
	for addr in "003412 013052".split(' '):
		diagram.setLoopUnavailabled(diagram.nodeByAddress[addr].loop)
		
	# (2, -12, 214, -106): 1
	# 121023
	diagram.setLoopUnavailabled(diagram.nodeByAddress['121023'].loop)
		
	for addr in "021212 021306 110334 120005 000134 003303 022106".split(' '):
		diagram.setLoopUnavailabled(diagram.nodeByAddress[addr].loop)
			
	for addr in "020041 110041 111032 013303 100342 013053 001453 012430 010330 103005 112005 010343 111106 020334 100054 012134 112406 013011 012106 013023 102330 013100 010320 010453 012406 001011 013014 003421 003152 001034 010311 110310 120013 121306".split(' '):
		diagram.setLoopUnavailabled(diagram.nodeByAddress[addr].loop)	
	' ''
	
	diagram.point()
	show(diagram)
	input("=== av loops: " + str(len([loop for loop in diagram.loops if loop.availabled])))
	
	singles = single()
	show(diagram)
	input("=== av loops: " + str(len([loop for loop in diagram.loops if loop.availabled])) + " | singled: " + str(len(singles)))			
			
	pointloops0 = [l for l in diagram.loops if l.availabled] # [node.loop for node in diagram.pointers]

	pointloops0 = trial(pointloops0)		
	'''
