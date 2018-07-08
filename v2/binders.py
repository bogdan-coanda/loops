import math

for base in range(16, 41):
	ex_loops = (math.factorial(base - 3) - 1) * (base - 1)
	cycles_per_ex_loop = base - 2
	binders = 0
	while True:
		binders += 1
		extenders = ex_loops - binders
		subsets = binders * cycles_per_ex_loop
		if extenders % subsets == 0:		
			print("base: " + str(base) + " | ex. loops: " + str(ex_loops) + " | cycles per ex. loop: " + str(cycles_per_ex_loop) + "\n | extenders: " + str(extenders) + " | binders: " + str(binders) + " | subsets: " + str(subsets) + " | » loops per subset: " + str(extenders / subsets))
		if extenders < subsets:
			break
			
