import pstats
import sys

ps = [pstats.Stats(file) for file in [
	'__cProfile_c2_1__', '__cProfile_c2_2__', '__cProfile_c2_3__',
	'__cProfile_gt_1__', '__cProfile_gt_2__', '__cProfile_gt_3__']] 

print("\n\n--- [CUMULATIVE TIME] ---\n")
for p in ps:
	p.strip_dirs().sort_stats(2).print_stats(10)
print("\n\n--- [INTERNAL TIME] ---\n")
for p in ps:
	p.strip_dirs().sort_stats(1).print_stats(10)
print("\n\n--- [CALL COUNT] ---\n")
for p in ps:
	p.strip_dirs().sort_stats(0).print_stats(10)
print("\n\n--- [INTERNAL TIME :: CALLERS] ---\n")
for p in ps:
	p.strip_dirs().sort_stats(1).print_callers(10)
print("\n\n--- [INTERNAL TIME :: CALLEES] ---\n")
for p in ps:
	p.strip_dirs().sort_stats(1).print_callees(10)

