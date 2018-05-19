from diagram import *
from jk import *

def 𝒞(node):
	if node.address[-1] == '7':
		return 'deepskyblue'
	elif int(node.address[-1]) + int(node.address[-2]) == 6:
		if node.address[-1] in ['0', '6']:
			return 'green'#'#99ff99'
		else:
			return 'limegreen'
	else:
		if node.address[-1] in ['0', '6']:
			return 'darkred'#'#ffbbbb'
		else:
			return 'red'
			
			
def run():
	diagram = Diagram(8)
	
	def extendAddress(address):
		node = diagram.nodeByAddress[address]
		assert diagram.extendLoop(
			sorted(node.loop.nodes, key = lambda n: n.looped).pop()
			if not node.looped and len([n for n in node.loop.nodes if n.looped]) is not 0
			else node)
		for nln in node.loop.nodes:
			nln.color = 𝒞(nln)
		return node.loop


	def drawBlock(address, reverse = False):
		
		for i in range(diagram.spClass-2): # 0:5
			for j in range(1, diagram.spClass-3): # 1:4
				extendAddress(address + str(i) + str(j) + '0')
			extendAddress(address + str(i) + ('0' if (reverse ^ (i % 2 == 0)) else str(diagram.spClass-3)) + '0') # 0/5

										
	drawBlock('1234')
	
	extendAddress('1233107')
	extendAddress('1233006')
	extendAddress('1233206')
	extendAddress('1233306')
	extendAddress('1233406')
		
	extendAddress('1230407')
	extendAddress('1230106')
	extendAddress('1230206')
	extendAddress('1230306')
	extendAddress('1230506')
		
	extendAddress('1203207')
	extendAddress('1203106')
	extendAddress('1203306')
	extendAddress('1203406')
	extendAddress('1203506')
	
	extendAddress('1024107')
	extendAddress('1024006')
	extendAddress('1024206')
	extendAddress('1024406')
	extendAddress('1024506')
	
	extendAddress('0234307')
	extendAddress('0234006')
	extendAddress('0234106')
	extendAddress('0234206')
	extendAddress('0234406')
	
	extendAddress('0134407')
	extendAddress('0134006')
	extendAddress('0134106')
	extendAddress('0134306')
	extendAddress('0134506')
	
	extendAddress('1233001')
	extendAddress('1203101')
	extendAddress('0134301')
	extendAddress('1230565')
	extendAddress('0234465')
	extendAddress('1024265')
		
	#drawBlock('1210', bar=True)
	#drawBlock('1222', bar=True)

	#drawBlock('1112', bar=True)

	#drawBlock('0034', bar=True)
	#drawBlock('0023', bar=True)
	#drawBlock('0104', bar=True)
	#drawBlock('0123', bar=True)
	#drawBlock('0223', bar=True)
	#drawBlock('0231', bar=True)

	#drawBlock('1121', bar=True)
	#drawBlock('1110', bar=True)
	#drawBlock('1002', bar=True)
	#drawBlock('1012', bar=True)
	#drawBlock('1220', bar=True)
	#drawBlock('1201', bar=True)

