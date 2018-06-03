import ui
from diagram import *
from colorsys import hls_to_rgb
from random import random
from enum import Enum
from uicanvas import *


def run():

	diagram = Diagram(7)
	
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
					extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, 0, 6]]))	
	#'''
	'''# type:1
	for i2 in range(2):
		for i3 in range(3):
			for i4 in range(4):
				for i5 in range(5):
					extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, 5, 0]]))
	#'''
	'''# type:2
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 4])
	
	for i2 in range(2):
		for i3 in range(3):
			for i4 in range(4):
				for i5 in range(5):
					extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, (4-i5)%5, 0]]))
	#'''
	# type:3
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 5])

	for i2 in range(2):
		for i3 in range(3):
			for i5 in range(5):
				for i4 in range(4):			
					extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, ((3-i4)%4-i5)%5, 0]]))
					# extendAddress(''.join([str(x) for x in [i2, i3, i4, (i5-i4)%5, (3-i5)%5, 0]]))
	#'''
	'''# type:4
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 6])

	for i2 in range(2):
		for i3 in range(3):
			for i4 in range(4):
				for i5 in range(5):
					extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, (((((2-i3)%3)-i4)%4)-i5)%5, '0']]))
	#'''	
	'''# type:5
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 6])
		
	for i5 in range(5):			
		for i4 in range(4):
			for i3 in range(3):
				for i2 in range(2):
					extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, (((((((1-i2)%2)-i3)%3)-i4)%4)-i5)%5, '0']]))
	#'''
	'''# type:6
	diagram.forceUnavailable([l for l in diagram.loops if l.type() is not 6])
	
	for i5 in range(5):
		for i4 in range(4):
			for i3 in range(3):
				for i2 in range(2):
					extendAddress(''.join([str(x) for x in [i2, i3, i4, i5, (((((((0-i2)%2)-i3)%3)-i4)%4)-i5)%5, '0']]))			
	#'''
			
	show(diagram)
	return diagram

	
if __name__ == "__main__":
	diagram = run()
	
