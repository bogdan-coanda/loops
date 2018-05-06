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
	
	extenders = [diagram.generateDiagramForKnownID(ik).extender() for ik in range(len(diagram.knowns))]
	print("Found " + str(len(set(extenders))) + "/" + str(len(extenders)) + " distinct roads")	
	
	with open("extenders."+str(diagram.spClass)+".pkl", 'wb') as outfile:
		pickle.dump(set(extenders), outfile, 0)	
		
	#with open('roads.'+str(diagram.spClass)+".pkl", 'rb') as infile:	
		#roads = list(pickle.load(infile))
	#print("Loaded "+str(len(roads))+" unique roads")
	
	
