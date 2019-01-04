import pstats
import sys

p = pstats.Stats('__cProfile__')
print("\n\n--- [CUMULATIVE TIME] ---\n")
p.strip_dirs().sort_stats(2).print_stats(10)
print("\n\n--- [INTERNAL TIME] ---\n")
p.strip_dirs().sort_stats(1).print_stats(10)
print("\n\n--- [CALL COUNT] ---\n")
p.strip_dirs().sort_stats(0).print_stats(10)
print("\n\n--- [INTERNAL TIME :: CALLERS] ---\n")
p.strip_dirs().sort_stats(1).print_callers(10)

