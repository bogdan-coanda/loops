from diagram import Diagram
from time import time
import pickle

if __name__ == "__main__":
	from common import Step, Sol
	
	diagram = Diagram(6)
	diagram.loadKnowns()
	diagram.startTime = time()

	# --- superperms --- #
			
	#superperms = [d.generateDiagramForKnownID(ik).superperm() for ik in range(len(d.knowns))]
	#print("Found " + str(len(set(superperms))) + " distinct superperms")
	
	# --- roads --- #
	
	#roads = [diagram.generateDiagramForKnownID(ik).road() for ik in range(12)]#len(diagram.knowns))]
	#print("Found " + str(len(set(roads))) + " distinct roads")	
	
	#with open("roads."+str(diagram.spClass)+".pkl", 'wb') as outfile:
		#pickle.dump(set(roads), outfile, 0)

	#with open('roads.'+str(diagram.spClass)+".pkl", 'rb') as infile:	
		#roads = list(pickle.load(infile))
	#print("Loaded "+str(len(roads))+" unique roads")
	
	# --- extenders --- #
	
	'''
	extenders = []
	#ec = 0
	for ik in range(len(diagram.knowns)):
		𝒟 = diagram.generateDiagramForKnownID(ik)
#		𝒟.road()
#		if 𝒟.road_is_walked:
		extenders.append(𝒟.extender())
		#ec += 1
		#print(str(ec) + " / " + str(ik+1))
	
	print("Found " + str(len(extenders)) + " distinct extenders")	
	
	with open("extenders."+str(diagram.spClass)+".pkl", 'wb') as outfile:
		pickle.dump(extenders, outfile, 0)	
	'''
	with open('extenders.'+str(diagram.spClass)+".pkl", 'rb') as infile:	
		extenders = list(pickle.load(infile))
	print("Loaded "+str(len(extenders))+" extenders")
	
	extenders = [[diagram.nodeByPerm[perm] for perm in extender] for extender in extenders]
	
	
