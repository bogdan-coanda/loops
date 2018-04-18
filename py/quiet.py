from diagram import *
from time import time
from math import floor
import pickle
from functools import cmp_to_key


def quiet(diagram, node):
	
	while node != None:
		
		if node.isExtendable():
			extend(diagram, node)	
			quiet(diagram, node.nextLink.next)
			collaps
		node = node.nextLink.next
