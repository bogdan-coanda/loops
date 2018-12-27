import pstats
import sys

from pstats import SortKey
p = pstats.Stats(sys.argv[1])
print("\n\n--- [CUMULATIVE TIME] ---\n")
p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(10)
print("\n\n--- [INTERNAL TIME] ---\n")
p.strip_dirs().sort_stats(SortKey.TIME).print_stats(10)
print("\n\n--- [CALL COUNT] ---\n")
p.strip_dirs().sort_stats(SortKey.CALLS).print_stats(10)
print("\n\n--- [PRIMITIVE CALL COUNT] ---\n")
p.strip_dirs().sort_stats(SortKey.PCALLS).print_stats(10)
