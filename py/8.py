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


	extendAddress("1234000")
	extendAddress("1234010")
	extendAddress("1234020")
	extendAddress("1234030")
	extendAddress("1234040")				
	
	extendAddress("1234110")
	extendAddress("1234120")
	extendAddress("1234130")
	extendAddress("1234140")				
	extendAddress("1234150")	
			
	extendAddress("1234200")
	extendAddress("1234210")
	extendAddress("1234220")
	extendAddress("1234230")
	extendAddress("1234240")				
	
	extendAddress("1234310")
	extendAddress("1234320")
	extendAddress("1234330")
	extendAddress("1234340")				
	extendAddress("1234350")	

	extendAddress("1234400")
	extendAddress("1234410")
	extendAddress("1234420")
	extendAddress("1234430")
	extendAddress("1234440")				
	
	extendAddress("1234510")
	extendAddress("1234520")
	extendAddress("1234530")
	extendAddress("1234540")				
	extendAddress("1234550")	
			
			
			
	extendAddress("0134407")
	extendAddress("0224407")			
	extendAddress("0233407")
	extendAddress("0234307")			
	extendAddress("1233107")
	extendAddress("1232207")
	extendAddress("1231307")
	extendAddress("1230407")
	extendAddress("1024107")
	extendAddress("1114107")
	extendAddress("1203207")
	extendAddress("1204107")	
					
	# ~~~~~~~~~~~~~~~~~~~~ #
	
	extendAddress("1233006")
	extendAddress("1233206")
	extendAddress("1233406")
	
	extendAddress("1203106")
	extendAddress("1203306")									
	extendAddress("1203506")	
													
	extendAddress("1230106")
	extendAddress("1230306")									
	extendAddress("1230506")
	
	extendAddress("1024006")
	extendAddress("1024206")
	extendAddress("1024406")

	extendAddress("0134106")
	extendAddress("0134306")									
	extendAddress("0134506")
	
	extendAddress("0234006")
	extendAddress("0234206")
	extendAddress("0234406")
	
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
																					
	extendAddress("1204006")
	extendAddress("1204206")
	extendAddress("1204406")
																					
	extendAddress("1232106")
	extendAddress("1232306")
	extendAddress("1232506")																					

	extendAddress("1231006")
	extendAddress("1231206")
	extendAddress("1231406")																					

	extendAddress("0224106")
	extendAddress("0224306")
	extendAddress("0224506")																						
	
	extendAddress("0233106")
	extendAddress("0233306")
	extendAddress("0233506")					
	
	extendAddress("1114006")
	extendAddress("1114206")
	extendAddress("1114406")
																					
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
																					
	extendAddress("1233033")
	extendAddress("1203042")
	extendAddress("1230024")
	extendAddress("1024051")
	extendAddress("0134006")	
	extendAddress("0234015")
	
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
	# ~~~~~~~~~~~~~~~~~~~~ #
	
	extendAddress("1232006")
	extendAddress("1232042")
	extendAddress("1231015")
	extendAddress("1231051")
	extendAddress("1204033")
	extendAddress("1204051")		
	extendAddress("1114033")
	extendAddress("1114051")	
	extendAddress("0224006")
	extendAddress("0224024")			
	extendAddress("0233006")
	extendAddress("0233024")		
	
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
