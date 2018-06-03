import ui
from diagram import *
from colorsys import hls_to_rgb
from random import random
from enum import Enum
from uicanvas import *
from itertools import chain


def run():

	diagram = Diagram(6)
	
	def extend(loop):
		assert diagram.extendLoop(loop)
		for l in diagram.loops:
			if l.availabled and len([n for n in l.nodes if n.chainID is not None]) is not 0:
				l.availabled = False

	def extendAddress(address):
		extend(diagram.nodeByAddress[address].loop)

	'''# type:0
	for i2 in range(2):
		for i3 in range(3):
			for i4 in range(4):
				extendAddress(''.join([str(x) for x in [i2, i3, i4, 0, 5]]))	
	
	assert sorted([
			l for l in diagram.loops if l.extended
		]) == sorted([
			l for l in diagram.loops if l.head.address.endswith('05')])	
	#'''
	'''# type:1
	for i2 in range(2):
		for i3 in range(3):
			for i4 in range(4):
				extendAddress(''.join([str(x) for x in [i2, i3, i4, 4, 0]]))
				
	assert sorted([
			l for l in diagram.loops if l.extended
		]) == sorted([
			l for l in diagram.loops if l.head.address.endswith('40')])				
	#'''
	'''# type:2
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 4])
	
	for i2 in range(2):
		for i3 in range(3):
			for i4 in range(4):
				extendAddress(''.join([str(x) for x in [i2, i3, i4, (3-i4)%4, 0]]))
				
	assert sorted([
			l for l in diagram.loops if l.extended
		]) == sorted([
			l for l in diagram.loops if l.head.address[-1] == '0' and int(l.head.address[-2]) == (3-int(l.head.address[-3]))%4])				
	#'''
	'''# type:3
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 5])

	for i2 in range(2):			
		for i4 in range(4):
			for i3 in range(3):
				extendAddress(''.join([str(x) for x in [i2, i3, i4, (((2-i3)%3)-i4)%4, '0']]))
				# extendAddress(''.join([str(x) for x in [i2, i3, (i4-i3)%4, (2-i4)%4, 0]]))

	assert sorted([
			l for l in diagram.loops if l.extended
		]) == sorted([
			l for l in diagram.loops if l.head.address[-1] == '0' and int(l.head.address[-2]) == (((2-int(l.head.address[-4]))%3)-int(l.head.address[-3]))%4])												
	#'''
	'''# type:4
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 5])

	for i2 in range(2):
		for i3 in range(3):
			for i4 in range(4):
				extendAddress(''.join([str(x) for x in [i2, i3, i4, (((((1-i2)%2)-i3)%3)-i4)%4, '0']]))
				
	assert sorted([
			l for l in diagram.loops if l.extended
		]) == sorted([
			l for l in diagram.loops if l.head.address[-1] == '0' and int(l.head.address[-2]) == (((((1-int(l.head.address[-5]))%2)-int(l.head.address[-4]))%3)-int(l.head.address[-3]))%4])				
	#'''	
	'''# type:5
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 5])
		
	for i4 in range(4):
		for i3 in range(3):
			for i2 in range(2):
				extendAddress(''.join([str(x) for x in [i2, i3, i4, (((((0-i2)%2)-i3)%3)-i4)%4, '0']]))
								
	assert sorted([
			l for l in diagram.loops if l.extended
		]) == sorted([
			l for l in diagram.loops if l.head.address[-1] == '0' and int(l.head.address[-2]) == (((((0-int(l.head.address[-5]))%2)-int(l.head.address[-4]))%3)-int(l.head.address[-3]))%4])				
	#'''
			
	U0 = sorted([l for l in diagram.loops if l.head.address.endswith('05')])
	U1 = sorted([l for l in diagram.loops if l.head.address.endswith('40')])
	U2 = sorted([l for l in diagram.loops if l.head.address[-1] == '0' and int(l.head.address[-2]) == (3-int(l.head.address[-3]))%4])
	U3 = sorted([l for l in diagram.loops if l.head.address[-1] == '0' and int(l.head.address[-2]) == (((2-int(l.head.address[-4]))%3)-int(l.head.address[-3]))%4])
	U4 = sorted([
l for l in diagram.loops if l.head.address[-1] == '0' and int(l.head.address[-2]) == (((((1-int(l.head.address[-5]))%2)-int(l.head.address[-4]))%3)-int(l.head.address[-3]))%4])
	U5 = sorted([
l for l in diagram.loops if l.head.address[-1] == '0' and int(l.head.address[-2]) == (((((0-int(l.head.address[-5]))%2)-int(l.head.address[-4]))%3)-int(l.head.address[-3]))%4])

	assert sorted(diagram.loops) == sorted(chain(U0, U1, U2, U3, U4, U5))

	assert sorted(chain(*[l.nodes for l in U0])) == sorted([n for n in diagram.nodes if n.address[-1] == '5'])
	assert sorted(chain(*[l.nodes for l in U1])) == sorted([n for n in diagram.nodes if int(n.address[-1]) == 4 - int(n.address[-2])])
	assert sorted(chain(*[l.nodes for l in U2])) == sorted([n for n in diagram.nodes if int(n.address[-1]) == ((((3 - int(n.address[-3])) % 4 ) - int(n.address[-2])) % 5)])
	assert sorted(chain(*[l.nodes for l in U3])) == sorted([n for n in diagram.nodes if int(n.address[-1]) == ((((((2 - int(n.address[-4])) % 3 ) - int(n.address[-3])) % 4 ) - int(n.address[-2])) % 5)])
	assert sorted(chain(*[l.nodes for l in U4])) == sorted([n for n in diagram.nodes if int(n.address[-1]) == ((((((((1 - int(n.address[-5])) % 2 ) - int(n.address[-4])) % 3 ) - int(n.address[-3])) % 4 ) - int(n.address[-2])) % 5)])
	assert sorted(chain(*[l.nodes for l in U5])) == sorted([n for n in diagram.nodes if int(n.address[-1]) == ((((((((0 - int(n.address[-5])) % 2 ) - int(n.address[-4])) % 3 ) - int(n.address[-3])) % 4 ) - int(n.address[-2])) % 5)])

	assert sorted(chain(*[l.nodes for l in U0])) == sorted([n for n in diagram.nodes if 0 == 5 - int(n.address[-1])])
	assert sorted(chain(*[l.nodes for l in U1])) == sorted([n for n in diagram.nodes if 0 == 4 - int(n.address[-2]) - int(n.address[-1])])			
	assert sorted(chain(*[l.nodes for l in U2])) == sorted([n for n in diagram.nodes if 0 == ((((3 - int(n.address[-3])) % 4 ) - int(n.address[-2])) % 5) - int(n.address[-1])])
	assert sorted(chain(*[l.nodes for l in U3])) == sorted([n for n in diagram.nodes if 0 == ((((((2 - int(n.address[-4])) % 3 ) - int(n.address[-3])) % 4 ) - int(n.address[-2])) % 5) - int(n.address[-1])])		
	assert sorted(chain(*[l.nodes for l in U4])) == sorted([n for n in diagram.nodes if 0 == ((((((((1 - int(n.address[-5])) % 2 ) - int(n.address[-4])) % 3 ) - int(n.address[-3])) % 4 ) - int(n.address[-2])) % 5) - int(n.address[-1])])	
	assert sorted(chain(*[l.nodes for l in U5])) == sorted([n for n in diagram.nodes if 0 == ((((((((0 - int(n.address[-5])) % 2 ) - int(n.address[-4])) % 3 ) - int(n.address[-3])) % 4 ) - int(n.address[-2])) % 5) - int(n.address[-1])])
	
	
	for i,u in enumerate([U0, U1, U2, U3, U4, U5]):
		for l in u:
			l.utype = i	
		
	'''
																						 0 == i5 && 5 == i6
																						 4 == i5 && 0 == i6
																( 3 - i4 ) % 4 == i5 && 0 == i6
								 ((( 2 - i3 ) % 3 ) - i4 ) % 4 == i5 && 0 == i6
	((((( 1 - i2 ) % 2 ) - i3 ) % 3 ) - i4 ) % 4 == i5 && 0 == i6
	((((( 0 - i2 ) % 2 ) - i3 ) % 3 ) - i4 ) % 4 == i5 && 0 == i6
	'''
	
	'''
	(ABCDYZ) ABCDEF -> BCDEFA -> CDEFAB -> DEFABC -> EFABCD -> FABCDE »»
	(BCDYAZ) BCDEAF -> CDEAFB -> DEAFBC -> EAFBCD -> AFBCDE -> FBCDEA »»
	(CDYABZ) CDEABF -> DEABFC -> EABFCD -> ABFCDE -> BFCDEA -> FCDEAB »»
	(DYABCZ) DEABCF -> EABCFD -> ABCFDE -> BCFDEA -> CFDEAB -> FDEABC »»
	(YABCDZ) EABCDF -> ABCDFE -> BCDFEA -> CDFEAB -> DFEABC -> FEABCD ⇒⇒	
	'''
	
		
						
	# diagram.generateKernel()		

	'''		
	for l in diagram.loops:
		if len([n for n in l.nodes if n.chainID is not None]) is not 0:
			l.availabled = False 
	'''
				
	diagram.loadExtenders()
				
	show(diagram)
	diagram.measure()
	return diagram

	
if __name__ == "__main__":
	diagram = run()
	
