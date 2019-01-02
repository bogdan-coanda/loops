from diagram import *
from uicanvas import *
from common import *
from measurement import *
from itertools import chain
from time import time
from collections import defaultdict
from random import *


if __name__ == "__main__":
	
	diagram = Diagram(8, 1)
						
	mx = Measurement(diagram)		
	mx.reduce(False)
	
	KillingField.assessAllLoops(diagram)
	
	print(f"[{tstr(time() - diagram.startTime):>11}] {mx}")
	
	
	# === #
	'''
	start_grx = sorted(groupby([l for l in diagram.loops if l.availabled], K = lambda l: len(l.killingField), G = lambda g: len(g)).items())
	print("---")
	# print("---\nkilling field size: matching loops count | before ("+str(len(start_grx))+"):\n"+"\n".join([str(x[0])+":"+str(x[1]) for x in start_grx]))

	for index, loop in enumerate(diagram.loops):
		if loop.availabled:

			diagram.extendLoop(loop)
			
			kfRemoves = []
			kfRecalcs = []
		
			kfRemovedLoops = []
			kfPreviousFields = []
			
			# for each dead loop
			for affected_loop in loop.extension_result.affected_loops:
				# remove it from its killing field :: loops :: killing fields
				for kf_loop in affected_loop.killingField:
					if kf_loop.availabled: # only update still available killing field :: loops
						kf_loop.killingField.remove(affected_loop)
						kfRemoves.append(kf_loop.killingField)
						kfRemovedLoops.append((kf_loop.killingField, affected_loop))
						
			for node in loop.extension_result.new_chain.avnodes:
				kfRecalcs.append(node.loop.killingField)
				kfPreviousFields.append((node.loop.killingField, node.loop.killingField.field))
				node.loop.killingField.regenerate()
			
			print(f"[{index}/{len(diagram.loops)}] kf: {len(loop.killingField)} | removes: {len(kfRemoves)} (uniq:{len(list(set(kfRemoves)))}) | recalcs: {len(kfRecalcs)} (uniq:{len(set(kfRecalcs))}) | redones: {len(set(kfRecalcs).intersection(kfRemoves))} | {loop}")
			
			assert set(loop.extension_result.affected_loops) == set(list(loop.killingField.field) + [loop])
				
			for l in diagram.loops:
				if l.availabled:
					l.killingField.assess()
			
			grx = sorted(groupby([l for l in diagram.loops if l.availabled], K = lambda l: len(l.killingField), G = lambda g: len(g)).items())
			# print("\nkilling field size: matching loops count | after extend ("+str(len(grx))+"):\n"+"\n".join([str(x[0])+":"+str(x[1]) for x in grx]))
			
			diagram.collapseBack(loop)
			
			# revert to previous killing fields (mandatory recalcs before removes)
			for kf, field in kfPreviousFields:
				kf.field = field
					
			for kf, l in kfRemovedLoops:
				kf.add(l)		
		
			for l in diagram.loops:
				if l.availabled:
					l.killingField.assess()
			
			# print(f"\ncollapsed back {loop}")
			
			grx = sorted(groupby([l for l in diagram.loops if l.availabled], K = lambda l: len(l.killingField), G = lambda g: len(g)).items())
			assert grx == start_grx
			
	#diagram.extendLoop(diagram.nodeByAddress['0000003'].loop)
	#show(diagram)
	'''
	
