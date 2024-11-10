import numpy as np
from abc import ABCMeta, abstractmethod
from .typing import ArrayLike, Array2D, Array3D
from typing import List, Tuple, Sequence, Union, Iterable


TOLERANCE: float = 1e-5


class BasisVector:
    __metaclass__ = ABCMeta

    @abstractmethod
    def ndim(self) -> int:
        raise NotImplemented

    @abstractmethod
    def __getitem__(self, item: Union[int, str]):
        raise NotImplemented

    @abstractmethod
    def __iter__(self):
        raise NotImplemented

    @abstractmethod
    def to_array(self) -> np.ndarray:
        raise NotImplemented

    def __eq__(self,
               other: "BasisVector",
               ):
        try:
            other = self.__class__(other)
        except ValueError as e:
            return False
        return (self.ndim == other.ndim) and bool(np.sum(np.square(self.to_array() - other.to_array())) < TOLERANCE)

    def __mul__(self,
                other: float,
                ) -> "BasisVector":
        v = self.to_array() * float(other)
        return self.__class__(v)

    def __add__(self,
                other: "BasisVector",
                ) -> "BasisVector":
        v1 = self.to_array()
        v2 = other.to_array()
        d = max(len(v1), len(v2))
        v = np.zeros(d)
        v[:len(v1)] = v[:len(v1)] + v1
        v[:len(v2)] = v[:len(v2)] + v2
        if other.ndim > self.ndim:
            return other.__class__(v)
        else:
            return self.__class__(v)

    def __sub__(self,
                other: "BasisVector") -> "BasisVector":
        v1 = self.to_array()
        v2 = other.to_array()
        d = max(len(v1), len(v2))
        v = np.zeros(d)
        v[:len(v1)] = v[:len(v1)] + v1
        v[:len(v2)] = v[:len(v2)] - v2
        if other.ndim > self.ndim:
            return other.__class__(v)
        else:
            return self.__class__(v)


class BasisVector2D(BasisVector):
    def __init__(self,
                 v: Array2D,
                 ):
        if isinstance(v, BasisVector2D):
            v = v.to_array()
        v = np.squeeze(np.array(v).astype(float))
        if (v.ndim != 1) or (v.shape[0] != 2):
            raise ValueError(f"Error: expect 2D array, received {v.shape}")
        super(BasisVector2D, self).__init__()
        self._v = v

    @property
    def x(self) -> float:
        return float(self._v[0])

    @property
    def y(self) -> float:
        return float(self._v[1])

    def __iter__(self):
        for x in self._v:
            yield x

    def __getitem__(self, item: Union[int, str]) -> float:
        if isinstance(item, str) and (item.lower() in ['x', 'y']):
            item = 0 if item.lower() == 'x' else 1

        if not isinstance(item, int):
            raise ValueError(f"Error: items can only be accessed as integer index (0, 1) / string literal (x, y)!")
        return float(self._v[item])

    def __len__(self) -> int:
        return len(self._v)

    @property
    def ndim(self) -> int:
        return 2

    @property
    def norm(self) -> float:
        return np.sum(np.square(self._v))

    def to_array(self) -> np.ndarray:
        return self._v.copy()

    def __repr__(self):
        return f'(x={self.x:.3f}, y={self.y:.3f})'


class BasisVector3D(BasisVector):
    def __init__(self,
                 v: Array3D,
                 ):
        if isinstance(v, BasisVector):
            v = v.to_array()
        v = np.squeeze(np.array(v).astype(float))
        if len(v) < 3:
            v_ = np.zeros(3)
            v_[:len(v)] = v[:]
            v = v_
        if (v.ndim != 1) or (v.shape[0] != 3):
            raise ValueError(f"Error: expect 2D array, received {v.shape}")
        super(BasisVector3D, self).__init__()
        self._v = v

    @property
    def ndim(self) -> int:
        return 3

    @property
    def x(self) -> float:
        return float(self._v[0])

    @property
    def y(self) -> float:
        return float(self._v[1])

    @property
    def z(self) -> float:
        return float(self._v[2])

    def __iter__(self):
        for x in self._v:
            yield x

    def __getitem__(self, item: Union[ int, str ]) -> float:
        if isinstance(item, str) and (item.lower() in ['x', 'y', 'z']):
            item = dict(x=0, y=1, z=2)[str(item).lower()]
        if not isinstance(item, int):
            raise ValueError(f"Error: items can only be accessed as integer index (0, 1) / string literal (x, y)!")
        return float(self._v[item])

    def __len__(self) -> int:
        return len(self._v)

    def to_array(self):
        return self._v.copy()

    def __repr__(self):
        return f"(x={self.x:.3f}, y={self.y:.3f}, z={self.z:.3f})"


def to_basis_vector(x: ArrayLike) -> BasisVector:
    d = len(x)
    if d == 2:
        return BasisVector2D(list(x))
    elif d == 3:
        return BasisVector3D(list(x))
    raise ValueError(f"Error: supports 2D/3D basis only, received {d}D vector!")

