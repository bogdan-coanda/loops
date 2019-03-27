from diagram import *
from uicanvas import *


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

	blue_0 = '00005'
	blue_12 = '10005'
	blue_13 = '10105'
	blue_16 = '11005'

	green_0  = '00004'
	green_12 = '10004'
	green_13 = '10104'
	green_16 = '11004'

	yellow_0  = '00030'
	yellow_12 = '10030'
	yellow_13 = '10120'
	yellow_16 = '10143'

	orange_6  = '01141'
	orange_9  = '00043'
	orange_21 = '01042'
	orange_22 = '01132'

	violet_1  = '00041'
	violet_2  = '00220'
	violet_14 = '00243'
	violet_17 = '02042'

	red_0  = '00010'
	red_2  = '00141'
	red_5  = '01041'
	red_6  = '01220'
	red_12 = '00001'
	red_13 = '00042'
	red_14 = '00132'
	red_15 = '00311'
	red_16 = '00033'
	red_19 = '00343'
	red_22 = '01243'

	# ⟨loop:[blue:0]:00005⟩ ∘ ⟨loop:[red:0]:00010⟩
	# addrs += [blue_0, blue_12, blue_13, blue_16]
	# addrs += [red_0, red_12, red_13, red_16]	

	# ⟨loop:[green:0]:00004⟩ ∘ ⟨loop:[red:12]:00001⟩
	# addrs += [green_0, green_12, green_13, green_16]
	# addrs += [red_12, red_13, red_14, red_15]
	
	# ⟨loop:[yellow:0]:00030⟩ ∘ ⟨loop:[red:13]:00042⟩
	# addrs += [yellow_0, yellow_12, yellow_13, yellow_16]
	# addrs += [red_13, red_16, red_19, red_22]
	
	# ⟨loop:[orange:6]:01141⟩ ∘ ⟨loop:[red:5]:01041⟩
	# addrs += [orange_6, orange_9, orange_21, orange_22]
	# addrs += [red_5, red_6, red_13, red_22]	
	
	# ⟨loop:[red:2]:00141⟩ ∘ ⟨loop:[violet:1]:00041⟩
	# addrs += [red_2, red_5, red_13, red_14]		
	# addrs += [violet_1, violet_2, violet_14, violet_17]
	
	for addr in addrs:
		diagram.extendLoop(diagram.nodeByAddress[addr].loop)
	
	# unavailable = [l for l in diagram.loops if not l.available]
	# print(f"unavailable loops: {len(unavailable)}")
	# print(' '.join([l.firstAddress() for l in unavailable]))
	
	# for loop in diagram.loops:
	# 	if loop.ktype == 5:
	# 		print(f"loops += diagram.nodeByAddress['{loop.firstAddress()}']")
	
	show(diagram)
