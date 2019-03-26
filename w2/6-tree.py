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

	diagram = Diagram(6, kernelPath='222')
	cOc('2322 2232 2223 2222')
	
	loops = []
	
	# ---  blue  --- #
	# loops += [diagram.nodeByAddress['00005'].loop]
	# loops += [diagram.nodeByAddress['00105'].loop]
	# loops += [diagram.nodeByAddress['00205'].loop]
	# loops += [diagram.nodeByAddress['00305'].loop]
	# 
	loops += [diagram.nodeByAddress['01005'].loop]
	loops += [diagram.nodeByAddress['01105'].loop]
	loops += [diagram.nodeByAddress['01205'].loop]
	loops += [diagram.nodeByAddress['01305'].loop]
	# 
	# loops += [diagram.nodeByAddress['02005'].loop]
	# loops += [diagram.nodeByAddress['02105'].loop]
	# loops += [diagram.nodeByAddress['02205'].loop]
	# loops += [diagram.nodeByAddress['02305'].loop]
	# 
	# loops += [diagram.nodeByAddress['10005'].loop]
	# loops += [diagram.nodeByAddress['10105'].loop]
	loops += [diagram.nodeByAddress['10205'].loop]
	# loops += [diagram.nodeByAddress['10305'].loop]
	# 
	loops += [diagram.nodeByAddress['11005'].loop]
	loops += [diagram.nodeByAddress['11105'].loop]
	loops += [diagram.nodeByAddress['11205'].loop]
	# loops += [diagram.nodeByAddress['11305'].loop]
	# 
	loops += [diagram.nodeByAddress['12005'].loop]
	loops += [diagram.nodeByAddress['12105'].loop]
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
	loops += [diagram.nodeByAddress['02004'].loop]
	loops += [diagram.nodeByAddress['02104'].loop]
	loops += [diagram.nodeByAddress['02204'].loop]
	loops += [diagram.nodeByAddress['02304'].loop]
	# 
	# loops += [diagram.nodeByAddress['10004'].loop]
	loops += [diagram.nodeByAddress['10104'].loop]
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
	loops += [diagram.nodeByAddress['10003'].loop]
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
	# loops += [diagram.nodeByAddress['00002'].loop]
	# loops += [diagram.nodeByAddress['00011'].loop]
	# loops += [diagram.nodeByAddress['00020'].loop]
	# loops += [diagram.nodeByAddress['00043'].loop]
	# 
	# loops += [diagram.nodeByAddress['00101'].loop]
	# loops += [diagram.nodeByAddress['00110'].loop]
	loops += [diagram.nodeByAddress['00133'].loop]
	# loops += [diagram.nodeByAddress['00142'].loop]
	# 
	# loops += [diagram.nodeByAddress['00200'].loop]
	# loops += [diagram.nodeByAddress['00223'].loop]
	# loops += [diagram.nodeByAddress['00232'].loop]
	# loops += [diagram.nodeByAddress['00241'].loop]
	# 
	# loops += [diagram.nodeByAddress['01001'].loop]
	# loops += [diagram.nodeByAddress['01010'].loop]
	loops += [diagram.nodeByAddress['01033'].loop]
	# loops += [diagram.nodeByAddress['01042'].loop]
	# 
	# loops += [diagram.nodeByAddress['01100'].loop]
	loops += [diagram.nodeByAddress['01123'].loop]
	# loops += [diagram.nodeByAddress['01132'].loop]
	# loops += [diagram.nodeByAddress['01141'].loop]
	# 
	# loops += [diagram.nodeByAddress['01302'].loop]
	# loops += [diagram.nodeByAddress['01311'].loop]
	# loops += [diagram.nodeByAddress['01320'].loop]
	loops += [diagram.nodeByAddress['01343'].loop]	
																						
	# ---  red  --- #
	# loops += [diagram.nodeByAddress['00001'].loop]
	# loops += [diagram.nodeByAddress['00010'].loop]
	# loops += [diagram.nodeByAddress['00033'].loop]
	loops += [diagram.nodeByAddress['00042'].loop]
	# 
	# loops += [diagram.nodeByAddress['00100'].loop]
	# loops += [diagram.nodeByAddress['00123'].loop]
	# loops += [diagram.nodeByAddress['00132'].loop]
	# loops += [diagram.nodeByAddress['00141'].loop]
	# 
	# loops += [diagram.nodeByAddress['00302'].loop]
	# loops += [diagram.nodeByAddress['00311'].loop]
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
	
	loops += [diagram.nodeByAddress['02302'].loop]
	loops += [diagram.nodeByAddress['02311'].loop]
	loops += [diagram.nodeByAddress['02320'].loop]
	loops += [diagram.nodeByAddress['02343'].loop]

	for loop in loops:
		diagram.extendLoop(loop)
	
	# unavailable = [l for l in diagram.loops if not l.available]
	# print(f"unavailable loops: {len(unavailable)}")
	# print(' '.join([l.firstAddress() for l in unavailable]))
	
	# for loop in diagram.loops:
	# 	if loop.ktype == 5:
	# 		print(f"loops += diagram.nodeByAddress['{loop.firstAddress()}']")
	
	show(diagram)
