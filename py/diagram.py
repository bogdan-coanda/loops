from state import State
from drawn import Drawn
from forest import Forest
from superperms import Permutator

class Diagram (object):
	
	def __init__(self, N):
		# defaults to remember
		#self.k3cc = -2
		#self.k2cc = -1
		#self.k1cc = -1
		
		self.startPerm = self.generateGraph()
	
		self.startNode = None
		self.solution = ""
		self.mode = "LOOP"
		self.currentColor = "yellow"
		self.currentColorHue = 60
		self.arrowCount = [0, 0, 0]
		self.available_count = 0
			
		self.jkcc = 0	
		self.eecc = 0
		self.RR = 1200
		self.mxlvl = 0
		self.auto = True
		self.cursive = True
		self.ss = State(self)

		self.drawn = Drawn(self)

		self.forest = Forest(self)

	def generateGraph(self):
		self.spClass = 7
		self.k3cc = self.spClass - 2
		self.k2cc = self.spClass - 1
		self.k1cc = self.spClass - 1
		self.perms = ["".join([str(p) for p in perm]) for perm in Permutator([0,1,2,3,4,5,6]).results]
		self.pids = {}
		for i in range(len(self.perms)):
			self.pids[self.perms[i]] = i
		
		
if __name__ == "__main__":
	
	diagram = Diagram(6)
	
	print("pid: " + diagram.pids["03124"] + " | perm: " + diagram.perms[diagram.pids["03124"]])
	
	print("---")
