import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt
from .bravais_lattice import BravaisLattice


def plot_lattice_grid(lattice: BravaisLattice,
                      color_map: Tuple[str, ...] = None,
                      figure_size: Tuple[float, float] = (10, 10),
                      to_plot: bool = True,
                      ):
    xyz, coordinate_type = lattice.xyz, lattice.site_types
    unique_types = np.unique(coordinate_type)
    if (color_map is None) or (len(unique_types) != len(color_map)):
        color_map = [ '#1f78b4', '#33a02c', '#e31a1c',
                      '#ff7f00', '#6a3d9a', '#b15928',
                      '#a6cee3', '#b2df8a', '#fb9a99',
                      '#fdbf6f', '#cab2d6', '#ffff99' ]

    colors = [color_map[c] for c in coordinate_type]

    fig = plt.figure(figsize=figure_size)
    if xyz.shape[-1] == 2:
        ax = fig.add_subplot()
        ax.scatter(xyz[:, 0], xyz[:, 1],
                   s=(coordinate_type + 1) * 10,
                   color=colors)
        ax.axis('equal')
    elif xyz.shape[-1] == 3:
        ax = fig.add_subplot(projection='3d')
        ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2],
                   s=(coordinate_type + 1) * 10,
                   color=colors)
        ax.axis('equal')
    else:
        raise RuntimeError(f"Error: unknown configuration with {xyz.shape}!")

    if not to_plot:
        return fig, ax
    plt.show()

