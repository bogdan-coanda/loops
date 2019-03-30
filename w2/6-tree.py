from diagram import *
from uicanvas import *
from common import *
from collections import defaultdict


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
			

if __name__ == "__main__":

	diagram = Diagram(6, kernelPath='222', noKernel=True)
	# cOc('2322 2232 2223 2222')
	
	addrs = []
	
	# ---  blue  --- #
	# loops += [diagram.nodeByAddress['00005'].loop]
	# loops += [diagram.nodeByAddress['00105'].loop]
	# loops += [diagram.nodeByAddress['00205'].loop]
	# loops += [diagram.nodeByAddress['00305'].loop]
	# 
	## loops += [diagram.nodeByAddress['01005'].loop]
	## loops += [diagram.nodeByAddress['01105'].loop]
	## loops += [diagram.nodeByAddress['01205'].loop]
	## loops += [diagram.nodeByAddress['01305'].loop]
	# 
	# loops += [diagram.nodeByAddress['02005'].loop]
	# loops += [diagram.nodeByAddress['02105'].loop]
	# loops += [diagram.nodeByAddress['02205'].loop]
	# loops += [diagram.nodeByAddress['02305'].loop]
	# 
	# loops += [diagram.nodeByAddress['10005'].loop]
	# loops += [diagram.nodeByAddress['10105'].loop]
	## loops += [diagram.nodeByAddress['10205'].loop]
	# loops += [diagram.nodeByAddress['10305'].loop]
	# 
	## loops += [diagram.nodeByAddress['11005'].loop]
	## loops += [diagram.nodeByAddress['11105'].loop]
	## loops += [diagram.nodeByAddress['11205'].loop]
	# loops += [diagram.nodeByAddress['11305'].loop]
	# 
	## loops += [diagram.nodeByAddress['12005'].loop]
	## loops += [diagram.nodeByAddress['12105'].loop]
	# loops += [diagram.nodeByAddress['12205'].loop]
	# loops += [diagram.nodeByAddress['12305'].loop]
	# 
	# ---  green  --- #
	# loops += [diagram.nodeByAddress['00004'].loop]
	# loops += [diagram.nodeByAddress['00104'].loop]
	# loops += [diagram.nodeByAddress['00204'].loop]
	# loops += [diagram.nodeByAddress['00304'].loop]
	# 
	# loops += [diagram.nodeByAddress['01004'].loop]
	# loops += [diagram.nodeByAddress['01104'].loop]
	# loops += [diagram.nodeByAddress['01204'].loop]
	# loops += [diagram.nodeByAddress['01304'].loop]
	# 
	## loops += [diagram.nodeByAddress['02004'].loop]
	## loops += [diagram.nodeByAddress['02104'].loop]
	## loops += [diagram.nodeByAddress['02204'].loop]
	## loops += [diagram.nodeByAddress['02304'].loop]
	# 
	# loops += [diagram.nodeByAddress['10004'].loop]
	## loops += [diagram.nodeByAddress['10104'].loop]
	# loops += [diagram.nodeByAddress['10204'].loop]
	# loops += [diagram.nodeByAddress['10304'].loop]
	# 
	# loops += [diagram.nodeByAddress['11004'].loop]
	# loops += [diagram.nodeByAddress['11104'].loop]
	# loops += [diagram.nodeByAddress['11204'].loop]
	# loops += [diagram.nodeByAddress['11304'].loop]
	# 
	# loops += [diagram.nodeByAddress['12004'].loop]
	# loops += [diagram.nodeByAddress['12104'].loop]
	# loops += [diagram.nodeByAddress['12204'].loop]
	# loops += [diagram.nodeByAddress['12304'].loop]																		

	# ---  yellow  --- #
	# loops += [diagram.nodeByAddress['00003'].loop]
	# loops += [diagram.nodeByAddress['00012'].loop]
	# loops += [diagram.nodeByAddress['00021'].loop]
	# loops += [diagram.nodeByAddress['00030'].loop]
	# 
	# loops += [diagram.nodeByAddress['00102'].loop]
	# loops += [diagram.nodeByAddress['00111'].loop]
	# loops += [diagram.nodeByAddress['00120'].loop]
	# loops += [diagram.nodeByAddress['00143'].loop]
	# 
	# loops += [diagram.nodeByAddress['00201'].loop]
	# loops += [diagram.nodeByAddress['00210'].loop]
	# loops += [diagram.nodeByAddress['00233'].loop]
	# loops += [diagram.nodeByAddress['00242'].loop]
	# 
	## loops += [diagram.nodeByAddress['10003'].loop]
	# loops += [diagram.nodeByAddress['10012'].loop]
	# loops += [diagram.nodeByAddress['10021'].loop]
	# loops += [diagram.nodeByAddress['10030'].loop]
	# 
	# loops += [diagram.nodeByAddress['10102'].loop]
	# loops += [diagram.nodeByAddress['10111'].loop]
	# loops += [diagram.nodeByAddress['10120'].loop]
	# loops += [diagram.nodeByAddress['10143'].loop]
	# 
	# loops += [diagram.nodeByAddress['10201'].loop]
	# loops += [diagram.nodeByAddress['10210'].loop]
	# loops += [diagram.nodeByAddress['10233'].loop]
	# loops += [diagram.nodeByAddress['10242'].loop]

	# ---  orange  --- #	
	# loops += [diagram.nodeByAddress['00002'].loop] # green:0,8,9,<16>
	# loops += [diagram.nodeByAddress['00011'].loop]
	# loops += [diagram.nodeByAddress['00020'].loop]
	# loops += [diagram.nodeByAddress['00043'].loop] # green:0,8,9,<16>
	# 
	# loops += [diagram.nodeByAddress['00101'].loop]
	# loops += [diagram.nodeByAddress['00110'].loop]
	## loops += [diagram.nodeByAddress['00133'].loop] # green:0,8,9,<16>
	# loops += [diagram.nodeByAddress['00142'].loop]
	# 
	# loops += [diagram.nodeByAddress['00200'].loop]
	# loops += [diagram.nodeByAddress['00223'].loop] # green:0,8,9,<16>
	# loops += [diagram.nodeByAddress['00232'].loop]
	# loops += [diagram.nodeByAddress['00241'].loop]
	# 
	# loops += [diagram.nodeByAddress['01001'].loop]
	# loops += [diagram.nodeByAddress['01010'].loop]
	##loops += [diagram.nodeByAddress['01033'].loop] # @ green:7,14,15,23
	# loops += [diagram.nodeByAddress['01042'].loop]
	# 
	# loops += [diagram.nodeByAddress['01100'].loop]
	## loops += [diagram.nodeByAddress['01123'].loop] # @ green:7,14,15,23
	# loops += [diagram.nodeByAddress['01132'].loop]
	# loops += [diagram.nodeByAddress['01141'].loop]
	# 
	# loops += [diagram.nodeByAddress['01302'].loop] # @ green:7,14,15,23	
	# loops += [diagram.nodeByAddress['01311'].loop]
	# loops += [diagram.nodeByAddress['01320'].loop]
	## loops += [diagram.nodeByAddress['01343'].loop] # @ green:7,14,15,23	
																						
	# ---  red  --- #
	# loops += [diagram.nodeByAddress['00001'].loop] # green:0,12,13,<16>
	# loops += [diagram.nodeByAddress['00010'].loop]
	# loops += [diagram.nodeByAddress['00033'].loop]
	## loops += [diagram.nodeByAddress['00042'].loop] # green:0,12,13,<16>
	# 
	# loops += [diagram.nodeByAddress['00100'].loop]
	# loops += [diagram.nodeByAddress['00123'].loop]
	# loops += [diagram.nodeByAddress['00132'].loop] # green:0,12,13,<16>
	# loops += [diagram.nodeByAddress['00141'].loop]
	# 
	# loops += [diagram.nodeByAddress['00302'].loop]
	# loops += [diagram.nodeByAddress['00311'].loop] # green:0,12,13,<16>
	# loops += [diagram.nodeByAddress['00320'].loop]
	# loops += [diagram.nodeByAddress['00343'].loop]
	# 
	# loops += [diagram.nodeByAddress['01000'].loop]
	# loops += [diagram.nodeByAddress['01023'].loop]
	# loops += [diagram.nodeByAddress['01032'].loop]
	# loops += [diagram.nodeByAddress['01041'].loop]
	# 
	# loops += [diagram.nodeByAddress['01202'].loop]
	# loops += [diagram.nodeByAddress['01211'].loop]
	# loops += [diagram.nodeByAddress['01220'].loop]
	# loops += [diagram.nodeByAddress['01243'].loop]
	# 
	# loops += [diagram.nodeByAddress['01301'].loop]
	# loops += [diagram.nodeByAddress['01310'].loop]
	# loops += [diagram.nodeByAddress['01333'].loop]
	# loops += [diagram.nodeByAddress['01342'].loop]	
														
	# ---  violet  --- #
	# loops += [diagram.nodeByAddress['00000'].loop]
	# loops += [diagram.nodeByAddress['00023'].loop]
	# loops += [diagram.nodeByAddress['00032'].loop]
	# loops += [diagram.nodeByAddress['00041'].loop]
	
	# loops += [diagram.nodeByAddress['00202'].loop]
	# loops += [diagram.nodeByAddress['00211'].loop]
	# loops += [diagram.nodeByAddress['00220'].loop]
	# loops += [diagram.nodeByAddress['00243'].loop]
	
	# loops += [diagram.nodeByAddress['00301'].loop]
	# loops += [diagram.nodeByAddress['00310'].loop]
	# loops += [diagram.nodeByAddress['00333'].loop]
	# loops += [diagram.nodeByAddress['00342'].loop]
	
	# loops += [diagram.nodeByAddress['02001'].loop]
	# loops += [diagram.nodeByAddress['02010'].loop]
	# loops += [diagram.nodeByAddress['02033'].loop]
	# loops += [diagram.nodeByAddress['02042'].loop]
	
	# loops += [diagram.nodeByAddress['02100'].loop]
	# loops += [diagram.nodeByAddress['02123'].loop]
	# loops += [diagram.nodeByAddress['02132'].loop]
	# loops += [diagram.nodeByAddress['02141'].loop]
	
	## loops += [diagram.nodeByAddress['02302'].loop]
	## loops += [diagram.nodeByAddress['02311'].loop]
	## loops += [diagram.nodeByAddress['02320'].loop]
	## loops += [diagram.nodeByAddress['02343'].loop]
	'''
	blue_0  = '00005'
	blue_1  = '00105'
	blue_2  = '00205'
	blue_3  = '00305'
	blue_4  = '01005'
	blue_5  = '01105'
	blue_6  = '01205'
	blue_7  = '01305'
	blue_8  = '02005'
	blue_9  = '02105'
	blue_10 = '02205'
	blue_11 = '02305'	
	blue_12 = '10005'
	blue_13 = '10105'
	blue_14 = '10205'
	blue_15 = '10305'
	blue_16 = '11005'
	blue_17 = '11105'
	blue_18 = '11205'
	blue_19 = '11305'
	blue_20 = '12005'
	blue_21 = '12105'
	blue_22 = '12205'
	blue_23 = '12305'	
	
	green_0  = '00004'
	green_1  = '00104'
	green_2  = '00204'
	green_3  = '00304'
	green_4  = '01004'
	green_5  = '01104'
	green_6  = '01204'
	green_7  = '01304'
	green_8  = '02004'
	green_9  = '02104'
	green_10 = '02204'
	green_11 = '02304'	
	green_12 = '10004'
	green_13 = '10104'
	green_14 = '10204'
	green_15 = '10304'	
	green_16 = '11004'
	green_17 = '11104'
	green_18 = '11204'
	green_19 = '11304'
	green_20 = '12004'
	green_21 = '12104'
	green_22 = '12204'
	green_23 = '12304'	
	
	yellow_0  = '00030'
	yellow_1  = '00120'
	yellow_2  = '00210'
	yellow_3  = '00003'
	yellow_4  = '00143'
	yellow_5  = '00233'
	yellow_6  = '00012'
	yellow_7  = '00102'
	yellow_8  = '00242'
	yellow_9  = '00021'
	yellow_10 = '00111'
	yellow_11 = '00201'
	yellow_12 = '10030'
	yellow_13 = '10120'
	yellow_14 = '10210'
	yellow_15 = '10003'
	yellow_16 = '10143'
	yellow_17 = '10233'
	yellow_18 = '10012'
	yellow_19 = '10102'
	yellow_20 = '10242'
	yellow_21 = '10021'
	yellow_22 = '10111'
	yellow_23 = '10201'

	orange_0  = '00020'
	orange_1  = '00110'
	orange_2  = '00200'
	orange_3  = '00241'
	orange_4  = '01010'
	orange_5  = '01100'
	orange_6  = '01141'
	orange_7  = '01320'
	orange_8  = '00002'
	orange_9  = '00043'
	orange_10 = '00133'
	orange_11 = '00223'
	orange_12 = '01033'
	orange_13 = '01123'
	orange_14 = '01302'
	orange_15 = '01343'
	orange_16 = '00011'
	orange_17 = '00101'
	orange_18 = '00142'
	orange_19 = '00232'
	orange_20 = '01001'
	orange_21 = '01042'
	orange_22 = '01132'
	orange_23 = '01311'

	red_0  = '00010'
	red_1  = '00100'
	red_2  = '00141'
	red_3  = '00320'
	red_4  = '01000'
	red_5  = '01041'
	red_6  = '01220'
	red_7  = '01310'
	red_8  = '01032'
	red_9  = '01211'
	red_10 = '01301'
	red_11 = '01342'
	red_12 = '00001'
	red_13 = '00042'
	red_14 = '00132'
	red_15 = '00311'
	red_16 = '00033'
	red_17 = '00123'
	red_18 = '00302'
	red_19 = '00343'
	red_20 = '01023'
	red_21 = '01202'
	red_22 = '01243'
	red_23 = '01333'

	violet_0  = '00000'
	violet_1  = '00041'
	violet_2  = '00220'
	violet_3  = '00310'
	violet_4  = '00032'
	violet_5  = '00211'
	violet_6  = '00301'
	violet_7  = '00342'
	violet_8  = '02010'
	violet_9  = '02100'
	violet_10 = '02141'
	violet_11 = '02320'
	violet_12 = '00023'
	violet_13 = '00202'
	violet_14 = '00243'
	violet_15 = '00333'
	violet_16 = '02001'
	violet_17 = '02042'
	violet_18 = '02132'
	violet_19 = '02311'
	violet_20 = '02033'
	violet_21 = '02123'
	violet_22 = '02302'
	violet_23 = '02343'
	'''
	# ---  blue ∘ green  --- #
	'''
	# addrs += [blue_0, blue_1, blue_2, blue_3]
	# addrs += [green_0, green_1, green_2, green_3]

	addrs += [blue_4, blue_5, blue_6, blue_7]
	# addrs += [green_4, green_5, green_6, green_7]

	# addrs += [blue_8, blue_9, blue_10, blue_11]
	addrs += [green_8, green_9, green_10, green_11]

	# addrs += [blue_12, blue_13, blue_14, blue_15]
	# addrs += [green_12, green_13, green_14, green_15]

	addrs += [blue_16, blue_17, blue_18]#, blue_19]
	# addrs += [green_16, green_17, green_18, green_19]

	# addrs += [blue_20, blue_21, blue_22, blue_23]
	# addrs += [green_20, green_21, green_22, green_23]
																															
	# ---  blue ∘ yellow  --- #
	
	# addrs += [blue_0, blue_3, blue_6, blue_9]
	# addrs += [yellow_0, yellow_3, yellow_6, yellow_9]
		
	# addrs += [blue_1, blue_4, blue_7, blue_10]
	# addrs += [yellow_1, yellow_4, yellow_7, yellow_10]	

	# addrs += [blue_2, blue_5, blue_8, blue_11]
	# addrs += [yellow_2, yellow_5, yellow_8, yellow_11]

	# addrs += [blue_12, blue_15, blue_18, blue_21]
	# addrs += [yellow_12, yellow_15, yellow_18, yellow_21]

	# addrs += [blue_13, blue_16, blue_19, blue_22]
	# addrs += [yellow_13, yellow_16, yellow_19, yellow_22]

	# addrs += [blue_14, blue_17, blue_20, blue_23]
	# addrs += [yellow_14, yellow_17, yellow_20, yellow_23]	
																																																			
	# ---  blue ∘ orange  --- #
	
	# addrs += [blue_0, blue_8, blue_9, blue_16]
	# addrs += [orange_0, orange_8, orange_9, orange_16]

	# addrs += [blue_1, blue_10, blue_17, blue_18]
	# addrs += [orange_1, orange_10, orange_17, orange_18]
			
	# addrs += [blue_2, blue_3, blue_11, blue_19]
	# addrs += [orange_2, orange_3, orange_11, orange_19]

	# addrs += [blue_4, blue_12, blue_20, blue_21]
	# addrs += [orange_4, orange_12, orange_20, orange_21]
									
	# addrs += [blue_5, blue_6, blue_13, blue_22]
	# addrs += [orange_5, orange_6, orange_13, orange_22]
	
	# addrs += [blue_7, blue_14, blue_15, blue_23]
	# addrs += [orange_7, orange_14, orange_15, orange_23]	
										
	# ---  blue ∘ red  --- #
	
	# addrs += [blue_0, blue_12, blue_13, blue_16]
	# addrs += [red_0, red_12, red_13, red_16]		

	# addrs += [blue_1, blue_2, blue_14, blue_17]
	# addrs += [red_1, red_2, red_14, red_17]		
			
	# addrs += [blue_3, blue_15, blue_18, blue_19]
	# addrs += [red_3, red_15, red_18, red_19]		
				
	# addrs += [blue_4, blue_5, blue_8, blue_20]
	# addrs += [red_4, red_5, red_8, red_20]		
	
	# addrs += [blue_6, blue_9, blue_21, blue_22]
	# addrs += [red_6, red_9, red_21, red_22]			
					
	# addrs += [blue_7, blue_10, blue_11, blue_23]
	# addrs += [red_7, red_10, red_11, red_23]		
						
	# ---  blue ∘ violet  --- #
	
	# addrs += [blue_0, blue_1, blue_4, blue_12]
	# addrs += [violet_0, violet_1, violet_4, violet_12]			
	
	# addrs += [blue_2, blue_5, blue_13, blue_14]
	# addrs += [violet_2, violet_5, violet_13, violet_14]			
	
	# addrs += [blue_3, blue_6, blue_7, blue_15]
	# addrs += [violet_3, violet_6, violet_7, violet_15]
	
	# addrs += [blue_8, blue_16, blue_17, blue_20]
	# addrs += [violet_8, violet_16, violet_17, violet_20]	
	
	# addrs += [blue_9, blue_10, blue_18, blue_21]
	# addrs += [violet_9, violet_10, violet_18, violet_21]
	
	# addrs += [blue_11, blue_19, blue_22, blue_23]
	addrs += [violet_11, violet_19, violet_22, violet_23]
		
	# ---  green ∘ yellow  --- #
	
	# addrs += [green_0, green_3, green_6, green_9]
	# addrs += [yellow_0, yellow_1, yellow_2, yellow_3]

	# addrs += [green_1, green_4, green_7, green_10]
	# addrs += [yellow_4, yellow_5, yellow_6, yellow_7]
			
	# addrs += [green_2, green_5, green_8, green_11]
	# addrs += [yellow_8, yellow_9, yellow_10, yellow_11]

	# addrs += [green_12, green_15, green_18, green_21]
	# addrs += [yellow_12, yellow_13, yellow_14, yellow_15]

	# addrs += [green_13, green_16, green_19, green_22]
	# addrs += [yellow_16, yellow_17, yellow_18, yellow_19]

	# addrs += [green_14, green_17, green_20, green_23]
	# addrs += [yellow_20, yellow_21, yellow_22, yellow_23]
																																							
	# ---  green ∘ orange  --- #

	# addrs += [green_0, green_8, green_9, green_16]
	# addrs += [orange_8, orange_9, orange_10, orange_11]

	# addrs += [green_1, green_10, green_17, green_18]
	# addrs += [orange_16, orange_17, orange_18, orange_19]

	# addrs += [green_2, green_3, green_11, green_19]
	# addrs += [orange_0, orange_1, orange_2, orange_3]

	# addrs += [green_4, green_12, green_20, green_21]
	# addrs += [orange_20, orange_21, orange_22, orange_23]

	# addrs += [green_5, green_6, green_13, green_22]
	# addrs += [orange_4, orange_5, orange_6, orange_7]

	# addrs += [green_7, green_14, green_15, green_23]
	addrs += [orange_12, orange_13, orange_15]#, orange_14
	
	# ---  green ∘ red  --- #
	
	# addrs += [green_0, green_12, green_13, green_16]
	# addrs += [red_12, red_13, red_14, red_15]

	# addrs += [green_1, green_2, green_14, green_17]
	# addrs += [red_0, red_1, red_2, red_3]
	
	# addrs += [green_3, green_15, green_18, green_19]
	# addrs += [red_16, red_17, red_18, red_19]

	# addrs += [green_4, green_5, green_8, green_20]
	# addrs += [red_4, red_5, red_6, red_7]
															
	# addrs += [green_6, green_9, green_21, green_22]
	# addrs += [red_20, red_21, red_22, red_23]
	
	# addrs += [green_7, green_10, green_11, green_23]
	# addrs += [red_8, red_9, red_10, red_11]
		
	# ---  green ∘ violet  --- #
	
	# addrs += [green_0, green_1, green_4, green_12]	
	# addrs += [violet_0, violet_1, violet_2, violet_3]	

	# addrs += [green_2, green_5, green_13, green_14]	
	# addrs += [violet_12, violet_13, violet_14, violet_15]	
			
	# addrs += [green_3, green_6, green_7, green_15]	
	# addrs += [violet_4, violet_5, violet_6, violet_7]	
				
	# addrs += [green_8, green_16, green_17, green_20]	
	# addrs += [violet_16, violet_17, violet_18, violet_19]	
					
	# addrs += [green_9, green_10, green_18, green_21]	
	# addrs += [violet_8, violet_9, violet_10, violet_11]	
						
	# addrs += [green_11, green_19, green_22, green_23]	
	# addrs += [violet_20, violet_21, violet_22, violet_23]	
							
	# ---  yellow ∘ orange  --- #

	# addrs += [yellow_0, yellow_8, yellow_9, yellow_16]
	# addrs += [orange_0, orange_3, orange_6, orange_9]		

	# addrs += [yellow_1, yellow_10, yellow_17, yellow_18]
	# addrs += [orange_1, orange_4, orange_7, orange_10]		
							
	# addrs += [yellow_2, yellow_3, yellow_11, yellow_19]
	# addrs += [orange_2, orange_5, orange_8, orange_11]		

	# addrs += [yellow_4, yellow_12, yellow_20, yellow_21]
	# addrs += [orange_12, orange_15, orange_18, orange_21]		
	
	# addrs += [yellow_5, yellow_6, yellow_13, yellow_22]
	# addrs += [orange_13, orange_16, orange_19, orange_22]		
		
	# addrs += [yellow_7, yellow_14, yellow_15, yellow_23]
	# addrs += [orange_14, orange_17, orange_20, orange_23]
		
	# ---  yellow ∘ red  --- #

	# addrs += [yellow_0, yellow_12, yellow_13, yellow_16]
	# addrs += [red_13, red_16, red_19, red_22]

	# addrs += [yellow_1, yellow_2, yellow_14, yellow_17]
	# addrs += [red_14, red_17, red_20, red_23]
							
	# addrs += [yellow_3, yellow_15, yellow_18, yellow_19]
	# addrs += [red_12, red_15, red_18, red_21]
								
	# addrs += [yellow_4, yellow_5, yellow_8, yellow_20]
	# addrs += [red_2, red_5, red_8, red_11]
									
	# addrs += [yellow_6, yellow_9, yellow_21, yellow_22]
	# addrs += [red_0, red_3, red_6, red_9]
				
	# addrs += [yellow_7, yellow_10, yellow_11, yellow_23]
	# addrs += [red_1, red_4, red_7, red_10]
																	
	# ---  yellow ∘ violet  --- #
	
	# addrs += [yellow_0, yellow_1, yellow_4, yellow_12]
	# addrs += [violet_1, violet_4, violet_7, violet_10]	

	# addrs += [yellow_2, yellow_5, yellow_13, yellow_14]
	# addrs += [violet_2, violet_5, violet_8, violet_11]	
							
	# addrs += [yellow_3, yellow_6, yellow_7, yellow_15]
	# addrs += [violet_0, violet_3, violet_6, violet_9]	
								
	# addrs += [yellow_8, yellow_16, yellow_17, yellow_20]
	# addrs += [violet_14, violet_17, violet_20, violet_23]	
									
	# addrs += [yellow_9, yellow_10, yellow_18, yellow_21]
	# addrs += [violet_12, violet_15, violet_18, violet_21]	
										
	# addrs += [yellow_11, yellow_19, yellow_22, yellow_23]
	# addrs += [violet_13, violet_16, violet_19, violet_22]	
											
	# ---  orange ∘ red  --- #

	# addrs += [orange_0, orange_12, orange_13, orange_16]
	# addrs += [red_0, red_8, red_9, red_16]	

	# addrs += [orange_1, orange_2, orange_14, orange_17]
	# addrs += [red_1, red_10, red_17, red_18]	
			
	# addrs += [orange_3, orange_15, orange_18, orange_19]
	# addrs += [red_2, red_3, red_11, red_19]	
		
	# addrs += [orange_4, orange_5, orange_8, orange_20]
	# addrs += [red_4, red_12, red_20, red_21]	
							
	# addrs += [orange_6, orange_9, orange_21, orange_22]
	# addrs += [red_5, red_6, red_13, red_22]	
			
	# addrs += [orange_7, orange_10, orange_11, orange_23]
	# addrs += [red_7, red_14, red_15, red_23]	
				
	# ---  orange ∘ violet  --- #

	# addrs += [orange_0, orange_1, orange_4, orange_12]
	# addrs += [violet_4, violet_12, violet_20, violet_21]	
				
	# addrs += [orange_2, orange_5, orange_13, orange_14]
	# addrs += [violet_5, violet_6, violet_13, violet_22]	
	
	# addrs += [orange_3, orange_6, orange_7, orange_15]
	# addrs += [violet_7, violet_14, violet_15, violet_23]	
		
	# addrs += [orange_8, orange_16, orange_17, orange_20]
	# addrs += [violet_0, violet_8, violet_9, violet_16]	
			
	# addrs += [orange_9, orange_10, orange_18, orange_21]
	# addrs += [violet_1, violet_10, violet_17, violet_18]	
				
	# addrs += [orange_11, orange_19, orange_22, orange_23]
	# addrs += [violet_2, violet_3, violet_11, violet_19]	
					
	# ---  red ∘ violet  --- #

	# addrs += [red_0, red_1, red_4, red_12]		
	# addrs += [violet_0, violet_12, violet_13, violet_16]
					
	# addrs += [red_2, red_5, red_13, red_14]		
	# addrs += [violet_1, violet_2, violet_14, violet_17]

	# addrs += [red_3, red_6, red_7, red_15]		
	# addrs += [violet_3, violet_15, violet_18, violet_19]
		
	# addrs += [red_8, red_16, red_17, red_20]		
	# addrs += [violet_4, violet_5, violet_8, violet_20]
	
	# addrs += [red_9, red_10, red_18, red_21]		
	# addrs += [violet_6, violet_9, violet_21, violet_22]
										
	# addrs += [red_11, red_19, red_22, red_23]		
	# addrs += [violet_7, violet_10, violet_11, violet_23]
	'''									
	# ---  --- - ---  --- #
	
	
	for addr in addrs:
		assert diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	
	# unavailable = [l for l in diagram.loops if not l.available]
	# print(f"unavailable loops: {len(unavailable)}")
	# print(' '.join([l.firstAddress() for l in unavailable]))
	
	# for loop in diagram.loops:
	# 	if loop.ktype == 5:
	# 		print(f"loops += diagram.nodeByAddress['{loop.firstAddress()}']")
		
	show(diagram)
	
	ktype_loops = groupby(diagram.loops, K = lambda l: l.ktype)
	ktype_pairs = defaultdict(list)
	for kt1 in range(0, 5):
		for kt2 in range(kt1+1, 6):
			seen1 = []
			seen2 = []
			for loop1 in sorted([l for l in diagram.loops if l.ktype == kt1], key = lambda l: l.ktype_radialIndex):
				if loop1 not in seen1:
					ls2 = sorted(set([[ncn.loop for ncn in n.cycle.nodes if ncn.ktype == kt2][0] for n in loop1.nodes]), key = lambda l: l.ktype_radialIndex)
					ls1 = sorted(set([[ncn.loop for ncn in n.cycle.nodes if ncn.ktype == kt1][0] for n in ls2[0].nodes]), key = lambda l: l.ktype_radialIndex)
					for l in ls1:
						assert l not in seen1
					for l in ls2:
						assert l not in seen2						
					seen1 += ls1
					seen2 += ls2
					ktype_pairs[(kt1, kt2)].append(ls1)
					ktype_pairs[(kt2, kt1)].append(ls2)
					print(f"({kt1}, {kt2}) ⇒ {[color_string(l.ktype) + ':' + str(l.ktype_radialIndex) for l in ls1]}")				
					print(f"({kt2}, {kt1}) ⇒ {[color_string(l.ktype) + ':' + str(l.ktype_radialIndex) for l in ls2]}")
					print('')					
					
	for kt1 in range(0, 5):
		for kt2 in range(kt1+1, 6):
			assert len(ktype_pairs[(kt1, kt2)]) == 6
			assert len(ktype_pairs[(kt2, kt1)]) == 6
			for i in range(6):
				print(f"({kt1}, {kt2}) ⇒ {[color_string(l.ktype) + ':' + str(l.ktype_radialIndex) for l in ktype_pairs[(kt1, kt2)][i]]}")				
				print(f"({kt2}, {kt1}) ⇒ {[color_string(l.ktype) + ':' + str(l.ktype_radialIndex) for l in ktype_pairs[(kt2, kt1)][i]]}")								
	# for loop in sorted(diagram.loops, key = lambda l: (l.ktype, l.ktype_radialIndex)):
		# print(f"{color_string(loop.ktype)}_{loop.ktype_radialIndex} = '{loop.firstAddress()}'")
	
	'''
	rx = [n for n in diagram.cycleByAddress['0000'].nodes if n.ktype == 4][0].loop
	ry = [n for n in diagram.cycleByAddress['0000'].nodes if n.ktype == 5][0].loop
	diagram.pointers = rx.nodes + ry.nodes; show(diagram)
	nx = sorted([[ncn.loop for ncn in n.cycle.nodes if ncn.ktype == ry.ktype][0] for n in rx.nodes], key = lambda l: l.ktype_radialIndex)
	ny = sorted([[ncn.loop for ncn in n.cycle.nodes if ncn.ktype == rx.ktype][0] for n in ry.nodes], key = lambda l: l.ktype_radialIndex)
	print(nx)
	print(ny)
	'''
