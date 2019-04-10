from math import floor
#from PIL import Image
import io
import math
from colorsys import hls_to_rgb
from random import random

def id(x): return x

def groupby(L, K = id, V = id, G = id, S = id):
	r = {}
	for e in L:
		k = K(e)
		if k not in r.keys():
			r[k] = []
		r[k].append(V(e))
	return S({ k:G(g) for k,g in r.items() })
	
def tstr(s):
	return "" + str(int(floor(s / 60))) + "m" + str(int(floor(s)) % 60) + "s." + str(int(s * 1000) % 1000)
	
def ui2pil(ui_img):
	png_data = ui_img.to_png()
	return Image.open(io.BytesIO(png_data))
	
class ordered_set (object):
	
	def __init__(self):
		self.data = []
		
	def add(self, obj):
		if obj not in self.data:
			self.data.append(obj)
			
	def pop(self):
		return self.data.pop(0)
		
	def __len__(self):
		return len(self.data)
		
_unitRootsCache = {}
		
def unitRoots(root_count, radius, unit_angle_fraction_offset):
	global _unitRootsCache
	if (root_count, radius, unit_angle_fraction_offset) not in _unitRootsCache:
		_unitRootsCache[(root_count, radius, unit_angle_fraction_offset)] = [(radius * math.cos(2 * math.pi * (i + unit_angle_fraction_offset) / root_count), radius * math.sin(2 * math.pi * (i + unit_angle_fraction_offset) / root_count))  for i in range(root_count)]
	return _unitRootsCache[(root_count, radius, unit_angle_fraction_offset)]
	
def upper(number):
	ups = "⁰¹²³⁴⁵⁶⁷⁸⁹"
	return "".join([ups[int(x)] for x in str(number)])
	
def input2(text):
	input(text+"  |  » ∘ «")	
	
def randomColor():
	return hls_to_rgb(random(), 0.5, 1)
	
	
NEWLINE = '\n'
