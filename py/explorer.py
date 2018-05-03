from diagram import Diagram
from time import time
import pickle

if __name__ == "__main__":
	from common import Step, Sol
	diagram = Diagram(6)
	diagram.loadKnowns()
	diagram.startTime = time()
	
	#superperms = [d.generateDiagramForKnownID(ik).superperm() for ik in range(len(d.knowns))]
	#print("Found " + str(len(set(superperms))) + " distinct superperms")
	
	roads = [diagram.generateDiagramForKnownID(ik).road() for ik in range(len(diagram.knowns))]
	print("Found " + str(len(set(roads))) + " distinct roads")
	
