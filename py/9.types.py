import ui
from diagram import *
from colorsys import hls_to_rgb
from random import random
from enum import Enum
from uicanvas import *


def run():

	diagram = Diagram(9)
	
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
				for i5 in range(5):
					print('[run] ⟨'+str(i2)+str(i3)+str(i4)+str(i5)+'⟩')
					for i6 in range(6):
						for i7 in range(7):
							extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, i6, i7, 0, 8]]))	
	'''#
	'''# type:1
	for i2 in range(2):
		for i3 in range(3):
			for i4 in range(4):
				for i5 in range(5):
					print('[run] ⟨'+str(i2)+str(i3)+str(i4)+str(i5)+'⟩')
					for i6 in range(6):
						for i7 in range(7):
							extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, i6, i7, 7, 0]]))
	#'''
	'''# type:2
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 4])
	
	for i2 in range(2):
		for i3 in range(3):
			for i4 in range(4):
				for i5 in range(5):
					print('[run] ⟨'+str(i2)+str(i3)+str(i4)+str(i5)+'⟩')					
					for i6 in range(6):
						for i7 in range(7):
							extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, i6, i7, (6-i7)%7, 0]]))
	#'''
	# type:3
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 5])

	for i2 in range(2):
		for i3 in range(3):
			for i4 in range(4):
				for i5 in range(5):
					print('[run] ⟨'+str(i2)+str(i3)+str(i4)+str(i5)+'⟩')										
					for i6 in range(6):
						for i7 in range(7):
							extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, i6, i7, (((5-i6)%6)-i7)%7, 0]]))
							# extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, i6, (i7-i6)%7, (5-i7)%7, 0]]))
	#'''
	'''# type:4
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 6])

	for i2 in range(2):
		for i3 in range(3):
			for i4 in range(4):
				for i5 in range(5):
					print('[run] ⟨'+str(i2)+str(i3)+str(i4)+str(i5)+'⟩')															
					for i6 in range(6):
						for i7 in range(7):
							extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, i6, i7, (((((4-i5)%5)-i6)%6)-i7)%7, '0']]))
	#'''	
	'''# type:5
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 7])
		
	for i7 in range(7):
		for i6 in range(6):
			for i5 in range(5):			
				for i4 in range(4):
					print('[run] ⟨'+str(i7)+str(i6)+str(i5)+str(i4)+'⟩')										
					for i3 in range(3):
						for i2 in range(2):
							extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, i6, i7, (((((((3-i4)%4)-i5)%5)-i6)%6)-i7)%7, '0']]))
	#'''
	'''# type:6
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 8])
	
	for i7 in range(7):
		for i6 in range(6):
			for i5 in range(5):
				for i4 in range(4):
					print('[run] ⟨'+str(i7)+str(i6)+str(i5)+str(i4)+'⟩')										
					for i3 in range(3):
						for i2 in range(2):
							extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, i6, i7, (((((((((2-i3)%3)-i4)%4)-i5)%5)-i6)%6)-i7)%7, '0']]))			
	#'''
	'''# type:7
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 8])
	
	for i7 in range(7):
		for i6 in range(6):
			for i5 in range(5):
				for i4 in range(4):
					print('[run] ⟨'+str(i7)+str(i6)+str(i5)+str(i4)+'⟩')															
					for i3 in range(3):
						for i2 in range(2):
							extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, i6, i7, (((((((((((1-i2)%2-i3)%3)-i4)%4)-i5)%5)-i6)%6)-i7)%7), '0']]))			
	#'''
	'''# type:8
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 8])
	
	for i7 in range(7):
		for i6 in range(6):
			for i5 in range(5):
				for i4 in range(4):
					print('[run] ⟨'+str(i7)+str(i6)+str(i5)+str(i4)+'⟩')															
					for i3 in range(3):
						for i2 in range(2):
							extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, i6, i7, (((((((((((0-i2)%2-i3)%3)-i4)%4)-i5)%5)-i6)%6)-i7)%7), '0']]))			
	#'''				
	show(diagram)
	return diagram

	
if __name__ == "__main__":
	diagram = run()
	
