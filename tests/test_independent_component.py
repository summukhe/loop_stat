import numpy as np
from loop_stats.bravais_lattice import get_basis_pair
from loop_stats.bravais_lattice import BravaisLattice
from loop_stats.loops import FundamentalLoopDefect, anti_cycle
from loop_stats.loops.simulator import independent_node_partition


if __name__ == "__main__":
    lattice_type = "D2"
    lattice_size = 48
    lattice_params = dict(theta=np.pi / 3,
                          alpha=np.pi / 3)
    bases, params = get_basis_pair(lattice_type, **lattice_params)
    bl = BravaisLattice(bases, size=lattice_size, **params)
    loop1 = FundamentalLoopDefect([(0, 1), (1, 0), (0, -1), (-1, 0)])
    loop2 = anti_cycle(loop1)
    colors = independent_node_partition(bl, [loop1, loop2])
    print(f"Number of colors, {len(colors)}")
    print(f"Partitions: {[len(p) for p in colors]}")
