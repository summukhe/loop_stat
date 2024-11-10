from typing import List, Union, Callable

import networkx as nx
import numpy as np
from tqdm import tqdm

from loop_stats.bravais_lattice import BravaisLattice
from loop_stats.bravais_lattice import (LatticeCoordinate,
                                        check_coordinate_validity,
                                        to_lattice_coordinate)
from loop_stats.bravais_lattice.typing import CoordinateTuple
from loop_stats.loops.defects import FundamentalLoopDefect, generate_defect_coordinates


class LatticeCoordinateValidityChecker:
    def __init__(self, lattice: BravaisLattice):
        self.config = dict(lattice_dim=lattice.ndim,
                           lattice_size=lattice.shape,
                           body_centered=lattice.body_centered,
                           xy_face_centered=lattice.xy_face_centered,
                           yz_face_centered=lattice.yz_face_centered,
                           xz_face_centered=lattice.xz_face_centered)

    def validate(self,
                 coord: Union[CoordinateTuple, LatticeCoordinate],
                 ) -> bool:
        return check_coordinate_validity(coord, **self.config)

    def __call__(self,
                 coord: Union[CoordinateTuple, LatticeCoordinate],
                 ) -> bool:
        return self.validate(coord)


def independent_node_partition(lattice: BravaisLattice,
                               loop_group: List[FundamentalLoopDefect],
                               coordinate_checker: Union[Callable, LatticeCoordinateValidityChecker] = None,
                               ):
    if coordinate_checker is None:
        coordinate_checker = LatticeCoordinateValidityChecker(lattice)
    valid_nodes = []
    coord_index = dict()
    counter = 0
    for i in tqdm(range(lattice.size), desc="Building Lattice Graph"):
        c = to_lattice_coordinate(lattice.coordinate[i])
        if coordinate_checker(c):
            coord_index[c] = (counter, i)
            counter = counter + 1
            valid_nodes.append(i)

    neighbor_edges = []

    for c in tqdm(coord_index, desc="Building Neighborhood Graph"):
        current_index = coord_index[c][1]
        lattice_neighbors = []
        for d in loop_group:
            neighbors = generate_defect_coordinates(d, c, lattice_size=lattice.shape)
            lattice_neighbors += [coord_index.get(c_, (-1, -1))[1] for c_ in neighbors]
        lattice_neighbors = [(current_index, j) for j in np.unique(lattice_neighbors) if j >= 0 and j > current_index]
        neighbor_edges += lattice_neighbors

    g = nx.Graph()
    g.add_nodes_from(valid_nodes)
    g.add_edges_from(neighbor_edges)
    colors = nx.greedy_color(g)
    uniq_colors = np.unique(list(colors.values()))
    node_partitions = list()
    for c in uniq_colors:
        node_partitions.append([k for k in colors if colors[k] == c])
    return node_partitions
