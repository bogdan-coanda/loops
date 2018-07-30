class Permutator (object):
	
	def __init__(self, inputArr):
		self.results = []
#		print("[permutator] input: " + str(inputArr))
		self.permute(inputArr, [])
	
	def permute(self, arr, memo):
#		print("[permute] start | arr: " + str(arr) + " | memo: " + str(memo))
		for i in range(len(arr)):
			curr = arr[i]
			del arr[i]
#			print("[permute] i: " + str(i) + " | cur: " + str(curr) + " | arr: " + str(arr) + " | memo: " + str(memo))
			if len(arr) == 0:
				self.results += [memo + [curr]]
#				print("[permute] pushed result: " + str(self.results[-1]))
						
			self.permute(arr, memo + [curr]);
			arr.insert(i, curr)
#			print("[permute] after splice i: " + str(i) + " | cur[0]: " + str(curr) + " | arr: " + str(arr))
#		print("[permute] on return: " + str(self.results))

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

if __name__ == "__main__":
		
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
