from typing import Union, Sequence, Iterable, List, Tuple, Annotated


ArrayLike = Union[Sequence[float], List[float], Tuple[float, ...], Iterable]

Array2D = Union[Annotated[Sequence[float], 2], Iterable, Annotated[List[float], 2], Tuple[float, float]]

Array3D = Union[Annotated[Sequence[float], 2], Iterable, Annotated[List[float], 2], Tuple[float, float, float]]

LatticeSize = Union[Tuple[int, int], Tuple[int, int, int], Annotated[List[int], 2], Annotated[List[int], 3]]

CoordinateTuple2D = Union[Annotated[List[int], 2],
                          Annotated[List[float], 2],
                          Tuple[int, int],
                          Tuple[float, float],
                          Tuple["OneAndHalfUnit", "OneAndHalfUnit"]]
CoordinateTuple3D = Union[Annotated[List[int], 3],
                          Annotated[List[float], 3],
                          Tuple[int, int, int],
                          Tuple[float, float],
                          Tuple["OneAndHalfUnit", "OneAndHalfUnit", "OneAndHalfUnit"]]

CoordinateTuple = Union[CoordinateTuple2D, CoordinateTuple3D]
