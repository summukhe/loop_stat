import numpy as np
from typing import Tuple, Union, List
from loop_stats.bravais_lattice.typing import LatticeSize
from loop_stats.bravais_lattice import BravaisLattice
from loop_stats.bravais_lattice import BasisVector
from loop_stats.loops.defects import FundamentalLoopDefect


class BravaisLatticeWithLoopDefects(BravaisLattice):
    def __init__(self,
                 basis: Tuple[BasisVector, ...],
                 size: Union[int, LatticeSize],
                 body_centered: bool = False,
                 xy_face_centered: bool = False,
                 yz_face_centered: bool = False,
                 xz_face_centered: bool = False,
                 **kwargs
                 ):
        super(BravaisLatticeWithLoopDefects, self).__init__(basis=basis,
                                                            size=size,
                                                            body_centered=body_centered,
                                                            xy_face_centered=xy_face_centered,
                                                            yz_face_centered=yz_face_centered,
                                                            xz_face_centered=xz_face_centered,
                                                            **kwargs)
        self._info_list = np.zeros((self.size, self.ndim))
        self._loop_register = []

    def register_loop(self,
                      loops: Union[FundamentalLoopDefect, List[FundamentalLoopDefect]]):
        if not isinstance(loops, (list, tuple)):
            loops = [loops]

        for loop in loops:
            if (loop not in self._loop_register) and (loop.ndim == self.ndim):
                self._loop_register.append(loop)

    @property
    def known_loop_count(self) -> int:
        return len(self._loop_register)

    def registered_loop(self, item: int) -> FundamentalLoopDefect:
        return self._loop_register[item]


