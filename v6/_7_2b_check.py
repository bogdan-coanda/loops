from collections import defaultdict


results1 = defaultdict(int)		
results2 = defaultdict(int)
	
with open("_7sync4coercedresults1b.txt", 'r') as log:
	lines1 = log.read().splitlines()
	for line in lines1:
		if not line.startswith("==="):
			key = tuple(int(x) for x in line.split(" : ")[0][1:-1].split(", "))
			val = int(line.split(" : ")[1])
			results1[key] += val

with open("_7sync4coercedresults2b.txt", 'r') as log:
	lines2 = log.read().splitlines()
	for line in lines2:
		if not line.startswith("==="):
			key = tuple(int(x) for x in line.split(" : ")[0][1:-1].split(", "))
			val = int(line.split(" : ")[1])
			results2[key] += val
					
grouped1 = sorted(results1.items())
grouped2 = sorted(results2.items())
#print("\n".join(str(g[0])+": "+str(g[1]) for g in grouped1))				
