from typing import Union, Sequence, Iterable, List, Tuple


ArrayLike = Union[Sequence[float], List[float], Tuple[float, ...], Iterable]

Array2D = Union[Sequence[float], Iterable, List[float], Tuple[float, float]]

Array3D = Union[Sequence[float], Iterable, List[float], Tuple[float, float, float]]

LatticeSize = Union[Tuple[int, int], Tuple[int, int, int]]

CoordinateTuple2D = Union[Tuple[int, int],
                          Tuple[float, float],
                          Tuple["OneAndHalfUnit", "OneAndHalfUnit"]]
CoordinateTuple3D = Union[Tuple[int, int, int],
                          Tuple[float, float],
                          Tuple["OneAndHalfUnit", "OneAndHalfUnit", "OneAndHalfUnit"]]

CoordinateTuple = Union[CoordinateTuple2D, CoordinateTuple3D]
