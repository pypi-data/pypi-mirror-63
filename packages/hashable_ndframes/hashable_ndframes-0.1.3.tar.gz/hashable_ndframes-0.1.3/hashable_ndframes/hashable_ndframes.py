from typing import Type

from numpy import ndarray
from pandas import DataFrame
from pandas import Index
from pandas import Series


class HashableNdarray(ndarray):
    """A subclass of ndarray which is hashable."""

    def __hash__(self: "HashableNdarray") -> int:
        return hash(self.tobytes())


class _IndexStore:
    """A hashable object designed to store Indices. It is well-known that
    Indices are not directly subclassable.

    (see: https://github.com/pandas-dev/pandas/issues/15258)
    """

    def __init__(self: "_IndexStore", index: Index) -> None:
        self._index = index

    def __hash__(self: "_IndexStore") -> int:
        return hash(
            (
                type(self._index),
                self._index.to_numpy().view(HashableNdarray),
                self._index.name,
            ),
        )


class HashableSeries(Series):
    """A subclass of Series which is hashable."""

    @property
    def _constructor(self: "HashableSeries") -> Type["HashableSeries"]:
        return HashableSeries

    @property
    def _constructor_expanddim(
        self: "HashableSeries",
    ) -> Type["HashableDataFrame"]:
        return HashableDataFrame

    def __hash__(self: "HashableSeries") -> int:
        return hash(
            (
                type(self),
                self.to_numpy().view(HashableNdarray),
                _IndexStore(self.index),
                self.dtype,
                self.name,
            ),
        )


class HashableDataFrame(DataFrame):
    """A subclass of DataFrame which is hashable."""

    @property
    def _constructor(self: "HashableDataFrame") -> Type["HashableDataFrame"]:
        return HashableDataFrame

    @property
    def _constructor_sliced(
        self: "HashableDataFrame",
    ) -> Type["HashableSeries"]:
        return HashableSeries

    def __hash__(self: "HashableDataFrame") -> int:
        return hash(
            (
                type(self),
                self.to_numpy().view(HashableNdarray),
                _IndexStore(self.index),
                _IndexStore(self.columns),
                HashableSeries(self.dtypes),
            ),
        )
