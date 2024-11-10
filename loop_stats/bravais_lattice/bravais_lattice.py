import numpy as np
from typing import Tuple, Union
from .typing import LatticeSize
from .lattice_coordinates import CoordinateTuple, LatticeCoordinate, to_lattice_coordinate
from .basis_vector import BasisVector, BasisVector3D, BasisVector2D


TOLERANCE: float = 1e-8


class BravaisLattice:
    def __init__(self,
                 basis: Tuple[BasisVector, ...],
                 size: Union[int, LatticeSize],
                 body_centered: bool = False,
                 xy_face_centered: bool = False,
                 yz_face_centered: bool = False,
                 xz_face_centered: bool = False,
                 **kwargs):
        if isinstance(size, int):
            size = tuple([size for _ in range(len(basis))])

        if len(basis) != len(size):
            raise ValueError(f"Error: size and basis dimension does not match [{len(size)} != {len(basis)}]")

        self._basis = []
        self._size = size
        if len(basis) == 2:
            self._basis = [BasisVector2D(x) for x in basis]
        elif len(basis) == 3:
            self._basis = [BasisVector3D(x) for x in basis]
        else:
            raise ValueError(f"Error: supports 2D/3D lattices only!")
        self._xyz = None
        self._lattice_type = None
        self._params = dict(body_centered=body_centered,
                            xy_face_centered=xy_face_centered,
                            yz_face_centered=yz_face_centered,
                            xz_face_centered=xz_face_centered)

    @property
    def ndim(self) -> int:
        return len(self._basis)

    @property
    def size(self) -> int:
        return np.prod(self._size)

    @property
    def shape(self) -> LatticeSize:
        return self._size

    @property
    def basis_x(self) -> BasisVector:
        return self._basis[0]

    @property
    def basis_y(self) -> BasisVector:
        return self._basis[1]

    @property
    def basis_z(self) -> BasisVector:
        if self.ndim == 2:
            raise ValueError(f"Error: basis z does not exists!")
        return self._basis[2]

    @property
    def body_centered(self) -> bool:
        return self._params.get('body_centered', False) if self.ndim == 3 else self.xy_face_centered

    @property
    def xy_face_centered(self) -> bool:
        return self._params.get('xy_face_centered', False)

    @property
    def yz_face_centered(self) -> bool:
        return self._params.get('yz_face_centered', False) if self.ndim == 3 else False

    @property
    def xz_face_centered(self) -> bool:
        return self._params.get('xz_face_centered', False) if self.ndim == 3 else False

    def check_coordinate(self, coordinate: LatticeCoordinate) -> bool:
        coordinate = to_lattice_coordinate(coordinate)
        if self.ndim == coordinate.ndim:
            if all([coordinate[i].is_integer for i in range(coordinate.ndim)]):
                return True

            if self.body_centered and not any([coordinate[i].is_integer for i in range(coordinate.ndim)]):
                return True

            x_check = (self.xy_face_centered or self.xz_face_centered) and not coordinate['x'].is_integer
            y_check = (self.xy_face_centered or self.yz_face_centered) and not coordinate['y'].is_integer

            check = (x_check or coordinate['x'].is_integer) and (y_check or coordinate['y'].is_integer)

            if self.ndim == 3:
                z_check = (self.xz_face_centered or self.yz_face_centered) and not coordinate['z'].is_integer
                check = check and (z_check or coordinate['z'].is_integer)
            return check
        return False

    def __getitem__(self, coordinate: Union[LatticeCoordinate, CoordinateTuple]) -> np.ndarray:
        coordinate = to_lattice_coordinate(coordinate)
        if self.check_coordinate(coordinate):
            coordinate = to_lattice_coordinate([coordinate[i].value % self._size[i] for i in range(self.ndim)])
            scaled = [self._basis[i] * coordinate[i].value
                      for i in range(self.ndim)]
            x = scaled[0]
            for y in scaled[1:]:
                x = x + y
            return x.to_array()
        raise IndexError(f"Error: invalid coordinate {coordinate}!")

    def __all_coord_list(self):
        data = list()
        tags = list()
        if self.ndim == 2:
            sx, sy = self._size
            for i in range(sx):
                for j in range(sy):
                    data.append(self[(i, j)])
                    tags.append(0)
                    if self.xy_face_centered:
                        data.append(self[(i + 0.5, j + 0.5)])
                        tags.append(2)
        else:
            sx, sy, sz = self._size
            for i in range(sx):
                for j in range(sy):
                    for k in range(sz):
                        data.append(self[(i, j, k)])
                        tags.append(0)
                        if self.body_centered:
                            data.append(self[(i + 0.5, j + 0.5, k + 0.5)])
                            tags.append(2)
                        if self.xy_face_centered:
                            data.append(self[(i + 0.5, j + 0.5, k)])
                            tags.append(1)
                        if self.yz_face_centered:
                            data.append(self[(i, j + 0.5, k + 0.5)])
                            tags.append(1)
                        if self.xz_face_centered:
                            data.append(self[(i+0.5, j, k+0.5)])
                            tags.append(1)
        self._xyz = np.array(data)
        self._lattice_type = np.array(tags)

    @property
    def xyz(self) -> np.ndarray:
        if self._xyz is None:
            self.__all_coord_list()
        return self._xyz

    @property
    def site_types(self) -> np.ndarray:
        if self._lattice_type is None:
            self.__all_coord_list()
        return self._lattice_type

