import threading
from common import *
from time import time
import random


thcc = 8
results = [0]*thcc

def do_cube(thx):
	r = 0
	for i in range(1000000):
		r += random.randint(0,20)**3
		#r = i**3
		#print("["+str(thx)+"] "+str(r))
	#results[thx] += r
		
startTime = time()
for thx in range(thcc):
	do_cube(thx)
sync_time = time() - startTime

threads = [None]*thcc
startTime = time()
for thx in range(thcc):
	threads[thx] = threading.Thread(target=do_cube, args=(thx,))
for thx in range(thcc):
	threads[thx].start()
for thx in range(thcc):
	threads[thx].join()
async_time = time() - startTime

print("[sync:"+tstr(sync_time)+"]")
print("[async:"+tstr(async_time)+"]")
print("Done!")
print(results)
