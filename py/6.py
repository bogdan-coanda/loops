from diagram import *
from jk import *
from explorer import groupby

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
	
	def extendNode(node):
		node.real = sorted(node.loop.nodes, key = lambda n: n.looped).pop() if not node.looped and len([n for n in node.loop.nodes if n.looped]) is not 0 else node
		node.real.marked = True
		assert diagram.extendLoop(node.real)
		for nln in node.loop.nodes:
			nln.color = 𝒞(nln)
	
	def extendAddress(address):
		extendNode(diagram.nodeByAddress[address])

	def extendReverse(last):
		return extendNode(last.prevs[1].node)
		
	def collapseNode(node):
		node.real.marked = False
		diagram.collapseLoop(node.real)

	def collapseReverse(last):
		collapseNode(last.prevs[1].node)

		
	
						
										
	# l1a = [l for l in diagram.loops if l.availabled and l.root() == '1']
	# extendNode(sorted(l1a[0].nodes, key=lambda n: n.address[-1])[0])
	# extendNode(sorted(l1a[1].nodes, key=lambda n: n.address[-1])[0])
	# extendNode(sorted(l1a[2].nodes, key=lambda n: n.address[-1])[0])
	# extendNode(sorted(l1a[3].nodes, key=lambda n: n.address[-1])[0])	
	# extendNode(sorted(l1a[4].nodes, key=lambda n: n.address[-1])[0])
	# extendNode(sorted(l1a[5].nodes, key=lambda n: n.address[-1])[0])
	# extendNode(sorted(l1a[6].nodes, key=lambda n: n.address[-1])[0])
	# extendNode(sorted(l1a[7].nodes, key=lambda n: n.address[-1])[0])
	# extendNode(sorted(l1a[8].nodes, key=lambda n: n.address[-1])[0])
	# extendNode(sorted(l1a[9].nodes, key=lambda n: n.address[-1])[0])
	# extendNode(sorted(l1a[10].nodes, key=lambda n: n.address[-1])[0])
	# extendNode(sorted(l1a[11].nodes, key=lambda n: n.address[-1])[0])
	# print(len(l1a))
	# 
	
	
	''' [~]
	
	α = diagram.nodeByAddress['12020']
	β = diagram.nodeByAddress['12125']
	γ = diagram.nodeByAddress['12220']
	δ = diagram.nodeByAddress['12325']
	
	for node in [α, γ]:
		node.marked = True
		extendAddress(node.address)
		#						···2···				···1···				···1···				···1···
		node = node.nextLink.next.nextLink.next.nextLink.next.nextLink.next		
		node.marked = True
		extendAddress(node.address)
		#						···2···				···1···				
		node = node.nextLink.next.nextLink.next
		extendAddress(node.address)
		#						···2···				···1···				···1···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				
		node = node.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next.nextLink.next
		print(str(node))
		extendAddress(node.address)		
		
	
	for node in [β, δ]:
		node.marked = True
		extendReverse(node.address)
		#						···2···				···1···				···1···				···1···
		node = node.prevLink.node.prevLink.node.prevLink.node.prevLink.node		
		node.marked = True
		extendReverse(node.address)													
		#						···2···				···1···				
		node = node.prevLink.node.prevLink.node
		extendReverse(node.address)	
		#						···2···				···1···				···1···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				···1···				···1···				···2···				···1···				···1···				···1···				
		node = node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node.prevLink.node
		print(str(node))
		extendReverse(node.address)			
						
	'''												
	
	
	
	#extendAddress('12345')
	#extendAddress('12245')	
	#extendAddress('12145')
	#extendAddress('12045')

	#extendAddress('12304')
	#extendAddress('12204')	
	#extendAddress('12104')
	#extendAddress('12004')
	
	#extendAddress('12003')
	#extendAddress('11003')
	#extendAddress('10003')
	
	#extendAddress('10002')
	#extendAddress('00002')
	# 	
	
	show(diagram)
	return diagram
	
	
if __name__ == "__main__":
	from common import Step, Sol
	diagram = run()
