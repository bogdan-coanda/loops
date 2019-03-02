class Permutator (object):
	
	def __init__(self, inputArr):
		self.results = []
		# print("[permutator] input: " + str(inputArr))
		self.permute(inputArr, [])
	
	def permute(self, arr, memo):
		# print("[permute] start | arr: " + str(arr) + " | memo: " + str(memo))
		for i in range(len(arr)):
			curr = arr[i]
			del arr[i]
			# print("[permute] i: " + str(i) + " | cur: " + str(curr) + " | arr: " + str(arr) + " | memo: " + str(memo))
			if len(arr) == 0:
				self.results += [memo + [curr]]
				# print("[permute] pushed result: " + str(self.results[-1]))
						
			self.permute(arr, memo + [curr]);
			arr.insert(i, curr)
			# print("[permute] after splice i: " + str(i) + " | cur[0]: " + str(curr) + " | arr: " + str(arr))
		# print("[permute] on return: " + str(self.results))


class SPGenerator(object):
	
	def __init__(self, startPerm):
		self.N = len(startPerm)
		
		curr_addr = '0' * (self.N-1)
		curr_perm = startPerm
		next_perm = curr_perm
		gn_cc = 0
		gn_qq = 0
		
		self.perms = []
		self.addrs = []
		
		def next(lvl = 2):
			nonlocal curr_addr, curr_perm, next_perm
			
			if lvl == self.N + 1:
				curr_perm = next_perm

				# print("appending @" + str(len(self.perms)) + ": ⟨" + curr_perm + "|" + curr_addr + "⟩")
				
				self.perms.append(curr_perm)
				self.addrs.append(curr_addr)

				next_perm = D1(curr_perm)
				return
								
			for q in range(0, lvl):
				curr_addr = curr_addr[:lvl-2] + str(q) + curr_addr[lvl-1:]
				next(lvl + 1)
				next_perm = DX(self.N - lvl + 1, curr_perm)
																	
		next()
		
		
	

def D1(perm):
	return perm[1:] + perm[0] 

def R1(perm):
	return perm[-1] + perm[0:-1]

def DX(x, perm):
	return perm[x:] + perm[0:x][::-1]

def RX(x, perm):
	return perm[-x:][::-1] + perm[0:-x]

def D2(perm): return DX(2, perm)
def D3(perm): return DX(3, perm)
def D4(perm): return DX(4, perm)
def D5(perm): return DX(5, perm)
def D6(perm): return DX(6, perm)

def R2(perm): return RX(2,perm)
def R3(perm): return RX(3,perm)
def R4(perm): return RX(4,perm)
def R5(perm): return RX(5,perm)
def R6(perm): return RX(6,perm)

def L3a(perm): return perm[3:]+perm[2]+perm[1]+perm[0]
def L3b(perm): return perm[3:]+perm[2]+perm[0]+perm[1]
def L3c(perm): return perm[3:]+perm[1]+perm[2]+perm[0]


if __name__ == "__main__":
		
	sp = SPGenerator("0123")
	
	print("###")
		
	p = Permutator([0,1,2,3,4])
	
	print("---")
	
	print(len(set([tuple(perm) for perm in p.results])))
	
	print(":::")	
	
	print(p.results)
	
	print("===")
	
	perm = "01234"
	print(perm)
	print(D1(perm))
	print(D2(perm))	
	print(D3(perm))
	print(D4(perm))
	print(R1(perm))
	print(R2(perm))
	print(R3(perm))	
	print(R4(perm))
	
	print("~~~")
	
	perm = "01234567"
	print(perm)
	print(L3a(perm))
	print(L3b(perm))	
	print(L3c(perm))	
