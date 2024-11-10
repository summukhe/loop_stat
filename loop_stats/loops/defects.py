import numpy as np
from typing import List, Union
from loop_stats.bravais_lattice.typing import CoordinateTuple, LatticeSize
from loop_stats.bravais_lattice import LatticeCoordinate
from loop_stats.bravais_lattice import to_lattice_coordinate


def validate_minimum_length(offsets: List[LatticeCoordinate]) -> bool:
    return len(offsets) >= 2


def validate_same_dimension_offsets(offsets: List[LatticeCoordinate]) -> bool:
    if len(offsets) > 0:
        ndim = len(offsets[0])
        return all([ndim == len(crd) for crd in offsets])
    return True


def validate_closed_cycle(offsets: List[LatticeCoordinate]) -> bool:
    if validate_minimum_length(offsets):
        start = to_lattice_coordinate(np.repeat(0, len(offsets[0])).tolist())
        end = start
        for crd in offsets:
            end = end + to_lattice_coordinate(crd)
        return start == end
    return True


def validate_unique_cycle(offsets: List[LatticeCoordinate]) -> bool:
    if validate_minimum_length(offsets):
        sequence = []
        start = to_lattice_coordinate(np.repeat(0, len(offsets[0])).tolist())
        for crd in offsets:
            start = start + to_lattice_coordinate(crd)
            sequence.append(start)
        return len(sequence) == len(set(sequence))
    return True


def validate_loop_defect(offsets: List[LatticeCoordinate]):
    offsets = [to_lattice_coordinate(crd) for crd in offsets]
    return (validate_minimum_length(offsets) and
            validate_same_dimension_offsets(offsets) and
            validate_closed_cycle(offsets) and
            validate_unique_cycle(offsets))


class FundamentalLoopDefect:
    def __init__(self,
                 offsets: List[LatticeCoordinate],
                 ):
        offsets = [to_lattice_coordinate(crd) for crd in offsets]
        if not validate_loop_defect(offsets):
            raise ValueError(f"Error: incomplete loop definition!")
        self._offsets = offsets

    @property
    def ndim(self):
        return self._offsets[0].ndim

    def __len__(self):
        return len(self._offsets)

    def __getitem__(self, item: int):
        return self._offsets[item]

    def __iter__(self):
        return self._offsets.__iter__()

    def to_string(self) -> str:
        return '->'.join([off.to_string() for off in self._offsets])

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def __hash__(self):
        return hash(self.to_string())

    def __eq__(self, other: "FundamentalLoopDefect"):
        return isinstance(other, FundamentalLoopDefect) and (str(self) == str(other))


def periodic_coordinate(coordinate: LatticeCoordinate,
                        lattice_boundary: LatticeSize = None
                        ) -> LatticeCoordinate:
    if (lattice_boundary is not None) and (len(coordinate) == len(lattice_boundary)):
        return to_lattice_coordinate([c % lattice_boundary[i] for i, c in enumerate(coordinate.to_list())])
    return coordinate


def generate_defect_coordinates(defect: FundamentalLoopDefect,
                                start_coord: Union[CoordinateTuple, LatticeCoordinate],
                                lattice_size: LatticeSize = None,
                                ) -> List[LatticeCoordinate]:
    start_coord = to_lattice_coordinate(start_coord)
    if defect.ndim != start_coord.ndim:
        raise ValueError(f"Error: defect incompatible with coordinate type!")
    return [periodic_coordinate(c + start_coord, lattice_size) for c in defect]


def anti_cycle(defect: FundamentalLoopDefect):
    n = len(defect)
    offsets = []
    for i in range(n):
        offset = to_lattice_coordinate([-entry if entry != 0 else entry
                                        for entry in defect[i].to_list()])
        offsets.append(offset)
    return FundamentalLoopDefect(offsets[::-1])


