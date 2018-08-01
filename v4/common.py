from math import floor
from PIL import Image
import io

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
	

