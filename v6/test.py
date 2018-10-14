from superperms import *
from node import *
from common import *

self_spClass = 6
self_spgen = SPGenerator("".join([str(x) for x in range(self_spClass)]))
self_nodes = [Node(i, self_spgen.perms[i], self_spgen.addrs[i]) for i in range(len(self_spgen.perms))]

self_nodeByPerm = {}
self_nodeByAddress = {}		
for node in self_nodes:
	self_nodeByPerm[node.perm] = node
	self_nodeByAddress[node.address] = node
