import numpy as np
from loop_stats.bravais_lattice import get_basis_pair
from loop_stats.bravais_lattice import BravaisLattice
from loop_stats.bravais_lattice import plot_lattice_grid


if __name__ == "__main__":
    lattice_type = "C2hS"
    lattice_size = 6
    lattice_params = dict(theta=np.pi / 3,
                          alpha=np.pi / 3)
    bases, params = get_basis_pair(lattice_type, **lattice_params)
    bl = BravaisLattice(bases, size=lattice_size, **params)
    if bl.ndim == 2:
        print(bl.basis_x, bl.basis_y)
    else:
        print(bl.basis_x, bl.basis_y, bl.basis_z)

    plot_lattice_grid(bl)
