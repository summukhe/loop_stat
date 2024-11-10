from typing import Any, Tuple, Union, List
from abc import ABCMeta, abstractmethod
from .basis_vector import BasisVector
from .bravais_lattice import BravaisLattice, LatticeSize
from .lattice_coordinates import CoordinateTuple, LatticeCoordinate, to_lattice_coordinate


CoordinateType = Union[str, CoordinateTuple, LatticeCoordinate]


class LatticeInfo:
    __metaclass__ = ABCMeta

    @abstractmethod
    def keys(self) -> List[str]:
        raise NotImplemented

    @abstractmethod
    def get_attr(self, attr: str) -> Any:
        raise NotImplemented

    @abstractmethod
    def set_attr(self, attr: str, value: Any):
        raise NotImplemented

    @abstractmethod
    def update(self, attr: str, value: Any):
        raise NotImplemented

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplemented

    @abstractmethod
    def load_dict(self, **kwargs):
        raise NotImplemented


class LatticeInfoFactory:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_instance(self, **kwargs) -> LatticeInfo:
        raise NotImplemented


class BravaisSystem(BravaisLattice):
    def __init__(self,
                 basis: Tuple[BasisVector, ...],
                 size: Union[int, LatticeSize],
                 info_factory: LatticeInfoFactory,
                 body_centered: bool = False,
                 xy_face_centered: bool = False,
                 yz_face_centered: bool = False,
                 xz_face_centered: bool = False,
                 **kwargs
                 ):
        super(BravaisSystem, self).__init__(basis=basis,
                                            size=size,
                                            body_centered=body_centered,
                                            xy_face_centered=xy_face_centered,
                                            yz_face_centered=yz_face_centered,
                                            xz_face_centered=xz_face_centered,
                                            **kwargs)
        self._factory = info_factory
        self._info_list = dict()

    def info_at(self,
                coord: CoordinateType,
                **kwargs):
        coord = to_lattice_coordinate(coord)
        return self._info_list.get(coord, self._factory.get_instance(**kwargs))

    def info_update(self,
                    coord: CoordinateType,
                    attr: str,
                    value: Any,
                    **kwargs):
        coord = to_lattice_coordinate(coord)
        if coord not in self._info_list:
            self._info_list[coord] = self._factory.get_instance(**kwargs)
        self._info_list[coord].update(attr, value)




