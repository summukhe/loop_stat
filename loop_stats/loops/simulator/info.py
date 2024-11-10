from typing import Union
from loop_stats.bravais_lattice import LatticeInfo, LatticeInfoFactory


class Defect3DInfo(LatticeInfo):
    __slot__ = ['_x', '_y', '_z']

    def __init__(self,
                 x: int = 0,
                 y: int = 0,
                 z: int = 0,
                 **kwargs):
        self._x = x
        self._y = y
        self._z = z

    def keys(self):
        return ['x', 'y', 'z']

    def get_attr(self, attr: str) -> Union[int, None]:
        if attr == 'x':
            return self._x
        elif attr == 'y':
            return self._y
        elif attr == 'z':
            return self._z

    def set_attr(self, attr: str, value: int):
        if attr == 'x':
            self._x = value
        elif attr == 'y':
            self._y = value
        elif attr == 'z':
            self._z = value

    def update(self, attr: str, value: int):
        if attr == 'x':
            self._x += value
        elif attr == 'y':
            self._y += value
        elif attr == 'z':
            self._z += value

    def to_dict(self) -> dict:
        return dict(x=self._x, y=self._y, z=self._z)

    def load_dict(self, **kwargs):
        if 'x' in kwargs:
            self._x = int(kwargs.get('x'))
        if 'y' in kwargs:
            self._y = int(kwargs.get('y'))
        if 'z' in kwargs:
            self._z = int(kwargs.get('z'))


class Defect2DInfo(LatticeInfo):
    __slot__ = [ '_x', '_y']

    def __init__(self,
                 x: int = 0,
                 y: int = 0,
                 **kwargs):
        self._x = x
        self._y = y

    def keys(self):
        return ['x', 'y']

    def get_attr(self, attr: str) -> Union[int, None]:
        if attr == 'x':
            return self._x
        elif attr == 'y':
            return self._y

    def set_attr(self, attr: str, value: int):
        if attr == 'x':
            self._x = value
        elif attr == 'y':
            self._y = value

    def update(self, attr: str, value: int):
        if attr == 'x':
            self._x += value
        elif attr == 'y':
            self._y += value

    def to_dict(self) -> dict:
        return dict(x=self._x, y=self._y)

    def load_dict(self, **kwargs):
        if 'x' in kwargs:
            self._x = int(kwargs.get('x'))
        if 'y' in kwargs:
            self._y = int(kwargs.get('y'))


class DefectInfoFactory(LatticeInfoFactory):
    def __init__(self,
                 dim: int,
                 ):
        if dim not in (2, 3):
            raise ValueError(f"Error: only 2/3D system supported, got [{dim}]!")
        self._ndim = dim

    @property
    def ndim(self) -> int:
        return self._ndim

    def get_instance(self, **kwargs) -> LatticeInfo:
        if self.ndim == 2:
            return Defect2DInfo(**kwargs)
        elif self.ndim == 3:
            return Defect3DInfo(**kwargs)
        raise RuntimeError(f"Error: system dimension must be 2 or 3!")



