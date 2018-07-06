def id(x): return x

def groupby(L, K = id, V = id, G = id, S = id):
	r = {}
	for e in L:
		k = K(e)
		if k not in r.keys():
			r[k] = []
		r[k].append(V(e))
	return S({ k:G(g) for k,g in r.items() })
