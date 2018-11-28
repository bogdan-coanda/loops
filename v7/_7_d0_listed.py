from diagram import *
from uicanvas import *
from common import *
from itertools import chain
from time import time
from collections import defaultdict


if __name__ == "__main__":

	# ============================================================================================================================================================================ #
		
	diagram = Diagram(7, 1)
	
	''' «sols__0__:0…4»
	[sol: 0][*13283619*][132m22s.393][lvl:24~18]  §⁰.0⁵.0⁴.0⁴.0⁴.2⁴.0³.1⁴.1³.1³.2³.1³.1².1³.2³.2³.1³.1³.0³.0³.0².2³.0².1³.1³ ~ §⁰.0⁵.2⁴.0³.1³.1³.0³.1³.1³.0².1².1².0¹.0¹.0¹.0¹.0¹.0¹.0¹
	tuples: 001006 001106 001206 001306 001403 001410 001430 001454 002020 002110 002200 002233 002242 002251 013002 013020 013044 013053 013224 013233 022006 022106 022306 112005
	loops: 000053 001044 001133 001303 002254 003005 003412 010004 010010 010302 010353 011452 012110 012403 100014 101430 103005 110112
	loops: 000153 001041 001053 001312 002002 002151 002203 002410 011401 011452 020130 021212 100003 100244 100333 101110 110023 111041
	loops: 000453 001041 001311 002002 002053 002100 002230 003233 003403 010330 010353 012454 020010 020303 021032 021212 022023 100012
	loops: 000253 001002 001224 002100 002151 003142 003412 010040 010302 020310 020330 021032 100012 100014 100253 110022 110103 121014
	loops: 000353 001042 001312 002053 003005 003411 010004 010040 011401 012430 020354 021033 021203 100013 100202 110023 110112 113032'''

	''' «sols__0__:5…9»
	[sol: 5][*13452111*][134m55s.711][lvl:24~18]  §⁰.0⁵.0⁴.0⁴.0⁴.2⁴.0³.3⁴.2³.1³.2³.1³.1³.2³.1³.2³.2³.1³.2³.0³.0².1³.0².2³.1³ ~ §⁰.0⁵.1⁴.0³.2³.1³.0³.1³.1³.0².1².0¹.0².0².0¹.0¹.0¹.0¹.0¹
	tuples: 001006 001106 001206 001306 001401 001410 001430 001452 002002 002011 002020 002053 002143 002233 013020 013044 013200 013224 013233 013251 022006 022106 022306 112005
	loops: 000402 001041 001043 001302 003152 003233 003411 010000 010052 010253 010330 011203 011254 012430 020010 021032 022041 110343
	loops: 000102 001041 001044 002402 002410 003143 010010 010051 010202 010253 020130 020352 100252 100333 101101 110023 110343 111014
	loops: 000202 001043 001224 002200 002251 003142 003453 010202 011254 020301 021032 021443 100014 100244 101110 110022 110352 121032
	loops: 000002 001052 001133 001311 002230 002251 002402 002453 003005 010001 011203 012110 021443 100014 100243 101152 101430 103023
	loops: 000302 001042 001353 002200 002453 003005 003143 003402 010000 010051 020310 020330 021033 021452 100013 100243 110023 113005'''		
	
	''' «sols__1__:0…4»
	[sol: 0][*16164014*][277m29s.110][lvl:24~18]  §⁰.1⁵.0⁴.0⁴.0⁴.2⁴.2³.1⁴.1³.2³.2³.1³.2³.2³.0³.2³.1³.0³.1³.1³.0².2³.0².1³.0³ ~ §⁰.0⁵.2⁴.0³.1³.1³.0³.1³.1³.0².1².1².0¹.0¹.0¹.0¹.0¹.0¹.0¹
	tuples: 001005 001014 001023 001032 001042 001224 001403 001454 002020 002110 002200 002233 002242 002251 013002 013010 013020 013043 013053 013233 022005 022014 022032 112006
	loops: 000002 001354 001412 001420 002203 003006 003044 010040 010142 010302 010353 011401 012242 012454 100106 101224 103006 110244
	loops: 000102 001002 001406 001444 002042 002053 002100 002254 011401 011452 020013 021344 100054 100112 100120 101242 110206 111406
	loops: 000202 001053 001430 002100 002151 003010 003044 010004 010353 020031 020124 021306 100106 100144 100202 110154 110220 121106
	loops: 000302 001410 001444 002002 003006 003043 010004 010040 011452 012224 020303 021254 021320 100130 100253 110206 110244 113306
	loops: 000402 001406 001443 002002 002024 002053 002151 003020 003454 010124 010302 012403 020142 020354 021306 021344 022206 100144'''

	''' «sols__1__:5…9»	
	[sol: 5][*16268023*][ 281m31s.33][lvl:24~18]  §⁰.1⁵.0⁴.0⁴.0⁴.2⁴.2³.3⁴.2³.2³.2³.0³.0².1³.2³.1³.2³.1³.2³.1³.1².1³.0².2³.0³ ~ §⁰.0⁵.3⁴.0³.2³.1³.0³.1³.2³.0².1².0¹.0².0².0¹.0¹.0¹.0¹.0¹
	tuples: 001005 001014 001023 001032 001042 001224 001401 001452 002002 002011 002020 002053 002143 002233 013010 013020 013043 013200 013233 013251 022005 022014 022032 112006
	loops: 000053 001001 001420 001443 002024 002200 002402 002453 003006 010052 011254 012242 021311 100106 100111 101101 101224 103206
	loops: 000353 001302 001410 002251 002402 003006 003011 003453 010000 010051 020031 020124 021320 021401 100111 100130 110206 113006
	loops: 000253 001411 001430 002200 002251 003010 003402 010253 011203 020352 021306 021311 100106 100112 101242 110220 110301 121306
	loops: 000153 001406 001412 002042 002453 003011 010000 010142 010202 010253 020013 020301 100120 100201 101152 110206 110211 111106
	loops: 000453 001353 001406 001411 003020 003043 003101 010001 010051 010124 010202 011203 011254 012224 020142 021306 022406 110211'''
	
	# «sols__0__:0…4»
	# taddrs = [
		# '001006', '001106', '001206', '001306', # 001 blue box-1
		# '001403', '001410', '001430', '001454', # 0014 blue fillers ((1))
		# '002020', '002110', '002200', '002233', '002242', '002251', # 011 diag box ((1))
		# '013002', '013020', '013044', '013053', '013224', '013233', # 123 box ((1))
		# '022006', '022106', '022306', # 022 blue box-2
		# '112005' # 112 green diag box
	# ]

	# «sols__0__:5…9»
	# taddrs = [
		# '001006', '001106', '001206', '001306', # 001 blue box-1
		# '001401', '001410', '001430', '001452', # 0014 blue fillers ((2))
		# '002002', '002011', '002020', '002053', '002143', '002233', # 011 diag box ((2))
		# '013020', '013044', '013200', '013224', '013233', '013251', # 123 box ((2))
		# '022006', '022106', '022306', # 022 blue box-2
		# '112005' # 112 green diag box
	# ]
			
	# «sols__0__:0…9» | common
	# taddrs = [
		#'001006', '001106', '001206', '001306', # 001 blue box-1
		
		# '001403', '001410', '001430', '001454', # 0014 blue fillers ((1))
		# '001401', '001410', '001430', '001452', # 0014 blue fillers ((2))		
		#'001410', '001430', # 0014 blue fillers ((∘))
				
		# '002020', '002110', '002200', '002233', '002242', '002251', # 011 diag box ((1))
		# '002002', '002011', '002020', '002053', '002143', '002233', # 011 diag box ((2))
		#'002020', '002233', # 011 diag box ((∘))
								
		# '013002', '013020', '013044', '013053', '013224', '013233', # 123 box ((1))
		# '013020', '013044', '013200', '013224', '013233', '013251', # 123 box ((2))
		#'013020', '013044', '013224', '013233', # 123 box ((∘))
				
		#'022006', '022106', '022306', # 022 blue box-2
		#'112005' # 112 green diag box
	# ]

	# «sols__1__:0…4»
	# taddrs = [
		# '001005', '001014', '001023', '001032', # 001 green box-1
		# '001042', '001224', '001403', '001454', # 00104 green fillers ((1))
		# '002020', '002110', '002200', '002233', '002242', '002251', # 011 diag box ((1))
		# '013002', '013010', '013020', '013043', '013053', '013233', # 123 box ((3))
		# '022005', '022014', '022032', # 022 green box-2
		# '112006' # 112 blue diag box
	# ]

	# «sols__1__:5…9»
	# taddrs = [	
		# '001005', '001014', '001023', '001032', # 001 green box-1
		# '001042', '001224', '001401', '001452', # 00104 green fillers ((2))
		# '002002', '002011', '002020', '002053', '002143', '002233', # 011 diag box ((2))
		# '013010', '013020', '013043', '013200', '013233', '013251', # 123 box ((4))
		# '022005', '022014', '022032', # 022 green box-2
		# '112006' # 112 blue diag box
	# ]
		
	# «sols__1__:0…9» | common
	# taddrs = [
	# 	'001005', '001014', '001023', '001032', # 001 green box-1
	# 
		# '001042', '001224', '001403', '001454', # 00104 green fillers ((1))
		# '001042', '001224', '001401', '001452', # 00104 green fillers ((2))
	# 	'001042', '001224', # 0014 blue fillers ((∘))
	# 
		# '002020', '002110', '002200', '002233', '002242', '002251', # 011 diag box ((1))
		# '002002', '002011', '002020', '002053', '002143', '002233', # 011 diag box ((2))
	# 	'002020', '002233', # 011 diag box ((∘))
	# 
		# '013002', '013010', '013020', '013043', '013053', '013233', # 123 box ((3))
		# '013010', '013020', '013043', '013200', '013233', '013251', # 123 box ((4))
	# 	'013010', '013020', '013043', '013233', # 123 box ((∘))
	# 
	# 	'022005', '022014', '022032', # 022 green box-2
	# 	'112006' # 112 blue diag box
	# ]		
		
	# «sols__0…1__:0…4» | common
	# taddrs = [
	# 	'001403', '001454', # 0014 blue fillers ((1)) / 00104 green fillers ((1))
	# 	'002020', '002110', '002200', '002233', '002242', '002251', # 011 diag box ((1))
	# 	'013002', '013020', '013053', '013233', # 123 box ((1)) / ((3))	
	# ]
			
	# «sols__0…1__:5…9» | common
	# taddrs = [
	# 	'001401', '001452', # 0014 blue fillers ((2)) / 00104 green fillers ((2))
	# 	'002002', '002011', '002020', '002053', '002143', '002233', # 011 diag box ((2))
	# 	'013020', '013200', '013233', '013251', # 123 box ((2)) / ((4))
	# ]			

	taddrs = []

	# «sols__0…1__:0…9» | bases [ABab]
	taddrs += [
		# 001 box-1		
		# 001 fillers ((1)) // ((2))
		# '002020', '002233', # 011 diag box ((1)) / ((2))
		# '013020', '013233', # 123 box ((1)) / ((3))	/ ((2)) / ((4))	
		# 022 box-2
		# 112 diag box		
	]


	# «sols__0…1__:0…4» | middles [Aa]
	# taddrs += [
		#001 box-1
	# 	'001403', '001454', # 0014 blue fillers ((1)) / 00104 green fillers ((1))
	# 	'002110', '002200', '002242', '002251', # 011 diag box ((1))
	# 	'013002', '013053', # 123 box ((1)) / ((3))	
		#022 box-2
		#112 diag box
	# ]

	# «sols__0…1__:5…9» | middles [Bb]
	# taddrs += [
		# 001 box-1
	# 	'001401', '001452', # 0014 blue fillers ((2)) / 00104 green fillers ((2))
	# 	'002002', '002011', '002053', '002143', # 011 diag box ((2))
	# 	'013200', '013251', # 123 box ((2)) / ((4))
		# 022 box-2
		# 112 diag box
	# ]		
	
	
	# «sols__0__:0…9» | endings [AB]
	# taddrs += [
	# 	'001006', '001106', '001206', '001306', # 001 blue box-1
	# 	'001410', '001430', # 0014 blue fillers ((1))
		# 011 diag box ((1))
	# 	'013044', '013224', # 123 box ((1))
	# 	'022006', '022106', '022306', # 022 blue box-2
	# 	'112005' # 112 green diag box
	# ]
	
	# «sols__1__:0…9» | endings [ab]
	# taddrs += [
	# 	'001005', '001014', '001023', '001032', # 001 green box-1
	# 	'001042', '001224', # 00104 green fillers ((1))
		# 011 diag box ((1))
	# 	'013010', '013043', # 123 box ((3))
	# 	'022005', '022014', '022032', # 022 green box-2
	# 	'112006' # 112 blue diag box
	# ]
																																		
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #	
							
	laddrs = [
		# «sols:0…4» | patches [A]
		# '000053', '001044', '001133', '001303', '002254', '003005', '003412', '010004', '010010', '010302', '010353', '011452', '012110', '012403', '100014', '101430', '103005', '110112'
		
		# «sols:5…9» | patches [B]
		# '000402', '001041', '001043', '001302', '003152', '003233', '003411', '010000', '010052', '010253', '010330', '011203', '011254', '012430', '020010', '021032', '022041', '110343'
		
		# «sols__1__:0…4» | patches [a]
		# '000002', '001354', '001412', '001420', '002203', '003006', '003044', '010040', '010142', '010302', '010353', '011401', '012242', '012454', '100106', '101224', '103006', '110244'		
		
		# «sols__1__:5…9» | patches [b]
		# '000053', '001001', '001420', '001443', '002024', '002200', '002402', '002453', '003006', '010052', '011254', '012242', '021311', '100106', '100111', '101101', '101224', '103206'
	]
	
	#print("laddrs: " + str(len(laddrs)) + " in tuples: " + str(len(set([diagram.nodeByAddress[addr].loop.tuple for addr in laddrs]))))
	print("\n".join([str(sorted([diagram.loop_tuples.index(diagram.nodeByAddress[addr].loop.tuple) for addr in laddrs.split(' ')]))
		for laddrs in [
			"000053 001044 001133 001303 002254 003005 003412 010004 010010 010302 010353 011452 012110 012403 100014 101430 103005 110112",
			"000153 001041 001053 001312 002002 002151 002203 002410 011401 011452 020130 021212 100003 100244 100333 101110 110023 111041",
			"000453 001041 001311 002002 002053 002100 002230 003233 003403 010330 010353 012454 020010 020303 021032 021212 022023 100012",
			"000253 001002 001224 002100 002151 003142 003412 010040 010302 020310 020330 021032 100012 100014 100253 110022 110103 121014", 
			"000353 001042 001312 002053 003005 003411 010004 010040 011401 012430 020354 021033 021203 100013 100202 110023 110112 113032",
			
			"000402 001041 001043 001302 003152 003233 003411 010000 010052 010253 010330 011203 011254 012430 020010 021032 022041 110343",
			"000102 001041 001044 002402 002410 003143 010010 010051 010202 010253 020130 020352 100252 100333 101101 110023 110343 111014",
			"000202 001043 001224 002200 002251 003142 003453 010202 011254 020301 021032 021443 100014 100244 101110 110022 110352 121032",
			"000002 001052 001133 001311 002230 002251 002402 002453 003005 010001 011203 012110 021443 100014 100243 101152 101430 103023",
			"000302 001042 001353 002200 002453 003005 003143 003402 010000 010051 020310 020330 021033 021452 100013 100243 110023 113005",

			"000002 001354 001412 001420 002203 003006 003044 010040 010142 010302 010353 011401 012242 012454 100106 101224 103006 110244",
			"000102 001002 001406 001444 002042 002053 002100 002254 011401 011452 020013 021344 100054 100112 100120 101242 110206 111406",
			"000202 001053 001430 002100 002151 003010 003044 010004 010353 020031 020124 021306 100106 100144 100202 110154 110220 121106",
			"000302 001410 001444 002002 003006 003043 010004 010040 011452 012224 020303 021254 021320 100130 100253 110206 110244 113306",
			"000402 001406 001443 002002 002024 002053 002151 003020 003454 010124 010302 012403 020142 020354 021306 021344 022206 100144",

			"000053 001001 001420 001443 002024 002200 002402 002453 003006 010052 011254 012242 021311 100106 100111 101101 101224 103206",
			"000353 001302 001410 002251 002402 003006 003011 003453 010000 010051 020031 020124 021320 021401 100111 100130 110206 113006",
			"000253 001411 001430 002200 002251 003010 003402 010253 011203 020352 021306 021311 100106 100112 101242 110220 110301 121306",
			"000153 001406 001412 002042 002453 003011 010000 010142 010202 010253 020013 020301 100120 100201 101152 110206 110211 111106",
			"000453 001353 001406 001411 003020 003043 003101 010001 010051 010124 010202 011203 011254 012224 020142 021306 022406 110211"]			
	]))
	
	sol_tuples = [diagram.nodeByAddress[addr].loop.tuple for addr in taddrs]
	sol_loops = [diagram.nodeByAddress[addr].loop for addr in laddrs]
	
	for i,t in enumerate(sol_tuples):
		for j,l in enumerate(t):
			assert diagram.extendLoop(l)
	for l in sol_loops:
		assert diagram.extendLoop(l)		
		
	# ============================================================================================================================================================================ #	

	#diagram.point()
	show(diagram)
