import numpy as np
from tqdm import tqdm
from typing import Tuple, Union
from .typing import LatticeSize
from .lattice_coordinates import (CoordinateTuple,
                                  LatticeCoordinate,
                                  to_lattice_coordinate,
                                  check_coordinate_validity)
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
                 show_progress: bool = True,
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
        self._coord = None
        self._params = dict(body_centered=body_centered,
                            xy_face_centered=xy_face_centered,
                            yz_face_centered=yz_face_centered,
                            xz_face_centered=xz_face_centered)
        self.__initialize_coordinates(show_progress)

    @property
    def ndim(self) -> int:
        return len(self._basis)

    @property
    def size(self) -> int:
        return self._xyz.shape[0]

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
        return check_coordinate_validity(coordinate,
                                         lattice_dim=self.ndim,
                                         lattice_size=self.shape,
                                         body_centered=self.body_centered,
                                         xy_face_centered=self.xy_face_centered,
                                         yz_face_centered=self.yz_face_centered,
                                         xz_face_centered=self.xz_face_centered)

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

    def __initialize_coordinates(self, show_prgress: bool = True):
        xyz = list()
        tags = list()
        coordinates = list()
        pbar = None
        if self.ndim == 2:
            sx, sy = self._size
            if show_prgress:
                pbar = tqdm(total=sx * sy, position=0, leave=True, desc="building lattice")
            for i in range(sx):
                for j in range(sy):
                    c = (i, j)
                    xyz.append(self[c])
                    tags.append(0)
                    coordinates.append(c)
                    if self.xy_face_centered:
                        c = (i + 0.5, j + 0.5)
                        xyz.append(self[c])
                        tags.append(2)
                        coordinates.append(c)
                    if pbar:
                        pbar.update(1)
        else:
            sx, sy, sz = self._size
            if show_prgress:
                pbar = tqdm(total=sx * sy, position=0, leave=True, desc="building lattice")
            for i in range(sx):
                for j in range(sy):
                    for k in range(sz):
                        c = (i, j, k)
                        xyz.append(self[c])
                        tags.append(0)
                        coordinates.append(c)
                        if self.body_centered:
                            c = (i + 0.5, j + 0.5, k + 0.5)
                            xyz.append(self[c])
                            tags.append(2)
                            coordinates.append(c)
                        if self.xy_face_centered:
                            c = (i + 0.5, j + 0.5, k)
                            xyz.append(self[c])
                            tags.append(1)
                            coordinates.append(c)
                        if self.yz_face_centered:
                            c = (i, j + 0.5, k + 0.5)
                            xyz.append(self[c])
                            tags.append(1)
                            coordinates.append(c)
                        if self.xz_face_centered:
                            c = (i+0.5, j, k+0.5)
                            xyz.append(self[c])
                            tags.append(1)
                            coordinates.append(c)
                        if pbar:
                            pbar.update(1)
        if pbar:
            pbar.close()
        self._xyz = np.array(xyz)
        self._lattice_type = np.array(tags)
        self._coord = np.array(coordinates)

    @property
    def xyz(self) -> np.ndarray:
        if self._xyz is None:
            self.__initialize_coordinates()
        return self._xyz

    @property
    def site_types(self) -> np.ndarray:
        if self._lattice_type is None:
            self.__initialize_coordinates()
        return self._lattice_type

    @property
    def coordinate(self) -> np.ndarray:
        if self._coord is None:
            self.__initialize_coordinates()
        return self._coord

