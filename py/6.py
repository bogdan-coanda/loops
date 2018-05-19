from diagram import *
from jk import *

def 𝒞(node):
	if node.address[-1] == '5':
		return 'deepskyblue'
	elif int(node.address[-1]) + int(node.address[-2]) == 4:
		if node.address[-1] in ['0', '4']:
			return 'green'#'#99ff99'
		else:
			return 'limegreen'
	else:
		if node.address[-1] in ['0', '4']:
			return 'darkred'#'#ffbbbb'
		else:
			return 'red'
			
			
def run():
	diagram = Diagram(6)
	
	def extendAddress(address):
		node = diagram.nodeByAddress[address]
		assert diagram.extendLoop(
			sorted(node.loop.nodes, key = lambda n: n.looped).pop()
			if not node.looped and len([n for n in node.loop.nodes if n.looped]) is not 0
			else node)
		for nln in node.loop.nodes:
			nln.color = 𝒞(nln)
		return node.loop
	
	def extendReverse(address):
		last = diagram.nodeByAddress[address]
		return extendAddress(last.prevs[1].node.address)
	
	α = diagram.nodeByAddress['12020']
	β = diagram.nodeByAddress['12125']
	γ = diagram.nodeByAddress['12220']
	δ = diagram.nodeByAddress['12325']
	
	for node in [α, γ]:
		node.marked = True
		extendAddress(node.address)
		#						'''2'''				'''1'''				'''1'''				'''1'''
		node = node.nextLink.next.nextLink.next.nextLink.next.nextLink.next		
		node.marked = True
		extendAddress(node.address)
		#						'''2'''				'''1'''				
		node = node.nextLink.next.nextLink.next
		extendAddress(node.address)
		#						'''2'''				'''1'''				'''1'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				
		node = node.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next
		print(str(node))
		extendAddress(node.address)		
		
	
	for node in [β, δ]:
		node.marked = True
		extendReverse(node.address)
		#						'''2'''				'''1'''				'''1'''				'''1'''
		node = node.prevLink.node.prevLink.node.prevLink.node.prevLink.node		
		node.marked = True
		extendReverse(node.address)													
		#						'''2'''				'''1'''				
		node = node.prevLink.node.prevLink.node
		extendReverse(node.address)	
		#						'''2'''				'''1'''				'''1'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				'''1'''				'''1'''				'''2'''				'''1'''				'''1'''				'''1'''				
		node = node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node
		print(str(node))
		extendReverse(node.address)			
		
													
	#extendAddress('12200')
	#extendAddress('12210')
	##extendAddress('12220')
	##extendAddress('12110')
	#extendAddress('12120')
	#extendAddress('12130')
		
		
	#extendAddress('12320')
	#extendAddress('12330')
	#extendAddress('12000')
	#extendAddress('12010')
	
		
	##extendAddress('01225')
	##extendAddress('02125')
	#extendAddress('10225')
	#extendAddress('11125')

	#extendAddress('01104')
	#extendAddress('01304')
	#extendAddress('02004')
	#extendAddress('02204')
	#extendAddress('10104')
	#extendAddress('10304')
	#extendAddress('11004')
	#extendAddress('11204')
	
	# diagram.nodeByAddress['00102'].loop.color = 'purple'
	# diagram.nodeByAddress['00302'].loop.color = 'violet'
	# diagram.nodeByAddress['00042'].loop.color = 'orange'
	# diagram.nodeByAddress['00242'].loop.color = 'black'		
	# 
		
	#extendAddress('00001')
	# 
	# diagram.nodeByAddress['01304'].loop.color = 'purple
	# extendAddress('01304')
	# extendAddress('01140')
	# extendAddress('02004')
	# extendAddress('02204')
	# extendAddress('10144')
	# extendAddress('10122')
	# extendAddress('10324')	
	# extendAddress('11022')	
	# # 
	
	# 
	# diagram.nodeByAddress['02313'].loop.color = 'purple'
	# extendAddress('02222')
	# 
	# diagram.nodeByAddress['02331'].loop.color = 'purple'
	# extendAddress('02331')
	# 
	
	
	show(diagram)
	return diagram
	
	
if __name__ == "__main__":
	from common import Step, Sol
	diagram = run()
