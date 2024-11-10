import re
from typing import Union, List
from abc import ABCMeta, abstractmethod
from loop_stats.bravais_lattice.typing import CoordinateTuple, CoordinateTuple3D, CoordinateTuple2D


TOLERANCE = 1e-5


class OneAndHalfUnit:
    def __init__(self,
                 unit: Union[int, float, "OneAndHalfUnit"],
                 ):
        u_ = int(unit)
        h_ = (unit % 1.) >= 0.5 - TOLERANCE
        self._u = u_
        self._h = h_

    @property
    def is_integer(self) -> bool:
        return not self._h

    def __repr__(self):
        return f'{self._u}.5' if self._h else f'{self._u}'

    def __int__(self) -> int:
        return self._u

    def __float__(self) -> float:
        return self.value

    def __mod__(self, other) -> float:
        return self.value % other

    def __add__(self, other) -> "OneAndHalfUnit":
        return OneAndHalfUnit(OneAndHalfUnit(other).value + self.value)

    def __mul__(self, other) -> "OneAndHalfUnit":
        return OneAndHalfUnit(float(other) * self.value)

    @property
    def value(self) -> float:
        return self._u + self._h * 0.5

    def __eq__(self, other: Union["OneAndHalfUnit", float, int]):
        other_ = OneAndHalfUnit(other)
        return (self._u == other_._u) and (self._h == other_._h)


class LatticeCoordinate:
    __metaclass__ = ABCMeta

    def __len__(self):
        return self.ndim

    @property
    @abstractmethod
    def ndim(self) -> int:
        raise NotImplemented

    @abstractmethod
    def __getitem__(self, item: Union[int, str]) -> OneAndHalfUnit:
        raise NotImplemented

    @abstractmethod
    def __add__(self, other: "LatticeCoordinate") -> "LatticeCoordinate":
        raise NotImplemented

    @abstractmethod
    def __mul__(self, other: float) -> "LatticeCoordinate":
        raise NotImplemented

    def to_string(self):
        m = ','.join([str(self[i]) for i in range(len(self))])
        return f'({m})'

    def __hash__(self):
        return hash(self.to_string())

    def __repr__(self):
        return self.to_string()

    def __str__(self):
        return self.to_string()

    def __eq__(self, other: Union["LatticeCoordinate", CoordinateTuple]) -> bool:
        other = to_lattice_coordinate(other)
        if self.ndim != other.ndim:
            return False
        return all([self[i] == other[i] for i in range(self.ndim)])

    def __ne__(self, other: Union["LatticeCoordinate", CoordinateTuple]) -> bool:
        return not (self == other)

    def to_list(self) -> List[float]:
        return [self[i].value for i in range(len(self))]


class LatticeCoordinate2D(LatticeCoordinate):
    def __init__(self,
                 data: CoordinateTuple2D,
                 ):
        if len(data) != 2:
            raise ValueError(f"Error: expects 2D coordinates!")
        x, y = data
        self._x = OneAndHalfUnit(x)
        self._y = OneAndHalfUnit(y)

    def __getitem__(self, item: Union[str, int]):
        if isinstance(item, int) and (item in [0, 1]):
            item = 'x' if item == 0 else 'y'
        item = str(item)
        if item.lower() == 'x':
            return self.x
        elif item.lower() == 'y':
            return self.y
        raise IndexError(f"Error invalid item access {item}!")

    @property
    def x(self) -> OneAndHalfUnit:
        return self._x

    @property
    def y(self) -> OneAndHalfUnit:
        return self._y

    @property
    def ndim(self) -> int:
        return 2

    def __add__(self, other: Union[CoordinateTuple2D, "LatticeCoordinate2D"]) -> "LatticeCoordinate2D":
        other_ = to_lattice_coordinate(other)
        return LatticeCoordinate2D((self.x + other_.x, self.y + other_.y))

    def __mul__(self, other: float) -> "LatticeCoordinate2D":
        return LatticeCoordinate2D((self.x * other, self.y * other))


class LatticeCoordinate3D(LatticeCoordinate):
    def __init__(self,
                 data: CoordinateTuple3D,
                 ):
        if len(data) != 3:
            raise ValueError(f"Error: expects 3D coordinates!")
        x, y, z = data
        self._x = OneAndHalfUnit(x)
        self._y = OneAndHalfUnit(y)
        self._z = OneAndHalfUnit(z)

    def __getitem__(self, item: Union[str, int]):
        if isinstance(item, int) and (item in [0, 1, 2]):
            item = dict({0: 'x', 1: 'y', 2: 'z'})[item]
        item = str(item)
        if item.lower() == 'x':
            return self.x
        elif item.lower() == 'y':
            return self.y
        elif item.lower() == 'z':
            return self.z
        raise IndexError(f"Error invalid item access {item}!")

    @property
    def x(self) -> OneAndHalfUnit:
        return self._x

    @property
    def y(self) -> OneAndHalfUnit:
        return self._y

    @property
    def z(self) -> OneAndHalfUnit:
        return self._z

    @property
    def ndim(self) -> int:
        return 3

    def __add__(self, other: Union[CoordinateTuple3D, "LatticeCoordinate3D"]) -> "LatticeCoordinate3D":
        other_ = to_lattice_coordinate(other)
        return LatticeCoordinate3D((self.x + other_.x, self.y + other_.y, self.z + other_.z))

    def __mul__(self, other: float) -> "LatticeCoordinate3D":
        return LatticeCoordinate3D((self.x * other, self.y * other, self.z * other))


def to_lattice_coordinate(x: Union[str, LatticeCoordinate, CoordinateTuple]) -> LatticeCoordinate:
    if isinstance(x, LatticeCoordinate):
        return x

    if isinstance(x, str):
        pattern = re.compile(r'\((?:-?\d+\.?[5]?,){1,2}-?\d+\.?[5]?\)')
        if not pattern.match(x):
            raise ValueError(f"Error: invalid string format [{x}]!")
        x = tuple([float(fld) for fld in x[1:-1].split(",")])

    if len(x) == 2:
        return LatticeCoordinate2D(x)
    elif len(x) == 3:
        return LatticeCoordinate3D(x)
    raise ValueError(f"Error: expects 2/3D tuple found {len(x)}!")

