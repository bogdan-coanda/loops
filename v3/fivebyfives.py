L = [set([0, 1, 2, 3, 4]), set(), set(), set(), set()]
C = [set([0]), set([1]), set([2]), set([3]), set([4])]
𝒟 = [[0, 1, 2, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
# 𝒟[line][column]

def 𝓖5(lineindex=1, columnindex=0):
	
	if lineindex is 5:
		yield [list(line) for line in 𝒟]
		#print("---["+str(cc)+"]---\n"+"\n".join(["".join([str(x) for x in line]) for line in 𝒟])+"\n----------")
		
		
	elif columnindex is 5:
		for d in 𝓖5(lineindex+1, 0):
			yield d
		
	else:
		for q in range(5):
			if q not in C[columnindex] and q not in L[lineindex]:
				C[columnindex].add(q)
				L[lineindex].add(q)
				𝒟[lineindex][columnindex] = q
				for d in 𝓖5(lineindex, columnindex+1):
					yield d
				L[lineindex].remove(q)
				C[columnindex].remove(q)

if __name__ == "__main__":
	cc = 0
	for d in 𝓖5():
		print("---["+str(cc)+"]---\n"+"\n".join(["".join([str(x) for x in line]) for line in d])+"\n----------")
		cc += 1
		
