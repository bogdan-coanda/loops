from diagram import Diagram
from time import time
import pickle

if __name__ == "__main__":
	from common import Step, Sol
	d = Diagram(6)
	d.loadKnowns()
	d.startTime = time()
	roads = [d.generateDiagramForKnownID(ik).road() for ik in range(len(d.knowns))]
	print("Found " + str(len(set(roads))) + " distinct roads")
	
	

