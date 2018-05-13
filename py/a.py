from diagram import *
from uicanvas import *
from uicanvas import chainColors

diagram = Diagram(6)
diagram.loadKnowns()

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

# targetLoops = [diagram.nodeByAddress[address].loop for address in [
# 	'01025', '01115', '01205', '01335', 
# 	'02025', '02115', '02245', '02335', 
# 	'12013', '12022', '12120', '12210', '12030', '12300']]
# targetLoops = [diagram.nodeByAddress[address].loop for address in [
# 	'11025', '11115', '11205', '11335', 
# 	'02025', '02115', '02245', '02335', 
# 	'12113', '12122', '12220', '12310', '12130', '12000']]
# targetLoops = [diagram.nodeByAddress[address].loop for address in [
# 	'11025', '11115', '11205', '11335', 
# 	'10025', '10115', '10245', '10335', 
# 	'12213', '12222', '12320', '12010', '12230', '12100']]
# targetLoops = [diagram.nodeByAddress[address].loop for address in [
# 	'01025', '01115', '01205', '01335', 
#		'10025', '10115', '10245', '10335', 
# 	'12313', '12322', '12020', '12110', '12330', '12200']]
			
targetLoops = [diagram.nodeByAddress[address].loop for address in [
	'01025', '01115', '01205', '01335', 
	'02025', '02115', '02245', '02335', 
	'11013', '11022', '11120', '11210', '11030', '11300']]			
			
pf = diagram.knowns

for target in targetLoops:
	pf = list(filter(lambda sol: target in [diagram.nodeByPerm[step.perm].loop for step in sol.state], pf))
	print(len(pf))
	
for sol in [pf[0]]:
	d = Diagram(6)
	for step in sol.state:
		n = d.nodeByPerm[step.perm]
		#n.loop.color = 𝒞(n)
		for nln in n.loop.nodes:
			nln.color = 𝒞(nln)
		d.extendLoop(n)
	show(d)
		