# 
	
	#drawBlock('1200')	
	#drawBlock('1211')	
	# 
	# drawBlock('1011')	
	# drawBlock("0223")


	# [~]
	#extendAddress("0000131")


	'''
	extendAddress("1004000")
	extendAddress("1004010")
	extendAddress("1004020")
	extendAddress("1004030")
	extendAddress("1004040")				
	
	extendAddress("1004110")
	extendAddress("1004120")
	extendAddress("1004130")
	extendAddress("1004140")				
	extendAddress("1004150")					
	
	extendAddress("1004200")
	extendAddress("1004210")
	extendAddress("1004220")
	extendAddress("1004230")
	extendAddress("1004240")				
	
	extendAddress("1004310")
	extendAddress("1004320")
	extendAddress("1004330")
	extendAddress("1004340")				
	extendAddress("1004350")						
										
	extendAddress("1004400")
	extendAddress("1004410")
	extendAddress("1004420")
	extendAddress("1004430")
	extendAddress("1004440")				
	
	extendAddress("1004510")
	extendAddress("1004520")
	extendAddress("1004530")
	extendAddress("1004540")				
	extendAddress("1004550")
'''

	'''
	extendAddress("0203000")
	extendAddress("0203010")	
	extendAddress("0203020")
	extendAddress("0203030")
	extendAddress("0203040")				

	extendAddress("0203110")
	extendAddress("0203120")
	extendAddress("0203130")
	extendAddress("0203140")				
	extendAddress("0203150")					

	extendAddress("0203200")
	extendAddress("0203210")
	extendAddress("0203220")
	extendAddress("0203230")
	extendAddress("0203240")				

	extendAddress("0203310")
	extendAddress("0203320")
	extendAddress("0203330")
	extendAddress("0203340")				
	extendAddress("0203350")						

	extendAddress("0203400")
	extendAddress("0203410")
	extendAddress("0203420")
	extendAddress("0203430")
	extendAddress("0203440")				

	extendAddress("0203510")
	extendAddress("0203520")
	extendAddress("0203530")
	extendAddress("0203540")				
	extendAddress("0203550")													
'''

				
	# extendAddress("0134407")
	# extendAddress("0224407")			
	# extendAddress("0233407")
	# extendAddress("0234307")			
	# extendAddress("1233107")
	# extendAddress("1232207")
	# extendAddress("1231307")
	# extendAddress("1230407")
	# extendAddress("1024107")
	# extendAddress("1114107")
	# extendAddress("1203207")
	# extendAddress("1204107")	
		
	# ~~~~~~~~~~~~~~~~~~~~ #

	# extendAddress("1233006")
	# extendAddress("1233206")
	# extendAddress("1233406")
	# 
	# extendAddress("1203106")
	# extendAddress("1203306")									
	# extendAddress("1203506")	
	# 
	# extendAddress("1230106")
	# extendAddress("1230306")									
	# extendAddress("1230506")
	# 
	# extendAddress("1024006")
	# extendAddress("1024206")
	# extendAddress("1024406")
	# 
	# extendAddress("0134106")
	# extendAddress("0134306")									
	# extendAddress("0134506")
	# 
	# extendAddress("0234006")
	# extendAddress("0234206")
	# extendAddress("0234406")
	
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #

	# extendAddress("1204006")
	# extendAddress("1204206")
	# extendAddress("1204406")
	# 
	# extendAddress("1232106")
	# extendAddress("1232306")
	# extendAddress("1232506")																					
	# 
	# extendAddress("1231006")
	# extendAddress("1231206")
	# extendAddress("1231406")																					
	# 
	# extendAddress("0224106")
	# extendAddress("0224306")
	# extendAddress("0224506")																						
	# 
	# extendAddress("0233106")
	# extendAddress("0233306")
	# extendAddress("0233506")					
	# 
	# extendAddress("1114006")
	# extendAddress("1114206")
	# extendAddress("1114406")
		
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
																					
	#extendAddress("1233033")
	#extendAddress("1203042")
	#extendAddress("1230024")
	#extendAddress("1024051")
	#extendAddress("0134006")	
	#extendAddress("0234015")
	
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
	
	#extendAddress("1232006")
	#extendAddress("1232042")
	#extendAddress("1231015")
	#extendAddress("1231051")
	#extendAddress("1204033")
	#extendAddress("1204051")		
	#extendAddress("1114033")
	#extendAddress("1114051")	
	#extendAddress("0224006")
	#extendAddress("0224024")			
	#extendAddress("0233006")
	#extendAddress("0233024")		
	
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #

	## extendAddress("1202307")
	# extendAddress("1202006")
	# extendAddress("1202024")
	# extendAddress("1202042")
	# 
	# extendAddress("1201407")
	# extendAddress("1201015")
	# extendAddress("1201033")
	# extendAddress("1201051")
	# extendAddress("1201316")

	# extendAddress("1200507")						
	# extendAddress("1200006")
	# extendAddress("1200024")
	# extendAddress("1200042")
	# extendAddress("1200417")	
	
	# diagram.nodeByAddress["1202215"].loop.color = 'red'
	
	# extendAddress("1202020")
	# extendAddress("1202010")
	# extendAddress("1202030")
	# extendAddress("1202040")
	# extendAddress("1202050")
	
	
#	extendAddress("1200042")
		
	show(diagram)
	return diagram
	
	
if __name__ == "__main__":
	from common import Step, Sol
	diagram = run()
	print("§§§")
