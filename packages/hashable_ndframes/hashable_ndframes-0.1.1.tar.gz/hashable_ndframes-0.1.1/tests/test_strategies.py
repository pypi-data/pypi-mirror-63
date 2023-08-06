from typing import Any
from typing import Optional

import hypothesis
from hypothesis import assume
from hypothesis import given
from hypothesis.extra.numpy import scalar_dtypes
from hypothesis.strategies import composite
from hypothesis.strategies import integers
from hypothesis.strategies import just
from hypothesis.strategies import lists
from hypothesis.strategies import none
from hypothesis.strategies import SearchStrategy
from hypothesis.strategies import text
from numpy import dtype
from numpy import ndarray
from pandas import concat
from pandas import DataFrame
from pandas import Index
from pandas import RangeIndex
from pandas import Series
from pandas._libs.tslibs import OutOfBoundsDatetime


lengths = integers(0, 5)


@composite
def arrays(draw: Any, lengths: SearchStrategy[int] = lengths) -> ndarray:
    dtype = draw(scalar_dtypes())
    length = draw(lengths)
    return draw(hypothesis.extra.numpy.arrays(dtype, length))


@given(array=arrays())
def test_arrays(array: ndarray) -> None:
    assert isinstance(array, ndarray)


names = none() | text()


@given(name=names)
def test_names(name: Optional[str]) -> None:
    assert isinstance(hash(name), int)


@composite
def range_indices(
    draw: Any, lengths: SearchStrategy[int] = lengths,
) -> RangeIndex:
    length = draw(lengths)
    name = draw(names)
    return RangeIndex(length, name=name)


@given(index=range_indices())
def test_range_indices(index: RangeIndex) -> None:
    assert isinstance(index, RangeIndex)


@composite
def main_indices(draw: Any, lengths: SearchStrategy[int] = lengths) -> Index:
    data = draw(arrays(lengths=lengths))
    assume(data.dtype != dtype(">M8[ns]"))
    name = draw(names)
    try:
        return Index(data, name=name)
    except OutOfBoundsDatetime:
        assume(False)


@given(index=main_indices())
def test_main_indices(index: Index) -> None:
    assert isinstance(index, Index)


def indices(lengths: SearchStrategy[int] = lengths) -> SearchStrategy[Index]:
    return range_indices(lengths=lengths) | main_indices(lengths=lengths)


@given(index=indices())
def test_indices(index: Index) -> None:
    assert isinstance(index, Index)


@composite
def series(draw: Any, indices: SearchStrategy[int] = indices()) -> None:
    index = draw(indices)
    data = draw(arrays(lengths=just(len(index))))
    name = draw(names)
    try:
        return Series(data, index=index, name=name)
    except OutOfBoundsDatetime:
        assume(False)


@given(series=series())
def test_series(series: Series) -> None:
    assert isinstance(series, Series)


@composite
def dataframes(
    draw: Any,
    num_rows: SearchStrategy[int] = lengths,
    num_cols: SearchStrategy[int] = lengths,
) -> DataFrame:
    num_row = draw(num_rows)
    index = draw(indices(lengths=just(num_row)))
    num_col = draw(num_cols)
    assume(num_col >= 1)
    all_series = draw(
        lists(series(indices=just(index)), min_size=num_col, max_size=num_col),
    )
    return concat(all_series, axis=1)


@given(df=dataframes())
def test_dataframes(df: DataFrame) -> None:
    assert isinstance(df, DataFrame)
